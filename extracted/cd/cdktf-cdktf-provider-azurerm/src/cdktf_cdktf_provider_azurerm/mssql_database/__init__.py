r'''
# `azurerm_mssql_database`

Refer to the Terraform Registry for docs: [`azurerm_mssql_database`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database).
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


class MssqlDatabase(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabase",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database azurerm_mssql_database}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        server_id: builtins.str,
        auto_pause_delay_in_minutes: typing.Optional[jsii.Number] = None,
        collation: typing.Optional[builtins.str] = None,
        create_mode: typing.Optional[builtins.str] = None,
        creation_source_database_id: typing.Optional[builtins.str] = None,
        elastic_pool_id: typing.Optional[builtins.str] = None,
        enclave_type: typing.Optional[builtins.str] = None,
        geo_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MssqlDatabaseIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        import_: typing.Optional[typing.Union["MssqlDatabaseImport", typing.Dict[builtins.str, typing.Any]]] = None,
        ledger_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_type: typing.Optional[builtins.str] = None,
        long_term_retention_policy: typing.Optional[typing.Union["MssqlDatabaseLongTermRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_configuration_name: typing.Optional[builtins.str] = None,
        max_size_gb: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        read_replica_count: typing.Optional[jsii.Number] = None,
        read_scale: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_database_id: typing.Optional[builtins.str] = None,
        recovery_point_id: typing.Optional[builtins.str] = None,
        restore_dropped_database_id: typing.Optional[builtins.str] = None,
        restore_long_term_retention_backup_id: typing.Optional[builtins.str] = None,
        restore_point_in_time: typing.Optional[builtins.str] = None,
        sample_name: typing.Optional[builtins.str] = None,
        secondary_type: typing.Optional[builtins.str] = None,
        short_term_retention_policy: typing.Optional[typing.Union["MssqlDatabaseShortTermRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        sku_name: typing.Optional[builtins.str] = None,
        storage_account_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        threat_detection_policy: typing.Optional[typing.Union["MssqlDatabaseThreatDetectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MssqlDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transparent_data_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transparent_data_encryption_key_automatic_rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transparent_data_encryption_key_vault_key_id: typing.Optional[builtins.str] = None,
        zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database azurerm_mssql_database} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#name MssqlDatabase#name}.
        :param server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#server_id MssqlDatabase#server_id}.
        :param auto_pause_delay_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#auto_pause_delay_in_minutes MssqlDatabase#auto_pause_delay_in_minutes}.
        :param collation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#collation MssqlDatabase#collation}.
        :param create_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#create_mode MssqlDatabase#create_mode}.
        :param creation_source_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#creation_source_database_id MssqlDatabase#creation_source_database_id}.
        :param elastic_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#elastic_pool_id MssqlDatabase#elastic_pool_id}.
        :param enclave_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#enclave_type MssqlDatabase#enclave_type}.
        :param geo_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#geo_backup_enabled MssqlDatabase#geo_backup_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#id MssqlDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#identity MssqlDatabase#identity}
        :param import_: import block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#import MssqlDatabase#import}
        :param ledger_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#ledger_enabled MssqlDatabase#ledger_enabled}.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#license_type MssqlDatabase#license_type}.
        :param long_term_retention_policy: long_term_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#long_term_retention_policy MssqlDatabase#long_term_retention_policy}
        :param maintenance_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#maintenance_configuration_name MssqlDatabase#maintenance_configuration_name}.
        :param max_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#max_size_gb MssqlDatabase#max_size_gb}.
        :param min_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#min_capacity MssqlDatabase#min_capacity}.
        :param read_replica_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read_replica_count MssqlDatabase#read_replica_count}.
        :param read_scale: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read_scale MssqlDatabase#read_scale}.
        :param recover_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#recover_database_id MssqlDatabase#recover_database_id}.
        :param recovery_point_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#recovery_point_id MssqlDatabase#recovery_point_id}.
        :param restore_dropped_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_dropped_database_id MssqlDatabase#restore_dropped_database_id}.
        :param restore_long_term_retention_backup_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_long_term_retention_backup_id MssqlDatabase#restore_long_term_retention_backup_id}.
        :param restore_point_in_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_point_in_time MssqlDatabase#restore_point_in_time}.
        :param sample_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#sample_name MssqlDatabase#sample_name}.
        :param secondary_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#secondary_type MssqlDatabase#secondary_type}.
        :param short_term_retention_policy: short_term_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#short_term_retention_policy MssqlDatabase#short_term_retention_policy}
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#sku_name MssqlDatabase#sku_name}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_type MssqlDatabase#storage_account_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#tags MssqlDatabase#tags}.
        :param threat_detection_policy: threat_detection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#threat_detection_policy MssqlDatabase#threat_detection_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#timeouts MssqlDatabase#timeouts}
        :param transparent_data_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_enabled MssqlDatabase#transparent_data_encryption_enabled}.
        :param transparent_data_encryption_key_automatic_rotation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_key_automatic_rotation_enabled MssqlDatabase#transparent_data_encryption_key_automatic_rotation_enabled}.
        :param transparent_data_encryption_key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_key_vault_key_id MssqlDatabase#transparent_data_encryption_key_vault_key_id}.
        :param zone_redundant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#zone_redundant MssqlDatabase#zone_redundant}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ff9fd913292a0afe91f8d3b341f3298b6e1012b4574553dc1fbb11b5f8a81a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MssqlDatabaseConfig(
            name=name,
            server_id=server_id,
            auto_pause_delay_in_minutes=auto_pause_delay_in_minutes,
            collation=collation,
            create_mode=create_mode,
            creation_source_database_id=creation_source_database_id,
            elastic_pool_id=elastic_pool_id,
            enclave_type=enclave_type,
            geo_backup_enabled=geo_backup_enabled,
            id=id,
            identity=identity,
            import_=import_,
            ledger_enabled=ledger_enabled,
            license_type=license_type,
            long_term_retention_policy=long_term_retention_policy,
            maintenance_configuration_name=maintenance_configuration_name,
            max_size_gb=max_size_gb,
            min_capacity=min_capacity,
            read_replica_count=read_replica_count,
            read_scale=read_scale,
            recover_database_id=recover_database_id,
            recovery_point_id=recovery_point_id,
            restore_dropped_database_id=restore_dropped_database_id,
            restore_long_term_retention_backup_id=restore_long_term_retention_backup_id,
            restore_point_in_time=restore_point_in_time,
            sample_name=sample_name,
            secondary_type=secondary_type,
            short_term_retention_policy=short_term_retention_policy,
            sku_name=sku_name,
            storage_account_type=storage_account_type,
            tags=tags,
            threat_detection_policy=threat_detection_policy,
            timeouts=timeouts,
            transparent_data_encryption_enabled=transparent_data_encryption_enabled,
            transparent_data_encryption_key_automatic_rotation_enabled=transparent_data_encryption_key_automatic_rotation_enabled,
            transparent_data_encryption_key_vault_key_id=transparent_data_encryption_key_vault_key_id,
            zone_redundant=zone_redundant,
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
        '''Generates CDKTF code for importing a MssqlDatabase resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MssqlDatabase to import.
        :param import_from_id: The id of the existing MssqlDatabase that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MssqlDatabase to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e9650bc7d4fea45ace0aacf007f26abb25d95fe0f8584d6803e991d9bf0248)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#identity_ids MssqlDatabase#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#type MssqlDatabase#type}.
        '''
        value = MssqlDatabaseIdentity(identity_ids=identity_ids, type=type)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putImport")
    def put_import(
        self,
        *,
        administrator_login: builtins.str,
        administrator_login_password: builtins.str,
        authentication_type: builtins.str,
        storage_key: builtins.str,
        storage_key_type: builtins.str,
        storage_uri: builtins.str,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param administrator_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#administrator_login MssqlDatabase#administrator_login}.
        :param administrator_login_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#administrator_login_password MssqlDatabase#administrator_login_password}.
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#authentication_type MssqlDatabase#authentication_type}.
        :param storage_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_key MssqlDatabase#storage_key}.
        :param storage_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_key_type MssqlDatabase#storage_key_type}.
        :param storage_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_uri MssqlDatabase#storage_uri}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_id MssqlDatabase#storage_account_id}.
        '''
        value = MssqlDatabaseImport(
            administrator_login=administrator_login,
            administrator_login_password=administrator_login_password,
            authentication_type=authentication_type,
            storage_key=storage_key,
            storage_key_type=storage_key_type,
            storage_uri=storage_uri,
            storage_account_id=storage_account_id,
        )

        return typing.cast(None, jsii.invoke(self, "putImport", [value]))

    @jsii.member(jsii_name="putLongTermRetentionPolicy")
    def put_long_term_retention_policy(
        self,
        *,
        immutable_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_retention: typing.Optional[builtins.str] = None,
        weekly_retention: typing.Optional[builtins.str] = None,
        week_of_year: typing.Optional[jsii.Number] = None,
        yearly_retention: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param immutable_backups_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#immutable_backups_enabled MssqlDatabase#immutable_backups_enabled}.
        :param monthly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#monthly_retention MssqlDatabase#monthly_retention}.
        :param weekly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#weekly_retention MssqlDatabase#weekly_retention}.
        :param week_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#week_of_year MssqlDatabase#week_of_year}.
        :param yearly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#yearly_retention MssqlDatabase#yearly_retention}.
        '''
        value = MssqlDatabaseLongTermRetentionPolicy(
            immutable_backups_enabled=immutable_backups_enabled,
            monthly_retention=monthly_retention,
            weekly_retention=weekly_retention,
            week_of_year=week_of_year,
            yearly_retention=yearly_retention,
        )

        return typing.cast(None, jsii.invoke(self, "putLongTermRetentionPolicy", [value]))

    @jsii.member(jsii_name="putShortTermRetentionPolicy")
    def put_short_term_retention_policy(
        self,
        *,
        retention_days: jsii.Number,
        backup_interval_in_hours: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#retention_days MssqlDatabase#retention_days}.
        :param backup_interval_in_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#backup_interval_in_hours MssqlDatabase#backup_interval_in_hours}.
        '''
        value = MssqlDatabaseShortTermRetentionPolicy(
            retention_days=retention_days,
            backup_interval_in_hours=backup_interval_in_hours,
        )

        return typing.cast(None, jsii.invoke(self, "putShortTermRetentionPolicy", [value]))

    @jsii.member(jsii_name="putThreatDetectionPolicy")
    def put_threat_detection_policy(
        self,
        *,
        disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_account_admins: typing.Optional[builtins.str] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled_alerts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#disabled_alerts MssqlDatabase#disabled_alerts}.
        :param email_account_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#email_account_admins MssqlDatabase#email_account_admins}.
        :param email_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#email_addresses MssqlDatabase#email_addresses}.
        :param retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#retention_days MssqlDatabase#retention_days}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#state MssqlDatabase#state}.
        :param storage_account_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_access_key MssqlDatabase#storage_account_access_key}.
        :param storage_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_endpoint MssqlDatabase#storage_endpoint}.
        '''
        value = MssqlDatabaseThreatDetectionPolicy(
            disabled_alerts=disabled_alerts,
            email_account_admins=email_account_admins,
            email_addresses=email_addresses,
            retention_days=retention_days,
            state=state,
            storage_account_access_key=storage_account_access_key,
            storage_endpoint=storage_endpoint,
        )

        return typing.cast(None, jsii.invoke(self, "putThreatDetectionPolicy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#create MssqlDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#delete MssqlDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read MssqlDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#update MssqlDatabase#update}.
        '''
        value = MssqlDatabaseTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutoPauseDelayInMinutes")
    def reset_auto_pause_delay_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoPauseDelayInMinutes", []))

    @jsii.member(jsii_name="resetCollation")
    def reset_collation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollation", []))

    @jsii.member(jsii_name="resetCreateMode")
    def reset_create_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateMode", []))

    @jsii.member(jsii_name="resetCreationSourceDatabaseId")
    def reset_creation_source_database_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreationSourceDatabaseId", []))

    @jsii.member(jsii_name="resetElasticPoolId")
    def reset_elastic_pool_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticPoolId", []))

    @jsii.member(jsii_name="resetEnclaveType")
    def reset_enclave_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnclaveType", []))

    @jsii.member(jsii_name="resetGeoBackupEnabled")
    def reset_geo_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoBackupEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetImport")
    def reset_import(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImport", []))

    @jsii.member(jsii_name="resetLedgerEnabled")
    def reset_ledger_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLedgerEnabled", []))

    @jsii.member(jsii_name="resetLicenseType")
    def reset_license_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicenseType", []))

    @jsii.member(jsii_name="resetLongTermRetentionPolicy")
    def reset_long_term_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongTermRetentionPolicy", []))

    @jsii.member(jsii_name="resetMaintenanceConfigurationName")
    def reset_maintenance_configuration_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceConfigurationName", []))

    @jsii.member(jsii_name="resetMaxSizeGb")
    def reset_max_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSizeGb", []))

    @jsii.member(jsii_name="resetMinCapacity")
    def reset_min_capacity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinCapacity", []))

    @jsii.member(jsii_name="resetReadReplicaCount")
    def reset_read_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadReplicaCount", []))

    @jsii.member(jsii_name="resetReadScale")
    def reset_read_scale(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadScale", []))

    @jsii.member(jsii_name="resetRecoverDatabaseId")
    def reset_recover_database_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoverDatabaseId", []))

    @jsii.member(jsii_name="resetRecoveryPointId")
    def reset_recovery_point_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryPointId", []))

    @jsii.member(jsii_name="resetRestoreDroppedDatabaseId")
    def reset_restore_dropped_database_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreDroppedDatabaseId", []))

    @jsii.member(jsii_name="resetRestoreLongTermRetentionBackupId")
    def reset_restore_long_term_retention_backup_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreLongTermRetentionBackupId", []))

    @jsii.member(jsii_name="resetRestorePointInTime")
    def reset_restore_point_in_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestorePointInTime", []))

    @jsii.member(jsii_name="resetSampleName")
    def reset_sample_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleName", []))

    @jsii.member(jsii_name="resetSecondaryType")
    def reset_secondary_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecondaryType", []))

    @jsii.member(jsii_name="resetShortTermRetentionPolicy")
    def reset_short_term_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShortTermRetentionPolicy", []))

    @jsii.member(jsii_name="resetSkuName")
    def reset_sku_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuName", []))

    @jsii.member(jsii_name="resetStorageAccountType")
    def reset_storage_account_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountType", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetThreatDetectionPolicy")
    def reset_threat_detection_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThreatDetectionPolicy", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransparentDataEncryptionEnabled")
    def reset_transparent_data_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransparentDataEncryptionEnabled", []))

    @jsii.member(jsii_name="resetTransparentDataEncryptionKeyAutomaticRotationEnabled")
    def reset_transparent_data_encryption_key_automatic_rotation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransparentDataEncryptionKeyAutomaticRotationEnabled", []))

    @jsii.member(jsii_name="resetTransparentDataEncryptionKeyVaultKeyId")
    def reset_transparent_data_encryption_key_vault_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransparentDataEncryptionKeyVaultKeyId", []))

    @jsii.member(jsii_name="resetZoneRedundant")
    def reset_zone_redundant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneRedundant", []))

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
    @jsii.member(jsii_name="identity")
    def identity(self) -> "MssqlDatabaseIdentityOutputReference":
        return typing.cast("MssqlDatabaseIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="import")
    def import_(self) -> "MssqlDatabaseImportOutputReference":
        return typing.cast("MssqlDatabaseImportOutputReference", jsii.get(self, "import"))

    @builtins.property
    @jsii.member(jsii_name="longTermRetentionPolicy")
    def long_term_retention_policy(
        self,
    ) -> "MssqlDatabaseLongTermRetentionPolicyOutputReference":
        return typing.cast("MssqlDatabaseLongTermRetentionPolicyOutputReference", jsii.get(self, "longTermRetentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="shortTermRetentionPolicy")
    def short_term_retention_policy(
        self,
    ) -> "MssqlDatabaseShortTermRetentionPolicyOutputReference":
        return typing.cast("MssqlDatabaseShortTermRetentionPolicyOutputReference", jsii.get(self, "shortTermRetentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="threatDetectionPolicy")
    def threat_detection_policy(
        self,
    ) -> "MssqlDatabaseThreatDetectionPolicyOutputReference":
        return typing.cast("MssqlDatabaseThreatDetectionPolicyOutputReference", jsii.get(self, "threatDetectionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MssqlDatabaseTimeoutsOutputReference":
        return typing.cast("MssqlDatabaseTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="autoPauseDelayInMinutesInput")
    def auto_pause_delay_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "autoPauseDelayInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="collationInput")
    def collation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collationInput"))

    @builtins.property
    @jsii.member(jsii_name="createModeInput")
    def create_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createModeInput"))

    @builtins.property
    @jsii.member(jsii_name="creationSourceDatabaseIdInput")
    def creation_source_database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creationSourceDatabaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticPoolIdInput")
    def elastic_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "elasticPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="enclaveTypeInput")
    def enclave_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "enclaveTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="geoBackupEnabledInput")
    def geo_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "geoBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["MssqlDatabaseIdentity"]:
        return typing.cast(typing.Optional["MssqlDatabaseIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importInput")
    def import_input(self) -> typing.Optional["MssqlDatabaseImport"]:
        return typing.cast(typing.Optional["MssqlDatabaseImport"], jsii.get(self, "importInput"))

    @builtins.property
    @jsii.member(jsii_name="ledgerEnabledInput")
    def ledger_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ledgerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseTypeInput")
    def license_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "licenseTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="longTermRetentionPolicyInput")
    def long_term_retention_policy_input(
        self,
    ) -> typing.Optional["MssqlDatabaseLongTermRetentionPolicy"]:
        return typing.cast(typing.Optional["MssqlDatabaseLongTermRetentionPolicy"], jsii.get(self, "longTermRetentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfigurationNameInput")
    def maintenance_configuration_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceConfigurationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSizeGbInput")
    def max_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="minCapacityInput")
    def min_capacity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minCapacityInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="readReplicaCountInput")
    def read_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="readScaleInput")
    def read_scale_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readScaleInput"))

    @builtins.property
    @jsii.member(jsii_name="recoverDatabaseIdInput")
    def recover_database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoverDatabaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryPointIdInput")
    def recovery_point_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recoveryPointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreDroppedDatabaseIdInput")
    def restore_dropped_database_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restoreDroppedDatabaseIdInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreLongTermRetentionBackupIdInput")
    def restore_long_term_retention_backup_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restoreLongTermRetentionBackupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePointInTimeInput")
    def restore_point_in_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "restorePointInTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleNameInput")
    def sample_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sampleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secondaryTypeInput")
    def secondary_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secondaryTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="serverIdInput")
    def server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverIdInput"))

    @builtins.property
    @jsii.member(jsii_name="shortTermRetentionPolicyInput")
    def short_term_retention_policy_input(
        self,
    ) -> typing.Optional["MssqlDatabaseShortTermRetentionPolicy"]:
        return typing.cast(typing.Optional["MssqlDatabaseShortTermRetentionPolicy"], jsii.get(self, "shortTermRetentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountTypeInput")
    def storage_account_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="threatDetectionPolicyInput")
    def threat_detection_policy_input(
        self,
    ) -> typing.Optional["MssqlDatabaseThreatDetectionPolicy"]:
        return typing.cast(typing.Optional["MssqlDatabaseThreatDetectionPolicy"], jsii.get(self, "threatDetectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlDatabaseTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MssqlDatabaseTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transparentDataEncryptionEnabledInput")
    def transparent_data_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "transparentDataEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="transparentDataEncryptionKeyAutomaticRotationEnabledInput")
    def transparent_data_encryption_key_automatic_rotation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "transparentDataEncryptionKeyAutomaticRotationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="transparentDataEncryptionKeyVaultKeyIdInput")
    def transparent_data_encryption_key_vault_key_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "transparentDataEncryptionKeyVaultKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneRedundantInput")
    def zone_redundant_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zoneRedundantInput"))

    @builtins.property
    @jsii.member(jsii_name="autoPauseDelayInMinutes")
    def auto_pause_delay_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "autoPauseDelayInMinutes"))

    @auto_pause_delay_in_minutes.setter
    def auto_pause_delay_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59d116c0cfd8d2e5c86eb9b6faa6633d53568a93875eeeb463fc7e63bf05891)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoPauseDelayInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collation")
    def collation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collation"))

    @collation.setter
    def collation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a5978a94c43abe4541e528b0bb0bc3afd6a3a7178593a2daa41305a48f66d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createMode")
    def create_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createMode"))

    @create_mode.setter
    def create_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992dec0189e77a097572f42a2dd4458b75636781e39a7b3605468bf28d3bfe47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creationSourceDatabaseId")
    def creation_source_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationSourceDatabaseId"))

    @creation_source_database_id.setter
    def creation_source_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42e04478dc17d9db20f5e685cf45a5b83d7641e3d2a32b8903348259c9c3d329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creationSourceDatabaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticPoolId")
    def elastic_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "elasticPoolId"))

    @elastic_pool_id.setter
    def elastic_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29780f7a90eae92b1489cae919f9eca66b7592010267cd07a86f6080c8859ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enclaveType")
    def enclave_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enclaveType"))

    @enclave_type.setter
    def enclave_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2439198b94c7db3b9acaaeb4b996a4b14888c5222d314e685a027f50a747d7d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enclaveType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geoBackupEnabled")
    def geo_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "geoBackupEnabled"))

    @geo_backup_enabled.setter
    def geo_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25744f0928c9ff16f22e6cce15b1fc7e1b18f7ad701c81a99a40378a5a6b7eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3e39cea2f41ebde8d0cc1786a81f985128e90ce163868020c52a7e0aa14499)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ledgerEnabled")
    def ledger_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ledgerEnabled"))

    @ledger_enabled.setter
    def ledger_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a672f80858b7d44795591a064b7cb970fe393a2a9bba52a7031dd7ed406306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ledgerEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="licenseType")
    def license_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "licenseType"))

    @license_type.setter
    def license_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda7c2b9f57c0b19556eae4f14587eaa1a62ed5ddc2e9e075778fdda64a5d421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfigurationName")
    def maintenance_configuration_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceConfigurationName"))

    @maintenance_configuration_name.setter
    def maintenance_configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a44e330d2b584c3e8b089bdf21ed2c352823febaee80c439f15a48d13e04590d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceConfigurationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxSizeGb")
    def max_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSizeGb"))

    @max_size_gb.setter
    def max_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d27b7afab69ce7970fe1c37c0df8a3cb5a0f47c2f7fbd8e68e7864e67b7d9a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSizeGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minCapacity")
    def min_capacity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minCapacity"))

    @min_capacity.setter
    def min_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2488a42036c92541349432bca90ea324e69cc61d9a91815e661178b3c26fd123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minCapacity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36cc61dd7fa5efec67b846a29246c0c321cb0737fe8e9299d6e42abe37cdc7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readReplicaCount")
    def read_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "readReplicaCount"))

    @read_replica_count.setter
    def read_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471a58fc6aa584fe515be1c2779e9d2aed21ef47ae454ed2ccbd174fd8573d57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readScale")
    def read_scale(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readScale"))

    @read_scale.setter
    def read_scale(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539f3fb952897290030b7e8d2d8afa2ea3fac92a7608212bb33833e52e21e531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readScale", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoverDatabaseId")
    def recover_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoverDatabaseId"))

    @recover_database_id.setter
    def recover_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83abda5e4806e57e16ab57f1b096d75ebdf28ab38cac61b1f6ca6a677252cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoverDatabaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryPointId")
    def recovery_point_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recoveryPointId"))

    @recovery_point_id.setter
    def recovery_point_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3bcfee27e7414b61faace86bbda8a0c6fbf9b65ea4c5912fcd74934d0dcd24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryPointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restoreDroppedDatabaseId")
    def restore_dropped_database_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restoreDroppedDatabaseId"))

    @restore_dropped_database_id.setter
    def restore_dropped_database_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b56d25fd24effcf39ffc6afe94207324ced2b0e2e94f18fdcc3e2aa63fd7479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreDroppedDatabaseId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restoreLongTermRetentionBackupId")
    def restore_long_term_retention_backup_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restoreLongTermRetentionBackupId"))

    @restore_long_term_retention_backup_id.setter
    def restore_long_term_retention_backup_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbbcbb425dfc0e90805b4c94521aff159740e1be0137e1f754d4105dbe8e16b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreLongTermRetentionBackupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="restorePointInTime")
    def restore_point_in_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "restorePointInTime"))

    @restore_point_in_time.setter
    def restore_point_in_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3955e2f991c8cf9f6f733728d8ece2a64bb1672f465921863ebabadcc39afac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restorePointInTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleName")
    def sample_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sampleName"))

    @sample_name.setter
    def sample_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7a0d6cf5d658007ade8bb39951324ee1c611f4006d323f7432cb40e539488e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secondaryType")
    def secondary_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryType"))

    @secondary_type.setter
    def secondary_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4558cc05fd1ef95289c75eb42b1eda16839e86e7c8572201ed8e742d81723504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secondaryType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverId")
    def server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverId"))

    @server_id.setter
    def server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6216351174bc0c689c2cebb2516fc0060d24f5ead1c6833e866539ca877120a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9d5d2445975b23e70e36c2947fd2b3755353221f49457acb057a0f4e81b040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountType")
    def storage_account_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountType"))

    @storage_account_type.setter
    def storage_account_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b2aeab5dc9a82f2377e2a3ed352731e3cc57fa38ef2e3f04130fd6aa5eed58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0fc604caa35bb8ff320a6feaed2782b17c0b6c2013626ad89a81f386e007f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transparentDataEncryptionEnabled")
    def transparent_data_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "transparentDataEncryptionEnabled"))

    @transparent_data_encryption_enabled.setter
    def transparent_data_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72cd719aacc2501a8c71a32ce3527396b591a665834c0009e565ad3d3ee4e709)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transparentDataEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transparentDataEncryptionKeyAutomaticRotationEnabled")
    def transparent_data_encryption_key_automatic_rotation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "transparentDataEncryptionKeyAutomaticRotationEnabled"))

    @transparent_data_encryption_key_automatic_rotation_enabled.setter
    def transparent_data_encryption_key_automatic_rotation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90edda22a5917eb1409f516268ab71db990575c3869fc1c70991d8e5af11ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transparentDataEncryptionKeyAutomaticRotationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transparentDataEncryptionKeyVaultKeyId")
    def transparent_data_encryption_key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transparentDataEncryptionKeyVaultKeyId"))

    @transparent_data_encryption_key_vault_key_id.setter
    def transparent_data_encryption_key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d7e425b35f23b2febefb87ce2ab67fb5828ee70aa2d65ad96fa8aef7fbe912)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transparentDataEncryptionKeyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneRedundant")
    def zone_redundant(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zoneRedundant"))

    @zone_redundant.setter
    def zone_redundant(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19dcb05a88a40ea640b274b22f4a89d2048f0a3b7ee4a9e5d65bd59998cd36a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneRedundant", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "server_id": "serverId",
        "auto_pause_delay_in_minutes": "autoPauseDelayInMinutes",
        "collation": "collation",
        "create_mode": "createMode",
        "creation_source_database_id": "creationSourceDatabaseId",
        "elastic_pool_id": "elasticPoolId",
        "enclave_type": "enclaveType",
        "geo_backup_enabled": "geoBackupEnabled",
        "id": "id",
        "identity": "identity",
        "import_": "import",
        "ledger_enabled": "ledgerEnabled",
        "license_type": "licenseType",
        "long_term_retention_policy": "longTermRetentionPolicy",
        "maintenance_configuration_name": "maintenanceConfigurationName",
        "max_size_gb": "maxSizeGb",
        "min_capacity": "minCapacity",
        "read_replica_count": "readReplicaCount",
        "read_scale": "readScale",
        "recover_database_id": "recoverDatabaseId",
        "recovery_point_id": "recoveryPointId",
        "restore_dropped_database_id": "restoreDroppedDatabaseId",
        "restore_long_term_retention_backup_id": "restoreLongTermRetentionBackupId",
        "restore_point_in_time": "restorePointInTime",
        "sample_name": "sampleName",
        "secondary_type": "secondaryType",
        "short_term_retention_policy": "shortTermRetentionPolicy",
        "sku_name": "skuName",
        "storage_account_type": "storageAccountType",
        "tags": "tags",
        "threat_detection_policy": "threatDetectionPolicy",
        "timeouts": "timeouts",
        "transparent_data_encryption_enabled": "transparentDataEncryptionEnabled",
        "transparent_data_encryption_key_automatic_rotation_enabled": "transparentDataEncryptionKeyAutomaticRotationEnabled",
        "transparent_data_encryption_key_vault_key_id": "transparentDataEncryptionKeyVaultKeyId",
        "zone_redundant": "zoneRedundant",
    },
)
class MssqlDatabaseConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        server_id: builtins.str,
        auto_pause_delay_in_minutes: typing.Optional[jsii.Number] = None,
        collation: typing.Optional[builtins.str] = None,
        create_mode: typing.Optional[builtins.str] = None,
        creation_source_database_id: typing.Optional[builtins.str] = None,
        elastic_pool_id: typing.Optional[builtins.str] = None,
        enclave_type: typing.Optional[builtins.str] = None,
        geo_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["MssqlDatabaseIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        import_: typing.Optional[typing.Union["MssqlDatabaseImport", typing.Dict[builtins.str, typing.Any]]] = None,
        ledger_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        license_type: typing.Optional[builtins.str] = None,
        long_term_retention_policy: typing.Optional[typing.Union["MssqlDatabaseLongTermRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_configuration_name: typing.Optional[builtins.str] = None,
        max_size_gb: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        read_replica_count: typing.Optional[jsii.Number] = None,
        read_scale: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_database_id: typing.Optional[builtins.str] = None,
        recovery_point_id: typing.Optional[builtins.str] = None,
        restore_dropped_database_id: typing.Optional[builtins.str] = None,
        restore_long_term_retention_backup_id: typing.Optional[builtins.str] = None,
        restore_point_in_time: typing.Optional[builtins.str] = None,
        sample_name: typing.Optional[builtins.str] = None,
        secondary_type: typing.Optional[builtins.str] = None,
        short_term_retention_policy: typing.Optional[typing.Union["MssqlDatabaseShortTermRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        sku_name: typing.Optional[builtins.str] = None,
        storage_account_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        threat_detection_policy: typing.Optional[typing.Union["MssqlDatabaseThreatDetectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["MssqlDatabaseTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transparent_data_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transparent_data_encryption_key_automatic_rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        transparent_data_encryption_key_vault_key_id: typing.Optional[builtins.str] = None,
        zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#name MssqlDatabase#name}.
        :param server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#server_id MssqlDatabase#server_id}.
        :param auto_pause_delay_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#auto_pause_delay_in_minutes MssqlDatabase#auto_pause_delay_in_minutes}.
        :param collation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#collation MssqlDatabase#collation}.
        :param create_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#create_mode MssqlDatabase#create_mode}.
        :param creation_source_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#creation_source_database_id MssqlDatabase#creation_source_database_id}.
        :param elastic_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#elastic_pool_id MssqlDatabase#elastic_pool_id}.
        :param enclave_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#enclave_type MssqlDatabase#enclave_type}.
        :param geo_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#geo_backup_enabled MssqlDatabase#geo_backup_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#id MssqlDatabase#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#identity MssqlDatabase#identity}
        :param import_: import block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#import MssqlDatabase#import}
        :param ledger_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#ledger_enabled MssqlDatabase#ledger_enabled}.
        :param license_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#license_type MssqlDatabase#license_type}.
        :param long_term_retention_policy: long_term_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#long_term_retention_policy MssqlDatabase#long_term_retention_policy}
        :param maintenance_configuration_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#maintenance_configuration_name MssqlDatabase#maintenance_configuration_name}.
        :param max_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#max_size_gb MssqlDatabase#max_size_gb}.
        :param min_capacity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#min_capacity MssqlDatabase#min_capacity}.
        :param read_replica_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read_replica_count MssqlDatabase#read_replica_count}.
        :param read_scale: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read_scale MssqlDatabase#read_scale}.
        :param recover_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#recover_database_id MssqlDatabase#recover_database_id}.
        :param recovery_point_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#recovery_point_id MssqlDatabase#recovery_point_id}.
        :param restore_dropped_database_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_dropped_database_id MssqlDatabase#restore_dropped_database_id}.
        :param restore_long_term_retention_backup_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_long_term_retention_backup_id MssqlDatabase#restore_long_term_retention_backup_id}.
        :param restore_point_in_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_point_in_time MssqlDatabase#restore_point_in_time}.
        :param sample_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#sample_name MssqlDatabase#sample_name}.
        :param secondary_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#secondary_type MssqlDatabase#secondary_type}.
        :param short_term_retention_policy: short_term_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#short_term_retention_policy MssqlDatabase#short_term_retention_policy}
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#sku_name MssqlDatabase#sku_name}.
        :param storage_account_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_type MssqlDatabase#storage_account_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#tags MssqlDatabase#tags}.
        :param threat_detection_policy: threat_detection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#threat_detection_policy MssqlDatabase#threat_detection_policy}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#timeouts MssqlDatabase#timeouts}
        :param transparent_data_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_enabled MssqlDatabase#transparent_data_encryption_enabled}.
        :param transparent_data_encryption_key_automatic_rotation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_key_automatic_rotation_enabled MssqlDatabase#transparent_data_encryption_key_automatic_rotation_enabled}.
        :param transparent_data_encryption_key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_key_vault_key_id MssqlDatabase#transparent_data_encryption_key_vault_key_id}.
        :param zone_redundant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#zone_redundant MssqlDatabase#zone_redundant}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = MssqlDatabaseIdentity(**identity)
        if isinstance(import_, dict):
            import_ = MssqlDatabaseImport(**import_)
        if isinstance(long_term_retention_policy, dict):
            long_term_retention_policy = MssqlDatabaseLongTermRetentionPolicy(**long_term_retention_policy)
        if isinstance(short_term_retention_policy, dict):
            short_term_retention_policy = MssqlDatabaseShortTermRetentionPolicy(**short_term_retention_policy)
        if isinstance(threat_detection_policy, dict):
            threat_detection_policy = MssqlDatabaseThreatDetectionPolicy(**threat_detection_policy)
        if isinstance(timeouts, dict):
            timeouts = MssqlDatabaseTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f205f3496fa1b29eb23bd4593c059a95e2ccfcf665cd3b2203477c9ba9ca87)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
            check_type(argname="argument auto_pause_delay_in_minutes", value=auto_pause_delay_in_minutes, expected_type=type_hints["auto_pause_delay_in_minutes"])
            check_type(argname="argument collation", value=collation, expected_type=type_hints["collation"])
            check_type(argname="argument create_mode", value=create_mode, expected_type=type_hints["create_mode"])
            check_type(argname="argument creation_source_database_id", value=creation_source_database_id, expected_type=type_hints["creation_source_database_id"])
            check_type(argname="argument elastic_pool_id", value=elastic_pool_id, expected_type=type_hints["elastic_pool_id"])
            check_type(argname="argument enclave_type", value=enclave_type, expected_type=type_hints["enclave_type"])
            check_type(argname="argument geo_backup_enabled", value=geo_backup_enabled, expected_type=type_hints["geo_backup_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument import_", value=import_, expected_type=type_hints["import_"])
            check_type(argname="argument ledger_enabled", value=ledger_enabled, expected_type=type_hints["ledger_enabled"])
            check_type(argname="argument license_type", value=license_type, expected_type=type_hints["license_type"])
            check_type(argname="argument long_term_retention_policy", value=long_term_retention_policy, expected_type=type_hints["long_term_retention_policy"])
            check_type(argname="argument maintenance_configuration_name", value=maintenance_configuration_name, expected_type=type_hints["maintenance_configuration_name"])
            check_type(argname="argument max_size_gb", value=max_size_gb, expected_type=type_hints["max_size_gb"])
            check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            check_type(argname="argument read_replica_count", value=read_replica_count, expected_type=type_hints["read_replica_count"])
            check_type(argname="argument read_scale", value=read_scale, expected_type=type_hints["read_scale"])
            check_type(argname="argument recover_database_id", value=recover_database_id, expected_type=type_hints["recover_database_id"])
            check_type(argname="argument recovery_point_id", value=recovery_point_id, expected_type=type_hints["recovery_point_id"])
            check_type(argname="argument restore_dropped_database_id", value=restore_dropped_database_id, expected_type=type_hints["restore_dropped_database_id"])
            check_type(argname="argument restore_long_term_retention_backup_id", value=restore_long_term_retention_backup_id, expected_type=type_hints["restore_long_term_retention_backup_id"])
            check_type(argname="argument restore_point_in_time", value=restore_point_in_time, expected_type=type_hints["restore_point_in_time"])
            check_type(argname="argument sample_name", value=sample_name, expected_type=type_hints["sample_name"])
            check_type(argname="argument secondary_type", value=secondary_type, expected_type=type_hints["secondary_type"])
            check_type(argname="argument short_term_retention_policy", value=short_term_retention_policy, expected_type=type_hints["short_term_retention_policy"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument storage_account_type", value=storage_account_type, expected_type=type_hints["storage_account_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument threat_detection_policy", value=threat_detection_policy, expected_type=type_hints["threat_detection_policy"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transparent_data_encryption_enabled", value=transparent_data_encryption_enabled, expected_type=type_hints["transparent_data_encryption_enabled"])
            check_type(argname="argument transparent_data_encryption_key_automatic_rotation_enabled", value=transparent_data_encryption_key_automatic_rotation_enabled, expected_type=type_hints["transparent_data_encryption_key_automatic_rotation_enabled"])
            check_type(argname="argument transparent_data_encryption_key_vault_key_id", value=transparent_data_encryption_key_vault_key_id, expected_type=type_hints["transparent_data_encryption_key_vault_key_id"])
            check_type(argname="argument zone_redundant", value=zone_redundant, expected_type=type_hints["zone_redundant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "server_id": server_id,
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
        if auto_pause_delay_in_minutes is not None:
            self._values["auto_pause_delay_in_minutes"] = auto_pause_delay_in_minutes
        if collation is not None:
            self._values["collation"] = collation
        if create_mode is not None:
            self._values["create_mode"] = create_mode
        if creation_source_database_id is not None:
            self._values["creation_source_database_id"] = creation_source_database_id
        if elastic_pool_id is not None:
            self._values["elastic_pool_id"] = elastic_pool_id
        if enclave_type is not None:
            self._values["enclave_type"] = enclave_type
        if geo_backup_enabled is not None:
            self._values["geo_backup_enabled"] = geo_backup_enabled
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if import_ is not None:
            self._values["import_"] = import_
        if ledger_enabled is not None:
            self._values["ledger_enabled"] = ledger_enabled
        if license_type is not None:
            self._values["license_type"] = license_type
        if long_term_retention_policy is not None:
            self._values["long_term_retention_policy"] = long_term_retention_policy
        if maintenance_configuration_name is not None:
            self._values["maintenance_configuration_name"] = maintenance_configuration_name
        if max_size_gb is not None:
            self._values["max_size_gb"] = max_size_gb
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if read_replica_count is not None:
            self._values["read_replica_count"] = read_replica_count
        if read_scale is not None:
            self._values["read_scale"] = read_scale
        if recover_database_id is not None:
            self._values["recover_database_id"] = recover_database_id
        if recovery_point_id is not None:
            self._values["recovery_point_id"] = recovery_point_id
        if restore_dropped_database_id is not None:
            self._values["restore_dropped_database_id"] = restore_dropped_database_id
        if restore_long_term_retention_backup_id is not None:
            self._values["restore_long_term_retention_backup_id"] = restore_long_term_retention_backup_id
        if restore_point_in_time is not None:
            self._values["restore_point_in_time"] = restore_point_in_time
        if sample_name is not None:
            self._values["sample_name"] = sample_name
        if secondary_type is not None:
            self._values["secondary_type"] = secondary_type
        if short_term_retention_policy is not None:
            self._values["short_term_retention_policy"] = short_term_retention_policy
        if sku_name is not None:
            self._values["sku_name"] = sku_name
        if storage_account_type is not None:
            self._values["storage_account_type"] = storage_account_type
        if tags is not None:
            self._values["tags"] = tags
        if threat_detection_policy is not None:
            self._values["threat_detection_policy"] = threat_detection_policy
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transparent_data_encryption_enabled is not None:
            self._values["transparent_data_encryption_enabled"] = transparent_data_encryption_enabled
        if transparent_data_encryption_key_automatic_rotation_enabled is not None:
            self._values["transparent_data_encryption_key_automatic_rotation_enabled"] = transparent_data_encryption_key_automatic_rotation_enabled
        if transparent_data_encryption_key_vault_key_id is not None:
            self._values["transparent_data_encryption_key_vault_key_id"] = transparent_data_encryption_key_vault_key_id
        if zone_redundant is not None:
            self._values["zone_redundant"] = zone_redundant

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#name MssqlDatabase#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#server_id MssqlDatabase#server_id}.'''
        result = self._values.get("server_id")
        assert result is not None, "Required property 'server_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_pause_delay_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#auto_pause_delay_in_minutes MssqlDatabase#auto_pause_delay_in_minutes}.'''
        result = self._values.get("auto_pause_delay_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def collation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#collation MssqlDatabase#collation}.'''
        result = self._values.get("collation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#create_mode MssqlDatabase#create_mode}.'''
        result = self._values.get("create_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creation_source_database_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#creation_source_database_id MssqlDatabase#creation_source_database_id}.'''
        result = self._values.get("creation_source_database_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elastic_pool_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#elastic_pool_id MssqlDatabase#elastic_pool_id}.'''
        result = self._values.get("elastic_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enclave_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#enclave_type MssqlDatabase#enclave_type}.'''
        result = self._values.get("enclave_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geo_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#geo_backup_enabled MssqlDatabase#geo_backup_enabled}.'''
        result = self._values.get("geo_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#id MssqlDatabase#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["MssqlDatabaseIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#identity MssqlDatabase#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["MssqlDatabaseIdentity"], result)

    @builtins.property
    def import_(self) -> typing.Optional["MssqlDatabaseImport"]:
        '''import block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#import MssqlDatabase#import}
        '''
        result = self._values.get("import_")
        return typing.cast(typing.Optional["MssqlDatabaseImport"], result)

    @builtins.property
    def ledger_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#ledger_enabled MssqlDatabase#ledger_enabled}.'''
        result = self._values.get("ledger_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def license_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#license_type MssqlDatabase#license_type}.'''
        result = self._values.get("license_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def long_term_retention_policy(
        self,
    ) -> typing.Optional["MssqlDatabaseLongTermRetentionPolicy"]:
        '''long_term_retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#long_term_retention_policy MssqlDatabase#long_term_retention_policy}
        '''
        result = self._values.get("long_term_retention_policy")
        return typing.cast(typing.Optional["MssqlDatabaseLongTermRetentionPolicy"], result)

    @builtins.property
    def maintenance_configuration_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#maintenance_configuration_name MssqlDatabase#maintenance_configuration_name}.'''
        result = self._values.get("maintenance_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#max_size_gb MssqlDatabase#max_size_gb}.'''
        result = self._values.get("max_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#min_capacity MssqlDatabase#min_capacity}.'''
        result = self._values.get("min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_replica_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read_replica_count MssqlDatabase#read_replica_count}.'''
        result = self._values.get("read_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_scale(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read_scale MssqlDatabase#read_scale}.'''
        result = self._values.get("read_scale")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recover_database_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#recover_database_id MssqlDatabase#recover_database_id}.'''
        result = self._values.get("recover_database_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recovery_point_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#recovery_point_id MssqlDatabase#recovery_point_id}.'''
        result = self._values.get("recovery_point_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_dropped_database_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_dropped_database_id MssqlDatabase#restore_dropped_database_id}.'''
        result = self._values.get("restore_dropped_database_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_long_term_retention_backup_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_long_term_retention_backup_id MssqlDatabase#restore_long_term_retention_backup_id}.'''
        result = self._values.get("restore_long_term_retention_backup_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restore_point_in_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#restore_point_in_time MssqlDatabase#restore_point_in_time}.'''
        result = self._values.get("restore_point_in_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#sample_name MssqlDatabase#sample_name}.'''
        result = self._values.get("sample_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secondary_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#secondary_type MssqlDatabase#secondary_type}.'''
        result = self._values.get("secondary_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def short_term_retention_policy(
        self,
    ) -> typing.Optional["MssqlDatabaseShortTermRetentionPolicy"]:
        '''short_term_retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#short_term_retention_policy MssqlDatabase#short_term_retention_policy}
        '''
        result = self._values.get("short_term_retention_policy")
        return typing.cast(typing.Optional["MssqlDatabaseShortTermRetentionPolicy"], result)

    @builtins.property
    def sku_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#sku_name MssqlDatabase#sku_name}.'''
        result = self._values.get("sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_type MssqlDatabase#storage_account_type}.'''
        result = self._values.get("storage_account_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#tags MssqlDatabase#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def threat_detection_policy(
        self,
    ) -> typing.Optional["MssqlDatabaseThreatDetectionPolicy"]:
        '''threat_detection_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#threat_detection_policy MssqlDatabase#threat_detection_policy}
        '''
        result = self._values.get("threat_detection_policy")
        return typing.cast(typing.Optional["MssqlDatabaseThreatDetectionPolicy"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MssqlDatabaseTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#timeouts MssqlDatabase#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MssqlDatabaseTimeouts"], result)

    @builtins.property
    def transparent_data_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_enabled MssqlDatabase#transparent_data_encryption_enabled}.'''
        result = self._values.get("transparent_data_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transparent_data_encryption_key_automatic_rotation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_key_automatic_rotation_enabled MssqlDatabase#transparent_data_encryption_key_automatic_rotation_enabled}.'''
        result = self._values.get("transparent_data_encryption_key_automatic_rotation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def transparent_data_encryption_key_vault_key_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#transparent_data_encryption_key_vault_key_id MssqlDatabase#transparent_data_encryption_key_vault_key_id}.'''
        result = self._values.get("transparent_data_encryption_key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_redundant(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#zone_redundant MssqlDatabase#zone_redundant}.'''
        result = self._values.get("zone_redundant")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlDatabaseConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseIdentity",
    jsii_struct_bases=[],
    name_mapping={"identity_ids": "identityIds", "type": "type"},
)
class MssqlDatabaseIdentity:
    def __init__(
        self,
        *,
        identity_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#identity_ids MssqlDatabase#identity_ids}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#type MssqlDatabase#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd1cfba0624c5a520ab5d1338e690a0d0a13713721315adb5d510d6d777b0ce)
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_ids": identity_ids,
            "type": type,
        }

    @builtins.property
    def identity_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#identity_ids MssqlDatabase#identity_ids}.'''
        result = self._values.get("identity_ids")
        assert result is not None, "Required property 'identity_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#type MssqlDatabase#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlDatabaseIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlDatabaseIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e2577ba667f939075d1583020d2f2f7dfc3b7b32f78dbef3751ab02368a67c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c27d377e07210e82e42661b71e79eaaef7a6f4557450ea8f0365cdd79efab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202a9766f942b7a101322514144caa8d470044522487582de96bb41c0f6c0a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlDatabaseIdentity]:
        return typing.cast(typing.Optional[MssqlDatabaseIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MssqlDatabaseIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a9dda4729051be04a977aa152a78764e52143e72bed7d1a72c3b7f93bdd7172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseImport",
    jsii_struct_bases=[],
    name_mapping={
        "administrator_login": "administratorLogin",
        "administrator_login_password": "administratorLoginPassword",
        "authentication_type": "authenticationType",
        "storage_key": "storageKey",
        "storage_key_type": "storageKeyType",
        "storage_uri": "storageUri",
        "storage_account_id": "storageAccountId",
    },
)
class MssqlDatabaseImport:
    def __init__(
        self,
        *,
        administrator_login: builtins.str,
        administrator_login_password: builtins.str,
        authentication_type: builtins.str,
        storage_key: builtins.str,
        storage_key_type: builtins.str,
        storage_uri: builtins.str,
        storage_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param administrator_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#administrator_login MssqlDatabase#administrator_login}.
        :param administrator_login_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#administrator_login_password MssqlDatabase#administrator_login_password}.
        :param authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#authentication_type MssqlDatabase#authentication_type}.
        :param storage_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_key MssqlDatabase#storage_key}.
        :param storage_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_key_type MssqlDatabase#storage_key_type}.
        :param storage_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_uri MssqlDatabase#storage_uri}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_id MssqlDatabase#storage_account_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca34f4f7db950e341d6bcd78037f59d4ad3c50d9ec21ff7a39316f45f748780)
            check_type(argname="argument administrator_login", value=administrator_login, expected_type=type_hints["administrator_login"])
            check_type(argname="argument administrator_login_password", value=administrator_login_password, expected_type=type_hints["administrator_login_password"])
            check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            check_type(argname="argument storage_key", value=storage_key, expected_type=type_hints["storage_key"])
            check_type(argname="argument storage_key_type", value=storage_key_type, expected_type=type_hints["storage_key_type"])
            check_type(argname="argument storage_uri", value=storage_uri, expected_type=type_hints["storage_uri"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "administrator_login": administrator_login,
            "administrator_login_password": administrator_login_password,
            "authentication_type": authentication_type,
            "storage_key": storage_key,
            "storage_key_type": storage_key_type,
            "storage_uri": storage_uri,
        }
        if storage_account_id is not None:
            self._values["storage_account_id"] = storage_account_id

    @builtins.property
    def administrator_login(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#administrator_login MssqlDatabase#administrator_login}.'''
        result = self._values.get("administrator_login")
        assert result is not None, "Required property 'administrator_login' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrator_login_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#administrator_login_password MssqlDatabase#administrator_login_password}.'''
        result = self._values.get("administrator_login_password")
        assert result is not None, "Required property 'administrator_login_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#authentication_type MssqlDatabase#authentication_type}.'''
        result = self._values.get("authentication_type")
        assert result is not None, "Required property 'authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_key MssqlDatabase#storage_key}.'''
        result = self._values.get("storage_key")
        assert result is not None, "Required property 'storage_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_key_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_key_type MssqlDatabase#storage_key_type}.'''
        result = self._values.get("storage_key_type")
        assert result is not None, "Required property 'storage_key_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_uri MssqlDatabase#storage_uri}.'''
        result = self._values.get("storage_uri")
        assert result is not None, "Required property 'storage_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_id MssqlDatabase#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlDatabaseImport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlDatabaseImportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseImportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce968740043b4c0c231aeb811b7ea531e1912aa80e97cc517929031d5d37526c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStorageAccountId")
    def reset_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginInput")
    def administrator_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginPasswordInput")
    def administrator_login_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypeInput")
    def authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageKeyInput")
    def storage_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageKeyTypeInput")
    def storage_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageUriInput")
    def storage_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLogin")
    def administrator_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLogin"))

    @administrator_login.setter
    def administrator_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a5472bf263e7918ad50d123c2810d58fd1b5a4401e300b5c64050de98517f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLogin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administratorLoginPassword")
    def administrator_login_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLoginPassword"))

    @administrator_login_password.setter
    def administrator_login_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0fa0fd08c7c6a400be07342429d064af2706c990722892b9af04d80382d4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLoginPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="authenticationType")
    def authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authenticationType"))

    @authentication_type.setter
    def authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e468e592ae8f4400924f46c58c2a0956e9b7a1d66715e3b7a63c05769c64058)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a29fe888994dacc87e584f7ad342e5dd444529b9dcbc64644eb6090e083269a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageKey")
    def storage_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageKey"))

    @storage_key.setter
    def storage_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940bfebef3777fdbfcb028c56cd20d1c53e92ce3f3bf116bbd8a302ddd92686e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageKeyType")
    def storage_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageKeyType"))

    @storage_key_type.setter
    def storage_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e91b5a2468f1706f8ba18b035f5a434353631ad7c00248533b3c8cc301fccec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageUri")
    def storage_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageUri"))

    @storage_uri.setter
    def storage_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0324202e22cf610e4e314338d34fb3e2176d656903db25e2ef9dbed249e862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlDatabaseImport]:
        return typing.cast(typing.Optional[MssqlDatabaseImport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[MssqlDatabaseImport]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37a30f34baf533744ad3e7984413648442d3f16c2d9d314cd7ce1302b793a15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseLongTermRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "immutable_backups_enabled": "immutableBackupsEnabled",
        "monthly_retention": "monthlyRetention",
        "weekly_retention": "weeklyRetention",
        "week_of_year": "weekOfYear",
        "yearly_retention": "yearlyRetention",
    },
)
class MssqlDatabaseLongTermRetentionPolicy:
    def __init__(
        self,
        *,
        immutable_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        monthly_retention: typing.Optional[builtins.str] = None,
        weekly_retention: typing.Optional[builtins.str] = None,
        week_of_year: typing.Optional[jsii.Number] = None,
        yearly_retention: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param immutable_backups_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#immutable_backups_enabled MssqlDatabase#immutable_backups_enabled}.
        :param monthly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#monthly_retention MssqlDatabase#monthly_retention}.
        :param weekly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#weekly_retention MssqlDatabase#weekly_retention}.
        :param week_of_year: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#week_of_year MssqlDatabase#week_of_year}.
        :param yearly_retention: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#yearly_retention MssqlDatabase#yearly_retention}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ebff0d76cb180e40a33a243f66a64e55f9cfcb5d4f340d2b255f9076b5ea20)
            check_type(argname="argument immutable_backups_enabled", value=immutable_backups_enabled, expected_type=type_hints["immutable_backups_enabled"])
            check_type(argname="argument monthly_retention", value=monthly_retention, expected_type=type_hints["monthly_retention"])
            check_type(argname="argument weekly_retention", value=weekly_retention, expected_type=type_hints["weekly_retention"])
            check_type(argname="argument week_of_year", value=week_of_year, expected_type=type_hints["week_of_year"])
            check_type(argname="argument yearly_retention", value=yearly_retention, expected_type=type_hints["yearly_retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if immutable_backups_enabled is not None:
            self._values["immutable_backups_enabled"] = immutable_backups_enabled
        if monthly_retention is not None:
            self._values["monthly_retention"] = monthly_retention
        if weekly_retention is not None:
            self._values["weekly_retention"] = weekly_retention
        if week_of_year is not None:
            self._values["week_of_year"] = week_of_year
        if yearly_retention is not None:
            self._values["yearly_retention"] = yearly_retention

    @builtins.property
    def immutable_backups_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#immutable_backups_enabled MssqlDatabase#immutable_backups_enabled}.'''
        result = self._values.get("immutable_backups_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def monthly_retention(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#monthly_retention MssqlDatabase#monthly_retention}.'''
        result = self._values.get("monthly_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly_retention(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#weekly_retention MssqlDatabase#weekly_retention}.'''
        result = self._values.get("weekly_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_of_year(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#week_of_year MssqlDatabase#week_of_year}.'''
        result = self._values.get("week_of_year")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def yearly_retention(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#yearly_retention MssqlDatabase#yearly_retention}.'''
        result = self._values.get("yearly_retention")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlDatabaseLongTermRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlDatabaseLongTermRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseLongTermRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b933ba048ab09ca163e05d1031f9c3aff4e7cde51d08e4ccc5b5501d9402df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImmutableBackupsEnabled")
    def reset_immutable_backups_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmutableBackupsEnabled", []))

    @jsii.member(jsii_name="resetMonthlyRetention")
    def reset_monthly_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthlyRetention", []))

    @jsii.member(jsii_name="resetWeeklyRetention")
    def reset_weekly_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklyRetention", []))

    @jsii.member(jsii_name="resetWeekOfYear")
    def reset_week_of_year(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekOfYear", []))

    @jsii.member(jsii_name="resetYearlyRetention")
    def reset_yearly_retention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYearlyRetention", []))

    @builtins.property
    @jsii.member(jsii_name="immutableBackupsEnabledInput")
    def immutable_backups_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "immutableBackupsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyRetentionInput")
    def monthly_retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monthlyRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyRetentionInput")
    def weekly_retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "weeklyRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="weekOfYearInput")
    def week_of_year_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weekOfYearInput"))

    @builtins.property
    @jsii.member(jsii_name="yearlyRetentionInput")
    def yearly_retention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "yearlyRetentionInput"))

    @builtins.property
    @jsii.member(jsii_name="immutableBackupsEnabled")
    def immutable_backups_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "immutableBackupsEnabled"))

    @immutable_backups_enabled.setter
    def immutable_backups_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3464ce49fe7d77c1f2430a4d7425db6023bc3083e3c7107db0b8b1fc58c12cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "immutableBackupsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monthlyRetention")
    def monthly_retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monthlyRetention"))

    @monthly_retention.setter
    def monthly_retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bff5692fc1f61a4a09678179dc0c0391686f6dc1c84eac857c363e03b9900b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monthlyRetention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeklyRetention")
    def weekly_retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "weeklyRetention"))

    @weekly_retention.setter
    def weekly_retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec5fe26ba4950396de0bc3b511b9888d775972e96f25af8baf90e2bfa970514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeklyRetention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekOfYear")
    def week_of_year(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weekOfYear"))

    @week_of_year.setter
    def week_of_year(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693d851e896832b63d32335c0d0121c0df8192348139e4b26b1cbf2e7fbea035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekOfYear", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="yearlyRetention")
    def yearly_retention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "yearlyRetention"))

    @yearly_retention.setter
    def yearly_retention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b906315e108b698275ec65fabfe97f6b9d157dbc92bfe3deb288730eaeb81c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "yearlyRetention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlDatabaseLongTermRetentionPolicy]:
        return typing.cast(typing.Optional[MssqlDatabaseLongTermRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlDatabaseLongTermRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006a6e5a84f36682ddbd3cf429111bee2ea08844a3de29ce4addb24aa203af5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseShortTermRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "retention_days": "retentionDays",
        "backup_interval_in_hours": "backupIntervalInHours",
    },
)
class MssqlDatabaseShortTermRetentionPolicy:
    def __init__(
        self,
        *,
        retention_days: jsii.Number,
        backup_interval_in_hours: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#retention_days MssqlDatabase#retention_days}.
        :param backup_interval_in_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#backup_interval_in_hours MssqlDatabase#backup_interval_in_hours}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8f0836294cdcc71c934f357a6e58ce3bca31b3fc4a34bc62ef7664dd4283120)
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
            check_type(argname="argument backup_interval_in_hours", value=backup_interval_in_hours, expected_type=type_hints["backup_interval_in_hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "retention_days": retention_days,
        }
        if backup_interval_in_hours is not None:
            self._values["backup_interval_in_hours"] = backup_interval_in_hours

    @builtins.property
    def retention_days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#retention_days MssqlDatabase#retention_days}.'''
        result = self._values.get("retention_days")
        assert result is not None, "Required property 'retention_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def backup_interval_in_hours(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#backup_interval_in_hours MssqlDatabase#backup_interval_in_hours}.'''
        result = self._values.get("backup_interval_in_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlDatabaseShortTermRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlDatabaseShortTermRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseShortTermRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0b44bde487c1d2d3307e549ebdb22c8c6a0aafeb4e4f82c773cce2aeaa4a8b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBackupIntervalInHours")
    def reset_backup_interval_in_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupIntervalInHours", []))

    @builtins.property
    @jsii.member(jsii_name="backupIntervalInHoursInput")
    def backup_interval_in_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupIntervalInHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaysInput")
    def retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="backupIntervalInHours")
    def backup_interval_in_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupIntervalInHours"))

    @backup_interval_in_hours.setter
    def backup_interval_in_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa299e513142c82547943a8537141cb4d6e9e3cef0a254ef43c3a558df6b0e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupIntervalInHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df289442e9b02673149eb4825d8591f913f341c0abad7316d2e97c1d24d8a207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlDatabaseShortTermRetentionPolicy]:
        return typing.cast(typing.Optional[MssqlDatabaseShortTermRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlDatabaseShortTermRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94995530b05fef4ff3281e60d575205807d1152a904fea464c417f6abbeaec5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseThreatDetectionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "disabled_alerts": "disabledAlerts",
        "email_account_admins": "emailAccountAdmins",
        "email_addresses": "emailAddresses",
        "retention_days": "retentionDays",
        "state": "state",
        "storage_account_access_key": "storageAccountAccessKey",
        "storage_endpoint": "storageEndpoint",
    },
)
class MssqlDatabaseThreatDetectionPolicy:
    def __init__(
        self,
        *,
        disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
        email_account_admins: typing.Optional[builtins.str] = None,
        email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        retention_days: typing.Optional[jsii.Number] = None,
        state: typing.Optional[builtins.str] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param disabled_alerts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#disabled_alerts MssqlDatabase#disabled_alerts}.
        :param email_account_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#email_account_admins MssqlDatabase#email_account_admins}.
        :param email_addresses: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#email_addresses MssqlDatabase#email_addresses}.
        :param retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#retention_days MssqlDatabase#retention_days}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#state MssqlDatabase#state}.
        :param storage_account_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_access_key MssqlDatabase#storage_account_access_key}.
        :param storage_endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_endpoint MssqlDatabase#storage_endpoint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e98c025a6db063682ea13b3651b37663fa3a38c82a10b1d8003229d39c91c9)
            check_type(argname="argument disabled_alerts", value=disabled_alerts, expected_type=type_hints["disabled_alerts"])
            check_type(argname="argument email_account_admins", value=email_account_admins, expected_type=type_hints["email_account_admins"])
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
            check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument storage_account_access_key", value=storage_account_access_key, expected_type=type_hints["storage_account_access_key"])
            check_type(argname="argument storage_endpoint", value=storage_endpoint, expected_type=type_hints["storage_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disabled_alerts is not None:
            self._values["disabled_alerts"] = disabled_alerts
        if email_account_admins is not None:
            self._values["email_account_admins"] = email_account_admins
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if retention_days is not None:
            self._values["retention_days"] = retention_days
        if state is not None:
            self._values["state"] = state
        if storage_account_access_key is not None:
            self._values["storage_account_access_key"] = storage_account_access_key
        if storage_endpoint is not None:
            self._values["storage_endpoint"] = storage_endpoint

    @builtins.property
    def disabled_alerts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#disabled_alerts MssqlDatabase#disabled_alerts}.'''
        result = self._values.get("disabled_alerts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def email_account_admins(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#email_account_admins MssqlDatabase#email_account_admins}.'''
        result = self._values.get("email_account_admins")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#email_addresses MssqlDatabase#email_addresses}.'''
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def retention_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#retention_days MssqlDatabase#retention_days}.'''
        result = self._values.get("retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#state MssqlDatabase#state}.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_account_access_key MssqlDatabase#storage_account_access_key}.'''
        result = self._values.get("storage_account_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#storage_endpoint MssqlDatabase#storage_endpoint}.'''
        result = self._values.get("storage_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlDatabaseThreatDetectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlDatabaseThreatDetectionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseThreatDetectionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5cb1d46c7117286e4d0eb96e69e8854d49a506200ce70da3b1a93044b4c12ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisabledAlerts")
    def reset_disabled_alerts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledAlerts", []))

    @jsii.member(jsii_name="resetEmailAccountAdmins")
    def reset_email_account_admins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAccountAdmins", []))

    @jsii.member(jsii_name="resetEmailAddresses")
    def reset_email_addresses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailAddresses", []))

    @jsii.member(jsii_name="resetRetentionDays")
    def reset_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionDays", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

    @jsii.member(jsii_name="resetStorageAccountAccessKey")
    def reset_storage_account_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountAccessKey", []))

    @jsii.member(jsii_name="resetStorageEndpoint")
    def reset_storage_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="disabledAlertsInput")
    def disabled_alerts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "disabledAlertsInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAccountAdminsInput")
    def email_account_admins_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAccountAdminsInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddressesInput")
    def email_addresses_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "emailAddressesInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionDaysInput")
    def retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKeyInput")
    def storage_account_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageEndpointInput")
    def storage_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledAlerts")
    def disabled_alerts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "disabledAlerts"))

    @disabled_alerts.setter
    def disabled_alerts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc82230fce4a1bbb1d148dddd2f03e2b8b698883affc10fefdaaec216ec05042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledAlerts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAccountAdmins")
    def email_account_admins(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAccountAdmins"))

    @email_account_admins.setter
    def email_account_admins(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e7651f1a2121a828d193ed6da9b5089f201c5a3859a8352c6fcd56a4c4603df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAccountAdmins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailAddresses")
    def email_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "emailAddresses"))

    @email_addresses.setter
    def email_addresses(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076a39fa1c4ddf5bfb50c568a9ab5560301bb5f33c89f6898efc9ad0051b4cbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddresses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionDays")
    def retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionDays"))

    @retention_days.setter
    def retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b672e43d670819f358754126076c010f964d0ea010ab80084df492255e54498f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe809d2e125218750bba067cb195504a7c4a60ffdb90ec6be2467ffd6c1121a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKey")
    def storage_account_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountAccessKey"))

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951f10b24ac728873352a2dc084c6670bce6b2783fa806d8c7c74736aac7d16e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageEndpoint")
    def storage_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageEndpoint"))

    @storage_endpoint.setter
    def storage_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd778ce92966699d80ac03a6eb1e74bdbf5557b8261ba76988a3ebe09b108b30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MssqlDatabaseThreatDetectionPolicy]:
        return typing.cast(typing.Optional[MssqlDatabaseThreatDetectionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MssqlDatabaseThreatDetectionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352d1246dcc9821d2c2e40778a41a2eb683453eeefc2dcd604ec1b6541c7053b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MssqlDatabaseTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#create MssqlDatabase#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#delete MssqlDatabase#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read MssqlDatabase#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#update MssqlDatabase#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a38ae82fb23825b1f6cdd5c16c65f0e9a95c529ee4f6d2b234031cbf56ec3e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#create MssqlDatabase#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#delete MssqlDatabase#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#read MssqlDatabase#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mssql_database#update MssqlDatabase#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MssqlDatabaseTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MssqlDatabaseTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mssqlDatabase.MssqlDatabaseTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bcc19d19ad318976bfe17df8462c6527061986f8aa489bebf8851d0f7d047f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a7aa68a623ddfc76604c485164f2efe7875bdc0d536e8882f8b2a7bb0f9731c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3aab395bd2ce8c203e77cc0f295468e35d9b43f617821ac626ab8ea8f63f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec7a6bafa390832acae7f174de2737e348f689be71019c74ef60741a669b3cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea372a1f96399115ec2c0b232ca54c20de96fc6a046f1604cbdbd217c0816ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlDatabaseTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlDatabaseTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlDatabaseTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d766e8f7bce4cdf4f41fb6b14b1472d838cc010d57ceb9e21b0c53ea4f84f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MssqlDatabase",
    "MssqlDatabaseConfig",
    "MssqlDatabaseIdentity",
    "MssqlDatabaseIdentityOutputReference",
    "MssqlDatabaseImport",
    "MssqlDatabaseImportOutputReference",
    "MssqlDatabaseLongTermRetentionPolicy",
    "MssqlDatabaseLongTermRetentionPolicyOutputReference",
    "MssqlDatabaseShortTermRetentionPolicy",
    "MssqlDatabaseShortTermRetentionPolicyOutputReference",
    "MssqlDatabaseThreatDetectionPolicy",
    "MssqlDatabaseThreatDetectionPolicyOutputReference",
    "MssqlDatabaseTimeouts",
    "MssqlDatabaseTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__44ff9fd913292a0afe91f8d3b341f3298b6e1012b4574553dc1fbb11b5f8a81a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    server_id: builtins.str,
    auto_pause_delay_in_minutes: typing.Optional[jsii.Number] = None,
    collation: typing.Optional[builtins.str] = None,
    create_mode: typing.Optional[builtins.str] = None,
    creation_source_database_id: typing.Optional[builtins.str] = None,
    elastic_pool_id: typing.Optional[builtins.str] = None,
    enclave_type: typing.Optional[builtins.str] = None,
    geo_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MssqlDatabaseIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    import_: typing.Optional[typing.Union[MssqlDatabaseImport, typing.Dict[builtins.str, typing.Any]]] = None,
    ledger_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_type: typing.Optional[builtins.str] = None,
    long_term_retention_policy: typing.Optional[typing.Union[MssqlDatabaseLongTermRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_configuration_name: typing.Optional[builtins.str] = None,
    max_size_gb: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    read_replica_count: typing.Optional[jsii.Number] = None,
    read_scale: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_database_id: typing.Optional[builtins.str] = None,
    recovery_point_id: typing.Optional[builtins.str] = None,
    restore_dropped_database_id: typing.Optional[builtins.str] = None,
    restore_long_term_retention_backup_id: typing.Optional[builtins.str] = None,
    restore_point_in_time: typing.Optional[builtins.str] = None,
    sample_name: typing.Optional[builtins.str] = None,
    secondary_type: typing.Optional[builtins.str] = None,
    short_term_retention_policy: typing.Optional[typing.Union[MssqlDatabaseShortTermRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    sku_name: typing.Optional[builtins.str] = None,
    storage_account_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    threat_detection_policy: typing.Optional[typing.Union[MssqlDatabaseThreatDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MssqlDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transparent_data_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transparent_data_encryption_key_automatic_rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transparent_data_encryption_key_vault_key_id: typing.Optional[builtins.str] = None,
    zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__67e9650bc7d4fea45ace0aacf007f26abb25d95fe0f8584d6803e991d9bf0248(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59d116c0cfd8d2e5c86eb9b6faa6633d53568a93875eeeb463fc7e63bf05891(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a5978a94c43abe4541e528b0bb0bc3afd6a3a7178593a2daa41305a48f66d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992dec0189e77a097572f42a2dd4458b75636781e39a7b3605468bf28d3bfe47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e04478dc17d9db20f5e685cf45a5b83d7641e3d2a32b8903348259c9c3d329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29780f7a90eae92b1489cae919f9eca66b7592010267cd07a86f6080c8859ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2439198b94c7db3b9acaaeb4b996a4b14888c5222d314e685a027f50a747d7d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25744f0928c9ff16f22e6cce15b1fc7e1b18f7ad701c81a99a40378a5a6b7eb5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3e39cea2f41ebde8d0cc1786a81f985128e90ce163868020c52a7e0aa14499(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a672f80858b7d44795591a064b7cb970fe393a2a9bba52a7031dd7ed406306(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda7c2b9f57c0b19556eae4f14587eaa1a62ed5ddc2e9e075778fdda64a5d421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a44e330d2b584c3e8b089bdf21ed2c352823febaee80c439f15a48d13e04590d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d27b7afab69ce7970fe1c37c0df8a3cb5a0f47c2f7fbd8e68e7864e67b7d9a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2488a42036c92541349432bca90ea324e69cc61d9a91815e661178b3c26fd123(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cc61dd7fa5efec67b846a29246c0c321cb0737fe8e9299d6e42abe37cdc7cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471a58fc6aa584fe515be1c2779e9d2aed21ef47ae454ed2ccbd174fd8573d57(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539f3fb952897290030b7e8d2d8afa2ea3fac92a7608212bb33833e52e21e531(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83abda5e4806e57e16ab57f1b096d75ebdf28ab38cac61b1f6ca6a677252cd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3bcfee27e7414b61faace86bbda8a0c6fbf9b65ea4c5912fcd74934d0dcd24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b56d25fd24effcf39ffc6afe94207324ced2b0e2e94f18fdcc3e2aa63fd7479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbcbb425dfc0e90805b4c94521aff159740e1be0137e1f754d4105dbe8e16b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3955e2f991c8cf9f6f733728d8ece2a64bb1672f465921863ebabadcc39afac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7a0d6cf5d658007ade8bb39951324ee1c611f4006d323f7432cb40e539488e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4558cc05fd1ef95289c75eb42b1eda16839e86e7c8572201ed8e742d81723504(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6216351174bc0c689c2cebb2516fc0060d24f5ead1c6833e866539ca877120a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9d5d2445975b23e70e36c2947fd2b3755353221f49457acb057a0f4e81b040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b2aeab5dc9a82f2377e2a3ed352731e3cc57fa38ef2e3f04130fd6aa5eed58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0fc604caa35bb8ff320a6feaed2782b17c0b6c2013626ad89a81f386e007f9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72cd719aacc2501a8c71a32ce3527396b591a665834c0009e565ad3d3ee4e709(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90edda22a5917eb1409f516268ab71db990575c3869fc1c70991d8e5af11ea8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d7e425b35f23b2febefb87ce2ab67fb5828ee70aa2d65ad96fa8aef7fbe912(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dcb05a88a40ea640b274b22f4a89d2048f0a3b7ee4a9e5d65bd59998cd36a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f205f3496fa1b29eb23bd4593c059a95e2ccfcf665cd3b2203477c9ba9ca87(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    server_id: builtins.str,
    auto_pause_delay_in_minutes: typing.Optional[jsii.Number] = None,
    collation: typing.Optional[builtins.str] = None,
    create_mode: typing.Optional[builtins.str] = None,
    creation_source_database_id: typing.Optional[builtins.str] = None,
    elastic_pool_id: typing.Optional[builtins.str] = None,
    enclave_type: typing.Optional[builtins.str] = None,
    geo_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[MssqlDatabaseIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    import_: typing.Optional[typing.Union[MssqlDatabaseImport, typing.Dict[builtins.str, typing.Any]]] = None,
    ledger_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    license_type: typing.Optional[builtins.str] = None,
    long_term_retention_policy: typing.Optional[typing.Union[MssqlDatabaseLongTermRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_configuration_name: typing.Optional[builtins.str] = None,
    max_size_gb: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    read_replica_count: typing.Optional[jsii.Number] = None,
    read_scale: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_database_id: typing.Optional[builtins.str] = None,
    recovery_point_id: typing.Optional[builtins.str] = None,
    restore_dropped_database_id: typing.Optional[builtins.str] = None,
    restore_long_term_retention_backup_id: typing.Optional[builtins.str] = None,
    restore_point_in_time: typing.Optional[builtins.str] = None,
    sample_name: typing.Optional[builtins.str] = None,
    secondary_type: typing.Optional[builtins.str] = None,
    short_term_retention_policy: typing.Optional[typing.Union[MssqlDatabaseShortTermRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    sku_name: typing.Optional[builtins.str] = None,
    storage_account_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    threat_detection_policy: typing.Optional[typing.Union[MssqlDatabaseThreatDetectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[MssqlDatabaseTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transparent_data_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transparent_data_encryption_key_automatic_rotation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    transparent_data_encryption_key_vault_key_id: typing.Optional[builtins.str] = None,
    zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd1cfba0624c5a520ab5d1338e690a0d0a13713721315adb5d510d6d777b0ce(
    *,
    identity_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2577ba667f939075d1583020d2f2f7dfc3b7b32f78dbef3751ab02368a67c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c27d377e07210e82e42661b71e79eaaef7a6f4557450ea8f0365cdd79efab1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202a9766f942b7a101322514144caa8d470044522487582de96bb41c0f6c0a35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a9dda4729051be04a977aa152a78764e52143e72bed7d1a72c3b7f93bdd7172(
    value: typing.Optional[MssqlDatabaseIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca34f4f7db950e341d6bcd78037f59d4ad3c50d9ec21ff7a39316f45f748780(
    *,
    administrator_login: builtins.str,
    administrator_login_password: builtins.str,
    authentication_type: builtins.str,
    storage_key: builtins.str,
    storage_key_type: builtins.str,
    storage_uri: builtins.str,
    storage_account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce968740043b4c0c231aeb811b7ea531e1912aa80e97cc517929031d5d37526c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a5472bf263e7918ad50d123c2810d58fd1b5a4401e300b5c64050de98517f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0fa0fd08c7c6a400be07342429d064af2706c990722892b9af04d80382d4e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e468e592ae8f4400924f46c58c2a0956e9b7a1d66715e3b7a63c05769c64058(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29fe888994dacc87e584f7ad342e5dd444529b9dcbc64644eb6090e083269a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940bfebef3777fdbfcb028c56cd20d1c53e92ce3f3bf116bbd8a302ddd92686e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e91b5a2468f1706f8ba18b035f5a434353631ad7c00248533b3c8cc301fccec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0324202e22cf610e4e314338d34fb3e2176d656903db25e2ef9dbed249e862(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37a30f34baf533744ad3e7984413648442d3f16c2d9d314cd7ce1302b793a15(
    value: typing.Optional[MssqlDatabaseImport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ebff0d76cb180e40a33a243f66a64e55f9cfcb5d4f340d2b255f9076b5ea20(
    *,
    immutable_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    monthly_retention: typing.Optional[builtins.str] = None,
    weekly_retention: typing.Optional[builtins.str] = None,
    week_of_year: typing.Optional[jsii.Number] = None,
    yearly_retention: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b933ba048ab09ca163e05d1031f9c3aff4e7cde51d08e4ccc5b5501d9402df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3464ce49fe7d77c1f2430a4d7425db6023bc3083e3c7107db0b8b1fc58c12cc0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bff5692fc1f61a4a09678179dc0c0391686f6dc1c84eac857c363e03b9900b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec5fe26ba4950396de0bc3b511b9888d775972e96f25af8baf90e2bfa970514(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693d851e896832b63d32335c0d0121c0df8192348139e4b26b1cbf2e7fbea035(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b906315e108b698275ec65fabfe97f6b9d157dbc92bfe3deb288730eaeb81c4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006a6e5a84f36682ddbd3cf429111bee2ea08844a3de29ce4addb24aa203af5d(
    value: typing.Optional[MssqlDatabaseLongTermRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f0836294cdcc71c934f357a6e58ce3bca31b3fc4a34bc62ef7664dd4283120(
    *,
    retention_days: jsii.Number,
    backup_interval_in_hours: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b44bde487c1d2d3307e549ebdb22c8c6a0aafeb4e4f82c773cce2aeaa4a8b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa299e513142c82547943a8537141cb4d6e9e3cef0a254ef43c3a558df6b0e6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df289442e9b02673149eb4825d8591f913f341c0abad7316d2e97c1d24d8a207(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94995530b05fef4ff3281e60d575205807d1152a904fea464c417f6abbeaec5c(
    value: typing.Optional[MssqlDatabaseShortTermRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e98c025a6db063682ea13b3651b37663fa3a38c82a10b1d8003229d39c91c9(
    *,
    disabled_alerts: typing.Optional[typing.Sequence[builtins.str]] = None,
    email_account_admins: typing.Optional[builtins.str] = None,
    email_addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
    retention_days: typing.Optional[jsii.Number] = None,
    state: typing.Optional[builtins.str] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5cb1d46c7117286e4d0eb96e69e8854d49a506200ce70da3b1a93044b4c12ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc82230fce4a1bbb1d148dddd2f03e2b8b698883affc10fefdaaec216ec05042(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7651f1a2121a828d193ed6da9b5089f201c5a3859a8352c6fcd56a4c4603df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076a39fa1c4ddf5bfb50c568a9ab5560301bb5f33c89f6898efc9ad0051b4cbd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b672e43d670819f358754126076c010f964d0ea010ab80084df492255e54498f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe809d2e125218750bba067cb195504a7c4a60ffdb90ec6be2467ffd6c1121a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951f10b24ac728873352a2dc084c6670bce6b2783fa806d8c7c74736aac7d16e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd778ce92966699d80ac03a6eb1e74bdbf5557b8261ba76988a3ebe09b108b30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352d1246dcc9821d2c2e40778a41a2eb683453eeefc2dcd604ec1b6541c7053b(
    value: typing.Optional[MssqlDatabaseThreatDetectionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a38ae82fb23825b1f6cdd5c16c65f0e9a95c529ee4f6d2b234031cbf56ec3e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcc19d19ad318976bfe17df8462c6527061986f8aa489bebf8851d0f7d047f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7aa68a623ddfc76604c485164f2efe7875bdc0d536e8882f8b2a7bb0f9731c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3aab395bd2ce8c203e77cc0f295468e35d9b43f617821ac626ab8ea8f63f87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7a6bafa390832acae7f174de2737e348f689be71019c74ef60741a669b3cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea372a1f96399115ec2c0b232ca54c20de96fc6a046f1604cbdbd217c0816ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d766e8f7bce4cdf4f41fb6b14b1472d838cc010d57ceb9e21b0c53ea4f84f3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MssqlDatabaseTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

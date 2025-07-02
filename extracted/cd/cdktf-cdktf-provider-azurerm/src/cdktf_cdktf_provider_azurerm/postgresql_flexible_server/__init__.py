r'''
# `azurerm_postgresql_flexible_server`

Refer to the Terraform Registry for docs: [`azurerm_postgresql_flexible_server`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server).
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


class PostgresqlFlexibleServer(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServer",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server azurerm_postgresql_flexible_server}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_password: typing.Optional[builtins.str] = None,
        administrator_password_wo: typing.Optional[builtins.str] = None,
        administrator_password_wo_version: typing.Optional[jsii.Number] = None,
        authentication: typing.Optional[typing.Union["PostgresqlFlexibleServerAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup_retention_days: typing.Optional[jsii.Number] = None,
        create_mode: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[typing.Union["PostgresqlFlexibleServerCustomerManagedKey", typing.Dict[builtins.str, typing.Any]]] = None,
        delegated_subnet_id: typing.Optional[builtins.str] = None,
        geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        high_availability: typing.Optional[typing.Union["PostgresqlFlexibleServerHighAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["PostgresqlFlexibleServerIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_window: typing.Optional[typing.Union["PostgresqlFlexibleServerMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        point_in_time_restore_time_in_utc: typing.Optional[builtins.str] = None,
        private_dns_zone_id: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replication_role: typing.Optional[builtins.str] = None,
        sku_name: typing.Optional[builtins.str] = None,
        source_server_id: typing.Optional[builtins.str] = None,
        storage_mb: typing.Optional[jsii.Number] = None,
        storage_tier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PostgresqlFlexibleServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server azurerm_postgresql_flexible_server} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#location PostgresqlFlexibleServer#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#name PostgresqlFlexibleServer#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#resource_group_name PostgresqlFlexibleServer#resource_group_name}.
        :param administrator_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_login PostgresqlFlexibleServer#administrator_login}.
        :param administrator_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password PostgresqlFlexibleServer#administrator_password}.
        :param administrator_password_wo: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password_wo PostgresqlFlexibleServer#administrator_password_wo}.
        :param administrator_password_wo_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password_wo_version PostgresqlFlexibleServer#administrator_password_wo_version}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#authentication PostgresqlFlexibleServer#authentication}
        :param auto_grow_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#auto_grow_enabled PostgresqlFlexibleServer#auto_grow_enabled}.
        :param backup_retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#backup_retention_days PostgresqlFlexibleServer#backup_retention_days}.
        :param create_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#create_mode PostgresqlFlexibleServer#create_mode}.
        :param customer_managed_key: customer_managed_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#customer_managed_key PostgresqlFlexibleServer#customer_managed_key}
        :param delegated_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#delegated_subnet_id PostgresqlFlexibleServer#delegated_subnet_id}.
        :param geo_redundant_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_redundant_backup_enabled PostgresqlFlexibleServer#geo_redundant_backup_enabled}.
        :param high_availability: high_availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#high_availability PostgresqlFlexibleServer#high_availability}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#id PostgresqlFlexibleServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#identity PostgresqlFlexibleServer#identity}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#maintenance_window PostgresqlFlexibleServer#maintenance_window}
        :param point_in_time_restore_time_in_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#point_in_time_restore_time_in_utc PostgresqlFlexibleServer#point_in_time_restore_time_in_utc}.
        :param private_dns_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#private_dns_zone_id PostgresqlFlexibleServer#private_dns_zone_id}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#public_network_access_enabled PostgresqlFlexibleServer#public_network_access_enabled}.
        :param replication_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#replication_role PostgresqlFlexibleServer#replication_role}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#sku_name PostgresqlFlexibleServer#sku_name}.
        :param source_server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#source_server_id PostgresqlFlexibleServer#source_server_id}.
        :param storage_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#storage_mb PostgresqlFlexibleServer#storage_mb}.
        :param storage_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#storage_tier PostgresqlFlexibleServer#storage_tier}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#tags PostgresqlFlexibleServer#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#timeouts PostgresqlFlexibleServer#timeouts}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#version PostgresqlFlexibleServer#version}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#zone PostgresqlFlexibleServer#zone}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc016494ad6e11b17a2bee11b75586052823833f5f3c3a5d970a134faa1f483)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PostgresqlFlexibleServerConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            administrator_login=administrator_login,
            administrator_password=administrator_password,
            administrator_password_wo=administrator_password_wo,
            administrator_password_wo_version=administrator_password_wo_version,
            authentication=authentication,
            auto_grow_enabled=auto_grow_enabled,
            backup_retention_days=backup_retention_days,
            create_mode=create_mode,
            customer_managed_key=customer_managed_key,
            delegated_subnet_id=delegated_subnet_id,
            geo_redundant_backup_enabled=geo_redundant_backup_enabled,
            high_availability=high_availability,
            id=id,
            identity=identity,
            maintenance_window=maintenance_window,
            point_in_time_restore_time_in_utc=point_in_time_restore_time_in_utc,
            private_dns_zone_id=private_dns_zone_id,
            public_network_access_enabled=public_network_access_enabled,
            replication_role=replication_role,
            sku_name=sku_name,
            source_server_id=source_server_id,
            storage_mb=storage_mb,
            storage_tier=storage_tier,
            tags=tags,
            timeouts=timeouts,
            version=version,
            zone=zone,
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
        '''Generates CDKTF code for importing a PostgresqlFlexibleServer resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PostgresqlFlexibleServer to import.
        :param import_from_id: The id of the existing PostgresqlFlexibleServer that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PostgresqlFlexibleServer to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1b8431bbd15b2940d19db23904b36744e18d5d797c157f1fc8caf3f51e73bc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthentication")
    def put_authentication(
        self,
        *,
        active_directory_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param active_directory_auth_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#active_directory_auth_enabled PostgresqlFlexibleServer#active_directory_auth_enabled}.
        :param password_auth_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#password_auth_enabled PostgresqlFlexibleServer#password_auth_enabled}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#tenant_id PostgresqlFlexibleServer#tenant_id}.
        '''
        value = PostgresqlFlexibleServerAuthentication(
            active_directory_auth_enabled=active_directory_auth_enabled,
            password_auth_enabled=password_auth_enabled,
            tenant_id=tenant_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthentication", [value]))

    @jsii.member(jsii_name="putCustomerManagedKey")
    def put_customer_managed_key(
        self,
        *,
        key_vault_key_id: builtins.str,
        geo_backup_key_vault_key_id: typing.Optional[builtins.str] = None,
        geo_backup_user_assigned_identity_id: typing.Optional[builtins.str] = None,
        primary_user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#key_vault_key_id PostgresqlFlexibleServer#key_vault_key_id}.
        :param geo_backup_key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_backup_key_vault_key_id PostgresqlFlexibleServer#geo_backup_key_vault_key_id}.
        :param geo_backup_user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_backup_user_assigned_identity_id PostgresqlFlexibleServer#geo_backup_user_assigned_identity_id}.
        :param primary_user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#primary_user_assigned_identity_id PostgresqlFlexibleServer#primary_user_assigned_identity_id}.
        '''
        value = PostgresqlFlexibleServerCustomerManagedKey(
            key_vault_key_id=key_vault_key_id,
            geo_backup_key_vault_key_id=geo_backup_key_vault_key_id,
            geo_backup_user_assigned_identity_id=geo_backup_user_assigned_identity_id,
            primary_user_assigned_identity_id=primary_user_assigned_identity_id,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerManagedKey", [value]))

    @jsii.member(jsii_name="putHighAvailability")
    def put_high_availability(
        self,
        *,
        mode: builtins.str,
        standby_availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#mode PostgresqlFlexibleServer#mode}.
        :param standby_availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#standby_availability_zone PostgresqlFlexibleServer#standby_availability_zone}.
        '''
        value = PostgresqlFlexibleServerHighAvailability(
            mode=mode, standby_availability_zone=standby_availability_zone
        )

        return typing.cast(None, jsii.invoke(self, "putHighAvailability", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#type PostgresqlFlexibleServer#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#identity_ids PostgresqlFlexibleServer#identity_ids}.
        '''
        value = PostgresqlFlexibleServerIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putMaintenanceWindow")
    def put_maintenance_window(
        self,
        *,
        day_of_week: typing.Optional[jsii.Number] = None,
        start_hour: typing.Optional[jsii.Number] = None,
        start_minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#day_of_week PostgresqlFlexibleServer#day_of_week}.
        :param start_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#start_hour PostgresqlFlexibleServer#start_hour}.
        :param start_minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#start_minute PostgresqlFlexibleServer#start_minute}.
        '''
        value = PostgresqlFlexibleServerMaintenanceWindow(
            day_of_week=day_of_week, start_hour=start_hour, start_minute=start_minute
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceWindow", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#create PostgresqlFlexibleServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#delete PostgresqlFlexibleServer#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#read PostgresqlFlexibleServer#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#update PostgresqlFlexibleServer#update}.
        '''
        value = PostgresqlFlexibleServerTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdministratorLogin")
    def reset_administrator_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorLogin", []))

    @jsii.member(jsii_name="resetAdministratorPassword")
    def reset_administrator_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorPassword", []))

    @jsii.member(jsii_name="resetAdministratorPasswordWo")
    def reset_administrator_password_wo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorPasswordWo", []))

    @jsii.member(jsii_name="resetAdministratorPasswordWoVersion")
    def reset_administrator_password_wo_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministratorPasswordWoVersion", []))

    @jsii.member(jsii_name="resetAuthentication")
    def reset_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthentication", []))

    @jsii.member(jsii_name="resetAutoGrowEnabled")
    def reset_auto_grow_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoGrowEnabled", []))

    @jsii.member(jsii_name="resetBackupRetentionDays")
    def reset_backup_retention_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupRetentionDays", []))

    @jsii.member(jsii_name="resetCreateMode")
    def reset_create_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateMode", []))

    @jsii.member(jsii_name="resetCustomerManagedKey")
    def reset_customer_managed_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedKey", []))

    @jsii.member(jsii_name="resetDelegatedSubnetId")
    def reset_delegated_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelegatedSubnetId", []))

    @jsii.member(jsii_name="resetGeoRedundantBackupEnabled")
    def reset_geo_redundant_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoRedundantBackupEnabled", []))

    @jsii.member(jsii_name="resetHighAvailability")
    def reset_high_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHighAvailability", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetMaintenanceWindow")
    def reset_maintenance_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindow", []))

    @jsii.member(jsii_name="resetPointInTimeRestoreTimeInUtc")
    def reset_point_in_time_restore_time_in_utc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTimeRestoreTimeInUtc", []))

    @jsii.member(jsii_name="resetPrivateDnsZoneId")
    def reset_private_dns_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateDnsZoneId", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetReplicationRole")
    def reset_replication_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReplicationRole", []))

    @jsii.member(jsii_name="resetSkuName")
    def reset_sku_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuName", []))

    @jsii.member(jsii_name="resetSourceServerId")
    def reset_source_server_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceServerId", []))

    @jsii.member(jsii_name="resetStorageMb")
    def reset_storage_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageMb", []))

    @jsii.member(jsii_name="resetStorageTier")
    def reset_storage_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageTier", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

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
    @jsii.member(jsii_name="authentication")
    def authentication(self) -> "PostgresqlFlexibleServerAuthenticationOutputReference":
        return typing.cast("PostgresqlFlexibleServerAuthenticationOutputReference", jsii.get(self, "authentication"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKey")
    def customer_managed_key(
        self,
    ) -> "PostgresqlFlexibleServerCustomerManagedKeyOutputReference":
        return typing.cast("PostgresqlFlexibleServerCustomerManagedKeyOutputReference", jsii.get(self, "customerManagedKey"))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @builtins.property
    @jsii.member(jsii_name="highAvailability")
    def high_availability(
        self,
    ) -> "PostgresqlFlexibleServerHighAvailabilityOutputReference":
        return typing.cast("PostgresqlFlexibleServerHighAvailabilityOutputReference", jsii.get(self, "highAvailability"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "PostgresqlFlexibleServerIdentityOutputReference":
        return typing.cast("PostgresqlFlexibleServerIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindow")
    def maintenance_window(
        self,
    ) -> "PostgresqlFlexibleServerMaintenanceWindowOutputReference":
        return typing.cast("PostgresqlFlexibleServerMaintenanceWindowOutputReference", jsii.get(self, "maintenanceWindow"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PostgresqlFlexibleServerTimeoutsOutputReference":
        return typing.cast("PostgresqlFlexibleServerTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="administratorLoginInput")
    def administrator_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorPasswordInput")
    def administrator_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorPasswordWoInput")
    def administrator_password_wo_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "administratorPasswordWoInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorPasswordWoVersionInput")
    def administrator_password_wo_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "administratorPasswordWoVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationInput")
    def authentication_input(
        self,
    ) -> typing.Optional["PostgresqlFlexibleServerAuthentication"]:
        return typing.cast(typing.Optional["PostgresqlFlexibleServerAuthentication"], jsii.get(self, "authenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="autoGrowEnabledInput")
    def auto_grow_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoGrowEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDaysInput")
    def backup_retention_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "backupRetentionDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="createModeInput")
    def create_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createModeInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyInput")
    def customer_managed_key_input(
        self,
    ) -> typing.Optional["PostgresqlFlexibleServerCustomerManagedKey"]:
        return typing.cast(typing.Optional["PostgresqlFlexibleServerCustomerManagedKey"], jsii.get(self, "customerManagedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="delegatedSubnetIdInput")
    def delegated_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delegatedSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="geoRedundantBackupEnabledInput")
    def geo_redundant_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "geoRedundantBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="highAvailabilityInput")
    def high_availability_input(
        self,
    ) -> typing.Optional["PostgresqlFlexibleServerHighAvailability"]:
        return typing.cast(typing.Optional["PostgresqlFlexibleServerHighAvailability"], jsii.get(self, "highAvailabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["PostgresqlFlexibleServerIdentity"]:
        return typing.cast(typing.Optional["PostgresqlFlexibleServerIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowInput")
    def maintenance_window_input(
        self,
    ) -> typing.Optional["PostgresqlFlexibleServerMaintenanceWindow"]:
        return typing.cast(typing.Optional["PostgresqlFlexibleServerMaintenanceWindow"], jsii.get(self, "maintenanceWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRestoreTimeInUtcInput")
    def point_in_time_restore_time_in_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pointInTimeRestoreTimeInUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="privateDnsZoneIdInput")
    def private_dns_zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateDnsZoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationRoleInput")
    def replication_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceServerIdInput")
    def source_server_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceServerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageMbInput")
    def storage_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageMbInput"))

    @builtins.property
    @jsii.member(jsii_name="storageTierInput")
    def storage_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageTierInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PostgresqlFlexibleServerTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PostgresqlFlexibleServerTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="administratorLogin")
    def administrator_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorLogin"))

    @administrator_login.setter
    def administrator_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335a92c1d8d238338a5e3d2411b4d69b24bbbbcee35e12b7df3b2b6e80b89f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorLogin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administratorPassword")
    def administrator_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorPassword"))

    @administrator_password.setter
    def administrator_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a2c9d8bb2572134a01582fddd8f07b2d58da099327c86c86ce1f38a14331cda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administratorPasswordWo")
    def administrator_password_wo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "administratorPasswordWo"))

    @administrator_password_wo.setter
    def administrator_password_wo(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382416965dd3b911e1b55e7658a066ce1d60f8c18f2da802a32676d0cbb09726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorPasswordWo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="administratorPasswordWoVersion")
    def administrator_password_wo_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "administratorPasswordWoVersion"))

    @administrator_password_wo_version.setter
    def administrator_password_wo_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f1972b7af8509ba4b7f292a0eb05f4b6964c6f6ab4c36b93b817e8cce48ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administratorPasswordWoVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoGrowEnabled")
    def auto_grow_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoGrowEnabled"))

    @auto_grow_enabled.setter
    def auto_grow_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e6724371bef5b21ea88b9ae053bb77925be6ba6f1b224139c81430afbf9f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoGrowEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupRetentionDays")
    def backup_retention_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "backupRetentionDays"))

    @backup_retention_days.setter
    def backup_retention_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c33939264eacfd1cd5de23c118f78079462df468ff20dc68b5e4f20e647772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupRetentionDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="createMode")
    def create_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createMode"))

    @create_mode.setter
    def create_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea4bc2c1a201c9700f86cb9f0fccb7be33011a40e610177ae1ea948b82ae4a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "createMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delegatedSubnetId")
    def delegated_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delegatedSubnetId"))

    @delegated_subnet_id.setter
    def delegated_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c198af550df5fff499ec03576a97ade0828dbc91e19455a75090df65f9df895)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delegatedSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geoRedundantBackupEnabled")
    def geo_redundant_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "geoRedundantBackupEnabled"))

    @geo_redundant_backup_enabled.setter
    def geo_redundant_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487214db9d0f38861aefad4ad5ea0f772b52b1de56a8ead9d0f5c92a5c1c74f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoRedundantBackupEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a17403cc8f17253464886e734e33307f069474fe64af3ebbb8d0890ea2f901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7664f9da1cae32f83c70d1d1899b0fd2959f24f2ab05c21c3138566ca15b16e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8bb0fd0d1006e4cbae68c4e0b5c9be434ebc3ed624d5fc36eb51865930f7ed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pointInTimeRestoreTimeInUtc")
    def point_in_time_restore_time_in_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pointInTimeRestoreTimeInUtc"))

    @point_in_time_restore_time_in_utc.setter
    def point_in_time_restore_time_in_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b841268f6d581e794eb25ed48b3844d936cb76ab805555791f15d02e391ef10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeRestoreTimeInUtc", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateDnsZoneId")
    def private_dns_zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateDnsZoneId"))

    @private_dns_zone_id.setter
    def private_dns_zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1846fde8f4f32df1bd17afe42c5c0d775553490ee77160b725c2d1c5b421272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateDnsZoneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fe1f36a774a4045640092abc7845bdb902489a679c260d81efba7deec5e10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationRole")
    def replication_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationRole"))

    @replication_role.setter
    def replication_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ae999707d011e85d43489f78434fc1e0bdf5a0f2cd75e725cdb9de8e659e72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__340cef0e8ee0ca6d18cc12f00777290da4deda55077a7219438d4d679f4dffa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1670d9a05fbb52068f10d683fd2471fa65a10928c5b2b5527abcc9b53b655f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceServerId")
    def source_server_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceServerId"))

    @source_server_id.setter
    def source_server_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b64d0749db276fa2d20d823d1911ce915ef770a70b87047291979315ba8b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceServerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageMb")
    def storage_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageMb"))

    @storage_mb.setter
    def storage_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c988ff9aec74994dc49ae31bbddb0ddc16c24ac69aadfabaa1c1a6c34effbc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageTier")
    def storage_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageTier"))

    @storage_tier.setter
    def storage_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8b0ca32ee13f06336604a84e25cf5545479661eee2749c22e3b57a9610139d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099fa272133fbfa5f768b0dbbb3ad6fa442583c35a95fb5a2947497d4a5a9802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd88bd1607be06c79895c7e408e6b0b25fe5a50fc23c2055db92ef3a55191109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a9e2e84ba23e9708ee80c7d725ca86202d500bf8e95257f9dd292a400b2053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "active_directory_auth_enabled": "activeDirectoryAuthEnabled",
        "password_auth_enabled": "passwordAuthEnabled",
        "tenant_id": "tenantId",
    },
)
class PostgresqlFlexibleServerAuthentication:
    def __init__(
        self,
        *,
        active_directory_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param active_directory_auth_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#active_directory_auth_enabled PostgresqlFlexibleServer#active_directory_auth_enabled}.
        :param password_auth_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#password_auth_enabled PostgresqlFlexibleServer#password_auth_enabled}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#tenant_id PostgresqlFlexibleServer#tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e912a69aa940d5cdd3c29ac564b3fa6467bcf1a61e9a4808251af6b342465c)
            check_type(argname="argument active_directory_auth_enabled", value=active_directory_auth_enabled, expected_type=type_hints["active_directory_auth_enabled"])
            check_type(argname="argument password_auth_enabled", value=password_auth_enabled, expected_type=type_hints["password_auth_enabled"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_directory_auth_enabled is not None:
            self._values["active_directory_auth_enabled"] = active_directory_auth_enabled
        if password_auth_enabled is not None:
            self._values["password_auth_enabled"] = password_auth_enabled
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id

    @builtins.property
    def active_directory_auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#active_directory_auth_enabled PostgresqlFlexibleServer#active_directory_auth_enabled}.'''
        result = self._values.get("active_directory_auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password_auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#password_auth_enabled PostgresqlFlexibleServer#password_auth_enabled}.'''
        result = self._values.get("password_auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#tenant_id PostgresqlFlexibleServer#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlFlexibleServerAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PostgresqlFlexibleServerAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3d5f65cf8470253bb61c1cec7b6f81aeefff9940d47fcbb6701e73ec07fe9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActiveDirectoryAuthEnabled")
    def reset_active_directory_auth_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryAuthEnabled", []))

    @jsii.member(jsii_name="resetPasswordAuthEnabled")
    def reset_password_auth_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPasswordAuthEnabled", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryAuthEnabledInput")
    def active_directory_auth_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeDirectoryAuthEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordAuthEnabledInput")
    def password_auth_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "passwordAuthEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryAuthEnabled")
    def active_directory_auth_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "activeDirectoryAuthEnabled"))

    @active_directory_auth_enabled.setter
    def active_directory_auth_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9adb50fdd022ee3708c0e6c58110b9851ea990a11fb651ca17df4637fe062ebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "activeDirectoryAuthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordAuthEnabled")
    def password_auth_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "passwordAuthEnabled"))

    @password_auth_enabled.setter
    def password_auth_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9f42b9203b2d10c60e658c073de8db02ca3c3016e4e751940e75c9bf419f69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordAuthEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c170e0af5f70866bbc9d43e8d8af058db6358ce2855a1560232831729c6052b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PostgresqlFlexibleServerAuthentication]:
        return typing.cast(typing.Optional[PostgresqlFlexibleServerAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PostgresqlFlexibleServerAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86289863456335af101d71a64d4e541bffec1a16b833de61dce37e8158bbb1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "administrator_login": "administratorLogin",
        "administrator_password": "administratorPassword",
        "administrator_password_wo": "administratorPasswordWo",
        "administrator_password_wo_version": "administratorPasswordWoVersion",
        "authentication": "authentication",
        "auto_grow_enabled": "autoGrowEnabled",
        "backup_retention_days": "backupRetentionDays",
        "create_mode": "createMode",
        "customer_managed_key": "customerManagedKey",
        "delegated_subnet_id": "delegatedSubnetId",
        "geo_redundant_backup_enabled": "geoRedundantBackupEnabled",
        "high_availability": "highAvailability",
        "id": "id",
        "identity": "identity",
        "maintenance_window": "maintenanceWindow",
        "point_in_time_restore_time_in_utc": "pointInTimeRestoreTimeInUtc",
        "private_dns_zone_id": "privateDnsZoneId",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "replication_role": "replicationRole",
        "sku_name": "skuName",
        "source_server_id": "sourceServerId",
        "storage_mb": "storageMb",
        "storage_tier": "storageTier",
        "tags": "tags",
        "timeouts": "timeouts",
        "version": "version",
        "zone": "zone",
    },
)
class PostgresqlFlexibleServerConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        administrator_login: typing.Optional[builtins.str] = None,
        administrator_password: typing.Optional[builtins.str] = None,
        administrator_password_wo: typing.Optional[builtins.str] = None,
        administrator_password_wo_version: typing.Optional[jsii.Number] = None,
        authentication: typing.Optional[typing.Union[PostgresqlFlexibleServerAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup_retention_days: typing.Optional[jsii.Number] = None,
        create_mode: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[typing.Union["PostgresqlFlexibleServerCustomerManagedKey", typing.Dict[builtins.str, typing.Any]]] = None,
        delegated_subnet_id: typing.Optional[builtins.str] = None,
        geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        high_availability: typing.Optional[typing.Union["PostgresqlFlexibleServerHighAvailability", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["PostgresqlFlexibleServerIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_window: typing.Optional[typing.Union["PostgresqlFlexibleServerMaintenanceWindow", typing.Dict[builtins.str, typing.Any]]] = None,
        point_in_time_restore_time_in_utc: typing.Optional[builtins.str] = None,
        private_dns_zone_id: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        replication_role: typing.Optional[builtins.str] = None,
        sku_name: typing.Optional[builtins.str] = None,
        source_server_id: typing.Optional[builtins.str] = None,
        storage_mb: typing.Optional[jsii.Number] = None,
        storage_tier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PostgresqlFlexibleServerTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#location PostgresqlFlexibleServer#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#name PostgresqlFlexibleServer#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#resource_group_name PostgresqlFlexibleServer#resource_group_name}.
        :param administrator_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_login PostgresqlFlexibleServer#administrator_login}.
        :param administrator_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password PostgresqlFlexibleServer#administrator_password}.
        :param administrator_password_wo: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password_wo PostgresqlFlexibleServer#administrator_password_wo}.
        :param administrator_password_wo_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password_wo_version PostgresqlFlexibleServer#administrator_password_wo_version}.
        :param authentication: authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#authentication PostgresqlFlexibleServer#authentication}
        :param auto_grow_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#auto_grow_enabled PostgresqlFlexibleServer#auto_grow_enabled}.
        :param backup_retention_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#backup_retention_days PostgresqlFlexibleServer#backup_retention_days}.
        :param create_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#create_mode PostgresqlFlexibleServer#create_mode}.
        :param customer_managed_key: customer_managed_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#customer_managed_key PostgresqlFlexibleServer#customer_managed_key}
        :param delegated_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#delegated_subnet_id PostgresqlFlexibleServer#delegated_subnet_id}.
        :param geo_redundant_backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_redundant_backup_enabled PostgresqlFlexibleServer#geo_redundant_backup_enabled}.
        :param high_availability: high_availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#high_availability PostgresqlFlexibleServer#high_availability}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#id PostgresqlFlexibleServer#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#identity PostgresqlFlexibleServer#identity}
        :param maintenance_window: maintenance_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#maintenance_window PostgresqlFlexibleServer#maintenance_window}
        :param point_in_time_restore_time_in_utc: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#point_in_time_restore_time_in_utc PostgresqlFlexibleServer#point_in_time_restore_time_in_utc}.
        :param private_dns_zone_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#private_dns_zone_id PostgresqlFlexibleServer#private_dns_zone_id}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#public_network_access_enabled PostgresqlFlexibleServer#public_network_access_enabled}.
        :param replication_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#replication_role PostgresqlFlexibleServer#replication_role}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#sku_name PostgresqlFlexibleServer#sku_name}.
        :param source_server_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#source_server_id PostgresqlFlexibleServer#source_server_id}.
        :param storage_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#storage_mb PostgresqlFlexibleServer#storage_mb}.
        :param storage_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#storage_tier PostgresqlFlexibleServer#storage_tier}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#tags PostgresqlFlexibleServer#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#timeouts PostgresqlFlexibleServer#timeouts}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#version PostgresqlFlexibleServer#version}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#zone PostgresqlFlexibleServer#zone}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(authentication, dict):
            authentication = PostgresqlFlexibleServerAuthentication(**authentication)
        if isinstance(customer_managed_key, dict):
            customer_managed_key = PostgresqlFlexibleServerCustomerManagedKey(**customer_managed_key)
        if isinstance(high_availability, dict):
            high_availability = PostgresqlFlexibleServerHighAvailability(**high_availability)
        if isinstance(identity, dict):
            identity = PostgresqlFlexibleServerIdentity(**identity)
        if isinstance(maintenance_window, dict):
            maintenance_window = PostgresqlFlexibleServerMaintenanceWindow(**maintenance_window)
        if isinstance(timeouts, dict):
            timeouts = PostgresqlFlexibleServerTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34cd8bacf42e143fb2a537691b5b31c415744c9de22a9acb4972a6472a36103f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument administrator_login", value=administrator_login, expected_type=type_hints["administrator_login"])
            check_type(argname="argument administrator_password", value=administrator_password, expected_type=type_hints["administrator_password"])
            check_type(argname="argument administrator_password_wo", value=administrator_password_wo, expected_type=type_hints["administrator_password_wo"])
            check_type(argname="argument administrator_password_wo_version", value=administrator_password_wo_version, expected_type=type_hints["administrator_password_wo_version"])
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument auto_grow_enabled", value=auto_grow_enabled, expected_type=type_hints["auto_grow_enabled"])
            check_type(argname="argument backup_retention_days", value=backup_retention_days, expected_type=type_hints["backup_retention_days"])
            check_type(argname="argument create_mode", value=create_mode, expected_type=type_hints["create_mode"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument delegated_subnet_id", value=delegated_subnet_id, expected_type=type_hints["delegated_subnet_id"])
            check_type(argname="argument geo_redundant_backup_enabled", value=geo_redundant_backup_enabled, expected_type=type_hints["geo_redundant_backup_enabled"])
            check_type(argname="argument high_availability", value=high_availability, expected_type=type_hints["high_availability"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument maintenance_window", value=maintenance_window, expected_type=type_hints["maintenance_window"])
            check_type(argname="argument point_in_time_restore_time_in_utc", value=point_in_time_restore_time_in_utc, expected_type=type_hints["point_in_time_restore_time_in_utc"])
            check_type(argname="argument private_dns_zone_id", value=private_dns_zone_id, expected_type=type_hints["private_dns_zone_id"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument replication_role", value=replication_role, expected_type=type_hints["replication_role"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument source_server_id", value=source_server_id, expected_type=type_hints["source_server_id"])
            check_type(argname="argument storage_mb", value=storage_mb, expected_type=type_hints["storage_mb"])
            check_type(argname="argument storage_tier", value=storage_tier, expected_type=type_hints["storage_tier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if administrator_login is not None:
            self._values["administrator_login"] = administrator_login
        if administrator_password is not None:
            self._values["administrator_password"] = administrator_password
        if administrator_password_wo is not None:
            self._values["administrator_password_wo"] = administrator_password_wo
        if administrator_password_wo_version is not None:
            self._values["administrator_password_wo_version"] = administrator_password_wo_version
        if authentication is not None:
            self._values["authentication"] = authentication
        if auto_grow_enabled is not None:
            self._values["auto_grow_enabled"] = auto_grow_enabled
        if backup_retention_days is not None:
            self._values["backup_retention_days"] = backup_retention_days
        if create_mode is not None:
            self._values["create_mode"] = create_mode
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if delegated_subnet_id is not None:
            self._values["delegated_subnet_id"] = delegated_subnet_id
        if geo_redundant_backup_enabled is not None:
            self._values["geo_redundant_backup_enabled"] = geo_redundant_backup_enabled
        if high_availability is not None:
            self._values["high_availability"] = high_availability
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if maintenance_window is not None:
            self._values["maintenance_window"] = maintenance_window
        if point_in_time_restore_time_in_utc is not None:
            self._values["point_in_time_restore_time_in_utc"] = point_in_time_restore_time_in_utc
        if private_dns_zone_id is not None:
            self._values["private_dns_zone_id"] = private_dns_zone_id
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if replication_role is not None:
            self._values["replication_role"] = replication_role
        if sku_name is not None:
            self._values["sku_name"] = sku_name
        if source_server_id is not None:
            self._values["source_server_id"] = source_server_id
        if storage_mb is not None:
            self._values["storage_mb"] = storage_mb
        if storage_tier is not None:
            self._values["storage_tier"] = storage_tier
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version
        if zone is not None:
            self._values["zone"] = zone

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#location PostgresqlFlexibleServer#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#name PostgresqlFlexibleServer#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#resource_group_name PostgresqlFlexibleServer#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrator_login(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_login PostgresqlFlexibleServer#administrator_login}.'''
        result = self._values.get("administrator_login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def administrator_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password PostgresqlFlexibleServer#administrator_password}.'''
        result = self._values.get("administrator_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def administrator_password_wo(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password_wo PostgresqlFlexibleServer#administrator_password_wo}.'''
        result = self._values.get("administrator_password_wo")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def administrator_password_wo_version(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#administrator_password_wo_version PostgresqlFlexibleServer#administrator_password_wo_version}.'''
        result = self._values.get("administrator_password_wo_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def authentication(self) -> typing.Optional[PostgresqlFlexibleServerAuthentication]:
        '''authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#authentication PostgresqlFlexibleServer#authentication}
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[PostgresqlFlexibleServerAuthentication], result)

    @builtins.property
    def auto_grow_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#auto_grow_enabled PostgresqlFlexibleServer#auto_grow_enabled}.'''
        result = self._values.get("auto_grow_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backup_retention_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#backup_retention_days PostgresqlFlexibleServer#backup_retention_days}.'''
        result = self._values.get("backup_retention_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def create_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#create_mode PostgresqlFlexibleServer#create_mode}.'''
        result = self._values.get("create_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_managed_key(
        self,
    ) -> typing.Optional["PostgresqlFlexibleServerCustomerManagedKey"]:
        '''customer_managed_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#customer_managed_key PostgresqlFlexibleServer#customer_managed_key}
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional["PostgresqlFlexibleServerCustomerManagedKey"], result)

    @builtins.property
    def delegated_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#delegated_subnet_id PostgresqlFlexibleServer#delegated_subnet_id}.'''
        result = self._values.get("delegated_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geo_redundant_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_redundant_backup_enabled PostgresqlFlexibleServer#geo_redundant_backup_enabled}.'''
        result = self._values.get("geo_redundant_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def high_availability(
        self,
    ) -> typing.Optional["PostgresqlFlexibleServerHighAvailability"]:
        '''high_availability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#high_availability PostgresqlFlexibleServer#high_availability}
        '''
        result = self._values.get("high_availability")
        return typing.cast(typing.Optional["PostgresqlFlexibleServerHighAvailability"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#id PostgresqlFlexibleServer#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["PostgresqlFlexibleServerIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#identity PostgresqlFlexibleServer#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["PostgresqlFlexibleServerIdentity"], result)

    @builtins.property
    def maintenance_window(
        self,
    ) -> typing.Optional["PostgresqlFlexibleServerMaintenanceWindow"]:
        '''maintenance_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#maintenance_window PostgresqlFlexibleServer#maintenance_window}
        '''
        result = self._values.get("maintenance_window")
        return typing.cast(typing.Optional["PostgresqlFlexibleServerMaintenanceWindow"], result)

    @builtins.property
    def point_in_time_restore_time_in_utc(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#point_in_time_restore_time_in_utc PostgresqlFlexibleServer#point_in_time_restore_time_in_utc}.'''
        result = self._values.get("point_in_time_restore_time_in_utc")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_dns_zone_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#private_dns_zone_id PostgresqlFlexibleServer#private_dns_zone_id}.'''
        result = self._values.get("private_dns_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#public_network_access_enabled PostgresqlFlexibleServer#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def replication_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#replication_role PostgresqlFlexibleServer#replication_role}.'''
        result = self._values.get("replication_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#sku_name PostgresqlFlexibleServer#sku_name}.'''
        result = self._values.get("sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_server_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#source_server_id PostgresqlFlexibleServer#source_server_id}.'''
        result = self._values.get("source_server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#storage_mb PostgresqlFlexibleServer#storage_mb}.'''
        result = self._values.get("storage_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#storage_tier PostgresqlFlexibleServer#storage_tier}.'''
        result = self._values.get("storage_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#tags PostgresqlFlexibleServer#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PostgresqlFlexibleServerTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#timeouts PostgresqlFlexibleServer#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PostgresqlFlexibleServerTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#version PostgresqlFlexibleServer#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#zone PostgresqlFlexibleServer#zone}.'''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlFlexibleServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerCustomerManagedKey",
    jsii_struct_bases=[],
    name_mapping={
        "key_vault_key_id": "keyVaultKeyId",
        "geo_backup_key_vault_key_id": "geoBackupKeyVaultKeyId",
        "geo_backup_user_assigned_identity_id": "geoBackupUserAssignedIdentityId",
        "primary_user_assigned_identity_id": "primaryUserAssignedIdentityId",
    },
)
class PostgresqlFlexibleServerCustomerManagedKey:
    def __init__(
        self,
        *,
        key_vault_key_id: builtins.str,
        geo_backup_key_vault_key_id: typing.Optional[builtins.str] = None,
        geo_backup_user_assigned_identity_id: typing.Optional[builtins.str] = None,
        primary_user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#key_vault_key_id PostgresqlFlexibleServer#key_vault_key_id}.
        :param geo_backup_key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_backup_key_vault_key_id PostgresqlFlexibleServer#geo_backup_key_vault_key_id}.
        :param geo_backup_user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_backup_user_assigned_identity_id PostgresqlFlexibleServer#geo_backup_user_assigned_identity_id}.
        :param primary_user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#primary_user_assigned_identity_id PostgresqlFlexibleServer#primary_user_assigned_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfce5724d35daf37f9c234bbebba31f59ac75df367908729d662542e60a21fca)
            check_type(argname="argument key_vault_key_id", value=key_vault_key_id, expected_type=type_hints["key_vault_key_id"])
            check_type(argname="argument geo_backup_key_vault_key_id", value=geo_backup_key_vault_key_id, expected_type=type_hints["geo_backup_key_vault_key_id"])
            check_type(argname="argument geo_backup_user_assigned_identity_id", value=geo_backup_user_assigned_identity_id, expected_type=type_hints["geo_backup_user_assigned_identity_id"])
            check_type(argname="argument primary_user_assigned_identity_id", value=primary_user_assigned_identity_id, expected_type=type_hints["primary_user_assigned_identity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_vault_key_id": key_vault_key_id,
        }
        if geo_backup_key_vault_key_id is not None:
            self._values["geo_backup_key_vault_key_id"] = geo_backup_key_vault_key_id
        if geo_backup_user_assigned_identity_id is not None:
            self._values["geo_backup_user_assigned_identity_id"] = geo_backup_user_assigned_identity_id
        if primary_user_assigned_identity_id is not None:
            self._values["primary_user_assigned_identity_id"] = primary_user_assigned_identity_id

    @builtins.property
    def key_vault_key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#key_vault_key_id PostgresqlFlexibleServer#key_vault_key_id}.'''
        result = self._values.get("key_vault_key_id")
        assert result is not None, "Required property 'key_vault_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def geo_backup_key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_backup_key_vault_key_id PostgresqlFlexibleServer#geo_backup_key_vault_key_id}.'''
        result = self._values.get("geo_backup_key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geo_backup_user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#geo_backup_user_assigned_identity_id PostgresqlFlexibleServer#geo_backup_user_assigned_identity_id}.'''
        result = self._values.get("geo_backup_user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary_user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#primary_user_assigned_identity_id PostgresqlFlexibleServer#primary_user_assigned_identity_id}.'''
        result = self._values.get("primary_user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlFlexibleServerCustomerManagedKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PostgresqlFlexibleServerCustomerManagedKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerCustomerManagedKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c69e4d21fb7115a68071f7571df682d54362f561243d405b2b25852e77107bf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeoBackupKeyVaultKeyId")
    def reset_geo_backup_key_vault_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoBackupKeyVaultKeyId", []))

    @jsii.member(jsii_name="resetGeoBackupUserAssignedIdentityId")
    def reset_geo_backup_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoBackupUserAssignedIdentityId", []))

    @jsii.member(jsii_name="resetPrimaryUserAssignedIdentityId")
    def reset_primary_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryUserAssignedIdentityId", []))

    @builtins.property
    @jsii.member(jsii_name="geoBackupKeyVaultKeyIdInput")
    def geo_backup_key_vault_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geoBackupKeyVaultKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="geoBackupUserAssignedIdentityIdInput")
    def geo_backup_user_assigned_identity_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "geoBackupUserAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyIdInput")
    def key_vault_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryUserAssignedIdentityIdInput")
    def primary_user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "primaryUserAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="geoBackupKeyVaultKeyId")
    def geo_backup_key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geoBackupKeyVaultKeyId"))

    @geo_backup_key_vault_key_id.setter
    def geo_backup_key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fdc8b3ccd3f10a782a0f76d193d2225e476352f34f6c73907d0be819d9f40bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoBackupKeyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="geoBackupUserAssignedIdentityId")
    def geo_backup_user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "geoBackupUserAssignedIdentityId"))

    @geo_backup_user_assigned_identity_id.setter
    def geo_backup_user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662858f9420b2183fe0dd3a56b35af30b9e0c650e4826a131ee4e92488031a49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "geoBackupUserAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyId")
    def key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultKeyId"))

    @key_vault_key_id.setter
    def key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b2621f457e9791368e20b324ccbfaf98b39b089809703fdab475e12cba62f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="primaryUserAssignedIdentityId")
    def primary_user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryUserAssignedIdentityId"))

    @primary_user_assigned_identity_id.setter
    def primary_user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc8af3e0da1aef7179f53e7c3c39bee9cebbcb56b1b504a949980d4dfa610a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryUserAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PostgresqlFlexibleServerCustomerManagedKey]:
        return typing.cast(typing.Optional[PostgresqlFlexibleServerCustomerManagedKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PostgresqlFlexibleServerCustomerManagedKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446068452c0a583f83bc62b8879c6e1b4cca52f21a733d1b20eb7dd6c3ab11b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerHighAvailability",
    jsii_struct_bases=[],
    name_mapping={
        "mode": "mode",
        "standby_availability_zone": "standbyAvailabilityZone",
    },
)
class PostgresqlFlexibleServerHighAvailability:
    def __init__(
        self,
        *,
        mode: builtins.str,
        standby_availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#mode PostgresqlFlexibleServer#mode}.
        :param standby_availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#standby_availability_zone PostgresqlFlexibleServer#standby_availability_zone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44dd0c8c276844cd87b639713995fcc8b5e26140c4d12e10609c2e5c499e315e)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument standby_availability_zone", value=standby_availability_zone, expected_type=type_hints["standby_availability_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if standby_availability_zone is not None:
            self._values["standby_availability_zone"] = standby_availability_zone

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#mode PostgresqlFlexibleServer#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def standby_availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#standby_availability_zone PostgresqlFlexibleServer#standby_availability_zone}.'''
        result = self._values.get("standby_availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlFlexibleServerHighAvailability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PostgresqlFlexibleServerHighAvailabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerHighAvailabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__250b05827dfad1c0d15f66b068dfa8409243ea58524db3fb4d3140e74991a87e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetStandbyAvailabilityZone")
    def reset_standby_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStandbyAvailabilityZone", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="standbyAvailabilityZoneInput")
    def standby_availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "standbyAvailabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594b66b54607cf8ef364da551fe3de396b8cc24715ead4b2b33ac8aa7b6e4136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="standbyAvailabilityZone")
    def standby_availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standbyAvailabilityZone"))

    @standby_availability_zone.setter
    def standby_availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8648b6a27234753a74d43fd158cc90cd4457db67ed858e72a1196d553326c89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standbyAvailabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PostgresqlFlexibleServerHighAvailability]:
        return typing.cast(typing.Optional[PostgresqlFlexibleServerHighAvailability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PostgresqlFlexibleServerHighAvailability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ed66ecb77f8a291757bc73b0c24acd3fa1eb55e5bca4eb6182d7a4de133295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class PostgresqlFlexibleServerIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#type PostgresqlFlexibleServer#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#identity_ids PostgresqlFlexibleServer#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8def3f8ee349f87dc0919a4cb5a9826bc2b8846f43e8dd7b78685a45a04fba26)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#type PostgresqlFlexibleServer#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#identity_ids PostgresqlFlexibleServer#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlFlexibleServerIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PostgresqlFlexibleServerIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6118f6a05dd45d42a8e75146a63c205566b1ede2ad5cd23d41b00db87af0a2c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d9c17f8a07514e50d9550b0792863ea417577449cde4a10c6c124961379c1bfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684635080bbb08fd62211f71a48d4f2565470497baf659bd68415fc89d96750b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[PostgresqlFlexibleServerIdentity]:
        return typing.cast(typing.Optional[PostgresqlFlexibleServerIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PostgresqlFlexibleServerIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18cbbcbf9bed466993bf534eb4f306fcc40be570da6f25df96359ba5e8c1d86e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerMaintenanceWindow",
    jsii_struct_bases=[],
    name_mapping={
        "day_of_week": "dayOfWeek",
        "start_hour": "startHour",
        "start_minute": "startMinute",
    },
)
class PostgresqlFlexibleServerMaintenanceWindow:
    def __init__(
        self,
        *,
        day_of_week: typing.Optional[jsii.Number] = None,
        start_hour: typing.Optional[jsii.Number] = None,
        start_minute: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#day_of_week PostgresqlFlexibleServer#day_of_week}.
        :param start_hour: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#start_hour PostgresqlFlexibleServer#start_hour}.
        :param start_minute: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#start_minute PostgresqlFlexibleServer#start_minute}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31f48b5a5c381743efc49af92a2677b9a9c9f95bcaa43ce80d1a8784478287a)
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument start_hour", value=start_hour, expected_type=type_hints["start_hour"])
            check_type(argname="argument start_minute", value=start_minute, expected_type=type_hints["start_minute"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day_of_week is not None:
            self._values["day_of_week"] = day_of_week
        if start_hour is not None:
            self._values["start_hour"] = start_hour
        if start_minute is not None:
            self._values["start_minute"] = start_minute

    @builtins.property
    def day_of_week(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#day_of_week PostgresqlFlexibleServer#day_of_week}.'''
        result = self._values.get("day_of_week")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_hour(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#start_hour PostgresqlFlexibleServer#start_hour}.'''
        result = self._values.get("start_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_minute(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#start_minute PostgresqlFlexibleServer#start_minute}.'''
        result = self._values.get("start_minute")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlFlexibleServerMaintenanceWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PostgresqlFlexibleServerMaintenanceWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerMaintenanceWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fad219bfd90934020ca0813f15b740980397089171cbcfb3f8a78ff84a62537)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDayOfWeek")
    def reset_day_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayOfWeek", []))

    @jsii.member(jsii_name="resetStartHour")
    def reset_start_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartHour", []))

    @jsii.member(jsii_name="resetStartMinute")
    def reset_start_minute(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartMinute", []))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="startHourInput")
    def start_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startHourInput"))

    @builtins.property
    @jsii.member(jsii_name="startMinuteInput")
    def start_minute_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startMinuteInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a989b31c3166097d83ca63714fc1eab19abfc925e4bdede7380aa01e425a972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startHour")
    def start_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startHour"))

    @start_hour.setter
    def start_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfbb0119734276336da2ce33855a07d4759ee33aa59dd85ddac159af68b8411d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startMinute")
    def start_minute(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startMinute"))

    @start_minute.setter
    def start_minute(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__804e2587db42fe70a60198834ae0f4cadd34519b610fcfff49e6348fb8800b14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startMinute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PostgresqlFlexibleServerMaintenanceWindow]:
        return typing.cast(typing.Optional[PostgresqlFlexibleServerMaintenanceWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PostgresqlFlexibleServerMaintenanceWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aea28d87ea130b595c5dc575224a5168a1c7157eec67dc0eeba6097e20f713f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class PostgresqlFlexibleServerTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#create PostgresqlFlexibleServer#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#delete PostgresqlFlexibleServer#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#read PostgresqlFlexibleServer#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#update PostgresqlFlexibleServer#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a3be7f42b349eff9641121c2a24c5dba9cf3c52858a1a9533fe2be0103773ce)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#create PostgresqlFlexibleServer#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#delete PostgresqlFlexibleServer#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#read PostgresqlFlexibleServer#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/postgresql_flexible_server#update PostgresqlFlexibleServer#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresqlFlexibleServerTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PostgresqlFlexibleServerTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.postgresqlFlexibleServer.PostgresqlFlexibleServerTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9511d7dd17f86303a2781678e3d362b9e04bd7c53622b2117c8d62fc394165a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e34fc33259b93a4a23d530d0d7f7a1a8fd83d1193fa0cbc7b01854991f121ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf539f4eb1315fb27e904a919c02406f42b65c1640eeab9d36c5762166c0b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9532c3757c94b789ee972c0303147d825c83fe4481422f44d402d6630dcc2383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__151fdb9758535a4b168bb6c3de3614eeea45afc6b1537459a0d4c00a5b103c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PostgresqlFlexibleServerTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PostgresqlFlexibleServerTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PostgresqlFlexibleServerTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c4299dd6bec5cf53248d4aa2be596a2d6cc37ab850e04ef9ce6d12a0eb7f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PostgresqlFlexibleServer",
    "PostgresqlFlexibleServerAuthentication",
    "PostgresqlFlexibleServerAuthenticationOutputReference",
    "PostgresqlFlexibleServerConfig",
    "PostgresqlFlexibleServerCustomerManagedKey",
    "PostgresqlFlexibleServerCustomerManagedKeyOutputReference",
    "PostgresqlFlexibleServerHighAvailability",
    "PostgresqlFlexibleServerHighAvailabilityOutputReference",
    "PostgresqlFlexibleServerIdentity",
    "PostgresqlFlexibleServerIdentityOutputReference",
    "PostgresqlFlexibleServerMaintenanceWindow",
    "PostgresqlFlexibleServerMaintenanceWindowOutputReference",
    "PostgresqlFlexibleServerTimeouts",
    "PostgresqlFlexibleServerTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3fc016494ad6e11b17a2bee11b75586052823833f5f3c3a5d970a134faa1f483(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    administrator_login: typing.Optional[builtins.str] = None,
    administrator_password: typing.Optional[builtins.str] = None,
    administrator_password_wo: typing.Optional[builtins.str] = None,
    administrator_password_wo_version: typing.Optional[jsii.Number] = None,
    authentication: typing.Optional[typing.Union[PostgresqlFlexibleServerAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup_retention_days: typing.Optional[jsii.Number] = None,
    create_mode: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[typing.Union[PostgresqlFlexibleServerCustomerManagedKey, typing.Dict[builtins.str, typing.Any]]] = None,
    delegated_subnet_id: typing.Optional[builtins.str] = None,
    geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    high_availability: typing.Optional[typing.Union[PostgresqlFlexibleServerHighAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[PostgresqlFlexibleServerIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_window: typing.Optional[typing.Union[PostgresqlFlexibleServerMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    point_in_time_restore_time_in_utc: typing.Optional[builtins.str] = None,
    private_dns_zone_id: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replication_role: typing.Optional[builtins.str] = None,
    sku_name: typing.Optional[builtins.str] = None,
    source_server_id: typing.Optional[builtins.str] = None,
    storage_mb: typing.Optional[jsii.Number] = None,
    storage_tier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PostgresqlFlexibleServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1c1b8431bbd15b2940d19db23904b36744e18d5d797c157f1fc8caf3f51e73bc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335a92c1d8d238338a5e3d2411b4d69b24bbbbcee35e12b7df3b2b6e80b89f2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a2c9d8bb2572134a01582fddd8f07b2d58da099327c86c86ce1f38a14331cda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382416965dd3b911e1b55e7658a066ce1d60f8c18f2da802a32676d0cbb09726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f1972b7af8509ba4b7f292a0eb05f4b6964c6f6ab4c36b93b817e8cce48ce7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e6724371bef5b21ea88b9ae053bb77925be6ba6f1b224139c81430afbf9f58(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c33939264eacfd1cd5de23c118f78079462df468ff20dc68b5e4f20e647772(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4bc2c1a201c9700f86cb9f0fccb7be33011a40e610177ae1ea948b82ae4a47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c198af550df5fff499ec03576a97ade0828dbc91e19455a75090df65f9df895(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487214db9d0f38861aefad4ad5ea0f772b52b1de56a8ead9d0f5c92a5c1c74f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a17403cc8f17253464886e734e33307f069474fe64af3ebbb8d0890ea2f901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7664f9da1cae32f83c70d1d1899b0fd2959f24f2ab05c21c3138566ca15b16e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bb0fd0d1006e4cbae68c4e0b5c9be434ebc3ed624d5fc36eb51865930f7ed1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b841268f6d581e794eb25ed48b3844d936cb76ab805555791f15d02e391ef10f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1846fde8f4f32df1bd17afe42c5c0d775553490ee77160b725c2d1c5b421272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fe1f36a774a4045640092abc7845bdb902489a679c260d81efba7deec5e10e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ae999707d011e85d43489f78434fc1e0bdf5a0f2cd75e725cdb9de8e659e72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340cef0e8ee0ca6d18cc12f00777290da4deda55077a7219438d4d679f4dffa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1670d9a05fbb52068f10d683fd2471fa65a10928c5b2b5527abcc9b53b655f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b64d0749db276fa2d20d823d1911ce915ef770a70b87047291979315ba8b43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c988ff9aec74994dc49ae31bbddb0ddc16c24ac69aadfabaa1c1a6c34effbc9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8b0ca32ee13f06336604a84e25cf5545479661eee2749c22e3b57a9610139d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099fa272133fbfa5f768b0dbbb3ad6fa442583c35a95fb5a2947497d4a5a9802(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd88bd1607be06c79895c7e408e6b0b25fe5a50fc23c2055db92ef3a55191109(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a9e2e84ba23e9708ee80c7d725ca86202d500bf8e95257f9dd292a400b2053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e912a69aa940d5cdd3c29ac564b3fa6467bcf1a61e9a4808251af6b342465c(
    *,
    active_directory_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password_auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3d5f65cf8470253bb61c1cec7b6f81aeefff9940d47fcbb6701e73ec07fe9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9adb50fdd022ee3708c0e6c58110b9851ea990a11fb651ca17df4637fe062ebc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9f42b9203b2d10c60e658c073de8db02ca3c3016e4e751940e75c9bf419f69(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c170e0af5f70866bbc9d43e8d8af058db6358ce2855a1560232831729c6052b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86289863456335af101d71a64d4e541bffec1a16b833de61dce37e8158bbb1aa(
    value: typing.Optional[PostgresqlFlexibleServerAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34cd8bacf42e143fb2a537691b5b31c415744c9de22a9acb4972a6472a36103f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    administrator_login: typing.Optional[builtins.str] = None,
    administrator_password: typing.Optional[builtins.str] = None,
    administrator_password_wo: typing.Optional[builtins.str] = None,
    administrator_password_wo_version: typing.Optional[jsii.Number] = None,
    authentication: typing.Optional[typing.Union[PostgresqlFlexibleServerAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_grow_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup_retention_days: typing.Optional[jsii.Number] = None,
    create_mode: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[typing.Union[PostgresqlFlexibleServerCustomerManagedKey, typing.Dict[builtins.str, typing.Any]]] = None,
    delegated_subnet_id: typing.Optional[builtins.str] = None,
    geo_redundant_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    high_availability: typing.Optional[typing.Union[PostgresqlFlexibleServerHighAvailability, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[PostgresqlFlexibleServerIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_window: typing.Optional[typing.Union[PostgresqlFlexibleServerMaintenanceWindow, typing.Dict[builtins.str, typing.Any]]] = None,
    point_in_time_restore_time_in_utc: typing.Optional[builtins.str] = None,
    private_dns_zone_id: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    replication_role: typing.Optional[builtins.str] = None,
    sku_name: typing.Optional[builtins.str] = None,
    source_server_id: typing.Optional[builtins.str] = None,
    storage_mb: typing.Optional[jsii.Number] = None,
    storage_tier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PostgresqlFlexibleServerTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfce5724d35daf37f9c234bbebba31f59ac75df367908729d662542e60a21fca(
    *,
    key_vault_key_id: builtins.str,
    geo_backup_key_vault_key_id: typing.Optional[builtins.str] = None,
    geo_backup_user_assigned_identity_id: typing.Optional[builtins.str] = None,
    primary_user_assigned_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69e4d21fb7115a68071f7571df682d54362f561243d405b2b25852e77107bf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdc8b3ccd3f10a782a0f76d193d2225e476352f34f6c73907d0be819d9f40bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662858f9420b2183fe0dd3a56b35af30b9e0c650e4826a131ee4e92488031a49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b2621f457e9791368e20b324ccbfaf98b39b089809703fdab475e12cba62f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc8af3e0da1aef7179f53e7c3c39bee9cebbcb56b1b504a949980d4dfa610a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446068452c0a583f83bc62b8879c6e1b4cca52f21a733d1b20eb7dd6c3ab11b3(
    value: typing.Optional[PostgresqlFlexibleServerCustomerManagedKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dd0c8c276844cd87b639713995fcc8b5e26140c4d12e10609c2e5c499e315e(
    *,
    mode: builtins.str,
    standby_availability_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250b05827dfad1c0d15f66b068dfa8409243ea58524db3fb4d3140e74991a87e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594b66b54607cf8ef364da551fe3de396b8cc24715ead4b2b33ac8aa7b6e4136(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8648b6a27234753a74d43fd158cc90cd4457db67ed858e72a1196d553326c89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ed66ecb77f8a291757bc73b0c24acd3fa1eb55e5bca4eb6182d7a4de133295(
    value: typing.Optional[PostgresqlFlexibleServerHighAvailability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8def3f8ee349f87dc0919a4cb5a9826bc2b8846f43e8dd7b78685a45a04fba26(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6118f6a05dd45d42a8e75146a63c205566b1ede2ad5cd23d41b00db87af0a2c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c17f8a07514e50d9550b0792863ea417577449cde4a10c6c124961379c1bfc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684635080bbb08fd62211f71a48d4f2565470497baf659bd68415fc89d96750b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18cbbcbf9bed466993bf534eb4f306fcc40be570da6f25df96359ba5e8c1d86e(
    value: typing.Optional[PostgresqlFlexibleServerIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31f48b5a5c381743efc49af92a2677b9a9c9f95bcaa43ce80d1a8784478287a(
    *,
    day_of_week: typing.Optional[jsii.Number] = None,
    start_hour: typing.Optional[jsii.Number] = None,
    start_minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fad219bfd90934020ca0813f15b740980397089171cbcfb3f8a78ff84a62537(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a989b31c3166097d83ca63714fc1eab19abfc925e4bdede7380aa01e425a972(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfbb0119734276336da2ce33855a07d4759ee33aa59dd85ddac159af68b8411d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__804e2587db42fe70a60198834ae0f4cadd34519b610fcfff49e6348fb8800b14(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aea28d87ea130b595c5dc575224a5168a1c7157eec67dc0eeba6097e20f713f7(
    value: typing.Optional[PostgresqlFlexibleServerMaintenanceWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a3be7f42b349eff9641121c2a24c5dba9cf3c52858a1a9533fe2be0103773ce(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9511d7dd17f86303a2781678e3d362b9e04bd7c53622b2117c8d62fc394165a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e34fc33259b93a4a23d530d0d7f7a1a8fd83d1193fa0cbc7b01854991f121ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf539f4eb1315fb27e904a919c02406f42b65c1640eeab9d36c5762166c0b9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9532c3757c94b789ee972c0303147d825c83fe4481422f44d402d6630dcc2383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151fdb9758535a4b168bb6c3de3614eeea45afc6b1537459a0d4c00a5b103c9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c4299dd6bec5cf53248d4aa2be596a2d6cc37ab850e04ef9ce6d12a0eb7f29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PostgresqlFlexibleServerTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

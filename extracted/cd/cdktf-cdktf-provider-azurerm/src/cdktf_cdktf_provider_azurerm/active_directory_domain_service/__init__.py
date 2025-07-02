r'''
# `azurerm_active_directory_domain_service`

Refer to the Terraform Registry for docs: [`azurerm_active_directory_domain_service`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service).
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


class ActiveDirectoryDomainService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service azurerm_active_directory_domain_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        domain_name: builtins.str,
        initial_replica_set: typing.Union["ActiveDirectoryDomainServiceInitialReplicaSet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: builtins.str,
        domain_configuration_type: typing.Optional[builtins.str] = None,
        filtered_sync_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union["ActiveDirectoryDomainServiceNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        secure_ldap: typing.Optional[typing.Union["ActiveDirectoryDomainServiceSecureLdap", typing.Dict[builtins.str, typing.Any]]] = None,
        security: typing.Optional[typing.Union["ActiveDirectoryDomainServiceSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ActiveDirectoryDomainServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service azurerm_active_directory_domain_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#domain_name ActiveDirectoryDomainService#domain_name}.
        :param initial_replica_set: initial_replica_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#initial_replica_set ActiveDirectoryDomainService#initial_replica_set}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#location ActiveDirectoryDomainService#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#name ActiveDirectoryDomainService#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#resource_group_name ActiveDirectoryDomainService#resource_group_name}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sku ActiveDirectoryDomainService#sku}.
        :param domain_configuration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#domain_configuration_type ActiveDirectoryDomainService#domain_configuration_type}.
        :param filtered_sync_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#filtered_sync_enabled ActiveDirectoryDomainService#filtered_sync_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#id ActiveDirectoryDomainService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notifications: notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notifications ActiveDirectoryDomainService#notifications}
        :param secure_ldap: secure_ldap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#secure_ldap ActiveDirectoryDomainService#secure_ldap}
        :param security: security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#security ActiveDirectoryDomainService#security}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#tags ActiveDirectoryDomainService#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#timeouts ActiveDirectoryDomainService#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935e60fc566c3f79ae1064f5cf39bcc8581e7a9fdd2856d98cd6f98940e9121f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ActiveDirectoryDomainServiceConfig(
            domain_name=domain_name,
            initial_replica_set=initial_replica_set,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sku=sku,
            domain_configuration_type=domain_configuration_type,
            filtered_sync_enabled=filtered_sync_enabled,
            id=id,
            notifications=notifications,
            secure_ldap=secure_ldap,
            security=security,
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
        '''Generates CDKTF code for importing a ActiveDirectoryDomainService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ActiveDirectoryDomainService to import.
        :param import_from_id: The id of the existing ActiveDirectoryDomainService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ActiveDirectoryDomainService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e0551e17fc036c8f42b94f46d29d7b8fcc4fb55c51258310733f22bd552426)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInitialReplicaSet")
    def put_initial_replica_set(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#subnet_id ActiveDirectoryDomainService#subnet_id}.
        '''
        value = ActiveDirectoryDomainServiceInitialReplicaSet(subnet_id=subnet_id)

        return typing.cast(None, jsii.invoke(self, "putInitialReplicaSet", [value]))

    @jsii.member(jsii_name="putNotifications")
    def put_notifications(
        self,
        *,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_dc_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_global_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param additional_recipients: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#additional_recipients ActiveDirectoryDomainService#additional_recipients}.
        :param notify_dc_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notify_dc_admins ActiveDirectoryDomainService#notify_dc_admins}.
        :param notify_global_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notify_global_admins ActiveDirectoryDomainService#notify_global_admins}.
        '''
        value = ActiveDirectoryDomainServiceNotifications(
            additional_recipients=additional_recipients,
            notify_dc_admins=notify_dc_admins,
            notify_global_admins=notify_global_admins,
        )

        return typing.cast(None, jsii.invoke(self, "putNotifications", [value]))

    @jsii.member(jsii_name="putSecureLdap")
    def put_secure_ldap(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        pfx_certificate: builtins.str,
        pfx_certificate_password: builtins.str,
        external_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#enabled ActiveDirectoryDomainService#enabled}.
        :param pfx_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#pfx_certificate ActiveDirectoryDomainService#pfx_certificate}.
        :param pfx_certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#pfx_certificate_password ActiveDirectoryDomainService#pfx_certificate_password}.
        :param external_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#external_access_enabled ActiveDirectoryDomainService#external_access_enabled}.
        '''
        value = ActiveDirectoryDomainServiceSecureLdap(
            enabled=enabled,
            pfx_certificate=pfx_certificate,
            pfx_certificate_password=pfx_certificate_password,
            external_access_enabled=external_access_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putSecureLdap", [value]))

    @jsii.member(jsii_name="putSecurity")
    def put_security(
        self,
        *,
        kerberos_armoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kerberos_rc4_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ntlm_v1_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_kerberos_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_ntlm_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_on_prem_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_v1_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param kerberos_armoring_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#kerberos_armoring_enabled ActiveDirectoryDomainService#kerberos_armoring_enabled}.
        :param kerberos_rc4_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#kerberos_rc4_encryption_enabled ActiveDirectoryDomainService#kerberos_rc4_encryption_enabled}.
        :param ntlm_v1_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#ntlm_v1_enabled ActiveDirectoryDomainService#ntlm_v1_enabled}.
        :param sync_kerberos_passwords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_kerberos_passwords ActiveDirectoryDomainService#sync_kerberos_passwords}.
        :param sync_ntlm_passwords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_ntlm_passwords ActiveDirectoryDomainService#sync_ntlm_passwords}.
        :param sync_on_prem_passwords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_on_prem_passwords ActiveDirectoryDomainService#sync_on_prem_passwords}.
        :param tls_v1_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#tls_v1_enabled ActiveDirectoryDomainService#tls_v1_enabled}.
        '''
        value = ActiveDirectoryDomainServiceSecurity(
            kerberos_armoring_enabled=kerberos_armoring_enabled,
            kerberos_rc4_encryption_enabled=kerberos_rc4_encryption_enabled,
            ntlm_v1_enabled=ntlm_v1_enabled,
            sync_kerberos_passwords=sync_kerberos_passwords,
            sync_ntlm_passwords=sync_ntlm_passwords,
            sync_on_prem_passwords=sync_on_prem_passwords,
            tls_v1_enabled=tls_v1_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putSecurity", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#create ActiveDirectoryDomainService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#delete ActiveDirectoryDomainService#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#read ActiveDirectoryDomainService#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#update ActiveDirectoryDomainService#update}.
        '''
        value = ActiveDirectoryDomainServiceTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDomainConfigurationType")
    def reset_domain_configuration_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainConfigurationType", []))

    @jsii.member(jsii_name="resetFilteredSyncEnabled")
    def reset_filtered_sync_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilteredSyncEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotifications")
    def reset_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifications", []))

    @jsii.member(jsii_name="resetSecureLdap")
    def reset_secure_ldap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureLdap", []))

    @jsii.member(jsii_name="resetSecurity")
    def reset_security(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurity", []))

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
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @builtins.property
    @jsii.member(jsii_name="initialReplicaSet")
    def initial_replica_set(
        self,
    ) -> "ActiveDirectoryDomainServiceInitialReplicaSetOutputReference":
        return typing.cast("ActiveDirectoryDomainServiceInitialReplicaSetOutputReference", jsii.get(self, "initialReplicaSet"))

    @builtins.property
    @jsii.member(jsii_name="notifications")
    def notifications(
        self,
    ) -> "ActiveDirectoryDomainServiceNotificationsOutputReference":
        return typing.cast("ActiveDirectoryDomainServiceNotificationsOutputReference", jsii.get(self, "notifications"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="secureLdap")
    def secure_ldap(self) -> "ActiveDirectoryDomainServiceSecureLdapOutputReference":
        return typing.cast("ActiveDirectoryDomainServiceSecureLdapOutputReference", jsii.get(self, "secureLdap"))

    @builtins.property
    @jsii.member(jsii_name="security")
    def security(self) -> "ActiveDirectoryDomainServiceSecurityOutputReference":
        return typing.cast("ActiveDirectoryDomainServiceSecurityOutputReference", jsii.get(self, "security"))

    @builtins.property
    @jsii.member(jsii_name="syncOwner")
    def sync_owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "syncOwner"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ActiveDirectoryDomainServiceTimeoutsOutputReference":
        return typing.cast("ActiveDirectoryDomainServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="domainConfigurationTypeInput")
    def domain_configuration_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainConfigurationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="filteredSyncEnabledInput")
    def filtered_sync_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filteredSyncEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="initialReplicaSetInput")
    def initial_replica_set_input(
        self,
    ) -> typing.Optional["ActiveDirectoryDomainServiceInitialReplicaSet"]:
        return typing.cast(typing.Optional["ActiveDirectoryDomainServiceInitialReplicaSet"], jsii.get(self, "initialReplicaSetInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationsInput")
    def notifications_input(
        self,
    ) -> typing.Optional["ActiveDirectoryDomainServiceNotifications"]:
        return typing.cast(typing.Optional["ActiveDirectoryDomainServiceNotifications"], jsii.get(self, "notificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secureLdapInput")
    def secure_ldap_input(
        self,
    ) -> typing.Optional["ActiveDirectoryDomainServiceSecureLdap"]:
        return typing.cast(typing.Optional["ActiveDirectoryDomainServiceSecureLdap"], jsii.get(self, "secureLdapInput"))

    @builtins.property
    @jsii.member(jsii_name="securityInput")
    def security_input(self) -> typing.Optional["ActiveDirectoryDomainServiceSecurity"]:
        return typing.cast(typing.Optional["ActiveDirectoryDomainServiceSecurity"], jsii.get(self, "securityInput"))

    @builtins.property
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ActiveDirectoryDomainServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ActiveDirectoryDomainServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainConfigurationType")
    def domain_configuration_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainConfigurationType"))

    @domain_configuration_type.setter
    def domain_configuration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8a2683338bcf882741de34f72e5a2fccb4b33b1767ea53039936c5ac3d6e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainConfigurationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a3e81e8cbd0614ddb7c6c27e34c57f9ab2c5bdee82e907b08315ff4f4a09c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filteredSyncEnabled")
    def filtered_sync_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filteredSyncEnabled"))

    @filtered_sync_enabled.setter
    def filtered_sync_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775e4c5bceea071558f2721f5f3db4ea41c63e5e5575bfb4ac05e4633efc000f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filteredSyncEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af1694e1e45138d70897ebd68a0cd1eb2f710770dcd48666bdf3b89a2213f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd67d58781b303cad50b1d80a7a9e5718e1f69a833af6d1af42504bebba1bc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca0b84c8505db2300e5c1d1114fd606d9d7ba499c8eb45d8e94812df44c2a83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd8a33329593ac6c082d837d64428d92f12116c30959f0a6ddb2eb2d1b00c67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba3eb4ed88e35fe3a9bb1be27b1564c995c60d311e85032a306b356bed9ed0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc35f190144ef9815b2e49979152dfa84a2ae758ccc8c901d5e948090ce12ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "domain_name": "domainName",
        "initial_replica_set": "initialReplicaSet",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "sku": "sku",
        "domain_configuration_type": "domainConfigurationType",
        "filtered_sync_enabled": "filteredSyncEnabled",
        "id": "id",
        "notifications": "notifications",
        "secure_ldap": "secureLdap",
        "security": "security",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class ActiveDirectoryDomainServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        domain_name: builtins.str,
        initial_replica_set: typing.Union["ActiveDirectoryDomainServiceInitialReplicaSet", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: builtins.str,
        domain_configuration_type: typing.Optional[builtins.str] = None,
        filtered_sync_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Union["ActiveDirectoryDomainServiceNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        secure_ldap: typing.Optional[typing.Union["ActiveDirectoryDomainServiceSecureLdap", typing.Dict[builtins.str, typing.Any]]] = None,
        security: typing.Optional[typing.Union["ActiveDirectoryDomainServiceSecurity", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ActiveDirectoryDomainServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#domain_name ActiveDirectoryDomainService#domain_name}.
        :param initial_replica_set: initial_replica_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#initial_replica_set ActiveDirectoryDomainService#initial_replica_set}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#location ActiveDirectoryDomainService#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#name ActiveDirectoryDomainService#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#resource_group_name ActiveDirectoryDomainService#resource_group_name}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sku ActiveDirectoryDomainService#sku}.
        :param domain_configuration_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#domain_configuration_type ActiveDirectoryDomainService#domain_configuration_type}.
        :param filtered_sync_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#filtered_sync_enabled ActiveDirectoryDomainService#filtered_sync_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#id ActiveDirectoryDomainService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notifications: notifications block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notifications ActiveDirectoryDomainService#notifications}
        :param secure_ldap: secure_ldap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#secure_ldap ActiveDirectoryDomainService#secure_ldap}
        :param security: security block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#security ActiveDirectoryDomainService#security}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#tags ActiveDirectoryDomainService#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#timeouts ActiveDirectoryDomainService#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(initial_replica_set, dict):
            initial_replica_set = ActiveDirectoryDomainServiceInitialReplicaSet(**initial_replica_set)
        if isinstance(notifications, dict):
            notifications = ActiveDirectoryDomainServiceNotifications(**notifications)
        if isinstance(secure_ldap, dict):
            secure_ldap = ActiveDirectoryDomainServiceSecureLdap(**secure_ldap)
        if isinstance(security, dict):
            security = ActiveDirectoryDomainServiceSecurity(**security)
        if isinstance(timeouts, dict):
            timeouts = ActiveDirectoryDomainServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001e20e214c988034e843afa00ce3e0660074ba94cf23cabd7e1f01d428e4a23)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument initial_replica_set", value=initial_replica_set, expected_type=type_hints["initial_replica_set"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument domain_configuration_type", value=domain_configuration_type, expected_type=type_hints["domain_configuration_type"])
            check_type(argname="argument filtered_sync_enabled", value=filtered_sync_enabled, expected_type=type_hints["filtered_sync_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
            check_type(argname="argument secure_ldap", value=secure_ldap, expected_type=type_hints["secure_ldap"])
            check_type(argname="argument security", value=security, expected_type=type_hints["security"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "initial_replica_set": initial_replica_set,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sku": sku,
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
        if domain_configuration_type is not None:
            self._values["domain_configuration_type"] = domain_configuration_type
        if filtered_sync_enabled is not None:
            self._values["filtered_sync_enabled"] = filtered_sync_enabled
        if id is not None:
            self._values["id"] = id
        if notifications is not None:
            self._values["notifications"] = notifications
        if secure_ldap is not None:
            self._values["secure_ldap"] = secure_ldap
        if security is not None:
            self._values["security"] = security
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
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#domain_name ActiveDirectoryDomainService#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def initial_replica_set(self) -> "ActiveDirectoryDomainServiceInitialReplicaSet":
        '''initial_replica_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#initial_replica_set ActiveDirectoryDomainService#initial_replica_set}
        '''
        result = self._values.get("initial_replica_set")
        assert result is not None, "Required property 'initial_replica_set' is missing"
        return typing.cast("ActiveDirectoryDomainServiceInitialReplicaSet", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#location ActiveDirectoryDomainService#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#name ActiveDirectoryDomainService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#resource_group_name ActiveDirectoryDomainService#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sku ActiveDirectoryDomainService#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_configuration_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#domain_configuration_type ActiveDirectoryDomainService#domain_configuration_type}.'''
        result = self._values.get("domain_configuration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filtered_sync_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#filtered_sync_enabled ActiveDirectoryDomainService#filtered_sync_enabled}.'''
        result = self._values.get("filtered_sync_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#id ActiveDirectoryDomainService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notifications(
        self,
    ) -> typing.Optional["ActiveDirectoryDomainServiceNotifications"]:
        '''notifications block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notifications ActiveDirectoryDomainService#notifications}
        '''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional["ActiveDirectoryDomainServiceNotifications"], result)

    @builtins.property
    def secure_ldap(self) -> typing.Optional["ActiveDirectoryDomainServiceSecureLdap"]:
        '''secure_ldap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#secure_ldap ActiveDirectoryDomainService#secure_ldap}
        '''
        result = self._values.get("secure_ldap")
        return typing.cast(typing.Optional["ActiveDirectoryDomainServiceSecureLdap"], result)

    @builtins.property
    def security(self) -> typing.Optional["ActiveDirectoryDomainServiceSecurity"]:
        '''security block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#security ActiveDirectoryDomainService#security}
        '''
        result = self._values.get("security")
        return typing.cast(typing.Optional["ActiveDirectoryDomainServiceSecurity"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#tags ActiveDirectoryDomainService#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ActiveDirectoryDomainServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#timeouts ActiveDirectoryDomainService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ActiveDirectoryDomainServiceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActiveDirectoryDomainServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceInitialReplicaSet",
    jsii_struct_bases=[],
    name_mapping={"subnet_id": "subnetId"},
)
class ActiveDirectoryDomainServiceInitialReplicaSet:
    def __init__(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#subnet_id ActiveDirectoryDomainService#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49943bda77f4ea7fa49652a67a9ae4f0f41ce3576abe84795991e630b66c29e)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
        }

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#subnet_id ActiveDirectoryDomainService#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActiveDirectoryDomainServiceInitialReplicaSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActiveDirectoryDomainServiceInitialReplicaSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceInitialReplicaSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07bacf9a2762ceab8b00f6258439fb48a4c5d22a6822401f802fdff6ec31a0eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="domainControllerIpAddresses")
    def domain_controller_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainControllerIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="externalAccessIpAddress")
    def external_access_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAccessIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="serviceStatus")
    def service_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceStatus"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07f1553ecfa53bca424737565f597b575f360868e3ab9d0a5f3a00b921d0828)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ActiveDirectoryDomainServiceInitialReplicaSet]:
        return typing.cast(typing.Optional[ActiveDirectoryDomainServiceInitialReplicaSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActiveDirectoryDomainServiceInitialReplicaSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe85ead5d03d1622f92e541816759b84d1b5c87a58ccca307d588f8ffa08498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "additional_recipients": "additionalRecipients",
        "notify_dc_admins": "notifyDcAdmins",
        "notify_global_admins": "notifyGlobalAdmins",
    },
)
class ActiveDirectoryDomainServiceNotifications:
    def __init__(
        self,
        *,
        additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_dc_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        notify_global_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param additional_recipients: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#additional_recipients ActiveDirectoryDomainService#additional_recipients}.
        :param notify_dc_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notify_dc_admins ActiveDirectoryDomainService#notify_dc_admins}.
        :param notify_global_admins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notify_global_admins ActiveDirectoryDomainService#notify_global_admins}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cd1ed6a424aed946fa33d53b6bc15b90a4d5389abc580766a26d09cc9657e74)
            check_type(argname="argument additional_recipients", value=additional_recipients, expected_type=type_hints["additional_recipients"])
            check_type(argname="argument notify_dc_admins", value=notify_dc_admins, expected_type=type_hints["notify_dc_admins"])
            check_type(argname="argument notify_global_admins", value=notify_global_admins, expected_type=type_hints["notify_global_admins"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_recipients is not None:
            self._values["additional_recipients"] = additional_recipients
        if notify_dc_admins is not None:
            self._values["notify_dc_admins"] = notify_dc_admins
        if notify_global_admins is not None:
            self._values["notify_global_admins"] = notify_global_admins

    @builtins.property
    def additional_recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#additional_recipients ActiveDirectoryDomainService#additional_recipients}.'''
        result = self._values.get("additional_recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def notify_dc_admins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notify_dc_admins ActiveDirectoryDomainService#notify_dc_admins}.'''
        result = self._values.get("notify_dc_admins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def notify_global_admins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#notify_global_admins ActiveDirectoryDomainService#notify_global_admins}.'''
        result = self._values.get("notify_global_admins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActiveDirectoryDomainServiceNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActiveDirectoryDomainServiceNotificationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceNotificationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91a689cdb6772d9e1671b6a9a93f29cb407081c087e8d3b093a33e7f90c23a39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdditionalRecipients")
    def reset_additional_recipients(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalRecipients", []))

    @jsii.member(jsii_name="resetNotifyDcAdmins")
    def reset_notify_dc_admins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyDcAdmins", []))

    @jsii.member(jsii_name="resetNotifyGlobalAdmins")
    def reset_notify_global_admins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifyGlobalAdmins", []))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipientsInput")
    def additional_recipients_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "additionalRecipientsInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyDcAdminsInput")
    def notify_dc_admins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyDcAdminsInput"))

    @builtins.property
    @jsii.member(jsii_name="notifyGlobalAdminsInput")
    def notify_global_admins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "notifyGlobalAdminsInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalRecipients")
    def additional_recipients(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalRecipients"))

    @additional_recipients.setter
    def additional_recipients(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52932bc4cf4116434bd78bd3b795606658f29c657f4693045f40a17264392cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalRecipients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyDcAdmins")
    def notify_dc_admins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notifyDcAdmins"))

    @notify_dc_admins.setter
    def notify_dc_admins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b7d4cb4d5f75b6d1b22557a87bd4520431f8330b746188911ca87e88867a39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyDcAdmins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifyGlobalAdmins")
    def notify_global_admins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "notifyGlobalAdmins"))

    @notify_global_admins.setter
    def notify_global_admins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e378dae86cbabbd043946ea5e37110870f3a8d4c3db1cb4fb52121419943c1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifyGlobalAdmins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ActiveDirectoryDomainServiceNotifications]:
        return typing.cast(typing.Optional[ActiveDirectoryDomainServiceNotifications], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActiveDirectoryDomainServiceNotifications],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2aa3f0974303d919abc3b36c458539cb0546f8234d31a2fd40eebb977e62702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceSecureLdap",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "pfx_certificate": "pfxCertificate",
        "pfx_certificate_password": "pfxCertificatePassword",
        "external_access_enabled": "externalAccessEnabled",
    },
)
class ActiveDirectoryDomainServiceSecureLdap:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        pfx_certificate: builtins.str,
        pfx_certificate_password: builtins.str,
        external_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#enabled ActiveDirectoryDomainService#enabled}.
        :param pfx_certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#pfx_certificate ActiveDirectoryDomainService#pfx_certificate}.
        :param pfx_certificate_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#pfx_certificate_password ActiveDirectoryDomainService#pfx_certificate_password}.
        :param external_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#external_access_enabled ActiveDirectoryDomainService#external_access_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320535be9ba94e8b76a7304e453272dd3ed45e74e804fa2dd7bd7385309a82df)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument pfx_certificate", value=pfx_certificate, expected_type=type_hints["pfx_certificate"])
            check_type(argname="argument pfx_certificate_password", value=pfx_certificate_password, expected_type=type_hints["pfx_certificate_password"])
            check_type(argname="argument external_access_enabled", value=external_access_enabled, expected_type=type_hints["external_access_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "pfx_certificate": pfx_certificate,
            "pfx_certificate_password": pfx_certificate_password,
        }
        if external_access_enabled is not None:
            self._values["external_access_enabled"] = external_access_enabled

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#enabled ActiveDirectoryDomainService#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def pfx_certificate(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#pfx_certificate ActiveDirectoryDomainService#pfx_certificate}.'''
        result = self._values.get("pfx_certificate")
        assert result is not None, "Required property 'pfx_certificate' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pfx_certificate_password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#pfx_certificate_password ActiveDirectoryDomainService#pfx_certificate_password}.'''
        result = self._values.get("pfx_certificate_password")
        assert result is not None, "Required property 'pfx_certificate_password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def external_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#external_access_enabled ActiveDirectoryDomainService#external_access_enabled}.'''
        result = self._values.get("external_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActiveDirectoryDomainServiceSecureLdap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActiveDirectoryDomainServiceSecureLdapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceSecureLdapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a314601dc9e1abfb9f1836a22dee681435070fe65edcc0507cbfd71db0435e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExternalAccessEnabled")
    def reset_external_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAccessEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="certificateExpiry")
    def certificate_expiry(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateExpiry"))

    @builtins.property
    @jsii.member(jsii_name="certificateThumbprint")
    def certificate_thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateThumbprint"))

    @builtins.property
    @jsii.member(jsii_name="publicCertificate")
    def public_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicCertificate"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAccessEnabledInput")
    def external_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "externalAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="pfxCertificateInput")
    def pfx_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pfxCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="pfxCertificatePasswordInput")
    def pfx_certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pfxCertificatePasswordInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5fe3e0deb551caec553d08475c93ab879ea61d6105ddb24062f756c605b7efe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalAccessEnabled")
    def external_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "externalAccessEnabled"))

    @external_access_enabled.setter
    def external_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1bb77b4e3be04dfb40fe82d15084e70c7999d7447eaddf6aa9465c23f614d4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pfxCertificate")
    def pfx_certificate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pfxCertificate"))

    @pfx_certificate.setter
    def pfx_certificate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4adc7eb44f6ffc9510e777d147d8c26dd050775758e8bdab23b9c321eeeb4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pfxCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pfxCertificatePassword")
    def pfx_certificate_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pfxCertificatePassword"))

    @pfx_certificate_password.setter
    def pfx_certificate_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4815615879370f81fb6601fe8d65eb358cbc3d5e1c3784c4c1f532fd89690a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pfxCertificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ActiveDirectoryDomainServiceSecureLdap]:
        return typing.cast(typing.Optional[ActiveDirectoryDomainServiceSecureLdap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActiveDirectoryDomainServiceSecureLdap],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985c1916445f6817c36dd40012d3a4e0ad3c43feb7ccd33e2ed216b5a78b428e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceSecurity",
    jsii_struct_bases=[],
    name_mapping={
        "kerberos_armoring_enabled": "kerberosArmoringEnabled",
        "kerberos_rc4_encryption_enabled": "kerberosRc4EncryptionEnabled",
        "ntlm_v1_enabled": "ntlmV1Enabled",
        "sync_kerberos_passwords": "syncKerberosPasswords",
        "sync_ntlm_passwords": "syncNtlmPasswords",
        "sync_on_prem_passwords": "syncOnPremPasswords",
        "tls_v1_enabled": "tlsV1Enabled",
    },
)
class ActiveDirectoryDomainServiceSecurity:
    def __init__(
        self,
        *,
        kerberos_armoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        kerberos_rc4_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ntlm_v1_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_kerberos_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_ntlm_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_on_prem_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tls_v1_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param kerberos_armoring_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#kerberos_armoring_enabled ActiveDirectoryDomainService#kerberos_armoring_enabled}.
        :param kerberos_rc4_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#kerberos_rc4_encryption_enabled ActiveDirectoryDomainService#kerberos_rc4_encryption_enabled}.
        :param ntlm_v1_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#ntlm_v1_enabled ActiveDirectoryDomainService#ntlm_v1_enabled}.
        :param sync_kerberos_passwords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_kerberos_passwords ActiveDirectoryDomainService#sync_kerberos_passwords}.
        :param sync_ntlm_passwords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_ntlm_passwords ActiveDirectoryDomainService#sync_ntlm_passwords}.
        :param sync_on_prem_passwords: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_on_prem_passwords ActiveDirectoryDomainService#sync_on_prem_passwords}.
        :param tls_v1_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#tls_v1_enabled ActiveDirectoryDomainService#tls_v1_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363a7284ca8cd397190c8be666c719b2471ed42e6d98ad740142961f33f9e673)
            check_type(argname="argument kerberos_armoring_enabled", value=kerberos_armoring_enabled, expected_type=type_hints["kerberos_armoring_enabled"])
            check_type(argname="argument kerberos_rc4_encryption_enabled", value=kerberos_rc4_encryption_enabled, expected_type=type_hints["kerberos_rc4_encryption_enabled"])
            check_type(argname="argument ntlm_v1_enabled", value=ntlm_v1_enabled, expected_type=type_hints["ntlm_v1_enabled"])
            check_type(argname="argument sync_kerberos_passwords", value=sync_kerberos_passwords, expected_type=type_hints["sync_kerberos_passwords"])
            check_type(argname="argument sync_ntlm_passwords", value=sync_ntlm_passwords, expected_type=type_hints["sync_ntlm_passwords"])
            check_type(argname="argument sync_on_prem_passwords", value=sync_on_prem_passwords, expected_type=type_hints["sync_on_prem_passwords"])
            check_type(argname="argument tls_v1_enabled", value=tls_v1_enabled, expected_type=type_hints["tls_v1_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kerberos_armoring_enabled is not None:
            self._values["kerberos_armoring_enabled"] = kerberos_armoring_enabled
        if kerberos_rc4_encryption_enabled is not None:
            self._values["kerberos_rc4_encryption_enabled"] = kerberos_rc4_encryption_enabled
        if ntlm_v1_enabled is not None:
            self._values["ntlm_v1_enabled"] = ntlm_v1_enabled
        if sync_kerberos_passwords is not None:
            self._values["sync_kerberos_passwords"] = sync_kerberos_passwords
        if sync_ntlm_passwords is not None:
            self._values["sync_ntlm_passwords"] = sync_ntlm_passwords
        if sync_on_prem_passwords is not None:
            self._values["sync_on_prem_passwords"] = sync_on_prem_passwords
        if tls_v1_enabled is not None:
            self._values["tls_v1_enabled"] = tls_v1_enabled

    @builtins.property
    def kerberos_armoring_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#kerberos_armoring_enabled ActiveDirectoryDomainService#kerberos_armoring_enabled}.'''
        result = self._values.get("kerberos_armoring_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def kerberos_rc4_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#kerberos_rc4_encryption_enabled ActiveDirectoryDomainService#kerberos_rc4_encryption_enabled}.'''
        result = self._values.get("kerberos_rc4_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ntlm_v1_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#ntlm_v1_enabled ActiveDirectoryDomainService#ntlm_v1_enabled}.'''
        result = self._values.get("ntlm_v1_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_kerberos_passwords(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_kerberos_passwords ActiveDirectoryDomainService#sync_kerberos_passwords}.'''
        result = self._values.get("sync_kerberos_passwords")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_ntlm_passwords(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_ntlm_passwords ActiveDirectoryDomainService#sync_ntlm_passwords}.'''
        result = self._values.get("sync_ntlm_passwords")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_on_prem_passwords(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#sync_on_prem_passwords ActiveDirectoryDomainService#sync_on_prem_passwords}.'''
        result = self._values.get("sync_on_prem_passwords")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tls_v1_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#tls_v1_enabled ActiveDirectoryDomainService#tls_v1_enabled}.'''
        result = self._values.get("tls_v1_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActiveDirectoryDomainServiceSecurity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActiveDirectoryDomainServiceSecurityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceSecurityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3ccc753f5b69921e890e77234487b54165fa2bc177bc07362325d8605779a86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKerberosArmoringEnabled")
    def reset_kerberos_armoring_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberosArmoringEnabled", []))

    @jsii.member(jsii_name="resetKerberosRc4EncryptionEnabled")
    def reset_kerberos_rc4_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberosRc4EncryptionEnabled", []))

    @jsii.member(jsii_name="resetNtlmV1Enabled")
    def reset_ntlm_v1_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNtlmV1Enabled", []))

    @jsii.member(jsii_name="resetSyncKerberosPasswords")
    def reset_sync_kerberos_passwords(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncKerberosPasswords", []))

    @jsii.member(jsii_name="resetSyncNtlmPasswords")
    def reset_sync_ntlm_passwords(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncNtlmPasswords", []))

    @jsii.member(jsii_name="resetSyncOnPremPasswords")
    def reset_sync_on_prem_passwords(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncOnPremPasswords", []))

    @jsii.member(jsii_name="resetTlsV1Enabled")
    def reset_tls_v1_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsV1Enabled", []))

    @builtins.property
    @jsii.member(jsii_name="kerberosArmoringEnabledInput")
    def kerberos_armoring_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberosArmoringEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberosRc4EncryptionEnabledInput")
    def kerberos_rc4_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "kerberosRc4EncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ntlmV1EnabledInput")
    def ntlm_v1_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ntlmV1EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="syncKerberosPasswordsInput")
    def sync_kerberos_passwords_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncKerberosPasswordsInput"))

    @builtins.property
    @jsii.member(jsii_name="syncNtlmPasswordsInput")
    def sync_ntlm_passwords_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncNtlmPasswordsInput"))

    @builtins.property
    @jsii.member(jsii_name="syncOnPremPasswordsInput")
    def sync_on_prem_passwords_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncOnPremPasswordsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsV1EnabledInput")
    def tls_v1_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsV1EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberosArmoringEnabled")
    def kerberos_armoring_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberosArmoringEnabled"))

    @kerberos_armoring_enabled.setter
    def kerberos_armoring_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30fd0268689e086d014309620bb3d7766cff8851f022ad635a5ad37156743aba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosArmoringEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberosRc4EncryptionEnabled")
    def kerberos_rc4_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "kerberosRc4EncryptionEnabled"))

    @kerberos_rc4_encryption_enabled.setter
    def kerberos_rc4_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2b62a59f18c06a78c65cb2fcb3d0f2a16dc5be6770db4c3d98fad4d259f242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosRc4EncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ntlmV1Enabled")
    def ntlm_v1_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ntlmV1Enabled"))

    @ntlm_v1_enabled.setter
    def ntlm_v1_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283ddc15a2e4e61d0d445049b1419a03459f53a3e3db542c70b95de5b50fe367)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ntlmV1Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncKerberosPasswords")
    def sync_kerberos_passwords(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncKerberosPasswords"))

    @sync_kerberos_passwords.setter
    def sync_kerberos_passwords(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c362c51954d8bb53daad09810be4f187c9b701c31fd32451ce9b1186d91bc8fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncKerberosPasswords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncNtlmPasswords")
    def sync_ntlm_passwords(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncNtlmPasswords"))

    @sync_ntlm_passwords.setter
    def sync_ntlm_passwords(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2eccaea079778510a8915db952548250db8967b2bea523e37ecdd1d0d8ba85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncNtlmPasswords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="syncOnPremPasswords")
    def sync_on_prem_passwords(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncOnPremPasswords"))

    @sync_on_prem_passwords.setter
    def sync_on_prem_passwords(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b023f4acfa23ed562e53a39fa87e98ad3bce9bb2aed4003ac9eeaf7288c51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncOnPremPasswords", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tlsV1Enabled")
    def tls_v1_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tlsV1Enabled"))

    @tls_v1_enabled.setter
    def tls_v1_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d31ebd453e192e525b7783e2c90dac25a2e9ea3ce761377ba780d1ae0a4d0af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsV1Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ActiveDirectoryDomainServiceSecurity]:
        return typing.cast(typing.Optional[ActiveDirectoryDomainServiceSecurity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ActiveDirectoryDomainServiceSecurity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49565cd03eaf0aca1e3dfa79f9ca773bcf54e761a3c30e1b7ee2d7aa2a98422)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ActiveDirectoryDomainServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#create ActiveDirectoryDomainService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#delete ActiveDirectoryDomainService#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#read ActiveDirectoryDomainService#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#update ActiveDirectoryDomainService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89fb31ce8dfe279cd58099670357363ae3bf2693b13466ba50d25a50197395f8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#create ActiveDirectoryDomainService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#delete ActiveDirectoryDomainService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#read ActiveDirectoryDomainService#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/active_directory_domain_service#update ActiveDirectoryDomainService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActiveDirectoryDomainServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActiveDirectoryDomainServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.activeDirectoryDomainService.ActiveDirectoryDomainServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf847a584d87df834c7c6e5d5920201e2a6c781c970ce5a2c8e4407598437240)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e472a3dc3637aac67cd700641e7f10ec098ea080ee07a91668c7f50d61ba919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc807d41b3867394689771b8eb88237980d3ee911faaa10a759e34dc84664a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f2227b4edc015d060bfd1bc8307e5fa7cbefb0400b98c04d44f4e99202f85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e41ad313821e02976b95858b7d31de046ea0ce4d00fb61fe1f45792524a2f62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActiveDirectoryDomainServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActiveDirectoryDomainServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActiveDirectoryDomainServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a562c67f385284850bfb1b3c34aed64efa70e59a8d6034547b1d52de273ca42d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ActiveDirectoryDomainService",
    "ActiveDirectoryDomainServiceConfig",
    "ActiveDirectoryDomainServiceInitialReplicaSet",
    "ActiveDirectoryDomainServiceInitialReplicaSetOutputReference",
    "ActiveDirectoryDomainServiceNotifications",
    "ActiveDirectoryDomainServiceNotificationsOutputReference",
    "ActiveDirectoryDomainServiceSecureLdap",
    "ActiveDirectoryDomainServiceSecureLdapOutputReference",
    "ActiveDirectoryDomainServiceSecurity",
    "ActiveDirectoryDomainServiceSecurityOutputReference",
    "ActiveDirectoryDomainServiceTimeouts",
    "ActiveDirectoryDomainServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__935e60fc566c3f79ae1064f5cf39bcc8581e7a9fdd2856d98cd6f98940e9121f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    domain_name: builtins.str,
    initial_replica_set: typing.Union[ActiveDirectoryDomainServiceInitialReplicaSet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: builtins.str,
    domain_configuration_type: typing.Optional[builtins.str] = None,
    filtered_sync_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Union[ActiveDirectoryDomainServiceNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    secure_ldap: typing.Optional[typing.Union[ActiveDirectoryDomainServiceSecureLdap, typing.Dict[builtins.str, typing.Any]]] = None,
    security: typing.Optional[typing.Union[ActiveDirectoryDomainServiceSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ActiveDirectoryDomainServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__88e0551e17fc036c8f42b94f46d29d7b8fcc4fb55c51258310733f22bd552426(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8a2683338bcf882741de34f72e5a2fccb4b33b1767ea53039936c5ac3d6e24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a3e81e8cbd0614ddb7c6c27e34c57f9ab2c5bdee82e907b08315ff4f4a09c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775e4c5bceea071558f2721f5f3db4ea41c63e5e5575bfb4ac05e4633efc000f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af1694e1e45138d70897ebd68a0cd1eb2f710770dcd48666bdf3b89a2213f1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd67d58781b303cad50b1d80a7a9e5718e1f69a833af6d1af42504bebba1bc8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca0b84c8505db2300e5c1d1114fd606d9d7ba499c8eb45d8e94812df44c2a83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd8a33329593ac6c082d837d64428d92f12116c30959f0a6ddb2eb2d1b00c67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba3eb4ed88e35fe3a9bb1be27b1564c995c60d311e85032a306b356bed9ed0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc35f190144ef9815b2e49979152dfa84a2ae758ccc8c901d5e948090ce12ed(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001e20e214c988034e843afa00ce3e0660074ba94cf23cabd7e1f01d428e4a23(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    domain_name: builtins.str,
    initial_replica_set: typing.Union[ActiveDirectoryDomainServiceInitialReplicaSet, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: builtins.str,
    domain_configuration_type: typing.Optional[builtins.str] = None,
    filtered_sync_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Union[ActiveDirectoryDomainServiceNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    secure_ldap: typing.Optional[typing.Union[ActiveDirectoryDomainServiceSecureLdap, typing.Dict[builtins.str, typing.Any]]] = None,
    security: typing.Optional[typing.Union[ActiveDirectoryDomainServiceSecurity, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ActiveDirectoryDomainServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49943bda77f4ea7fa49652a67a9ae4f0f41ce3576abe84795991e630b66c29e(
    *,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07bacf9a2762ceab8b00f6258439fb48a4c5d22a6822401f802fdff6ec31a0eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07f1553ecfa53bca424737565f597b575f360868e3ab9d0a5f3a00b921d0828(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe85ead5d03d1622f92e541816759b84d1b5c87a58ccca307d588f8ffa08498(
    value: typing.Optional[ActiveDirectoryDomainServiceInitialReplicaSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cd1ed6a424aed946fa33d53b6bc15b90a4d5389abc580766a26d09cc9657e74(
    *,
    additional_recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify_dc_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    notify_global_admins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a689cdb6772d9e1671b6a9a93f29cb407081c087e8d3b093a33e7f90c23a39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52932bc4cf4116434bd78bd3b795606658f29c657f4693045f40a17264392cf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b7d4cb4d5f75b6d1b22557a87bd4520431f8330b746188911ca87e88867a39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e378dae86cbabbd043946ea5e37110870f3a8d4c3db1cb4fb52121419943c1ff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2aa3f0974303d919abc3b36c458539cb0546f8234d31a2fd40eebb977e62702(
    value: typing.Optional[ActiveDirectoryDomainServiceNotifications],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320535be9ba94e8b76a7304e453272dd3ed45e74e804fa2dd7bd7385309a82df(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    pfx_certificate: builtins.str,
    pfx_certificate_password: builtins.str,
    external_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a314601dc9e1abfb9f1836a22dee681435070fe65edcc0507cbfd71db0435e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe3e0deb551caec553d08475c93ab879ea61d6105ddb24062f756c605b7efe5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1bb77b4e3be04dfb40fe82d15084e70c7999d7447eaddf6aa9465c23f614d4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4adc7eb44f6ffc9510e777d147d8c26dd050775758e8bdab23b9c321eeeb4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4815615879370f81fb6601fe8d65eb358cbc3d5e1c3784c4c1f532fd89690a84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985c1916445f6817c36dd40012d3a4e0ad3c43feb7ccd33e2ed216b5a78b428e(
    value: typing.Optional[ActiveDirectoryDomainServiceSecureLdap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363a7284ca8cd397190c8be666c719b2471ed42e6d98ad740142961f33f9e673(
    *,
    kerberos_armoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    kerberos_rc4_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ntlm_v1_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_kerberos_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_ntlm_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_on_prem_passwords: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tls_v1_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ccc753f5b69921e890e77234487b54165fa2bc177bc07362325d8605779a86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30fd0268689e086d014309620bb3d7766cff8851f022ad635a5ad37156743aba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2b62a59f18c06a78c65cb2fcb3d0f2a16dc5be6770db4c3d98fad4d259f242(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283ddc15a2e4e61d0d445049b1419a03459f53a3e3db542c70b95de5b50fe367(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c362c51954d8bb53daad09810be4f187c9b701c31fd32451ce9b1186d91bc8fa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2eccaea079778510a8915db952548250db8967b2bea523e37ecdd1d0d8ba85(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b023f4acfa23ed562e53a39fa87e98ad3bce9bb2aed4003ac9eeaf7288c51a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d31ebd453e192e525b7783e2c90dac25a2e9ea3ce761377ba780d1ae0a4d0af(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49565cd03eaf0aca1e3dfa79f9ca773bcf54e761a3c30e1b7ee2d7aa2a98422(
    value: typing.Optional[ActiveDirectoryDomainServiceSecurity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fb31ce8dfe279cd58099670357363ae3bf2693b13466ba50d25a50197395f8(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf847a584d87df834c7c6e5d5920201e2a6c781c970ce5a2c8e4407598437240(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e472a3dc3637aac67cd700641e7f10ec098ea080ee07a91668c7f50d61ba919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc807d41b3867394689771b8eb88237980d3ee911faaa10a759e34dc84664a67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f2227b4edc015d060bfd1bc8307e5fa7cbefb0400b98c04d44f4e99202f85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e41ad313821e02976b95858b7d31de046ea0ce4d00fb61fe1f45792524a2f62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a562c67f385284850bfb1b3c34aed64efa70e59a8d6034547b1d52de273ca42d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ActiveDirectoryDomainServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

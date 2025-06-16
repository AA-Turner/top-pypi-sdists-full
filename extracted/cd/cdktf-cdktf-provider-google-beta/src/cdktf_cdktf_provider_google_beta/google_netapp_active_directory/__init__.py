r'''
# `google_netapp_active_directory`

Refer to the Terraform Registry for docs: [`google_netapp_active_directory`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory).
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


class GoogleNetappActiveDirectory(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappActiveDirectory.GoogleNetappActiveDirectory",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory google_netapp_active_directory}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dns: builtins.str,
        domain: builtins.str,
        location: builtins.str,
        name: builtins.str,
        net_bios_prefix: builtins.str,
        password: builtins.str,
        username: builtins.str,
        administrators: typing.Optional[typing.Sequence[builtins.str]] = None,
        aes_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        encrypt_dc_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        kdc_hostname: typing.Optional[builtins.str] = None,
        kdc_ip: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ldap_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        nfs_users_with_ldap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        security_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
        site: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetappActiveDirectoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory google_netapp_active_directory} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dns: Comma separated list of DNS server IP addresses for the Active Directory domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#dns GoogleNetappActiveDirectory#dns}
        :param domain: Fully qualified domain name for the Active Directory domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#domain GoogleNetappActiveDirectory#domain}
        :param location: Name of the region for the policy to apply to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#location GoogleNetappActiveDirectory#location}
        :param name: The resource name of the Active Directory pool. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#name GoogleNetappActiveDirectory#name}
        :param net_bios_prefix: NetBIOS name prefix of the server to be created. A five-character random ID is generated automatically, for example, -6f9a, and appended to the prefix. The full UNC share path will have the following format: '\\NetBIOS_PREFIX-ABCD.DOMAIN_NAME\\SHARE_NAME' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#net_bios_prefix GoogleNetappActiveDirectory#net_bios_prefix}
        :param password: Password for specified username. Note - Manual changes done to the password will not be detected. Terraform will not re-apply the password, unless you use a new password in Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#password GoogleNetappActiveDirectory#password}
        :param username: Username for the Active Directory account with permissions to create the compute account within the specified organizational unit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#username GoogleNetappActiveDirectory#username}
        :param administrators: Domain user accounts to be added to the local Administrators group of the SMB service. Comma-separated list of domain users or groups. The Domain Admin group is automatically added when the service joins your domain as a hidden group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#administrators GoogleNetappActiveDirectory#administrators}
        :param aes_encryption: Enables AES-128 and AES-256 encryption for Kerberos-based communication with Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#aes_encryption GoogleNetappActiveDirectory#aes_encryption}
        :param backup_operators: Domain user/group accounts to be added to the Backup Operators group of the SMB service. The Backup Operators group allows members to backup and restore files regardless of whether they have read or write access to the files. Comma-separated list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#backup_operators GoogleNetappActiveDirectory#backup_operators}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#description GoogleNetappActiveDirectory#description}
        :param encrypt_dc_connections: If enabled, traffic between the SMB server to Domain Controller (DC) will be encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#encrypt_dc_connections GoogleNetappActiveDirectory#encrypt_dc_connections}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#id GoogleNetappActiveDirectory#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kdc_hostname: Hostname of the Active Directory server used as Kerberos Key Distribution Center. Only required for volumes using kerberized NFSv4.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#kdc_hostname GoogleNetappActiveDirectory#kdc_hostname}
        :param kdc_ip: IP address of the Active Directory server used as Kerberos Key Distribution Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#kdc_ip GoogleNetappActiveDirectory#kdc_ip}
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#labels GoogleNetappActiveDirectory#labels}
        :param ldap_signing: Specifies whether or not the LDAP traffic needs to be signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#ldap_signing GoogleNetappActiveDirectory#ldap_signing}
        :param nfs_users_with_ldap: Local UNIX users on clients without valid user information in Active Directory are blocked from access to LDAP enabled volumes. This option can be used to temporarily switch such volumes to AUTH_SYS authentication (user ID + 1-16 groups). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#nfs_users_with_ldap GoogleNetappActiveDirectory#nfs_users_with_ldap}
        :param organizational_unit: Name of the Organizational Unit where you intend to create the computer account for NetApp Volumes. Defaults to 'CN=Computers' if left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#organizational_unit GoogleNetappActiveDirectory#organizational_unit}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#project GoogleNetappActiveDirectory#project}.
        :param security_operators: Domain accounts that require elevated privileges such as 'SeSecurityPrivilege' to manage security logs. Comma-separated list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#security_operators GoogleNetappActiveDirectory#security_operators}
        :param site: Specifies an Active Directory site to manage domain controller selection. Use when Active Directory domain controllers in multiple regions are configured. Defaults to 'Default-First-Site-Name' if left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#site GoogleNetappActiveDirectory#site}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#timeouts GoogleNetappActiveDirectory#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9fd699d78ac0d74bd666c0fffc815333905903b1e090cc9da6f999c8998023)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetappActiveDirectoryConfig(
            dns=dns,
            domain=domain,
            location=location,
            name=name,
            net_bios_prefix=net_bios_prefix,
            password=password,
            username=username,
            administrators=administrators,
            aes_encryption=aes_encryption,
            backup_operators=backup_operators,
            description=description,
            encrypt_dc_connections=encrypt_dc_connections,
            id=id,
            kdc_hostname=kdc_hostname,
            kdc_ip=kdc_ip,
            labels=labels,
            ldap_signing=ldap_signing,
            nfs_users_with_ldap=nfs_users_with_ldap,
            organizational_unit=organizational_unit,
            project=project,
            security_operators=security_operators,
            site=site,
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
        '''Generates CDKTF code for importing a GoogleNetappActiveDirectory resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetappActiveDirectory to import.
        :param import_from_id: The id of the existing GoogleNetappActiveDirectory that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetappActiveDirectory to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__369e860df184797da25f82e1e85b4496966f97ad9ce4a511d21281f447a23b54)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#create GoogleNetappActiveDirectory#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#delete GoogleNetappActiveDirectory#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#update GoogleNetappActiveDirectory#update}.
        '''
        value = GoogleNetappActiveDirectoryTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdministrators")
    def reset_administrators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdministrators", []))

    @jsii.member(jsii_name="resetAesEncryption")
    def reset_aes_encryption(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAesEncryption", []))

    @jsii.member(jsii_name="resetBackupOperators")
    def reset_backup_operators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupOperators", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryptDcConnections")
    def reset_encrypt_dc_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptDcConnections", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKdcHostname")
    def reset_kdc_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKdcHostname", []))

    @jsii.member(jsii_name="resetKdcIp")
    def reset_kdc_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKdcIp", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLdapSigning")
    def reset_ldap_signing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLdapSigning", []))

    @jsii.member(jsii_name="resetNfsUsersWithLdap")
    def reset_nfs_users_with_ldap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfsUsersWithLdap", []))

    @jsii.member(jsii_name="resetOrganizationalUnit")
    def reset_organizational_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrganizationalUnit", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSecurityOperators")
    def reset_security_operators(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityOperators", []))

    @jsii.member(jsii_name="resetSite")
    def reset_site(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSite", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateDetails")
    def state_details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateDetails"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleNetappActiveDirectoryTimeoutsOutputReference":
        return typing.cast("GoogleNetappActiveDirectoryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="administratorsInput")
    def administrators_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "administratorsInput"))

    @builtins.property
    @jsii.member(jsii_name="aesEncryptionInput")
    def aes_encryption_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "aesEncryptionInput"))

    @builtins.property
    @jsii.member(jsii_name="backupOperatorsInput")
    def backup_operators_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "backupOperatorsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsInput")
    def dns_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptDcConnectionsInput")
    def encrypt_dc_connections_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptDcConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kdcHostnameInput")
    def kdc_hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kdcHostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="kdcIpInput")
    def kdc_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kdcIpInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="ldapSigningInput")
    def ldap_signing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ldapSigningInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="netBiosPrefixInput")
    def net_bios_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netBiosPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsUsersWithLdapInput")
    def nfs_users_with_ldap_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nfsUsersWithLdapInput"))

    @builtins.property
    @jsii.member(jsii_name="organizationalUnitInput")
    def organizational_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "organizationalUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="securityOperatorsInput")
    def security_operators_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityOperatorsInput"))

    @builtins.property
    @jsii.member(jsii_name="siteInput")
    def site_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "siteInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetappActiveDirectoryTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetappActiveDirectoryTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="administrators")
    def administrators(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "administrators"))

    @administrators.setter
    def administrators(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6832b41a85507b436e168b8af7d4fad1f2702ec4dfe2ed2fc8007181dd4a0cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "administrators", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="aesEncryption")
    def aes_encryption(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "aesEncryption"))

    @aes_encryption.setter
    def aes_encryption(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1b4df3f7bf83d1708fd4aaad502e6e99a04ab66edced79b3b1433751efc917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aesEncryption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="backupOperators")
    def backup_operators(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "backupOperators"))

    @backup_operators.setter
    def backup_operators(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e83e2b198a951ec48b333ebe4d87b8dba953f1613977849bd2e28e9f00dbd72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupOperators", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7082a370fa44b39ba86bb9717905ca0bf68019ecb906b0814b28afab1e27cb1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dns"))

    @dns.setter
    def dns(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddde809614329312f0bd6aef31781bd3f4473c86b1a7f9d7b6238a92809c6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fef1090bc9980c38bc5d6bf63b14d3297b01509d32d60c312ee9b15c6bb64bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptDcConnections")
    def encrypt_dc_connections(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptDcConnections"))

    @encrypt_dc_connections.setter
    def encrypt_dc_connections(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381e7ad111f058ad6420b33167210af69dcf53c55046caba60411caa588e9b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptDcConnections", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ff6e0084d9ccbb774b2c204397183ebdde3ebcd976b71a297ecfa40fbe3cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kdcHostname")
    def kdc_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kdcHostname"))

    @kdc_hostname.setter
    def kdc_hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efcc18357861e6446e7f318410210776edcd15ae51d228d4537cfa55e98c620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kdcHostname", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kdcIp")
    def kdc_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kdcIp"))

    @kdc_ip.setter
    def kdc_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a3be12c10aa48276e6348c544c63f729f9cec5619df7a6a5f24352a5f5d2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kdcIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4db9b661d60d1d4e768da8f3607acd5c2a07836ca6401b286db04640b87b7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ldapSigning")
    def ldap_signing(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ldapSigning"))

    @ldap_signing.setter
    def ldap_signing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad610ba579067d10e17b2c1879fa4a5a698172bcc5dc251bb97ae5a4b4d3fd06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ldapSigning", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfde8e9754a389bbe7a548ad209874b39b1f65b86ff4b0fce21da6141eab1dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d0221017caa94328c71b213a01e1bef047a5b9ca6ab73622676ecf132e1566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netBiosPrefix")
    def net_bios_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netBiosPrefix"))

    @net_bios_prefix.setter
    def net_bios_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f23416156a463ab89224a11bff8eff2b97dc9bba4f827756d5314a1c76a4648c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netBiosPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsUsersWithLdap")
    def nfs_users_with_ldap(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nfsUsersWithLdap"))

    @nfs_users_with_ldap.setter
    def nfs_users_with_ldap(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac784a1f808e788289c77a2efbccabe87414bc56b0c7331d2d6a059d26415952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsUsersWithLdap", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="organizationalUnit")
    def organizational_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organizationalUnit"))

    @organizational_unit.setter
    def organizational_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe00aa1f7bb13ec7c9708fadcc84816b1eb94b80fa53aa8325cf7971a902911)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "organizationalUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfdca0c05ac8f197fa0c0d25476b1b6a4e0134952432a3e3b0ac22802f57537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70783669c4e3dbf3e0a8938f79286e083bc0459a4f9c240937608fe47ef13fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityOperators")
    def security_operators(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityOperators"))

    @security_operators.setter
    def security_operators(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee37c39e498711054df3f623f708e228fd01aec2f1bd2d8fe28898c6fbf3c9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityOperators", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="site")
    def site(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "site"))

    @site.setter
    def site(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717ab5599396c3407be3d1213574f296559323389ac97bfc0df60603c05a5378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "site", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d309c61280d8090ff7ae0b4c87b1d60a4a7e012a13e2505de3f62659ff3c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappActiveDirectory.GoogleNetappActiveDirectoryConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dns": "dns",
        "domain": "domain",
        "location": "location",
        "name": "name",
        "net_bios_prefix": "netBiosPrefix",
        "password": "password",
        "username": "username",
        "administrators": "administrators",
        "aes_encryption": "aesEncryption",
        "backup_operators": "backupOperators",
        "description": "description",
        "encrypt_dc_connections": "encryptDcConnections",
        "id": "id",
        "kdc_hostname": "kdcHostname",
        "kdc_ip": "kdcIp",
        "labels": "labels",
        "ldap_signing": "ldapSigning",
        "nfs_users_with_ldap": "nfsUsersWithLdap",
        "organizational_unit": "organizationalUnit",
        "project": "project",
        "security_operators": "securityOperators",
        "site": "site",
        "timeouts": "timeouts",
    },
)
class GoogleNetappActiveDirectoryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dns: builtins.str,
        domain: builtins.str,
        location: builtins.str,
        name: builtins.str,
        net_bios_prefix: builtins.str,
        password: builtins.str,
        username: builtins.str,
        administrators: typing.Optional[typing.Sequence[builtins.str]] = None,
        aes_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backup_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        encrypt_dc_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        kdc_hostname: typing.Optional[builtins.str] = None,
        kdc_ip: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        ldap_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        nfs_users_with_ldap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        organizational_unit: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        security_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
        site: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetappActiveDirectoryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dns: Comma separated list of DNS server IP addresses for the Active Directory domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#dns GoogleNetappActiveDirectory#dns}
        :param domain: Fully qualified domain name for the Active Directory domain. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#domain GoogleNetappActiveDirectory#domain}
        :param location: Name of the region for the policy to apply to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#location GoogleNetappActiveDirectory#location}
        :param name: The resource name of the Active Directory pool. Needs to be unique per location. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#name GoogleNetappActiveDirectory#name}
        :param net_bios_prefix: NetBIOS name prefix of the server to be created. A five-character random ID is generated automatically, for example, -6f9a, and appended to the prefix. The full UNC share path will have the following format: '\\NetBIOS_PREFIX-ABCD.DOMAIN_NAME\\SHARE_NAME' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#net_bios_prefix GoogleNetappActiveDirectory#net_bios_prefix}
        :param password: Password for specified username. Note - Manual changes done to the password will not be detected. Terraform will not re-apply the password, unless you use a new password in Terraform. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#password GoogleNetappActiveDirectory#password}
        :param username: Username for the Active Directory account with permissions to create the compute account within the specified organizational unit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#username GoogleNetappActiveDirectory#username}
        :param administrators: Domain user accounts to be added to the local Administrators group of the SMB service. Comma-separated list of domain users or groups. The Domain Admin group is automatically added when the service joins your domain as a hidden group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#administrators GoogleNetappActiveDirectory#administrators}
        :param aes_encryption: Enables AES-128 and AES-256 encryption for Kerberos-based communication with Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#aes_encryption GoogleNetappActiveDirectory#aes_encryption}
        :param backup_operators: Domain user/group accounts to be added to the Backup Operators group of the SMB service. The Backup Operators group allows members to backup and restore files regardless of whether they have read or write access to the files. Comma-separated list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#backup_operators GoogleNetappActiveDirectory#backup_operators}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#description GoogleNetappActiveDirectory#description}
        :param encrypt_dc_connections: If enabled, traffic between the SMB server to Domain Controller (DC) will be encrypted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#encrypt_dc_connections GoogleNetappActiveDirectory#encrypt_dc_connections}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#id GoogleNetappActiveDirectory#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kdc_hostname: Hostname of the Active Directory server used as Kerberos Key Distribution Center. Only required for volumes using kerberized NFSv4.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#kdc_hostname GoogleNetappActiveDirectory#kdc_hostname}
        :param kdc_ip: IP address of the Active Directory server used as Kerberos Key Distribution Center. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#kdc_ip GoogleNetappActiveDirectory#kdc_ip}
        :param labels: Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#labels GoogleNetappActiveDirectory#labels}
        :param ldap_signing: Specifies whether or not the LDAP traffic needs to be signed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#ldap_signing GoogleNetappActiveDirectory#ldap_signing}
        :param nfs_users_with_ldap: Local UNIX users on clients without valid user information in Active Directory are blocked from access to LDAP enabled volumes. This option can be used to temporarily switch such volumes to AUTH_SYS authentication (user ID + 1-16 groups). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#nfs_users_with_ldap GoogleNetappActiveDirectory#nfs_users_with_ldap}
        :param organizational_unit: Name of the Organizational Unit where you intend to create the computer account for NetApp Volumes. Defaults to 'CN=Computers' if left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#organizational_unit GoogleNetappActiveDirectory#organizational_unit}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#project GoogleNetappActiveDirectory#project}.
        :param security_operators: Domain accounts that require elevated privileges such as 'SeSecurityPrivilege' to manage security logs. Comma-separated list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#security_operators GoogleNetappActiveDirectory#security_operators}
        :param site: Specifies an Active Directory site to manage domain controller selection. Use when Active Directory domain controllers in multiple regions are configured. Defaults to 'Default-First-Site-Name' if left empty. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#site GoogleNetappActiveDirectory#site}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#timeouts GoogleNetappActiveDirectory#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetappActiveDirectoryTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f5f552eadad7140174018a8efd06e618df10d9f7c2859fa0ef944d0b4816e2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument net_bios_prefix", value=net_bios_prefix, expected_type=type_hints["net_bios_prefix"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument administrators", value=administrators, expected_type=type_hints["administrators"])
            check_type(argname="argument aes_encryption", value=aes_encryption, expected_type=type_hints["aes_encryption"])
            check_type(argname="argument backup_operators", value=backup_operators, expected_type=type_hints["backup_operators"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encrypt_dc_connections", value=encrypt_dc_connections, expected_type=type_hints["encrypt_dc_connections"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kdc_hostname", value=kdc_hostname, expected_type=type_hints["kdc_hostname"])
            check_type(argname="argument kdc_ip", value=kdc_ip, expected_type=type_hints["kdc_ip"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument ldap_signing", value=ldap_signing, expected_type=type_hints["ldap_signing"])
            check_type(argname="argument nfs_users_with_ldap", value=nfs_users_with_ldap, expected_type=type_hints["nfs_users_with_ldap"])
            check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument security_operators", value=security_operators, expected_type=type_hints["security_operators"])
            check_type(argname="argument site", value=site, expected_type=type_hints["site"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns": dns,
            "domain": domain,
            "location": location,
            "name": name,
            "net_bios_prefix": net_bios_prefix,
            "password": password,
            "username": username,
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
        if administrators is not None:
            self._values["administrators"] = administrators
        if aes_encryption is not None:
            self._values["aes_encryption"] = aes_encryption
        if backup_operators is not None:
            self._values["backup_operators"] = backup_operators
        if description is not None:
            self._values["description"] = description
        if encrypt_dc_connections is not None:
            self._values["encrypt_dc_connections"] = encrypt_dc_connections
        if id is not None:
            self._values["id"] = id
        if kdc_hostname is not None:
            self._values["kdc_hostname"] = kdc_hostname
        if kdc_ip is not None:
            self._values["kdc_ip"] = kdc_ip
        if labels is not None:
            self._values["labels"] = labels
        if ldap_signing is not None:
            self._values["ldap_signing"] = ldap_signing
        if nfs_users_with_ldap is not None:
            self._values["nfs_users_with_ldap"] = nfs_users_with_ldap
        if organizational_unit is not None:
            self._values["organizational_unit"] = organizational_unit
        if project is not None:
            self._values["project"] = project
        if security_operators is not None:
            self._values["security_operators"] = security_operators
        if site is not None:
            self._values["site"] = site
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
    def dns(self) -> builtins.str:
        '''Comma separated list of DNS server IP addresses for the Active Directory domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#dns GoogleNetappActiveDirectory#dns}
        '''
        result = self._values.get("dns")
        assert result is not None, "Required property 'dns' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain(self) -> builtins.str:
        '''Fully qualified domain name for the Active Directory domain.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#domain GoogleNetappActiveDirectory#domain}
        '''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Name of the region for the policy to apply to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#location GoogleNetappActiveDirectory#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name of the Active Directory pool. Needs to be unique per location.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#name GoogleNetappActiveDirectory#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def net_bios_prefix(self) -> builtins.str:
        '''NetBIOS name prefix of the server to be created.

        A five-character random ID is generated automatically, for example, -6f9a, and appended to the prefix. The full UNC share path will have the following format:
        '\\NetBIOS_PREFIX-ABCD.DOMAIN_NAME\\SHARE_NAME'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#net_bios_prefix GoogleNetappActiveDirectory#net_bios_prefix}
        '''
        result = self._values.get("net_bios_prefix")
        assert result is not None, "Required property 'net_bios_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Password for specified username.

        Note - Manual changes done to the password will not be detected. Terraform will not re-apply the password, unless you use a new password in Terraform.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#password GoogleNetappActiveDirectory#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for the Active Directory account with permissions to create the compute account within the specified organizational unit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#username GoogleNetappActiveDirectory#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def administrators(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Domain user accounts to be added to the local Administrators group of the SMB service.

        Comma-separated list of domain users or groups. The Domain Admin group is automatically added when the service joins your domain as a hidden group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#administrators GoogleNetappActiveDirectory#administrators}
        '''
        result = self._values.get("administrators")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def aes_encryption(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables AES-128 and AES-256 encryption for Kerberos-based communication with Active Directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#aes_encryption GoogleNetappActiveDirectory#aes_encryption}
        '''
        result = self._values.get("aes_encryption")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backup_operators(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Domain user/group accounts to be added to the Backup Operators group of the SMB service.

        The Backup Operators group allows members to backup and restore files regardless of whether they have read or write access to the files. Comma-separated list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#backup_operators GoogleNetappActiveDirectory#backup_operators}
        '''
        result = self._values.get("backup_operators")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#description GoogleNetappActiveDirectory#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypt_dc_connections(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If enabled, traffic between the SMB server to Domain Controller (DC) will be encrypted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#encrypt_dc_connections GoogleNetappActiveDirectory#encrypt_dc_connections}
        '''
        result = self._values.get("encrypt_dc_connections")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#id GoogleNetappActiveDirectory#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kdc_hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname of the Active Directory server used as Kerberos Key Distribution Center. Only required for volumes using kerberized NFSv4.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#kdc_hostname GoogleNetappActiveDirectory#kdc_hostname}
        '''
        result = self._values.get("kdc_hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kdc_ip(self) -> typing.Optional[builtins.str]:
        '''IP address of the Active Directory server used as Kerberos Key Distribution Center.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#kdc_ip GoogleNetappActiveDirectory#kdc_ip}
        '''
        result = self._values.get("kdc_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels as key value pairs. Example: '{ "owner": "Bob", "department": "finance", "purpose": "testing" }'.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#labels GoogleNetappActiveDirectory#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def ldap_signing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether or not the LDAP traffic needs to be signed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#ldap_signing GoogleNetappActiveDirectory#ldap_signing}
        '''
        result = self._values.get("ldap_signing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def nfs_users_with_ldap(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Local UNIX users on clients without valid user information in Active Directory are blocked from access to LDAP enabled volumes.

        This option can be used to temporarily switch such volumes to AUTH_SYS authentication (user ID + 1-16 groups).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#nfs_users_with_ldap GoogleNetappActiveDirectory#nfs_users_with_ldap}
        '''
        result = self._values.get("nfs_users_with_ldap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def organizational_unit(self) -> typing.Optional[builtins.str]:
        '''Name of the Organizational Unit where you intend to create the computer account for NetApp Volumes.

        Defaults to 'CN=Computers' if left empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#organizational_unit GoogleNetappActiveDirectory#organizational_unit}
        '''
        result = self._values.get("organizational_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#project GoogleNetappActiveDirectory#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_operators(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Domain accounts that require elevated privileges such as 'SeSecurityPrivilege' to manage security logs. Comma-separated list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#security_operators GoogleNetappActiveDirectory#security_operators}
        '''
        result = self._values.get("security_operators")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def site(self) -> typing.Optional[builtins.str]:
        '''Specifies an Active Directory site to manage domain controller selection.

        Use when Active Directory domain controllers in multiple regions are configured. Defaults to 'Default-First-Site-Name' if left empty.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#site GoogleNetappActiveDirectory#site}
        '''
        result = self._values.get("site")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleNetappActiveDirectoryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#timeouts GoogleNetappActiveDirectory#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetappActiveDirectoryTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappActiveDirectoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetappActiveDirectory.GoogleNetappActiveDirectoryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetappActiveDirectoryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#create GoogleNetappActiveDirectory#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#delete GoogleNetappActiveDirectory#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#update GoogleNetappActiveDirectory#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a17f4808bd9372122811ef38832913c0bde39d8b36516730fbc598afd1c23e5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#create GoogleNetappActiveDirectory#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#delete GoogleNetappActiveDirectory#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_netapp_active_directory#update GoogleNetappActiveDirectory#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetappActiveDirectoryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetappActiveDirectoryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetappActiveDirectory.GoogleNetappActiveDirectoryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad1bf7ad4fe557065a69e1b87c3d4a6813d2aba7d91388e4e6175ec2c3affd66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14b41fc504f4d57390ab9d822b4bf802ae172dbe2fb9caaaff36108c11cf1103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbab5270142240c2b4a8688df2e92a7519539974f3c2ae1410e786726d6d4a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53679a14a24c3ee514685e014f5659bcd484200c0b86f52be10700dcee28a901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappActiveDirectoryTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappActiveDirectoryTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappActiveDirectoryTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d93c5b975d4e3a26a9f0be6cf5bc864eb3361bb2696e523a06d51fbc670b3d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetappActiveDirectory",
    "GoogleNetappActiveDirectoryConfig",
    "GoogleNetappActiveDirectoryTimeouts",
    "GoogleNetappActiveDirectoryTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__5a9fd699d78ac0d74bd666c0fffc815333905903b1e090cc9da6f999c8998023(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dns: builtins.str,
    domain: builtins.str,
    location: builtins.str,
    name: builtins.str,
    net_bios_prefix: builtins.str,
    password: builtins.str,
    username: builtins.str,
    administrators: typing.Optional[typing.Sequence[builtins.str]] = None,
    aes_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    encrypt_dc_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    kdc_hostname: typing.Optional[builtins.str] = None,
    kdc_ip: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ldap_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    nfs_users_with_ldap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    security_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
    site: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetappActiveDirectoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__369e860df184797da25f82e1e85b4496966f97ad9ce4a511d21281f447a23b54(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6832b41a85507b436e168b8af7d4fad1f2702ec4dfe2ed2fc8007181dd4a0cc7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1b4df3f7bf83d1708fd4aaad502e6e99a04ab66edced79b3b1433751efc917(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e83e2b198a951ec48b333ebe4d87b8dba953f1613977849bd2e28e9f00dbd72(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7082a370fa44b39ba86bb9717905ca0bf68019ecb906b0814b28afab1e27cb1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddde809614329312f0bd6aef31781bd3f4473c86b1a7f9d7b6238a92809c6f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fef1090bc9980c38bc5d6bf63b14d3297b01509d32d60c312ee9b15c6bb64bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381e7ad111f058ad6420b33167210af69dcf53c55046caba60411caa588e9b5d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ff6e0084d9ccbb774b2c204397183ebdde3ebcd976b71a297ecfa40fbe3cf5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efcc18357861e6446e7f318410210776edcd15ae51d228d4537cfa55e98c620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a3be12c10aa48276e6348c544c63f729f9cec5619df7a6a5f24352a5f5d2d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4db9b661d60d1d4e768da8f3607acd5c2a07836ca6401b286db04640b87b7e8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad610ba579067d10e17b2c1879fa4a5a698172bcc5dc251bb97ae5a4b4d3fd06(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfde8e9754a389bbe7a548ad209874b39b1f65b86ff4b0fce21da6141eab1dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d0221017caa94328c71b213a01e1bef047a5b9ca6ab73622676ecf132e1566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f23416156a463ab89224a11bff8eff2b97dc9bba4f827756d5314a1c76a4648c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac784a1f808e788289c77a2efbccabe87414bc56b0c7331d2d6a059d26415952(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe00aa1f7bb13ec7c9708fadcc84816b1eb94b80fa53aa8325cf7971a902911(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfdca0c05ac8f197fa0c0d25476b1b6a4e0134952432a3e3b0ac22802f57537(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70783669c4e3dbf3e0a8938f79286e083bc0459a4f9c240937608fe47ef13fc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee37c39e498711054df3f623f708e228fd01aec2f1bd2d8fe28898c6fbf3c9dd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717ab5599396c3407be3d1213574f296559323389ac97bfc0df60603c05a5378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d309c61280d8090ff7ae0b4c87b1d60a4a7e012a13e2505de3f62659ff3c63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f5f552eadad7140174018a8efd06e618df10d9f7c2859fa0ef944d0b4816e2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dns: builtins.str,
    domain: builtins.str,
    location: builtins.str,
    name: builtins.str,
    net_bios_prefix: builtins.str,
    password: builtins.str,
    username: builtins.str,
    administrators: typing.Optional[typing.Sequence[builtins.str]] = None,
    aes_encryption: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backup_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    encrypt_dc_connections: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    kdc_hostname: typing.Optional[builtins.str] = None,
    kdc_ip: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ldap_signing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    nfs_users_with_ldap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    security_operators: typing.Optional[typing.Sequence[builtins.str]] = None,
    site: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetappActiveDirectoryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a17f4808bd9372122811ef38832913c0bde39d8b36516730fbc598afd1c23e5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1bf7ad4fe557065a69e1b87c3d4a6813d2aba7d91388e4e6175ec2c3affd66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b41fc504f4d57390ab9d822b4bf802ae172dbe2fb9caaaff36108c11cf1103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbab5270142240c2b4a8688df2e92a7519539974f3c2ae1410e786726d6d4a99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53679a14a24c3ee514685e014f5659bcd484200c0b86f52be10700dcee28a901(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d93c5b975d4e3a26a9f0be6cf5bc864eb3361bb2696e523a06d51fbc670b3d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetappActiveDirectoryTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

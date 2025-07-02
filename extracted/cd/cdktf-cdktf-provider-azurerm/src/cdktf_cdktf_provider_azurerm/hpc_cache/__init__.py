r'''
# `azurerm_hpc_cache`

Refer to the Terraform Registry for docs: [`azurerm_hpc_cache`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache).
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


class HpcCache(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCache",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache azurerm_hpc_cache}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cache_size_in_gb: jsii.Number,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku_name: builtins.str,
        subnet_id: builtins.str,
        automatically_rotate_key_to_latest_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_access_policy: typing.Optional[typing.Union["HpcCacheDefaultAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        directory_active_directory: typing.Optional[typing.Union["HpcCacheDirectoryActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        directory_flat_file: typing.Optional[typing.Union["HpcCacheDirectoryFlatFile", typing.Dict[builtins.str, typing.Any]]] = None,
        directory_ldap: typing.Optional[typing.Union["HpcCacheDirectoryLdap", typing.Dict[builtins.str, typing.Any]]] = None,
        dns: typing.Optional[typing.Union["HpcCacheDns", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["HpcCacheIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        ntp_server: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HpcCacheTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache azurerm_hpc_cache} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cache_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#cache_size_in_gb HpcCache#cache_size_in_gb}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#location HpcCache#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#name HpcCache#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#resource_group_name HpcCache#resource_group_name}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#sku_name HpcCache#sku_name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#subnet_id HpcCache#subnet_id}.
        :param automatically_rotate_key_to_latest_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#automatically_rotate_key_to_latest_enabled HpcCache#automatically_rotate_key_to_latest_enabled}.
        :param default_access_policy: default_access_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#default_access_policy HpcCache#default_access_policy}
        :param directory_active_directory: directory_active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_active_directory HpcCache#directory_active_directory}
        :param directory_flat_file: directory_flat_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_flat_file HpcCache#directory_flat_file}
        :param directory_ldap: directory_ldap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_ldap HpcCache#directory_ldap}
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns HpcCache#dns}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#id HpcCache#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#identity HpcCache#identity}
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#key_vault_key_id HpcCache#key_vault_key_id}.
        :param mtu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#mtu HpcCache#mtu}.
        :param ntp_server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#ntp_server HpcCache#ntp_server}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#tags HpcCache#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#timeouts HpcCache#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8001c815869451fe98f943f28e3505f27ae65151dd023bd03c49167ffa724bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = HpcCacheConfig(
            cache_size_in_gb=cache_size_in_gb,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            sku_name=sku_name,
            subnet_id=subnet_id,
            automatically_rotate_key_to_latest_enabled=automatically_rotate_key_to_latest_enabled,
            default_access_policy=default_access_policy,
            directory_active_directory=directory_active_directory,
            directory_flat_file=directory_flat_file,
            directory_ldap=directory_ldap,
            dns=dns,
            id=id,
            identity=identity,
            key_vault_key_id=key_vault_key_id,
            mtu=mtu,
            ntp_server=ntp_server,
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
        '''Generates CDKTF code for importing a HpcCache resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the HpcCache to import.
        :param import_from_id: The id of the existing HpcCache that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the HpcCache to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e70b764de6274b17c6fb457cdf0c545abaa8d3132142ff36838fffc636e538c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDefaultAccessPolicy")
    def put_default_access_policy(
        self,
        *,
        access_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HpcCacheDefaultAccessPolicyAccessRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param access_rule: access_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#access_rule HpcCache#access_rule}
        '''
        value = HpcCacheDefaultAccessPolicy(access_rule=access_rule)

        return typing.cast(None, jsii.invoke(self, "putDefaultAccessPolicy", [value]))

    @jsii.member(jsii_name="putDirectoryActiveDirectory")
    def put_directory_active_directory(
        self,
        *,
        cache_netbios_name: builtins.str,
        dns_primary_ip: builtins.str,
        domain_name: builtins.str,
        domain_netbios_name: builtins.str,
        password: builtins.str,
        username: builtins.str,
        dns_secondary_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cache_netbios_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#cache_netbios_name HpcCache#cache_netbios_name}.
        :param dns_primary_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns_primary_ip HpcCache#dns_primary_ip}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#domain_name HpcCache#domain_name}.
        :param domain_netbios_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#domain_netbios_name HpcCache#domain_netbios_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password HpcCache#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#username HpcCache#username}.
        :param dns_secondary_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns_secondary_ip HpcCache#dns_secondary_ip}.
        '''
        value = HpcCacheDirectoryActiveDirectory(
            cache_netbios_name=cache_netbios_name,
            dns_primary_ip=dns_primary_ip,
            domain_name=domain_name,
            domain_netbios_name=domain_netbios_name,
            password=password,
            username=username,
            dns_secondary_ip=dns_secondary_ip,
        )

        return typing.cast(None, jsii.invoke(self, "putDirectoryActiveDirectory", [value]))

    @jsii.member(jsii_name="putDirectoryFlatFile")
    def put_directory_flat_file(
        self,
        *,
        group_file_uri: builtins.str,
        password_file_uri: builtins.str,
    ) -> None:
        '''
        :param group_file_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#group_file_uri HpcCache#group_file_uri}.
        :param password_file_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password_file_uri HpcCache#password_file_uri}.
        '''
        value = HpcCacheDirectoryFlatFile(
            group_file_uri=group_file_uri, password_file_uri=password_file_uri
        )

        return typing.cast(None, jsii.invoke(self, "putDirectoryFlatFile", [value]))

    @jsii.member(jsii_name="putDirectoryLdap")
    def put_directory_ldap(
        self,
        *,
        base_dn: builtins.str,
        server: builtins.str,
        bind: typing.Optional[typing.Union["HpcCacheDirectoryLdapBind", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_validation_uri: typing.Optional[builtins.str] = None,
        download_certificate_automatically: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param base_dn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#base_dn HpcCache#base_dn}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#server HpcCache#server}.
        :param bind: bind block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#bind HpcCache#bind}
        :param certificate_validation_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#certificate_validation_uri HpcCache#certificate_validation_uri}.
        :param download_certificate_automatically: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#download_certificate_automatically HpcCache#download_certificate_automatically}.
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#encrypted HpcCache#encrypted}.
        '''
        value = HpcCacheDirectoryLdap(
            base_dn=base_dn,
            server=server,
            bind=bind,
            certificate_validation_uri=certificate_validation_uri,
            download_certificate_automatically=download_certificate_automatically,
            encrypted=encrypted,
        )

        return typing.cast(None, jsii.invoke(self, "putDirectoryLdap", [value]))

    @jsii.member(jsii_name="putDns")
    def put_dns(
        self,
        *,
        servers: typing.Sequence[builtins.str],
        search_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#servers HpcCache#servers}.
        :param search_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#search_domain HpcCache#search_domain}.
        '''
        value = HpcCacheDns(servers=servers, search_domain=search_domain)

        return typing.cast(None, jsii.invoke(self, "putDns", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#type HpcCache#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#identity_ids HpcCache#identity_ids}.
        '''
        value = HpcCacheIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#create HpcCache#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#delete HpcCache#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#read HpcCache#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#update HpcCache#update}.
        '''
        value = HpcCacheTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutomaticallyRotateKeyToLatestEnabled")
    def reset_automatically_rotate_key_to_latest_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticallyRotateKeyToLatestEnabled", []))

    @jsii.member(jsii_name="resetDefaultAccessPolicy")
    def reset_default_access_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAccessPolicy", []))

    @jsii.member(jsii_name="resetDirectoryActiveDirectory")
    def reset_directory_active_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryActiveDirectory", []))

    @jsii.member(jsii_name="resetDirectoryFlatFile")
    def reset_directory_flat_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryFlatFile", []))

    @jsii.member(jsii_name="resetDirectoryLdap")
    def reset_directory_ldap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDirectoryLdap", []))

    @jsii.member(jsii_name="resetDns")
    def reset_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetKeyVaultKeyId")
    def reset_key_vault_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultKeyId", []))

    @jsii.member(jsii_name="resetMtu")
    def reset_mtu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtu", []))

    @jsii.member(jsii_name="resetNtpServer")
    def reset_ntp_server(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNtpServer", []))

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
    @jsii.member(jsii_name="defaultAccessPolicy")
    def default_access_policy(self) -> "HpcCacheDefaultAccessPolicyOutputReference":
        return typing.cast("HpcCacheDefaultAccessPolicyOutputReference", jsii.get(self, "defaultAccessPolicy"))

    @builtins.property
    @jsii.member(jsii_name="directoryActiveDirectory")
    def directory_active_directory(
        self,
    ) -> "HpcCacheDirectoryActiveDirectoryOutputReference":
        return typing.cast("HpcCacheDirectoryActiveDirectoryOutputReference", jsii.get(self, "directoryActiveDirectory"))

    @builtins.property
    @jsii.member(jsii_name="directoryFlatFile")
    def directory_flat_file(self) -> "HpcCacheDirectoryFlatFileOutputReference":
        return typing.cast("HpcCacheDirectoryFlatFileOutputReference", jsii.get(self, "directoryFlatFile"))

    @builtins.property
    @jsii.member(jsii_name="directoryLdap")
    def directory_ldap(self) -> "HpcCacheDirectoryLdapOutputReference":
        return typing.cast("HpcCacheDirectoryLdapOutputReference", jsii.get(self, "directoryLdap"))

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> "HpcCacheDnsOutputReference":
        return typing.cast("HpcCacheDnsOutputReference", jsii.get(self, "dns"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "HpcCacheIdentityOutputReference":
        return typing.cast("HpcCacheIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="mountAddresses")
    def mount_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mountAddresses"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "HpcCacheTimeoutsOutputReference":
        return typing.cast("HpcCacheTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="automaticallyRotateKeyToLatestEnabledInput")
    def automatically_rotate_key_to_latest_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automaticallyRotateKeyToLatestEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheSizeInGbInput")
    def cache_size_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cacheSizeInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAccessPolicyInput")
    def default_access_policy_input(
        self,
    ) -> typing.Optional["HpcCacheDefaultAccessPolicy"]:
        return typing.cast(typing.Optional["HpcCacheDefaultAccessPolicy"], jsii.get(self, "defaultAccessPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryActiveDirectoryInput")
    def directory_active_directory_input(
        self,
    ) -> typing.Optional["HpcCacheDirectoryActiveDirectory"]:
        return typing.cast(typing.Optional["HpcCacheDirectoryActiveDirectory"], jsii.get(self, "directoryActiveDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryFlatFileInput")
    def directory_flat_file_input(self) -> typing.Optional["HpcCacheDirectoryFlatFile"]:
        return typing.cast(typing.Optional["HpcCacheDirectoryFlatFile"], jsii.get(self, "directoryFlatFileInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryLdapInput")
    def directory_ldap_input(self) -> typing.Optional["HpcCacheDirectoryLdap"]:
        return typing.cast(typing.Optional["HpcCacheDirectoryLdap"], jsii.get(self, "directoryLdapInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsInput")
    def dns_input(self) -> typing.Optional["HpcCacheDns"]:
        return typing.cast(typing.Optional["HpcCacheDns"], jsii.get(self, "dnsInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["HpcCacheIdentity"]:
        return typing.cast(typing.Optional["HpcCacheIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyIdInput")
    def key_vault_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mtuInput")
    def mtu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mtuInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ntpServerInput")
    def ntp_server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ntpServerInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HpcCacheTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "HpcCacheTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticallyRotateKeyToLatestEnabled")
    def automatically_rotate_key_to_latest_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automaticallyRotateKeyToLatestEnabled"))

    @automatically_rotate_key_to_latest_enabled.setter
    def automatically_rotate_key_to_latest_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32a62cbe5fdec47263efcf730939daa2f28feed2f0fd8846dbf4e786a75eb4b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticallyRotateKeyToLatestEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cacheSizeInGb")
    def cache_size_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cacheSizeInGb"))

    @cache_size_in_gb.setter
    def cache_size_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e59b8a9abf4a4a29fcb762261654f5055b55d0f32b5c1feddce608171835ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheSizeInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32d9e9281db7d973972a4a418eef3fe2ea69a06b7d05ebd91ebe1f34f438d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyId")
    def key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultKeyId"))

    @key_vault_key_id.setter
    def key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ff9b7f0e6334450f729f8ed267f01f54176bbed2b71c6f3188241849b7b2af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfcdf37e3588b9d80a21119abfaf47722833d7a5b585ca5254e39ec4a31d8226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c936136721dae6e8203e0d28bd220605d2120d46d06aea3a8b5bf27b8e1321bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58186b451976af365dc7c8cb09f4f7523763570372793559a572bddc1a4da513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ntpServer")
    def ntp_server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ntpServer"))

    @ntp_server.setter
    def ntp_server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc82ede40e8d0c503b5f239feb0ddfbec6bdf9e4185ab48ed82d8bf855d58a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ntpServer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8965f81b987055341d2d15a9aeb1aa3c1c623768c7116cfa4b4da1cf0a7c288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc44ee738744fc2f2cced36d4c035816e49753b0fef1dbee1538359752a0931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125a5c800f161435bed85ae986ad249c1e823db7e9a04137ea756f116583d889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53914767e321c7b2be72744a247f9b26abaa80a9f4ece5f72f9e9aaf115c9dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cache_size_in_gb": "cacheSizeInGb",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "sku_name": "skuName",
        "subnet_id": "subnetId",
        "automatically_rotate_key_to_latest_enabled": "automaticallyRotateKeyToLatestEnabled",
        "default_access_policy": "defaultAccessPolicy",
        "directory_active_directory": "directoryActiveDirectory",
        "directory_flat_file": "directoryFlatFile",
        "directory_ldap": "directoryLdap",
        "dns": "dns",
        "id": "id",
        "identity": "identity",
        "key_vault_key_id": "keyVaultKeyId",
        "mtu": "mtu",
        "ntp_server": "ntpServer",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class HpcCacheConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cache_size_in_gb: jsii.Number,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku_name: builtins.str,
        subnet_id: builtins.str,
        automatically_rotate_key_to_latest_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_access_policy: typing.Optional[typing.Union["HpcCacheDefaultAccessPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        directory_active_directory: typing.Optional[typing.Union["HpcCacheDirectoryActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        directory_flat_file: typing.Optional[typing.Union["HpcCacheDirectoryFlatFile", typing.Dict[builtins.str, typing.Any]]] = None,
        directory_ldap: typing.Optional[typing.Union["HpcCacheDirectoryLdap", typing.Dict[builtins.str, typing.Any]]] = None,
        dns: typing.Optional[typing.Union["HpcCacheDns", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["HpcCacheIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        ntp_server: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["HpcCacheTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cache_size_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#cache_size_in_gb HpcCache#cache_size_in_gb}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#location HpcCache#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#name HpcCache#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#resource_group_name HpcCache#resource_group_name}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#sku_name HpcCache#sku_name}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#subnet_id HpcCache#subnet_id}.
        :param automatically_rotate_key_to_latest_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#automatically_rotate_key_to_latest_enabled HpcCache#automatically_rotate_key_to_latest_enabled}.
        :param default_access_policy: default_access_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#default_access_policy HpcCache#default_access_policy}
        :param directory_active_directory: directory_active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_active_directory HpcCache#directory_active_directory}
        :param directory_flat_file: directory_flat_file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_flat_file HpcCache#directory_flat_file}
        :param directory_ldap: directory_ldap block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_ldap HpcCache#directory_ldap}
        :param dns: dns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns HpcCache#dns}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#id HpcCache#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#identity HpcCache#identity}
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#key_vault_key_id HpcCache#key_vault_key_id}.
        :param mtu: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#mtu HpcCache#mtu}.
        :param ntp_server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#ntp_server HpcCache#ntp_server}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#tags HpcCache#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#timeouts HpcCache#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_access_policy, dict):
            default_access_policy = HpcCacheDefaultAccessPolicy(**default_access_policy)
        if isinstance(directory_active_directory, dict):
            directory_active_directory = HpcCacheDirectoryActiveDirectory(**directory_active_directory)
        if isinstance(directory_flat_file, dict):
            directory_flat_file = HpcCacheDirectoryFlatFile(**directory_flat_file)
        if isinstance(directory_ldap, dict):
            directory_ldap = HpcCacheDirectoryLdap(**directory_ldap)
        if isinstance(dns, dict):
            dns = HpcCacheDns(**dns)
        if isinstance(identity, dict):
            identity = HpcCacheIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = HpcCacheTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f6c860f445b81cee3d3f1d064cca9ae800d31f86d6e8b0a7cbc88dd83658adf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cache_size_in_gb", value=cache_size_in_gb, expected_type=type_hints["cache_size_in_gb"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument automatically_rotate_key_to_latest_enabled", value=automatically_rotate_key_to_latest_enabled, expected_type=type_hints["automatically_rotate_key_to_latest_enabled"])
            check_type(argname="argument default_access_policy", value=default_access_policy, expected_type=type_hints["default_access_policy"])
            check_type(argname="argument directory_active_directory", value=directory_active_directory, expected_type=type_hints["directory_active_directory"])
            check_type(argname="argument directory_flat_file", value=directory_flat_file, expected_type=type_hints["directory_flat_file"])
            check_type(argname="argument directory_ldap", value=directory_ldap, expected_type=type_hints["directory_ldap"])
            check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument key_vault_key_id", value=key_vault_key_id, expected_type=type_hints["key_vault_key_id"])
            check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
            check_type(argname="argument ntp_server", value=ntp_server, expected_type=type_hints["ntp_server"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_size_in_gb": cache_size_in_gb,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "sku_name": sku_name,
            "subnet_id": subnet_id,
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
        if automatically_rotate_key_to_latest_enabled is not None:
            self._values["automatically_rotate_key_to_latest_enabled"] = automatically_rotate_key_to_latest_enabled
        if default_access_policy is not None:
            self._values["default_access_policy"] = default_access_policy
        if directory_active_directory is not None:
            self._values["directory_active_directory"] = directory_active_directory
        if directory_flat_file is not None:
            self._values["directory_flat_file"] = directory_flat_file
        if directory_ldap is not None:
            self._values["directory_ldap"] = directory_ldap
        if dns is not None:
            self._values["dns"] = dns
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if key_vault_key_id is not None:
            self._values["key_vault_key_id"] = key_vault_key_id
        if mtu is not None:
            self._values["mtu"] = mtu
        if ntp_server is not None:
            self._values["ntp_server"] = ntp_server
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
    def cache_size_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#cache_size_in_gb HpcCache#cache_size_in_gb}.'''
        result = self._values.get("cache_size_in_gb")
        assert result is not None, "Required property 'cache_size_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#location HpcCache#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#name HpcCache#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#resource_group_name HpcCache#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#sku_name HpcCache#sku_name}.'''
        result = self._values.get("sku_name")
        assert result is not None, "Required property 'sku_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#subnet_id HpcCache#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automatically_rotate_key_to_latest_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#automatically_rotate_key_to_latest_enabled HpcCache#automatically_rotate_key_to_latest_enabled}.'''
        result = self._values.get("automatically_rotate_key_to_latest_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_access_policy(self) -> typing.Optional["HpcCacheDefaultAccessPolicy"]:
        '''default_access_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#default_access_policy HpcCache#default_access_policy}
        '''
        result = self._values.get("default_access_policy")
        return typing.cast(typing.Optional["HpcCacheDefaultAccessPolicy"], result)

    @builtins.property
    def directory_active_directory(
        self,
    ) -> typing.Optional["HpcCacheDirectoryActiveDirectory"]:
        '''directory_active_directory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_active_directory HpcCache#directory_active_directory}
        '''
        result = self._values.get("directory_active_directory")
        return typing.cast(typing.Optional["HpcCacheDirectoryActiveDirectory"], result)

    @builtins.property
    def directory_flat_file(self) -> typing.Optional["HpcCacheDirectoryFlatFile"]:
        '''directory_flat_file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_flat_file HpcCache#directory_flat_file}
        '''
        result = self._values.get("directory_flat_file")
        return typing.cast(typing.Optional["HpcCacheDirectoryFlatFile"], result)

    @builtins.property
    def directory_ldap(self) -> typing.Optional["HpcCacheDirectoryLdap"]:
        '''directory_ldap block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#directory_ldap HpcCache#directory_ldap}
        '''
        result = self._values.get("directory_ldap")
        return typing.cast(typing.Optional["HpcCacheDirectoryLdap"], result)

    @builtins.property
    def dns(self) -> typing.Optional["HpcCacheDns"]:
        '''dns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns HpcCache#dns}
        '''
        result = self._values.get("dns")
        return typing.cast(typing.Optional["HpcCacheDns"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#id HpcCache#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["HpcCacheIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#identity HpcCache#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["HpcCacheIdentity"], result)

    @builtins.property
    def key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#key_vault_key_id HpcCache#key_vault_key_id}.'''
        result = self._values.get("key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#mtu HpcCache#mtu}.'''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ntp_server(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#ntp_server HpcCache#ntp_server}.'''
        result = self._values.get("ntp_server")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#tags HpcCache#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["HpcCacheTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#timeouts HpcCache#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["HpcCacheTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDefaultAccessPolicy",
    jsii_struct_bases=[],
    name_mapping={"access_rule": "accessRule"},
)
class HpcCacheDefaultAccessPolicy:
    def __init__(
        self,
        *,
        access_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["HpcCacheDefaultAccessPolicyAccessRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param access_rule: access_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#access_rule HpcCache#access_rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1475ab4184aed3e9f8d1f74a49c5db6c02458e141f7a3d80ad269afee71a5af0)
            check_type(argname="argument access_rule", value=access_rule, expected_type=type_hints["access_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_rule": access_rule,
        }

    @builtins.property
    def access_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HpcCacheDefaultAccessPolicyAccessRule"]]:
        '''access_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#access_rule HpcCache#access_rule}
        '''
        result = self._values.get("access_rule")
        assert result is not None, "Required property 'access_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["HpcCacheDefaultAccessPolicyAccessRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheDefaultAccessPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDefaultAccessPolicyAccessRule",
    jsii_struct_bases=[],
    name_mapping={
        "access": "access",
        "scope": "scope",
        "anonymous_gid": "anonymousGid",
        "anonymous_uid": "anonymousUid",
        "filter": "filter",
        "root_squash_enabled": "rootSquashEnabled",
        "submount_access_enabled": "submountAccessEnabled",
        "suid_enabled": "suidEnabled",
    },
)
class HpcCacheDefaultAccessPolicyAccessRule:
    def __init__(
        self,
        *,
        access: builtins.str,
        scope: builtins.str,
        anonymous_gid: typing.Optional[jsii.Number] = None,
        anonymous_uid: typing.Optional[jsii.Number] = None,
        filter: typing.Optional[builtins.str] = None,
        root_squash_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        submount_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suid_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param access: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#access HpcCache#access}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#scope HpcCache#scope}.
        :param anonymous_gid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#anonymous_gid HpcCache#anonymous_gid}.
        :param anonymous_uid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#anonymous_uid HpcCache#anonymous_uid}.
        :param filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#filter HpcCache#filter}.
        :param root_squash_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#root_squash_enabled HpcCache#root_squash_enabled}.
        :param submount_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#submount_access_enabled HpcCache#submount_access_enabled}.
        :param suid_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#suid_enabled HpcCache#suid_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c7b2a57d4d86aa5a203e413f4efc7d1dd7b8292db140addd0a425979172480)
            check_type(argname="argument access", value=access, expected_type=type_hints["access"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument anonymous_gid", value=anonymous_gid, expected_type=type_hints["anonymous_gid"])
            check_type(argname="argument anonymous_uid", value=anonymous_uid, expected_type=type_hints["anonymous_uid"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument root_squash_enabled", value=root_squash_enabled, expected_type=type_hints["root_squash_enabled"])
            check_type(argname="argument submount_access_enabled", value=submount_access_enabled, expected_type=type_hints["submount_access_enabled"])
            check_type(argname="argument suid_enabled", value=suid_enabled, expected_type=type_hints["suid_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access": access,
            "scope": scope,
        }
        if anonymous_gid is not None:
            self._values["anonymous_gid"] = anonymous_gid
        if anonymous_uid is not None:
            self._values["anonymous_uid"] = anonymous_uid
        if filter is not None:
            self._values["filter"] = filter
        if root_squash_enabled is not None:
            self._values["root_squash_enabled"] = root_squash_enabled
        if submount_access_enabled is not None:
            self._values["submount_access_enabled"] = submount_access_enabled
        if suid_enabled is not None:
            self._values["suid_enabled"] = suid_enabled

    @builtins.property
    def access(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#access HpcCache#access}.'''
        result = self._values.get("access")
        assert result is not None, "Required property 'access' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#scope HpcCache#scope}.'''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def anonymous_gid(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#anonymous_gid HpcCache#anonymous_gid}.'''
        result = self._values.get("anonymous_gid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def anonymous_uid(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#anonymous_uid HpcCache#anonymous_uid}.'''
        result = self._values.get("anonymous_uid")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#filter HpcCache#filter}.'''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_squash_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#root_squash_enabled HpcCache#root_squash_enabled}.'''
        result = self._values.get("root_squash_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def submount_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#submount_access_enabled HpcCache#submount_access_enabled}.'''
        result = self._values.get("submount_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suid_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#suid_enabled HpcCache#suid_enabled}.'''
        result = self._values.get("suid_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheDefaultAccessPolicyAccessRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheDefaultAccessPolicyAccessRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDefaultAccessPolicyAccessRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7569a7fd21f11ffe0b420f075360a6e1c1c599289d2671760c6c9124740fdb49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "HpcCacheDefaultAccessPolicyAccessRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03aeb783cfb150c478b25c2deb503ee9ca0f9b7de0ccd1558a57e67c4cf8d99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("HpcCacheDefaultAccessPolicyAccessRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb74d3a9ec69f74972a121ba26711a82a47c18207dfcf120d4d12a55914e22f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__694e596436c39479aa8849fb4dc5e1001633f765fee38d262a54c712736de08f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0bd146f8b09ade1d82aead5ce5160eb5a5dc8255a7327982629f2abcac0567a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheDefaultAccessPolicyAccessRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheDefaultAccessPolicyAccessRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheDefaultAccessPolicyAccessRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c5b7f441d78554db5641817d7b811c96097780fffaad7da04f8de4897a07493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HpcCacheDefaultAccessPolicyAccessRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDefaultAccessPolicyAccessRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cbae9c111a6eac13f88dedb65a075bb7af493b9713bd9a52427cfeb376d46f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAnonymousGid")
    def reset_anonymous_gid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonymousGid", []))

    @jsii.member(jsii_name="resetAnonymousUid")
    def reset_anonymous_uid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonymousUid", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetRootSquashEnabled")
    def reset_root_squash_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootSquashEnabled", []))

    @jsii.member(jsii_name="resetSubmountAccessEnabled")
    def reset_submount_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubmountAccessEnabled", []))

    @jsii.member(jsii_name="resetSuidEnabled")
    def reset_suid_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuidEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="accessInput")
    def access_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessInput"))

    @builtins.property
    @jsii.member(jsii_name="anonymousGidInput")
    def anonymous_gid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "anonymousGidInput"))

    @builtins.property
    @jsii.member(jsii_name="anonymousUidInput")
    def anonymous_uid_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "anonymousUidInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="rootSquashEnabledInput")
    def root_squash_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rootSquashEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="submountAccessEnabledInput")
    def submount_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "submountAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="suidEnabledInput")
    def suid_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suidEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="access")
    def access(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "access"))

    @access.setter
    def access(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe3f9c60b3110b4d2df3fb7b9d765de7c2b1a2455078b08c1ae7153a14fe528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "access", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="anonymousGid")
    def anonymous_gid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "anonymousGid"))

    @anonymous_gid.setter
    def anonymous_gid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f6dd7fd586590b5bb21919777e71b2d5c5120a976f5d476fb05c0da35cd27f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anonymousGid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="anonymousUid")
    def anonymous_uid(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "anonymousUid"))

    @anonymous_uid.setter
    def anonymous_uid(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50471c4e80a7946b96ab3ddd9d9db69a1e043ef535d01af8709216c265efe1d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anonymousUid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "filter"))

    @filter.setter
    def filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0679db9ebf794f97e5a458eaf87015496302d3465d75d3a618f000584da318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootSquashEnabled")
    def root_squash_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rootSquashEnabled"))

    @root_squash_enabled.setter
    def root_squash_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19405f8858aad8b918b76f0dc925abfe06aab86b68d690fa788bb1a0bf03fa31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootSquashEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9fb8f41cad06dc13fcd2ceca8eb53c5b9caacac894302b0b8aa6ab8d19c665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="submountAccessEnabled")
    def submount_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "submountAccessEnabled"))

    @submount_access_enabled.setter
    def submount_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa1122b1bac59e059384baa4c3cc6a2dcf579b00b24e4806c39c885ce1e1b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "submountAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suidEnabled")
    def suid_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suidEnabled"))

    @suid_enabled.setter
    def suid_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d9b57af281ad4eab766526323a77bee2ad054b1593c3a6d7c50c35f5431d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suidEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheDefaultAccessPolicyAccessRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheDefaultAccessPolicyAccessRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheDefaultAccessPolicyAccessRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b171be4047f15c887fbcaae30b909fa87df3468e1e9123614370f251345442f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HpcCacheDefaultAccessPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDefaultAccessPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e60553ba87432332d4e4f11ee8bf81b33401198f821bf5b6a1aff05bc4984af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAccessRule")
    def put_access_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HpcCacheDefaultAccessPolicyAccessRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411416faf441433d92d4a9cf98c6fcbbce286dbde0a9438b1db4033602a0667f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAccessRule", [value]))

    @builtins.property
    @jsii.member(jsii_name="accessRule")
    def access_rule(self) -> HpcCacheDefaultAccessPolicyAccessRuleList:
        return typing.cast(HpcCacheDefaultAccessPolicyAccessRuleList, jsii.get(self, "accessRule"))

    @builtins.property
    @jsii.member(jsii_name="accessRuleInput")
    def access_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheDefaultAccessPolicyAccessRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheDefaultAccessPolicyAccessRule]]], jsii.get(self, "accessRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HpcCacheDefaultAccessPolicy]:
        return typing.cast(typing.Optional[HpcCacheDefaultAccessPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HpcCacheDefaultAccessPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e73e06d826a2b89b35aaa2c6d655ee66c5b4cac5e9345976e2942772896f640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDirectoryActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={
        "cache_netbios_name": "cacheNetbiosName",
        "dns_primary_ip": "dnsPrimaryIp",
        "domain_name": "domainName",
        "domain_netbios_name": "domainNetbiosName",
        "password": "password",
        "username": "username",
        "dns_secondary_ip": "dnsSecondaryIp",
    },
)
class HpcCacheDirectoryActiveDirectory:
    def __init__(
        self,
        *,
        cache_netbios_name: builtins.str,
        dns_primary_ip: builtins.str,
        domain_name: builtins.str,
        domain_netbios_name: builtins.str,
        password: builtins.str,
        username: builtins.str,
        dns_secondary_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cache_netbios_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#cache_netbios_name HpcCache#cache_netbios_name}.
        :param dns_primary_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns_primary_ip HpcCache#dns_primary_ip}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#domain_name HpcCache#domain_name}.
        :param domain_netbios_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#domain_netbios_name HpcCache#domain_netbios_name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password HpcCache#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#username HpcCache#username}.
        :param dns_secondary_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns_secondary_ip HpcCache#dns_secondary_ip}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2851c790af3ba00d89032bde29d9d2c024729e9cc9de8cad43594d453931dcb9)
            check_type(argname="argument cache_netbios_name", value=cache_netbios_name, expected_type=type_hints["cache_netbios_name"])
            check_type(argname="argument dns_primary_ip", value=dns_primary_ip, expected_type=type_hints["dns_primary_ip"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_netbios_name", value=domain_netbios_name, expected_type=type_hints["domain_netbios_name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument dns_secondary_ip", value=dns_secondary_ip, expected_type=type_hints["dns_secondary_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_netbios_name": cache_netbios_name,
            "dns_primary_ip": dns_primary_ip,
            "domain_name": domain_name,
            "domain_netbios_name": domain_netbios_name,
            "password": password,
            "username": username,
        }
        if dns_secondary_ip is not None:
            self._values["dns_secondary_ip"] = dns_secondary_ip

    @builtins.property
    def cache_netbios_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#cache_netbios_name HpcCache#cache_netbios_name}.'''
        result = self._values.get("cache_netbios_name")
        assert result is not None, "Required property 'cache_netbios_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dns_primary_ip(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns_primary_ip HpcCache#dns_primary_ip}.'''
        result = self._values.get("dns_primary_ip")
        assert result is not None, "Required property 'dns_primary_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#domain_name HpcCache#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_netbios_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#domain_netbios_name HpcCache#domain_netbios_name}.'''
        result = self._values.get("domain_netbios_name")
        assert result is not None, "Required property 'domain_netbios_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password HpcCache#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#username HpcCache#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dns_secondary_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dns_secondary_ip HpcCache#dns_secondary_ip}.'''
        result = self._values.get("dns_secondary_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheDirectoryActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheDirectoryActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDirectoryActiveDirectoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43170107b1f78eebb290ea9964eaec46440b6562da8d2010d5337aaeae1f9693)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDnsSecondaryIp")
    def reset_dns_secondary_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsSecondaryIp", []))

    @builtins.property
    @jsii.member(jsii_name="cacheNetbiosNameInput")
    def cache_netbios_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheNetbiosNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsPrimaryIpInput")
    def dns_primary_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsPrimaryIpInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsSecondaryIpInput")
    def dns_secondary_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsSecondaryIpInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNetbiosNameInput")
    def domain_netbios_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNetbiosNameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="cacheNetbiosName")
    def cache_netbios_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheNetbiosName"))

    @cache_netbios_name.setter
    def cache_netbios_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b64e5d045b70a461489df9b0e401ee11545030a98853de86ed65a33baada26d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cacheNetbiosName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsPrimaryIp")
    def dns_primary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsPrimaryIp"))

    @dns_primary_ip.setter
    def dns_primary_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5155bb2ce9eed233bd4896e1266ab04188abbf00eb917ce56ce857dd73514152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsPrimaryIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsSecondaryIp")
    def dns_secondary_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsSecondaryIp"))

    @dns_secondary_ip.setter
    def dns_secondary_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f2d6880a8b66cb411d6e9360395d9825cb9462f3146743a0d0d9c851667772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsSecondaryIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219ab91654849d078313d41b1a99cfd16b01973796530fc4ab41d29cc63781fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainNetbiosName")
    def domain_netbios_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainNetbiosName"))

    @domain_netbios_name.setter
    def domain_netbios_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e7cbdc76825e511b28afdde1e41647a24ccf1dcbf2b719a7306886f0a8512b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainNetbiosName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28b060891671a13976aa79a5101330b4c6e0c4c6313b6ff5a7b64cfc5f89d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036f4d796e6cfe5760f6812265ac0ee0228c6c82572c1b4886b65c7e3f59287c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HpcCacheDirectoryActiveDirectory]:
        return typing.cast(typing.Optional[HpcCacheDirectoryActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[HpcCacheDirectoryActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f82f8e4094d8094d0efc6ed284b72ace3c8873fa3d33e196dd7b5a205423929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDirectoryFlatFile",
    jsii_struct_bases=[],
    name_mapping={
        "group_file_uri": "groupFileUri",
        "password_file_uri": "passwordFileUri",
    },
)
class HpcCacheDirectoryFlatFile:
    def __init__(
        self,
        *,
        group_file_uri: builtins.str,
        password_file_uri: builtins.str,
    ) -> None:
        '''
        :param group_file_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#group_file_uri HpcCache#group_file_uri}.
        :param password_file_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password_file_uri HpcCache#password_file_uri}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79a24a879d5ee0ad6a62150488abf794c7d9371e0f99c98ef42aa86cc20ef89)
            check_type(argname="argument group_file_uri", value=group_file_uri, expected_type=type_hints["group_file_uri"])
            check_type(argname="argument password_file_uri", value=password_file_uri, expected_type=type_hints["password_file_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_file_uri": group_file_uri,
            "password_file_uri": password_file_uri,
        }

    @builtins.property
    def group_file_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#group_file_uri HpcCache#group_file_uri}.'''
        result = self._values.get("group_file_uri")
        assert result is not None, "Required property 'group_file_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password_file_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password_file_uri HpcCache#password_file_uri}.'''
        result = self._values.get("password_file_uri")
        assert result is not None, "Required property 'password_file_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheDirectoryFlatFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheDirectoryFlatFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDirectoryFlatFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8ed05d249be876e99a7505a3e8623105f92e277629c5972f7855eb185adcaf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="groupFileUriInput")
    def group_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordFileUriInput")
    def password_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="groupFileUri")
    def group_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupFileUri"))

    @group_file_uri.setter
    def group_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4cd042b2f60c8c071ab5d367dd5eccc7283ffa750cf237830cd7bbe58ab6210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="passwordFileUri")
    def password_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passwordFileUri"))

    @password_file_uri.setter
    def password_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaadba78eb220aae71650266be2aac23e07cb9e005e3c00aaf7e0a0fefa44a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passwordFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HpcCacheDirectoryFlatFile]:
        return typing.cast(typing.Optional[HpcCacheDirectoryFlatFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[HpcCacheDirectoryFlatFile]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bcfe49bb82f74af9e48e19c28d98c2fb30fdd8030385681a2efa338546a7f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDirectoryLdap",
    jsii_struct_bases=[],
    name_mapping={
        "base_dn": "baseDn",
        "server": "server",
        "bind": "bind",
        "certificate_validation_uri": "certificateValidationUri",
        "download_certificate_automatically": "downloadCertificateAutomatically",
        "encrypted": "encrypted",
    },
)
class HpcCacheDirectoryLdap:
    def __init__(
        self,
        *,
        base_dn: builtins.str,
        server: builtins.str,
        bind: typing.Optional[typing.Union["HpcCacheDirectoryLdapBind", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate_validation_uri: typing.Optional[builtins.str] = None,
        download_certificate_automatically: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param base_dn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#base_dn HpcCache#base_dn}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#server HpcCache#server}.
        :param bind: bind block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#bind HpcCache#bind}
        :param certificate_validation_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#certificate_validation_uri HpcCache#certificate_validation_uri}.
        :param download_certificate_automatically: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#download_certificate_automatically HpcCache#download_certificate_automatically}.
        :param encrypted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#encrypted HpcCache#encrypted}.
        '''
        if isinstance(bind, dict):
            bind = HpcCacheDirectoryLdapBind(**bind)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdcaf670e460044ee49f87179b58e16dad2ae0ab8f4e650eff70dc3192e0df62)
            check_type(argname="argument base_dn", value=base_dn, expected_type=type_hints["base_dn"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument bind", value=bind, expected_type=type_hints["bind"])
            check_type(argname="argument certificate_validation_uri", value=certificate_validation_uri, expected_type=type_hints["certificate_validation_uri"])
            check_type(argname="argument download_certificate_automatically", value=download_certificate_automatically, expected_type=type_hints["download_certificate_automatically"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_dn": base_dn,
            "server": server,
        }
        if bind is not None:
            self._values["bind"] = bind
        if certificate_validation_uri is not None:
            self._values["certificate_validation_uri"] = certificate_validation_uri
        if download_certificate_automatically is not None:
            self._values["download_certificate_automatically"] = download_certificate_automatically
        if encrypted is not None:
            self._values["encrypted"] = encrypted

    @builtins.property
    def base_dn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#base_dn HpcCache#base_dn}.'''
        result = self._values.get("base_dn")
        assert result is not None, "Required property 'base_dn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#server HpcCache#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bind(self) -> typing.Optional["HpcCacheDirectoryLdapBind"]:
        '''bind block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#bind HpcCache#bind}
        '''
        result = self._values.get("bind")
        return typing.cast(typing.Optional["HpcCacheDirectoryLdapBind"], result)

    @builtins.property
    def certificate_validation_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#certificate_validation_uri HpcCache#certificate_validation_uri}.'''
        result = self._values.get("certificate_validation_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def download_certificate_automatically(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#download_certificate_automatically HpcCache#download_certificate_automatically}.'''
        result = self._values.get("download_certificate_automatically")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def encrypted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#encrypted HpcCache#encrypted}.'''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheDirectoryLdap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDirectoryLdapBind",
    jsii_struct_bases=[],
    name_mapping={"dn": "dn", "password": "password"},
)
class HpcCacheDirectoryLdapBind:
    def __init__(self, *, dn: builtins.str, password: builtins.str) -> None:
        '''
        :param dn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dn HpcCache#dn}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password HpcCache#password}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aca9e9e9f3e7d968d8d434972a254951ec03c038559e1c5fcf919adcc0a1a1f)
            check_type(argname="argument dn", value=dn, expected_type=type_hints["dn"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dn": dn,
            "password": password,
        }

    @builtins.property
    def dn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dn HpcCache#dn}.'''
        result = self._values.get("dn")
        assert result is not None, "Required property 'dn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password HpcCache#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheDirectoryLdapBind(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheDirectoryLdapBindOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDirectoryLdapBindOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57e867bef3ab3a3fae947dedf485eb9c08dde6c8b8c76ef77fffd10917e53987)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="dnInput")
    def dn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="dn")
    def dn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dn"))

    @dn.setter
    def dn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b301f81b3e0f8ed2cab74ca5da366c806c25889186b30a30ce3711676da924d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636fd49841e1182bf8f4e793ff36b1f76107bd715beb901cd268098023175347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HpcCacheDirectoryLdapBind]:
        return typing.cast(typing.Optional[HpcCacheDirectoryLdapBind], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[HpcCacheDirectoryLdapBind]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3bdad424405a92e973623b4b695df96adda1bc175fc0fe3e0a02c2246ad073a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class HpcCacheDirectoryLdapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDirectoryLdapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a37639d09335e5025929ad50b2c2c656a45532804dc590e3e67b49a0dc64eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBind")
    def put_bind(self, *, dn: builtins.str, password: builtins.str) -> None:
        '''
        :param dn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#dn HpcCache#dn}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#password HpcCache#password}.
        '''
        value = HpcCacheDirectoryLdapBind(dn=dn, password=password)

        return typing.cast(None, jsii.invoke(self, "putBind", [value]))

    @jsii.member(jsii_name="resetBind")
    def reset_bind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBind", []))

    @jsii.member(jsii_name="resetCertificateValidationUri")
    def reset_certificate_validation_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificateValidationUri", []))

    @jsii.member(jsii_name="resetDownloadCertificateAutomatically")
    def reset_download_certificate_automatically(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDownloadCertificateAutomatically", []))

    @jsii.member(jsii_name="resetEncrypted")
    def reset_encrypted(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncrypted", []))

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> HpcCacheDirectoryLdapBindOutputReference:
        return typing.cast(HpcCacheDirectoryLdapBindOutputReference, jsii.get(self, "bind"))

    @builtins.property
    @jsii.member(jsii_name="baseDnInput")
    def base_dn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseDnInput"))

    @builtins.property
    @jsii.member(jsii_name="bindInput")
    def bind_input(self) -> typing.Optional[HpcCacheDirectoryLdapBind]:
        return typing.cast(typing.Optional[HpcCacheDirectoryLdapBind], jsii.get(self, "bindInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateValidationUriInput")
    def certificate_validation_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateValidationUriInput"))

    @builtins.property
    @jsii.member(jsii_name="downloadCertificateAutomaticallyInput")
    def download_certificate_automatically_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "downloadCertificateAutomaticallyInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedInput")
    def encrypted_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptedInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="baseDn")
    def base_dn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseDn"))

    @base_dn.setter
    def base_dn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d1102b07ffedf1ca0c24d03d2018ba36059ce7385ff91224836f2492e7e76c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseDn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="certificateValidationUri")
    def certificate_validation_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificateValidationUri"))

    @certificate_validation_uri.setter
    def certificate_validation_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f8f702d5ebe29adb27f091aa74ea774a8cc49f3d67ca612a559b0b2ae02be2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateValidationUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="downloadCertificateAutomatically")
    def download_certificate_automatically(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "downloadCertificateAutomatically"))

    @download_certificate_automatically.setter
    def download_certificate_automatically(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a055c07346c52479f88dc97783588889edb07144949c9dc9df4bfafe1ccd49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downloadCertificateAutomatically", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encrypted")
    def encrypted(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encrypted"))

    @encrypted.setter
    def encrypted(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a5d4933e6e588a564366b296f03b7ee0a86e9ff98047789fe11ffb17ea6af0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encrypted", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5022e4a10a0495919de172abbe2daccaadaf0e357d6ebcd9b5d0bf1128ac967)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HpcCacheDirectoryLdap]:
        return typing.cast(typing.Optional[HpcCacheDirectoryLdap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[HpcCacheDirectoryLdap]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19da0c81fdbbdd230ae620116251eff148ea7f32a62a8ded4ec466c75d10db3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDns",
    jsii_struct_bases=[],
    name_mapping={"servers": "servers", "search_domain": "searchDomain"},
)
class HpcCacheDns:
    def __init__(
        self,
        *,
        servers: typing.Sequence[builtins.str],
        search_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#servers HpcCache#servers}.
        :param search_domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#search_domain HpcCache#search_domain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1707cdac33fee3f94e1f776deb60d502f0b2fd9702efba365b075ec0665c94a)
            check_type(argname="argument servers", value=servers, expected_type=type_hints["servers"])
            check_type(argname="argument search_domain", value=search_domain, expected_type=type_hints["search_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "servers": servers,
        }
        if search_domain is not None:
            self._values["search_domain"] = search_domain

    @builtins.property
    def servers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#servers HpcCache#servers}.'''
        result = self._values.get("servers")
        assert result is not None, "Required property 'servers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def search_domain(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#search_domain HpcCache#search_domain}.'''
        result = self._values.get("search_domain")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheDns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheDnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheDnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab6437d775104e904d613f32c984108ccdaf8ccdf60cb562a4bd2592efa7e172)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSearchDomain")
    def reset_search_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchDomain", []))

    @builtins.property
    @jsii.member(jsii_name="searchDomainInput")
    def search_domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="serversInput")
    def servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serversInput"))

    @builtins.property
    @jsii.member(jsii_name="searchDomain")
    def search_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchDomain"))

    @search_domain.setter
    def search_domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0c3ecd15e9c426cb7f4cd19e5a0c6fb0bbcfa0f644c734adec392291bb70c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchDomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servers")
    def servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "servers"))

    @servers.setter
    def servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe1656add94792453a925f8918fd190fed1b04f5bbd06964546e9815953eef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HpcCacheDns]:
        return typing.cast(typing.Optional[HpcCacheDns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[HpcCacheDns]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ef76361f589e2dc6fd34ad45f95d51ce8618d19ea037c12792be1d551697e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class HpcCacheIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#type HpcCache#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#identity_ids HpcCache#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b384fbe602eb24af70470d7630a716b458acdd298372a70a9357b852a5a3b58)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#type HpcCache#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#identity_ids HpcCache#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__228534dd6e614aae4df37143e5800c4806ae3892c36180b93dd317ff54bfc35e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9785e5180ca23036309ef7d933e3801344130947a0170b708c35d648f22be23e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68781ce49acb5405a126770e8f6bf3a7680b0dbd640469bc057eeb5671981671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[HpcCacheIdentity]:
        return typing.cast(typing.Optional[HpcCacheIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[HpcCacheIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2492244fb780c9059cd80604c8f30c0f49581ad9c6a150cf1e1659ac4fd0ef80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class HpcCacheTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#create HpcCache#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#delete HpcCache#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#read HpcCache#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#update HpcCache#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e5ebc5ba89e2a03886b6bedf024e0bde56c645e26ce7100b628a956dca528a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#create HpcCache#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#delete HpcCache#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#read HpcCache#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/hpc_cache#update HpcCache#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HpcCacheTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HpcCacheTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.hpcCache.HpcCacheTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c14470559fb8cfd51f1989e7a3a296c6c2c2b8a54fad9250609538a9a0150a81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67ea7964c631e111067b9730e6b86ae97e28c6cffc6e00f5102a8c4f106b78e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c54244397127609ca5d3d0c6024d1455deab1e2718d19018e8c9cb7ff044ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e791014476eb00681f6279367b955563e9fb697ce831321ba997aee7726223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ba97f2eb938b489ce440fe6509ad6df19c5930502bd4989c45ecb3b73a8173)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6449ba5afa928c88d312c6d035f15f3a92c95edb2b2ab48b159c836baaa5da81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "HpcCache",
    "HpcCacheConfig",
    "HpcCacheDefaultAccessPolicy",
    "HpcCacheDefaultAccessPolicyAccessRule",
    "HpcCacheDefaultAccessPolicyAccessRuleList",
    "HpcCacheDefaultAccessPolicyAccessRuleOutputReference",
    "HpcCacheDefaultAccessPolicyOutputReference",
    "HpcCacheDirectoryActiveDirectory",
    "HpcCacheDirectoryActiveDirectoryOutputReference",
    "HpcCacheDirectoryFlatFile",
    "HpcCacheDirectoryFlatFileOutputReference",
    "HpcCacheDirectoryLdap",
    "HpcCacheDirectoryLdapBind",
    "HpcCacheDirectoryLdapBindOutputReference",
    "HpcCacheDirectoryLdapOutputReference",
    "HpcCacheDns",
    "HpcCacheDnsOutputReference",
    "HpcCacheIdentity",
    "HpcCacheIdentityOutputReference",
    "HpcCacheTimeouts",
    "HpcCacheTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c8001c815869451fe98f943f28e3505f27ae65151dd023bd03c49167ffa724bb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cache_size_in_gb: jsii.Number,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku_name: builtins.str,
    subnet_id: builtins.str,
    automatically_rotate_key_to_latest_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_access_policy: typing.Optional[typing.Union[HpcCacheDefaultAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    directory_active_directory: typing.Optional[typing.Union[HpcCacheDirectoryActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    directory_flat_file: typing.Optional[typing.Union[HpcCacheDirectoryFlatFile, typing.Dict[builtins.str, typing.Any]]] = None,
    directory_ldap: typing.Optional[typing.Union[HpcCacheDirectoryLdap, typing.Dict[builtins.str, typing.Any]]] = None,
    dns: typing.Optional[typing.Union[HpcCacheDns, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[HpcCacheIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    ntp_server: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HpcCacheTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9e70b764de6274b17c6fb457cdf0c545abaa8d3132142ff36838fffc636e538c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a62cbe5fdec47263efcf730939daa2f28feed2f0fd8846dbf4e786a75eb4b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e59b8a9abf4a4a29fcb762261654f5055b55d0f32b5c1feddce608171835ee(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32d9e9281db7d973972a4a418eef3fe2ea69a06b7d05ebd91ebe1f34f438d3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ff9b7f0e6334450f729f8ed267f01f54176bbed2b71c6f3188241849b7b2af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfcdf37e3588b9d80a21119abfaf47722833d7a5b585ca5254e39ec4a31d8226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c936136721dae6e8203e0d28bd220605d2120d46d06aea3a8b5bf27b8e1321bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58186b451976af365dc7c8cb09f4f7523763570372793559a572bddc1a4da513(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc82ede40e8d0c503b5f239feb0ddfbec6bdf9e4185ab48ed82d8bf855d58a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8965f81b987055341d2d15a9aeb1aa3c1c623768c7116cfa4b4da1cf0a7c288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc44ee738744fc2f2cced36d4c035816e49753b0fef1dbee1538359752a0931(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125a5c800f161435bed85ae986ad249c1e823db7e9a04137ea756f116583d889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53914767e321c7b2be72744a247f9b26abaa80a9f4ece5f72f9e9aaf115c9dc2(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6c860f445b81cee3d3f1d064cca9ae800d31f86d6e8b0a7cbc88dd83658adf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cache_size_in_gb: jsii.Number,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku_name: builtins.str,
    subnet_id: builtins.str,
    automatically_rotate_key_to_latest_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_access_policy: typing.Optional[typing.Union[HpcCacheDefaultAccessPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    directory_active_directory: typing.Optional[typing.Union[HpcCacheDirectoryActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    directory_flat_file: typing.Optional[typing.Union[HpcCacheDirectoryFlatFile, typing.Dict[builtins.str, typing.Any]]] = None,
    directory_ldap: typing.Optional[typing.Union[HpcCacheDirectoryLdap, typing.Dict[builtins.str, typing.Any]]] = None,
    dns: typing.Optional[typing.Union[HpcCacheDns, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[HpcCacheIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    ntp_server: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[HpcCacheTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1475ab4184aed3e9f8d1f74a49c5db6c02458e141f7a3d80ad269afee71a5af0(
    *,
    access_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HpcCacheDefaultAccessPolicyAccessRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c7b2a57d4d86aa5a203e413f4efc7d1dd7b8292db140addd0a425979172480(
    *,
    access: builtins.str,
    scope: builtins.str,
    anonymous_gid: typing.Optional[jsii.Number] = None,
    anonymous_uid: typing.Optional[jsii.Number] = None,
    filter: typing.Optional[builtins.str] = None,
    root_squash_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    submount_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suid_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7569a7fd21f11ffe0b420f075360a6e1c1c599289d2671760c6c9124740fdb49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03aeb783cfb150c478b25c2deb503ee9ca0f9b7de0ccd1558a57e67c4cf8d99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb74d3a9ec69f74972a121ba26711a82a47c18207dfcf120d4d12a55914e22f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694e596436c39479aa8849fb4dc5e1001633f765fee38d262a54c712736de08f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bd146f8b09ade1d82aead5ce5160eb5a5dc8255a7327982629f2abcac0567a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c5b7f441d78554db5641817d7b811c96097780fffaad7da04f8de4897a07493(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[HpcCacheDefaultAccessPolicyAccessRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbae9c111a6eac13f88dedb65a075bb7af493b9713bd9a52427cfeb376d46f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe3f9c60b3110b4d2df3fb7b9d765de7c2b1a2455078b08c1ae7153a14fe528(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f6dd7fd586590b5bb21919777e71b2d5c5120a976f5d476fb05c0da35cd27f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50471c4e80a7946b96ab3ddd9d9db69a1e043ef535d01af8709216c265efe1d5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0679db9ebf794f97e5a458eaf87015496302d3465d75d3a618f000584da318(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19405f8858aad8b918b76f0dc925abfe06aab86b68d690fa788bb1a0bf03fa31(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9fb8f41cad06dc13fcd2ceca8eb53c5b9caacac894302b0b8aa6ab8d19c665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa1122b1bac59e059384baa4c3cc6a2dcf579b00b24e4806c39c885ce1e1b5b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d9b57af281ad4eab766526323a77bee2ad054b1593c3a6d7c50c35f5431d56(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b171be4047f15c887fbcaae30b909fa87df3468e1e9123614370f251345442f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheDefaultAccessPolicyAccessRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e60553ba87432332d4e4f11ee8bf81b33401198f821bf5b6a1aff05bc4984af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411416faf441433d92d4a9cf98c6fcbbce286dbde0a9438b1db4033602a0667f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[HpcCacheDefaultAccessPolicyAccessRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e73e06d826a2b89b35aaa2c6d655ee66c5b4cac5e9345976e2942772896f640(
    value: typing.Optional[HpcCacheDefaultAccessPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2851c790af3ba00d89032bde29d9d2c024729e9cc9de8cad43594d453931dcb9(
    *,
    cache_netbios_name: builtins.str,
    dns_primary_ip: builtins.str,
    domain_name: builtins.str,
    domain_netbios_name: builtins.str,
    password: builtins.str,
    username: builtins.str,
    dns_secondary_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43170107b1f78eebb290ea9964eaec46440b6562da8d2010d5337aaeae1f9693(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b64e5d045b70a461489df9b0e401ee11545030a98853de86ed65a33baada26d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5155bb2ce9eed233bd4896e1266ab04188abbf00eb917ce56ce857dd73514152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f2d6880a8b66cb411d6e9360395d9825cb9462f3146743a0d0d9c851667772(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219ab91654849d078313d41b1a99cfd16b01973796530fc4ab41d29cc63781fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e7cbdc76825e511b28afdde1e41647a24ccf1dcbf2b719a7306886f0a8512b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28b060891671a13976aa79a5101330b4c6e0c4c6313b6ff5a7b64cfc5f89d52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036f4d796e6cfe5760f6812265ac0ee0228c6c82572c1b4886b65c7e3f59287c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f82f8e4094d8094d0efc6ed284b72ace3c8873fa3d33e196dd7b5a205423929(
    value: typing.Optional[HpcCacheDirectoryActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79a24a879d5ee0ad6a62150488abf794c7d9371e0f99c98ef42aa86cc20ef89(
    *,
    group_file_uri: builtins.str,
    password_file_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ed05d249be876e99a7505a3e8623105f92e277629c5972f7855eb185adcaf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4cd042b2f60c8c071ab5d367dd5eccc7283ffa750cf237830cd7bbe58ab6210(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaadba78eb220aae71650266be2aac23e07cb9e005e3c00aaf7e0a0fefa44a52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcfe49bb82f74af9e48e19c28d98c2fb30fdd8030385681a2efa338546a7f60(
    value: typing.Optional[HpcCacheDirectoryFlatFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdcaf670e460044ee49f87179b58e16dad2ae0ab8f4e650eff70dc3192e0df62(
    *,
    base_dn: builtins.str,
    server: builtins.str,
    bind: typing.Optional[typing.Union[HpcCacheDirectoryLdapBind, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate_validation_uri: typing.Optional[builtins.str] = None,
    download_certificate_automatically: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    encrypted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aca9e9e9f3e7d968d8d434972a254951ec03c038559e1c5fcf919adcc0a1a1f(
    *,
    dn: builtins.str,
    password: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e867bef3ab3a3fae947dedf485eb9c08dde6c8b8c76ef77fffd10917e53987(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b301f81b3e0f8ed2cab74ca5da366c806c25889186b30a30ce3711676da924d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636fd49841e1182bf8f4e793ff36b1f76107bd715beb901cd268098023175347(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3bdad424405a92e973623b4b695df96adda1bc175fc0fe3e0a02c2246ad073a(
    value: typing.Optional[HpcCacheDirectoryLdapBind],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a37639d09335e5025929ad50b2c2c656a45532804dc590e3e67b49a0dc64eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d1102b07ffedf1ca0c24d03d2018ba36059ce7385ff91224836f2492e7e76c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f8f702d5ebe29adb27f091aa74ea774a8cc49f3d67ca612a559b0b2ae02be2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a055c07346c52479f88dc97783588889edb07144949c9dc9df4bfafe1ccd49(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a5d4933e6e588a564366b296f03b7ee0a86e9ff98047789fe11ffb17ea6af0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5022e4a10a0495919de172abbe2daccaadaf0e357d6ebcd9b5d0bf1128ac967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19da0c81fdbbdd230ae620116251eff148ea7f32a62a8ded4ec466c75d10db3a(
    value: typing.Optional[HpcCacheDirectoryLdap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1707cdac33fee3f94e1f776deb60d502f0b2fd9702efba365b075ec0665c94a(
    *,
    servers: typing.Sequence[builtins.str],
    search_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6437d775104e904d613f32c984108ccdaf8ccdf60cb562a4bd2592efa7e172(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0c3ecd15e9c426cb7f4cd19e5a0c6fb0bbcfa0f644c734adec392291bb70c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe1656add94792453a925f8918fd190fed1b04f5bbd06964546e9815953eef8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ef76361f589e2dc6fd34ad45f95d51ce8618d19ea037c12792be1d551697e6(
    value: typing.Optional[HpcCacheDns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b384fbe602eb24af70470d7630a716b458acdd298372a70a9357b852a5a3b58(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228534dd6e614aae4df37143e5800c4806ae3892c36180b93dd317ff54bfc35e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9785e5180ca23036309ef7d933e3801344130947a0170b708c35d648f22be23e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68781ce49acb5405a126770e8f6bf3a7680b0dbd640469bc057eeb5671981671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2492244fb780c9059cd80604c8f30c0f49581ad9c6a150cf1e1659ac4fd0ef80(
    value: typing.Optional[HpcCacheIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e5ebc5ba89e2a03886b6bedf024e0bde56c645e26ce7100b628a956dca528a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c14470559fb8cfd51f1989e7a3a296c6c2c2b8a54fad9250609538a9a0150a81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ea7964c631e111067b9730e6b86ae97e28c6cffc6e00f5102a8c4f106b78e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c54244397127609ca5d3d0c6024d1455deab1e2718d19018e8c9cb7ff044ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e791014476eb00681f6279367b955563e9fb697ce831321ba997aee7726223(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ba97f2eb938b489ce440fe6509ad6df19c5930502bd4989c45ecb3b73a8173(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6449ba5afa928c88d312c6d035f15f3a92c95edb2b2ab48b159c836baaa5da81(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, HpcCacheTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

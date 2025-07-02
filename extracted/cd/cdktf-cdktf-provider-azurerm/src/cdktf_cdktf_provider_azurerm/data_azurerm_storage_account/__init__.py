r'''
# `data_azurerm_storage_account`

Refer to the Terraform Registry for docs: [`data_azurerm_storage_account`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account).
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


class DataAzurermStorageAccount(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccount",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account azurerm_storage_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAzurermStorageAccountTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account azurerm_storage_account} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#name DataAzurermStorageAccount#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#resource_group_name DataAzurermStorageAccount#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#id DataAzurermStorageAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_tls_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#min_tls_version DataAzurermStorageAccount#min_tls_version}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#timeouts DataAzurermStorageAccount#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da53b6ba70107e453b4a696ce98372099e5359bf9d2ce7d7269cb71f7a1e4ad5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAzurermStorageAccountConfig(
            name=name,
            resource_group_name=resource_group_name,
            id=id,
            min_tls_version=min_tls_version,
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
        '''Generates CDKTF code for importing a DataAzurermStorageAccount resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataAzurermStorageAccount to import.
        :param import_from_id: The id of the existing DataAzurermStorageAccount that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataAzurermStorageAccount to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19bab86dc769f9b5293bd836e6dd85f0063d303f6ffca2d1e281ed56126acab3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#read DataAzurermStorageAccount#read}.
        '''
        value = DataAzurermStorageAccountTimeouts(read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMinTlsVersion")
    def reset_min_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTlsVersion", []))

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
    @jsii.member(jsii_name="accessTier")
    def access_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessTier"))

    @builtins.property
    @jsii.member(jsii_name="accountKind")
    def account_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountKind"))

    @builtins.property
    @jsii.member(jsii_name="accountReplicationType")
    def account_replication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountReplicationType"))

    @builtins.property
    @jsii.member(jsii_name="accountTier")
    def account_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountTier"))

    @builtins.property
    @jsii.member(jsii_name="allowNestedItemsToBePublic")
    def allow_nested_items_to_be_public(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowNestedItemsToBePublic"))

    @builtins.property
    @jsii.member(jsii_name="azureFilesAuthentication")
    def azure_files_authentication(
        self,
    ) -> "DataAzurermStorageAccountAzureFilesAuthenticationList":
        return typing.cast("DataAzurermStorageAccountAzureFilesAuthenticationList", jsii.get(self, "azureFilesAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> "DataAzurermStorageAccountCustomDomainList":
        return typing.cast("DataAzurermStorageAccountCustomDomainList", jsii.get(self, "customDomain"))

    @builtins.property
    @jsii.member(jsii_name="dnsEndpointType")
    def dns_endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsEndpointType"))

    @builtins.property
    @jsii.member(jsii_name="httpsTrafficOnlyEnabled")
    def https_traffic_only_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "httpsTrafficOnlyEnabled"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "DataAzurermStorageAccountIdentityList":
        return typing.cast("DataAzurermStorageAccountIdentityList", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureEncryptionEnabled")
    def infrastructure_encryption_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "infrastructureEncryptionEnabled"))

    @builtins.property
    @jsii.member(jsii_name="isHnsEnabled")
    def is_hns_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isHnsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="nfsv3Enabled")
    def nfsv3_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "nfsv3Enabled"))

    @builtins.property
    @jsii.member(jsii_name="primaryAccessKey")
    def primary_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="primaryBlobConnectionString")
    def primary_blob_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBlobConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="primaryBlobEndpoint")
    def primary_blob_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBlobEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryBlobHost")
    def primary_blob_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBlobHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryBlobInternetEndpoint")
    def primary_blob_internet_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBlobInternetEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryBlobInternetHost")
    def primary_blob_internet_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBlobInternetHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryBlobMicrosoftEndpoint")
    def primary_blob_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBlobMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryBlobMicrosoftHost")
    def primary_blob_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryBlobMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryConnectionString")
    def primary_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="primaryDfsEndpoint")
    def primary_dfs_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryDfsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryDfsHost")
    def primary_dfs_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryDfsHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryDfsInternetEndpoint")
    def primary_dfs_internet_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryDfsInternetEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryDfsInternetHost")
    def primary_dfs_internet_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryDfsInternetHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryDfsMicrosoftEndpoint")
    def primary_dfs_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryDfsMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryDfsMicrosoftHost")
    def primary_dfs_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryDfsMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryFileEndpoint")
    def primary_file_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryFileEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryFileHost")
    def primary_file_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryFileHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryFileInternetEndpoint")
    def primary_file_internet_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryFileInternetEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryFileInternetHost")
    def primary_file_internet_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryFileInternetHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryFileMicrosoftEndpoint")
    def primary_file_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryFileMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryFileMicrosoftHost")
    def primary_file_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryFileMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryLocation")
    def primary_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryLocation"))

    @builtins.property
    @jsii.member(jsii_name="primaryQueueEndpoint")
    def primary_queue_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryQueueEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryQueueHost")
    def primary_queue_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryQueueHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryQueueMicrosoftEndpoint")
    def primary_queue_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryQueueMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryQueueMicrosoftHost")
    def primary_queue_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryQueueMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryTableEndpoint")
    def primary_table_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryTableEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryTableHost")
    def primary_table_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryTableHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryTableMicrosoftEndpoint")
    def primary_table_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryTableMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryTableMicrosoftHost")
    def primary_table_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryTableMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryWebEndpoint")
    def primary_web_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryWebEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryWebHost")
    def primary_web_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryWebHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryWebInternetEndpoint")
    def primary_web_internet_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryWebInternetEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryWebInternetHost")
    def primary_web_internet_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryWebInternetHost"))

    @builtins.property
    @jsii.member(jsii_name="primaryWebMicrosoftEndpoint")
    def primary_web_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryWebMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="primaryWebMicrosoftHost")
    def primary_web_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryWebMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="queueEncryptionKeyType")
    def queue_encryption_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueEncryptionKeyType"))

    @builtins.property
    @jsii.member(jsii_name="secondaryAccessKey")
    def secondary_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBlobConnectionString")
    def secondary_blob_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBlobConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBlobEndpoint")
    def secondary_blob_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBlobEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBlobHost")
    def secondary_blob_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBlobHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBlobInternetEndpoint")
    def secondary_blob_internet_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBlobInternetEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBlobInternetHost")
    def secondary_blob_internet_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBlobInternetHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBlobMicrosoftEndpoint")
    def secondary_blob_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBlobMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryBlobMicrosoftHost")
    def secondary_blob_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryBlobMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryConnectionString")
    def secondary_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="secondaryDfsEndpoint")
    def secondary_dfs_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryDfsEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryDfsHost")
    def secondary_dfs_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryDfsHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryDfsInternetEndpoint")
    def secondary_dfs_internet_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryDfsInternetEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryDfsInternetHost")
    def secondary_dfs_internet_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryDfsInternetHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryDfsMicrosoftEndpoint")
    def secondary_dfs_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryDfsMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryDfsMicrosoftHost")
    def secondary_dfs_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryDfsMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryFileEndpoint")
    def secondary_file_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryFileEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryFileHost")
    def secondary_file_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryFileHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryFileInternetEndpoint")
    def secondary_file_internet_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryFileInternetEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryFileInternetHost")
    def secondary_file_internet_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryFileInternetHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryFileMicrosoftEndpoint")
    def secondary_file_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryFileMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryFileMicrosoftHost")
    def secondary_file_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryFileMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryLocation")
    def secondary_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryLocation"))

    @builtins.property
    @jsii.member(jsii_name="secondaryQueueEndpoint")
    def secondary_queue_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryQueueEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryQueueHost")
    def secondary_queue_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryQueueHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryQueueMicrosoftEndpoint")
    def secondary_queue_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryQueueMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryQueueMicrosoftHost")
    def secondary_queue_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryQueueMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryTableEndpoint")
    def secondary_table_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryTableEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryTableHost")
    def secondary_table_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryTableHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryTableMicrosoftEndpoint")
    def secondary_table_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryTableMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryTableMicrosoftHost")
    def secondary_table_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryTableMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWebEndpoint")
    def secondary_web_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryWebEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWebHost")
    def secondary_web_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryWebHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWebInternetEndpoint")
    def secondary_web_internet_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryWebInternetEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWebInternetHost")
    def secondary_web_internet_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryWebInternetHost"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWebMicrosoftEndpoint")
    def secondary_web_microsoft_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryWebMicrosoftEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="secondaryWebMicrosoftHost")
    def secondary_web_microsoft_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondaryWebMicrosoftHost"))

    @builtins.property
    @jsii.member(jsii_name="tableEncryptionKeyType")
    def table_encryption_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableEncryptionKeyType"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataAzurermStorageAccountTimeoutsOutputReference":
        return typing.cast("DataAzurermStorageAccountTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="minTlsVersionInput")
    def min_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataAzurermStorageAccountTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataAzurermStorageAccountTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3d5f6b90f4a9d08b2a9ca3b83648ed949000d992264be30d61cd83afdd6f34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTlsVersion")
    def min_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minTlsVersion"))

    @min_tls_version.setter
    def min_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__771692ea269f84251dad70f3ddd8b63ec7bdbc0278ff03c1d8c0ce6596798dac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTlsVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b41d6211716e5cd6d41bde6125df687bc4460ab550d5353f250f83a6061aacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a6591693ea740bff4316cd007bd3714c43e699f1bce55d6ecbf7bf57cfb25b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountAzureFilesAuthentication",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermStorageAccountAzureFilesAuthentication:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermStorageAccountAzureFilesAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa1c79dfba5d837772759a976900564e50de80fbaf416cf84c8a3ca2756dd12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d641edfdf15150c58a07be26c58d3df41e1c33cd10243d30490df81612b937)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908c1ddd059d7a11953b45939a70cc7bd111511a6ab60bb9e51777446f7d7a88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a724219ae1571c7ee6980ef5388e06be5037787804a8ac52d67398bb3568f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a93c94b1d804328cf35c5d8dcadd1f5a54e62916fb2cd1ec642d3808b826e3f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf7cc0967433f0f7ca51674bf3bf280fd3e0c396acb3fd63b6931517e2858133)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="domainGuid")
    def domain_guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainGuid"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="domainSid")
    def domain_sid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainSid"))

    @builtins.property
    @jsii.member(jsii_name="forestName")
    def forest_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forestName"))

    @builtins.property
    @jsii.member(jsii_name="netbiosDomainName")
    def netbios_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netbiosDomainName"))

    @builtins.property
    @jsii.member(jsii_name="storageSid")
    def storage_sid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSid"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectory]:
        return typing.cast(typing.Optional[DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc136d24ab3ae7575e6239ec6b2d0e2b4e22a2fb7f769a5284a65c419275ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataAzurermStorageAccountAzureFilesAuthenticationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountAzureFilesAuthenticationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c22272a22822119263a8adeb89827d86c125263ab2d05c9ada829018b2cf66ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermStorageAccountAzureFilesAuthenticationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dfd82043aeb85b0d3dc7868571a110e3434442384c5ea62714701148e5e9c4a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermStorageAccountAzureFilesAuthenticationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7aae972e4d924c8f02b1b6c33043df676ea9a040932d2ac460c20e651d2393)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e44dd1905b4d954314a6a2a37e97ec440d8e740907179ef5972a053e67684bbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2563a5192142577e65dfed97b902b27340e1020e3546cbd4cb16f74cc4b38e15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataAzurermStorageAccountAzureFilesAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountAzureFilesAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__048476cd54a5086ba360c5c3394d51cae31a4ecd0eeeff971a36fb94031ffad4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="activeDirectory")
    def active_directory(
        self,
    ) -> DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryList:
        return typing.cast(DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryList, jsii.get(self, "activeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="defaultShareLevelPermission")
    def default_share_level_permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultShareLevelPermission"))

    @builtins.property
    @jsii.member(jsii_name="directoryType")
    def directory_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermStorageAccountAzureFilesAuthentication]:
        return typing.cast(typing.Optional[DataAzurermStorageAccountAzureFilesAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermStorageAccountAzureFilesAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f9fb39abea203ad21e7cfe818b6938e7f1a7f0d173019cbd9c8104ae490ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountConfig",
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
        "resource_group_name": "resourceGroupName",
        "id": "id",
        "min_tls_version": "minTlsVersion",
        "timeouts": "timeouts",
    },
)
class DataAzurermStorageAccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAzurermStorageAccountTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#name DataAzurermStorageAccount#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#resource_group_name DataAzurermStorageAccount#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#id DataAzurermStorageAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param min_tls_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#min_tls_version DataAzurermStorageAccount#min_tls_version}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#timeouts DataAzurermStorageAccount#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataAzurermStorageAccountTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6543012f631ab90019f621ef631dbc2d27a9f097e0783e7e46333ea7f1bdab52)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument min_tls_version", value=min_tls_version, expected_type=type_hints["min_tls_version"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if id is not None:
            self._values["id"] = id
        if min_tls_version is not None:
            self._values["min_tls_version"] = min_tls_version
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#name DataAzurermStorageAccount#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#resource_group_name DataAzurermStorageAccount#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#id DataAzurermStorageAccount#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_tls_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#min_tls_version DataAzurermStorageAccount#min_tls_version}.'''
        result = self._values.get("min_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataAzurermStorageAccountTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#timeouts DataAzurermStorageAccount#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataAzurermStorageAccountTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermStorageAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountCustomDomain",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermStorageAccountCustomDomain:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermStorageAccountCustomDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermStorageAccountCustomDomainList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountCustomDomainList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92f3c01dac2c71a65813ffd30887ea2972413e76949f2d32595b351deae08377)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermStorageAccountCustomDomainOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae26af52073e426b68cc13bec8dd45ca3fb17281396f62a22b8fa77497385113)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermStorageAccountCustomDomainOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ac84ebeb4a30e80c602d92699ccfffef41cff394b5d5c2e2f9e82c10074a13d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03de58d6791d1b2fe661bd405ce48c5cb23613768a32b0840add679afdb4472b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90085b367124209644e34be3a60a43a74f75c45f87d727b5612348d61bf37f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataAzurermStorageAccountCustomDomainOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountCustomDomainOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44b72d7d64c1ee9486dc8fa473633dc526536b5b955d69e64a5ec06e152028ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataAzurermStorageAccountCustomDomain]:
        return typing.cast(typing.Optional[DataAzurermStorageAccountCustomDomain], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermStorageAccountCustomDomain],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876f2d70ace2dda4c11dc67c8eacb617d8adf803d007f0d48fc554e37335f5f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountIdentity",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermStorageAccountIdentity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermStorageAccountIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermStorageAccountIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__210b803cdaf3a38f9f0d2a52ac011c1b67cedbe39cfa2eccfbe2701f0b21b2e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermStorageAccountIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090c3684acdc94f0f7de098688a726caa749754be0236fe3f056350fccca0c3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermStorageAccountIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ddeb337e862c819b3598e6acf9a5bb8f8ecea8bc0249bdce75c378d4367f6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee9287a3ce406d147011fcbbacdab51066f64805ccbcddc7ec73b1f995ddca2e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bfe75628730968008dfcd5f224de8a2de6934b0125f6fbb43dede85384695ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataAzurermStorageAccountIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cefd3fc68a086b8a5081595ae5213903fb5ee4293805da122b1940c29d42573)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataAzurermStorageAccountIdentity]:
        return typing.cast(typing.Optional[DataAzurermStorageAccountIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermStorageAccountIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67275004a68a3da28486fbd7070fc8e671b2c2d9fab5ea78a6d2d0d0ce1f2b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountTimeouts",
    jsii_struct_bases=[],
    name_mapping={"read": "read"},
)
class DataAzurermStorageAccountTimeouts:
    def __init__(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#read DataAzurermStorageAccount#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06fa8e0d9337de3716e64f36b521bb6c8cf0197d64486d070856cbbf9bef262b)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/data-sources/storage_account#read DataAzurermStorageAccount#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermStorageAccountTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermStorageAccountTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermStorageAccount.DataAzurermStorageAccountTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f10db04efc54dd240a28740e59928da8b6ff74877937825488caa1fe9becfc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ccb9a87328396538665b3eca5e63ffc24d271c44f1a9746ac1b55f84ddee8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzurermStorageAccountTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzurermStorageAccountTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzurermStorageAccountTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69f303b7b1263cae1670ab9441941c37393c330596716367ed51d9cdababcf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataAzurermStorageAccount",
    "DataAzurermStorageAccountAzureFilesAuthentication",
    "DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectory",
    "DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryList",
    "DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference",
    "DataAzurermStorageAccountAzureFilesAuthenticationList",
    "DataAzurermStorageAccountAzureFilesAuthenticationOutputReference",
    "DataAzurermStorageAccountConfig",
    "DataAzurermStorageAccountCustomDomain",
    "DataAzurermStorageAccountCustomDomainList",
    "DataAzurermStorageAccountCustomDomainOutputReference",
    "DataAzurermStorageAccountIdentity",
    "DataAzurermStorageAccountIdentityList",
    "DataAzurermStorageAccountIdentityOutputReference",
    "DataAzurermStorageAccountTimeouts",
    "DataAzurermStorageAccountTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__da53b6ba70107e453b4a696ce98372099e5359bf9d2ce7d7269cb71f7a1e4ad5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    min_tls_version: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAzurermStorageAccountTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__19bab86dc769f9b5293bd836e6dd85f0063d303f6ffca2d1e281ed56126acab3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3d5f6b90f4a9d08b2a9ca3b83648ed949000d992264be30d61cd83afdd6f34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__771692ea269f84251dad70f3ddd8b63ec7bdbc0278ff03c1d8c0ce6596798dac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b41d6211716e5cd6d41bde6125df687bc4460ab550d5353f250f83a6061aacb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a6591693ea740bff4316cd007bd3714c43e699f1bce55d6ecbf7bf57cfb25b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa1c79dfba5d837772759a976900564e50de80fbaf416cf84c8a3ca2756dd12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d641edfdf15150c58a07be26c58d3df41e1c33cd10243d30490df81612b937(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908c1ddd059d7a11953b45939a70cc7bd111511a6ab60bb9e51777446f7d7a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a724219ae1571c7ee6980ef5388e06be5037787804a8ac52d67398bb3568f2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93c94b1d804328cf35c5d8dcadd1f5a54e62916fb2cd1ec642d3808b826e3f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7cc0967433f0f7ca51674bf3bf280fd3e0c396acb3fd63b6931517e2858133(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc136d24ab3ae7575e6239ec6b2d0e2b4e22a2fb7f769a5284a65c419275ece(
    value: typing.Optional[DataAzurermStorageAccountAzureFilesAuthenticationActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22272a22822119263a8adeb89827d86c125263ab2d05c9ada829018b2cf66ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dfd82043aeb85b0d3dc7868571a110e3434442384c5ea62714701148e5e9c4a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7aae972e4d924c8f02b1b6c33043df676ea9a040932d2ac460c20e651d2393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44dd1905b4d954314a6a2a37e97ec440d8e740907179ef5972a053e67684bbe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2563a5192142577e65dfed97b902b27340e1020e3546cbd4cb16f74cc4b38e15(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048476cd54a5086ba360c5c3394d51cae31a4ecd0eeeff971a36fb94031ffad4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f9fb39abea203ad21e7cfe818b6938e7f1a7f0d173019cbd9c8104ae490ce7(
    value: typing.Optional[DataAzurermStorageAccountAzureFilesAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6543012f631ab90019f621ef631dbc2d27a9f097e0783e7e46333ea7f1bdab52(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    min_tls_version: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAzurermStorageAccountTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f3c01dac2c71a65813ffd30887ea2972413e76949f2d32595b351deae08377(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae26af52073e426b68cc13bec8dd45ca3fb17281396f62a22b8fa77497385113(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac84ebeb4a30e80c602d92699ccfffef41cff394b5d5c2e2f9e82c10074a13d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03de58d6791d1b2fe661bd405ce48c5cb23613768a32b0840add679afdb4472b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90085b367124209644e34be3a60a43a74f75c45f87d727b5612348d61bf37f0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b72d7d64c1ee9486dc8fa473633dc526536b5b955d69e64a5ec06e152028ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876f2d70ace2dda4c11dc67c8eacb617d8adf803d007f0d48fc554e37335f5f6(
    value: typing.Optional[DataAzurermStorageAccountCustomDomain],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210b803cdaf3a38f9f0d2a52ac011c1b67cedbe39cfa2eccfbe2701f0b21b2e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090c3684acdc94f0f7de098688a726caa749754be0236fe3f056350fccca0c3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ddeb337e862c819b3598e6acf9a5bb8f8ecea8bc0249bdce75c378d4367f6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9287a3ce406d147011fcbbacdab51066f64805ccbcddc7ec73b1f995ddca2e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfe75628730968008dfcd5f224de8a2de6934b0125f6fbb43dede85384695ab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cefd3fc68a086b8a5081595ae5213903fb5ee4293805da122b1940c29d42573(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67275004a68a3da28486fbd7070fc8e671b2c2d9fab5ea78a6d2d0d0ce1f2b02(
    value: typing.Optional[DataAzurermStorageAccountIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06fa8e0d9337de3716e64f36b521bb6c8cf0197d64486d070856cbbf9bef262b(
    *,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f10db04efc54dd240a28740e59928da8b6ff74877937825488caa1fe9becfc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ccb9a87328396538665b3eca5e63ffc24d271c44f1a9746ac1b55f84ddee8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69f303b7b1263cae1670ab9441941c37393c330596716367ed51d9cdababcf8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataAzurermStorageAccountTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

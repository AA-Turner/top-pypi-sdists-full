r'''
# `azurerm_storage_account`

Refer to the Terraform Registry for docs: [`azurerm_storage_account`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account).
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


class StorageAccount(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccount",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account azurerm_storage_account}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_replication_type: builtins.str,
        account_tier: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        access_tier: typing.Optional[builtins.str] = None,
        account_kind: typing.Optional[builtins.str] = None,
        allowed_copy_scope: typing.Optional[builtins.str] = None,
        allow_nested_items_to_be_public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_files_authentication: typing.Optional[typing.Union["StorageAccountAzureFilesAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        blob_properties: typing.Optional[typing.Union["StorageAccountBlobProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        cross_tenant_replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_domain: typing.Optional[typing.Union["StorageAccountCustomDomain", typing.Dict[builtins.str, typing.Any]]] = None,
        customer_managed_key: typing.Optional[typing.Union["StorageAccountCustomerManagedKey", typing.Dict[builtins.str, typing.Any]]] = None,
        default_to_oauth_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dns_endpoint_type: typing.Optional[builtins.str] = None,
        edge_zone: typing.Optional[builtins.str] = None,
        https_traffic_only_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["StorageAccountIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        immutability_policy: typing.Optional[typing.Union["StorageAccountImmutabilityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_hns_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        large_file_share_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        local_user_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        network_rules: typing.Optional[typing.Union["StorageAccountNetworkRules", typing.Dict[builtins.str, typing.Any]]] = None,
        nfsv3_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        queue_encryption_key_type: typing.Optional[builtins.str] = None,
        queue_properties: typing.Optional[typing.Union["StorageAccountQueueProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        routing: typing.Optional[typing.Union["StorageAccountRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        sas_policy: typing.Optional[typing.Union["StorageAccountSasPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        sftp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_access_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        share_properties: typing.Optional[typing.Union["StorageAccountShareProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        static_website: typing.Optional[typing.Union["StorageAccountStaticWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
        table_encryption_key_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["StorageAccountTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account azurerm_storage_account} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_replication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_replication_type StorageAccount#account_replication_type}.
        :param account_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_tier StorageAccount#account_tier}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#location StorageAccount#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#name StorageAccount#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#resource_group_name StorageAccount#resource_group_name}.
        :param access_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#access_tier StorageAccount#access_tier}.
        :param account_kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_kind StorageAccount#account_kind}.
        :param allowed_copy_scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_copy_scope StorageAccount#allowed_copy_scope}.
        :param allow_nested_items_to_be_public: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allow_nested_items_to_be_public StorageAccount#allow_nested_items_to_be_public}.
        :param azure_files_authentication: azure_files_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#azure_files_authentication StorageAccount#azure_files_authentication}
        :param blob_properties: blob_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#blob_properties StorageAccount#blob_properties}
        :param cross_tenant_replication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cross_tenant_replication_enabled StorageAccount#cross_tenant_replication_enabled}.
        :param custom_domain: custom_domain block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#custom_domain StorageAccount#custom_domain}
        :param customer_managed_key: customer_managed_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#customer_managed_key StorageAccount#customer_managed_key}
        :param default_to_oauth_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_to_oauth_authentication StorageAccount#default_to_oauth_authentication}.
        :param dns_endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#dns_endpoint_type StorageAccount#dns_endpoint_type}.
        :param edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#edge_zone StorageAccount#edge_zone}.
        :param https_traffic_only_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#https_traffic_only_enabled StorageAccount#https_traffic_only_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#id StorageAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#identity StorageAccount#identity}
        :param immutability_policy: immutability_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#immutability_policy StorageAccount#immutability_policy}
        :param infrastructure_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#infrastructure_encryption_enabled StorageAccount#infrastructure_encryption_enabled}.
        :param is_hns_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#is_hns_enabled StorageAccount#is_hns_enabled}.
        :param large_file_share_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#large_file_share_enabled StorageAccount#large_file_share_enabled}.
        :param local_user_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#local_user_enabled StorageAccount#local_user_enabled}.
        :param min_tls_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#min_tls_version StorageAccount#min_tls_version}.
        :param network_rules: network_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#network_rules StorageAccount#network_rules}
        :param nfsv3_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#nfsv3_enabled StorageAccount#nfsv3_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#public_network_access_enabled StorageAccount#public_network_access_enabled}.
        :param queue_encryption_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#queue_encryption_key_type StorageAccount#queue_encryption_key_type}.
        :param queue_properties: queue_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#queue_properties StorageAccount#queue_properties}
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#routing StorageAccount#routing}
        :param sas_policy: sas_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#sas_policy StorageAccount#sas_policy}
        :param sftp_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#sftp_enabled StorageAccount#sftp_enabled}.
        :param shared_access_key_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#shared_access_key_enabled StorageAccount#shared_access_key_enabled}.
        :param share_properties: share_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#share_properties StorageAccount#share_properties}
        :param static_website: static_website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#static_website StorageAccount#static_website}
        :param table_encryption_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#table_encryption_key_type StorageAccount#table_encryption_key_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#tags StorageAccount#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#timeouts StorageAccount#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce651f82e85befcf5b1b70214df997041e8773c34ce411c0cffe913042c32e37)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = StorageAccountConfig(
            account_replication_type=account_replication_type,
            account_tier=account_tier,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            access_tier=access_tier,
            account_kind=account_kind,
            allowed_copy_scope=allowed_copy_scope,
            allow_nested_items_to_be_public=allow_nested_items_to_be_public,
            azure_files_authentication=azure_files_authentication,
            blob_properties=blob_properties,
            cross_tenant_replication_enabled=cross_tenant_replication_enabled,
            custom_domain=custom_domain,
            customer_managed_key=customer_managed_key,
            default_to_oauth_authentication=default_to_oauth_authentication,
            dns_endpoint_type=dns_endpoint_type,
            edge_zone=edge_zone,
            https_traffic_only_enabled=https_traffic_only_enabled,
            id=id,
            identity=identity,
            immutability_policy=immutability_policy,
            infrastructure_encryption_enabled=infrastructure_encryption_enabled,
            is_hns_enabled=is_hns_enabled,
            large_file_share_enabled=large_file_share_enabled,
            local_user_enabled=local_user_enabled,
            min_tls_version=min_tls_version,
            network_rules=network_rules,
            nfsv3_enabled=nfsv3_enabled,
            public_network_access_enabled=public_network_access_enabled,
            queue_encryption_key_type=queue_encryption_key_type,
            queue_properties=queue_properties,
            routing=routing,
            sas_policy=sas_policy,
            sftp_enabled=sftp_enabled,
            shared_access_key_enabled=shared_access_key_enabled,
            share_properties=share_properties,
            static_website=static_website,
            table_encryption_key_type=table_encryption_key_type,
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
        '''Generates CDKTF code for importing a StorageAccount resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the StorageAccount to import.
        :param import_from_id: The id of the existing StorageAccount that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the StorageAccount to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d623c20ef496cdb6ad4244f6ef5021407eb8722ce68adc7f94def7dc8f032160)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureFilesAuthentication")
    def put_azure_files_authentication(
        self,
        *,
        directory_type: builtins.str,
        active_directory: typing.Optional[typing.Union["StorageAccountAzureFilesAuthenticationActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        default_share_level_permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#directory_type StorageAccount#directory_type}.
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#active_directory StorageAccount#active_directory}
        :param default_share_level_permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_share_level_permission StorageAccount#default_share_level_permission}.
        '''
        value = StorageAccountAzureFilesAuthentication(
            directory_type=directory_type,
            active_directory=active_directory,
            default_share_level_permission=default_share_level_permission,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureFilesAuthentication", [value]))

    @jsii.member(jsii_name="putBlobProperties")
    def put_blob_properties(
        self,
        *,
        change_feed_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        change_feed_retention_in_days: typing.Optional[jsii.Number] = None,
        container_delete_retention_policy: typing.Optional[typing.Union["StorageAccountBlobPropertiesContainerDeleteRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountBlobPropertiesCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_service_version: typing.Optional[builtins.str] = None,
        delete_retention_policy: typing.Optional[typing.Union["StorageAccountBlobPropertiesDeleteRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        last_access_time_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore_policy: typing.Optional[typing.Union["StorageAccountBlobPropertiesRestorePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        versioning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param change_feed_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#change_feed_enabled StorageAccount#change_feed_enabled}.
        :param change_feed_retention_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#change_feed_retention_in_days StorageAccount#change_feed_retention_in_days}.
        :param container_delete_retention_policy: container_delete_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#container_delete_retention_policy StorageAccount#container_delete_retention_policy}
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        :param default_service_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_service_version StorageAccount#default_service_version}.
        :param delete_retention_policy: delete_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete_retention_policy StorageAccount#delete_retention_policy}
        :param last_access_time_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#last_access_time_enabled StorageAccount#last_access_time_enabled}.
        :param restore_policy: restore_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#restore_policy StorageAccount#restore_policy}
        :param versioning_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#versioning_enabled StorageAccount#versioning_enabled}.
        '''
        value = StorageAccountBlobProperties(
            change_feed_enabled=change_feed_enabled,
            change_feed_retention_in_days=change_feed_retention_in_days,
            container_delete_retention_policy=container_delete_retention_policy,
            cors_rule=cors_rule,
            default_service_version=default_service_version,
            delete_retention_policy=delete_retention_policy,
            last_access_time_enabled=last_access_time_enabled,
            restore_policy=restore_policy,
            versioning_enabled=versioning_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putBlobProperties", [value]))

    @jsii.member(jsii_name="putCustomDomain")
    def put_custom_domain(
        self,
        *,
        name: builtins.str,
        use_subdomain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#name StorageAccount#name}.
        :param use_subdomain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#use_subdomain StorageAccount#use_subdomain}.
        '''
        value = StorageAccountCustomDomain(name=name, use_subdomain=use_subdomain)

        return typing.cast(None, jsii.invoke(self, "putCustomDomain", [value]))

    @jsii.member(jsii_name="putCustomerManagedKey")
    def put_customer_managed_key(
        self,
        *,
        user_assigned_identity_id: builtins.str,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        managed_hsm_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#user_assigned_identity_id StorageAccount#user_assigned_identity_id}.
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#key_vault_key_id StorageAccount#key_vault_key_id}.
        :param managed_hsm_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#managed_hsm_key_id StorageAccount#managed_hsm_key_id}.
        '''
        value = StorageAccountCustomerManagedKey(
            user_assigned_identity_id=user_assigned_identity_id,
            key_vault_key_id=key_vault_key_id,
            managed_hsm_key_id=managed_hsm_key_id,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerManagedKey", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#type StorageAccount#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#identity_ids StorageAccount#identity_ids}.
        '''
        value = StorageAccountIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putImmutabilityPolicy")
    def put_immutability_policy(
        self,
        *,
        allow_protected_append_writes: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        period_since_creation_in_days: jsii.Number,
        state: builtins.str,
    ) -> None:
        '''
        :param allow_protected_append_writes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allow_protected_append_writes StorageAccount#allow_protected_append_writes}.
        :param period_since_creation_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#period_since_creation_in_days StorageAccount#period_since_creation_in_days}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#state StorageAccount#state}.
        '''
        value = StorageAccountImmutabilityPolicy(
            allow_protected_append_writes=allow_protected_append_writes,
            period_since_creation_in_days=period_since_creation_in_days,
            state=state,
        )

        return typing.cast(None, jsii.invoke(self, "putImmutabilityPolicy", [value]))

    @jsii.member(jsii_name="putNetworkRules")
    def put_network_rules(
        self,
        *,
        default_action: builtins.str,
        bypass: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_link_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountNetworkRulesPrivateLinkAccess", typing.Dict[builtins.str, typing.Any]]]]] = None,
        virtual_network_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_action StorageAccount#default_action}.
        :param bypass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#bypass StorageAccount#bypass}.
        :param ip_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#ip_rules StorageAccount#ip_rules}.
        :param private_link_access: private_link_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#private_link_access StorageAccount#private_link_access}
        :param virtual_network_subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#virtual_network_subnet_ids StorageAccount#virtual_network_subnet_ids}.
        '''
        value = StorageAccountNetworkRules(
            default_action=default_action,
            bypass=bypass,
            ip_rules=ip_rules,
            private_link_access=private_link_access,
            virtual_network_subnet_ids=virtual_network_subnet_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putNetworkRules", [value]))

    @jsii.member(jsii_name="putQueueProperties")
    def put_queue_properties(
        self,
        *,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountQueuePropertiesCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hour_metrics: typing.Optional[typing.Union["StorageAccountQueuePropertiesHourMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union["StorageAccountQueuePropertiesLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        minute_metrics: typing.Optional[typing.Union["StorageAccountQueuePropertiesMinuteMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        :param hour_metrics: hour_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#hour_metrics StorageAccount#hour_metrics}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#logging StorageAccount#logging}
        :param minute_metrics: minute_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#minute_metrics StorageAccount#minute_metrics}
        '''
        value = StorageAccountQueueProperties(
            cors_rule=cors_rule,
            hour_metrics=hour_metrics,
            logging=logging,
            minute_metrics=minute_metrics,
        )

        return typing.cast(None, jsii.invoke(self, "putQueueProperties", [value]))

    @jsii.member(jsii_name="putRouting")
    def put_routing(
        self,
        *,
        choice: typing.Optional[builtins.str] = None,
        publish_internet_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        publish_microsoft_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param choice: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#choice StorageAccount#choice}.
        :param publish_internet_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#publish_internet_endpoints StorageAccount#publish_internet_endpoints}.
        :param publish_microsoft_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#publish_microsoft_endpoints StorageAccount#publish_microsoft_endpoints}.
        '''
        value = StorageAccountRouting(
            choice=choice,
            publish_internet_endpoints=publish_internet_endpoints,
            publish_microsoft_endpoints=publish_microsoft_endpoints,
        )

        return typing.cast(None, jsii.invoke(self, "putRouting", [value]))

    @jsii.member(jsii_name="putSasPolicy")
    def put_sas_policy(
        self,
        *,
        expiration_period: builtins.str,
        expiration_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#expiration_period StorageAccount#expiration_period}.
        :param expiration_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#expiration_action StorageAccount#expiration_action}.
        '''
        value = StorageAccountSasPolicy(
            expiration_period=expiration_period, expiration_action=expiration_action
        )

        return typing.cast(None, jsii.invoke(self, "putSasPolicy", [value]))

    @jsii.member(jsii_name="putShareProperties")
    def put_share_properties(
        self,
        *,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountSharePropertiesCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        retention_policy: typing.Optional[typing.Union["StorageAccountSharePropertiesRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        smb: typing.Optional[typing.Union["StorageAccountSharePropertiesSmb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy StorageAccount#retention_policy}
        :param smb: smb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#smb StorageAccount#smb}
        '''
        value = StorageAccountShareProperties(
            cors_rule=cors_rule, retention_policy=retention_policy, smb=smb
        )

        return typing.cast(None, jsii.invoke(self, "putShareProperties", [value]))

    @jsii.member(jsii_name="putStaticWebsite")
    def put_static_website(
        self,
        *,
        error404_document: typing.Optional[builtins.str] = None,
        index_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error404_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#error_404_document StorageAccount#error_404_document}.
        :param index_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#index_document StorageAccount#index_document}.
        '''
        value = StorageAccountStaticWebsite(
            error404_document=error404_document, index_document=index_document
        )

        return typing.cast(None, jsii.invoke(self, "putStaticWebsite", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#create StorageAccount#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete StorageAccount#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#read StorageAccount#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#update StorageAccount#update}.
        '''
        value = StorageAccountTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAccessTier")
    def reset_access_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccessTier", []))

    @jsii.member(jsii_name="resetAccountKind")
    def reset_account_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountKind", []))

    @jsii.member(jsii_name="resetAllowedCopyScope")
    def reset_allowed_copy_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedCopyScope", []))

    @jsii.member(jsii_name="resetAllowNestedItemsToBePublic")
    def reset_allow_nested_items_to_be_public(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowNestedItemsToBePublic", []))

    @jsii.member(jsii_name="resetAzureFilesAuthentication")
    def reset_azure_files_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureFilesAuthentication", []))

    @jsii.member(jsii_name="resetBlobProperties")
    def reset_blob_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlobProperties", []))

    @jsii.member(jsii_name="resetCrossTenantReplicationEnabled")
    def reset_cross_tenant_replication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCrossTenantReplicationEnabled", []))

    @jsii.member(jsii_name="resetCustomDomain")
    def reset_custom_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomDomain", []))

    @jsii.member(jsii_name="resetCustomerManagedKey")
    def reset_customer_managed_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedKey", []))

    @jsii.member(jsii_name="resetDefaultToOauthAuthentication")
    def reset_default_to_oauth_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultToOauthAuthentication", []))

    @jsii.member(jsii_name="resetDnsEndpointType")
    def reset_dns_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsEndpointType", []))

    @jsii.member(jsii_name="resetEdgeZone")
    def reset_edge_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeZone", []))

    @jsii.member(jsii_name="resetHttpsTrafficOnlyEnabled")
    def reset_https_traffic_only_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsTrafficOnlyEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetImmutabilityPolicy")
    def reset_immutability_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImmutabilityPolicy", []))

    @jsii.member(jsii_name="resetInfrastructureEncryptionEnabled")
    def reset_infrastructure_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureEncryptionEnabled", []))

    @jsii.member(jsii_name="resetIsHnsEnabled")
    def reset_is_hns_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsHnsEnabled", []))

    @jsii.member(jsii_name="resetLargeFileShareEnabled")
    def reset_large_file_share_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLargeFileShareEnabled", []))

    @jsii.member(jsii_name="resetLocalUserEnabled")
    def reset_local_user_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalUserEnabled", []))

    @jsii.member(jsii_name="resetMinTlsVersion")
    def reset_min_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinTlsVersion", []))

    @jsii.member(jsii_name="resetNetworkRules")
    def reset_network_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkRules", []))

    @jsii.member(jsii_name="resetNfsv3Enabled")
    def reset_nfsv3_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfsv3Enabled", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetQueueEncryptionKeyType")
    def reset_queue_encryption_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueEncryptionKeyType", []))

    @jsii.member(jsii_name="resetQueueProperties")
    def reset_queue_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueueProperties", []))

    @jsii.member(jsii_name="resetRouting")
    def reset_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouting", []))

    @jsii.member(jsii_name="resetSasPolicy")
    def reset_sas_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSasPolicy", []))

    @jsii.member(jsii_name="resetSftpEnabled")
    def reset_sftp_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSftpEnabled", []))

    @jsii.member(jsii_name="resetSharedAccessKeyEnabled")
    def reset_shared_access_key_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedAccessKeyEnabled", []))

    @jsii.member(jsii_name="resetShareProperties")
    def reset_share_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShareProperties", []))

    @jsii.member(jsii_name="resetStaticWebsite")
    def reset_static_website(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStaticWebsite", []))

    @jsii.member(jsii_name="resetTableEncryptionKeyType")
    def reset_table_encryption_key_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTableEncryptionKeyType", []))

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
    @jsii.member(jsii_name="azureFilesAuthentication")
    def azure_files_authentication(
        self,
    ) -> "StorageAccountAzureFilesAuthenticationOutputReference":
        return typing.cast("StorageAccountAzureFilesAuthenticationOutputReference", jsii.get(self, "azureFilesAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="blobProperties")
    def blob_properties(self) -> "StorageAccountBlobPropertiesOutputReference":
        return typing.cast("StorageAccountBlobPropertiesOutputReference", jsii.get(self, "blobProperties"))

    @builtins.property
    @jsii.member(jsii_name="customDomain")
    def custom_domain(self) -> "StorageAccountCustomDomainOutputReference":
        return typing.cast("StorageAccountCustomDomainOutputReference", jsii.get(self, "customDomain"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKey")
    def customer_managed_key(self) -> "StorageAccountCustomerManagedKeyOutputReference":
        return typing.cast("StorageAccountCustomerManagedKeyOutputReference", jsii.get(self, "customerManagedKey"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "StorageAccountIdentityOutputReference":
        return typing.cast("StorageAccountIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="immutabilityPolicy")
    def immutability_policy(self) -> "StorageAccountImmutabilityPolicyOutputReference":
        return typing.cast("StorageAccountImmutabilityPolicyOutputReference", jsii.get(self, "immutabilityPolicy"))

    @builtins.property
    @jsii.member(jsii_name="networkRules")
    def network_rules(self) -> "StorageAccountNetworkRulesOutputReference":
        return typing.cast("StorageAccountNetworkRulesOutputReference", jsii.get(self, "networkRules"))

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
    @jsii.member(jsii_name="queueProperties")
    def queue_properties(self) -> "StorageAccountQueuePropertiesOutputReference":
        return typing.cast("StorageAccountQueuePropertiesOutputReference", jsii.get(self, "queueProperties"))

    @builtins.property
    @jsii.member(jsii_name="routing")
    def routing(self) -> "StorageAccountRoutingOutputReference":
        return typing.cast("StorageAccountRoutingOutputReference", jsii.get(self, "routing"))

    @builtins.property
    @jsii.member(jsii_name="sasPolicy")
    def sas_policy(self) -> "StorageAccountSasPolicyOutputReference":
        return typing.cast("StorageAccountSasPolicyOutputReference", jsii.get(self, "sasPolicy"))

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
    @jsii.member(jsii_name="shareProperties")
    def share_properties(self) -> "StorageAccountSharePropertiesOutputReference":
        return typing.cast("StorageAccountSharePropertiesOutputReference", jsii.get(self, "shareProperties"))

    @builtins.property
    @jsii.member(jsii_name="staticWebsite")
    def static_website(self) -> "StorageAccountStaticWebsiteOutputReference":
        return typing.cast("StorageAccountStaticWebsiteOutputReference", jsii.get(self, "staticWebsite"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "StorageAccountTimeoutsOutputReference":
        return typing.cast("StorageAccountTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="accessTierInput")
    def access_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessTierInput"))

    @builtins.property
    @jsii.member(jsii_name="accountKindInput")
    def account_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountKindInput"))

    @builtins.property
    @jsii.member(jsii_name="accountReplicationTypeInput")
    def account_replication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountReplicationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountTierInput")
    def account_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountTierInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedCopyScopeInput")
    def allowed_copy_scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedCopyScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowNestedItemsToBePublicInput")
    def allow_nested_items_to_be_public_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowNestedItemsToBePublicInput"))

    @builtins.property
    @jsii.member(jsii_name="azureFilesAuthenticationInput")
    def azure_files_authentication_input(
        self,
    ) -> typing.Optional["StorageAccountAzureFilesAuthentication"]:
        return typing.cast(typing.Optional["StorageAccountAzureFilesAuthentication"], jsii.get(self, "azureFilesAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="blobPropertiesInput")
    def blob_properties_input(self) -> typing.Optional["StorageAccountBlobProperties"]:
        return typing.cast(typing.Optional["StorageAccountBlobProperties"], jsii.get(self, "blobPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="crossTenantReplicationEnabledInput")
    def cross_tenant_replication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "crossTenantReplicationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="customDomainInput")
    def custom_domain_input(self) -> typing.Optional["StorageAccountCustomDomain"]:
        return typing.cast(typing.Optional["StorageAccountCustomDomain"], jsii.get(self, "customDomainInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyInput")
    def customer_managed_key_input(
        self,
    ) -> typing.Optional["StorageAccountCustomerManagedKey"]:
        return typing.cast(typing.Optional["StorageAccountCustomerManagedKey"], jsii.get(self, "customerManagedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultToOauthAuthenticationInput")
    def default_to_oauth_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultToOauthAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsEndpointTypeInput")
    def dns_endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dnsEndpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeZoneInput")
    def edge_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "edgeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsTrafficOnlyEnabledInput")
    def https_traffic_only_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpsTrafficOnlyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["StorageAccountIdentity"]:
        return typing.cast(typing.Optional["StorageAccountIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="immutabilityPolicyInput")
    def immutability_policy_input(
        self,
    ) -> typing.Optional["StorageAccountImmutabilityPolicy"]:
        return typing.cast(typing.Optional["StorageAccountImmutabilityPolicy"], jsii.get(self, "immutabilityPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureEncryptionEnabledInput")
    def infrastructure_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "infrastructureEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isHnsEnabledInput")
    def is_hns_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isHnsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="largeFileShareEnabledInput")
    def large_file_share_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "largeFileShareEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="localUserEnabledInput")
    def local_user_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localUserEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="minTlsVersionInput")
    def min_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkRulesInput")
    def network_rules_input(self) -> typing.Optional["StorageAccountNetworkRules"]:
        return typing.cast(typing.Optional["StorageAccountNetworkRules"], jsii.get(self, "networkRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsv3EnabledInput")
    def nfsv3_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nfsv3EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="queueEncryptionKeyTypeInput")
    def queue_encryption_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queueEncryptionKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="queuePropertiesInput")
    def queue_properties_input(
        self,
    ) -> typing.Optional["StorageAccountQueueProperties"]:
        return typing.cast(typing.Optional["StorageAccountQueueProperties"], jsii.get(self, "queuePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="routingInput")
    def routing_input(self) -> typing.Optional["StorageAccountRouting"]:
        return typing.cast(typing.Optional["StorageAccountRouting"], jsii.get(self, "routingInput"))

    @builtins.property
    @jsii.member(jsii_name="sasPolicyInput")
    def sas_policy_input(self) -> typing.Optional["StorageAccountSasPolicy"]:
        return typing.cast(typing.Optional["StorageAccountSasPolicy"], jsii.get(self, "sasPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="sftpEnabledInput")
    def sftp_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sftpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedAccessKeyEnabledInput")
    def shared_access_key_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sharedAccessKeyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sharePropertiesInput")
    def share_properties_input(
        self,
    ) -> typing.Optional["StorageAccountShareProperties"]:
        return typing.cast(typing.Optional["StorageAccountShareProperties"], jsii.get(self, "sharePropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="staticWebsiteInput")
    def static_website_input(self) -> typing.Optional["StorageAccountStaticWebsite"]:
        return typing.cast(typing.Optional["StorageAccountStaticWebsite"], jsii.get(self, "staticWebsiteInput"))

    @builtins.property
    @jsii.member(jsii_name="tableEncryptionKeyTypeInput")
    def table_encryption_key_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableEncryptionKeyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageAccountTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "StorageAccountTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="accessTier")
    def access_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessTier"))

    @access_tier.setter
    def access_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5509f28bca2a4dea8e0aab327fb3ac1221861a151d0b48ae249912b15b93c1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountKind")
    def account_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountKind"))

    @account_kind.setter
    def account_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf37fd5d0a2cb4d73a6e2e0c4219711e87dffc4f1e61c756d4e7b7195048b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountReplicationType")
    def account_replication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountReplicationType"))

    @account_replication_type.setter
    def account_replication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca8b656211910a0aa8025b673d36c3b25e63cc664d6cb1a4a8443712a11cfe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountReplicationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountTier")
    def account_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountTier"))

    @account_tier.setter
    def account_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164d07418fab5b22b506b51e1c8e51b39bbda1a569e3c6feab4ea4023b3fb73e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedCopyScope")
    def allowed_copy_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedCopyScope"))

    @allowed_copy_scope.setter
    def allowed_copy_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0938838b0271c52b58d86c2d0cad4977fe484abb044ce8ca21af08040922227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedCopyScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowNestedItemsToBePublic")
    def allow_nested_items_to_be_public(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowNestedItemsToBePublic"))

    @allow_nested_items_to_be_public.setter
    def allow_nested_items_to_be_public(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4edae5b8b37f8266b4eae54207b7c6c6d39a62d98852e09521161a7925f12528)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNestedItemsToBePublic", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="crossTenantReplicationEnabled")
    def cross_tenant_replication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "crossTenantReplicationEnabled"))

    @cross_tenant_replication_enabled.setter
    def cross_tenant_replication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba859791facc1107dcbb34a9b00a56aad7efa54c1d83c4dfc0cfce6629e36e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "crossTenantReplicationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultToOauthAuthentication")
    def default_to_oauth_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultToOauthAuthentication"))

    @default_to_oauth_authentication.setter
    def default_to_oauth_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63478ea634c4d3697f5e4db2ba411663af5d8912a1f5ab8d2456d775405e934f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultToOauthAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dnsEndpointType")
    def dns_endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dnsEndpointType"))

    @dns_endpoint_type.setter
    def dns_endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdd24803f6d097a06a0c9160673e9fe095bbb1fb0f8ee6bc6ca71f20251bf47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsEndpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeZone")
    def edge_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "edgeZone"))

    @edge_zone.setter
    def edge_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6579060cff9393a14136405677d95cb0a6d119c231cd4788034ec7b3af4f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsTrafficOnlyEnabled")
    def https_traffic_only_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpsTrafficOnlyEnabled"))

    @https_traffic_only_enabled.setter
    def https_traffic_only_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59b4add0a6a1dd84dc842fb6b85f861cbfaf2a9ce9d4d105509371e669069f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsTrafficOnlyEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00affcd6634a915de2022f0d26cad021b40589613ce9242157f1b0d52daa1d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="infrastructureEncryptionEnabled")
    def infrastructure_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "infrastructureEncryptionEnabled"))

    @infrastructure_encryption_enabled.setter
    def infrastructure_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c855487a4e02eea5557644787da02d82ae00cd74eb943f151e9a5400c86f2dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureEncryptionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isHnsEnabled")
    def is_hns_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isHnsEnabled"))

    @is_hns_enabled.setter
    def is_hns_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985b9274488616658964abc4654d0c113ce7e00ec5c088739e3114649277cc76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isHnsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="largeFileShareEnabled")
    def large_file_share_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "largeFileShareEnabled"))

    @large_file_share_enabled.setter
    def large_file_share_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400a5cb0f34f8184813420bb69666fd830a1be4de9be39cd6ec7704c7fc3c62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "largeFileShareEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localUserEnabled")
    def local_user_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "localUserEnabled"))

    @local_user_enabled.setter
    def local_user_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbdf98d1d7535958a0dd94a4679b1f6b209fef91618d0adc73aed8ef5c96d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localUserEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d8a2c333be192b920a204706c967959bd8e11ea354fd085da5b5a92c07dd88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minTlsVersion")
    def min_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minTlsVersion"))

    @min_tls_version.setter
    def min_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__120b8beef36c1b857b3b2c5154aaeb59cd35942d4dac2c7085c93187b0f69ca7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minTlsVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce738233af1ea4e8e6d9e8a5165df682665e93f72058b06c71b9b74d3a9e4f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsv3Enabled")
    def nfsv3_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nfsv3Enabled"))

    @nfsv3_enabled.setter
    def nfsv3_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186dee099299a876b2c8816b3b68a8aaf85c53d59c7725d90d91d4a85562a257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsv3Enabled", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b27e525daa2e2d15851b8ea987888bfd923ae9bbb3b24cd1f5917d4ef3acb4ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queueEncryptionKeyType")
    def queue_encryption_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queueEncryptionKeyType"))

    @queue_encryption_key_type.setter
    def queue_encryption_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc3afd391739f688d50cbb1ab279121be97d5d81182f38fac4702dd8a6e7be8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queueEncryptionKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553bbc0d40ebf30b293c040b665fe2eac04325f23337897a3ae4b29d21563a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sftpEnabled")
    def sftp_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sftpEnabled"))

    @sftp_enabled.setter
    def sftp_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b521ae0d33ca7e6631cc6e2b9106bbc5f9487d83562c821068cecec215ed2130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sftpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedAccessKeyEnabled")
    def shared_access_key_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sharedAccessKeyEnabled"))

    @shared_access_key_enabled.setter
    def shared_access_key_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3185b20705992a4c137d676c8f8fa8da0bd548b9df680f2ca615ab5626cc861c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedAccessKeyEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableEncryptionKeyType")
    def table_encryption_key_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableEncryptionKeyType"))

    @table_encryption_key_type.setter
    def table_encryption_key_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcdaa9baf0a4ecca46dfa2e4b13d369779496b273c79f1b5c46480ac38378f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableEncryptionKeyType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291684da71c6233f617d8763d1831b08a9af3ee1f0a4c600e48dfcf0ebadda6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountAzureFilesAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "directory_type": "directoryType",
        "active_directory": "activeDirectory",
        "default_share_level_permission": "defaultShareLevelPermission",
    },
)
class StorageAccountAzureFilesAuthentication:
    def __init__(
        self,
        *,
        directory_type: builtins.str,
        active_directory: typing.Optional[typing.Union["StorageAccountAzureFilesAuthenticationActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        default_share_level_permission: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#directory_type StorageAccount#directory_type}.
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#active_directory StorageAccount#active_directory}
        :param default_share_level_permission: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_share_level_permission StorageAccount#default_share_level_permission}.
        '''
        if isinstance(active_directory, dict):
            active_directory = StorageAccountAzureFilesAuthenticationActiveDirectory(**active_directory)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c7c4844f589e62c26caa271cabd1b933f7cfbbf5fc9e606c8d93233c202770)
            check_type(argname="argument directory_type", value=directory_type, expected_type=type_hints["directory_type"])
            check_type(argname="argument active_directory", value=active_directory, expected_type=type_hints["active_directory"])
            check_type(argname="argument default_share_level_permission", value=default_share_level_permission, expected_type=type_hints["default_share_level_permission"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directory_type": directory_type,
        }
        if active_directory is not None:
            self._values["active_directory"] = active_directory
        if default_share_level_permission is not None:
            self._values["default_share_level_permission"] = default_share_level_permission

    @builtins.property
    def directory_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#directory_type StorageAccount#directory_type}.'''
        result = self._values.get("directory_type")
        assert result is not None, "Required property 'directory_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def active_directory(
        self,
    ) -> typing.Optional["StorageAccountAzureFilesAuthenticationActiveDirectory"]:
        '''active_directory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#active_directory StorageAccount#active_directory}
        '''
        result = self._values.get("active_directory")
        return typing.cast(typing.Optional["StorageAccountAzureFilesAuthenticationActiveDirectory"], result)

    @builtins.property
    def default_share_level_permission(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_share_level_permission StorageAccount#default_share_level_permission}.'''
        result = self._values.get("default_share_level_permission")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountAzureFilesAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountAzureFilesAuthenticationActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={
        "domain_guid": "domainGuid",
        "domain_name": "domainName",
        "domain_sid": "domainSid",
        "forest_name": "forestName",
        "netbios_domain_name": "netbiosDomainName",
        "storage_sid": "storageSid",
    },
)
class StorageAccountAzureFilesAuthenticationActiveDirectory:
    def __init__(
        self,
        *,
        domain_guid: builtins.str,
        domain_name: builtins.str,
        domain_sid: typing.Optional[builtins.str] = None,
        forest_name: typing.Optional[builtins.str] = None,
        netbios_domain_name: typing.Optional[builtins.str] = None,
        storage_sid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_guid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_guid StorageAccount#domain_guid}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_name StorageAccount#domain_name}.
        :param domain_sid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_sid StorageAccount#domain_sid}.
        :param forest_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#forest_name StorageAccount#forest_name}.
        :param netbios_domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#netbios_domain_name StorageAccount#netbios_domain_name}.
        :param storage_sid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#storage_sid StorageAccount#storage_sid}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36e3349ae74542f974fc8b566a50a811327891f324ba03b970b2b2e208072de)
            check_type(argname="argument domain_guid", value=domain_guid, expected_type=type_hints["domain_guid"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_sid", value=domain_sid, expected_type=type_hints["domain_sid"])
            check_type(argname="argument forest_name", value=forest_name, expected_type=type_hints["forest_name"])
            check_type(argname="argument netbios_domain_name", value=netbios_domain_name, expected_type=type_hints["netbios_domain_name"])
            check_type(argname="argument storage_sid", value=storage_sid, expected_type=type_hints["storage_sid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_guid": domain_guid,
            "domain_name": domain_name,
        }
        if domain_sid is not None:
            self._values["domain_sid"] = domain_sid
        if forest_name is not None:
            self._values["forest_name"] = forest_name
        if netbios_domain_name is not None:
            self._values["netbios_domain_name"] = netbios_domain_name
        if storage_sid is not None:
            self._values["storage_sid"] = storage_sid

    @builtins.property
    def domain_guid(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_guid StorageAccount#domain_guid}.'''
        result = self._values.get("domain_guid")
        assert result is not None, "Required property 'domain_guid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_name StorageAccount#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_sid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_sid StorageAccount#domain_sid}.'''
        result = self._values.get("domain_sid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forest_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#forest_name StorageAccount#forest_name}.'''
        result = self._values.get("forest_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netbios_domain_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#netbios_domain_name StorageAccount#netbios_domain_name}.'''
        result = self._values.get("netbios_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_sid(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#storage_sid StorageAccount#storage_sid}.'''
        result = self._values.get("storage_sid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountAzureFilesAuthenticationActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c968783755f02282d89974468d4dabc85b2115ea3c7aa73f73fd8343836b3c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDomainSid")
    def reset_domain_sid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainSid", []))

    @jsii.member(jsii_name="resetForestName")
    def reset_forest_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForestName", []))

    @jsii.member(jsii_name="resetNetbiosDomainName")
    def reset_netbios_domain_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetbiosDomainName", []))

    @jsii.member(jsii_name="resetStorageSid")
    def reset_storage_sid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageSid", []))

    @builtins.property
    @jsii.member(jsii_name="domainGuidInput")
    def domain_guid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainGuidInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainSidInput")
    def domain_sid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainSidInput"))

    @builtins.property
    @jsii.member(jsii_name="forestNameInput")
    def forest_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forestNameInput"))

    @builtins.property
    @jsii.member(jsii_name="netbiosDomainNameInput")
    def netbios_domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netbiosDomainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageSidInput")
    def storage_sid_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageSidInput"))

    @builtins.property
    @jsii.member(jsii_name="domainGuid")
    def domain_guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainGuid"))

    @domain_guid.setter
    def domain_guid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88447d8ce99b1339c23154c470a796a90af35a3ff6c6686264dc4aed3698c8c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainGuid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9c289fcc94c775f9eda0c08f03a4d036170d1f88d57844ff2679df7d77b86d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domainSid")
    def domain_sid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainSid"))

    @domain_sid.setter
    def domain_sid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc654db6fdf686a02d95c9d8e859245fb3952f0c51971dccf08ce372881991f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainSid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forestName")
    def forest_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forestName"))

    @forest_name.setter
    def forest_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd22c2adefe93d452715f254e294c8fd6e327578385c9af38bdff346c8a4a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forestName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="netbiosDomainName")
    def netbios_domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netbiosDomainName"))

    @netbios_domain_name.setter
    def netbios_domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4107d1a8d924c56fed1c4ed380e25cb178f6af1c2ac4726d7f92e11c7b46de6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netbiosDomainName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageSid")
    def storage_sid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageSid"))

    @storage_sid.setter
    def storage_sid(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13474445904897111a16fb43030ad09f3dec6f38e00f17d2a3c93339e0431569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageSid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountAzureFilesAuthenticationActiveDirectory]:
        return typing.cast(typing.Optional[StorageAccountAzureFilesAuthenticationActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountAzureFilesAuthenticationActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45f6db353efc897bd02977cbde15f77078cad7d88779e8bda2327ae6cacdf584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountAzureFilesAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountAzureFilesAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cc7a72b13e2c567f37b59c05b2ab2afdd63b8f5871d68640e1c3318261df404)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveDirectory")
    def put_active_directory(
        self,
        *,
        domain_guid: builtins.str,
        domain_name: builtins.str,
        domain_sid: typing.Optional[builtins.str] = None,
        forest_name: typing.Optional[builtins.str] = None,
        netbios_domain_name: typing.Optional[builtins.str] = None,
        storage_sid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain_guid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_guid StorageAccount#domain_guid}.
        :param domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_name StorageAccount#domain_name}.
        :param domain_sid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#domain_sid StorageAccount#domain_sid}.
        :param forest_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#forest_name StorageAccount#forest_name}.
        :param netbios_domain_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#netbios_domain_name StorageAccount#netbios_domain_name}.
        :param storage_sid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#storage_sid StorageAccount#storage_sid}.
        '''
        value = StorageAccountAzureFilesAuthenticationActiveDirectory(
            domain_guid=domain_guid,
            domain_name=domain_name,
            domain_sid=domain_sid,
            forest_name=forest_name,
            netbios_domain_name=netbios_domain_name,
            storage_sid=storage_sid,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveDirectory", [value]))

    @jsii.member(jsii_name="resetActiveDirectory")
    def reset_active_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectory", []))

    @jsii.member(jsii_name="resetDefaultShareLevelPermission")
    def reset_default_share_level_permission(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultShareLevelPermission", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectory")
    def active_directory(
        self,
    ) -> StorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference:
        return typing.cast(StorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference, jsii.get(self, "activeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryInput")
    def active_directory_input(
        self,
    ) -> typing.Optional[StorageAccountAzureFilesAuthenticationActiveDirectory]:
        return typing.cast(typing.Optional[StorageAccountAzureFilesAuthenticationActiveDirectory], jsii.get(self, "activeDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultShareLevelPermissionInput")
    def default_share_level_permission_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultShareLevelPermissionInput"))

    @builtins.property
    @jsii.member(jsii_name="directoryTypeInput")
    def directory_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultShareLevelPermission")
    def default_share_level_permission(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultShareLevelPermission"))

    @default_share_level_permission.setter
    def default_share_level_permission(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc99b9f6097ea9bf007854362ae46655b32c6cbb4e163b5c3ba0bc7cac4ad13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultShareLevelPermission", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="directoryType")
    def directory_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "directoryType"))

    @directory_type.setter
    def directory_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0f3652f5866422b9b1001a9e4f36ff840f7a19d9f7196140b763f046f66c64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountAzureFilesAuthentication]:
        return typing.cast(typing.Optional[StorageAccountAzureFilesAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountAzureFilesAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf22381183669de15e025a3acc4a0b3745ca045806655fb0b494ebd55f50927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobProperties",
    jsii_struct_bases=[],
    name_mapping={
        "change_feed_enabled": "changeFeedEnabled",
        "change_feed_retention_in_days": "changeFeedRetentionInDays",
        "container_delete_retention_policy": "containerDeleteRetentionPolicy",
        "cors_rule": "corsRule",
        "default_service_version": "defaultServiceVersion",
        "delete_retention_policy": "deleteRetentionPolicy",
        "last_access_time_enabled": "lastAccessTimeEnabled",
        "restore_policy": "restorePolicy",
        "versioning_enabled": "versioningEnabled",
    },
)
class StorageAccountBlobProperties:
    def __init__(
        self,
        *,
        change_feed_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        change_feed_retention_in_days: typing.Optional[jsii.Number] = None,
        container_delete_retention_policy: typing.Optional[typing.Union["StorageAccountBlobPropertiesContainerDeleteRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountBlobPropertiesCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_service_version: typing.Optional[builtins.str] = None,
        delete_retention_policy: typing.Optional[typing.Union["StorageAccountBlobPropertiesDeleteRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        last_access_time_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        restore_policy: typing.Optional[typing.Union["StorageAccountBlobPropertiesRestorePolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        versioning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param change_feed_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#change_feed_enabled StorageAccount#change_feed_enabled}.
        :param change_feed_retention_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#change_feed_retention_in_days StorageAccount#change_feed_retention_in_days}.
        :param container_delete_retention_policy: container_delete_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#container_delete_retention_policy StorageAccount#container_delete_retention_policy}
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        :param default_service_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_service_version StorageAccount#default_service_version}.
        :param delete_retention_policy: delete_retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete_retention_policy StorageAccount#delete_retention_policy}
        :param last_access_time_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#last_access_time_enabled StorageAccount#last_access_time_enabled}.
        :param restore_policy: restore_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#restore_policy StorageAccount#restore_policy}
        :param versioning_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#versioning_enabled StorageAccount#versioning_enabled}.
        '''
        if isinstance(container_delete_retention_policy, dict):
            container_delete_retention_policy = StorageAccountBlobPropertiesContainerDeleteRetentionPolicy(**container_delete_retention_policy)
        if isinstance(delete_retention_policy, dict):
            delete_retention_policy = StorageAccountBlobPropertiesDeleteRetentionPolicy(**delete_retention_policy)
        if isinstance(restore_policy, dict):
            restore_policy = StorageAccountBlobPropertiesRestorePolicy(**restore_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6df10245dd529c2b54c3dd2f3266d99c45628de920de244abf443ba1d77c7b6d)
            check_type(argname="argument change_feed_enabled", value=change_feed_enabled, expected_type=type_hints["change_feed_enabled"])
            check_type(argname="argument change_feed_retention_in_days", value=change_feed_retention_in_days, expected_type=type_hints["change_feed_retention_in_days"])
            check_type(argname="argument container_delete_retention_policy", value=container_delete_retention_policy, expected_type=type_hints["container_delete_retention_policy"])
            check_type(argname="argument cors_rule", value=cors_rule, expected_type=type_hints["cors_rule"])
            check_type(argname="argument default_service_version", value=default_service_version, expected_type=type_hints["default_service_version"])
            check_type(argname="argument delete_retention_policy", value=delete_retention_policy, expected_type=type_hints["delete_retention_policy"])
            check_type(argname="argument last_access_time_enabled", value=last_access_time_enabled, expected_type=type_hints["last_access_time_enabled"])
            check_type(argname="argument restore_policy", value=restore_policy, expected_type=type_hints["restore_policy"])
            check_type(argname="argument versioning_enabled", value=versioning_enabled, expected_type=type_hints["versioning_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if change_feed_enabled is not None:
            self._values["change_feed_enabled"] = change_feed_enabled
        if change_feed_retention_in_days is not None:
            self._values["change_feed_retention_in_days"] = change_feed_retention_in_days
        if container_delete_retention_policy is not None:
            self._values["container_delete_retention_policy"] = container_delete_retention_policy
        if cors_rule is not None:
            self._values["cors_rule"] = cors_rule
        if default_service_version is not None:
            self._values["default_service_version"] = default_service_version
        if delete_retention_policy is not None:
            self._values["delete_retention_policy"] = delete_retention_policy
        if last_access_time_enabled is not None:
            self._values["last_access_time_enabled"] = last_access_time_enabled
        if restore_policy is not None:
            self._values["restore_policy"] = restore_policy
        if versioning_enabled is not None:
            self._values["versioning_enabled"] = versioning_enabled

    @builtins.property
    def change_feed_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#change_feed_enabled StorageAccount#change_feed_enabled}.'''
        result = self._values.get("change_feed_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def change_feed_retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#change_feed_retention_in_days StorageAccount#change_feed_retention_in_days}.'''
        result = self._values.get("change_feed_retention_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def container_delete_retention_policy(
        self,
    ) -> typing.Optional["StorageAccountBlobPropertiesContainerDeleteRetentionPolicy"]:
        '''container_delete_retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#container_delete_retention_policy StorageAccount#container_delete_retention_policy}
        '''
        result = self._values.get("container_delete_retention_policy")
        return typing.cast(typing.Optional["StorageAccountBlobPropertiesContainerDeleteRetentionPolicy"], result)

    @builtins.property
    def cors_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountBlobPropertiesCorsRule"]]]:
        '''cors_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        '''
        result = self._values.get("cors_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountBlobPropertiesCorsRule"]]], result)

    @builtins.property
    def default_service_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_service_version StorageAccount#default_service_version}.'''
        result = self._values.get("default_service_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete_retention_policy(
        self,
    ) -> typing.Optional["StorageAccountBlobPropertiesDeleteRetentionPolicy"]:
        '''delete_retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete_retention_policy StorageAccount#delete_retention_policy}
        '''
        result = self._values.get("delete_retention_policy")
        return typing.cast(typing.Optional["StorageAccountBlobPropertiesDeleteRetentionPolicy"], result)

    @builtins.property
    def last_access_time_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#last_access_time_enabled StorageAccount#last_access_time_enabled}.'''
        result = self._values.get("last_access_time_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def restore_policy(
        self,
    ) -> typing.Optional["StorageAccountBlobPropertiesRestorePolicy"]:
        '''restore_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#restore_policy StorageAccount#restore_policy}
        '''
        result = self._values.get("restore_policy")
        return typing.cast(typing.Optional["StorageAccountBlobPropertiesRestorePolicy"], result)

    @builtins.property
    def versioning_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#versioning_enabled StorageAccount#versioning_enabled}.'''
        result = self._values.get("versioning_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountBlobProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesContainerDeleteRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={"days": "days"},
)
class StorageAccountBlobPropertiesContainerDeleteRetentionPolicy:
    def __init__(self, *, days: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1b3f1f346f85e36cc6bddb53d1d00b3cdc7647abc2419b0ca6d09a7fab4d363)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountBlobPropertiesContainerDeleteRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountBlobPropertiesContainerDeleteRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesContainerDeleteRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__201929429b4e663a863ea825f8216c77e899158488b6b88301834990bf28f8a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf15397e1163609379a7315d38ef86a6792fece889ebf8d9c1cba8e2af8c5f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountBlobPropertiesContainerDeleteRetentionPolicy]:
        return typing.cast(typing.Optional[StorageAccountBlobPropertiesContainerDeleteRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountBlobPropertiesContainerDeleteRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef376ca802832793373547e08d0986990aa67b874a178f80596184fd6e8013a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesCorsRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "exposed_headers": "exposedHeaders",
        "max_age_in_seconds": "maxAgeInSeconds",
    },
)
class StorageAccountBlobPropertiesCorsRule:
    def __init__(
        self,
        *,
        allowed_headers: typing.Sequence[builtins.str],
        allowed_methods: typing.Sequence[builtins.str],
        allowed_origins: typing.Sequence[builtins.str],
        exposed_headers: typing.Sequence[builtins.str],
        max_age_in_seconds: jsii.Number,
    ) -> None:
        '''
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_headers StorageAccount#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_methods StorageAccount#allowed_methods}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_origins StorageAccount#allowed_origins}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#exposed_headers StorageAccount#exposed_headers}.
        :param max_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#max_age_in_seconds StorageAccount#max_age_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab350d1852f307a865c2dc72de4b01824bcdce81d00db130b51efd01db75e26)
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument exposed_headers", value=exposed_headers, expected_type=type_hints["exposed_headers"])
            check_type(argname="argument max_age_in_seconds", value=max_age_in_seconds, expected_type=type_hints["max_age_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_headers": allowed_headers,
            "allowed_methods": allowed_methods,
            "allowed_origins": allowed_origins,
            "exposed_headers": exposed_headers,
            "max_age_in_seconds": max_age_in_seconds,
        }

    @builtins.property
    def allowed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_headers StorageAccount#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        assert result is not None, "Required property 'allowed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_methods StorageAccount#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_origins StorageAccount#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def exposed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#exposed_headers StorageAccount#exposed_headers}.'''
        result = self._values.get("exposed_headers")
        assert result is not None, "Required property 'exposed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def max_age_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#max_age_in_seconds StorageAccount#max_age_in_seconds}.'''
        result = self._values.get("max_age_in_seconds")
        assert result is not None, "Required property 'max_age_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountBlobPropertiesCorsRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountBlobPropertiesCorsRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesCorsRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95461c7c174b5678c49b420ee12abce520d0c5bda044ffbaf40abb9448616386)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageAccountBlobPropertiesCorsRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc1b085458a8954def2f99a76882dc3471da0a25729c9994a2d425d8537ad81)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageAccountBlobPropertiesCorsRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04dc9f0982832b5e85cc1d73f706c1b3ccdcf082a1bcbd6e951456e24ed4dfdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c1b1e870c7f9b9b364bb1277d391b31571b61c5d9da62f6a323edf20caf378d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__095a6890153788345da9639fac979506d0eda17f703377da31522af2efe22eee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountBlobPropertiesCorsRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountBlobPropertiesCorsRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountBlobPropertiesCorsRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ef755d055feaf21e516a6406278000e1055885bd10403d85de89883c6149f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountBlobPropertiesCorsRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesCorsRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__526ab63018f0d5506eb220a363408a1c3c81fafb6f0e7d70542baf45ab66f313)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposedHeadersInput")
    def exposed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSecondsInput")
    def max_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26083cfd3e1e91b880655b139595692cb6017073755814d46d40a513b7085594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6108e8378558fdd9a992cb8228d4642c210d1918f870d219e43728b6f52558df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b92cb48598b77b7934f6ecbb1a730493a4ba9abf5ac15e2514f27b50feb90f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposedHeaders")
    def exposed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposedHeaders"))

    @exposed_headers.setter
    def exposed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c222f4b3916a0c56196feee93c1fefc90787a36fd68b3f86ba7cb904d1a7b4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSeconds")
    def max_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeInSeconds"))

    @max_age_in_seconds.setter
    def max_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68551dde0bbff40d2e2fc3e981818201104895e6efb43ab420bf35a745a1b3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountBlobPropertiesCorsRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountBlobPropertiesCorsRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountBlobPropertiesCorsRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d1c40d8ed96bf8f3191ba410c596f14bf4d830b8f4d262c6778ea9bc7bb091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesDeleteRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "days": "days",
        "permanent_delete_enabled": "permanentDeleteEnabled",
    },
)
class StorageAccountBlobPropertiesDeleteRetentionPolicy:
    def __init__(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        permanent_delete_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.
        :param permanent_delete_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#permanent_delete_enabled StorageAccount#permanent_delete_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868a8114349e3923b4e4483c045be5e938cb06143a765d87835b8f3fedef50a1)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument permanent_delete_enabled", value=permanent_delete_enabled, expected_type=type_hints["permanent_delete_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days
        if permanent_delete_enabled is not None:
            self._values["permanent_delete_enabled"] = permanent_delete_enabled

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def permanent_delete_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#permanent_delete_enabled StorageAccount#permanent_delete_enabled}.'''
        result = self._values.get("permanent_delete_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountBlobPropertiesDeleteRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountBlobPropertiesDeleteRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesDeleteRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__983e88827d25ab340143c3a7f26d05f1f88890f2a96821358bfd560b0996a7f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetPermanentDeleteEnabled")
    def reset_permanent_delete_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermanentDeleteEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="permanentDeleteEnabledInput")
    def permanent_delete_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permanentDeleteEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140a300b1d330f089cfb3be4a093c629409ae33a7a1ab8f82c956406a1dee49a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permanentDeleteEnabled")
    def permanent_delete_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permanentDeleteEnabled"))

    @permanent_delete_enabled.setter
    def permanent_delete_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f21e562a6799cd01f7d57674d77269c6ede0d81afa89b62157477b90469433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permanentDeleteEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountBlobPropertiesDeleteRetentionPolicy]:
        return typing.cast(typing.Optional[StorageAccountBlobPropertiesDeleteRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountBlobPropertiesDeleteRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eceab6fc546dcd454774bd13feb90b1a91514424693427bab776ff33f09ce16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountBlobPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f205238a7b68cd770ed7febe5a6472254a70955bd5db53bf26f338708ce85698)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainerDeleteRetentionPolicy")
    def put_container_delete_retention_policy(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.
        '''
        value = StorageAccountBlobPropertiesContainerDeleteRetentionPolicy(days=days)

        return typing.cast(None, jsii.invoke(self, "putContainerDeleteRetentionPolicy", [value]))

    @jsii.member(jsii_name="putCorsRule")
    def put_cors_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountBlobPropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5febc330ac8e1c1c5b752055dea81bfea45ec178b4003dace7a78b00a9893f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsRule", [value]))

    @jsii.member(jsii_name="putDeleteRetentionPolicy")
    def put_delete_retention_policy(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        permanent_delete_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.
        :param permanent_delete_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#permanent_delete_enabled StorageAccount#permanent_delete_enabled}.
        '''
        value = StorageAccountBlobPropertiesDeleteRetentionPolicy(
            days=days, permanent_delete_enabled=permanent_delete_enabled
        )

        return typing.cast(None, jsii.invoke(self, "putDeleteRetentionPolicy", [value]))

    @jsii.member(jsii_name="putRestorePolicy")
    def put_restore_policy(self, *, days: jsii.Number) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.
        '''
        value = StorageAccountBlobPropertiesRestorePolicy(days=days)

        return typing.cast(None, jsii.invoke(self, "putRestorePolicy", [value]))

    @jsii.member(jsii_name="resetChangeFeedEnabled")
    def reset_change_feed_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeFeedEnabled", []))

    @jsii.member(jsii_name="resetChangeFeedRetentionInDays")
    def reset_change_feed_retention_in_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChangeFeedRetentionInDays", []))

    @jsii.member(jsii_name="resetContainerDeleteRetentionPolicy")
    def reset_container_delete_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerDeleteRetentionPolicy", []))

    @jsii.member(jsii_name="resetCorsRule")
    def reset_cors_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsRule", []))

    @jsii.member(jsii_name="resetDefaultServiceVersion")
    def reset_default_service_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultServiceVersion", []))

    @jsii.member(jsii_name="resetDeleteRetentionPolicy")
    def reset_delete_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteRetentionPolicy", []))

    @jsii.member(jsii_name="resetLastAccessTimeEnabled")
    def reset_last_access_time_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastAccessTimeEnabled", []))

    @jsii.member(jsii_name="resetRestorePolicy")
    def reset_restore_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestorePolicy", []))

    @jsii.member(jsii_name="resetVersioningEnabled")
    def reset_versioning_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersioningEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="containerDeleteRetentionPolicy")
    def container_delete_retention_policy(
        self,
    ) -> StorageAccountBlobPropertiesContainerDeleteRetentionPolicyOutputReference:
        return typing.cast(StorageAccountBlobPropertiesContainerDeleteRetentionPolicyOutputReference, jsii.get(self, "containerDeleteRetentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="corsRule")
    def cors_rule(self) -> StorageAccountBlobPropertiesCorsRuleList:
        return typing.cast(StorageAccountBlobPropertiesCorsRuleList, jsii.get(self, "corsRule"))

    @builtins.property
    @jsii.member(jsii_name="deleteRetentionPolicy")
    def delete_retention_policy(
        self,
    ) -> StorageAccountBlobPropertiesDeleteRetentionPolicyOutputReference:
        return typing.cast(StorageAccountBlobPropertiesDeleteRetentionPolicyOutputReference, jsii.get(self, "deleteRetentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="restorePolicy")
    def restore_policy(
        self,
    ) -> "StorageAccountBlobPropertiesRestorePolicyOutputReference":
        return typing.cast("StorageAccountBlobPropertiesRestorePolicyOutputReference", jsii.get(self, "restorePolicy"))

    @builtins.property
    @jsii.member(jsii_name="changeFeedEnabledInput")
    def change_feed_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "changeFeedEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="changeFeedRetentionInDaysInput")
    def change_feed_retention_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "changeFeedRetentionInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="containerDeleteRetentionPolicyInput")
    def container_delete_retention_policy_input(
        self,
    ) -> typing.Optional[StorageAccountBlobPropertiesContainerDeleteRetentionPolicy]:
        return typing.cast(typing.Optional[StorageAccountBlobPropertiesContainerDeleteRetentionPolicy], jsii.get(self, "containerDeleteRetentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="corsRuleInput")
    def cors_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountBlobPropertiesCorsRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountBlobPropertiesCorsRule]]], jsii.get(self, "corsRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultServiceVersionInput")
    def default_service_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultServiceVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteRetentionPolicyInput")
    def delete_retention_policy_input(
        self,
    ) -> typing.Optional[StorageAccountBlobPropertiesDeleteRetentionPolicy]:
        return typing.cast(typing.Optional[StorageAccountBlobPropertiesDeleteRetentionPolicy], jsii.get(self, "deleteRetentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="lastAccessTimeEnabledInput")
    def last_access_time_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "lastAccessTimeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="restorePolicyInput")
    def restore_policy_input(
        self,
    ) -> typing.Optional["StorageAccountBlobPropertiesRestorePolicy"]:
        return typing.cast(typing.Optional["StorageAccountBlobPropertiesRestorePolicy"], jsii.get(self, "restorePolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="versioningEnabledInput")
    def versioning_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "versioningEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="changeFeedEnabled")
    def change_feed_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "changeFeedEnabled"))

    @change_feed_enabled.setter
    def change_feed_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a108d090bf9d872c2ce5bbe6627051c2ce1c1809d56b0e539441f1c1bd4a8489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeFeedEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="changeFeedRetentionInDays")
    def change_feed_retention_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "changeFeedRetentionInDays"))

    @change_feed_retention_in_days.setter
    def change_feed_retention_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22efc201d63effc5b4707f6a50e8dd88b7daf5b7c4cd8746ea3460113acb3156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "changeFeedRetentionInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultServiceVersion")
    def default_service_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultServiceVersion"))

    @default_service_version.setter
    def default_service_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c85988f21a554479cbf09af01e72e356e0994632aae4a2048363d6a77faca13e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultServiceVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastAccessTimeEnabled")
    def last_access_time_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "lastAccessTimeEnabled"))

    @last_access_time_enabled.setter
    def last_access_time_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea5b3b356c44539bd67bed97fb5902253d344a2e7cb8317cc9f2a78ad8decea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastAccessTimeEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versioningEnabled")
    def versioning_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "versioningEnabled"))

    @versioning_enabled.setter
    def versioning_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9871ca0bcc47104970f278d5126b9593da3ea55a4bed45f093f89991e19148bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versioningEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountBlobProperties]:
        return typing.cast(typing.Optional[StorageAccountBlobProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountBlobProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac34cce493a79da5b50300a7a7cd1553fd61c21ed0531010c4006a82dff88a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesRestorePolicy",
    jsii_struct_bases=[],
    name_mapping={"days": "days"},
)
class StorageAccountBlobPropertiesRestorePolicy:
    def __init__(self, *, days: jsii.Number) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3ad12b229031e3afd9e04587bec6a930677921d9f11b394fcabbc201410d543)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days": days,
        }

    @builtins.property
    def days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.'''
        result = self._values.get("days")
        assert result is not None, "Required property 'days' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountBlobPropertiesRestorePolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountBlobPropertiesRestorePolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountBlobPropertiesRestorePolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__050d45d550aa2048af1c1a84f40cb3dbaf4b34c6304a82c5268c638c33856f1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98736747ace794951b0dffd9be584ebd1ba2bd14f87a5d9dd407b5c72798e77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountBlobPropertiesRestorePolicy]:
        return typing.cast(typing.Optional[StorageAccountBlobPropertiesRestorePolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountBlobPropertiesRestorePolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b483925f143a13fdb06c356a0cabb6d129f9acca8ed135610b81dce2892294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_replication_type": "accountReplicationType",
        "account_tier": "accountTier",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "access_tier": "accessTier",
        "account_kind": "accountKind",
        "allowed_copy_scope": "allowedCopyScope",
        "allow_nested_items_to_be_public": "allowNestedItemsToBePublic",
        "azure_files_authentication": "azureFilesAuthentication",
        "blob_properties": "blobProperties",
        "cross_tenant_replication_enabled": "crossTenantReplicationEnabled",
        "custom_domain": "customDomain",
        "customer_managed_key": "customerManagedKey",
        "default_to_oauth_authentication": "defaultToOauthAuthentication",
        "dns_endpoint_type": "dnsEndpointType",
        "edge_zone": "edgeZone",
        "https_traffic_only_enabled": "httpsTrafficOnlyEnabled",
        "id": "id",
        "identity": "identity",
        "immutability_policy": "immutabilityPolicy",
        "infrastructure_encryption_enabled": "infrastructureEncryptionEnabled",
        "is_hns_enabled": "isHnsEnabled",
        "large_file_share_enabled": "largeFileShareEnabled",
        "local_user_enabled": "localUserEnabled",
        "min_tls_version": "minTlsVersion",
        "network_rules": "networkRules",
        "nfsv3_enabled": "nfsv3Enabled",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "queue_encryption_key_type": "queueEncryptionKeyType",
        "queue_properties": "queueProperties",
        "routing": "routing",
        "sas_policy": "sasPolicy",
        "sftp_enabled": "sftpEnabled",
        "shared_access_key_enabled": "sharedAccessKeyEnabled",
        "share_properties": "shareProperties",
        "static_website": "staticWebsite",
        "table_encryption_key_type": "tableEncryptionKeyType",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class StorageAccountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_replication_type: builtins.str,
        account_tier: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        access_tier: typing.Optional[builtins.str] = None,
        account_kind: typing.Optional[builtins.str] = None,
        allowed_copy_scope: typing.Optional[builtins.str] = None,
        allow_nested_items_to_be_public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_files_authentication: typing.Optional[typing.Union[StorageAccountAzureFilesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
        blob_properties: typing.Optional[typing.Union[StorageAccountBlobProperties, typing.Dict[builtins.str, typing.Any]]] = None,
        cross_tenant_replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        custom_domain: typing.Optional[typing.Union["StorageAccountCustomDomain", typing.Dict[builtins.str, typing.Any]]] = None,
        customer_managed_key: typing.Optional[typing.Union["StorageAccountCustomerManagedKey", typing.Dict[builtins.str, typing.Any]]] = None,
        default_to_oauth_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        dns_endpoint_type: typing.Optional[builtins.str] = None,
        edge_zone: typing.Optional[builtins.str] = None,
        https_traffic_only_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["StorageAccountIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        immutability_policy: typing.Optional[typing.Union["StorageAccountImmutabilityPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_hns_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        large_file_share_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        local_user_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_tls_version: typing.Optional[builtins.str] = None,
        network_rules: typing.Optional[typing.Union["StorageAccountNetworkRules", typing.Dict[builtins.str, typing.Any]]] = None,
        nfsv3_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        queue_encryption_key_type: typing.Optional[builtins.str] = None,
        queue_properties: typing.Optional[typing.Union["StorageAccountQueueProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        routing: typing.Optional[typing.Union["StorageAccountRouting", typing.Dict[builtins.str, typing.Any]]] = None,
        sas_policy: typing.Optional[typing.Union["StorageAccountSasPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        sftp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_access_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        share_properties: typing.Optional[typing.Union["StorageAccountShareProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        static_website: typing.Optional[typing.Union["StorageAccountStaticWebsite", typing.Dict[builtins.str, typing.Any]]] = None,
        table_encryption_key_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["StorageAccountTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_replication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_replication_type StorageAccount#account_replication_type}.
        :param account_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_tier StorageAccount#account_tier}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#location StorageAccount#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#name StorageAccount#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#resource_group_name StorageAccount#resource_group_name}.
        :param access_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#access_tier StorageAccount#access_tier}.
        :param account_kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_kind StorageAccount#account_kind}.
        :param allowed_copy_scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_copy_scope StorageAccount#allowed_copy_scope}.
        :param allow_nested_items_to_be_public: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allow_nested_items_to_be_public StorageAccount#allow_nested_items_to_be_public}.
        :param azure_files_authentication: azure_files_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#azure_files_authentication StorageAccount#azure_files_authentication}
        :param blob_properties: blob_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#blob_properties StorageAccount#blob_properties}
        :param cross_tenant_replication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cross_tenant_replication_enabled StorageAccount#cross_tenant_replication_enabled}.
        :param custom_domain: custom_domain block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#custom_domain StorageAccount#custom_domain}
        :param customer_managed_key: customer_managed_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#customer_managed_key StorageAccount#customer_managed_key}
        :param default_to_oauth_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_to_oauth_authentication StorageAccount#default_to_oauth_authentication}.
        :param dns_endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#dns_endpoint_type StorageAccount#dns_endpoint_type}.
        :param edge_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#edge_zone StorageAccount#edge_zone}.
        :param https_traffic_only_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#https_traffic_only_enabled StorageAccount#https_traffic_only_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#id StorageAccount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#identity StorageAccount#identity}
        :param immutability_policy: immutability_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#immutability_policy StorageAccount#immutability_policy}
        :param infrastructure_encryption_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#infrastructure_encryption_enabled StorageAccount#infrastructure_encryption_enabled}.
        :param is_hns_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#is_hns_enabled StorageAccount#is_hns_enabled}.
        :param large_file_share_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#large_file_share_enabled StorageAccount#large_file_share_enabled}.
        :param local_user_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#local_user_enabled StorageAccount#local_user_enabled}.
        :param min_tls_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#min_tls_version StorageAccount#min_tls_version}.
        :param network_rules: network_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#network_rules StorageAccount#network_rules}
        :param nfsv3_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#nfsv3_enabled StorageAccount#nfsv3_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#public_network_access_enabled StorageAccount#public_network_access_enabled}.
        :param queue_encryption_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#queue_encryption_key_type StorageAccount#queue_encryption_key_type}.
        :param queue_properties: queue_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#queue_properties StorageAccount#queue_properties}
        :param routing: routing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#routing StorageAccount#routing}
        :param sas_policy: sas_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#sas_policy StorageAccount#sas_policy}
        :param sftp_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#sftp_enabled StorageAccount#sftp_enabled}.
        :param shared_access_key_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#shared_access_key_enabled StorageAccount#shared_access_key_enabled}.
        :param share_properties: share_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#share_properties StorageAccount#share_properties}
        :param static_website: static_website block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#static_website StorageAccount#static_website}
        :param table_encryption_key_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#table_encryption_key_type StorageAccount#table_encryption_key_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#tags StorageAccount#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#timeouts StorageAccount#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(azure_files_authentication, dict):
            azure_files_authentication = StorageAccountAzureFilesAuthentication(**azure_files_authentication)
        if isinstance(blob_properties, dict):
            blob_properties = StorageAccountBlobProperties(**blob_properties)
        if isinstance(custom_domain, dict):
            custom_domain = StorageAccountCustomDomain(**custom_domain)
        if isinstance(customer_managed_key, dict):
            customer_managed_key = StorageAccountCustomerManagedKey(**customer_managed_key)
        if isinstance(identity, dict):
            identity = StorageAccountIdentity(**identity)
        if isinstance(immutability_policy, dict):
            immutability_policy = StorageAccountImmutabilityPolicy(**immutability_policy)
        if isinstance(network_rules, dict):
            network_rules = StorageAccountNetworkRules(**network_rules)
        if isinstance(queue_properties, dict):
            queue_properties = StorageAccountQueueProperties(**queue_properties)
        if isinstance(routing, dict):
            routing = StorageAccountRouting(**routing)
        if isinstance(sas_policy, dict):
            sas_policy = StorageAccountSasPolicy(**sas_policy)
        if isinstance(share_properties, dict):
            share_properties = StorageAccountShareProperties(**share_properties)
        if isinstance(static_website, dict):
            static_website = StorageAccountStaticWebsite(**static_website)
        if isinstance(timeouts, dict):
            timeouts = StorageAccountTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64332c35e92aaa3ef7d040a7f09ecb59c7db234ca11aebf2b4c7362eb81b302b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_replication_type", value=account_replication_type, expected_type=type_hints["account_replication_type"])
            check_type(argname="argument account_tier", value=account_tier, expected_type=type_hints["account_tier"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument access_tier", value=access_tier, expected_type=type_hints["access_tier"])
            check_type(argname="argument account_kind", value=account_kind, expected_type=type_hints["account_kind"])
            check_type(argname="argument allowed_copy_scope", value=allowed_copy_scope, expected_type=type_hints["allowed_copy_scope"])
            check_type(argname="argument allow_nested_items_to_be_public", value=allow_nested_items_to_be_public, expected_type=type_hints["allow_nested_items_to_be_public"])
            check_type(argname="argument azure_files_authentication", value=azure_files_authentication, expected_type=type_hints["azure_files_authentication"])
            check_type(argname="argument blob_properties", value=blob_properties, expected_type=type_hints["blob_properties"])
            check_type(argname="argument cross_tenant_replication_enabled", value=cross_tenant_replication_enabled, expected_type=type_hints["cross_tenant_replication_enabled"])
            check_type(argname="argument custom_domain", value=custom_domain, expected_type=type_hints["custom_domain"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument default_to_oauth_authentication", value=default_to_oauth_authentication, expected_type=type_hints["default_to_oauth_authentication"])
            check_type(argname="argument dns_endpoint_type", value=dns_endpoint_type, expected_type=type_hints["dns_endpoint_type"])
            check_type(argname="argument edge_zone", value=edge_zone, expected_type=type_hints["edge_zone"])
            check_type(argname="argument https_traffic_only_enabled", value=https_traffic_only_enabled, expected_type=type_hints["https_traffic_only_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument immutability_policy", value=immutability_policy, expected_type=type_hints["immutability_policy"])
            check_type(argname="argument infrastructure_encryption_enabled", value=infrastructure_encryption_enabled, expected_type=type_hints["infrastructure_encryption_enabled"])
            check_type(argname="argument is_hns_enabled", value=is_hns_enabled, expected_type=type_hints["is_hns_enabled"])
            check_type(argname="argument large_file_share_enabled", value=large_file_share_enabled, expected_type=type_hints["large_file_share_enabled"])
            check_type(argname="argument local_user_enabled", value=local_user_enabled, expected_type=type_hints["local_user_enabled"])
            check_type(argname="argument min_tls_version", value=min_tls_version, expected_type=type_hints["min_tls_version"])
            check_type(argname="argument network_rules", value=network_rules, expected_type=type_hints["network_rules"])
            check_type(argname="argument nfsv3_enabled", value=nfsv3_enabled, expected_type=type_hints["nfsv3_enabled"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument queue_encryption_key_type", value=queue_encryption_key_type, expected_type=type_hints["queue_encryption_key_type"])
            check_type(argname="argument queue_properties", value=queue_properties, expected_type=type_hints["queue_properties"])
            check_type(argname="argument routing", value=routing, expected_type=type_hints["routing"])
            check_type(argname="argument sas_policy", value=sas_policy, expected_type=type_hints["sas_policy"])
            check_type(argname="argument sftp_enabled", value=sftp_enabled, expected_type=type_hints["sftp_enabled"])
            check_type(argname="argument shared_access_key_enabled", value=shared_access_key_enabled, expected_type=type_hints["shared_access_key_enabled"])
            check_type(argname="argument share_properties", value=share_properties, expected_type=type_hints["share_properties"])
            check_type(argname="argument static_website", value=static_website, expected_type=type_hints["static_website"])
            check_type(argname="argument table_encryption_key_type", value=table_encryption_key_type, expected_type=type_hints["table_encryption_key_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_replication_type": account_replication_type,
            "account_tier": account_tier,
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
        if access_tier is not None:
            self._values["access_tier"] = access_tier
        if account_kind is not None:
            self._values["account_kind"] = account_kind
        if allowed_copy_scope is not None:
            self._values["allowed_copy_scope"] = allowed_copy_scope
        if allow_nested_items_to_be_public is not None:
            self._values["allow_nested_items_to_be_public"] = allow_nested_items_to_be_public
        if azure_files_authentication is not None:
            self._values["azure_files_authentication"] = azure_files_authentication
        if blob_properties is not None:
            self._values["blob_properties"] = blob_properties
        if cross_tenant_replication_enabled is not None:
            self._values["cross_tenant_replication_enabled"] = cross_tenant_replication_enabled
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if default_to_oauth_authentication is not None:
            self._values["default_to_oauth_authentication"] = default_to_oauth_authentication
        if dns_endpoint_type is not None:
            self._values["dns_endpoint_type"] = dns_endpoint_type
        if edge_zone is not None:
            self._values["edge_zone"] = edge_zone
        if https_traffic_only_enabled is not None:
            self._values["https_traffic_only_enabled"] = https_traffic_only_enabled
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if immutability_policy is not None:
            self._values["immutability_policy"] = immutability_policy
        if infrastructure_encryption_enabled is not None:
            self._values["infrastructure_encryption_enabled"] = infrastructure_encryption_enabled
        if is_hns_enabled is not None:
            self._values["is_hns_enabled"] = is_hns_enabled
        if large_file_share_enabled is not None:
            self._values["large_file_share_enabled"] = large_file_share_enabled
        if local_user_enabled is not None:
            self._values["local_user_enabled"] = local_user_enabled
        if min_tls_version is not None:
            self._values["min_tls_version"] = min_tls_version
        if network_rules is not None:
            self._values["network_rules"] = network_rules
        if nfsv3_enabled is not None:
            self._values["nfsv3_enabled"] = nfsv3_enabled
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if queue_encryption_key_type is not None:
            self._values["queue_encryption_key_type"] = queue_encryption_key_type
        if queue_properties is not None:
            self._values["queue_properties"] = queue_properties
        if routing is not None:
            self._values["routing"] = routing
        if sas_policy is not None:
            self._values["sas_policy"] = sas_policy
        if sftp_enabled is not None:
            self._values["sftp_enabled"] = sftp_enabled
        if shared_access_key_enabled is not None:
            self._values["shared_access_key_enabled"] = shared_access_key_enabled
        if share_properties is not None:
            self._values["share_properties"] = share_properties
        if static_website is not None:
            self._values["static_website"] = static_website
        if table_encryption_key_type is not None:
            self._values["table_encryption_key_type"] = table_encryption_key_type
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
    def account_replication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_replication_type StorageAccount#account_replication_type}.'''
        result = self._values.get("account_replication_type")
        assert result is not None, "Required property 'account_replication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_tier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_tier StorageAccount#account_tier}.'''
        result = self._values.get("account_tier")
        assert result is not None, "Required property 'account_tier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#location StorageAccount#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#name StorageAccount#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#resource_group_name StorageAccount#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#access_tier StorageAccount#access_tier}.'''
        result = self._values.get("access_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_kind(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#account_kind StorageAccount#account_kind}.'''
        result = self._values.get("account_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_copy_scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_copy_scope StorageAccount#allowed_copy_scope}.'''
        result = self._values.get("allowed_copy_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_nested_items_to_be_public(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allow_nested_items_to_be_public StorageAccount#allow_nested_items_to_be_public}.'''
        result = self._values.get("allow_nested_items_to_be_public")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def azure_files_authentication(
        self,
    ) -> typing.Optional[StorageAccountAzureFilesAuthentication]:
        '''azure_files_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#azure_files_authentication StorageAccount#azure_files_authentication}
        '''
        result = self._values.get("azure_files_authentication")
        return typing.cast(typing.Optional[StorageAccountAzureFilesAuthentication], result)

    @builtins.property
    def blob_properties(self) -> typing.Optional[StorageAccountBlobProperties]:
        '''blob_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#blob_properties StorageAccount#blob_properties}
        '''
        result = self._values.get("blob_properties")
        return typing.cast(typing.Optional[StorageAccountBlobProperties], result)

    @builtins.property
    def cross_tenant_replication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cross_tenant_replication_enabled StorageAccount#cross_tenant_replication_enabled}.'''
        result = self._values.get("cross_tenant_replication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def custom_domain(self) -> typing.Optional["StorageAccountCustomDomain"]:
        '''custom_domain block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#custom_domain StorageAccount#custom_domain}
        '''
        result = self._values.get("custom_domain")
        return typing.cast(typing.Optional["StorageAccountCustomDomain"], result)

    @builtins.property
    def customer_managed_key(
        self,
    ) -> typing.Optional["StorageAccountCustomerManagedKey"]:
        '''customer_managed_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#customer_managed_key StorageAccount#customer_managed_key}
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional["StorageAccountCustomerManagedKey"], result)

    @builtins.property
    def default_to_oauth_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_to_oauth_authentication StorageAccount#default_to_oauth_authentication}.'''
        result = self._values.get("default_to_oauth_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def dns_endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#dns_endpoint_type StorageAccount#dns_endpoint_type}.'''
        result = self._values.get("dns_endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#edge_zone StorageAccount#edge_zone}.'''
        result = self._values.get("edge_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_traffic_only_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#https_traffic_only_enabled StorageAccount#https_traffic_only_enabled}.'''
        result = self._values.get("https_traffic_only_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#id StorageAccount#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["StorageAccountIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#identity StorageAccount#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["StorageAccountIdentity"], result)

    @builtins.property
    def immutability_policy(
        self,
    ) -> typing.Optional["StorageAccountImmutabilityPolicy"]:
        '''immutability_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#immutability_policy StorageAccount#immutability_policy}
        '''
        result = self._values.get("immutability_policy")
        return typing.cast(typing.Optional["StorageAccountImmutabilityPolicy"], result)

    @builtins.property
    def infrastructure_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#infrastructure_encryption_enabled StorageAccount#infrastructure_encryption_enabled}.'''
        result = self._values.get("infrastructure_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_hns_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#is_hns_enabled StorageAccount#is_hns_enabled}.'''
        result = self._values.get("is_hns_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def large_file_share_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#large_file_share_enabled StorageAccount#large_file_share_enabled}.'''
        result = self._values.get("large_file_share_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def local_user_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#local_user_enabled StorageAccount#local_user_enabled}.'''
        result = self._values.get("local_user_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def min_tls_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#min_tls_version StorageAccount#min_tls_version}.'''
        result = self._values.get("min_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_rules(self) -> typing.Optional["StorageAccountNetworkRules"]:
        '''network_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#network_rules StorageAccount#network_rules}
        '''
        result = self._values.get("network_rules")
        return typing.cast(typing.Optional["StorageAccountNetworkRules"], result)

    @builtins.property
    def nfsv3_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#nfsv3_enabled StorageAccount#nfsv3_enabled}.'''
        result = self._values.get("nfsv3_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#public_network_access_enabled StorageAccount#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def queue_encryption_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#queue_encryption_key_type StorageAccount#queue_encryption_key_type}.'''
        result = self._values.get("queue_encryption_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_properties(self) -> typing.Optional["StorageAccountQueueProperties"]:
        '''queue_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#queue_properties StorageAccount#queue_properties}
        '''
        result = self._values.get("queue_properties")
        return typing.cast(typing.Optional["StorageAccountQueueProperties"], result)

    @builtins.property
    def routing(self) -> typing.Optional["StorageAccountRouting"]:
        '''routing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#routing StorageAccount#routing}
        '''
        result = self._values.get("routing")
        return typing.cast(typing.Optional["StorageAccountRouting"], result)

    @builtins.property
    def sas_policy(self) -> typing.Optional["StorageAccountSasPolicy"]:
        '''sas_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#sas_policy StorageAccount#sas_policy}
        '''
        result = self._values.get("sas_policy")
        return typing.cast(typing.Optional["StorageAccountSasPolicy"], result)

    @builtins.property
    def sftp_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#sftp_enabled StorageAccount#sftp_enabled}.'''
        result = self._values.get("sftp_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def shared_access_key_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#shared_access_key_enabled StorageAccount#shared_access_key_enabled}.'''
        result = self._values.get("shared_access_key_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def share_properties(self) -> typing.Optional["StorageAccountShareProperties"]:
        '''share_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#share_properties StorageAccount#share_properties}
        '''
        result = self._values.get("share_properties")
        return typing.cast(typing.Optional["StorageAccountShareProperties"], result)

    @builtins.property
    def static_website(self) -> typing.Optional["StorageAccountStaticWebsite"]:
        '''static_website block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#static_website StorageAccount#static_website}
        '''
        result = self._values.get("static_website")
        return typing.cast(typing.Optional["StorageAccountStaticWebsite"], result)

    @builtins.property
    def table_encryption_key_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#table_encryption_key_type StorageAccount#table_encryption_key_type}.'''
        result = self._values.get("table_encryption_key_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#tags StorageAccount#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["StorageAccountTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#timeouts StorageAccount#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["StorageAccountTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountCustomDomain",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "use_subdomain": "useSubdomain"},
)
class StorageAccountCustomDomain:
    def __init__(
        self,
        *,
        name: builtins.str,
        use_subdomain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#name StorageAccount#name}.
        :param use_subdomain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#use_subdomain StorageAccount#use_subdomain}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b927d48374e4b062fc040462e52f3ce85dc699f5e28158a4c0b5be88bc1d8ff)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument use_subdomain", value=use_subdomain, expected_type=type_hints["use_subdomain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if use_subdomain is not None:
            self._values["use_subdomain"] = use_subdomain

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#name StorageAccount#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_subdomain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#use_subdomain StorageAccount#use_subdomain}.'''
        result = self._values.get("use_subdomain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountCustomDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountCustomDomainOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountCustomDomainOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__777d5836ce7dc85d992587167b0b73e3c8ae8050fecca9c8c444f953dd06ed78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUseSubdomain")
    def reset_use_subdomain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseSubdomain", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="useSubdomainInput")
    def use_subdomain_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useSubdomainInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d91b1257c4c592afb6017165f5c983a7d540165a72df133532bef49defddf0ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useSubdomain")
    def use_subdomain(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useSubdomain"))

    @use_subdomain.setter
    def use_subdomain(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70d6b04da900d2d6ad208fc42a7b00c3ad52db5a455517706a2da5e2ebeb0a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useSubdomain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountCustomDomain]:
        return typing.cast(typing.Optional[StorageAccountCustomDomain], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountCustomDomain],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae32e526ed79a3250b460355170428252a28a08c8d6a6fd253127fbb789175d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountCustomerManagedKey",
    jsii_struct_bases=[],
    name_mapping={
        "user_assigned_identity_id": "userAssignedIdentityId",
        "key_vault_key_id": "keyVaultKeyId",
        "managed_hsm_key_id": "managedHsmKeyId",
    },
)
class StorageAccountCustomerManagedKey:
    def __init__(
        self,
        *,
        user_assigned_identity_id: builtins.str,
        key_vault_key_id: typing.Optional[builtins.str] = None,
        managed_hsm_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#user_assigned_identity_id StorageAccount#user_assigned_identity_id}.
        :param key_vault_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#key_vault_key_id StorageAccount#key_vault_key_id}.
        :param managed_hsm_key_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#managed_hsm_key_id StorageAccount#managed_hsm_key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718e82b00304ac54b807d4f54feba5f29c9ba241d86dcffbd8b437b68dba04bb)
            check_type(argname="argument user_assigned_identity_id", value=user_assigned_identity_id, expected_type=type_hints["user_assigned_identity_id"])
            check_type(argname="argument key_vault_key_id", value=key_vault_key_id, expected_type=type_hints["key_vault_key_id"])
            check_type(argname="argument managed_hsm_key_id", value=managed_hsm_key_id, expected_type=type_hints["managed_hsm_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_assigned_identity_id": user_assigned_identity_id,
        }
        if key_vault_key_id is not None:
            self._values["key_vault_key_id"] = key_vault_key_id
        if managed_hsm_key_id is not None:
            self._values["managed_hsm_key_id"] = managed_hsm_key_id

    @builtins.property
    def user_assigned_identity_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#user_assigned_identity_id StorageAccount#user_assigned_identity_id}.'''
        result = self._values.get("user_assigned_identity_id")
        assert result is not None, "Required property 'user_assigned_identity_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_vault_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#key_vault_key_id StorageAccount#key_vault_key_id}.'''
        result = self._values.get("key_vault_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_hsm_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#managed_hsm_key_id StorageAccount#managed_hsm_key_id}.'''
        result = self._values.get("managed_hsm_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountCustomerManagedKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountCustomerManagedKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountCustomerManagedKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f0f3cd022cbe04d1b57ccee45243ae3ddaf74a80635d47200121ad3b2d334c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyVaultKeyId")
    def reset_key_vault_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultKeyId", []))

    @jsii.member(jsii_name="resetManagedHsmKeyId")
    def reset_managed_hsm_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedHsmKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyIdInput")
    def key_vault_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="managedHsmKeyIdInput")
    def managed_hsm_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedHsmKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityIdInput")
    def user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultKeyId")
    def key_vault_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultKeyId"))

    @key_vault_key_id.setter
    def key_vault_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5203faed2015cffe88a5b73ca202fc61e88ac7a949e3acea4ed05a4c6b8d87e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedHsmKeyId")
    def managed_hsm_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedHsmKeyId"))

    @managed_hsm_key_id.setter
    def managed_hsm_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a1e0678a41ffc74665c1080d136afe17607bf2c2de5ca1e0d9909b69bd924a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedHsmKeyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a81d3c4cc62a41f65dd472ac22592aec2033260e3842f02d8c512a0f083567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountCustomerManagedKey]:
        return typing.cast(typing.Optional[StorageAccountCustomerManagedKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountCustomerManagedKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4a24cbdb8dc44ca977268b666874e2cb83668c1cef117c6b2ee3ab3e4edac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class StorageAccountIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#type StorageAccount#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#identity_ids StorageAccount#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8f459717de58a7b8c5d708614af039b7675bb2bb96411c8a0ff0dde14dc427)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#type StorageAccount#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#identity_ids StorageAccount#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f72851fe35a5e86c8194b947d69d76bf6751ff4613b99970057d4c4c470504c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__572014204a2a080f7994792c927b836859f39ec7c284ee5a2f8f63bb97e9e61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3f0e87b0d99d6b9dab94943e1f90633a25d4cd812423819914efeaa8494a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountIdentity]:
        return typing.cast(typing.Optional[StorageAccountIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageAccountIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e1d759e097c7a8ac73fe4c39da1dd0866fc81f3dc982966e82c7bc09a12787)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountImmutabilityPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allow_protected_append_writes": "allowProtectedAppendWrites",
        "period_since_creation_in_days": "periodSinceCreationInDays",
        "state": "state",
    },
)
class StorageAccountImmutabilityPolicy:
    def __init__(
        self,
        *,
        allow_protected_append_writes: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        period_since_creation_in_days: jsii.Number,
        state: builtins.str,
    ) -> None:
        '''
        :param allow_protected_append_writes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allow_protected_append_writes StorageAccount#allow_protected_append_writes}.
        :param period_since_creation_in_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#period_since_creation_in_days StorageAccount#period_since_creation_in_days}.
        :param state: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#state StorageAccount#state}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bb5691a2bcbf4273cf02e7ebdaee6410534bd170bc7a6a57de81925bfdefd65)
            check_type(argname="argument allow_protected_append_writes", value=allow_protected_append_writes, expected_type=type_hints["allow_protected_append_writes"])
            check_type(argname="argument period_since_creation_in_days", value=period_since_creation_in_days, expected_type=type_hints["period_since_creation_in_days"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_protected_append_writes": allow_protected_append_writes,
            "period_since_creation_in_days": period_since_creation_in_days,
            "state": state,
        }

    @builtins.property
    def allow_protected_append_writes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allow_protected_append_writes StorageAccount#allow_protected_append_writes}.'''
        result = self._values.get("allow_protected_append_writes")
        assert result is not None, "Required property 'allow_protected_append_writes' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def period_since_creation_in_days(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#period_since_creation_in_days StorageAccount#period_since_creation_in_days}.'''
        result = self._values.get("period_since_creation_in_days")
        assert result is not None, "Required property 'period_since_creation_in_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#state StorageAccount#state}.'''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountImmutabilityPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountImmutabilityPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountImmutabilityPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__721f37dce983f02666ab5d2c5e7104917532ee5ca346169dff69db0001ebef31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowProtectedAppendWritesInput")
    def allow_protected_append_writes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowProtectedAppendWritesInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSinceCreationInDaysInput")
    def period_since_creation_in_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSinceCreationInDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="allowProtectedAppendWrites")
    def allow_protected_append_writes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowProtectedAppendWrites"))

    @allow_protected_append_writes.setter
    def allow_protected_append_writes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff90c53adc789c7b9c7521cecb40cd21216b95b4a819facc76273e0ab23a440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowProtectedAppendWrites", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSinceCreationInDays")
    def period_since_creation_in_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSinceCreationInDays"))

    @period_since_creation_in_days.setter
    def period_since_creation_in_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b80bf0dcefbd9881b60fd22b94d0027866a46c2746061d0e43b706327b3c178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSinceCreationInDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3d67b5d4b5618f855e29ddb9228fa1f2e12cb55548e31b31357d44ea7bdd383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountImmutabilityPolicy]:
        return typing.cast(typing.Optional[StorageAccountImmutabilityPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountImmutabilityPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d780a5166e5e59a9aed226ebb7ddfbd2eeca9edc8f91dd9982abcec3c4c84db0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountNetworkRules",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "bypass": "bypass",
        "ip_rules": "ipRules",
        "private_link_access": "privateLinkAccess",
        "virtual_network_subnet_ids": "virtualNetworkSubnetIds",
    },
)
class StorageAccountNetworkRules:
    def __init__(
        self,
        *,
        default_action: builtins.str,
        bypass: typing.Optional[typing.Sequence[builtins.str]] = None,
        ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        private_link_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountNetworkRulesPrivateLinkAccess", typing.Dict[builtins.str, typing.Any]]]]] = None,
        virtual_network_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_action StorageAccount#default_action}.
        :param bypass: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#bypass StorageAccount#bypass}.
        :param ip_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#ip_rules StorageAccount#ip_rules}.
        :param private_link_access: private_link_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#private_link_access StorageAccount#private_link_access}
        :param virtual_network_subnet_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#virtual_network_subnet_ids StorageAccount#virtual_network_subnet_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7289f51993ff24b0f732378607ced170c4b67b1c6a755ad347ed3b2edc08d6b3)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument bypass", value=bypass, expected_type=type_hints["bypass"])
            check_type(argname="argument ip_rules", value=ip_rules, expected_type=type_hints["ip_rules"])
            check_type(argname="argument private_link_access", value=private_link_access, expected_type=type_hints["private_link_access"])
            check_type(argname="argument virtual_network_subnet_ids", value=virtual_network_subnet_ids, expected_type=type_hints["virtual_network_subnet_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
        }
        if bypass is not None:
            self._values["bypass"] = bypass
        if ip_rules is not None:
            self._values["ip_rules"] = ip_rules
        if private_link_access is not None:
            self._values["private_link_access"] = private_link_access
        if virtual_network_subnet_ids is not None:
            self._values["virtual_network_subnet_ids"] = virtual_network_subnet_ids

    @builtins.property
    def default_action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#default_action StorageAccount#default_action}.'''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bypass(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#bypass StorageAccount#bypass}.'''
        result = self._values.get("bypass")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ip_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#ip_rules StorageAccount#ip_rules}.'''
        result = self._values.get("ip_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def private_link_access(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountNetworkRulesPrivateLinkAccess"]]]:
        '''private_link_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#private_link_access StorageAccount#private_link_access}
        '''
        result = self._values.get("private_link_access")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountNetworkRulesPrivateLinkAccess"]]], result)

    @builtins.property
    def virtual_network_subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#virtual_network_subnet_ids StorageAccount#virtual_network_subnet_ids}.'''
        result = self._values.get("virtual_network_subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountNetworkRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountNetworkRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountNetworkRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e07449092563cf5d9eef19965f152fc57e8912665032e009d86c25c335a5bb80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPrivateLinkAccess")
    def put_private_link_access(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountNetworkRulesPrivateLinkAccess", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8214af41ee890d6b679749b47b80a0a63b55eea999c4e473574588f15ca0563d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrivateLinkAccess", [value]))

    @jsii.member(jsii_name="resetBypass")
    def reset_bypass(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBypass", []))

    @jsii.member(jsii_name="resetIpRules")
    def reset_ip_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRules", []))

    @jsii.member(jsii_name="resetPrivateLinkAccess")
    def reset_private_link_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateLinkAccess", []))

    @jsii.member(jsii_name="resetVirtualNetworkSubnetIds")
    def reset_virtual_network_subnet_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkSubnetIds", []))

    @builtins.property
    @jsii.member(jsii_name="privateLinkAccess")
    def private_link_access(self) -> "StorageAccountNetworkRulesPrivateLinkAccessList":
        return typing.cast("StorageAccountNetworkRulesPrivateLinkAccessList", jsii.get(self, "privateLinkAccess"))

    @builtins.property
    @jsii.member(jsii_name="bypassInput")
    def bypass_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bypassInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionInput")
    def default_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRulesInput")
    def ip_rules_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="privateLinkAccessInput")
    def private_link_access_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountNetworkRulesPrivateLinkAccess"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountNetworkRulesPrivateLinkAccess"]]], jsii.get(self, "privateLinkAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIdsInput")
    def virtual_network_subnet_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "virtualNetworkSubnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="bypass")
    def bypass(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "bypass"))

    @bypass.setter
    def bypass(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2aff5217862600fd6d1df426d585b1cce67075635d73792af9d5f93331cdbb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bypass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultAction")
    def default_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f11feb3470d8af7405c5fb5847bc4da18d6f6cbfe76407c559ba7b9b8cb7f5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipRules")
    def ip_rules(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipRules"))

    @ip_rules.setter
    def ip_rules(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f53de50d70f4db3c042799103f61cbca98c93f1bfa16ad08f78b3a71a7b88f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIds")
    def virtual_network_subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "virtualNetworkSubnetIds"))

    @virtual_network_subnet_ids.setter
    def virtual_network_subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6977dfabf365ecf31a9f9e586b779d27c0171890942c3e052b14b273acbbe0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountNetworkRules]:
        return typing.cast(typing.Optional[StorageAccountNetworkRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountNetworkRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aaeb4bfb5eefe8fa3af00f67745774dc739a916ff62247795604249de5f9ce4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountNetworkRulesPrivateLinkAccess",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_resource_id": "endpointResourceId",
        "endpoint_tenant_id": "endpointTenantId",
    },
)
class StorageAccountNetworkRulesPrivateLinkAccess:
    def __init__(
        self,
        *,
        endpoint_resource_id: builtins.str,
        endpoint_tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#endpoint_resource_id StorageAccount#endpoint_resource_id}.
        :param endpoint_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#endpoint_tenant_id StorageAccount#endpoint_tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8629c9fcb9e793471227143c3ba3f3eda3e5782f6b586ea249d3ad7e08e309c7)
            check_type(argname="argument endpoint_resource_id", value=endpoint_resource_id, expected_type=type_hints["endpoint_resource_id"])
            check_type(argname="argument endpoint_tenant_id", value=endpoint_tenant_id, expected_type=type_hints["endpoint_tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_resource_id": endpoint_resource_id,
        }
        if endpoint_tenant_id is not None:
            self._values["endpoint_tenant_id"] = endpoint_tenant_id

    @builtins.property
    def endpoint_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#endpoint_resource_id StorageAccount#endpoint_resource_id}.'''
        result = self._values.get("endpoint_resource_id")
        assert result is not None, "Required property 'endpoint_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#endpoint_tenant_id StorageAccount#endpoint_tenant_id}.'''
        result = self._values.get("endpoint_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountNetworkRulesPrivateLinkAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountNetworkRulesPrivateLinkAccessList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountNetworkRulesPrivateLinkAccessList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5e16045fb82eb0b21dc538c8f032bc9b911aa40f8b28d8dcf623f121298c5c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageAccountNetworkRulesPrivateLinkAccessOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eeb4361a708cf93ef42f0fe13f763804031e16111b530ad103d915b24e64fbf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageAccountNetworkRulesPrivateLinkAccessOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae584df620903bddba3d8588ed5ada5924191353fdf0eb5df2281e7c1ef5927d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58490d7237a1307a88c2a6ee14a3152267b3b280d47257604d4c66642816f099)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31fab904cc82fdcfab3c3953fde07729c1b1b964107997a878d8b97ee3a95d13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountNetworkRulesPrivateLinkAccess]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountNetworkRulesPrivateLinkAccess]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountNetworkRulesPrivateLinkAccess]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4643a6f62d2d5818edcd41ff52359c176e96934839df8a8d77f75144824b5518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountNetworkRulesPrivateLinkAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountNetworkRulesPrivateLinkAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e6eb46b80b234a76f3e4522fa741d05d791600af0e88379bd7f83b526072354)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEndpointTenantId")
    def reset_endpoint_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointTenantId", []))

    @builtins.property
    @jsii.member(jsii_name="endpointResourceIdInput")
    def endpoint_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointTenantIdInput")
    def endpoint_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointResourceId")
    def endpoint_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointResourceId"))

    @endpoint_resource_id.setter
    def endpoint_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fcdc0916256ccaaa70578fa6f371909cb7c89766c7dba2c1f99568afe8dcf8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpointTenantId")
    def endpoint_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointTenantId"))

    @endpoint_tenant_id.setter
    def endpoint_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25bd3669e55f4c431faf5e56910098de305534c45470c2b5704028ecf2defc0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountNetworkRulesPrivateLinkAccess]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountNetworkRulesPrivateLinkAccess]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountNetworkRulesPrivateLinkAccess]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f92f1a7230b68243f748534085d478cbef2ffb74887660d4a38ffd3e84f1880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueueProperties",
    jsii_struct_bases=[],
    name_mapping={
        "cors_rule": "corsRule",
        "hour_metrics": "hourMetrics",
        "logging": "logging",
        "minute_metrics": "minuteMetrics",
    },
)
class StorageAccountQueueProperties:
    def __init__(
        self,
        *,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountQueuePropertiesCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        hour_metrics: typing.Optional[typing.Union["StorageAccountQueuePropertiesHourMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[typing.Union["StorageAccountQueuePropertiesLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        minute_metrics: typing.Optional[typing.Union["StorageAccountQueuePropertiesMinuteMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        :param hour_metrics: hour_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#hour_metrics StorageAccount#hour_metrics}
        :param logging: logging block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#logging StorageAccount#logging}
        :param minute_metrics: minute_metrics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#minute_metrics StorageAccount#minute_metrics}
        '''
        if isinstance(hour_metrics, dict):
            hour_metrics = StorageAccountQueuePropertiesHourMetrics(**hour_metrics)
        if isinstance(logging, dict):
            logging = StorageAccountQueuePropertiesLogging(**logging)
        if isinstance(minute_metrics, dict):
            minute_metrics = StorageAccountQueuePropertiesMinuteMetrics(**minute_metrics)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c304b5e9c8da5f2db7919f7d699ffe59fcbb5ce5f917b2eae6c28e52465dc54)
            check_type(argname="argument cors_rule", value=cors_rule, expected_type=type_hints["cors_rule"])
            check_type(argname="argument hour_metrics", value=hour_metrics, expected_type=type_hints["hour_metrics"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument minute_metrics", value=minute_metrics, expected_type=type_hints["minute_metrics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cors_rule is not None:
            self._values["cors_rule"] = cors_rule
        if hour_metrics is not None:
            self._values["hour_metrics"] = hour_metrics
        if logging is not None:
            self._values["logging"] = logging
        if minute_metrics is not None:
            self._values["minute_metrics"] = minute_metrics

    @builtins.property
    def cors_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountQueuePropertiesCorsRule"]]]:
        '''cors_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        '''
        result = self._values.get("cors_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountQueuePropertiesCorsRule"]]], result)

    @builtins.property
    def hour_metrics(
        self,
    ) -> typing.Optional["StorageAccountQueuePropertiesHourMetrics"]:
        '''hour_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#hour_metrics StorageAccount#hour_metrics}
        '''
        result = self._values.get("hour_metrics")
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesHourMetrics"], result)

    @builtins.property
    def logging(self) -> typing.Optional["StorageAccountQueuePropertiesLogging"]:
        '''logging block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#logging StorageAccount#logging}
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesLogging"], result)

    @builtins.property
    def minute_metrics(
        self,
    ) -> typing.Optional["StorageAccountQueuePropertiesMinuteMetrics"]:
        '''minute_metrics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#minute_metrics StorageAccount#minute_metrics}
        '''
        result = self._values.get("minute_metrics")
        return typing.cast(typing.Optional["StorageAccountQueuePropertiesMinuteMetrics"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueueProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesCorsRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "exposed_headers": "exposedHeaders",
        "max_age_in_seconds": "maxAgeInSeconds",
    },
)
class StorageAccountQueuePropertiesCorsRule:
    def __init__(
        self,
        *,
        allowed_headers: typing.Sequence[builtins.str],
        allowed_methods: typing.Sequence[builtins.str],
        allowed_origins: typing.Sequence[builtins.str],
        exposed_headers: typing.Sequence[builtins.str],
        max_age_in_seconds: jsii.Number,
    ) -> None:
        '''
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_headers StorageAccount#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_methods StorageAccount#allowed_methods}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_origins StorageAccount#allowed_origins}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#exposed_headers StorageAccount#exposed_headers}.
        :param max_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#max_age_in_seconds StorageAccount#max_age_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba792e58dec5020224c628b61e94c3d9c8c2c4a4e2968ccd0971479a04a78680)
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument exposed_headers", value=exposed_headers, expected_type=type_hints["exposed_headers"])
            check_type(argname="argument max_age_in_seconds", value=max_age_in_seconds, expected_type=type_hints["max_age_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_headers": allowed_headers,
            "allowed_methods": allowed_methods,
            "allowed_origins": allowed_origins,
            "exposed_headers": exposed_headers,
            "max_age_in_seconds": max_age_in_seconds,
        }

    @builtins.property
    def allowed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_headers StorageAccount#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        assert result is not None, "Required property 'allowed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_methods StorageAccount#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_origins StorageAccount#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def exposed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#exposed_headers StorageAccount#exposed_headers}.'''
        result = self._values.get("exposed_headers")
        assert result is not None, "Required property 'exposed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def max_age_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#max_age_in_seconds StorageAccount#max_age_in_seconds}.'''
        result = self._values.get("max_age_in_seconds")
        assert result is not None, "Required property 'max_age_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesCorsRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesCorsRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesCorsRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__710fe092bc3dc8692c226f3c691e8085a640b25590b3699f9d74c11c8cc3c171)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageAccountQueuePropertiesCorsRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1d37f884a7b8cd851dc1d75b48f378cd11aa7746e2c3d58fe0dee5372deefe)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageAccountQueuePropertiesCorsRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d536019c4148eba404308e206b29bc269bd9a02cc2b338a5c257cf4869ffc9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94544a8dcc5552e214fa236cacf684f667da504436c487d3202a27991d4d1d9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3c5b76f9a18dc6874d5d730314c1cb91798e61d321214f7a25fdef4042324ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4a85ce99e286a7c5b27a11076eeba6a68874750763195973e67c00b6cb85d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountQueuePropertiesCorsRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesCorsRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__786839df518e50783f79262fff6a6c873d5ea9d2e4cdbac7650911d50f05922d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposedHeadersInput")
    def exposed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSecondsInput")
    def max_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04d6a148601eb3b26e20ed10aa39d368b24217e58e2a9f0042d5870ce1c018e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af92a964fbe492612c55659ff5eb023a78fdb2cf19404980033eb5d33db61ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3b27a84eac06d3f00fb14d4e98dfaedc9c6eac72266e2e81cb6c51bb38d225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposedHeaders")
    def exposed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposedHeaders"))

    @exposed_headers.setter
    def exposed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34615fdf56ddd5448977d8921cc23450e1c38149160135f4f52614dc6d515a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSeconds")
    def max_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeInSeconds"))

    @max_age_in_seconds.setter
    def max_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dbddd3c80639ec5230954b5dcf7f4ecce4c9e358808377ee538e4cce349d28e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesCorsRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesCorsRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesCorsRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5be8f567c83a5840158e229f410959981e8e284b1d42c13db077bd4e282e84a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesHourMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "version": "version",
        "include_apis": "includeApis",
        "retention_policy_days": "retentionPolicyDays",
    },
)
class StorageAccountQueuePropertiesHourMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#enabled StorageAccount#enabled}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.
        :param include_apis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#include_apis StorageAccount#include_apis}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa121c1310abed15c2f59f539705402dcd70e1552726a2b03a195fad9bbed07)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument include_apis", value=include_apis, expected_type=type_hints["include_apis"])
            check_type(argname="argument retention_policy_days", value=retention_policy_days, expected_type=type_hints["retention_policy_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "version": version,
        }
        if include_apis is not None:
            self._values["include_apis"] = include_apis
        if retention_policy_days is not None:
            self._values["retention_policy_days"] = retention_policy_days

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#enabled StorageAccount#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_apis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#include_apis StorageAccount#include_apis}.'''
        result = self._values.get("include_apis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_policy_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.'''
        result = self._values.get("retention_policy_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesHourMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesHourMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesHourMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__191ba63d344e1a0850211d5e4164b3379cc9ebea229fda8ed84165b1d0152e0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeApis")
    def reset_include_apis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeApis", []))

    @jsii.member(jsii_name="resetRetentionPolicyDays")
    def reset_retention_policy_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicyDays", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="includeApisInput")
    def include_apis_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeApisInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDaysInput")
    def retention_policy_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPolicyDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4ae4f2a99b4e854af0918b9fb6d573f4a2cc5baaa17b6def529138d2934bc18b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeApis")
    def include_apis(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeApis"))

    @include_apis.setter
    def include_apis(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c26e4cc72505e9d2a2864b5a5878cedd95e9bba1e9fe078e320e67d7179fe16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeApis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDays")
    def retention_policy_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPolicyDays"))

    @retention_policy_days.setter
    def retention_policy_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785a51da8a33fff693fa612aa23df2d9467613c84b88ab76af25a1e7d42f21a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicyDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9759e648036a27d0dc52c4473580b8cf36be8b8d990cb355f984d9d53f645d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountQueuePropertiesHourMetrics]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesHourMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountQueuePropertiesHourMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4bbd2bd2747eda3d11965ba25948f99f7c8259e88a1436e70d791d55f521d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesLogging",
    jsii_struct_bases=[],
    name_mapping={
        "delete": "delete",
        "read": "read",
        "version": "version",
        "write": "write",
        "retention_policy_days": "retentionPolicyDays",
    },
)
class StorageAccountQueuePropertiesLogging:
    def __init__(
        self,
        *,
        delete: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        read: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        write: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete StorageAccount#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#read StorageAccount#read}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.
        :param write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#write StorageAccount#write}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e60fb75d325712510ce02e66e680fabe3db37683108491f0deab18cd8d7c6dab)
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument write", value=write, expected_type=type_hints["write"])
            check_type(argname="argument retention_policy_days", value=retention_policy_days, expected_type=type_hints["retention_policy_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delete": delete,
            "read": read,
            "version": version,
            "write": write,
        }
        if retention_policy_days is not None:
            self._values["retention_policy_days"] = retention_policy_days

    @builtins.property
    def delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete StorageAccount#delete}.'''
        result = self._values.get("delete")
        assert result is not None, "Required property 'delete' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def read(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#read StorageAccount#read}.'''
        result = self._values.get("read")
        assert result is not None, "Required property 'read' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def write(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#write StorageAccount#write}.'''
        result = self._values.get("write")
        assert result is not None, "Required property 'write' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def retention_policy_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.'''
        result = self._values.get("retention_policy_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesLoggingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesLoggingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f601abb412602e09ab3c666b5231aea70c092133ba68d276b21112dd72057a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRetentionPolicyDays")
    def reset_retention_policy_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicyDays", []))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDaysInput")
    def retention_policy_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPolicyDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="writeInput")
    def write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "writeInput"))

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "delete"))

    @delete.setter
    def delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a88dbd83510f6841074f83f53816a25db1dba64c66505e11462b75d7a92aea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "read"))

    @read.setter
    def read(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd2919f02944b80d5156ce6004350c9326ddc4b853bfb42714275678bfb7e3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDays")
    def retention_policy_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPolicyDays"))

    @retention_policy_days.setter
    def retention_policy_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c90a81a70e38fb2aaf42bda343e9128b7edb279c7d0bde6b0b3935dae6b7ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicyDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ad0c0eb97d798879c3656328aa4e051ecdd44bd0b20bf3db3e072d4664755e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="write")
    def write(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "write"))

    @write.setter
    def write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca50b73f50862640aa5830635c8bb3ebc061135fd67ca09828d2a20474e22ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "write", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountQueuePropertiesLogging]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesLogging], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountQueuePropertiesLogging],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a382e38d91c5149862a21cb6cd13157a538ad974c8110a3d69313993a6f578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesMinuteMetrics",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "version": "version",
        "include_apis": "includeApis",
        "retention_policy_days": "retentionPolicyDays",
    },
)
class StorageAccountQueuePropertiesMinuteMetrics:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#enabled StorageAccount#enabled}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.
        :param include_apis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#include_apis StorageAccount#include_apis}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b35d0581f123411c1f92a3de9aff782644ff616c30663cf222f770e0685edb33)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument include_apis", value=include_apis, expected_type=type_hints["include_apis"])
            check_type(argname="argument retention_policy_days", value=retention_policy_days, expected_type=type_hints["retention_policy_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "version": version,
        }
        if include_apis is not None:
            self._values["include_apis"] = include_apis
        if retention_policy_days is not None:
            self._values["retention_policy_days"] = retention_policy_days

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#enabled StorageAccount#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_apis(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#include_apis StorageAccount#include_apis}.'''
        result = self._values.get("include_apis")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_policy_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.'''
        result = self._values.get("retention_policy_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountQueuePropertiesMinuteMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountQueuePropertiesMinuteMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesMinuteMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b5e66a1665c57385bfe5b15a214621641b12083d6f8a65e883d39f7596251e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludeApis")
    def reset_include_apis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeApis", []))

    @jsii.member(jsii_name="resetRetentionPolicyDays")
    def reset_retention_policy_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicyDays", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="includeApisInput")
    def include_apis_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeApisInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDaysInput")
    def retention_policy_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPolicyDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c71727971972446567a6237b12d8ad9f49bf80f279cd3382f70fba2440851098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeApis")
    def include_apis(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeApis"))

    @include_apis.setter
    def include_apis(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ed404899a9c9009f02298dbfe94c71ee031546629cc82e2d384cc24f729bb29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeApis", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyDays")
    def retention_policy_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPolicyDays"))

    @retention_policy_days.setter
    def retention_policy_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f2afcfa892682396e72d9d70cf0a032a14920c195845838dcb2bd11d6bfc70f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPolicyDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5149ff2e3e038ed0fedb280a4bc388906e0f9d5686d3bf4890d07e14c7f48ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountQueuePropertiesMinuteMetrics]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesMinuteMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountQueuePropertiesMinuteMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22015976cc598076436f489232ed19a0017e1f3821cfb7e8df32afe5cac43973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountQueuePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountQueuePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be5c22351ee3dfdc61ab3001b16f822fc9b272bc59b96b0a4229799c271a6647)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCorsRule")
    def put_cors_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountQueuePropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c5b858416cb4531acabb58d8f57c7ca87d14babe8e9d4d833cfdab252dc9dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsRule", [value]))

    @jsii.member(jsii_name="putHourMetrics")
    def put_hour_metrics(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#enabled StorageAccount#enabled}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.
        :param include_apis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#include_apis StorageAccount#include_apis}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.
        '''
        value = StorageAccountQueuePropertiesHourMetrics(
            enabled=enabled,
            version=version,
            include_apis=include_apis,
            retention_policy_days=retention_policy_days,
        )

        return typing.cast(None, jsii.invoke(self, "putHourMetrics", [value]))

    @jsii.member(jsii_name="putLogging")
    def put_logging(
        self,
        *,
        delete: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        read: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        write: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete StorageAccount#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#read StorageAccount#read}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.
        :param write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#write StorageAccount#write}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.
        '''
        value = StorageAccountQueuePropertiesLogging(
            delete=delete,
            read=read,
            version=version,
            write=write,
            retention_policy_days=retention_policy_days,
        )

        return typing.cast(None, jsii.invoke(self, "putLogging", [value]))

    @jsii.member(jsii_name="putMinuteMetrics")
    def put_minute_metrics(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        version: builtins.str,
        include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_policy_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#enabled StorageAccount#enabled}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#version StorageAccount#version}.
        :param include_apis: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#include_apis StorageAccount#include_apis}.
        :param retention_policy_days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy_days StorageAccount#retention_policy_days}.
        '''
        value = StorageAccountQueuePropertiesMinuteMetrics(
            enabled=enabled,
            version=version,
            include_apis=include_apis,
            retention_policy_days=retention_policy_days,
        )

        return typing.cast(None, jsii.invoke(self, "putMinuteMetrics", [value]))

    @jsii.member(jsii_name="resetCorsRule")
    def reset_cors_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsRule", []))

    @jsii.member(jsii_name="resetHourMetrics")
    def reset_hour_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourMetrics", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @jsii.member(jsii_name="resetMinuteMetrics")
    def reset_minute_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinuteMetrics", []))

    @builtins.property
    @jsii.member(jsii_name="corsRule")
    def cors_rule(self) -> StorageAccountQueuePropertiesCorsRuleList:
        return typing.cast(StorageAccountQueuePropertiesCorsRuleList, jsii.get(self, "corsRule"))

    @builtins.property
    @jsii.member(jsii_name="hourMetrics")
    def hour_metrics(self) -> StorageAccountQueuePropertiesHourMetricsOutputReference:
        return typing.cast(StorageAccountQueuePropertiesHourMetricsOutputReference, jsii.get(self, "hourMetrics"))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> StorageAccountQueuePropertiesLoggingOutputReference:
        return typing.cast(StorageAccountQueuePropertiesLoggingOutputReference, jsii.get(self, "logging"))

    @builtins.property
    @jsii.member(jsii_name="minuteMetrics")
    def minute_metrics(
        self,
    ) -> StorageAccountQueuePropertiesMinuteMetricsOutputReference:
        return typing.cast(StorageAccountQueuePropertiesMinuteMetricsOutputReference, jsii.get(self, "minuteMetrics"))

    @builtins.property
    @jsii.member(jsii_name="corsRuleInput")
    def cors_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRule]]], jsii.get(self, "corsRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="hourMetricsInput")
    def hour_metrics_input(
        self,
    ) -> typing.Optional[StorageAccountQueuePropertiesHourMetrics]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesHourMetrics], jsii.get(self, "hourMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional[StorageAccountQueuePropertiesLogging]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesLogging], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="minuteMetricsInput")
    def minute_metrics_input(
        self,
    ) -> typing.Optional[StorageAccountQueuePropertiesMinuteMetrics]:
        return typing.cast(typing.Optional[StorageAccountQueuePropertiesMinuteMetrics], jsii.get(self, "minuteMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountQueueProperties]:
        return typing.cast(typing.Optional[StorageAccountQueueProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountQueueProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74efba9c18e84809a5db4c4d74b97ef0b2a9a4d5c3202297d9142a127d022b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountRouting",
    jsii_struct_bases=[],
    name_mapping={
        "choice": "choice",
        "publish_internet_endpoints": "publishInternetEndpoints",
        "publish_microsoft_endpoints": "publishMicrosoftEndpoints",
    },
)
class StorageAccountRouting:
    def __init__(
        self,
        *,
        choice: typing.Optional[builtins.str] = None,
        publish_internet_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        publish_microsoft_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param choice: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#choice StorageAccount#choice}.
        :param publish_internet_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#publish_internet_endpoints StorageAccount#publish_internet_endpoints}.
        :param publish_microsoft_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#publish_microsoft_endpoints StorageAccount#publish_microsoft_endpoints}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73e59beae78c1c5504753ad91cc0b11acab5f4367b297b3aeba2e6e1630e6fc8)
            check_type(argname="argument choice", value=choice, expected_type=type_hints["choice"])
            check_type(argname="argument publish_internet_endpoints", value=publish_internet_endpoints, expected_type=type_hints["publish_internet_endpoints"])
            check_type(argname="argument publish_microsoft_endpoints", value=publish_microsoft_endpoints, expected_type=type_hints["publish_microsoft_endpoints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if choice is not None:
            self._values["choice"] = choice
        if publish_internet_endpoints is not None:
            self._values["publish_internet_endpoints"] = publish_internet_endpoints
        if publish_microsoft_endpoints is not None:
            self._values["publish_microsoft_endpoints"] = publish_microsoft_endpoints

    @builtins.property
    def choice(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#choice StorageAccount#choice}.'''
        result = self._values.get("choice")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_internet_endpoints(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#publish_internet_endpoints StorageAccount#publish_internet_endpoints}.'''
        result = self._values.get("publish_internet_endpoints")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def publish_microsoft_endpoints(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#publish_microsoft_endpoints StorageAccount#publish_microsoft_endpoints}.'''
        result = self._values.get("publish_microsoft_endpoints")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__824b7af7b1c0965f58cc39cd8ecf2742f4c030c8aa2f3d9e87209bea471b5af2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChoice")
    def reset_choice(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChoice", []))

    @jsii.member(jsii_name="resetPublishInternetEndpoints")
    def reset_publish_internet_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishInternetEndpoints", []))

    @jsii.member(jsii_name="resetPublishMicrosoftEndpoints")
    def reset_publish_microsoft_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublishMicrosoftEndpoints", []))

    @builtins.property
    @jsii.member(jsii_name="choiceInput")
    def choice_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "choiceInput"))

    @builtins.property
    @jsii.member(jsii_name="publishInternetEndpointsInput")
    def publish_internet_endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publishInternetEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="publishMicrosoftEndpointsInput")
    def publish_microsoft_endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publishMicrosoftEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="choice")
    def choice(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "choice"))

    @choice.setter
    def choice(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36553a336a147a2ec39fd88b24b7e91c1887ed569f8ab57b125fb9b9c06174a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "choice", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishInternetEndpoints")
    def publish_internet_endpoints(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publishInternetEndpoints"))

    @publish_internet_endpoints.setter
    def publish_internet_endpoints(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ffa9c44b457c67a6f9a12bfbefcf66b434d55b2994f6312ccdd86f7be139c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishInternetEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publishMicrosoftEndpoints")
    def publish_microsoft_endpoints(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publishMicrosoftEndpoints"))

    @publish_microsoft_endpoints.setter
    def publish_microsoft_endpoints(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c37136565d83e694c5a05734d381bfb2c4ff5fe1fae70b414a05dc2c5036d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishMicrosoftEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountRouting]:
        return typing.cast(typing.Optional[StorageAccountRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageAccountRouting]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cae6f4f4a15daa92857492efcbfb6d5c12a4fad9f9ac5192468e1172af2823e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSasPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "expiration_period": "expirationPeriod",
        "expiration_action": "expirationAction",
    },
)
class StorageAccountSasPolicy:
    def __init__(
        self,
        *,
        expiration_period: builtins.str,
        expiration_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param expiration_period: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#expiration_period StorageAccount#expiration_period}.
        :param expiration_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#expiration_action StorageAccount#expiration_action}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51b161f36cce15b5dc022b3fdd39bb55efeb36a0b457451bd77028382855b91)
            check_type(argname="argument expiration_period", value=expiration_period, expected_type=type_hints["expiration_period"])
            check_type(argname="argument expiration_action", value=expiration_action, expected_type=type_hints["expiration_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expiration_period": expiration_period,
        }
        if expiration_action is not None:
            self._values["expiration_action"] = expiration_action

    @builtins.property
    def expiration_period(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#expiration_period StorageAccount#expiration_period}.'''
        result = self._values.get("expiration_period")
        assert result is not None, "Required property 'expiration_period' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expiration_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#expiration_action StorageAccount#expiration_action}.'''
        result = self._values.get("expiration_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountSasPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountSasPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSasPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39f2b8c510f579c038fd0f530889de493db371f5a84feb5cc40dbea15360e7be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExpirationAction")
    def reset_expiration_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpirationAction", []))

    @builtins.property
    @jsii.member(jsii_name="expirationActionInput")
    def expiration_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationPeriodInput")
    def expiration_period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationPeriodInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationAction")
    def expiration_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationAction"))

    @expiration_action.setter
    def expiration_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbfc6cf594078242d52248c153fdb76c66625b416fec3eaebede07e7d12fdd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expirationPeriod")
    def expiration_period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expirationPeriod"))

    @expiration_period.setter
    def expiration_period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c283f588c9fec3df6bd994100605fec6d64cb464f710878fb38f0839fe1978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expirationPeriod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountSasPolicy]:
        return typing.cast(typing.Optional[StorageAccountSasPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[StorageAccountSasPolicy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f3932d8728645c3a3fdfa9268e73299394d5d3ce02eba3ec7087131341ed65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountShareProperties",
    jsii_struct_bases=[],
    name_mapping={
        "cors_rule": "corsRule",
        "retention_policy": "retentionPolicy",
        "smb": "smb",
    },
)
class StorageAccountShareProperties:
    def __init__(
        self,
        *,
        cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["StorageAccountSharePropertiesCorsRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        retention_policy: typing.Optional[typing.Union["StorageAccountSharePropertiesRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        smb: typing.Optional[typing.Union["StorageAccountSharePropertiesSmb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cors_rule: cors_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy StorageAccount#retention_policy}
        :param smb: smb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#smb StorageAccount#smb}
        '''
        if isinstance(retention_policy, dict):
            retention_policy = StorageAccountSharePropertiesRetentionPolicy(**retention_policy)
        if isinstance(smb, dict):
            smb = StorageAccountSharePropertiesSmb(**smb)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1ee7a99482c22453d395f3b17bf7b5ba358f999223a7596e76ffb6e093ec00e)
            check_type(argname="argument cors_rule", value=cors_rule, expected_type=type_hints["cors_rule"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument smb", value=smb, expected_type=type_hints["smb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cors_rule is not None:
            self._values["cors_rule"] = cors_rule
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if smb is not None:
            self._values["smb"] = smb

    @builtins.property
    def cors_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountSharePropertiesCorsRule"]]]:
        '''cors_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#cors_rule StorageAccount#cors_rule}
        '''
        result = self._values.get("cors_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["StorageAccountSharePropertiesCorsRule"]]], result)

    @builtins.property
    def retention_policy(
        self,
    ) -> typing.Optional["StorageAccountSharePropertiesRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#retention_policy StorageAccount#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["StorageAccountSharePropertiesRetentionPolicy"], result)

    @builtins.property
    def smb(self) -> typing.Optional["StorageAccountSharePropertiesSmb"]:
        '''smb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#smb StorageAccount#smb}
        '''
        result = self._values.get("smb")
        return typing.cast(typing.Optional["StorageAccountSharePropertiesSmb"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountShareProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSharePropertiesCorsRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_headers": "allowedHeaders",
        "allowed_methods": "allowedMethods",
        "allowed_origins": "allowedOrigins",
        "exposed_headers": "exposedHeaders",
        "max_age_in_seconds": "maxAgeInSeconds",
    },
)
class StorageAccountSharePropertiesCorsRule:
    def __init__(
        self,
        *,
        allowed_headers: typing.Sequence[builtins.str],
        allowed_methods: typing.Sequence[builtins.str],
        allowed_origins: typing.Sequence[builtins.str],
        exposed_headers: typing.Sequence[builtins.str],
        max_age_in_seconds: jsii.Number,
    ) -> None:
        '''
        :param allowed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_headers StorageAccount#allowed_headers}.
        :param allowed_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_methods StorageAccount#allowed_methods}.
        :param allowed_origins: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_origins StorageAccount#allowed_origins}.
        :param exposed_headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#exposed_headers StorageAccount#exposed_headers}.
        :param max_age_in_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#max_age_in_seconds StorageAccount#max_age_in_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ae5cf5e62de47bb4932fefaf568a5ec680c9adff9be449f3bee027c37ed614)
            check_type(argname="argument allowed_headers", value=allowed_headers, expected_type=type_hints["allowed_headers"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument exposed_headers", value=exposed_headers, expected_type=type_hints["exposed_headers"])
            check_type(argname="argument max_age_in_seconds", value=max_age_in_seconds, expected_type=type_hints["max_age_in_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_headers": allowed_headers,
            "allowed_methods": allowed_methods,
            "allowed_origins": allowed_origins,
            "exposed_headers": exposed_headers,
            "max_age_in_seconds": max_age_in_seconds,
        }

    @builtins.property
    def allowed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_headers StorageAccount#allowed_headers}.'''
        result = self._values.get("allowed_headers")
        assert result is not None, "Required property 'allowed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_methods(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_methods StorageAccount#allowed_methods}.'''
        result = self._values.get("allowed_methods")
        assert result is not None, "Required property 'allowed_methods' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#allowed_origins StorageAccount#allowed_origins}.'''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def exposed_headers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#exposed_headers StorageAccount#exposed_headers}.'''
        result = self._values.get("exposed_headers")
        assert result is not None, "Required property 'exposed_headers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def max_age_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#max_age_in_seconds StorageAccount#max_age_in_seconds}.'''
        result = self._values.get("max_age_in_seconds")
        assert result is not None, "Required property 'max_age_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountSharePropertiesCorsRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountSharePropertiesCorsRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSharePropertiesCorsRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d4ceb1ec75b0ba4be15e16ea4ea0b44cdfb01b7c021974b376858651690674e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "StorageAccountSharePropertiesCorsRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463f09aaee4873ca6cad0dd9bd1ca8f846185fecc6436aab24120409d8832ce8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("StorageAccountSharePropertiesCorsRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c7b6430e8b6a02605339c9d6603baca65ebded03cd5cca4a48643a8b3f4edb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9706f52fb90a2768e943c97840ce0ab47a1213f8af68fd41259beed601a60062)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d07ff3d3242dc1da3f4e8c7330fb0fae0417703a2e9c3d6615106c0ad927dc39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountSharePropertiesCorsRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountSharePropertiesCorsRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountSharePropertiesCorsRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042ae4338877cc8c4cb831a5b9934649b0330a9d4a09139a751c8977abee3492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountSharePropertiesCorsRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSharePropertiesCorsRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__110599aad7f06b2890bc17ef85dd80db6782d4404107b115c2c0ad67acdd8fe5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedHeadersInput")
    def allowed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedMethodsInput")
    def allowed_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="exposedHeadersInput")
    def exposed_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposedHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSecondsInput")
    def max_age_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAgeInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedHeaders")
    def allowed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedHeaders"))

    @allowed_headers.setter
    def allowed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5610d2dcc6589f4bc25f956745ca20a72f9089849494107b1220c9296fe2bf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedMethods")
    def allowed_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedMethods"))

    @allowed_methods.setter
    def allowed_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea134c603206e67d58af402be26135c5fcbe032bd26a4d867314ab15ff92d7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c509ecd147a3b165d9ca5abbd6a5c399abad92bcf8bf9533276e4979a8bb7d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposedHeaders")
    def exposed_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposedHeaders"))

    @exposed_headers.setter
    def exposed_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__235539cc50ef45bb7da033c1d95cb186865ebf22d6133d225f37a741c7a346eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposedHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAgeInSeconds")
    def max_age_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxAgeInSeconds"))

    @max_age_in_seconds.setter
    def max_age_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437b35897d8d523cc3b9148393a5d78807ee9d862a2bae04898c7e380bcfdf9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAgeInSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountSharePropertiesCorsRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountSharePropertiesCorsRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountSharePropertiesCorsRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424a0a535e050e86a22af685146504a28e7dff9c498b76c884c79e018c6af059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class StorageAccountSharePropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSharePropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d8e7e15272c4fa87180b91b404714b9e436dca0f6f39cb395aa393537c3686)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCorsRule")
    def put_cors_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountSharePropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7feedc2c7c68d90e0ade87420a545a36017b8e5c01122c75fb051c3e2743ff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCorsRule", [value]))

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.
        '''
        value = StorageAccountSharePropertiesRetentionPolicy(days=days)

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="putSmb")
    def put_smb(
        self,
        *,
        authentication_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        channel_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        kerberos_ticket_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        multichannel_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param authentication_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#authentication_types StorageAccount#authentication_types}.
        :param channel_encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#channel_encryption_type StorageAccount#channel_encryption_type}.
        :param kerberos_ticket_encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#kerberos_ticket_encryption_type StorageAccount#kerberos_ticket_encryption_type}.
        :param multichannel_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#multichannel_enabled StorageAccount#multichannel_enabled}.
        :param versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#versions StorageAccount#versions}.
        '''
        value = StorageAccountSharePropertiesSmb(
            authentication_types=authentication_types,
            channel_encryption_type=channel_encryption_type,
            kerberos_ticket_encryption_type=kerberos_ticket_encryption_type,
            multichannel_enabled=multichannel_enabled,
            versions=versions,
        )

        return typing.cast(None, jsii.invoke(self, "putSmb", [value]))

    @jsii.member(jsii_name="resetCorsRule")
    def reset_cors_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsRule", []))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetSmb")
    def reset_smb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmb", []))

    @builtins.property
    @jsii.member(jsii_name="corsRule")
    def cors_rule(self) -> StorageAccountSharePropertiesCorsRuleList:
        return typing.cast(StorageAccountSharePropertiesCorsRuleList, jsii.get(self, "corsRule"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(
        self,
    ) -> "StorageAccountSharePropertiesRetentionPolicyOutputReference":
        return typing.cast("StorageAccountSharePropertiesRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="smb")
    def smb(self) -> "StorageAccountSharePropertiesSmbOutputReference":
        return typing.cast("StorageAccountSharePropertiesSmbOutputReference", jsii.get(self, "smb"))

    @builtins.property
    @jsii.member(jsii_name="corsRuleInput")
    def cors_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountSharePropertiesCorsRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountSharePropertiesCorsRule]]], jsii.get(self, "corsRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["StorageAccountSharePropertiesRetentionPolicy"]:
        return typing.cast(typing.Optional["StorageAccountSharePropertiesRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="smbInput")
    def smb_input(self) -> typing.Optional["StorageAccountSharePropertiesSmb"]:
        return typing.cast(typing.Optional["StorageAccountSharePropertiesSmb"], jsii.get(self, "smbInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountShareProperties]:
        return typing.cast(typing.Optional[StorageAccountShareProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountShareProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df8a7b5f3589b78154813882f942bdf0a9d9a25eea89140b732fe39359640af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSharePropertiesRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={"days": "days"},
)
class StorageAccountSharePropertiesRetentionPolicy:
    def __init__(self, *, days: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee35e27cfd232c0d8bdb801586e888f400716a5f137324b3fb8abe221c53f326)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#days StorageAccount#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountSharePropertiesRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountSharePropertiesRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSharePropertiesRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92c59e6acbbf7de738d3841d8568834ff3f59bd9a211ae56e828ca19c2f8a57f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92e1037340e5c0f58ca335a5bd9b28dcc2afe1ecb9ab02ec77c66a38d4e01ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[StorageAccountSharePropertiesRetentionPolicy]:
        return typing.cast(typing.Optional[StorageAccountSharePropertiesRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountSharePropertiesRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a18b9fe2d1064178035f9825feb73d44a9fca9a82335b419398446ccfd8a46e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSharePropertiesSmb",
    jsii_struct_bases=[],
    name_mapping={
        "authentication_types": "authenticationTypes",
        "channel_encryption_type": "channelEncryptionType",
        "kerberos_ticket_encryption_type": "kerberosTicketEncryptionType",
        "multichannel_enabled": "multichannelEnabled",
        "versions": "versions",
    },
)
class StorageAccountSharePropertiesSmb:
    def __init__(
        self,
        *,
        authentication_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        channel_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        kerberos_ticket_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
        multichannel_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        versions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param authentication_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#authentication_types StorageAccount#authentication_types}.
        :param channel_encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#channel_encryption_type StorageAccount#channel_encryption_type}.
        :param kerberos_ticket_encryption_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#kerberos_ticket_encryption_type StorageAccount#kerberos_ticket_encryption_type}.
        :param multichannel_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#multichannel_enabled StorageAccount#multichannel_enabled}.
        :param versions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#versions StorageAccount#versions}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407c4dcc6ab56a23291bf001c7727f675711ef5c589ea208e95125ab95a3c17a)
            check_type(argname="argument authentication_types", value=authentication_types, expected_type=type_hints["authentication_types"])
            check_type(argname="argument channel_encryption_type", value=channel_encryption_type, expected_type=type_hints["channel_encryption_type"])
            check_type(argname="argument kerberos_ticket_encryption_type", value=kerberos_ticket_encryption_type, expected_type=type_hints["kerberos_ticket_encryption_type"])
            check_type(argname="argument multichannel_enabled", value=multichannel_enabled, expected_type=type_hints["multichannel_enabled"])
            check_type(argname="argument versions", value=versions, expected_type=type_hints["versions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication_types is not None:
            self._values["authentication_types"] = authentication_types
        if channel_encryption_type is not None:
            self._values["channel_encryption_type"] = channel_encryption_type
        if kerberos_ticket_encryption_type is not None:
            self._values["kerberos_ticket_encryption_type"] = kerberos_ticket_encryption_type
        if multichannel_enabled is not None:
            self._values["multichannel_enabled"] = multichannel_enabled
        if versions is not None:
            self._values["versions"] = versions

    @builtins.property
    def authentication_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#authentication_types StorageAccount#authentication_types}.'''
        result = self._values.get("authentication_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def channel_encryption_type(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#channel_encryption_type StorageAccount#channel_encryption_type}.'''
        result = self._values.get("channel_encryption_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def kerberos_ticket_encryption_type(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#kerberos_ticket_encryption_type StorageAccount#kerberos_ticket_encryption_type}.'''
        result = self._values.get("kerberos_ticket_encryption_type")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def multichannel_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#multichannel_enabled StorageAccount#multichannel_enabled}.'''
        result = self._values.get("multichannel_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#versions StorageAccount#versions}.'''
        result = self._values.get("versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountSharePropertiesSmb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountSharePropertiesSmbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountSharePropertiesSmbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c4d16d7bc7c97e10527be9b7c7bc822b06e7735692eb8024f891b2c947cc1ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAuthenticationTypes")
    def reset_authentication_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthenticationTypes", []))

    @jsii.member(jsii_name="resetChannelEncryptionType")
    def reset_channel_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannelEncryptionType", []))

    @jsii.member(jsii_name="resetKerberosTicketEncryptionType")
    def reset_kerberos_ticket_encryption_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKerberosTicketEncryptionType", []))

    @jsii.member(jsii_name="resetMultichannelEnabled")
    def reset_multichannel_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMultichannelEnabled", []))

    @jsii.member(jsii_name="resetVersions")
    def reset_versions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersions", []))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypesInput")
    def authentication_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "authenticationTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="channelEncryptionTypeInput")
    def channel_encryption_type_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "channelEncryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="kerberosTicketEncryptionTypeInput")
    def kerberos_ticket_encryption_type_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "kerberosTicketEncryptionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="multichannelEnabledInput")
    def multichannel_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "multichannelEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="versionsInput")
    def versions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "versionsInput"))

    @builtins.property
    @jsii.member(jsii_name="authenticationTypes")
    def authentication_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "authenticationTypes"))

    @authentication_types.setter
    def authentication_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ba6bc797e9202987ec861d92b33674ab91b65fd81b9d54493926833cdfec9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authenticationTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="channelEncryptionType")
    def channel_encryption_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "channelEncryptionType"))

    @channel_encryption_type.setter
    def channel_encryption_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e78d46bbb7ef9f24a20e3d741e59649307ba314cc34cc4fa962d6cfdde90cf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelEncryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kerberosTicketEncryptionType")
    def kerberos_ticket_encryption_type(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "kerberosTicketEncryptionType"))

    @kerberos_ticket_encryption_type.setter
    def kerberos_ticket_encryption_type(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59bffeb5e07b3b47324a0733cd2ee3ab553dfbde8b736ffa18885d9885c5ab49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kerberosTicketEncryptionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="multichannelEnabled")
    def multichannel_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "multichannelEnabled"))

    @multichannel_enabled.setter
    def multichannel_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38fb456067ea81355b9294bbcb1d3f41724d626a6fa891826f821bbf7f8584c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "multichannelEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versions")
    def versions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "versions"))

    @versions.setter
    def versions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9faaef156c0f516bd2c4051bab430805fe7d898a746b15c94e5062ea7b4feecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountSharePropertiesSmb]:
        return typing.cast(typing.Optional[StorageAccountSharePropertiesSmb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountSharePropertiesSmb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4385afe2a9392eea2cc07bfb3d9be9ae49b8ed569e86d3a18d7445394df17449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountStaticWebsite",
    jsii_struct_bases=[],
    name_mapping={
        "error404_document": "error404Document",
        "index_document": "indexDocument",
    },
)
class StorageAccountStaticWebsite:
    def __init__(
        self,
        *,
        error404_document: typing.Optional[builtins.str] = None,
        index_document: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param error404_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#error_404_document StorageAccount#error_404_document}.
        :param index_document: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#index_document StorageAccount#index_document}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc7b5bdb1a73309a5b116db0cbe02ed8b6c3a41b1c2edf56c8449a3f7453f391)
            check_type(argname="argument error404_document", value=error404_document, expected_type=type_hints["error404_document"])
            check_type(argname="argument index_document", value=index_document, expected_type=type_hints["index_document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if error404_document is not None:
            self._values["error404_document"] = error404_document
        if index_document is not None:
            self._values["index_document"] = index_document

    @builtins.property
    def error404_document(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#error_404_document StorageAccount#error_404_document}.'''
        result = self._values.get("error404_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index_document(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#index_document StorageAccount#index_document}.'''
        result = self._values.get("index_document")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountStaticWebsite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountStaticWebsiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountStaticWebsiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8abcd9f125495f030c6558c610d7ba30fd3fe685486ec19fa78abe48dcce0e4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetError404Document")
    def reset_error404_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetError404Document", []))

    @jsii.member(jsii_name="resetIndexDocument")
    def reset_index_document(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndexDocument", []))

    @builtins.property
    @jsii.member(jsii_name="error404DocumentInput")
    def error404_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "error404DocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="indexDocumentInput")
    def index_document_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexDocumentInput"))

    @builtins.property
    @jsii.member(jsii_name="error404Document")
    def error404_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "error404Document"))

    @error404_document.setter
    def error404_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e1dd9b133d4bccb869cafe10f490a619469563e0b1af161d29ad4a6f857385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "error404Document", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexDocument")
    def index_document(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexDocument"))

    @index_document.setter
    def index_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3de6db6939b1d732417671763b149d9f5c0a61be963cbe7b7cae52ed7ba6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexDocument", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[StorageAccountStaticWebsite]:
        return typing.cast(typing.Optional[StorageAccountStaticWebsite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[StorageAccountStaticWebsite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7ab5c0eef454cac7cc71d5eb7949052ba45c3506dc7fbaa73faa11270c658b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class StorageAccountTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#create StorageAccount#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete StorageAccount#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#read StorageAccount#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#update StorageAccount#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8b81d854d8deb8279cab432a28738baac3bfde4c2734ff61a2175e3f0459e4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#create StorageAccount#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#delete StorageAccount#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#read StorageAccount#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/storage_account#update StorageAccount#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageAccountTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageAccountTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.storageAccount.StorageAccountTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__711de6d30d4605d8d7be34e2678b775b2e5437ab1ef4e3518c0c9237001aa626)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64e7332ff7b5ec874fcf8c1b4463e4f32f35454b4c9ebd653cf1b979008da835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a05b0942ec35a1d9dde5a876f0badec8471dcd79a5f2a0d6202e2861709f1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afff968663f8cb1088f26e214280a9117902d4f3e8e4351244b1363c0fa9fcbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145c34fcfc0326b6a6a7f8ba640118f7809329c0b6f35cc70664c6c2fa0d065f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d006be3b1901731deccd29f4479643db81bc0dee9528d4aa4b5b5b81d7c6f19d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "StorageAccount",
    "StorageAccountAzureFilesAuthentication",
    "StorageAccountAzureFilesAuthenticationActiveDirectory",
    "StorageAccountAzureFilesAuthenticationActiveDirectoryOutputReference",
    "StorageAccountAzureFilesAuthenticationOutputReference",
    "StorageAccountBlobProperties",
    "StorageAccountBlobPropertiesContainerDeleteRetentionPolicy",
    "StorageAccountBlobPropertiesContainerDeleteRetentionPolicyOutputReference",
    "StorageAccountBlobPropertiesCorsRule",
    "StorageAccountBlobPropertiesCorsRuleList",
    "StorageAccountBlobPropertiesCorsRuleOutputReference",
    "StorageAccountBlobPropertiesDeleteRetentionPolicy",
    "StorageAccountBlobPropertiesDeleteRetentionPolicyOutputReference",
    "StorageAccountBlobPropertiesOutputReference",
    "StorageAccountBlobPropertiesRestorePolicy",
    "StorageAccountBlobPropertiesRestorePolicyOutputReference",
    "StorageAccountConfig",
    "StorageAccountCustomDomain",
    "StorageAccountCustomDomainOutputReference",
    "StorageAccountCustomerManagedKey",
    "StorageAccountCustomerManagedKeyOutputReference",
    "StorageAccountIdentity",
    "StorageAccountIdentityOutputReference",
    "StorageAccountImmutabilityPolicy",
    "StorageAccountImmutabilityPolicyOutputReference",
    "StorageAccountNetworkRules",
    "StorageAccountNetworkRulesOutputReference",
    "StorageAccountNetworkRulesPrivateLinkAccess",
    "StorageAccountNetworkRulesPrivateLinkAccessList",
    "StorageAccountNetworkRulesPrivateLinkAccessOutputReference",
    "StorageAccountQueueProperties",
    "StorageAccountQueuePropertiesCorsRule",
    "StorageAccountQueuePropertiesCorsRuleList",
    "StorageAccountQueuePropertiesCorsRuleOutputReference",
    "StorageAccountQueuePropertiesHourMetrics",
    "StorageAccountQueuePropertiesHourMetricsOutputReference",
    "StorageAccountQueuePropertiesLogging",
    "StorageAccountQueuePropertiesLoggingOutputReference",
    "StorageAccountQueuePropertiesMinuteMetrics",
    "StorageAccountQueuePropertiesMinuteMetricsOutputReference",
    "StorageAccountQueuePropertiesOutputReference",
    "StorageAccountRouting",
    "StorageAccountRoutingOutputReference",
    "StorageAccountSasPolicy",
    "StorageAccountSasPolicyOutputReference",
    "StorageAccountShareProperties",
    "StorageAccountSharePropertiesCorsRule",
    "StorageAccountSharePropertiesCorsRuleList",
    "StorageAccountSharePropertiesCorsRuleOutputReference",
    "StorageAccountSharePropertiesOutputReference",
    "StorageAccountSharePropertiesRetentionPolicy",
    "StorageAccountSharePropertiesRetentionPolicyOutputReference",
    "StorageAccountSharePropertiesSmb",
    "StorageAccountSharePropertiesSmbOutputReference",
    "StorageAccountStaticWebsite",
    "StorageAccountStaticWebsiteOutputReference",
    "StorageAccountTimeouts",
    "StorageAccountTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ce651f82e85befcf5b1b70214df997041e8773c34ce411c0cffe913042c32e37(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_replication_type: builtins.str,
    account_tier: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    access_tier: typing.Optional[builtins.str] = None,
    account_kind: typing.Optional[builtins.str] = None,
    allowed_copy_scope: typing.Optional[builtins.str] = None,
    allow_nested_items_to_be_public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_files_authentication: typing.Optional[typing.Union[StorageAccountAzureFilesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    blob_properties: typing.Optional[typing.Union[StorageAccountBlobProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_tenant_replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_domain: typing.Optional[typing.Union[StorageAccountCustomDomain, typing.Dict[builtins.str, typing.Any]]] = None,
    customer_managed_key: typing.Optional[typing.Union[StorageAccountCustomerManagedKey, typing.Dict[builtins.str, typing.Any]]] = None,
    default_to_oauth_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dns_endpoint_type: typing.Optional[builtins.str] = None,
    edge_zone: typing.Optional[builtins.str] = None,
    https_traffic_only_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[StorageAccountIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    immutability_policy: typing.Optional[typing.Union[StorageAccountImmutabilityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_hns_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    large_file_share_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    local_user_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_tls_version: typing.Optional[builtins.str] = None,
    network_rules: typing.Optional[typing.Union[StorageAccountNetworkRules, typing.Dict[builtins.str, typing.Any]]] = None,
    nfsv3_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    queue_encryption_key_type: typing.Optional[builtins.str] = None,
    queue_properties: typing.Optional[typing.Union[StorageAccountQueueProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    routing: typing.Optional[typing.Union[StorageAccountRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    sas_policy: typing.Optional[typing.Union[StorageAccountSasPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    sftp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_access_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    share_properties: typing.Optional[typing.Union[StorageAccountShareProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    static_website: typing.Optional[typing.Union[StorageAccountStaticWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
    table_encryption_key_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[StorageAccountTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d623c20ef496cdb6ad4244f6ef5021407eb8722ce68adc7f94def7dc8f032160(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5509f28bca2a4dea8e0aab327fb3ac1221861a151d0b48ae249912b15b93c1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf37fd5d0a2cb4d73a6e2e0c4219711e87dffc4f1e61c756d4e7b7195048b28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca8b656211910a0aa8025b673d36c3b25e63cc664d6cb1a4a8443712a11cfe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164d07418fab5b22b506b51e1c8e51b39bbda1a569e3c6feab4ea4023b3fb73e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0938838b0271c52b58d86c2d0cad4977fe484abb044ce8ca21af08040922227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edae5b8b37f8266b4eae54207b7c6c6d39a62d98852e09521161a7925f12528(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba859791facc1107dcbb34a9b00a56aad7efa54c1d83c4dfc0cfce6629e36e95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63478ea634c4d3697f5e4db2ba411663af5d8912a1f5ab8d2456d775405e934f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdd24803f6d097a06a0c9160673e9fe095bbb1fb0f8ee6bc6ca71f20251bf47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6579060cff9393a14136405677d95cb0a6d119c231cd4788034ec7b3af4f96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59b4add0a6a1dd84dc842fb6b85f861cbfaf2a9ce9d4d105509371e669069f7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00affcd6634a915de2022f0d26cad021b40589613ce9242157f1b0d52daa1d76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c855487a4e02eea5557644787da02d82ae00cd74eb943f151e9a5400c86f2dd8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985b9274488616658964abc4654d0c113ce7e00ec5c088739e3114649277cc76(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400a5cb0f34f8184813420bb69666fd830a1be4de9be39cd6ec7704c7fc3c62f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbdf98d1d7535958a0dd94a4679b1f6b209fef91618d0adc73aed8ef5c96d1b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d8a2c333be192b920a204706c967959bd8e11ea354fd085da5b5a92c07dd88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120b8beef36c1b857b3b2c5154aaeb59cd35942d4dac2c7085c93187b0f69ca7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce738233af1ea4e8e6d9e8a5165df682665e93f72058b06c71b9b74d3a9e4f1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186dee099299a876b2c8816b3b68a8aaf85c53d59c7725d90d91d4a85562a257(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27e525daa2e2d15851b8ea987888bfd923ae9bbb3b24cd1f5917d4ef3acb4ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc3afd391739f688d50cbb1ab279121be97d5d81182f38fac4702dd8a6e7be8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553bbc0d40ebf30b293c040b665fe2eac04325f23337897a3ae4b29d21563a30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b521ae0d33ca7e6631cc6e2b9106bbc5f9487d83562c821068cecec215ed2130(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3185b20705992a4c137d676c8f8fa8da0bd548b9df680f2ca615ab5626cc861c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdaa9baf0a4ecca46dfa2e4b13d369779496b273c79f1b5c46480ac38378f9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291684da71c6233f617d8763d1831b08a9af3ee1f0a4c600e48dfcf0ebadda6f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c7c4844f589e62c26caa271cabd1b933f7cfbbf5fc9e606c8d93233c202770(
    *,
    directory_type: builtins.str,
    active_directory: typing.Optional[typing.Union[StorageAccountAzureFilesAuthenticationActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    default_share_level_permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36e3349ae74542f974fc8b566a50a811327891f324ba03b970b2b2e208072de(
    *,
    domain_guid: builtins.str,
    domain_name: builtins.str,
    domain_sid: typing.Optional[builtins.str] = None,
    forest_name: typing.Optional[builtins.str] = None,
    netbios_domain_name: typing.Optional[builtins.str] = None,
    storage_sid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c968783755f02282d89974468d4dabc85b2115ea3c7aa73f73fd8343836b3c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88447d8ce99b1339c23154c470a796a90af35a3ff6c6686264dc4aed3698c8c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9c289fcc94c775f9eda0c08f03a4d036170d1f88d57844ff2679df7d77b86d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc654db6fdf686a02d95c9d8e859245fb3952f0c51971dccf08ce372881991f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd22c2adefe93d452715f254e294c8fd6e327578385c9af38bdff346c8a4a7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4107d1a8d924c56fed1c4ed380e25cb178f6af1c2ac4726d7f92e11c7b46de6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13474445904897111a16fb43030ad09f3dec6f38e00f17d2a3c93339e0431569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f6db353efc897bd02977cbde15f77078cad7d88779e8bda2327ae6cacdf584(
    value: typing.Optional[StorageAccountAzureFilesAuthenticationActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc7a72b13e2c567f37b59c05b2ab2afdd63b8f5871d68640e1c3318261df404(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc99b9f6097ea9bf007854362ae46655b32c6cbb4e163b5c3ba0bc7cac4ad13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0f3652f5866422b9b1001a9e4f36ff840f7a19d9f7196140b763f046f66c64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf22381183669de15e025a3acc4a0b3745ca045806655fb0b494ebd55f50927(
    value: typing.Optional[StorageAccountAzureFilesAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6df10245dd529c2b54c3dd2f3266d99c45628de920de244abf443ba1d77c7b6d(
    *,
    change_feed_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    change_feed_retention_in_days: typing.Optional[jsii.Number] = None,
    container_delete_retention_policy: typing.Optional[typing.Union[StorageAccountBlobPropertiesContainerDeleteRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountBlobPropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_service_version: typing.Optional[builtins.str] = None,
    delete_retention_policy: typing.Optional[typing.Union[StorageAccountBlobPropertiesDeleteRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    last_access_time_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    restore_policy: typing.Optional[typing.Union[StorageAccountBlobPropertiesRestorePolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    versioning_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1b3f1f346f85e36cc6bddb53d1d00b3cdc7647abc2419b0ca6d09a7fab4d363(
    *,
    days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201929429b4e663a863ea825f8216c77e899158488b6b88301834990bf28f8a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf15397e1163609379a7315d38ef86a6792fece889ebf8d9c1cba8e2af8c5f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef376ca802832793373547e08d0986990aa67b874a178f80596184fd6e8013a7(
    value: typing.Optional[StorageAccountBlobPropertiesContainerDeleteRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab350d1852f307a865c2dc72de4b01824bcdce81d00db130b51efd01db75e26(
    *,
    allowed_headers: typing.Sequence[builtins.str],
    allowed_methods: typing.Sequence[builtins.str],
    allowed_origins: typing.Sequence[builtins.str],
    exposed_headers: typing.Sequence[builtins.str],
    max_age_in_seconds: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95461c7c174b5678c49b420ee12abce520d0c5bda044ffbaf40abb9448616386(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc1b085458a8954def2f99a76882dc3471da0a25729c9994a2d425d8537ad81(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04dc9f0982832b5e85cc1d73f706c1b3ccdcf082a1bcbd6e951456e24ed4dfdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1b1e870c7f9b9b364bb1277d391b31571b61c5d9da62f6a323edf20caf378d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095a6890153788345da9639fac979506d0eda17f703377da31522af2efe22eee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ef755d055feaf21e516a6406278000e1055885bd10403d85de89883c6149f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountBlobPropertiesCorsRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__526ab63018f0d5506eb220a363408a1c3c81fafb6f0e7d70542baf45ab66f313(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26083cfd3e1e91b880655b139595692cb6017073755814d46d40a513b7085594(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6108e8378558fdd9a992cb8228d4642c210d1918f870d219e43728b6f52558df(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b92cb48598b77b7934f6ecbb1a730493a4ba9abf5ac15e2514f27b50feb90f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c222f4b3916a0c56196feee93c1fefc90787a36fd68b3f86ba7cb904d1a7b4f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68551dde0bbff40d2e2fc3e981818201104895e6efb43ab420bf35a745a1b3d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d1c40d8ed96bf8f3191ba410c596f14bf4d830b8f4d262c6778ea9bc7bb091(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountBlobPropertiesCorsRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868a8114349e3923b4e4483c045be5e938cb06143a765d87835b8f3fedef50a1(
    *,
    days: typing.Optional[jsii.Number] = None,
    permanent_delete_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983e88827d25ab340143c3a7f26d05f1f88890f2a96821358bfd560b0996a7f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140a300b1d330f089cfb3be4a093c629409ae33a7a1ab8f82c956406a1dee49a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f21e562a6799cd01f7d57674d77269c6ede0d81afa89b62157477b90469433(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eceab6fc546dcd454774bd13feb90b1a91514424693427bab776ff33f09ce16(
    value: typing.Optional[StorageAccountBlobPropertiesDeleteRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f205238a7b68cd770ed7febe5a6472254a70955bd5db53bf26f338708ce85698(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5febc330ac8e1c1c5b752055dea81bfea45ec178b4003dace7a78b00a9893f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountBlobPropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a108d090bf9d872c2ce5bbe6627051c2ce1c1809d56b0e539441f1c1bd4a8489(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22efc201d63effc5b4707f6a50e8dd88b7daf5b7c4cd8746ea3460113acb3156(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85988f21a554479cbf09af01e72e356e0994632aae4a2048363d6a77faca13e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5b3b356c44539bd67bed97fb5902253d344a2e7cb8317cc9f2a78ad8decea4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9871ca0bcc47104970f278d5126b9593da3ea55a4bed45f093f89991e19148bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac34cce493a79da5b50300a7a7cd1553fd61c21ed0531010c4006a82dff88a0(
    value: typing.Optional[StorageAccountBlobProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3ad12b229031e3afd9e04587bec6a930677921d9f11b394fcabbc201410d543(
    *,
    days: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050d45d550aa2048af1c1a84f40cb3dbaf4b34c6304a82c5268c638c33856f1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98736747ace794951b0dffd9be584ebd1ba2bd14f87a5d9dd407b5c72798e77(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b483925f143a13fdb06c356a0cabb6d129f9acca8ed135610b81dce2892294(
    value: typing.Optional[StorageAccountBlobPropertiesRestorePolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64332c35e92aaa3ef7d040a7f09ecb59c7db234ca11aebf2b4c7362eb81b302b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_replication_type: builtins.str,
    account_tier: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    access_tier: typing.Optional[builtins.str] = None,
    account_kind: typing.Optional[builtins.str] = None,
    allowed_copy_scope: typing.Optional[builtins.str] = None,
    allow_nested_items_to_be_public: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_files_authentication: typing.Optional[typing.Union[StorageAccountAzureFilesAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    blob_properties: typing.Optional[typing.Union[StorageAccountBlobProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    cross_tenant_replication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    custom_domain: typing.Optional[typing.Union[StorageAccountCustomDomain, typing.Dict[builtins.str, typing.Any]]] = None,
    customer_managed_key: typing.Optional[typing.Union[StorageAccountCustomerManagedKey, typing.Dict[builtins.str, typing.Any]]] = None,
    default_to_oauth_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    dns_endpoint_type: typing.Optional[builtins.str] = None,
    edge_zone: typing.Optional[builtins.str] = None,
    https_traffic_only_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[StorageAccountIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    immutability_policy: typing.Optional[typing.Union[StorageAccountImmutabilityPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    infrastructure_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_hns_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    large_file_share_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    local_user_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_tls_version: typing.Optional[builtins.str] = None,
    network_rules: typing.Optional[typing.Union[StorageAccountNetworkRules, typing.Dict[builtins.str, typing.Any]]] = None,
    nfsv3_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    queue_encryption_key_type: typing.Optional[builtins.str] = None,
    queue_properties: typing.Optional[typing.Union[StorageAccountQueueProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    routing: typing.Optional[typing.Union[StorageAccountRouting, typing.Dict[builtins.str, typing.Any]]] = None,
    sas_policy: typing.Optional[typing.Union[StorageAccountSasPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    sftp_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_access_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    share_properties: typing.Optional[typing.Union[StorageAccountShareProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    static_website: typing.Optional[typing.Union[StorageAccountStaticWebsite, typing.Dict[builtins.str, typing.Any]]] = None,
    table_encryption_key_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[StorageAccountTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b927d48374e4b062fc040462e52f3ce85dc699f5e28158a4c0b5be88bc1d8ff(
    *,
    name: builtins.str,
    use_subdomain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777d5836ce7dc85d992587167b0b73e3c8ae8050fecca9c8c444f953dd06ed78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91b1257c4c592afb6017165f5c983a7d540165a72df133532bef49defddf0ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70d6b04da900d2d6ad208fc42a7b00c3ad52db5a455517706a2da5e2ebeb0a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae32e526ed79a3250b460355170428252a28a08c8d6a6fd253127fbb789175d(
    value: typing.Optional[StorageAccountCustomDomain],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718e82b00304ac54b807d4f54feba5f29c9ba241d86dcffbd8b437b68dba04bb(
    *,
    user_assigned_identity_id: builtins.str,
    key_vault_key_id: typing.Optional[builtins.str] = None,
    managed_hsm_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f0f3cd022cbe04d1b57ccee45243ae3ddaf74a80635d47200121ad3b2d334c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5203faed2015cffe88a5b73ca202fc61e88ac7a949e3acea4ed05a4c6b8d87e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a1e0678a41ffc74665c1080d136afe17607bf2c2de5ca1e0d9909b69bd924a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a81d3c4cc62a41f65dd472ac22592aec2033260e3842f02d8c512a0f083567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4a24cbdb8dc44ca977268b666874e2cb83668c1cef117c6b2ee3ab3e4edac4(
    value: typing.Optional[StorageAccountCustomerManagedKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8f459717de58a7b8c5d708614af039b7675bb2bb96411c8a0ff0dde14dc427(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f72851fe35a5e86c8194b947d69d76bf6751ff4613b99970057d4c4c470504c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572014204a2a080f7994792c927b836859f39ec7c284ee5a2f8f63bb97e9e61b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3f0e87b0d99d6b9dab94943e1f90633a25d4cd812423819914efeaa8494a6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e1d759e097c7a8ac73fe4c39da1dd0866fc81f3dc982966e82c7bc09a12787(
    value: typing.Optional[StorageAccountIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb5691a2bcbf4273cf02e7ebdaee6410534bd170bc7a6a57de81925bfdefd65(
    *,
    allow_protected_append_writes: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    period_since_creation_in_days: jsii.Number,
    state: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721f37dce983f02666ab5d2c5e7104917532ee5ca346169dff69db0001ebef31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff90c53adc789c7b9c7521cecb40cd21216b95b4a819facc76273e0ab23a440(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b80bf0dcefbd9881b60fd22b94d0027866a46c2746061d0e43b706327b3c178(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d67b5d4b5618f855e29ddb9228fa1f2e12cb55548e31b31357d44ea7bdd383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d780a5166e5e59a9aed226ebb7ddfbd2eeca9edc8f91dd9982abcec3c4c84db0(
    value: typing.Optional[StorageAccountImmutabilityPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7289f51993ff24b0f732378607ced170c4b67b1c6a755ad347ed3b2edc08d6b3(
    *,
    default_action: builtins.str,
    bypass: typing.Optional[typing.Sequence[builtins.str]] = None,
    ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    private_link_access: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountNetworkRulesPrivateLinkAccess, typing.Dict[builtins.str, typing.Any]]]]] = None,
    virtual_network_subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07449092563cf5d9eef19965f152fc57e8912665032e009d86c25c335a5bb80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8214af41ee890d6b679749b47b80a0a63b55eea999c4e473574588f15ca0563d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountNetworkRulesPrivateLinkAccess, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2aff5217862600fd6d1df426d585b1cce67075635d73792af9d5f93331cdbb1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f11feb3470d8af7405c5fb5847bc4da18d6f6cbfe76407c559ba7b9b8cb7f5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f53de50d70f4db3c042799103f61cbca98c93f1bfa16ad08f78b3a71a7b88f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6977dfabf365ecf31a9f9e586b779d27c0171890942c3e052b14b273acbbe0a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaeb4bfb5eefe8fa3af00f67745774dc739a916ff62247795604249de5f9ce4(
    value: typing.Optional[StorageAccountNetworkRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8629c9fcb9e793471227143c3ba3f3eda3e5782f6b586ea249d3ad7e08e309c7(
    *,
    endpoint_resource_id: builtins.str,
    endpoint_tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e16045fb82eb0b21dc538c8f032bc9b911aa40f8b28d8dcf623f121298c5c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eeb4361a708cf93ef42f0fe13f763804031e16111b530ad103d915b24e64fbf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae584df620903bddba3d8588ed5ada5924191353fdf0eb5df2281e7c1ef5927d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58490d7237a1307a88c2a6ee14a3152267b3b280d47257604d4c66642816f099(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fab904cc82fdcfab3c3953fde07729c1b1b964107997a878d8b97ee3a95d13(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4643a6f62d2d5818edcd41ff52359c176e96934839df8a8d77f75144824b5518(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountNetworkRulesPrivateLinkAccess]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e6eb46b80b234a76f3e4522fa741d05d791600af0e88379bd7f83b526072354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fcdc0916256ccaaa70578fa6f371909cb7c89766c7dba2c1f99568afe8dcf8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25bd3669e55f4c431faf5e56910098de305534c45470c2b5704028ecf2defc0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f92f1a7230b68243f748534085d478cbef2ffb74887660d4a38ffd3e84f1880(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountNetworkRulesPrivateLinkAccess]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c304b5e9c8da5f2db7919f7d699ffe59fcbb5ce5f917b2eae6c28e52465dc54(
    *,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountQueuePropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hour_metrics: typing.Optional[typing.Union[StorageAccountQueuePropertiesHourMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[typing.Union[StorageAccountQueuePropertiesLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    minute_metrics: typing.Optional[typing.Union[StorageAccountQueuePropertiesMinuteMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba792e58dec5020224c628b61e94c3d9c8c2c4a4e2968ccd0971479a04a78680(
    *,
    allowed_headers: typing.Sequence[builtins.str],
    allowed_methods: typing.Sequence[builtins.str],
    allowed_origins: typing.Sequence[builtins.str],
    exposed_headers: typing.Sequence[builtins.str],
    max_age_in_seconds: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710fe092bc3dc8692c226f3c691e8085a640b25590b3699f9d74c11c8cc3c171(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1d37f884a7b8cd851dc1d75b48f378cd11aa7746e2c3d58fe0dee5372deefe(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d536019c4148eba404308e206b29bc269bd9a02cc2b338a5c257cf4869ffc9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94544a8dcc5552e214fa236cacf684f667da504436c487d3202a27991d4d1d9b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c5b76f9a18dc6874d5d730314c1cb91798e61d321214f7a25fdef4042324ae(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4a85ce99e286a7c5b27a11076eeba6a68874750763195973e67c00b6cb85d8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountQueuePropertiesCorsRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786839df518e50783f79262fff6a6c873d5ea9d2e4cdbac7650911d50f05922d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f04d6a148601eb3b26e20ed10aa39d368b24217e58e2a9f0042d5870ce1c018e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af92a964fbe492612c55659ff5eb023a78fdb2cf19404980033eb5d33db61ffe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3b27a84eac06d3f00fb14d4e98dfaedc9c6eac72266e2e81cb6c51bb38d225(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34615fdf56ddd5448977d8921cc23450e1c38149160135f4f52614dc6d515a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dbddd3c80639ec5230954b5dcf7f4ecce4c9e358808377ee538e4cce349d28e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5be8f567c83a5840158e229f410959981e8e284b1d42c13db077bd4e282e84a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountQueuePropertiesCorsRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa121c1310abed15c2f59f539705402dcd70e1552726a2b03a195fad9bbed07(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    version: builtins.str,
    include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_policy_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191ba63d344e1a0850211d5e4164b3379cc9ebea229fda8ed84165b1d0152e0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae4f2a99b4e854af0918b9fb6d573f4a2cc5baaa17b6def529138d2934bc18b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c26e4cc72505e9d2a2864b5a5878cedd95e9bba1e9fe078e320e67d7179fe16(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785a51da8a33fff693fa612aa23df2d9467613c84b88ab76af25a1e7d42f21a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9759e648036a27d0dc52c4473580b8cf36be8b8d990cb355f984d9d53f645d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4bbd2bd2747eda3d11965ba25948f99f7c8259e88a1436e70d791d55f521d97(
    value: typing.Optional[StorageAccountQueuePropertiesHourMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e60fb75d325712510ce02e66e680fabe3db37683108491f0deab18cd8d7c6dab(
    *,
    delete: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    read: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    version: builtins.str,
    write: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    retention_policy_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f601abb412602e09ab3c666b5231aea70c092133ba68d276b21112dd72057a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a88dbd83510f6841074f83f53816a25db1dba64c66505e11462b75d7a92aea2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2919f02944b80d5156ce6004350c9326ddc4b853bfb42714275678bfb7e3e6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c90a81a70e38fb2aaf42bda343e9128b7edb279c7d0bde6b0b3935dae6b7ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ad0c0eb97d798879c3656328aa4e051ecdd44bd0b20bf3db3e072d4664755e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca50b73f50862640aa5830635c8bb3ebc061135fd67ca09828d2a20474e22ffc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a382e38d91c5149862a21cb6cd13157a538ad974c8110a3d69313993a6f578(
    value: typing.Optional[StorageAccountQueuePropertiesLogging],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35d0581f123411c1f92a3de9aff782644ff616c30663cf222f770e0685edb33(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    version: builtins.str,
    include_apis: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_policy_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5e66a1665c57385bfe5b15a214621641b12083d6f8a65e883d39f7596251e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71727971972446567a6237b12d8ad9f49bf80f279cd3382f70fba2440851098(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed404899a9c9009f02298dbfe94c71ee031546629cc82e2d384cc24f729bb29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2afcfa892682396e72d9d70cf0a032a14920c195845838dcb2bd11d6bfc70f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5149ff2e3e038ed0fedb280a4bc388906e0f9d5686d3bf4890d07e14c7f48ade(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22015976cc598076436f489232ed19a0017e1f3821cfb7e8df32afe5cac43973(
    value: typing.Optional[StorageAccountQueuePropertiesMinuteMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5c22351ee3dfdc61ab3001b16f822fc9b272bc59b96b0a4229799c271a6647(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c5b858416cb4531acabb58d8f57c7ca87d14babe8e9d4d833cfdab252dc9dd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountQueuePropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74efba9c18e84809a5db4c4d74b97ef0b2a9a4d5c3202297d9142a127d022b1(
    value: typing.Optional[StorageAccountQueueProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e59beae78c1c5504753ad91cc0b11acab5f4367b297b3aeba2e6e1630e6fc8(
    *,
    choice: typing.Optional[builtins.str] = None,
    publish_internet_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    publish_microsoft_endpoints: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824b7af7b1c0965f58cc39cd8ecf2742f4c030c8aa2f3d9e87209bea471b5af2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36553a336a147a2ec39fd88b24b7e91c1887ed569f8ab57b125fb9b9c06174a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ffa9c44b457c67a6f9a12bfbefcf66b434d55b2994f6312ccdd86f7be139c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c37136565d83e694c5a05734d381bfb2c4ff5fe1fae70b414a05dc2c5036d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cae6f4f4a15daa92857492efcbfb6d5c12a4fad9f9ac5192468e1172af2823e(
    value: typing.Optional[StorageAccountRouting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51b161f36cce15b5dc022b3fdd39bb55efeb36a0b457451bd77028382855b91(
    *,
    expiration_period: builtins.str,
    expiration_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f2b8c510f579c038fd0f530889de493db371f5a84feb5cc40dbea15360e7be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbfc6cf594078242d52248c153fdb76c66625b416fec3eaebede07e7d12fdd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c283f588c9fec3df6bd994100605fec6d64cb464f710878fb38f0839fe1978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f3932d8728645c3a3fdfa9268e73299394d5d3ce02eba3ec7087131341ed65(
    value: typing.Optional[StorageAccountSasPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ee7a99482c22453d395f3b17bf7b5ba358f999223a7596e76ffb6e093ec00e(
    *,
    cors_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountSharePropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    retention_policy: typing.Optional[typing.Union[StorageAccountSharePropertiesRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    smb: typing.Optional[typing.Union[StorageAccountSharePropertiesSmb, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ae5cf5e62de47bb4932fefaf568a5ec680c9adff9be449f3bee027c37ed614(
    *,
    allowed_headers: typing.Sequence[builtins.str],
    allowed_methods: typing.Sequence[builtins.str],
    allowed_origins: typing.Sequence[builtins.str],
    exposed_headers: typing.Sequence[builtins.str],
    max_age_in_seconds: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4ceb1ec75b0ba4be15e16ea4ea0b44cdfb01b7c021974b376858651690674e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463f09aaee4873ca6cad0dd9bd1ca8f846185fecc6436aab24120409d8832ce8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c7b6430e8b6a02605339c9d6603baca65ebded03cd5cca4a48643a8b3f4edb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9706f52fb90a2768e943c97840ce0ab47a1213f8af68fd41259beed601a60062(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07ff3d3242dc1da3f4e8c7330fb0fae0417703a2e9c3d6615106c0ad927dc39(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042ae4338877cc8c4cb831a5b9934649b0330a9d4a09139a751c8977abee3492(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[StorageAccountSharePropertiesCorsRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110599aad7f06b2890bc17ef85dd80db6782d4404107b115c2c0ad67acdd8fe5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5610d2dcc6589f4bc25f956745ca20a72f9089849494107b1220c9296fe2bf3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea134c603206e67d58af402be26135c5fcbe032bd26a4d867314ab15ff92d7fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c509ecd147a3b165d9ca5abbd6a5c399abad92bcf8bf9533276e4979a8bb7d9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__235539cc50ef45bb7da033c1d95cb186865ebf22d6133d225f37a741c7a346eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437b35897d8d523cc3b9148393a5d78807ee9d862a2bae04898c7e380bcfdf9d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424a0a535e050e86a22af685146504a28e7dff9c498b76c884c79e018c6af059(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountSharePropertiesCorsRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d8e7e15272c4fa87180b91b404714b9e436dca0f6f39cb395aa393537c3686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7feedc2c7c68d90e0ade87420a545a36017b8e5c01122c75fb051c3e2743ff1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[StorageAccountSharePropertiesCorsRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df8a7b5f3589b78154813882f942bdf0a9d9a25eea89140b732fe39359640af(
    value: typing.Optional[StorageAccountShareProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee35e27cfd232c0d8bdb801586e888f400716a5f137324b3fb8abe221c53f326(
    *,
    days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c59e6acbbf7de738d3841d8568834ff3f59bd9a211ae56e828ca19c2f8a57f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92e1037340e5c0f58ca335a5bd9b28dcc2afe1ecb9ab02ec77c66a38d4e01ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a18b9fe2d1064178035f9825feb73d44a9fca9a82335b419398446ccfd8a46e(
    value: typing.Optional[StorageAccountSharePropertiesRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407c4dcc6ab56a23291bf001c7727f675711ef5c589ea208e95125ab95a3c17a(
    *,
    authentication_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    channel_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    kerberos_ticket_encryption_type: typing.Optional[typing.Sequence[builtins.str]] = None,
    multichannel_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    versions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4d16d7bc7c97e10527be9b7c7bc822b06e7735692eb8024f891b2c947cc1ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ba6bc797e9202987ec861d92b33674ab91b65fd81b9d54493926833cdfec9d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e78d46bbb7ef9f24a20e3d741e59649307ba314cc34cc4fa962d6cfdde90cf6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59bffeb5e07b3b47324a0733cd2ee3ab553dfbde8b736ffa18885d9885c5ab49(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38fb456067ea81355b9294bbcb1d3f41724d626a6fa891826f821bbf7f8584c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9faaef156c0f516bd2c4051bab430805fe7d898a746b15c94e5062ea7b4feecf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4385afe2a9392eea2cc07bfb3d9be9ae49b8ed569e86d3a18d7445394df17449(
    value: typing.Optional[StorageAccountSharePropertiesSmb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7b5bdb1a73309a5b116db0cbe02ed8b6c3a41b1c2edf56c8449a3f7453f391(
    *,
    error404_document: typing.Optional[builtins.str] = None,
    index_document: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8abcd9f125495f030c6558c610d7ba30fd3fe685486ec19fa78abe48dcce0e4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e1dd9b133d4bccb869cafe10f490a619469563e0b1af161d29ad4a6f857385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3de6db6939b1d732417671763b149d9f5c0a61be963cbe7b7cae52ed7ba6ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7ab5c0eef454cac7cc71d5eb7949052ba45c3506dc7fbaa73faa11270c658b(
    value: typing.Optional[StorageAccountStaticWebsite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac8b81d854d8deb8279cab432a28738baac3bfde4c2734ff61a2175e3f0459e4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711de6d30d4605d8d7be34e2678b775b2e5437ab1ef4e3518c0c9237001aa626(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e7332ff7b5ec874fcf8c1b4463e4f32f35454b4c9ebd653cf1b979008da835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a05b0942ec35a1d9dde5a876f0badec8471dcd79a5f2a0d6202e2861709f1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afff968663f8cb1088f26e214280a9117902d4f3e8e4351244b1363c0fa9fcbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145c34fcfc0326b6a6a7f8ba640118f7809329c0b6f35cc70664c6c2fa0d065f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d006be3b1901731deccd29f4479643db81bc0dee9528d4aa4b5b5b81d7c6f19d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, StorageAccountTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

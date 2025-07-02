r'''
# `azurerm_synapse_workspace`

Refer to the Terraform Registry for docs: [`azurerm_synapse_workspace`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace).
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


class SynapseWorkspace(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspace",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace azurerm_synapse_workspace}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        storage_data_lake_gen2_filesystem_id: builtins.str,
        azuread_authentication_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_devops_repo: typing.Optional[typing.Union["SynapseWorkspaceAzureDevopsRepo", typing.Dict[builtins.str, typing.Any]]] = None,
        compute_subnet_id: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[typing.Union["SynapseWorkspaceCustomerManagedKey", typing.Dict[builtins.str, typing.Any]]] = None,
        data_exfiltration_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        github_repo: typing.Optional[typing.Union["SynapseWorkspaceGithubRepo", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["SynapseWorkspaceIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        linking_allowed_for_aad_tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        managed_virtual_network_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purview_id: typing.Optional[builtins.str] = None,
        sql_administrator_login: typing.Optional[builtins.str] = None,
        sql_administrator_login_password: typing.Optional[builtins.str] = None,
        sql_identity_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SynapseWorkspaceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace azurerm_synapse_workspace} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#location SynapseWorkspace#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#name SynapseWorkspace#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#resource_group_name SynapseWorkspace#resource_group_name}.
        :param storage_data_lake_gen2_filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#storage_data_lake_gen2_filesystem_id SynapseWorkspace#storage_data_lake_gen2_filesystem_id}.
        :param azuread_authentication_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#azuread_authentication_only SynapseWorkspace#azuread_authentication_only}.
        :param azure_devops_repo: azure_devops_repo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#azure_devops_repo SynapseWorkspace#azure_devops_repo}
        :param compute_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#compute_subnet_id SynapseWorkspace#compute_subnet_id}.
        :param customer_managed_key: customer_managed_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#customer_managed_key SynapseWorkspace#customer_managed_key}
        :param data_exfiltration_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#data_exfiltration_protection_enabled SynapseWorkspace#data_exfiltration_protection_enabled}.
        :param github_repo: github_repo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#github_repo SynapseWorkspace#github_repo}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#id SynapseWorkspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#identity SynapseWorkspace#identity}
        :param linking_allowed_for_aad_tenant_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#linking_allowed_for_aad_tenant_ids SynapseWorkspace#linking_allowed_for_aad_tenant_ids}.
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#managed_resource_group_name SynapseWorkspace#managed_resource_group_name}.
        :param managed_virtual_network_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#managed_virtual_network_enabled SynapseWorkspace#managed_virtual_network_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#public_network_access_enabled SynapseWorkspace#public_network_access_enabled}.
        :param purview_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#purview_id SynapseWorkspace#purview_id}.
        :param sql_administrator_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_administrator_login SynapseWorkspace#sql_administrator_login}.
        :param sql_administrator_login_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_administrator_login_password SynapseWorkspace#sql_administrator_login_password}.
        :param sql_identity_control_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_identity_control_enabled SynapseWorkspace#sql_identity_control_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#tags SynapseWorkspace#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#timeouts SynapseWorkspace#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415c7ed4a685a7b9c91323444402101bb804b8294a3be518a1f4f9a775a616e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SynapseWorkspaceConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            storage_data_lake_gen2_filesystem_id=storage_data_lake_gen2_filesystem_id,
            azuread_authentication_only=azuread_authentication_only,
            azure_devops_repo=azure_devops_repo,
            compute_subnet_id=compute_subnet_id,
            customer_managed_key=customer_managed_key,
            data_exfiltration_protection_enabled=data_exfiltration_protection_enabled,
            github_repo=github_repo,
            id=id,
            identity=identity,
            linking_allowed_for_aad_tenant_ids=linking_allowed_for_aad_tenant_ids,
            managed_resource_group_name=managed_resource_group_name,
            managed_virtual_network_enabled=managed_virtual_network_enabled,
            public_network_access_enabled=public_network_access_enabled,
            purview_id=purview_id,
            sql_administrator_login=sql_administrator_login,
            sql_administrator_login_password=sql_administrator_login_password,
            sql_identity_control_enabled=sql_identity_control_enabled,
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
        '''Generates CDKTF code for importing a SynapseWorkspace resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SynapseWorkspace to import.
        :param import_from_id: The id of the existing SynapseWorkspace that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SynapseWorkspace to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de0942db4d32465745f05e63022e496f45f7afff2729511228e2a830fcf13c93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureDevopsRepo")
    def put_azure_devops_repo(
        self,
        *,
        account_name: builtins.str,
        branch_name: builtins.str,
        project_name: builtins.str,
        repository_name: builtins.str,
        root_folder: builtins.str,
        last_commit_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#account_name SynapseWorkspace#account_name}.
        :param branch_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#branch_name SynapseWorkspace#branch_name}.
        :param project_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#project_name SynapseWorkspace#project_name}.
        :param repository_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#repository_name SynapseWorkspace#repository_name}.
        :param root_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#root_folder SynapseWorkspace#root_folder}.
        :param last_commit_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#last_commit_id SynapseWorkspace#last_commit_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#tenant_id SynapseWorkspace#tenant_id}.
        '''
        value = SynapseWorkspaceAzureDevopsRepo(
            account_name=account_name,
            branch_name=branch_name,
            project_name=project_name,
            repository_name=repository_name,
            root_folder=root_folder,
            last_commit_id=last_commit_id,
            tenant_id=tenant_id,
        )

        return typing.cast(None, jsii.invoke(self, "putAzureDevopsRepo", [value]))

    @jsii.member(jsii_name="putCustomerManagedKey")
    def put_customer_managed_key(
        self,
        *,
        key_versionless_id: builtins.str,
        key_name: typing.Optional[builtins.str] = None,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_versionless_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#key_versionless_id SynapseWorkspace#key_versionless_id}.
        :param key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#key_name SynapseWorkspace#key_name}.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#user_assigned_identity_id SynapseWorkspace#user_assigned_identity_id}.
        '''
        value = SynapseWorkspaceCustomerManagedKey(
            key_versionless_id=key_versionless_id,
            key_name=key_name,
            user_assigned_identity_id=user_assigned_identity_id,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomerManagedKey", [value]))

    @jsii.member(jsii_name="putGithubRepo")
    def put_github_repo(
        self,
        *,
        account_name: builtins.str,
        branch_name: builtins.str,
        repository_name: builtins.str,
        root_folder: builtins.str,
        git_url: typing.Optional[builtins.str] = None,
        last_commit_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#account_name SynapseWorkspace#account_name}.
        :param branch_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#branch_name SynapseWorkspace#branch_name}.
        :param repository_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#repository_name SynapseWorkspace#repository_name}.
        :param root_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#root_folder SynapseWorkspace#root_folder}.
        :param git_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#git_url SynapseWorkspace#git_url}.
        :param last_commit_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#last_commit_id SynapseWorkspace#last_commit_id}.
        '''
        value = SynapseWorkspaceGithubRepo(
            account_name=account_name,
            branch_name=branch_name,
            repository_name=repository_name,
            root_folder=root_folder,
            git_url=git_url,
            last_commit_id=last_commit_id,
        )

        return typing.cast(None, jsii.invoke(self, "putGithubRepo", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#type SynapseWorkspace#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#identity_ids SynapseWorkspace#identity_ids}.
        '''
        value = SynapseWorkspaceIdentity(type=type, identity_ids=identity_ids)

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#create SynapseWorkspace#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#delete SynapseWorkspace#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#read SynapseWorkspace#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#update SynapseWorkspace#update}.
        '''
        value = SynapseWorkspaceTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAzureadAuthenticationOnly")
    def reset_azuread_authentication_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureadAuthenticationOnly", []))

    @jsii.member(jsii_name="resetAzureDevopsRepo")
    def reset_azure_devops_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureDevopsRepo", []))

    @jsii.member(jsii_name="resetComputeSubnetId")
    def reset_compute_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeSubnetId", []))

    @jsii.member(jsii_name="resetCustomerManagedKey")
    def reset_customer_managed_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedKey", []))

    @jsii.member(jsii_name="resetDataExfiltrationProtectionEnabled")
    def reset_data_exfiltration_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataExfiltrationProtectionEnabled", []))

    @jsii.member(jsii_name="resetGithubRepo")
    def reset_github_repo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubRepo", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetLinkingAllowedForAadTenantIds")
    def reset_linking_allowed_for_aad_tenant_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkingAllowedForAadTenantIds", []))

    @jsii.member(jsii_name="resetManagedResourceGroupName")
    def reset_managed_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedResourceGroupName", []))

    @jsii.member(jsii_name="resetManagedVirtualNetworkEnabled")
    def reset_managed_virtual_network_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedVirtualNetworkEnabled", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetPurviewId")
    def reset_purview_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPurviewId", []))

    @jsii.member(jsii_name="resetSqlAdministratorLogin")
    def reset_sql_administrator_login(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlAdministratorLogin", []))

    @jsii.member(jsii_name="resetSqlAdministratorLoginPassword")
    def reset_sql_administrator_login_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlAdministratorLoginPassword", []))

    @jsii.member(jsii_name="resetSqlIdentityControlEnabled")
    def reset_sql_identity_control_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlIdentityControlEnabled", []))

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
    @jsii.member(jsii_name="azureDevopsRepo")
    def azure_devops_repo(self) -> "SynapseWorkspaceAzureDevopsRepoOutputReference":
        return typing.cast("SynapseWorkspaceAzureDevopsRepoOutputReference", jsii.get(self, "azureDevopsRepo"))

    @builtins.property
    @jsii.member(jsii_name="connectivityEndpoints")
    def connectivity_endpoints(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "connectivityEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKey")
    def customer_managed_key(
        self,
    ) -> "SynapseWorkspaceCustomerManagedKeyOutputReference":
        return typing.cast("SynapseWorkspaceCustomerManagedKeyOutputReference", jsii.get(self, "customerManagedKey"))

    @builtins.property
    @jsii.member(jsii_name="githubRepo")
    def github_repo(self) -> "SynapseWorkspaceGithubRepoOutputReference":
        return typing.cast("SynapseWorkspaceGithubRepoOutputReference", jsii.get(self, "githubRepo"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "SynapseWorkspaceIdentityOutputReference":
        return typing.cast("SynapseWorkspaceIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SynapseWorkspaceTimeoutsOutputReference":
        return typing.cast("SynapseWorkspaceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="azureadAuthenticationOnlyInput")
    def azuread_authentication_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "azureadAuthenticationOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="azureDevopsRepoInput")
    def azure_devops_repo_input(
        self,
    ) -> typing.Optional["SynapseWorkspaceAzureDevopsRepo"]:
        return typing.cast(typing.Optional["SynapseWorkspaceAzureDevopsRepo"], jsii.get(self, "azureDevopsRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="computeSubnetIdInput")
    def compute_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyInput")
    def customer_managed_key_input(
        self,
    ) -> typing.Optional["SynapseWorkspaceCustomerManagedKey"]:
        return typing.cast(typing.Optional["SynapseWorkspaceCustomerManagedKey"], jsii.get(self, "customerManagedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="dataExfiltrationProtectionEnabledInput")
    def data_exfiltration_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dataExfiltrationProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="githubRepoInput")
    def github_repo_input(self) -> typing.Optional["SynapseWorkspaceGithubRepo"]:
        return typing.cast(typing.Optional["SynapseWorkspaceGithubRepo"], jsii.get(self, "githubRepoInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["SynapseWorkspaceIdentity"]:
        return typing.cast(typing.Optional["SynapseWorkspaceIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linkingAllowedForAadTenantIdsInput")
    def linking_allowed_for_aad_tenant_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "linkingAllowedForAadTenantIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupNameInput")
    def managed_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="managedVirtualNetworkEnabledInput")
    def managed_virtual_network_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "managedVirtualNetworkEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="purviewIdInput")
    def purview_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "purviewIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlAdministratorLoginInput")
    def sql_administrator_login_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlAdministratorLoginInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlAdministratorLoginPasswordInput")
    def sql_administrator_login_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlAdministratorLoginPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlIdentityControlEnabledInput")
    def sql_identity_control_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sqlIdentityControlEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="storageDataLakeGen2FilesystemIdInput")
    def storage_data_lake_gen2_filesystem_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageDataLakeGen2FilesystemIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SynapseWorkspaceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SynapseWorkspaceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="azureadAuthenticationOnly")
    def azuread_authentication_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "azureadAuthenticationOnly"))

    @azuread_authentication_only.setter
    def azuread_authentication_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d11377f50d39be5ebd9532d22ec44c1bba1e8f75d7b654e1ad5a2bcf0f182b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "azureadAuthenticationOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="computeSubnetId")
    def compute_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeSubnetId"))

    @compute_subnet_id.setter
    def compute_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0473514189445b567d2bc41237cd68d3c0a86bccce45126184bbf2fa4ca5693a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataExfiltrationProtectionEnabled")
    def data_exfiltration_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dataExfiltrationProtectionEnabled"))

    @data_exfiltration_protection_enabled.setter
    def data_exfiltration_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644d10cfc73b4595ae2812c9c4ca5581d1f2ba4780b82624024ed2704a6e2a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataExfiltrationProtectionEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50cf5d949c3b1cdcd73a1d613cc5350c6cb64b878425b487cf54f60827be35d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="linkingAllowedForAadTenantIds")
    def linking_allowed_for_aad_tenant_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "linkingAllowedForAadTenantIds"))

    @linking_allowed_for_aad_tenant_ids.setter
    def linking_allowed_for_aad_tenant_ids(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61bf03dab344d63b557bba9917755a2c013a1396ab89fa12cac48d752fa8f5b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkingAllowedForAadTenantIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e5460e4c78a1e5353e430a0abad402e7e331ed16627ba25abec42572be9fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedResourceGroupName")
    def managed_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedResourceGroupName"))

    @managed_resource_group_name.setter
    def managed_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38fc9023d8c2fda86dcca642700f71203c565cb37ea9fe80f8d1dee23bcb22fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedVirtualNetworkEnabled")
    def managed_virtual_network_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "managedVirtualNetworkEnabled"))

    @managed_virtual_network_enabled.setter
    def managed_virtual_network_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c227d42239fe8da65d38a7debf726ef06ebda212b04d71d4d0448ae673ce54f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedVirtualNetworkEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad98ad1aef1e5d6a8ead4a089a56b6d29606e0971da5bdae97cc674f1189fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__bae8d4a349fc44b52b0d91526a70f7eefeaa2b83d37f6056a908fba91619b15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="purviewId")
    def purview_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "purviewId"))

    @purview_id.setter
    def purview_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6302d4b221c86e832d2f9dca52ab780e00919469c887954ecdbce5a4dd4dbac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "purviewId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d8bc25b895c9ad95f8272df88fa5cc88ba12ed5c9e97bca16f44038b3a95d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlAdministratorLogin")
    def sql_administrator_login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlAdministratorLogin"))

    @sql_administrator_login.setter
    def sql_administrator_login(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__669735306c716c0b2dec92e8b2475fe36386cd299b848cc8792261a268bb9dea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlAdministratorLogin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlAdministratorLoginPassword")
    def sql_administrator_login_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlAdministratorLoginPassword"))

    @sql_administrator_login_password.setter
    def sql_administrator_login_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48ae0c50bd0351ddad8ee6d92997473b11497adbdcc01233ebd811c5ff323a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlAdministratorLoginPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlIdentityControlEnabled")
    def sql_identity_control_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sqlIdentityControlEnabled"))

    @sql_identity_control_enabled.setter
    def sql_identity_control_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d749a64a3bcbf4f67915ef74f617ac4c0ccfb6e77bdd749035efc73c7e325f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlIdentityControlEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageDataLakeGen2FilesystemId")
    def storage_data_lake_gen2_filesystem_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageDataLakeGen2FilesystemId"))

    @storage_data_lake_gen2_filesystem_id.setter
    def storage_data_lake_gen2_filesystem_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bdf041b10cbc35e948f4c886e394f2e716bf7e51e676d819ead517bfa8fd3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageDataLakeGen2FilesystemId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0788301f1546ecd3139b259ff934aaae6ecff6c2b7794c6fa188d3443c2961b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceAzureDevopsRepo",
    jsii_struct_bases=[],
    name_mapping={
        "account_name": "accountName",
        "branch_name": "branchName",
        "project_name": "projectName",
        "repository_name": "repositoryName",
        "root_folder": "rootFolder",
        "last_commit_id": "lastCommitId",
        "tenant_id": "tenantId",
    },
)
class SynapseWorkspaceAzureDevopsRepo:
    def __init__(
        self,
        *,
        account_name: builtins.str,
        branch_name: builtins.str,
        project_name: builtins.str,
        repository_name: builtins.str,
        root_folder: builtins.str,
        last_commit_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#account_name SynapseWorkspace#account_name}.
        :param branch_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#branch_name SynapseWorkspace#branch_name}.
        :param project_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#project_name SynapseWorkspace#project_name}.
        :param repository_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#repository_name SynapseWorkspace#repository_name}.
        :param root_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#root_folder SynapseWorkspace#root_folder}.
        :param last_commit_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#last_commit_id SynapseWorkspace#last_commit_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#tenant_id SynapseWorkspace#tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45483737a6a3dc2aab9e2b84b4095c5e06a3bb700ec05304737b791702bd03f)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument root_folder", value=root_folder, expected_type=type_hints["root_folder"])
            check_type(argname="argument last_commit_id", value=last_commit_id, expected_type=type_hints["last_commit_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "branch_name": branch_name,
            "project_name": project_name,
            "repository_name": repository_name,
            "root_folder": root_folder,
        }
        if last_commit_id is not None:
            self._values["last_commit_id"] = last_commit_id
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id

    @builtins.property
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#account_name SynapseWorkspace#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#branch_name SynapseWorkspace#branch_name}.'''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#project_name SynapseWorkspace#project_name}.'''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#repository_name SynapseWorkspace#repository_name}.'''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_folder(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#root_folder SynapseWorkspace#root_folder}.'''
        result = self._values.get("root_folder")
        assert result is not None, "Required property 'root_folder' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def last_commit_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#last_commit_id SynapseWorkspace#last_commit_id}.'''
        result = self._values.get("last_commit_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#tenant_id SynapseWorkspace#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseWorkspaceAzureDevopsRepo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseWorkspaceAzureDevopsRepoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceAzureDevopsRepoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edb5aa156bc8a75ddf0fa21d792f3019aeb983d576691e9ab431a4aaf64caf11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLastCommitId")
    def reset_last_commit_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastCommitId", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="branchNameInput")
    def branch_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchNameInput"))

    @builtins.property
    @jsii.member(jsii_name="lastCommitIdInput")
    def last_commit_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastCommitIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectNameInput")
    def project_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectNameInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryNameInput")
    def repository_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootFolderInput")
    def root_folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootFolderInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18328a0557f17305ac11f2c7843fd97453c98d1f5c0e7acd1254c637dab5e93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @branch_name.setter
    def branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e528bdefca032f14d10338a9ac74899e9934cd7c65f83d745c2f56936e6018d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastCommitId")
    def last_commit_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastCommitId"))

    @last_commit_id.setter
    def last_commit_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e09a500dc2acec4007f925822c4aff292f408af14313a8ab338ec35fd19e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastCommitId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectName"))

    @project_name.setter
    def project_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd80af48d30c34eaf2d4a3d241d03693691d98a8a2cc1b5c56010927c422369f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e49465469ea1158c2af7a848b0c0877ae2c44fd2908cffcde452a53e5aa23510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootFolder")
    def root_folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootFolder"))

    @root_folder.setter
    def root_folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe79f397353c2009f6af906111fffe2da370a03c1cd2f361421f1b7d900437e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootFolder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__273763090cc7454a8f5c04197e9a4d041fa889f0324c32f46563ea6897a96c39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SynapseWorkspaceAzureDevopsRepo]:
        return typing.cast(typing.Optional[SynapseWorkspaceAzureDevopsRepo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SynapseWorkspaceAzureDevopsRepo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d878e5695a9af8cce5a5e243fe33dca30600cc4286685708bd4b8b257ffe89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceConfig",
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
        "storage_data_lake_gen2_filesystem_id": "storageDataLakeGen2FilesystemId",
        "azuread_authentication_only": "azureadAuthenticationOnly",
        "azure_devops_repo": "azureDevopsRepo",
        "compute_subnet_id": "computeSubnetId",
        "customer_managed_key": "customerManagedKey",
        "data_exfiltration_protection_enabled": "dataExfiltrationProtectionEnabled",
        "github_repo": "githubRepo",
        "id": "id",
        "identity": "identity",
        "linking_allowed_for_aad_tenant_ids": "linkingAllowedForAadTenantIds",
        "managed_resource_group_name": "managedResourceGroupName",
        "managed_virtual_network_enabled": "managedVirtualNetworkEnabled",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "purview_id": "purviewId",
        "sql_administrator_login": "sqlAdministratorLogin",
        "sql_administrator_login_password": "sqlAdministratorLoginPassword",
        "sql_identity_control_enabled": "sqlIdentityControlEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class SynapseWorkspaceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        storage_data_lake_gen2_filesystem_id: builtins.str,
        azuread_authentication_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_devops_repo: typing.Optional[typing.Union[SynapseWorkspaceAzureDevopsRepo, typing.Dict[builtins.str, typing.Any]]] = None,
        compute_subnet_id: typing.Optional[builtins.str] = None,
        customer_managed_key: typing.Optional[typing.Union["SynapseWorkspaceCustomerManagedKey", typing.Dict[builtins.str, typing.Any]]] = None,
        data_exfiltration_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        github_repo: typing.Optional[typing.Union["SynapseWorkspaceGithubRepo", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["SynapseWorkspaceIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        linking_allowed_for_aad_tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        managed_resource_group_name: typing.Optional[builtins.str] = None,
        managed_virtual_network_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purview_id: typing.Optional[builtins.str] = None,
        sql_administrator_login: typing.Optional[builtins.str] = None,
        sql_administrator_login_password: typing.Optional[builtins.str] = None,
        sql_identity_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SynapseWorkspaceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#location SynapseWorkspace#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#name SynapseWorkspace#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#resource_group_name SynapseWorkspace#resource_group_name}.
        :param storage_data_lake_gen2_filesystem_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#storage_data_lake_gen2_filesystem_id SynapseWorkspace#storage_data_lake_gen2_filesystem_id}.
        :param azuread_authentication_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#azuread_authentication_only SynapseWorkspace#azuread_authentication_only}.
        :param azure_devops_repo: azure_devops_repo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#azure_devops_repo SynapseWorkspace#azure_devops_repo}
        :param compute_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#compute_subnet_id SynapseWorkspace#compute_subnet_id}.
        :param customer_managed_key: customer_managed_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#customer_managed_key SynapseWorkspace#customer_managed_key}
        :param data_exfiltration_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#data_exfiltration_protection_enabled SynapseWorkspace#data_exfiltration_protection_enabled}.
        :param github_repo: github_repo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#github_repo SynapseWorkspace#github_repo}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#id SynapseWorkspace#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#identity SynapseWorkspace#identity}
        :param linking_allowed_for_aad_tenant_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#linking_allowed_for_aad_tenant_ids SynapseWorkspace#linking_allowed_for_aad_tenant_ids}.
        :param managed_resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#managed_resource_group_name SynapseWorkspace#managed_resource_group_name}.
        :param managed_virtual_network_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#managed_virtual_network_enabled SynapseWorkspace#managed_virtual_network_enabled}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#public_network_access_enabled SynapseWorkspace#public_network_access_enabled}.
        :param purview_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#purview_id SynapseWorkspace#purview_id}.
        :param sql_administrator_login: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_administrator_login SynapseWorkspace#sql_administrator_login}.
        :param sql_administrator_login_password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_administrator_login_password SynapseWorkspace#sql_administrator_login_password}.
        :param sql_identity_control_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_identity_control_enabled SynapseWorkspace#sql_identity_control_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#tags SynapseWorkspace#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#timeouts SynapseWorkspace#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(azure_devops_repo, dict):
            azure_devops_repo = SynapseWorkspaceAzureDevopsRepo(**azure_devops_repo)
        if isinstance(customer_managed_key, dict):
            customer_managed_key = SynapseWorkspaceCustomerManagedKey(**customer_managed_key)
        if isinstance(github_repo, dict):
            github_repo = SynapseWorkspaceGithubRepo(**github_repo)
        if isinstance(identity, dict):
            identity = SynapseWorkspaceIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = SynapseWorkspaceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dfcf6df084475ad9694b89c1c519158d0f1edf56c42e7e4cf5504064edcfe65)
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
            check_type(argname="argument storage_data_lake_gen2_filesystem_id", value=storage_data_lake_gen2_filesystem_id, expected_type=type_hints["storage_data_lake_gen2_filesystem_id"])
            check_type(argname="argument azuread_authentication_only", value=azuread_authentication_only, expected_type=type_hints["azuread_authentication_only"])
            check_type(argname="argument azure_devops_repo", value=azure_devops_repo, expected_type=type_hints["azure_devops_repo"])
            check_type(argname="argument compute_subnet_id", value=compute_subnet_id, expected_type=type_hints["compute_subnet_id"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument data_exfiltration_protection_enabled", value=data_exfiltration_protection_enabled, expected_type=type_hints["data_exfiltration_protection_enabled"])
            check_type(argname="argument github_repo", value=github_repo, expected_type=type_hints["github_repo"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument linking_allowed_for_aad_tenant_ids", value=linking_allowed_for_aad_tenant_ids, expected_type=type_hints["linking_allowed_for_aad_tenant_ids"])
            check_type(argname="argument managed_resource_group_name", value=managed_resource_group_name, expected_type=type_hints["managed_resource_group_name"])
            check_type(argname="argument managed_virtual_network_enabled", value=managed_virtual_network_enabled, expected_type=type_hints["managed_virtual_network_enabled"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument purview_id", value=purview_id, expected_type=type_hints["purview_id"])
            check_type(argname="argument sql_administrator_login", value=sql_administrator_login, expected_type=type_hints["sql_administrator_login"])
            check_type(argname="argument sql_administrator_login_password", value=sql_administrator_login_password, expected_type=type_hints["sql_administrator_login_password"])
            check_type(argname="argument sql_identity_control_enabled", value=sql_identity_control_enabled, expected_type=type_hints["sql_identity_control_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "storage_data_lake_gen2_filesystem_id": storage_data_lake_gen2_filesystem_id,
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
        if azuread_authentication_only is not None:
            self._values["azuread_authentication_only"] = azuread_authentication_only
        if azure_devops_repo is not None:
            self._values["azure_devops_repo"] = azure_devops_repo
        if compute_subnet_id is not None:
            self._values["compute_subnet_id"] = compute_subnet_id
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if data_exfiltration_protection_enabled is not None:
            self._values["data_exfiltration_protection_enabled"] = data_exfiltration_protection_enabled
        if github_repo is not None:
            self._values["github_repo"] = github_repo
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if linking_allowed_for_aad_tenant_ids is not None:
            self._values["linking_allowed_for_aad_tenant_ids"] = linking_allowed_for_aad_tenant_ids
        if managed_resource_group_name is not None:
            self._values["managed_resource_group_name"] = managed_resource_group_name
        if managed_virtual_network_enabled is not None:
            self._values["managed_virtual_network_enabled"] = managed_virtual_network_enabled
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if purview_id is not None:
            self._values["purview_id"] = purview_id
        if sql_administrator_login is not None:
            self._values["sql_administrator_login"] = sql_administrator_login
        if sql_administrator_login_password is not None:
            self._values["sql_administrator_login_password"] = sql_administrator_login_password
        if sql_identity_control_enabled is not None:
            self._values["sql_identity_control_enabled"] = sql_identity_control_enabled
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#location SynapseWorkspace#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#name SynapseWorkspace#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#resource_group_name SynapseWorkspace#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_data_lake_gen2_filesystem_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#storage_data_lake_gen2_filesystem_id SynapseWorkspace#storage_data_lake_gen2_filesystem_id}.'''
        result = self._values.get("storage_data_lake_gen2_filesystem_id")
        assert result is not None, "Required property 'storage_data_lake_gen2_filesystem_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azuread_authentication_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#azuread_authentication_only SynapseWorkspace#azuread_authentication_only}.'''
        result = self._values.get("azuread_authentication_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def azure_devops_repo(self) -> typing.Optional[SynapseWorkspaceAzureDevopsRepo]:
        '''azure_devops_repo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#azure_devops_repo SynapseWorkspace#azure_devops_repo}
        '''
        result = self._values.get("azure_devops_repo")
        return typing.cast(typing.Optional[SynapseWorkspaceAzureDevopsRepo], result)

    @builtins.property
    def compute_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#compute_subnet_id SynapseWorkspace#compute_subnet_id}.'''
        result = self._values.get("compute_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_managed_key(
        self,
    ) -> typing.Optional["SynapseWorkspaceCustomerManagedKey"]:
        '''customer_managed_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#customer_managed_key SynapseWorkspace#customer_managed_key}
        '''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional["SynapseWorkspaceCustomerManagedKey"], result)

    @builtins.property
    def data_exfiltration_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#data_exfiltration_protection_enabled SynapseWorkspace#data_exfiltration_protection_enabled}.'''
        result = self._values.get("data_exfiltration_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def github_repo(self) -> typing.Optional["SynapseWorkspaceGithubRepo"]:
        '''github_repo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#github_repo SynapseWorkspace#github_repo}
        '''
        result = self._values.get("github_repo")
        return typing.cast(typing.Optional["SynapseWorkspaceGithubRepo"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#id SynapseWorkspace#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["SynapseWorkspaceIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#identity SynapseWorkspace#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["SynapseWorkspaceIdentity"], result)

    @builtins.property
    def linking_allowed_for_aad_tenant_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#linking_allowed_for_aad_tenant_ids SynapseWorkspace#linking_allowed_for_aad_tenant_ids}.'''
        result = self._values.get("linking_allowed_for_aad_tenant_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def managed_resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#managed_resource_group_name SynapseWorkspace#managed_resource_group_name}.'''
        result = self._values.get("managed_resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_virtual_network_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#managed_virtual_network_enabled SynapseWorkspace#managed_virtual_network_enabled}.'''
        result = self._values.get("managed_virtual_network_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#public_network_access_enabled SynapseWorkspace#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def purview_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#purview_id SynapseWorkspace#purview_id}.'''
        result = self._values.get("purview_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_administrator_login(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_administrator_login SynapseWorkspace#sql_administrator_login}.'''
        result = self._values.get("sql_administrator_login")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_administrator_login_password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_administrator_login_password SynapseWorkspace#sql_administrator_login_password}.'''
        result = self._values.get("sql_administrator_login_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_identity_control_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#sql_identity_control_enabled SynapseWorkspace#sql_identity_control_enabled}.'''
        result = self._values.get("sql_identity_control_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#tags SynapseWorkspace#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SynapseWorkspaceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#timeouts SynapseWorkspace#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SynapseWorkspaceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseWorkspaceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceCustomerManagedKey",
    jsii_struct_bases=[],
    name_mapping={
        "key_versionless_id": "keyVersionlessId",
        "key_name": "keyName",
        "user_assigned_identity_id": "userAssignedIdentityId",
    },
)
class SynapseWorkspaceCustomerManagedKey:
    def __init__(
        self,
        *,
        key_versionless_id: builtins.str,
        key_name: typing.Optional[builtins.str] = None,
        user_assigned_identity_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_versionless_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#key_versionless_id SynapseWorkspace#key_versionless_id}.
        :param key_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#key_name SynapseWorkspace#key_name}.
        :param user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#user_assigned_identity_id SynapseWorkspace#user_assigned_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc875d71642879d63cc9577e9b6567d7f22611c727fe7a3ddd00ef19d0301970)
            check_type(argname="argument key_versionless_id", value=key_versionless_id, expected_type=type_hints["key_versionless_id"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument user_assigned_identity_id", value=user_assigned_identity_id, expected_type=type_hints["user_assigned_identity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_versionless_id": key_versionless_id,
        }
        if key_name is not None:
            self._values["key_name"] = key_name
        if user_assigned_identity_id is not None:
            self._values["user_assigned_identity_id"] = user_assigned_identity_id

    @builtins.property
    def key_versionless_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#key_versionless_id SynapseWorkspace#key_versionless_id}.'''
        result = self._values.get("key_versionless_id")
        assert result is not None, "Required property 'key_versionless_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#key_name SynapseWorkspace#key_name}.'''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#user_assigned_identity_id SynapseWorkspace#user_assigned_identity_id}.'''
        result = self._values.get("user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseWorkspaceCustomerManagedKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseWorkspaceCustomerManagedKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceCustomerManagedKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d438b6641a6e34c243971979714c0901dc70ab7c16ab561a4260b532d1af72f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyName")
    def reset_key_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyName", []))

    @jsii.member(jsii_name="resetUserAssignedIdentityId")
    def reset_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserAssignedIdentityId", []))

    @builtins.property
    @jsii.member(jsii_name="keyNameInput")
    def key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVersionlessIdInput")
    def key_versionless_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVersionlessIdInput"))

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityIdInput")
    def user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="keyName")
    def key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyName"))

    @key_name.setter
    def key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208869e3714bad339d0953116c1781cb14fc94e5c99d82e5857c447a028ceebc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVersionlessId")
    def key_versionless_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVersionlessId"))

    @key_versionless_id.setter
    def key_versionless_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc15761b43a3f0ec76c0ae91ea348ba94f742d1221f00561c623b41f2b29df31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVersionlessId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userAssignedIdentityId")
    def user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userAssignedIdentityId"))

    @user_assigned_identity_id.setter
    def user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6622c4ac55958781a396fea604d932d37de56d7c92afe6059875d7562ddc64e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SynapseWorkspaceCustomerManagedKey]:
        return typing.cast(typing.Optional[SynapseWorkspaceCustomerManagedKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SynapseWorkspaceCustomerManagedKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b825fb07ee09e52eac613e4349961b971b9b1177e15e31e2096395e1be42af84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceGithubRepo",
    jsii_struct_bases=[],
    name_mapping={
        "account_name": "accountName",
        "branch_name": "branchName",
        "repository_name": "repositoryName",
        "root_folder": "rootFolder",
        "git_url": "gitUrl",
        "last_commit_id": "lastCommitId",
    },
)
class SynapseWorkspaceGithubRepo:
    def __init__(
        self,
        *,
        account_name: builtins.str,
        branch_name: builtins.str,
        repository_name: builtins.str,
        root_folder: builtins.str,
        git_url: typing.Optional[builtins.str] = None,
        last_commit_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#account_name SynapseWorkspace#account_name}.
        :param branch_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#branch_name SynapseWorkspace#branch_name}.
        :param repository_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#repository_name SynapseWorkspace#repository_name}.
        :param root_folder: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#root_folder SynapseWorkspace#root_folder}.
        :param git_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#git_url SynapseWorkspace#git_url}.
        :param last_commit_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#last_commit_id SynapseWorkspace#last_commit_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36435424d8a1baf8ed041ad3992baec370004dbc6e40f0345247b08c7f2e8772)
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument root_folder", value=root_folder, expected_type=type_hints["root_folder"])
            check_type(argname="argument git_url", value=git_url, expected_type=type_hints["git_url"])
            check_type(argname="argument last_commit_id", value=last_commit_id, expected_type=type_hints["last_commit_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "branch_name": branch_name,
            "repository_name": repository_name,
            "root_folder": root_folder,
        }
        if git_url is not None:
            self._values["git_url"] = git_url
        if last_commit_id is not None:
            self._values["last_commit_id"] = last_commit_id

    @builtins.property
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#account_name SynapseWorkspace#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#branch_name SynapseWorkspace#branch_name}.'''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#repository_name SynapseWorkspace#repository_name}.'''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def root_folder(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#root_folder SynapseWorkspace#root_folder}.'''
        result = self._values.get("root_folder")
        assert result is not None, "Required property 'root_folder' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#git_url SynapseWorkspace#git_url}.'''
        result = self._values.get("git_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def last_commit_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#last_commit_id SynapseWorkspace#last_commit_id}.'''
        result = self._values.get("last_commit_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseWorkspaceGithubRepo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseWorkspaceGithubRepoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceGithubRepoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6550999c5f399818cb80f23a348c9e3b85e4ac483ef7a35978fe24f69fc40be1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGitUrl")
    def reset_git_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitUrl", []))

    @jsii.member(jsii_name="resetLastCommitId")
    def reset_last_commit_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLastCommitId", []))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="branchNameInput")
    def branch_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "branchNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gitUrlInput")
    def git_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="lastCommitIdInput")
    def last_commit_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lastCommitIdInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryNameInput")
    def repository_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootFolderInput")
    def root_folder_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootFolderInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8392c54b2543e17b6829fcba1071d9fd42cbf0e269bbd7eb30fdaeab3bf7ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @branch_name.setter
    def branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600adf92282d411360a310629076a04b9dbf4a84aaf1cbb0c53d49030c5f065d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gitUrl")
    def git_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitUrl"))

    @git_url.setter
    def git_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c226a94876a97994728d5ba52db390401b2600939262a721a8a16d780ffb699a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lastCommitId")
    def last_commit_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastCommitId"))

    @last_commit_id.setter
    def last_commit_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41cf54c2ee09e1c728a9c642465e3954fa893851fc2ce95eda0343cb97e9a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lastCommitId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryName"))

    @repository_name.setter
    def repository_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4233086a605ae0ff612f1ffca6e17cb5ec6861b922badbc0b6adabb5b3e50cfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootFolder")
    def root_folder(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootFolder"))

    @root_folder.setter
    def root_folder(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d004f4c60df6aa18c79c6269972d67b5ebd663d9591158d4b036f4efc8ca58de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootFolder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SynapseWorkspaceGithubRepo]:
        return typing.cast(typing.Optional[SynapseWorkspaceGithubRepo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SynapseWorkspaceGithubRepo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e138ca8dff989bce622c935cc5e58442b75ae5aa9efc90c3149b21bd65dc3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class SynapseWorkspaceIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#type SynapseWorkspace#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#identity_ids SynapseWorkspace#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a22100379d835c4debd5f1071081e1284ad009dd36177ed57885bb4c7ab76a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#type SynapseWorkspace#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#identity_ids SynapseWorkspace#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseWorkspaceIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseWorkspaceIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__477bda555a0767d79af1e10aafc0256db0881e6a5f4bf0569e58a850fc47e4b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fd90c7ac7e61726b4fbe0ff0074d7b5786e3901f2d21a1b9fee2b21304cf2e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f6cc64205f58bf5ef268451562284d4c84ca07b8669c8f5809fb9808267359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SynapseWorkspaceIdentity]:
        return typing.cast(typing.Optional[SynapseWorkspaceIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SynapseWorkspaceIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4902992d0bb2273db51035a58c3b5c02a9811cff7cca1927b2f3f9cd7debb717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SynapseWorkspaceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#create SynapseWorkspace#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#delete SynapseWorkspace#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#read SynapseWorkspace#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#update SynapseWorkspace#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29db9c53c100cb74f5d14d85b71c49791a79dc54f411e791a9bef6f0b0bea47f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#create SynapseWorkspace#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#delete SynapseWorkspace#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#read SynapseWorkspace#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/synapse_workspace#update SynapseWorkspace#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynapseWorkspaceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SynapseWorkspaceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.synapseWorkspace.SynapseWorkspaceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61382112c59e712e864a9586d202a281c51b74f5a511ccbc0f3c065f4d55b22a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9edd1675de7f8ca938c7bfa9c7f1000dffab9caccf42ce93deb8f52e949f9c74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127eade8aa0869e719a749cc0f341f2a33acfafead7d56afeffe8cc169cc8d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f2eeb300ed13f7658f45bb7a0ecb80e111ef406cc9ff8f95e7c2f884f9d677e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78195635a226eed26a84bb320321dfb7d1b879cdf3835eab5f5f71abc935cf16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynapseWorkspaceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynapseWorkspaceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynapseWorkspaceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514e8aed25c3478f0661c848a3418627ad8f7f6c78ba46fff4948e0cf8629352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SynapseWorkspace",
    "SynapseWorkspaceAzureDevopsRepo",
    "SynapseWorkspaceAzureDevopsRepoOutputReference",
    "SynapseWorkspaceConfig",
    "SynapseWorkspaceCustomerManagedKey",
    "SynapseWorkspaceCustomerManagedKeyOutputReference",
    "SynapseWorkspaceGithubRepo",
    "SynapseWorkspaceGithubRepoOutputReference",
    "SynapseWorkspaceIdentity",
    "SynapseWorkspaceIdentityOutputReference",
    "SynapseWorkspaceTimeouts",
    "SynapseWorkspaceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__415c7ed4a685a7b9c91323444402101bb804b8294a3be518a1f4f9a775a616e5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    storage_data_lake_gen2_filesystem_id: builtins.str,
    azuread_authentication_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_devops_repo: typing.Optional[typing.Union[SynapseWorkspaceAzureDevopsRepo, typing.Dict[builtins.str, typing.Any]]] = None,
    compute_subnet_id: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[typing.Union[SynapseWorkspaceCustomerManagedKey, typing.Dict[builtins.str, typing.Any]]] = None,
    data_exfiltration_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    github_repo: typing.Optional[typing.Union[SynapseWorkspaceGithubRepo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[SynapseWorkspaceIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    linking_allowed_for_aad_tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    managed_virtual_network_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purview_id: typing.Optional[builtins.str] = None,
    sql_administrator_login: typing.Optional[builtins.str] = None,
    sql_administrator_login_password: typing.Optional[builtins.str] = None,
    sql_identity_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SynapseWorkspaceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__de0942db4d32465745f05e63022e496f45f7afff2729511228e2a830fcf13c93(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d11377f50d39be5ebd9532d22ec44c1bba1e8f75d7b654e1ad5a2bcf0f182b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0473514189445b567d2bc41237cd68d3c0a86bccce45126184bbf2fa4ca5693a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644d10cfc73b4595ae2812c9c4ca5581d1f2ba4780b82624024ed2704a6e2a6d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50cf5d949c3b1cdcd73a1d613cc5350c6cb64b878425b487cf54f60827be35d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61bf03dab344d63b557bba9917755a2c013a1396ab89fa12cac48d752fa8f5b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e5460e4c78a1e5353e430a0abad402e7e331ed16627ba25abec42572be9fa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38fc9023d8c2fda86dcca642700f71203c565cb37ea9fe80f8d1dee23bcb22fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c227d42239fe8da65d38a7debf726ef06ebda212b04d71d4d0448ae673ce54f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad98ad1aef1e5d6a8ead4a089a56b6d29606e0971da5bdae97cc674f1189fa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae8d4a349fc44b52b0d91526a70f7eefeaa2b83d37f6056a908fba91619b15f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6302d4b221c86e832d2f9dca52ab780e00919469c887954ecdbce5a4dd4dbac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d8bc25b895c9ad95f8272df88fa5cc88ba12ed5c9e97bca16f44038b3a95d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__669735306c716c0b2dec92e8b2475fe36386cd299b848cc8792261a268bb9dea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48ae0c50bd0351ddad8ee6d92997473b11497adbdcc01233ebd811c5ff323a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d749a64a3bcbf4f67915ef74f617ac4c0ccfb6e77bdd749035efc73c7e325f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bdf041b10cbc35e948f4c886e394f2e716bf7e51e676d819ead517bfa8fd3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0788301f1546ecd3139b259ff934aaae6ecff6c2b7794c6fa188d3443c2961b1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45483737a6a3dc2aab9e2b84b4095c5e06a3bb700ec05304737b791702bd03f(
    *,
    account_name: builtins.str,
    branch_name: builtins.str,
    project_name: builtins.str,
    repository_name: builtins.str,
    root_folder: builtins.str,
    last_commit_id: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb5aa156bc8a75ddf0fa21d792f3019aeb983d576691e9ab431a4aaf64caf11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18328a0557f17305ac11f2c7843fd97453c98d1f5c0e7acd1254c637dab5e93f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e528bdefca032f14d10338a9ac74899e9934cd7c65f83d745c2f56936e6018d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e09a500dc2acec4007f925822c4aff292f408af14313a8ab338ec35fd19e25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd80af48d30c34eaf2d4a3d241d03693691d98a8a2cc1b5c56010927c422369f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49465469ea1158c2af7a848b0c0877ae2c44fd2908cffcde452a53e5aa23510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe79f397353c2009f6af906111fffe2da370a03c1cd2f361421f1b7d900437e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273763090cc7454a8f5c04197e9a4d041fa889f0324c32f46563ea6897a96c39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d878e5695a9af8cce5a5e243fe33dca30600cc4286685708bd4b8b257ffe89(
    value: typing.Optional[SynapseWorkspaceAzureDevopsRepo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dfcf6df084475ad9694b89c1c519158d0f1edf56c42e7e4cf5504064edcfe65(
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
    storage_data_lake_gen2_filesystem_id: builtins.str,
    azuread_authentication_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_devops_repo: typing.Optional[typing.Union[SynapseWorkspaceAzureDevopsRepo, typing.Dict[builtins.str, typing.Any]]] = None,
    compute_subnet_id: typing.Optional[builtins.str] = None,
    customer_managed_key: typing.Optional[typing.Union[SynapseWorkspaceCustomerManagedKey, typing.Dict[builtins.str, typing.Any]]] = None,
    data_exfiltration_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    github_repo: typing.Optional[typing.Union[SynapseWorkspaceGithubRepo, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[SynapseWorkspaceIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    linking_allowed_for_aad_tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    managed_resource_group_name: typing.Optional[builtins.str] = None,
    managed_virtual_network_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purview_id: typing.Optional[builtins.str] = None,
    sql_administrator_login: typing.Optional[builtins.str] = None,
    sql_administrator_login_password: typing.Optional[builtins.str] = None,
    sql_identity_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SynapseWorkspaceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc875d71642879d63cc9577e9b6567d7f22611c727fe7a3ddd00ef19d0301970(
    *,
    key_versionless_id: builtins.str,
    key_name: typing.Optional[builtins.str] = None,
    user_assigned_identity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d438b6641a6e34c243971979714c0901dc70ab7c16ab561a4260b532d1af72f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208869e3714bad339d0953116c1781cb14fc94e5c99d82e5857c447a028ceebc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc15761b43a3f0ec76c0ae91ea348ba94f742d1221f00561c623b41f2b29df31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6622c4ac55958781a396fea604d932d37de56d7c92afe6059875d7562ddc64e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b825fb07ee09e52eac613e4349961b971b9b1177e15e31e2096395e1be42af84(
    value: typing.Optional[SynapseWorkspaceCustomerManagedKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36435424d8a1baf8ed041ad3992baec370004dbc6e40f0345247b08c7f2e8772(
    *,
    account_name: builtins.str,
    branch_name: builtins.str,
    repository_name: builtins.str,
    root_folder: builtins.str,
    git_url: typing.Optional[builtins.str] = None,
    last_commit_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6550999c5f399818cb80f23a348c9e3b85e4ac483ef7a35978fe24f69fc40be1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8392c54b2543e17b6829fcba1071d9fd42cbf0e269bbd7eb30fdaeab3bf7ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600adf92282d411360a310629076a04b9dbf4a84aaf1cbb0c53d49030c5f065d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c226a94876a97994728d5ba52db390401b2600939262a721a8a16d780ffb699a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41cf54c2ee09e1c728a9c642465e3954fa893851fc2ce95eda0343cb97e9a23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4233086a605ae0ff612f1ffca6e17cb5ec6861b922badbc0b6adabb5b3e50cfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d004f4c60df6aa18c79c6269972d67b5ebd663d9591158d4b036f4efc8ca58de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e138ca8dff989bce622c935cc5e58442b75ae5aa9efc90c3149b21bd65dc3a(
    value: typing.Optional[SynapseWorkspaceGithubRepo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a22100379d835c4debd5f1071081e1284ad009dd36177ed57885bb4c7ab76a(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477bda555a0767d79af1e10aafc0256db0881e6a5f4bf0569e58a850fc47e4b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd90c7ac7e61726b4fbe0ff0074d7b5786e3901f2d21a1b9fee2b21304cf2e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f6cc64205f58bf5ef268451562284d4c84ca07b8669c8f5809fb9808267359(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4902992d0bb2273db51035a58c3b5c02a9811cff7cca1927b2f3f9cd7debb717(
    value: typing.Optional[SynapseWorkspaceIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29db9c53c100cb74f5d14d85b71c49791a79dc54f411e791a9bef6f0b0bea47f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61382112c59e712e864a9586d202a281c51b74f5a511ccbc0f3c065f4d55b22a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9edd1675de7f8ca938c7bfa9c7f1000dffab9caccf42ce93deb8f52e949f9c74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127eade8aa0869e719a749cc0f341f2a33acfafead7d56afeffe8cc169cc8d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f2eeb300ed13f7658f45bb7a0ecb80e111ef406cc9ff8f95e7c2f884f9d677e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78195635a226eed26a84bb320321dfb7d1b879cdf3835eab5f5f71abc935cf16(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514e8aed25c3478f0661c848a3418627ad8f7f6c78ba46fff4948e0cf8629352(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SynapseWorkspaceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

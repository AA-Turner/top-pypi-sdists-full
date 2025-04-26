r'''
# `provider`

Refer to the Terraform Registry for docs: [`azuread`](https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs).
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


class AzureadProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azuread.provider.AzureadProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs azuread}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ado_pipeline_service_connection_id: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_certificate_password: typing.Optional[builtins.str] = None,
        client_certificate_path: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_id_file_path: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_file_path: typing.Optional[builtins.str] = None,
        disable_terraform_partner_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata_host: typing.Optional[builtins.str] = None,
        msi_endpoint: typing.Optional[builtins.str] = None,
        oidc_request_token: typing.Optional[builtins.str] = None,
        oidc_request_url: typing.Optional[builtins.str] = None,
        oidc_token: typing.Optional[builtins.str] = None,
        oidc_token_file_path: typing.Optional[builtins.str] = None,
        partner_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_aks_workload_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_cli: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_msi: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_oidc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs azuread} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param ado_pipeline_service_connection_id: The Azure DevOps Pipeline Service Connection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#ado_pipeline_service_connection_id AzureadProvider#ado_pipeline_service_connection_id}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#alias AzureadProvider#alias}
        :param client_certificate: Base64 encoded PKCS#12 certificate bundle to use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate AzureadProvider#client_certificate}
        :param client_certificate_password: The password to decrypt the Client Certificate. For use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate_password AzureadProvider#client_certificate_password}
        :param client_certificate_path: The path to the Client Certificate associated with the Service Principal for use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate_path AzureadProvider#client_certificate_path}
        :param client_id: The Client ID which should be used for service principal authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_id AzureadProvider#client_id}
        :param client_id_file_path: The path to a file containing the Client ID which should be used for service principal authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_id_file_path AzureadProvider#client_id_file_path}
        :param client_secret: The application password to use when authenticating as a Service Principal using a Client Secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_secret AzureadProvider#client_secret}
        :param client_secret_file_path: The path to a file containing the application password to use when authenticating as a Service Principal using a Client Secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_secret_file_path AzureadProvider#client_secret_file_path}
        :param disable_terraform_partner_id: Disable the Terraform Partner ID, which is used if a custom ``partner_id`` isn't specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#disable_terraform_partner_id AzureadProvider#disable_terraform_partner_id}
        :param environment: The cloud environment which should be used. Possible values are: ``global`` (also ``public``), ``usgovernmentl4`` (also ``usgovernment``), ``usgovernmentl5`` (also ``dod``), and ``china``. Defaults to ``global``. Not used and should not be specified when ``metadata_host`` is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#environment AzureadProvider#environment}
        :param metadata_host: The Hostname which should be used for the Azure Metadata Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#metadata_host AzureadProvider#metadata_host}
        :param msi_endpoint: The path to a custom endpoint for Managed Identity - in most circumstances this should be detected automatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#msi_endpoint AzureadProvider#msi_endpoint}
        :param oidc_request_token: The bearer token for the request to the OIDC provider. For use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_request_token AzureadProvider#oidc_request_token}
        :param oidc_request_url: The URL for the OIDC provider from which to request an ID token. For use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_request_url AzureadProvider#oidc_request_url}
        :param oidc_token: The ID token for use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_token AzureadProvider#oidc_token}
        :param oidc_token_file_path: The path to a file containing an ID token for use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_token_file_path AzureadProvider#oidc_token_file_path}
        :param partner_id: A GUID/UUID that is registered with Microsoft to facilitate partner resource usage attribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#partner_id AzureadProvider#partner_id}
        :param tenant_id: The Tenant ID which should be used. Works with all authentication methods except Managed Identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#tenant_id AzureadProvider#tenant_id}
        :param use_aks_workload_identity: Allow Azure AKS Workload Identity to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_aks_workload_identity AzureadProvider#use_aks_workload_identity}
        :param use_cli: Allow Azure CLI to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_cli AzureadProvider#use_cli}
        :param use_msi: Allow Managed Identity to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_msi AzureadProvider#use_msi}
        :param use_oidc: Allow OpenID Connect to be used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_oidc AzureadProvider#use_oidc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__988275f1bceb7bfc887f76bbf357fe55dd063c6c42e4093c45cd0ed4a89a301c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AzureadProviderConfig(
            ado_pipeline_service_connection_id=ado_pipeline_service_connection_id,
            alias=alias,
            client_certificate=client_certificate,
            client_certificate_password=client_certificate_password,
            client_certificate_path=client_certificate_path,
            client_id=client_id,
            client_id_file_path=client_id_file_path,
            client_secret=client_secret,
            client_secret_file_path=client_secret_file_path,
            disable_terraform_partner_id=disable_terraform_partner_id,
            environment=environment,
            metadata_host=metadata_host,
            msi_endpoint=msi_endpoint,
            oidc_request_token=oidc_request_token,
            oidc_request_url=oidc_request_url,
            oidc_token=oidc_token,
            oidc_token_file_path=oidc_token_file_path,
            partner_id=partner_id,
            tenant_id=tenant_id,
            use_aks_workload_identity=use_aks_workload_identity,
            use_cli=use_cli,
            use_msi=use_msi,
            use_oidc=use_oidc,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a AzureadProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AzureadProvider to import.
        :param import_from_id: The id of the existing AzureadProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AzureadProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c571843c7e9bc697561acad0c39ce32f02c184654985757f68bc5f692d9c71f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetAdoPipelineServiceConnectionId")
    def reset_ado_pipeline_service_connection_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdoPipelineServiceConnectionId", []))

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetClientCertificate")
    def reset_client_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificate", []))

    @jsii.member(jsii_name="resetClientCertificatePassword")
    def reset_client_certificate_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificatePassword", []))

    @jsii.member(jsii_name="resetClientCertificatePath")
    def reset_client_certificate_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificatePath", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientIdFilePath")
    def reset_client_id_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientIdFilePath", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretFilePath")
    def reset_client_secret_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretFilePath", []))

    @jsii.member(jsii_name="resetDisableTerraformPartnerId")
    def reset_disable_terraform_partner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableTerraformPartnerId", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetMetadataHost")
    def reset_metadata_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataHost", []))

    @jsii.member(jsii_name="resetMsiEndpoint")
    def reset_msi_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMsiEndpoint", []))

    @jsii.member(jsii_name="resetOidcRequestToken")
    def reset_oidc_request_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcRequestToken", []))

    @jsii.member(jsii_name="resetOidcRequestUrl")
    def reset_oidc_request_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcRequestUrl", []))

    @jsii.member(jsii_name="resetOidcToken")
    def reset_oidc_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcToken", []))

    @jsii.member(jsii_name="resetOidcTokenFilePath")
    def reset_oidc_token_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOidcTokenFilePath", []))

    @jsii.member(jsii_name="resetPartnerId")
    def reset_partner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartnerId", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetUseAksWorkloadIdentity")
    def reset_use_aks_workload_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseAksWorkloadIdentity", []))

    @jsii.member(jsii_name="resetUseCli")
    def reset_use_cli(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCli", []))

    @jsii.member(jsii_name="resetUseMsi")
    def reset_use_msi(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseMsi", []))

    @jsii.member(jsii_name="resetUseOidc")
    def reset_use_oidc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseOidc", []))

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
    @jsii.member(jsii_name="adoPipelineServiceConnectionIdInput")
    def ado_pipeline_service_connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adoPipelineServiceConnectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateInput")
    def client_certificate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePasswordInput")
    def client_certificate_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificatePasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePathInput")
    def client_certificate_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificatePathInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdFilePathInput")
    def client_id_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretFilePathInput")
    def client_secret_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="disableTerraformPartnerIdInput")
    def disable_terraform_partner_id_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableTerraformPartnerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentInput")
    def environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataHostInput")
    def metadata_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataHostInput"))

    @builtins.property
    @jsii.member(jsii_name="msiEndpointInput")
    def msi_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "msiEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcRequestTokenInput")
    def oidc_request_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcRequestTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcRequestUrlInput")
    def oidc_request_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcRequestUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenFilePathInput")
    def oidc_token_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcTokenFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="oidcTokenInput")
    def oidc_token_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="partnerIdInput")
    def partner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partnerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="useAksWorkloadIdentityInput")
    def use_aks_workload_identity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useAksWorkloadIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="useCliInput")
    def use_cli_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCliInput"))

    @builtins.property
    @jsii.member(jsii_name="useMsiInput")
    def use_msi_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useMsiInput"))

    @builtins.property
    @jsii.member(jsii_name="useOidcInput")
    def use_oidc_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useOidcInput"))

    @builtins.property
    @jsii.member(jsii_name="adoPipelineServiceConnectionId")
    def ado_pipeline_service_connection_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adoPipelineServiceConnectionId"))

    @ado_pipeline_service_connection_id.setter
    def ado_pipeline_service_connection_id(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32046c113291ab26445581eb92c7c0d2991426886fff1241c143e046812933e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adoPipelineServiceConnectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c9123f3c31cce0e808ea5f1238f0873bfe0c125ee44dd336086e3a426d1684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f558248aceda7bf34da99c300d7c4ab1e88938daf875d71dafa7d2826f343a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePassword")
    def client_certificate_password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificatePassword"))

    @client_certificate_password.setter
    def client_certificate_password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853b56605156833524a7858163ea2ef648b8c7b7be7bbd88e59ce15f6b0ebbf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePath")
    def client_certificate_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificatePath"))

    @client_certificate_path.setter
    def client_certificate_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c39e1936a384a2dbd4b4853cc01af6048e00eb0a5628c6be61480c49a2f64d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificatePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22c13c457537b4ca3be2c155a99a3b99ef077c2912d1a99852a7d67f89d2379a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientIdFilePath")
    def client_id_file_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdFilePath"))

    @client_id_file_path.setter
    def client_id_file_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64ec49865e2e956828d7e2275b441857ea040cf3ace112392ff656b4a11c0c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientIdFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5beb043a12114a2cfcef4e70f693a383e6e3bbf38ebfe0f16f3ccd95868dd74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretFilePath")
    def client_secret_file_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretFilePath"))

    @client_secret_file_path.setter
    def client_secret_file_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4172fd486bf7b82ff9a21807e1e19d81244fe67d4424b3b1e7241583cf55a7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableTerraformPartnerId")
    def disable_terraform_partner_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableTerraformPartnerId"))

    @disable_terraform_partner_id.setter
    def disable_terraform_partner_id(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7089b07992bebb496a70c3bf6c75dc2ea6d4f8a3082c8894bbac30b3a365d5d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTerraformPartnerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ea6c7487cbce1e374bc796dcc7b6311eec4ef5f71d6c3577b6131d6689ec9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataHost")
    def metadata_host(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataHost"))

    @metadata_host.setter
    def metadata_host(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2e40e561ca9d677534ec8069a58420206cf98415ac1c5da2b53f52fd54d5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msiEndpoint")
    def msi_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "msiEndpoint"))

    @msi_endpoint.setter
    def msi_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc0be5d08764a73ec857ad9a2ac19875aaba587b0505eea8c00cd176275ad3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msiEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oidcRequestToken")
    def oidc_request_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcRequestToken"))

    @oidc_request_token.setter
    def oidc_request_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a51da8de841e970ef7244a4a9c6080177b9501ef51aebb0bbaf367374d8839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcRequestToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oidcRequestUrl")
    def oidc_request_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcRequestUrl"))

    @oidc_request_url.setter
    def oidc_request_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b20bfbd05faa6972cf8c4ca7954c2305427bed04cb725cf28d85a131ceea76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcRequestUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcToken"))

    @oidc_token.setter
    def oidc_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4896c98e4e3cc840acaa43a7d0ced3a92518a661efd88ea935eadf2f68d54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oidcTokenFilePath")
    def oidc_token_file_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcTokenFilePath"))

    @oidc_token_file_path.setter
    def oidc_token_file_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579e49f8b64d464769aa74154ad61a34aabd5371022588539de41ef0aba01cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcTokenFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partnerId")
    def partner_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partnerId"))

    @partner_id.setter
    def partner_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e16eb3c1d7cc4316857a9aebbb5513bdf43177bba11c0657ed61afa6805343fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae778f7e418aa1b39cbc57ab4c52e7643eec89242e7a59d567fcacd7c278b6a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useAksWorkloadIdentity")
    def use_aks_workload_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useAksWorkloadIdentity"))

    @use_aks_workload_identity.setter
    def use_aks_workload_identity(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c287b07579a47bb6cb31af536579b8d32a1d90c570e275f77f2ab0d551c5f674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useAksWorkloadIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCli")
    def use_cli(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCli"))

    @use_cli.setter
    def use_cli(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db12d4c35b45ddb8f328d887f71ae54132f9493f9ecd39ea4e3e5d7c0db66192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCli", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useMsi")
    def use_msi(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useMsi"))

    @use_msi.setter
    def use_msi(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb580307d103b3e33eff4b0adb4ed591e77c185986a84aca71d9b0324ad20afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useMsi", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useOidc")
    def use_oidc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useOidc"))

    @use_oidc.setter
    def use_oidc(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e8677471e1d2f6b4997670fd0b88f6e70d58788fdeb74355ddd9d0ea87a553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOidc", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azuread.provider.AzureadProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ado_pipeline_service_connection_id": "adoPipelineServiceConnectionId",
        "alias": "alias",
        "client_certificate": "clientCertificate",
        "client_certificate_password": "clientCertificatePassword",
        "client_certificate_path": "clientCertificatePath",
        "client_id": "clientId",
        "client_id_file_path": "clientIdFilePath",
        "client_secret": "clientSecret",
        "client_secret_file_path": "clientSecretFilePath",
        "disable_terraform_partner_id": "disableTerraformPartnerId",
        "environment": "environment",
        "metadata_host": "metadataHost",
        "msi_endpoint": "msiEndpoint",
        "oidc_request_token": "oidcRequestToken",
        "oidc_request_url": "oidcRequestUrl",
        "oidc_token": "oidcToken",
        "oidc_token_file_path": "oidcTokenFilePath",
        "partner_id": "partnerId",
        "tenant_id": "tenantId",
        "use_aks_workload_identity": "useAksWorkloadIdentity",
        "use_cli": "useCli",
        "use_msi": "useMsi",
        "use_oidc": "useOidc",
    },
)
class AzureadProviderConfig:
    def __init__(
        self,
        *,
        ado_pipeline_service_connection_id: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_certificate_password: typing.Optional[builtins.str] = None,
        client_certificate_path: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_id_file_path: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_file_path: typing.Optional[builtins.str] = None,
        disable_terraform_partner_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata_host: typing.Optional[builtins.str] = None,
        msi_endpoint: typing.Optional[builtins.str] = None,
        oidc_request_token: typing.Optional[builtins.str] = None,
        oidc_request_url: typing.Optional[builtins.str] = None,
        oidc_token: typing.Optional[builtins.str] = None,
        oidc_token_file_path: typing.Optional[builtins.str] = None,
        partner_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_aks_workload_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_cli: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_msi: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_oidc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ado_pipeline_service_connection_id: The Azure DevOps Pipeline Service Connection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#ado_pipeline_service_connection_id AzureadProvider#ado_pipeline_service_connection_id}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#alias AzureadProvider#alias}
        :param client_certificate: Base64 encoded PKCS#12 certificate bundle to use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate AzureadProvider#client_certificate}
        :param client_certificate_password: The password to decrypt the Client Certificate. For use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate_password AzureadProvider#client_certificate_password}
        :param client_certificate_path: The path to the Client Certificate associated with the Service Principal for use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate_path AzureadProvider#client_certificate_path}
        :param client_id: The Client ID which should be used for service principal authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_id AzureadProvider#client_id}
        :param client_id_file_path: The path to a file containing the Client ID which should be used for service principal authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_id_file_path AzureadProvider#client_id_file_path}
        :param client_secret: The application password to use when authenticating as a Service Principal using a Client Secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_secret AzureadProvider#client_secret}
        :param client_secret_file_path: The path to a file containing the application password to use when authenticating as a Service Principal using a Client Secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_secret_file_path AzureadProvider#client_secret_file_path}
        :param disable_terraform_partner_id: Disable the Terraform Partner ID, which is used if a custom ``partner_id`` isn't specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#disable_terraform_partner_id AzureadProvider#disable_terraform_partner_id}
        :param environment: The cloud environment which should be used. Possible values are: ``global`` (also ``public``), ``usgovernmentl4`` (also ``usgovernment``), ``usgovernmentl5`` (also ``dod``), and ``china``. Defaults to ``global``. Not used and should not be specified when ``metadata_host`` is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#environment AzureadProvider#environment}
        :param metadata_host: The Hostname which should be used for the Azure Metadata Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#metadata_host AzureadProvider#metadata_host}
        :param msi_endpoint: The path to a custom endpoint for Managed Identity - in most circumstances this should be detected automatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#msi_endpoint AzureadProvider#msi_endpoint}
        :param oidc_request_token: The bearer token for the request to the OIDC provider. For use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_request_token AzureadProvider#oidc_request_token}
        :param oidc_request_url: The URL for the OIDC provider from which to request an ID token. For use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_request_url AzureadProvider#oidc_request_url}
        :param oidc_token: The ID token for use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_token AzureadProvider#oidc_token}
        :param oidc_token_file_path: The path to a file containing an ID token for use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_token_file_path AzureadProvider#oidc_token_file_path}
        :param partner_id: A GUID/UUID that is registered with Microsoft to facilitate partner resource usage attribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#partner_id AzureadProvider#partner_id}
        :param tenant_id: The Tenant ID which should be used. Works with all authentication methods except Managed Identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#tenant_id AzureadProvider#tenant_id}
        :param use_aks_workload_identity: Allow Azure AKS Workload Identity to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_aks_workload_identity AzureadProvider#use_aks_workload_identity}
        :param use_cli: Allow Azure CLI to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_cli AzureadProvider#use_cli}
        :param use_msi: Allow Managed Identity to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_msi AzureadProvider#use_msi}
        :param use_oidc: Allow OpenID Connect to be used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_oidc AzureadProvider#use_oidc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f0905ad810448c8e11b39eb5a782dc762149bdb6189d128ca02599bb25014f)
            check_type(argname="argument ado_pipeline_service_connection_id", value=ado_pipeline_service_connection_id, expected_type=type_hints["ado_pipeline_service_connection_id"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_certificate_password", value=client_certificate_password, expected_type=type_hints["client_certificate_password"])
            check_type(argname="argument client_certificate_path", value=client_certificate_path, expected_type=type_hints["client_certificate_path"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_id_file_path", value=client_id_file_path, expected_type=type_hints["client_id_file_path"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_file_path", value=client_secret_file_path, expected_type=type_hints["client_secret_file_path"])
            check_type(argname="argument disable_terraform_partner_id", value=disable_terraform_partner_id, expected_type=type_hints["disable_terraform_partner_id"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument metadata_host", value=metadata_host, expected_type=type_hints["metadata_host"])
            check_type(argname="argument msi_endpoint", value=msi_endpoint, expected_type=type_hints["msi_endpoint"])
            check_type(argname="argument oidc_request_token", value=oidc_request_token, expected_type=type_hints["oidc_request_token"])
            check_type(argname="argument oidc_request_url", value=oidc_request_url, expected_type=type_hints["oidc_request_url"])
            check_type(argname="argument oidc_token", value=oidc_token, expected_type=type_hints["oidc_token"])
            check_type(argname="argument oidc_token_file_path", value=oidc_token_file_path, expected_type=type_hints["oidc_token_file_path"])
            check_type(argname="argument partner_id", value=partner_id, expected_type=type_hints["partner_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument use_aks_workload_identity", value=use_aks_workload_identity, expected_type=type_hints["use_aks_workload_identity"])
            check_type(argname="argument use_cli", value=use_cli, expected_type=type_hints["use_cli"])
            check_type(argname="argument use_msi", value=use_msi, expected_type=type_hints["use_msi"])
            check_type(argname="argument use_oidc", value=use_oidc, expected_type=type_hints["use_oidc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ado_pipeline_service_connection_id is not None:
            self._values["ado_pipeline_service_connection_id"] = ado_pipeline_service_connection_id
        if alias is not None:
            self._values["alias"] = alias
        if client_certificate is not None:
            self._values["client_certificate"] = client_certificate
        if client_certificate_password is not None:
            self._values["client_certificate_password"] = client_certificate_password
        if client_certificate_path is not None:
            self._values["client_certificate_path"] = client_certificate_path
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_id_file_path is not None:
            self._values["client_id_file_path"] = client_id_file_path
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_file_path is not None:
            self._values["client_secret_file_path"] = client_secret_file_path
        if disable_terraform_partner_id is not None:
            self._values["disable_terraform_partner_id"] = disable_terraform_partner_id
        if environment is not None:
            self._values["environment"] = environment
        if metadata_host is not None:
            self._values["metadata_host"] = metadata_host
        if msi_endpoint is not None:
            self._values["msi_endpoint"] = msi_endpoint
        if oidc_request_token is not None:
            self._values["oidc_request_token"] = oidc_request_token
        if oidc_request_url is not None:
            self._values["oidc_request_url"] = oidc_request_url
        if oidc_token is not None:
            self._values["oidc_token"] = oidc_token
        if oidc_token_file_path is not None:
            self._values["oidc_token_file_path"] = oidc_token_file_path
        if partner_id is not None:
            self._values["partner_id"] = partner_id
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if use_aks_workload_identity is not None:
            self._values["use_aks_workload_identity"] = use_aks_workload_identity
        if use_cli is not None:
            self._values["use_cli"] = use_cli
        if use_msi is not None:
            self._values["use_msi"] = use_msi
        if use_oidc is not None:
            self._values["use_oidc"] = use_oidc

    @builtins.property
    def ado_pipeline_service_connection_id(self) -> typing.Optional[builtins.str]:
        '''The Azure DevOps Pipeline Service Connection ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#ado_pipeline_service_connection_id AzureadProvider#ado_pipeline_service_connection_id}
        '''
        result = self._values.get("ado_pipeline_service_connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#alias AzureadProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded PKCS#12 certificate bundle to use when authenticating as a Service Principal using a Client Certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate AzureadProvider#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_password(self) -> typing.Optional[builtins.str]:
        '''The password to decrypt the Client Certificate. For use when authenticating as a Service Principal using a Client Certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate_password AzureadProvider#client_certificate_password}
        '''
        result = self._values.get("client_certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_path(self) -> typing.Optional[builtins.str]:
        '''The path to the Client Certificate associated with the Service Principal for use when authenticating as a Service Principal using a Client Certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_certificate_path AzureadProvider#client_certificate_path}
        '''
        result = self._values.get("client_certificate_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The Client ID which should be used for service principal authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_id AzureadProvider#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id_file_path(self) -> typing.Optional[builtins.str]:
        '''The path to a file containing the Client ID which should be used for service principal authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_id_file_path AzureadProvider#client_id_file_path}
        '''
        result = self._values.get("client_id_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The application password to use when authenticating as a Service Principal using a Client Secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_secret AzureadProvider#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_file_path(self) -> typing.Optional[builtins.str]:
        '''The path to a file containing the application password to use when authenticating as a Service Principal using a Client Secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#client_secret_file_path AzureadProvider#client_secret_file_path}
        '''
        result = self._values.get("client_secret_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_terraform_partner_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the Terraform Partner ID, which is used if a custom ``partner_id`` isn't specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#disable_terraform_partner_id AzureadProvider#disable_terraform_partner_id}
        '''
        result = self._values.get("disable_terraform_partner_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        '''The cloud environment which should be used.

        Possible values are: ``global`` (also ``public``), ``usgovernmentl4`` (also ``usgovernment``), ``usgovernmentl5`` (also ``dod``), and ``china``. Defaults to ``global``. Not used and should not be specified when ``metadata_host`` is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#environment AzureadProvider#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata_host(self) -> typing.Optional[builtins.str]:
        '''The Hostname which should be used for the Azure Metadata Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#metadata_host AzureadProvider#metadata_host}
        '''
        result = self._values.get("metadata_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def msi_endpoint(self) -> typing.Optional[builtins.str]:
        '''The path to a custom endpoint for Managed Identity - in most circumstances this should be detected automatically.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#msi_endpoint AzureadProvider#msi_endpoint}
        '''
        result = self._values.get("msi_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_request_token(self) -> typing.Optional[builtins.str]:
        '''The bearer token for the request to the OIDC provider.

        For use when authenticating as a Service Principal using OpenID Connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_request_token AzureadProvider#oidc_request_token}
        '''
        result = self._values.get("oidc_request_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_request_url(self) -> typing.Optional[builtins.str]:
        '''The URL for the OIDC provider from which to request an ID token.

        For use when authenticating as a Service Principal using OpenID Connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_request_url AzureadProvider#oidc_request_url}
        '''
        result = self._values.get("oidc_request_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_token(self) -> typing.Optional[builtins.str]:
        '''The ID token for use when authenticating as a Service Principal using OpenID Connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_token AzureadProvider#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_token_file_path(self) -> typing.Optional[builtins.str]:
        '''The path to a file containing an ID token for use when authenticating as a Service Principal using OpenID Connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#oidc_token_file_path AzureadProvider#oidc_token_file_path}
        '''
        result = self._values.get("oidc_token_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partner_id(self) -> typing.Optional[builtins.str]:
        '''A GUID/UUID that is registered with Microsoft to facilitate partner resource usage attribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#partner_id AzureadProvider#partner_id}
        '''
        result = self._values.get("partner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''The Tenant ID which should be used. Works with all authentication methods except Managed Identity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#tenant_id AzureadProvider#tenant_id}
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_aks_workload_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow Azure AKS Workload Identity to be used for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_aks_workload_identity AzureadProvider#use_aks_workload_identity}
        '''
        result = self._values.get("use_aks_workload_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_cli(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow Azure CLI to be used for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_cli AzureadProvider#use_cli}
        '''
        result = self._values.get("use_cli")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_msi(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow Managed Identity to be used for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_msi AzureadProvider#use_msi}
        '''
        result = self._values.get("use_msi")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_oidc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow OpenID Connect to be used for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azuread/3.3.0/docs#use_oidc AzureadProvider#use_oidc}
        '''
        result = self._values.get("use_oidc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzureadProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AzureadProvider",
    "AzureadProviderConfig",
]

publication.publish()

def _typecheckingstub__988275f1bceb7bfc887f76bbf357fe55dd063c6c42e4093c45cd0ed4a89a301c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ado_pipeline_service_connection_id: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_certificate_password: typing.Optional[builtins.str] = None,
    client_certificate_path: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_id_file_path: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_file_path: typing.Optional[builtins.str] = None,
    disable_terraform_partner_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment: typing.Optional[builtins.str] = None,
    metadata_host: typing.Optional[builtins.str] = None,
    msi_endpoint: typing.Optional[builtins.str] = None,
    oidc_request_token: typing.Optional[builtins.str] = None,
    oidc_request_url: typing.Optional[builtins.str] = None,
    oidc_token: typing.Optional[builtins.str] = None,
    oidc_token_file_path: typing.Optional[builtins.str] = None,
    partner_id: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    use_aks_workload_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_cli: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_msi: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_oidc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c571843c7e9bc697561acad0c39ce32f02c184654985757f68bc5f692d9c71f7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32046c113291ab26445581eb92c7c0d2991426886fff1241c143e046812933e9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c9123f3c31cce0e808ea5f1238f0873bfe0c125ee44dd336086e3a426d1684(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f558248aceda7bf34da99c300d7c4ab1e88938daf875d71dafa7d2826f343a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853b56605156833524a7858163ea2ef648b8c7b7be7bbd88e59ce15f6b0ebbf9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c39e1936a384a2dbd4b4853cc01af6048e00eb0a5628c6be61480c49a2f64d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c13c457537b4ca3be2c155a99a3b99ef077c2912d1a99852a7d67f89d2379a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64ec49865e2e956828d7e2275b441857ea040cf3ace112392ff656b4a11c0c6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5beb043a12114a2cfcef4e70f693a383e6e3bbf38ebfe0f16f3ccd95868dd74c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4172fd486bf7b82ff9a21807e1e19d81244fe67d4424b3b1e7241583cf55a7a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7089b07992bebb496a70c3bf6c75dc2ea6d4f8a3082c8894bbac30b3a365d5d7(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ea6c7487cbce1e374bc796dcc7b6311eec4ef5f71d6c3577b6131d6689ec9f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2e40e561ca9d677534ec8069a58420206cf98415ac1c5da2b53f52fd54d5f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc0be5d08764a73ec857ad9a2ac19875aaba587b0505eea8c00cd176275ad3a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a51da8de841e970ef7244a4a9c6080177b9501ef51aebb0bbaf367374d8839(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b20bfbd05faa6972cf8c4ca7954c2305427bed04cb725cf28d85a131ceea76(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4896c98e4e3cc840acaa43a7d0ced3a92518a661efd88ea935eadf2f68d54b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579e49f8b64d464769aa74154ad61a34aabd5371022588539de41ef0aba01cd1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16eb3c1d7cc4316857a9aebbb5513bdf43177bba11c0657ed61afa6805343fd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae778f7e418aa1b39cbc57ab4c52e7643eec89242e7a59d567fcacd7c278b6a9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c287b07579a47bb6cb31af536579b8d32a1d90c570e275f77f2ab0d551c5f674(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db12d4c35b45ddb8f328d887f71ae54132f9493f9ecd39ea4e3e5d7c0db66192(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb580307d103b3e33eff4b0adb4ed591e77c185986a84aca71d9b0324ad20afa(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e8677471e1d2f6b4997670fd0b88f6e70d58788fdeb74355ddd9d0ea87a553(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f0905ad810448c8e11b39eb5a782dc762149bdb6189d128ca02599bb25014f(
    *,
    ado_pipeline_service_connection_id: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_certificate_password: typing.Optional[builtins.str] = None,
    client_certificate_path: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_id_file_path: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_file_path: typing.Optional[builtins.str] = None,
    disable_terraform_partner_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment: typing.Optional[builtins.str] = None,
    metadata_host: typing.Optional[builtins.str] = None,
    msi_endpoint: typing.Optional[builtins.str] = None,
    oidc_request_token: typing.Optional[builtins.str] = None,
    oidc_request_url: typing.Optional[builtins.str] = None,
    oidc_token: typing.Optional[builtins.str] = None,
    oidc_token_file_path: typing.Optional[builtins.str] = None,
    partner_id: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    use_aks_workload_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_cli: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_msi: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_oidc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

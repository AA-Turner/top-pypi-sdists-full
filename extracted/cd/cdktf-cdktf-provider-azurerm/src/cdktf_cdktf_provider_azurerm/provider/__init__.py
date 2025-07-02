r'''
# `provider`

Refer to the Terraform Registry for docs: [`azurerm`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs).
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


class AzurermProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs azurerm}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ado_pipeline_service_connection_id: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        auxiliary_tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_certificate_password: typing.Optional[builtins.str] = None,
        client_certificate_path: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_id_file_path: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_file_path: typing.Optional[builtins.str] = None,
        disable_correlation_request_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_terraform_partner_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment: typing.Optional[builtins.str] = None,
        features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata_host: typing.Optional[builtins.str] = None,
        msi_api_version: typing.Optional[builtins.str] = None,
        msi_endpoint: typing.Optional[builtins.str] = None,
        oidc_request_token: typing.Optional[builtins.str] = None,
        oidc_request_url: typing.Optional[builtins.str] = None,
        oidc_token: typing.Optional[builtins.str] = None,
        oidc_token_file_path: typing.Optional[builtins.str] = None,
        partner_id: typing.Optional[builtins.str] = None,
        resource_provider_registrations: typing.Optional[builtins.str] = None,
        resource_providers_to_register: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_provider_registration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_use_azuread: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_aks_workload_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_cli: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_msi: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_oidc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs azurerm} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param ado_pipeline_service_connection_id: The Azure DevOps Pipeline Service Connection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#ado_pipeline_service_connection_id AzurermProvider#ado_pipeline_service_connection_id}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#alias AzurermProvider#alias}
        :param auxiliary_tenant_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#auxiliary_tenant_ids AzurermProvider#auxiliary_tenant_ids}.
        :param client_certificate: Base64 encoded PKCS#12 certificate bundle to use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate AzurermProvider#client_certificate}
        :param client_certificate_password: The password associated with the Client Certificate. For use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate_password AzurermProvider#client_certificate_password}
        :param client_certificate_path: The path to the Client Certificate associated with the Service Principal for use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate_path AzurermProvider#client_certificate_path}
        :param client_id: The Client ID which should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_id AzurermProvider#client_id}
        :param client_id_file_path: The path to a file containing the Client ID which should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_id_file_path AzurermProvider#client_id_file_path}
        :param client_secret: The Client Secret which should be used. For use When authenticating as a Service Principal using a Client Secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_secret AzurermProvider#client_secret}
        :param client_secret_file_path: The path to a file containing the Client Secret which should be used. For use When authenticating as a Service Principal using a Client Secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_secret_file_path AzurermProvider#client_secret_file_path}
        :param disable_correlation_request_id: This will disable the x-ms-correlation-request-id header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#disable_correlation_request_id AzurermProvider#disable_correlation_request_id}
        :param disable_terraform_partner_id: This will disable the Terraform Partner ID which is used if a custom ``partner_id`` isn't specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#disable_terraform_partner_id AzurermProvider#disable_terraform_partner_id}
        :param environment: The Cloud Environment which should be used. Possible values are public, usgovernment, and china. Defaults to public. Not used and should not be specified when ``metadata_host`` is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#environment AzurermProvider#environment}
        :param features: features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#features AzurermProvider#features}
        :param metadata_host: The Hostname which should be used for the Azure Metadata Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#metadata_host AzurermProvider#metadata_host}
        :param msi_api_version: The API version to use for Managed Service Identity (IMDS) - for cases where the default API version is not supported by the endpoint. e.g. for Azure Container Apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#msi_api_version AzurermProvider#msi_api_version}
        :param msi_endpoint: The path to a custom endpoint for Managed Service Identity - in most circumstances this should be detected automatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#msi_endpoint AzurermProvider#msi_endpoint}
        :param oidc_request_token: The bearer token for the request to the OIDC provider. For use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_request_token AzurermProvider#oidc_request_token}
        :param oidc_request_url: The URL for the OIDC provider from which to request an ID token. For use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_request_url AzurermProvider#oidc_request_url}
        :param oidc_token: The OIDC ID token for use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_token AzurermProvider#oidc_token}
        :param oidc_token_file_path: The path to a file containing an OIDC ID token for use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_token_file_path AzurermProvider#oidc_token_file_path}
        :param partner_id: A GUID/UUID that is registered with Microsoft to facilitate partner resource usage attribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#partner_id AzurermProvider#partner_id}
        :param resource_provider_registrations: The set of Resource Providers which should be automatically registered for the subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#resource_provider_registrations AzurermProvider#resource_provider_registrations}
        :param resource_providers_to_register: A list of Resource Providers to explicitly register for the subscription, in addition to those specified by the ``resource_provider_registrations`` property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#resource_providers_to_register AzurermProvider#resource_providers_to_register}
        :param skip_provider_registration: Should the AzureRM Provider skip registering all of the Resource Providers that it supports, if they're not already registered? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#skip_provider_registration AzurermProvider#skip_provider_registration}
        :param storage_use_azuread: Should the AzureRM Provider use Azure AD Authentication when accessing the Storage Data Plane APIs? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#storage_use_azuread AzurermProvider#storage_use_azuread}
        :param subscription_id: The Subscription ID which should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#subscription_id AzurermProvider#subscription_id}
        :param tenant_id: The Tenant ID which should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#tenant_id AzurermProvider#tenant_id}
        :param use_aks_workload_identity: Allow Azure AKS Workload Identity to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_aks_workload_identity AzurermProvider#use_aks_workload_identity}
        :param use_cli: Allow Azure CLI to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_cli AzurermProvider#use_cli}
        :param use_msi: Allow Managed Service Identity to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_msi AzurermProvider#use_msi}
        :param use_oidc: Allow OpenID Connect to be used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_oidc AzurermProvider#use_oidc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d612cb0ea42e0d04a986b52842f95dbbb6757bb17c26ccf9ccc136e8c917d94)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AzurermProviderConfig(
            ado_pipeline_service_connection_id=ado_pipeline_service_connection_id,
            alias=alias,
            auxiliary_tenant_ids=auxiliary_tenant_ids,
            client_certificate=client_certificate,
            client_certificate_password=client_certificate_password,
            client_certificate_path=client_certificate_path,
            client_id=client_id,
            client_id_file_path=client_id_file_path,
            client_secret=client_secret,
            client_secret_file_path=client_secret_file_path,
            disable_correlation_request_id=disable_correlation_request_id,
            disable_terraform_partner_id=disable_terraform_partner_id,
            environment=environment,
            features=features,
            metadata_host=metadata_host,
            msi_api_version=msi_api_version,
            msi_endpoint=msi_endpoint,
            oidc_request_token=oidc_request_token,
            oidc_request_url=oidc_request_url,
            oidc_token=oidc_token,
            oidc_token_file_path=oidc_token_file_path,
            partner_id=partner_id,
            resource_provider_registrations=resource_provider_registrations,
            resource_providers_to_register=resource_providers_to_register,
            skip_provider_registration=skip_provider_registration,
            storage_use_azuread=storage_use_azuread,
            subscription_id=subscription_id,
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
        '''Generates CDKTF code for importing a AzurermProvider resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AzurermProvider to import.
        :param import_from_id: The id of the existing AzurermProvider that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AzurermProvider to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f28cd221c0a8956938dbcfe651dedc5e126e3b1eae3f49b2a14350d362dda34)
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

    @jsii.member(jsii_name="resetAuxiliaryTenantIds")
    def reset_auxiliary_tenant_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuxiliaryTenantIds", []))

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

    @jsii.member(jsii_name="resetDisableCorrelationRequestId")
    def reset_disable_correlation_request_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableCorrelationRequestId", []))

    @jsii.member(jsii_name="resetDisableTerraformPartnerId")
    def reset_disable_terraform_partner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableTerraformPartnerId", []))

    @jsii.member(jsii_name="resetEnvironment")
    def reset_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironment", []))

    @jsii.member(jsii_name="resetFeatures")
    def reset_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFeatures", []))

    @jsii.member(jsii_name="resetMetadataHost")
    def reset_metadata_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadataHost", []))

    @jsii.member(jsii_name="resetMsiApiVersion")
    def reset_msi_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMsiApiVersion", []))

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

    @jsii.member(jsii_name="resetResourceProviderRegistrations")
    def reset_resource_provider_registrations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceProviderRegistrations", []))

    @jsii.member(jsii_name="resetResourceProvidersToRegister")
    def reset_resource_providers_to_register(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceProvidersToRegister", []))

    @jsii.member(jsii_name="resetSkipProviderRegistration")
    def reset_skip_provider_registration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipProviderRegistration", []))

    @jsii.member(jsii_name="resetStorageUseAzuread")
    def reset_storage_use_azuread(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageUseAzuread", []))

    @jsii.member(jsii_name="resetSubscriptionId")
    def reset_subscription_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriptionId", []))

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
    @jsii.member(jsii_name="auxiliaryTenantIdsInput")
    def auxiliary_tenant_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "auxiliaryTenantIdsInput"))

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
    @jsii.member(jsii_name="disableCorrelationRequestIdInput")
    def disable_correlation_request_id_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableCorrelationRequestIdInput"))

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
    @jsii.member(jsii_name="featuresInput")
    def features_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeatures"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeatures"]]], jsii.get(self, "featuresInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataHostInput")
    def metadata_host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataHostInput"))

    @builtins.property
    @jsii.member(jsii_name="msiApiVersionInput")
    def msi_api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "msiApiVersionInput"))

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
    @jsii.member(jsii_name="resourceProviderRegistrationsInput")
    def resource_provider_registrations_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceProviderRegistrationsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceProvidersToRegisterInput")
    def resource_providers_to_register_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceProvidersToRegisterInput"))

    @builtins.property
    @jsii.member(jsii_name="skipProviderRegistrationInput")
    def skip_provider_registration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipProviderRegistrationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageUseAzureadInput")
    def storage_use_azuread_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storageUseAzureadInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionIdInput")
    def subscription_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5183b547764c4a96ee74ac4edcd6d9762a7466424753a0e1ae294bd3c102dc9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adoPipelineServiceConnectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1523e91cdfb6f51086599bf200611ee10faa93fa9c37cdcb2d1c2421bd024d65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="auxiliaryTenantIds")
    def auxiliary_tenant_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "auxiliaryTenantIds"))

    @auxiliary_tenant_ids.setter
    def auxiliary_tenant_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9144096b220f881cb7f1f8923f8f13a85f6451eb6a4be08deecf0a112868cc05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auxiliaryTenantIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificate")
    def client_certificate(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificate"))

    @client_certificate.setter
    def client_certificate(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04bfa0d73cfe140336d37aff39792146dbcee79074ecabd1541cb355ab3b13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePassword")
    def client_certificate_password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificatePassword"))

    @client_certificate_password.setter
    def client_certificate_password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b6b921a8825272b14b71faa7994f1051c57fe216a706279640d802f5fe686c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificatePassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificatePath")
    def client_certificate_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificatePath"))

    @client_certificate_path.setter
    def client_certificate_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a8fe55c591ab2bf461b30580d6e9d9ce5683b2444f4864037bc8417a1a5543d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificatePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a47f4524dafc3df2503ef2768dc1d3a33c61710321c08052dcaea3b50df7115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientIdFilePath")
    def client_id_file_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdFilePath"))

    @client_id_file_path.setter
    def client_id_file_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10af9b007767870f98e04964077f0e222c06c04116005ed6d1a19c472fd35da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientIdFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81663fcf4065492bb889303dd916452140ef72c9514f5d08b5b5bbc837b09e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretFilePath")
    def client_secret_file_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretFilePath"))

    @client_secret_file_path.setter
    def client_secret_file_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0e6d5416f03f701cb609986a5b0f86616222d75bf609b1bd24ec4d8a41d98e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableCorrelationRequestId")
    def disable_correlation_request_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableCorrelationRequestId"))

    @disable_correlation_request_id.setter
    def disable_correlation_request_id(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__614ef03a9911ecc789c792ff87ce3414745f45f5b63ce5238d62dd0285b79558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableCorrelationRequestId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__d230bb82634caaf5a25592c647569ada140c5628156ec71b7c911177ebe12611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableTerraformPartnerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environment"))

    @environment.setter
    def environment(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c408f69d016c58c04f4685d1521340e839de2374117924ac0394703128632a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="features")
    def features(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeatures"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeatures"]]], jsii.get(self, "features"))

    @features.setter
    def features(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeatures"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f70fad43d7cc3b607cfcd5ad95e72d2ae33000149eff41eee601f6353ebef61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "features", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metadataHost")
    def metadata_host(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataHost"))

    @metadata_host.setter
    def metadata_host(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__853a6ee43e3456e010e42412a57e38f5b6bb4143231be6bf372af406232ab19e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadataHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msiApiVersion")
    def msi_api_version(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "msiApiVersion"))

    @msi_api_version.setter
    def msi_api_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604790c21de537c0ccaca4efcc5b9f46235e452e5c421da26ef3f2b6964f16b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msiApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="msiEndpoint")
    def msi_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "msiEndpoint"))

    @msi_endpoint.setter
    def msi_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3469bbdc46cf49a92158fabd40550df8e50d9c90d44d909dd6066df60d0554cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "msiEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oidcRequestToken")
    def oidc_request_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcRequestToken"))

    @oidc_request_token.setter
    def oidc_request_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e4c9bcafa230931323166957cfcbbc1bbae68d2a1735f59fe891b5b154c63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcRequestToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oidcRequestUrl")
    def oidc_request_url(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcRequestUrl"))

    @oidc_request_url.setter
    def oidc_request_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3cbe862b08533674079b1f87d406cf0e32a31f042b9fd9c7e5f59f2f85ca07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcRequestUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oidcToken")
    def oidc_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcToken"))

    @oidc_token.setter
    def oidc_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bb1aad80fa9cbb2d4b1ee8a12f74c3571f9eedf01bcc6bd2e7577e1a0e8f23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcToken", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oidcTokenFilePath")
    def oidc_token_file_path(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oidcTokenFilePath"))

    @oidc_token_file_path.setter
    def oidc_token_file_path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__776fc9fdf447742adcdbefa31bba132bc5793cd9c99fbf50692878ba778d9ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oidcTokenFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="partnerId")
    def partner_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "partnerId"))

    @partner_id.setter
    def partner_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ce974198a33a4d4e2589cc1c8780a5f02228abf0cd9c42a52b6b80abac2ea3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "partnerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceProviderRegistrations")
    def resource_provider_registrations(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceProviderRegistrations"))

    @resource_provider_registrations.setter
    def resource_provider_registrations(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9fb0cd060971865274740d84bcd52c9a74ca1058b1c2ee1f16b923e2bf8e44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceProviderRegistrations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceProvidersToRegister")
    def resource_providers_to_register(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceProvidersToRegister"))

    @resource_providers_to_register.setter
    def resource_providers_to_register(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb4ecdcf0cd96ef9d562e52ea0965adf8e353a736facabda9bb60dafdc486e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceProvidersToRegister", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipProviderRegistration")
    def skip_provider_registration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipProviderRegistration"))

    @skip_provider_registration.setter
    def skip_provider_registration(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7dd1db69fdae658eedd4e3ba4c9c96b07f3da7292764b7f64338f48e0b2b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipProviderRegistration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageUseAzuread")
    def storage_use_azuread(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storageUseAzuread"))

    @storage_use_azuread.setter
    def storage_use_azuread(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5d877412d16ee85b2925c17956f3b9aec7a714c671817f13545e8d51d2827f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageUseAzuread", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionId")
    def subscription_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionId"))

    @subscription_id.setter
    def subscription_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d88ffe9921ac7cd02d903ce6579e6ed4eb24d309d90a0e3d5b9aa2649b72243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0a0d0150d026f85d25daa830c51bda7892e81be958c2bbde9a0b0fb3c76fea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__643d3eb598148f207d2669b5593b40077ad06e32a7aee0d281f5579a490f12f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f6434be286962ce3ae2d2650d973cb379046962ef75bfccd038152cd059e750)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7079a2ae9ee82de109aceb15c7743472a653d8aa361d70e3c922f934e60a554c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eb023b4999764e37b3b7e10ac8f7c7e11c1cd30137627621e3f021998846f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useOidc", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "ado_pipeline_service_connection_id": "adoPipelineServiceConnectionId",
        "alias": "alias",
        "auxiliary_tenant_ids": "auxiliaryTenantIds",
        "client_certificate": "clientCertificate",
        "client_certificate_password": "clientCertificatePassword",
        "client_certificate_path": "clientCertificatePath",
        "client_id": "clientId",
        "client_id_file_path": "clientIdFilePath",
        "client_secret": "clientSecret",
        "client_secret_file_path": "clientSecretFilePath",
        "disable_correlation_request_id": "disableCorrelationRequestId",
        "disable_terraform_partner_id": "disableTerraformPartnerId",
        "environment": "environment",
        "features": "features",
        "metadata_host": "metadataHost",
        "msi_api_version": "msiApiVersion",
        "msi_endpoint": "msiEndpoint",
        "oidc_request_token": "oidcRequestToken",
        "oidc_request_url": "oidcRequestUrl",
        "oidc_token": "oidcToken",
        "oidc_token_file_path": "oidcTokenFilePath",
        "partner_id": "partnerId",
        "resource_provider_registrations": "resourceProviderRegistrations",
        "resource_providers_to_register": "resourceProvidersToRegister",
        "skip_provider_registration": "skipProviderRegistration",
        "storage_use_azuread": "storageUseAzuread",
        "subscription_id": "subscriptionId",
        "tenant_id": "tenantId",
        "use_aks_workload_identity": "useAksWorkloadIdentity",
        "use_cli": "useCli",
        "use_msi": "useMsi",
        "use_oidc": "useOidc",
    },
)
class AzurermProviderConfig:
    def __init__(
        self,
        *,
        ado_pipeline_service_connection_id: typing.Optional[builtins.str] = None,
        alias: typing.Optional[builtins.str] = None,
        auxiliary_tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_certificate: typing.Optional[builtins.str] = None,
        client_certificate_password: typing.Optional[builtins.str] = None,
        client_certificate_path: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_id_file_path: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_file_path: typing.Optional[builtins.str] = None,
        disable_correlation_request_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_terraform_partner_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment: typing.Optional[builtins.str] = None,
        features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeatures", typing.Dict[builtins.str, typing.Any]]]]] = None,
        metadata_host: typing.Optional[builtins.str] = None,
        msi_api_version: typing.Optional[builtins.str] = None,
        msi_endpoint: typing.Optional[builtins.str] = None,
        oidc_request_token: typing.Optional[builtins.str] = None,
        oidc_request_url: typing.Optional[builtins.str] = None,
        oidc_token: typing.Optional[builtins.str] = None,
        oidc_token_file_path: typing.Optional[builtins.str] = None,
        partner_id: typing.Optional[builtins.str] = None,
        resource_provider_registrations: typing.Optional[builtins.str] = None,
        resource_providers_to_register: typing.Optional[typing.Sequence[builtins.str]] = None,
        skip_provider_registration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage_use_azuread: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_aks_workload_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_cli: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_msi: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_oidc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param ado_pipeline_service_connection_id: The Azure DevOps Pipeline Service Connection ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#ado_pipeline_service_connection_id AzurermProvider#ado_pipeline_service_connection_id}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#alias AzurermProvider#alias}
        :param auxiliary_tenant_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#auxiliary_tenant_ids AzurermProvider#auxiliary_tenant_ids}.
        :param client_certificate: Base64 encoded PKCS#12 certificate bundle to use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate AzurermProvider#client_certificate}
        :param client_certificate_password: The password associated with the Client Certificate. For use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate_password AzurermProvider#client_certificate_password}
        :param client_certificate_path: The path to the Client Certificate associated with the Service Principal for use when authenticating as a Service Principal using a Client Certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate_path AzurermProvider#client_certificate_path}
        :param client_id: The Client ID which should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_id AzurermProvider#client_id}
        :param client_id_file_path: The path to a file containing the Client ID which should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_id_file_path AzurermProvider#client_id_file_path}
        :param client_secret: The Client Secret which should be used. For use When authenticating as a Service Principal using a Client Secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_secret AzurermProvider#client_secret}
        :param client_secret_file_path: The path to a file containing the Client Secret which should be used. For use When authenticating as a Service Principal using a Client Secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_secret_file_path AzurermProvider#client_secret_file_path}
        :param disable_correlation_request_id: This will disable the x-ms-correlation-request-id header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#disable_correlation_request_id AzurermProvider#disable_correlation_request_id}
        :param disable_terraform_partner_id: This will disable the Terraform Partner ID which is used if a custom ``partner_id`` isn't specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#disable_terraform_partner_id AzurermProvider#disable_terraform_partner_id}
        :param environment: The Cloud Environment which should be used. Possible values are public, usgovernment, and china. Defaults to public. Not used and should not be specified when ``metadata_host`` is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#environment AzurermProvider#environment}
        :param features: features block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#features AzurermProvider#features}
        :param metadata_host: The Hostname which should be used for the Azure Metadata Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#metadata_host AzurermProvider#metadata_host}
        :param msi_api_version: The API version to use for Managed Service Identity (IMDS) - for cases where the default API version is not supported by the endpoint. e.g. for Azure Container Apps. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#msi_api_version AzurermProvider#msi_api_version}
        :param msi_endpoint: The path to a custom endpoint for Managed Service Identity - in most circumstances this should be detected automatically. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#msi_endpoint AzurermProvider#msi_endpoint}
        :param oidc_request_token: The bearer token for the request to the OIDC provider. For use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_request_token AzurermProvider#oidc_request_token}
        :param oidc_request_url: The URL for the OIDC provider from which to request an ID token. For use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_request_url AzurermProvider#oidc_request_url}
        :param oidc_token: The OIDC ID token for use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_token AzurermProvider#oidc_token}
        :param oidc_token_file_path: The path to a file containing an OIDC ID token for use when authenticating as a Service Principal using OpenID Connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_token_file_path AzurermProvider#oidc_token_file_path}
        :param partner_id: A GUID/UUID that is registered with Microsoft to facilitate partner resource usage attribution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#partner_id AzurermProvider#partner_id}
        :param resource_provider_registrations: The set of Resource Providers which should be automatically registered for the subscription. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#resource_provider_registrations AzurermProvider#resource_provider_registrations}
        :param resource_providers_to_register: A list of Resource Providers to explicitly register for the subscription, in addition to those specified by the ``resource_provider_registrations`` property. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#resource_providers_to_register AzurermProvider#resource_providers_to_register}
        :param skip_provider_registration: Should the AzureRM Provider skip registering all of the Resource Providers that it supports, if they're not already registered? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#skip_provider_registration AzurermProvider#skip_provider_registration}
        :param storage_use_azuread: Should the AzureRM Provider use Azure AD Authentication when accessing the Storage Data Plane APIs? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#storage_use_azuread AzurermProvider#storage_use_azuread}
        :param subscription_id: The Subscription ID which should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#subscription_id AzurermProvider#subscription_id}
        :param tenant_id: The Tenant ID which should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#tenant_id AzurermProvider#tenant_id}
        :param use_aks_workload_identity: Allow Azure AKS Workload Identity to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_aks_workload_identity AzurermProvider#use_aks_workload_identity}
        :param use_cli: Allow Azure CLI to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_cli AzurermProvider#use_cli}
        :param use_msi: Allow Managed Service Identity to be used for Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_msi AzurermProvider#use_msi}
        :param use_oidc: Allow OpenID Connect to be used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_oidc AzurermProvider#use_oidc}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92eb1fb6a38ebf26e757be24396414a7b978b452e851810b7c1d8535d70ed5f2)
            check_type(argname="argument ado_pipeline_service_connection_id", value=ado_pipeline_service_connection_id, expected_type=type_hints["ado_pipeline_service_connection_id"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument auxiliary_tenant_ids", value=auxiliary_tenant_ids, expected_type=type_hints["auxiliary_tenant_ids"])
            check_type(argname="argument client_certificate", value=client_certificate, expected_type=type_hints["client_certificate"])
            check_type(argname="argument client_certificate_password", value=client_certificate_password, expected_type=type_hints["client_certificate_password"])
            check_type(argname="argument client_certificate_path", value=client_certificate_path, expected_type=type_hints["client_certificate_path"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_id_file_path", value=client_id_file_path, expected_type=type_hints["client_id_file_path"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_file_path", value=client_secret_file_path, expected_type=type_hints["client_secret_file_path"])
            check_type(argname="argument disable_correlation_request_id", value=disable_correlation_request_id, expected_type=type_hints["disable_correlation_request_id"])
            check_type(argname="argument disable_terraform_partner_id", value=disable_terraform_partner_id, expected_type=type_hints["disable_terraform_partner_id"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument features", value=features, expected_type=type_hints["features"])
            check_type(argname="argument metadata_host", value=metadata_host, expected_type=type_hints["metadata_host"])
            check_type(argname="argument msi_api_version", value=msi_api_version, expected_type=type_hints["msi_api_version"])
            check_type(argname="argument msi_endpoint", value=msi_endpoint, expected_type=type_hints["msi_endpoint"])
            check_type(argname="argument oidc_request_token", value=oidc_request_token, expected_type=type_hints["oidc_request_token"])
            check_type(argname="argument oidc_request_url", value=oidc_request_url, expected_type=type_hints["oidc_request_url"])
            check_type(argname="argument oidc_token", value=oidc_token, expected_type=type_hints["oidc_token"])
            check_type(argname="argument oidc_token_file_path", value=oidc_token_file_path, expected_type=type_hints["oidc_token_file_path"])
            check_type(argname="argument partner_id", value=partner_id, expected_type=type_hints["partner_id"])
            check_type(argname="argument resource_provider_registrations", value=resource_provider_registrations, expected_type=type_hints["resource_provider_registrations"])
            check_type(argname="argument resource_providers_to_register", value=resource_providers_to_register, expected_type=type_hints["resource_providers_to_register"])
            check_type(argname="argument skip_provider_registration", value=skip_provider_registration, expected_type=type_hints["skip_provider_registration"])
            check_type(argname="argument storage_use_azuread", value=storage_use_azuread, expected_type=type_hints["storage_use_azuread"])
            check_type(argname="argument subscription_id", value=subscription_id, expected_type=type_hints["subscription_id"])
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
        if auxiliary_tenant_ids is not None:
            self._values["auxiliary_tenant_ids"] = auxiliary_tenant_ids
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
        if disable_correlation_request_id is not None:
            self._values["disable_correlation_request_id"] = disable_correlation_request_id
        if disable_terraform_partner_id is not None:
            self._values["disable_terraform_partner_id"] = disable_terraform_partner_id
        if environment is not None:
            self._values["environment"] = environment
        if features is not None:
            self._values["features"] = features
        if metadata_host is not None:
            self._values["metadata_host"] = metadata_host
        if msi_api_version is not None:
            self._values["msi_api_version"] = msi_api_version
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
        if resource_provider_registrations is not None:
            self._values["resource_provider_registrations"] = resource_provider_registrations
        if resource_providers_to_register is not None:
            self._values["resource_providers_to_register"] = resource_providers_to_register
        if skip_provider_registration is not None:
            self._values["skip_provider_registration"] = skip_provider_registration
        if storage_use_azuread is not None:
            self._values["storage_use_azuread"] = storage_use_azuread
        if subscription_id is not None:
            self._values["subscription_id"] = subscription_id
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#ado_pipeline_service_connection_id AzurermProvider#ado_pipeline_service_connection_id}
        '''
        result = self._values.get("ado_pipeline_service_connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#alias AzurermProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auxiliary_tenant_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#auxiliary_tenant_ids AzurermProvider#auxiliary_tenant_ids}.'''
        result = self._values.get("auxiliary_tenant_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_certificate(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded PKCS#12 certificate bundle to use when authenticating as a Service Principal using a Client Certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate AzurermProvider#client_certificate}
        '''
        result = self._values.get("client_certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_password(self) -> typing.Optional[builtins.str]:
        '''The password associated with the Client Certificate. For use when authenticating as a Service Principal using a Client Certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate_password AzurermProvider#client_certificate_password}
        '''
        result = self._values.get("client_certificate_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_path(self) -> typing.Optional[builtins.str]:
        '''The path to the Client Certificate associated with the Service Principal for use when authenticating as a Service Principal using a Client Certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_certificate_path AzurermProvider#client_certificate_path}
        '''
        result = self._values.get("client_certificate_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''The Client ID which should be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_id AzurermProvider#client_id}
        '''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id_file_path(self) -> typing.Optional[builtins.str]:
        '''The path to a file containing the Client ID which should be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_id_file_path AzurermProvider#client_id_file_path}
        '''
        result = self._values.get("client_id_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The Client Secret which should be used. For use When authenticating as a Service Principal using a Client Secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_secret AzurermProvider#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_file_path(self) -> typing.Optional[builtins.str]:
        '''The path to a file containing the Client Secret which should be used.

        For use When authenticating as a Service Principal using a Client Secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#client_secret_file_path AzurermProvider#client_secret_file_path}
        '''
        result = self._values.get("client_secret_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_correlation_request_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This will disable the x-ms-correlation-request-id header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#disable_correlation_request_id AzurermProvider#disable_correlation_request_id}
        '''
        result = self._values.get("disable_correlation_request_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_terraform_partner_id(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This will disable the Terraform Partner ID which is used if a custom ``partner_id`` isn't specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#disable_terraform_partner_id AzurermProvider#disable_terraform_partner_id}
        '''
        result = self._values.get("disable_terraform_partner_id")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        '''The Cloud Environment which should be used.

        Possible values are public, usgovernment, and china. Defaults to public. Not used and should not be specified when ``metadata_host`` is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#environment AzurermProvider#environment}
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def features(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeatures"]]]:
        '''features block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#features AzurermProvider#features}
        '''
        result = self._values.get("features")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeatures"]]], result)

    @builtins.property
    def metadata_host(self) -> typing.Optional[builtins.str]:
        '''The Hostname which should be used for the Azure Metadata Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#metadata_host AzurermProvider#metadata_host}
        '''
        result = self._values.get("metadata_host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def msi_api_version(self) -> typing.Optional[builtins.str]:
        '''The API version to use for Managed Service Identity (IMDS) - for cases where the default API version is not supported by the endpoint.

        e.g. for Azure Container Apps.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#msi_api_version AzurermProvider#msi_api_version}
        '''
        result = self._values.get("msi_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def msi_endpoint(self) -> typing.Optional[builtins.str]:
        '''The path to a custom endpoint for Managed Service Identity - in most circumstances this should be detected automatically.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#msi_endpoint AzurermProvider#msi_endpoint}
        '''
        result = self._values.get("msi_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_request_token(self) -> typing.Optional[builtins.str]:
        '''The bearer token for the request to the OIDC provider.

        For use when authenticating as a Service Principal using OpenID Connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_request_token AzurermProvider#oidc_request_token}
        '''
        result = self._values.get("oidc_request_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_request_url(self) -> typing.Optional[builtins.str]:
        '''The URL for the OIDC provider from which to request an ID token.

        For use when authenticating as a Service Principal using OpenID Connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_request_url AzurermProvider#oidc_request_url}
        '''
        result = self._values.get("oidc_request_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_token(self) -> typing.Optional[builtins.str]:
        '''The OIDC ID token for use when authenticating as a Service Principal using OpenID Connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_token AzurermProvider#oidc_token}
        '''
        result = self._values.get("oidc_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc_token_file_path(self) -> typing.Optional[builtins.str]:
        '''The path to a file containing an OIDC ID token for use when authenticating as a Service Principal using OpenID Connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#oidc_token_file_path AzurermProvider#oidc_token_file_path}
        '''
        result = self._values.get("oidc_token_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partner_id(self) -> typing.Optional[builtins.str]:
        '''A GUID/UUID that is registered with Microsoft to facilitate partner resource usage attribution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#partner_id AzurermProvider#partner_id}
        '''
        result = self._values.get("partner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_provider_registrations(self) -> typing.Optional[builtins.str]:
        '''The set of Resource Providers which should be automatically registered for the subscription.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#resource_provider_registrations AzurermProvider#resource_provider_registrations}
        '''
        result = self._values.get("resource_provider_registrations")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_providers_to_register(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Resource Providers to explicitly register for the subscription, in addition to those specified by the ``resource_provider_registrations`` property.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#resource_providers_to_register AzurermProvider#resource_providers_to_register}
        '''
        result = self._values.get("resource_providers_to_register")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def skip_provider_registration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the AzureRM Provider skip registering all of the Resource Providers that it supports, if they're not already registered?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#skip_provider_registration AzurermProvider#skip_provider_registration}
        '''
        result = self._values.get("skip_provider_registration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def storage_use_azuread(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the AzureRM Provider use Azure AD Authentication when accessing the Storage Data Plane APIs?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#storage_use_azuread AzurermProvider#storage_use_azuread}
        '''
        result = self._values.get("storage_use_azuread")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def subscription_id(self) -> typing.Optional[builtins.str]:
        '''The Subscription ID which should be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#subscription_id AzurermProvider#subscription_id}
        '''
        result = self._values.get("subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''The Tenant ID which should be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#tenant_id AzurermProvider#tenant_id}
        '''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_aks_workload_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow Azure AKS Workload Identity to be used for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_aks_workload_identity AzurermProvider#use_aks_workload_identity}
        '''
        result = self._values.get("use_aks_workload_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_cli(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow Azure CLI to be used for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_cli AzurermProvider#use_cli}
        '''
        result = self._values.get("use_cli")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_msi(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow Managed Service Identity to be used for Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_msi AzurermProvider#use_msi}
        '''
        result = self._values.get("use_msi")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_oidc(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Allow OpenID Connect to be used for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#use_oidc AzurermProvider#use_oidc}
        '''
        result = self._values.get("use_oidc")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeatures",
    jsii_struct_bases=[],
    name_mapping={
        "api_management": "apiManagement",
        "app_configuration": "appConfiguration",
        "application_insights": "applicationInsights",
        "cognitive_account": "cognitiveAccount",
        "databricks_workspace": "databricksWorkspace",
        "key_vault": "keyVault",
        "log_analytics_workspace": "logAnalyticsWorkspace",
        "machine_learning": "machineLearning",
        "managed_disk": "managedDisk",
        "netapp": "netapp",
        "postgresql_flexible_server": "postgresqlFlexibleServer",
        "recovery_service": "recoveryService",
        "recovery_services_vaults": "recoveryServicesVaults",
        "resource_group": "resourceGroup",
        "storage": "storage",
        "subscription": "subscription",
        "template_deployment": "templateDeployment",
        "virtual_machine": "virtualMachine",
        "virtual_machine_scale_set": "virtualMachineScaleSet",
    },
)
class AzurermProviderFeatures:
    def __init__(
        self,
        *,
        api_management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesApiManagement", typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesAppConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        application_insights: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesApplicationInsights", typing.Dict[builtins.str, typing.Any]]]]] = None,
        cognitive_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesCognitiveAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        databricks_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesDatabricksWorkspace", typing.Dict[builtins.str, typing.Any]]]]] = None,
        key_vault: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesKeyVault", typing.Dict[builtins.str, typing.Any]]]]] = None,
        log_analytics_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesLogAnalyticsWorkspace", typing.Dict[builtins.str, typing.Any]]]]] = None,
        machine_learning: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesMachineLearning", typing.Dict[builtins.str, typing.Any]]]]] = None,
        managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesManagedDisk", typing.Dict[builtins.str, typing.Any]]]]] = None,
        netapp: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesNetapp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        postgresql_flexible_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesPostgresqlFlexibleServer", typing.Dict[builtins.str, typing.Any]]]]] = None,
        recovery_service: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesRecoveryService", typing.Dict[builtins.str, typing.Any]]]]] = None,
        recovery_services_vaults: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesRecoveryServicesVaults", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesResourceGroup", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesStorage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        subscription: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesSubscription", typing.Dict[builtins.str, typing.Any]]]]] = None,
        template_deployment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesTemplateDeployment", typing.Dict[builtins.str, typing.Any]]]]] = None,
        virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesVirtualMachine", typing.Dict[builtins.str, typing.Any]]]]] = None,
        virtual_machine_scale_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AzurermProviderFeaturesVirtualMachineScaleSet", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param api_management: api_management block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#api_management AzurermProvider#api_management}
        :param app_configuration: app_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#app_configuration AzurermProvider#app_configuration}
        :param application_insights: application_insights block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#application_insights AzurermProvider#application_insights}
        :param cognitive_account: cognitive_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#cognitive_account AzurermProvider#cognitive_account}
        :param databricks_workspace: databricks_workspace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#databricks_workspace AzurermProvider#databricks_workspace}
        :param key_vault: key_vault block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#key_vault AzurermProvider#key_vault}
        :param log_analytics_workspace: log_analytics_workspace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#log_analytics_workspace AzurermProvider#log_analytics_workspace}
        :param machine_learning: machine_learning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#machine_learning AzurermProvider#machine_learning}
        :param managed_disk: managed_disk block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#managed_disk AzurermProvider#managed_disk}
        :param netapp: netapp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#netapp AzurermProvider#netapp}
        :param postgresql_flexible_server: postgresql_flexible_server block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#postgresql_flexible_server AzurermProvider#postgresql_flexible_server}
        :param recovery_service: recovery_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recovery_service AzurermProvider#recovery_service}
        :param recovery_services_vaults: recovery_services_vaults block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recovery_services_vaults AzurermProvider#recovery_services_vaults}
        :param resource_group: resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#resource_group AzurermProvider#resource_group}
        :param storage: storage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#storage AzurermProvider#storage}
        :param subscription: subscription block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#subscription AzurermProvider#subscription}
        :param template_deployment: template_deployment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#template_deployment AzurermProvider#template_deployment}
        :param virtual_machine: virtual_machine block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#virtual_machine AzurermProvider#virtual_machine}
        :param virtual_machine_scale_set: virtual_machine_scale_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#virtual_machine_scale_set AzurermProvider#virtual_machine_scale_set}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a9682424bbe642a04b278e2b8074066025d046a35f868494b3173c6c7ab7965)
            check_type(argname="argument api_management", value=api_management, expected_type=type_hints["api_management"])
            check_type(argname="argument app_configuration", value=app_configuration, expected_type=type_hints["app_configuration"])
            check_type(argname="argument application_insights", value=application_insights, expected_type=type_hints["application_insights"])
            check_type(argname="argument cognitive_account", value=cognitive_account, expected_type=type_hints["cognitive_account"])
            check_type(argname="argument databricks_workspace", value=databricks_workspace, expected_type=type_hints["databricks_workspace"])
            check_type(argname="argument key_vault", value=key_vault, expected_type=type_hints["key_vault"])
            check_type(argname="argument log_analytics_workspace", value=log_analytics_workspace, expected_type=type_hints["log_analytics_workspace"])
            check_type(argname="argument machine_learning", value=machine_learning, expected_type=type_hints["machine_learning"])
            check_type(argname="argument managed_disk", value=managed_disk, expected_type=type_hints["managed_disk"])
            check_type(argname="argument netapp", value=netapp, expected_type=type_hints["netapp"])
            check_type(argname="argument postgresql_flexible_server", value=postgresql_flexible_server, expected_type=type_hints["postgresql_flexible_server"])
            check_type(argname="argument recovery_service", value=recovery_service, expected_type=type_hints["recovery_service"])
            check_type(argname="argument recovery_services_vaults", value=recovery_services_vaults, expected_type=type_hints["recovery_services_vaults"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument subscription", value=subscription, expected_type=type_hints["subscription"])
            check_type(argname="argument template_deployment", value=template_deployment, expected_type=type_hints["template_deployment"])
            check_type(argname="argument virtual_machine", value=virtual_machine, expected_type=type_hints["virtual_machine"])
            check_type(argname="argument virtual_machine_scale_set", value=virtual_machine_scale_set, expected_type=type_hints["virtual_machine_scale_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_management is not None:
            self._values["api_management"] = api_management
        if app_configuration is not None:
            self._values["app_configuration"] = app_configuration
        if application_insights is not None:
            self._values["application_insights"] = application_insights
        if cognitive_account is not None:
            self._values["cognitive_account"] = cognitive_account
        if databricks_workspace is not None:
            self._values["databricks_workspace"] = databricks_workspace
        if key_vault is not None:
            self._values["key_vault"] = key_vault
        if log_analytics_workspace is not None:
            self._values["log_analytics_workspace"] = log_analytics_workspace
        if machine_learning is not None:
            self._values["machine_learning"] = machine_learning
        if managed_disk is not None:
            self._values["managed_disk"] = managed_disk
        if netapp is not None:
            self._values["netapp"] = netapp
        if postgresql_flexible_server is not None:
            self._values["postgresql_flexible_server"] = postgresql_flexible_server
        if recovery_service is not None:
            self._values["recovery_service"] = recovery_service
        if recovery_services_vaults is not None:
            self._values["recovery_services_vaults"] = recovery_services_vaults
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if storage is not None:
            self._values["storage"] = storage
        if subscription is not None:
            self._values["subscription"] = subscription
        if template_deployment is not None:
            self._values["template_deployment"] = template_deployment
        if virtual_machine is not None:
            self._values["virtual_machine"] = virtual_machine
        if virtual_machine_scale_set is not None:
            self._values["virtual_machine_scale_set"] = virtual_machine_scale_set

    @builtins.property
    def api_management(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesApiManagement"]]]:
        '''api_management block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#api_management AzurermProvider#api_management}
        '''
        result = self._values.get("api_management")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesApiManagement"]]], result)

    @builtins.property
    def app_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesAppConfiguration"]]]:
        '''app_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#app_configuration AzurermProvider#app_configuration}
        '''
        result = self._values.get("app_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesAppConfiguration"]]], result)

    @builtins.property
    def application_insights(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesApplicationInsights"]]]:
        '''application_insights block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#application_insights AzurermProvider#application_insights}
        '''
        result = self._values.get("application_insights")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesApplicationInsights"]]], result)

    @builtins.property
    def cognitive_account(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesCognitiveAccount"]]]:
        '''cognitive_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#cognitive_account AzurermProvider#cognitive_account}
        '''
        result = self._values.get("cognitive_account")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesCognitiveAccount"]]], result)

    @builtins.property
    def databricks_workspace(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesDatabricksWorkspace"]]]:
        '''databricks_workspace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#databricks_workspace AzurermProvider#databricks_workspace}
        '''
        result = self._values.get("databricks_workspace")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesDatabricksWorkspace"]]], result)

    @builtins.property
    def key_vault(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesKeyVault"]]]:
        '''key_vault block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#key_vault AzurermProvider#key_vault}
        '''
        result = self._values.get("key_vault")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesKeyVault"]]], result)

    @builtins.property
    def log_analytics_workspace(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesLogAnalyticsWorkspace"]]]:
        '''log_analytics_workspace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#log_analytics_workspace AzurermProvider#log_analytics_workspace}
        '''
        result = self._values.get("log_analytics_workspace")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesLogAnalyticsWorkspace"]]], result)

    @builtins.property
    def machine_learning(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesMachineLearning"]]]:
        '''machine_learning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#machine_learning AzurermProvider#machine_learning}
        '''
        result = self._values.get("machine_learning")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesMachineLearning"]]], result)

    @builtins.property
    def managed_disk(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesManagedDisk"]]]:
        '''managed_disk block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#managed_disk AzurermProvider#managed_disk}
        '''
        result = self._values.get("managed_disk")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesManagedDisk"]]], result)

    @builtins.property
    def netapp(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesNetapp"]]]:
        '''netapp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#netapp AzurermProvider#netapp}
        '''
        result = self._values.get("netapp")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesNetapp"]]], result)

    @builtins.property
    def postgresql_flexible_server(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesPostgresqlFlexibleServer"]]]:
        '''postgresql_flexible_server block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#postgresql_flexible_server AzurermProvider#postgresql_flexible_server}
        '''
        result = self._values.get("postgresql_flexible_server")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesPostgresqlFlexibleServer"]]], result)

    @builtins.property
    def recovery_service(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesRecoveryService"]]]:
        '''recovery_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recovery_service AzurermProvider#recovery_service}
        '''
        result = self._values.get("recovery_service")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesRecoveryService"]]], result)

    @builtins.property
    def recovery_services_vaults(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesRecoveryServicesVaults"]]]:
        '''recovery_services_vaults block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recovery_services_vaults AzurermProvider#recovery_services_vaults}
        '''
        result = self._values.get("recovery_services_vaults")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesRecoveryServicesVaults"]]], result)

    @builtins.property
    def resource_group(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesResourceGroup"]]]:
        '''resource_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#resource_group AzurermProvider#resource_group}
        '''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesResourceGroup"]]], result)

    @builtins.property
    def storage(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesStorage"]]]:
        '''storage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#storage AzurermProvider#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesStorage"]]], result)

    @builtins.property
    def subscription(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesSubscription"]]]:
        '''subscription block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#subscription AzurermProvider#subscription}
        '''
        result = self._values.get("subscription")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesSubscription"]]], result)

    @builtins.property
    def template_deployment(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesTemplateDeployment"]]]:
        '''template_deployment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#template_deployment AzurermProvider#template_deployment}
        '''
        result = self._values.get("template_deployment")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesTemplateDeployment"]]], result)

    @builtins.property
    def virtual_machine(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesVirtualMachine"]]]:
        '''virtual_machine block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#virtual_machine AzurermProvider#virtual_machine}
        '''
        result = self._values.get("virtual_machine")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesVirtualMachine"]]], result)

    @builtins.property
    def virtual_machine_scale_set(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesVirtualMachineScaleSet"]]]:
        '''virtual_machine_scale_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#virtual_machine_scale_set AzurermProvider#virtual_machine_scale_set}
        '''
        result = self._values.get("virtual_machine_scale_set")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AzurermProviderFeaturesVirtualMachineScaleSet"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesApiManagement",
    jsii_struct_bases=[],
    name_mapping={
        "purge_soft_delete_on_destroy": "purgeSoftDeleteOnDestroy",
        "recover_soft_deleted": "recoverSoftDeleted",
    },
)
class AzurermProviderFeaturesApiManagement:
    def __init__(
        self,
        *,
        purge_soft_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_soft_deleted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param purge_soft_delete_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_delete_on_destroy AzurermProvider#purge_soft_delete_on_destroy}.
        :param recover_soft_deleted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted AzurermProvider#recover_soft_deleted}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db184db9aac7ca40a8e3d0e850b11d5e3444c9a33a8dcb670f1336998c9a04f7)
            check_type(argname="argument purge_soft_delete_on_destroy", value=purge_soft_delete_on_destroy, expected_type=type_hints["purge_soft_delete_on_destroy"])
            check_type(argname="argument recover_soft_deleted", value=recover_soft_deleted, expected_type=type_hints["recover_soft_deleted"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if purge_soft_delete_on_destroy is not None:
            self._values["purge_soft_delete_on_destroy"] = purge_soft_delete_on_destroy
        if recover_soft_deleted is not None:
            self._values["recover_soft_deleted"] = recover_soft_deleted

    @builtins.property
    def purge_soft_delete_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_delete_on_destroy AzurermProvider#purge_soft_delete_on_destroy}.'''
        result = self._values.get("purge_soft_delete_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recover_soft_deleted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted AzurermProvider#recover_soft_deleted}.'''
        result = self._values.get("recover_soft_deleted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesApiManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesAppConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "purge_soft_delete_on_destroy": "purgeSoftDeleteOnDestroy",
        "recover_soft_deleted": "recoverSoftDeleted",
    },
)
class AzurermProviderFeaturesAppConfiguration:
    def __init__(
        self,
        *,
        purge_soft_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_soft_deleted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param purge_soft_delete_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_delete_on_destroy AzurermProvider#purge_soft_delete_on_destroy}.
        :param recover_soft_deleted: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted AzurermProvider#recover_soft_deleted}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29a21dadee83b0f19ed7fdd189e5f67885eee1eab7e6a754b66a9d62676091d)
            check_type(argname="argument purge_soft_delete_on_destroy", value=purge_soft_delete_on_destroy, expected_type=type_hints["purge_soft_delete_on_destroy"])
            check_type(argname="argument recover_soft_deleted", value=recover_soft_deleted, expected_type=type_hints["recover_soft_deleted"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if purge_soft_delete_on_destroy is not None:
            self._values["purge_soft_delete_on_destroy"] = purge_soft_delete_on_destroy
        if recover_soft_deleted is not None:
            self._values["recover_soft_deleted"] = recover_soft_deleted

    @builtins.property
    def purge_soft_delete_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_delete_on_destroy AzurermProvider#purge_soft_delete_on_destroy}.'''
        result = self._values.get("purge_soft_delete_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recover_soft_deleted(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted AzurermProvider#recover_soft_deleted}.'''
        result = self._values.get("recover_soft_deleted")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesAppConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesApplicationInsights",
    jsii_struct_bases=[],
    name_mapping={"disable_generated_rule": "disableGeneratedRule"},
)
class AzurermProviderFeaturesApplicationInsights:
    def __init__(
        self,
        *,
        disable_generated_rule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_generated_rule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#disable_generated_rule AzurermProvider#disable_generated_rule}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__294d30d37a89ddbf177e76c5480a4a1973abf805a4e41308fde01f3f513d8437)
            check_type(argname="argument disable_generated_rule", value=disable_generated_rule, expected_type=type_hints["disable_generated_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_generated_rule is not None:
            self._values["disable_generated_rule"] = disable_generated_rule

    @builtins.property
    def disable_generated_rule(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#disable_generated_rule AzurermProvider#disable_generated_rule}.'''
        result = self._values.get("disable_generated_rule")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesApplicationInsights(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesCognitiveAccount",
    jsii_struct_bases=[],
    name_mapping={"purge_soft_delete_on_destroy": "purgeSoftDeleteOnDestroy"},
)
class AzurermProviderFeaturesCognitiveAccount:
    def __init__(
        self,
        *,
        purge_soft_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param purge_soft_delete_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_delete_on_destroy AzurermProvider#purge_soft_delete_on_destroy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b10ccf4278fa426817d52619a2902e9dae1529834b3745a84b6a41c52522f6)
            check_type(argname="argument purge_soft_delete_on_destroy", value=purge_soft_delete_on_destroy, expected_type=type_hints["purge_soft_delete_on_destroy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if purge_soft_delete_on_destroy is not None:
            self._values["purge_soft_delete_on_destroy"] = purge_soft_delete_on_destroy

    @builtins.property
    def purge_soft_delete_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_delete_on_destroy AzurermProvider#purge_soft_delete_on_destroy}.'''
        result = self._values.get("purge_soft_delete_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesCognitiveAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesDatabricksWorkspace",
    jsii_struct_bases=[],
    name_mapping={"force_delete": "forceDelete"},
)
class AzurermProviderFeaturesDatabricksWorkspace:
    def __init__(
        self,
        *,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param force_delete: When enabled, the managed resource group that contains the Unity Catalog data will be forcibly deleted when the workspace is destroyed, regardless of contents. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#force_delete AzurermProvider#force_delete}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0edbf68fcbb59ae1afc1ac4357d4e4f6f687514ebbc658b5c651d39f21d8fe88)
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if force_delete is not None:
            self._values["force_delete"] = force_delete

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, the managed resource group that contains the Unity Catalog data will be forcibly deleted when the workspace is destroyed, regardless of contents.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#force_delete AzurermProvider#force_delete}
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesDatabricksWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesKeyVault",
    jsii_struct_bases=[],
    name_mapping={
        "purge_soft_deleted_certificates_on_destroy": "purgeSoftDeletedCertificatesOnDestroy",
        "purge_soft_deleted_hardware_security_module_keys_on_destroy": "purgeSoftDeletedHardwareSecurityModuleKeysOnDestroy",
        "purge_soft_deleted_hardware_security_modules_on_destroy": "purgeSoftDeletedHardwareSecurityModulesOnDestroy",
        "purge_soft_deleted_keys_on_destroy": "purgeSoftDeletedKeysOnDestroy",
        "purge_soft_deleted_secrets_on_destroy": "purgeSoftDeletedSecretsOnDestroy",
        "purge_soft_delete_on_destroy": "purgeSoftDeleteOnDestroy",
        "recover_soft_deleted_certificates": "recoverSoftDeletedCertificates",
        "recover_soft_deleted_hardware_security_module_keys": "recoverSoftDeletedHardwareSecurityModuleKeys",
        "recover_soft_deleted_keys": "recoverSoftDeletedKeys",
        "recover_soft_deleted_key_vaults": "recoverSoftDeletedKeyVaults",
        "recover_soft_deleted_secrets": "recoverSoftDeletedSecrets",
    },
)
class AzurermProviderFeaturesKeyVault:
    def __init__(
        self,
        *,
        purge_soft_deleted_certificates_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purge_soft_deleted_hardware_security_module_keys_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purge_soft_deleted_hardware_security_modules_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purge_soft_deleted_keys_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purge_soft_deleted_secrets_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        purge_soft_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_soft_deleted_certificates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_soft_deleted_hardware_security_module_keys: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_soft_deleted_keys: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_soft_deleted_key_vaults: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        recover_soft_deleted_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param purge_soft_deleted_certificates_on_destroy: When enabled soft-deleted ``azurerm_key_vault_certificate`` resources will be permanently deleted (e.g purged), when destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_certificates_on_destroy AzurermProvider#purge_soft_deleted_certificates_on_destroy}
        :param purge_soft_deleted_hardware_security_module_keys_on_destroy: When enabled soft-deleted ``azurerm_key_vault_managed_hardware_security_module_key`` resources will be permanently deleted (e.g purged), when destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_hardware_security_module_keys_on_destroy AzurermProvider#purge_soft_deleted_hardware_security_module_keys_on_destroy}
        :param purge_soft_deleted_hardware_security_modules_on_destroy: When enabled soft-deleted ``azurerm_key_vault_managed_hardware_security_module`` resources will be permanently deleted (e.g purged), when destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_hardware_security_modules_on_destroy AzurermProvider#purge_soft_deleted_hardware_security_modules_on_destroy}
        :param purge_soft_deleted_keys_on_destroy: When enabled soft-deleted ``azurerm_key_vault_key`` resources will be permanently deleted (e.g purged), when destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_keys_on_destroy AzurermProvider#purge_soft_deleted_keys_on_destroy}
        :param purge_soft_deleted_secrets_on_destroy: When enabled soft-deleted ``azurerm_key_vault_secret`` resources will be permanently deleted (e.g purged), when destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_secrets_on_destroy AzurermProvider#purge_soft_deleted_secrets_on_destroy}
        :param purge_soft_delete_on_destroy: When enabled soft-deleted ``azurerm_key_vault`` resources will be permanently deleted (e.g purged), when destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_delete_on_destroy AzurermProvider#purge_soft_delete_on_destroy}
        :param recover_soft_deleted_certificates: When enabled soft-deleted ``azurerm_key_vault_certificate`` resources will be restored, instead of creating new ones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_certificates AzurermProvider#recover_soft_deleted_certificates}
        :param recover_soft_deleted_hardware_security_module_keys: When enabled soft-deleted ``azurerm_key_vault_managed_hardware_security_module_key`` resources will be restored, instead of creating new ones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_hardware_security_module_keys AzurermProvider#recover_soft_deleted_hardware_security_module_keys}
        :param recover_soft_deleted_keys: When enabled soft-deleted ``azurerm_key_vault_key`` resources will be restored, instead of creating new ones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_keys AzurermProvider#recover_soft_deleted_keys}
        :param recover_soft_deleted_key_vaults: When enabled soft-deleted ``azurerm_key_vault`` resources will be restored, instead of creating new ones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_key_vaults AzurermProvider#recover_soft_deleted_key_vaults}
        :param recover_soft_deleted_secrets: When enabled soft-deleted ``azurerm_key_vault_secret`` resources will be restored, instead of creating new ones. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_secrets AzurermProvider#recover_soft_deleted_secrets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1321221c1f4728075104d844a663420209d7ac49457ba222671b6c1522ebb5)
            check_type(argname="argument purge_soft_deleted_certificates_on_destroy", value=purge_soft_deleted_certificates_on_destroy, expected_type=type_hints["purge_soft_deleted_certificates_on_destroy"])
            check_type(argname="argument purge_soft_deleted_hardware_security_module_keys_on_destroy", value=purge_soft_deleted_hardware_security_module_keys_on_destroy, expected_type=type_hints["purge_soft_deleted_hardware_security_module_keys_on_destroy"])
            check_type(argname="argument purge_soft_deleted_hardware_security_modules_on_destroy", value=purge_soft_deleted_hardware_security_modules_on_destroy, expected_type=type_hints["purge_soft_deleted_hardware_security_modules_on_destroy"])
            check_type(argname="argument purge_soft_deleted_keys_on_destroy", value=purge_soft_deleted_keys_on_destroy, expected_type=type_hints["purge_soft_deleted_keys_on_destroy"])
            check_type(argname="argument purge_soft_deleted_secrets_on_destroy", value=purge_soft_deleted_secrets_on_destroy, expected_type=type_hints["purge_soft_deleted_secrets_on_destroy"])
            check_type(argname="argument purge_soft_delete_on_destroy", value=purge_soft_delete_on_destroy, expected_type=type_hints["purge_soft_delete_on_destroy"])
            check_type(argname="argument recover_soft_deleted_certificates", value=recover_soft_deleted_certificates, expected_type=type_hints["recover_soft_deleted_certificates"])
            check_type(argname="argument recover_soft_deleted_hardware_security_module_keys", value=recover_soft_deleted_hardware_security_module_keys, expected_type=type_hints["recover_soft_deleted_hardware_security_module_keys"])
            check_type(argname="argument recover_soft_deleted_keys", value=recover_soft_deleted_keys, expected_type=type_hints["recover_soft_deleted_keys"])
            check_type(argname="argument recover_soft_deleted_key_vaults", value=recover_soft_deleted_key_vaults, expected_type=type_hints["recover_soft_deleted_key_vaults"])
            check_type(argname="argument recover_soft_deleted_secrets", value=recover_soft_deleted_secrets, expected_type=type_hints["recover_soft_deleted_secrets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if purge_soft_deleted_certificates_on_destroy is not None:
            self._values["purge_soft_deleted_certificates_on_destroy"] = purge_soft_deleted_certificates_on_destroy
        if purge_soft_deleted_hardware_security_module_keys_on_destroy is not None:
            self._values["purge_soft_deleted_hardware_security_module_keys_on_destroy"] = purge_soft_deleted_hardware_security_module_keys_on_destroy
        if purge_soft_deleted_hardware_security_modules_on_destroy is not None:
            self._values["purge_soft_deleted_hardware_security_modules_on_destroy"] = purge_soft_deleted_hardware_security_modules_on_destroy
        if purge_soft_deleted_keys_on_destroy is not None:
            self._values["purge_soft_deleted_keys_on_destroy"] = purge_soft_deleted_keys_on_destroy
        if purge_soft_deleted_secrets_on_destroy is not None:
            self._values["purge_soft_deleted_secrets_on_destroy"] = purge_soft_deleted_secrets_on_destroy
        if purge_soft_delete_on_destroy is not None:
            self._values["purge_soft_delete_on_destroy"] = purge_soft_delete_on_destroy
        if recover_soft_deleted_certificates is not None:
            self._values["recover_soft_deleted_certificates"] = recover_soft_deleted_certificates
        if recover_soft_deleted_hardware_security_module_keys is not None:
            self._values["recover_soft_deleted_hardware_security_module_keys"] = recover_soft_deleted_hardware_security_module_keys
        if recover_soft_deleted_keys is not None:
            self._values["recover_soft_deleted_keys"] = recover_soft_deleted_keys
        if recover_soft_deleted_key_vaults is not None:
            self._values["recover_soft_deleted_key_vaults"] = recover_soft_deleted_key_vaults
        if recover_soft_deleted_secrets is not None:
            self._values["recover_soft_deleted_secrets"] = recover_soft_deleted_secrets

    @builtins.property
    def purge_soft_deleted_certificates_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_certificate`` resources will be permanently deleted (e.g purged), when destroyed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_certificates_on_destroy AzurermProvider#purge_soft_deleted_certificates_on_destroy}
        '''
        result = self._values.get("purge_soft_deleted_certificates_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def purge_soft_deleted_hardware_security_module_keys_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_managed_hardware_security_module_key`` resources will be permanently deleted (e.g purged), when destroyed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_hardware_security_module_keys_on_destroy AzurermProvider#purge_soft_deleted_hardware_security_module_keys_on_destroy}
        '''
        result = self._values.get("purge_soft_deleted_hardware_security_module_keys_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def purge_soft_deleted_hardware_security_modules_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_managed_hardware_security_module`` resources will be permanently deleted (e.g purged), when destroyed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_hardware_security_modules_on_destroy AzurermProvider#purge_soft_deleted_hardware_security_modules_on_destroy}
        '''
        result = self._values.get("purge_soft_deleted_hardware_security_modules_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def purge_soft_deleted_keys_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_key`` resources will be permanently deleted (e.g purged), when destroyed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_keys_on_destroy AzurermProvider#purge_soft_deleted_keys_on_destroy}
        '''
        result = self._values.get("purge_soft_deleted_keys_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def purge_soft_deleted_secrets_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_secret`` resources will be permanently deleted (e.g purged), when destroyed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_secrets_on_destroy AzurermProvider#purge_soft_deleted_secrets_on_destroy}
        '''
        result = self._values.get("purge_soft_deleted_secrets_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def purge_soft_delete_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault`` resources will be permanently deleted (e.g purged), when destroyed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_delete_on_destroy AzurermProvider#purge_soft_delete_on_destroy}
        '''
        result = self._values.get("purge_soft_delete_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recover_soft_deleted_certificates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_certificate`` resources will be restored, instead of creating new ones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_certificates AzurermProvider#recover_soft_deleted_certificates}
        '''
        result = self._values.get("recover_soft_deleted_certificates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recover_soft_deleted_hardware_security_module_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_managed_hardware_security_module_key`` resources will be restored, instead of creating new ones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_hardware_security_module_keys AzurermProvider#recover_soft_deleted_hardware_security_module_keys}
        '''
        result = self._values.get("recover_soft_deleted_hardware_security_module_keys")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recover_soft_deleted_keys(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_key`` resources will be restored, instead of creating new ones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_keys AzurermProvider#recover_soft_deleted_keys}
        '''
        result = self._values.get("recover_soft_deleted_keys")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recover_soft_deleted_key_vaults(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault`` resources will be restored, instead of creating new ones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_key_vaults AzurermProvider#recover_soft_deleted_key_vaults}
        '''
        result = self._values.get("recover_soft_deleted_key_vaults")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def recover_soft_deleted_secrets(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled soft-deleted ``azurerm_key_vault_secret`` resources will be restored, instead of creating new ones.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_secrets AzurermProvider#recover_soft_deleted_secrets}
        '''
        result = self._values.get("recover_soft_deleted_secrets")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesKeyVault(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesLogAnalyticsWorkspace",
    jsii_struct_bases=[],
    name_mapping={"permanently_delete_on_destroy": "permanentlyDeleteOnDestroy"},
)
class AzurermProviderFeaturesLogAnalyticsWorkspace:
    def __init__(
        self,
        *,
        permanently_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param permanently_delete_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#permanently_delete_on_destroy AzurermProvider#permanently_delete_on_destroy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9217d5928ddf184eaec97f68af5d98d74d81ef3fac38106d66c32271b55f2f30)
            check_type(argname="argument permanently_delete_on_destroy", value=permanently_delete_on_destroy, expected_type=type_hints["permanently_delete_on_destroy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if permanently_delete_on_destroy is not None:
            self._values["permanently_delete_on_destroy"] = permanently_delete_on_destroy

    @builtins.property
    def permanently_delete_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#permanently_delete_on_destroy AzurermProvider#permanently_delete_on_destroy}.'''
        result = self._values.get("permanently_delete_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesLogAnalyticsWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesMachineLearning",
    jsii_struct_bases=[],
    name_mapping={
        "purge_soft_deleted_workspace_on_destroy": "purgeSoftDeletedWorkspaceOnDestroy",
    },
)
class AzurermProviderFeaturesMachineLearning:
    def __init__(
        self,
        *,
        purge_soft_deleted_workspace_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param purge_soft_deleted_workspace_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_workspace_on_destroy AzurermProvider#purge_soft_deleted_workspace_on_destroy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dd3b739322c5d2ec876869d8994e55a0694235b13c939b4caaee1f3aef7a52)
            check_type(argname="argument purge_soft_deleted_workspace_on_destroy", value=purge_soft_deleted_workspace_on_destroy, expected_type=type_hints["purge_soft_deleted_workspace_on_destroy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if purge_soft_deleted_workspace_on_destroy is not None:
            self._values["purge_soft_deleted_workspace_on_destroy"] = purge_soft_deleted_workspace_on_destroy

    @builtins.property
    def purge_soft_deleted_workspace_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_soft_deleted_workspace_on_destroy AzurermProvider#purge_soft_deleted_workspace_on_destroy}.'''
        result = self._values.get("purge_soft_deleted_workspace_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesMachineLearning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesManagedDisk",
    jsii_struct_bases=[],
    name_mapping={"expand_without_downtime": "expandWithoutDowntime"},
)
class AzurermProviderFeaturesManagedDisk:
    def __init__(
        self,
        *,
        expand_without_downtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param expand_without_downtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#expand_without_downtime AzurermProvider#expand_without_downtime}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63db36ed9ca59b65104672633cd1dabf0fdc6d4f6f5dea463b25b60fdbd6755c)
            check_type(argname="argument expand_without_downtime", value=expand_without_downtime, expected_type=type_hints["expand_without_downtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expand_without_downtime is not None:
            self._values["expand_without_downtime"] = expand_without_downtime

    @builtins.property
    def expand_without_downtime(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#expand_without_downtime AzurermProvider#expand_without_downtime}.'''
        result = self._values.get("expand_without_downtime")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesManagedDisk(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesNetapp",
    jsii_struct_bases=[],
    name_mapping={
        "delete_backups_on_backup_vault_destroy": "deleteBackupsOnBackupVaultDestroy",
        "prevent_volume_destruction": "preventVolumeDestruction",
    },
)
class AzurermProviderFeaturesNetapp:
    def __init__(
        self,
        *,
        delete_backups_on_backup_vault_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prevent_volume_destruction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param delete_backups_on_backup_vault_destroy: When enabled, backups will be deleted when the ``azurerm_netapp_backup_vault`` resource is destroyed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#delete_backups_on_backup_vault_destroy AzurermProvider#delete_backups_on_backup_vault_destroy}
        :param prevent_volume_destruction: When enabled, the volume will not be destroyed, safeguarding from severe data loss. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#prevent_volume_destruction AzurermProvider#prevent_volume_destruction}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c49bc8f7c1c353567588e93c89b3e5be54e680428792da6781e1910678806516)
            check_type(argname="argument delete_backups_on_backup_vault_destroy", value=delete_backups_on_backup_vault_destroy, expected_type=type_hints["delete_backups_on_backup_vault_destroy"])
            check_type(argname="argument prevent_volume_destruction", value=prevent_volume_destruction, expected_type=type_hints["prevent_volume_destruction"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_backups_on_backup_vault_destroy is not None:
            self._values["delete_backups_on_backup_vault_destroy"] = delete_backups_on_backup_vault_destroy
        if prevent_volume_destruction is not None:
            self._values["prevent_volume_destruction"] = prevent_volume_destruction

    @builtins.property
    def delete_backups_on_backup_vault_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, backups will be deleted when the ``azurerm_netapp_backup_vault`` resource is destroyed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#delete_backups_on_backup_vault_destroy AzurermProvider#delete_backups_on_backup_vault_destroy}
        '''
        result = self._values.get("delete_backups_on_backup_vault_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prevent_volume_destruction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When enabled, the volume will not be destroyed, safeguarding from severe data loss.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#prevent_volume_destruction AzurermProvider#prevent_volume_destruction}
        '''
        result = self._values.get("prevent_volume_destruction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesNetapp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesPostgresqlFlexibleServer",
    jsii_struct_bases=[],
    name_mapping={
        "restart_server_on_configuration_value_change": "restartServerOnConfigurationValueChange",
    },
)
class AzurermProviderFeaturesPostgresqlFlexibleServer:
    def __init__(
        self,
        *,
        restart_server_on_configuration_value_change: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param restart_server_on_configuration_value_change: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#restart_server_on_configuration_value_change AzurermProvider#restart_server_on_configuration_value_change}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e12caa55f24eeef1eb5693386dd2d4966cfc71f56cb6ace1c11104f300138d4)
            check_type(argname="argument restart_server_on_configuration_value_change", value=restart_server_on_configuration_value_change, expected_type=type_hints["restart_server_on_configuration_value_change"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if restart_server_on_configuration_value_change is not None:
            self._values["restart_server_on_configuration_value_change"] = restart_server_on_configuration_value_change

    @builtins.property
    def restart_server_on_configuration_value_change(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#restart_server_on_configuration_value_change AzurermProvider#restart_server_on_configuration_value_change}.'''
        result = self._values.get("restart_server_on_configuration_value_change")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesPostgresqlFlexibleServer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesRecoveryService",
    jsii_struct_bases=[],
    name_mapping={
        "purge_protected_items_from_vault_on_destroy": "purgeProtectedItemsFromVaultOnDestroy",
        "vm_backup_stop_protection_and_retain_data_on_destroy": "vmBackupStopProtectionAndRetainDataOnDestroy",
        "vm_backup_suspend_protection_and_retain_data_on_destroy": "vmBackupSuspendProtectionAndRetainDataOnDestroy",
    },
)
class AzurermProviderFeaturesRecoveryService:
    def __init__(
        self,
        *,
        purge_protected_items_from_vault_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vm_backup_stop_protection_and_retain_data_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vm_backup_suspend_protection_and_retain_data_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param purge_protected_items_from_vault_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_protected_items_from_vault_on_destroy AzurermProvider#purge_protected_items_from_vault_on_destroy}.
        :param vm_backup_stop_protection_and_retain_data_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#vm_backup_stop_protection_and_retain_data_on_destroy AzurermProvider#vm_backup_stop_protection_and_retain_data_on_destroy}.
        :param vm_backup_suspend_protection_and_retain_data_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#vm_backup_suspend_protection_and_retain_data_on_destroy AzurermProvider#vm_backup_suspend_protection_and_retain_data_on_destroy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c60a755ce617a8215f4f3e68211babf3b376b224e82f1935c1a48257567c174)
            check_type(argname="argument purge_protected_items_from_vault_on_destroy", value=purge_protected_items_from_vault_on_destroy, expected_type=type_hints["purge_protected_items_from_vault_on_destroy"])
            check_type(argname="argument vm_backup_stop_protection_and_retain_data_on_destroy", value=vm_backup_stop_protection_and_retain_data_on_destroy, expected_type=type_hints["vm_backup_stop_protection_and_retain_data_on_destroy"])
            check_type(argname="argument vm_backup_suspend_protection_and_retain_data_on_destroy", value=vm_backup_suspend_protection_and_retain_data_on_destroy, expected_type=type_hints["vm_backup_suspend_protection_and_retain_data_on_destroy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if purge_protected_items_from_vault_on_destroy is not None:
            self._values["purge_protected_items_from_vault_on_destroy"] = purge_protected_items_from_vault_on_destroy
        if vm_backup_stop_protection_and_retain_data_on_destroy is not None:
            self._values["vm_backup_stop_protection_and_retain_data_on_destroy"] = vm_backup_stop_protection_and_retain_data_on_destroy
        if vm_backup_suspend_protection_and_retain_data_on_destroy is not None:
            self._values["vm_backup_suspend_protection_and_retain_data_on_destroy"] = vm_backup_suspend_protection_and_retain_data_on_destroy

    @builtins.property
    def purge_protected_items_from_vault_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#purge_protected_items_from_vault_on_destroy AzurermProvider#purge_protected_items_from_vault_on_destroy}.'''
        result = self._values.get("purge_protected_items_from_vault_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vm_backup_stop_protection_and_retain_data_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#vm_backup_stop_protection_and_retain_data_on_destroy AzurermProvider#vm_backup_stop_protection_and_retain_data_on_destroy}.'''
        result = self._values.get("vm_backup_stop_protection_and_retain_data_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vm_backup_suspend_protection_and_retain_data_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#vm_backup_suspend_protection_and_retain_data_on_destroy AzurermProvider#vm_backup_suspend_protection_and_retain_data_on_destroy}.'''
        result = self._values.get("vm_backup_suspend_protection_and_retain_data_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesRecoveryService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesRecoveryServicesVaults",
    jsii_struct_bases=[],
    name_mapping={
        "recover_soft_deleted_backup_protected_vm": "recoverSoftDeletedBackupProtectedVm",
    },
)
class AzurermProviderFeaturesRecoveryServicesVaults:
    def __init__(
        self,
        *,
        recover_soft_deleted_backup_protected_vm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param recover_soft_deleted_backup_protected_vm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_backup_protected_vm AzurermProvider#recover_soft_deleted_backup_protected_vm}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9deba963993ad51c7c93fbffbbd65074e9b9527699600c7978cc7e2e028d8049)
            check_type(argname="argument recover_soft_deleted_backup_protected_vm", value=recover_soft_deleted_backup_protected_vm, expected_type=type_hints["recover_soft_deleted_backup_protected_vm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recover_soft_deleted_backup_protected_vm is not None:
            self._values["recover_soft_deleted_backup_protected_vm"] = recover_soft_deleted_backup_protected_vm

    @builtins.property
    def recover_soft_deleted_backup_protected_vm(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#recover_soft_deleted_backup_protected_vm AzurermProvider#recover_soft_deleted_backup_protected_vm}.'''
        result = self._values.get("recover_soft_deleted_backup_protected_vm")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesRecoveryServicesVaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesResourceGroup",
    jsii_struct_bases=[],
    name_mapping={
        "prevent_deletion_if_contains_resources": "preventDeletionIfContainsResources",
    },
)
class AzurermProviderFeaturesResourceGroup:
    def __init__(
        self,
        *,
        prevent_deletion_if_contains_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param prevent_deletion_if_contains_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#prevent_deletion_if_contains_resources AzurermProvider#prevent_deletion_if_contains_resources}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027a6cc8e6d8f6110b7b9860fa26532f4ac8e92fe10efa98c73a90505847b9cd)
            check_type(argname="argument prevent_deletion_if_contains_resources", value=prevent_deletion_if_contains_resources, expected_type=type_hints["prevent_deletion_if_contains_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prevent_deletion_if_contains_resources is not None:
            self._values["prevent_deletion_if_contains_resources"] = prevent_deletion_if_contains_resources

    @builtins.property
    def prevent_deletion_if_contains_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#prevent_deletion_if_contains_resources AzurermProvider#prevent_deletion_if_contains_resources}.'''
        result = self._values.get("prevent_deletion_if_contains_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesResourceGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesStorage",
    jsii_struct_bases=[],
    name_mapping={"data_plane_available": "dataPlaneAvailable"},
)
class AzurermProviderFeaturesStorage:
    def __init__(
        self,
        *,
        data_plane_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param data_plane_available: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#data_plane_available AzurermProvider#data_plane_available}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e62dbde16353d25699a93154500d5c450164bd1e2c4a16ba1c1c10ae8338b4f)
            check_type(argname="argument data_plane_available", value=data_plane_available, expected_type=type_hints["data_plane_available"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_plane_available is not None:
            self._values["data_plane_available"] = data_plane_available

    @builtins.property
    def data_plane_available(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#data_plane_available AzurermProvider#data_plane_available}.'''
        result = self._values.get("data_plane_available")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesStorage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesSubscription",
    jsii_struct_bases=[],
    name_mapping={"prevent_cancellation_on_destroy": "preventCancellationOnDestroy"},
)
class AzurermProviderFeaturesSubscription:
    def __init__(
        self,
        *,
        prevent_cancellation_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param prevent_cancellation_on_destroy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#prevent_cancellation_on_destroy AzurermProvider#prevent_cancellation_on_destroy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__318768033bcd7125819674c8b24fe58f1a297bf334de5d13cd7fc0577d08662f)
            check_type(argname="argument prevent_cancellation_on_destroy", value=prevent_cancellation_on_destroy, expected_type=type_hints["prevent_cancellation_on_destroy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prevent_cancellation_on_destroy is not None:
            self._values["prevent_cancellation_on_destroy"] = prevent_cancellation_on_destroy

    @builtins.property
    def prevent_cancellation_on_destroy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#prevent_cancellation_on_destroy AzurermProvider#prevent_cancellation_on_destroy}.'''
        result = self._values.get("prevent_cancellation_on_destroy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesSubscription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesTemplateDeployment",
    jsii_struct_bases=[],
    name_mapping={
        "delete_nested_items_during_deletion": "deleteNestedItemsDuringDeletion",
    },
)
class AzurermProviderFeaturesTemplateDeployment:
    def __init__(
        self,
        *,
        delete_nested_items_during_deletion: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param delete_nested_items_during_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#delete_nested_items_during_deletion AzurermProvider#delete_nested_items_during_deletion}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0542c1742d31b978b163d2d0d308d590581c94d5050313f3ae37138328f1987)
            check_type(argname="argument delete_nested_items_during_deletion", value=delete_nested_items_during_deletion, expected_type=type_hints["delete_nested_items_during_deletion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delete_nested_items_during_deletion": delete_nested_items_during_deletion,
        }

    @builtins.property
    def delete_nested_items_during_deletion(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#delete_nested_items_during_deletion AzurermProvider#delete_nested_items_during_deletion}.'''
        result = self._values.get("delete_nested_items_during_deletion")
        assert result is not None, "Required property 'delete_nested_items_during_deletion' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesTemplateDeployment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesVirtualMachine",
    jsii_struct_bases=[],
    name_mapping={
        "delete_os_disk_on_deletion": "deleteOsDiskOnDeletion",
        "detach_implicit_data_disk_on_deletion": "detachImplicitDataDiskOnDeletion",
        "graceful_shutdown": "gracefulShutdown",
        "skip_shutdown_and_force_delete": "skipShutdownAndForceDelete",
    },
)
class AzurermProviderFeaturesVirtualMachine:
    def __init__(
        self,
        *,
        delete_os_disk_on_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        detach_implicit_data_disk_on_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        graceful_shutdown: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        skip_shutdown_and_force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param delete_os_disk_on_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#delete_os_disk_on_deletion AzurermProvider#delete_os_disk_on_deletion}.
        :param detach_implicit_data_disk_on_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#detach_implicit_data_disk_on_deletion AzurermProvider#detach_implicit_data_disk_on_deletion}.
        :param graceful_shutdown: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#graceful_shutdown AzurermProvider#graceful_shutdown}.
        :param skip_shutdown_and_force_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#skip_shutdown_and_force_delete AzurermProvider#skip_shutdown_and_force_delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36a4c2309035348900124a3ee283f8f725c3ead1e74e7ac6a240e6c6d00ef4f)
            check_type(argname="argument delete_os_disk_on_deletion", value=delete_os_disk_on_deletion, expected_type=type_hints["delete_os_disk_on_deletion"])
            check_type(argname="argument detach_implicit_data_disk_on_deletion", value=detach_implicit_data_disk_on_deletion, expected_type=type_hints["detach_implicit_data_disk_on_deletion"])
            check_type(argname="argument graceful_shutdown", value=graceful_shutdown, expected_type=type_hints["graceful_shutdown"])
            check_type(argname="argument skip_shutdown_and_force_delete", value=skip_shutdown_and_force_delete, expected_type=type_hints["skip_shutdown_and_force_delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delete_os_disk_on_deletion is not None:
            self._values["delete_os_disk_on_deletion"] = delete_os_disk_on_deletion
        if detach_implicit_data_disk_on_deletion is not None:
            self._values["detach_implicit_data_disk_on_deletion"] = detach_implicit_data_disk_on_deletion
        if graceful_shutdown is not None:
            self._values["graceful_shutdown"] = graceful_shutdown
        if skip_shutdown_and_force_delete is not None:
            self._values["skip_shutdown_and_force_delete"] = skip_shutdown_and_force_delete

    @builtins.property
    def delete_os_disk_on_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#delete_os_disk_on_deletion AzurermProvider#delete_os_disk_on_deletion}.'''
        result = self._values.get("delete_os_disk_on_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def detach_implicit_data_disk_on_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#detach_implicit_data_disk_on_deletion AzurermProvider#detach_implicit_data_disk_on_deletion}.'''
        result = self._values.get("detach_implicit_data_disk_on_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def graceful_shutdown(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#graceful_shutdown AzurermProvider#graceful_shutdown}.'''
        result = self._values.get("graceful_shutdown")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def skip_shutdown_and_force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#skip_shutdown_and_force_delete AzurermProvider#skip_shutdown_and_force_delete}.'''
        result = self._values.get("skip_shutdown_and_force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesVirtualMachine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.provider.AzurermProviderFeaturesVirtualMachineScaleSet",
    jsii_struct_bases=[],
    name_mapping={
        "force_delete": "forceDelete",
        "reimage_on_manual_upgrade": "reimageOnManualUpgrade",
        "roll_instances_when_required": "rollInstancesWhenRequired",
        "scale_to_zero_before_deletion": "scaleToZeroBeforeDeletion",
    },
)
class AzurermProviderFeaturesVirtualMachineScaleSet:
    def __init__(
        self,
        *,
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        reimage_on_manual_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        roll_instances_when_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scale_to_zero_before_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param force_delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#force_delete AzurermProvider#force_delete}.
        :param reimage_on_manual_upgrade: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#reimage_on_manual_upgrade AzurermProvider#reimage_on_manual_upgrade}.
        :param roll_instances_when_required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#roll_instances_when_required AzurermProvider#roll_instances_when_required}.
        :param scale_to_zero_before_deletion: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#scale_to_zero_before_deletion AzurermProvider#scale_to_zero_before_deletion}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7832e5cffa83e13b844f319f4283f80a84b458fc676ac1c02172b64c99e744b7)
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument reimage_on_manual_upgrade", value=reimage_on_manual_upgrade, expected_type=type_hints["reimage_on_manual_upgrade"])
            check_type(argname="argument roll_instances_when_required", value=roll_instances_when_required, expected_type=type_hints["roll_instances_when_required"])
            check_type(argname="argument scale_to_zero_before_deletion", value=scale_to_zero_before_deletion, expected_type=type_hints["scale_to_zero_before_deletion"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if reimage_on_manual_upgrade is not None:
            self._values["reimage_on_manual_upgrade"] = reimage_on_manual_upgrade
        if roll_instances_when_required is not None:
            self._values["roll_instances_when_required"] = roll_instances_when_required
        if scale_to_zero_before_deletion is not None:
            self._values["scale_to_zero_before_deletion"] = scale_to_zero_before_deletion

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#force_delete AzurermProvider#force_delete}.'''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def reimage_on_manual_upgrade(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#reimage_on_manual_upgrade AzurermProvider#reimage_on_manual_upgrade}.'''
        result = self._values.get("reimage_on_manual_upgrade")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def roll_instances_when_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#roll_instances_when_required AzurermProvider#roll_instances_when_required}.'''
        result = self._values.get("roll_instances_when_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scale_to_zero_before_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs#scale_to_zero_before_deletion AzurermProvider#scale_to_zero_before_deletion}.'''
        result = self._values.get("scale_to_zero_before_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermProviderFeaturesVirtualMachineScaleSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AzurermProvider",
    "AzurermProviderConfig",
    "AzurermProviderFeatures",
    "AzurermProviderFeaturesApiManagement",
    "AzurermProviderFeaturesAppConfiguration",
    "AzurermProviderFeaturesApplicationInsights",
    "AzurermProviderFeaturesCognitiveAccount",
    "AzurermProviderFeaturesDatabricksWorkspace",
    "AzurermProviderFeaturesKeyVault",
    "AzurermProviderFeaturesLogAnalyticsWorkspace",
    "AzurermProviderFeaturesMachineLearning",
    "AzurermProviderFeaturesManagedDisk",
    "AzurermProviderFeaturesNetapp",
    "AzurermProviderFeaturesPostgresqlFlexibleServer",
    "AzurermProviderFeaturesRecoveryService",
    "AzurermProviderFeaturesRecoveryServicesVaults",
    "AzurermProviderFeaturesResourceGroup",
    "AzurermProviderFeaturesStorage",
    "AzurermProviderFeaturesSubscription",
    "AzurermProviderFeaturesTemplateDeployment",
    "AzurermProviderFeaturesVirtualMachine",
    "AzurermProviderFeaturesVirtualMachineScaleSet",
]

publication.publish()

def _typecheckingstub__1d612cb0ea42e0d04a986b52842f95dbbb6757bb17c26ccf9ccc136e8c917d94(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ado_pipeline_service_connection_id: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    auxiliary_tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_certificate_password: typing.Optional[builtins.str] = None,
    client_certificate_path: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_id_file_path: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_file_path: typing.Optional[builtins.str] = None,
    disable_correlation_request_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_terraform_partner_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment: typing.Optional[builtins.str] = None,
    features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata_host: typing.Optional[builtins.str] = None,
    msi_api_version: typing.Optional[builtins.str] = None,
    msi_endpoint: typing.Optional[builtins.str] = None,
    oidc_request_token: typing.Optional[builtins.str] = None,
    oidc_request_url: typing.Optional[builtins.str] = None,
    oidc_token: typing.Optional[builtins.str] = None,
    oidc_token_file_path: typing.Optional[builtins.str] = None,
    partner_id: typing.Optional[builtins.str] = None,
    resource_provider_registrations: typing.Optional[builtins.str] = None,
    resource_providers_to_register: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_provider_registration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_use_azuread: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subscription_id: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    use_aks_workload_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_cli: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_msi: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_oidc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f28cd221c0a8956938dbcfe651dedc5e126e3b1eae3f49b2a14350d362dda34(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5183b547764c4a96ee74ac4edcd6d9762a7466424753a0e1ae294bd3c102dc9a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1523e91cdfb6f51086599bf200611ee10faa93fa9c37cdcb2d1c2421bd024d65(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9144096b220f881cb7f1f8923f8f13a85f6451eb6a4be08deecf0a112868cc05(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04bfa0d73cfe140336d37aff39792146dbcee79074ecabd1541cb355ab3b13a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b6b921a8825272b14b71faa7994f1051c57fe216a706279640d802f5fe686c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8fe55c591ab2bf461b30580d6e9d9ce5683b2444f4864037bc8417a1a5543d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a47f4524dafc3df2503ef2768dc1d3a33c61710321c08052dcaea3b50df7115(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10af9b007767870f98e04964077f0e222c06c04116005ed6d1a19c472fd35da2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81663fcf4065492bb889303dd916452140ef72c9514f5d08b5b5bbc837b09e59(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e6d5416f03f701cb609986a5b0f86616222d75bf609b1bd24ec4d8a41d98e1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__614ef03a9911ecc789c792ff87ce3414745f45f5b63ce5238d62dd0285b79558(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d230bb82634caaf5a25592c647569ada140c5628156ec71b7c911177ebe12611(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c408f69d016c58c04f4685d1521340e839de2374117924ac0394703128632a52(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f70fad43d7cc3b607cfcd5ad95e72d2ae33000149eff41eee601f6353ebef61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AzurermProviderFeatures]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853a6ee43e3456e010e42412a57e38f5b6bb4143231be6bf372af406232ab19e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604790c21de537c0ccaca4efcc5b9f46235e452e5c421da26ef3f2b6964f16b5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3469bbdc46cf49a92158fabd40550df8e50d9c90d44d909dd6066df60d0554cb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e4c9bcafa230931323166957cfcbbc1bbae68d2a1735f59fe891b5b154c63c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3cbe862b08533674079b1f87d406cf0e32a31f042b9fd9c7e5f59f2f85ca07(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bb1aad80fa9cbb2d4b1ee8a12f74c3571f9eedf01bcc6bd2e7577e1a0e8f23(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776fc9fdf447742adcdbefa31bba132bc5793cd9c99fbf50692878ba778d9ba5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ce974198a33a4d4e2589cc1c8780a5f02228abf0cd9c42a52b6b80abac2ea3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9fb0cd060971865274740d84bcd52c9a74ca1058b1c2ee1f16b923e2bf8e44(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb4ecdcf0cd96ef9d562e52ea0965adf8e353a736facabda9bb60dafdc486e5(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7dd1db69fdae658eedd4e3ba4c9c96b07f3da7292764b7f64338f48e0b2b8e(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5d877412d16ee85b2925c17956f3b9aec7a714c671817f13545e8d51d2827f(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d88ffe9921ac7cd02d903ce6579e6ed4eb24d309d90a0e3d5b9aa2649b72243(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0a0d0150d026f85d25daa830c51bda7892e81be958c2bbde9a0b0fb3c76fea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643d3eb598148f207d2669b5593b40077ad06e32a7aee0d281f5579a490f12f1(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6434be286962ce3ae2d2650d973cb379046962ef75bfccd038152cd059e750(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7079a2ae9ee82de109aceb15c7743472a653d8aa361d70e3c922f934e60a554c(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb023b4999764e37b3b7e10ac8f7c7e11c1cd30137627621e3f021998846f5a(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92eb1fb6a38ebf26e757be24396414a7b978b452e851810b7c1d8535d70ed5f2(
    *,
    ado_pipeline_service_connection_id: typing.Optional[builtins.str] = None,
    alias: typing.Optional[builtins.str] = None,
    auxiliary_tenant_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_certificate: typing.Optional[builtins.str] = None,
    client_certificate_password: typing.Optional[builtins.str] = None,
    client_certificate_path: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_id_file_path: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_file_path: typing.Optional[builtins.str] = None,
    disable_correlation_request_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_terraform_partner_id: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment: typing.Optional[builtins.str] = None,
    features: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeatures, typing.Dict[builtins.str, typing.Any]]]]] = None,
    metadata_host: typing.Optional[builtins.str] = None,
    msi_api_version: typing.Optional[builtins.str] = None,
    msi_endpoint: typing.Optional[builtins.str] = None,
    oidc_request_token: typing.Optional[builtins.str] = None,
    oidc_request_url: typing.Optional[builtins.str] = None,
    oidc_token: typing.Optional[builtins.str] = None,
    oidc_token_file_path: typing.Optional[builtins.str] = None,
    partner_id: typing.Optional[builtins.str] = None,
    resource_provider_registrations: typing.Optional[builtins.str] = None,
    resource_providers_to_register: typing.Optional[typing.Sequence[builtins.str]] = None,
    skip_provider_registration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage_use_azuread: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    subscription_id: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    use_aks_workload_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_cli: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_msi: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_oidc: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a9682424bbe642a04b278e2b8074066025d046a35f868494b3173c6c7ab7965(
    *,
    api_management: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesApiManagement, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesAppConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_insights: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesApplicationInsights, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cognitive_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesCognitiveAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    databricks_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesDatabricksWorkspace, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_vault: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesKeyVault, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log_analytics_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesLogAnalyticsWorkspace, typing.Dict[builtins.str, typing.Any]]]]] = None,
    machine_learning: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesMachineLearning, typing.Dict[builtins.str, typing.Any]]]]] = None,
    managed_disk: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesManagedDisk, typing.Dict[builtins.str, typing.Any]]]]] = None,
    netapp: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesNetapp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    postgresql_flexible_server: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesPostgresqlFlexibleServer, typing.Dict[builtins.str, typing.Any]]]]] = None,
    recovery_service: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesRecoveryService, typing.Dict[builtins.str, typing.Any]]]]] = None,
    recovery_services_vaults: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesRecoveryServicesVaults, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_group: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesResourceGroup, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesStorage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    subscription: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesSubscription, typing.Dict[builtins.str, typing.Any]]]]] = None,
    template_deployment: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesTemplateDeployment, typing.Dict[builtins.str, typing.Any]]]]] = None,
    virtual_machine: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesVirtualMachine, typing.Dict[builtins.str, typing.Any]]]]] = None,
    virtual_machine_scale_set: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AzurermProviderFeaturesVirtualMachineScaleSet, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db184db9aac7ca40a8e3d0e850b11d5e3444c9a33a8dcb670f1336998c9a04f7(
    *,
    purge_soft_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_soft_deleted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29a21dadee83b0f19ed7fdd189e5f67885eee1eab7e6a754b66a9d62676091d(
    *,
    purge_soft_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_soft_deleted: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__294d30d37a89ddbf177e76c5480a4a1973abf805a4e41308fde01f3f513d8437(
    *,
    disable_generated_rule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4b10ccf4278fa426817d52619a2902e9dae1529834b3745a84b6a41c52522f6(
    *,
    purge_soft_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edbf68fcbb59ae1afc1ac4357d4e4f6f687514ebbc658b5c651d39f21d8fe88(
    *,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1321221c1f4728075104d844a663420209d7ac49457ba222671b6c1522ebb5(
    *,
    purge_soft_deleted_certificates_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purge_soft_deleted_hardware_security_module_keys_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purge_soft_deleted_hardware_security_modules_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purge_soft_deleted_keys_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purge_soft_deleted_secrets_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    purge_soft_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_soft_deleted_certificates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_soft_deleted_hardware_security_module_keys: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_soft_deleted_keys: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_soft_deleted_key_vaults: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    recover_soft_deleted_secrets: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9217d5928ddf184eaec97f68af5d98d74d81ef3fac38106d66c32271b55f2f30(
    *,
    permanently_delete_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dd3b739322c5d2ec876869d8994e55a0694235b13c939b4caaee1f3aef7a52(
    *,
    purge_soft_deleted_workspace_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63db36ed9ca59b65104672633cd1dabf0fdc6d4f6f5dea463b25b60fdbd6755c(
    *,
    expand_without_downtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49bc8f7c1c353567588e93c89b3e5be54e680428792da6781e1910678806516(
    *,
    delete_backups_on_backup_vault_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prevent_volume_destruction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e12caa55f24eeef1eb5693386dd2d4966cfc71f56cb6ace1c11104f300138d4(
    *,
    restart_server_on_configuration_value_change: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c60a755ce617a8215f4f3e68211babf3b376b224e82f1935c1a48257567c174(
    *,
    purge_protected_items_from_vault_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vm_backup_stop_protection_and_retain_data_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vm_backup_suspend_protection_and_retain_data_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9deba963993ad51c7c93fbffbbd65074e9b9527699600c7978cc7e2e028d8049(
    *,
    recover_soft_deleted_backup_protected_vm: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027a6cc8e6d8f6110b7b9860fa26532f4ac8e92fe10efa98c73a90505847b9cd(
    *,
    prevent_deletion_if_contains_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e62dbde16353d25699a93154500d5c450164bd1e2c4a16ba1c1c10ae8338b4f(
    *,
    data_plane_available: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318768033bcd7125819674c8b24fe58f1a297bf334de5d13cd7fc0577d08662f(
    *,
    prevent_cancellation_on_destroy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0542c1742d31b978b163d2d0d308d590581c94d5050313f3ae37138328f1987(
    *,
    delete_nested_items_during_deletion: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36a4c2309035348900124a3ee283f8f725c3ead1e74e7ac6a240e6c6d00ef4f(
    *,
    delete_os_disk_on_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    detach_implicit_data_disk_on_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    graceful_shutdown: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    skip_shutdown_and_force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7832e5cffa83e13b844f319f4283f80a84b458fc676ac1c02172b64c99e744b7(
    *,
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    reimage_on_manual_upgrade: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    roll_instances_when_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scale_to_zero_before_deletion: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

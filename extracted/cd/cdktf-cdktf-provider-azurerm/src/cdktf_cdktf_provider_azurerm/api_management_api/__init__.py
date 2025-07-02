r'''
# `azurerm_api_management_api`

Refer to the Terraform Registry for docs: [`azurerm_api_management_api`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api).
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


class ApiManagementApi(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApi",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api azurerm_api_management_api}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_management_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        revision: builtins.str,
        api_type: typing.Optional[builtins.str] = None,
        contact: typing.Optional[typing.Union["ApiManagementApiContact", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        import_: typing.Optional[typing.Union["ApiManagementApiImport", typing.Dict[builtins.str, typing.Any]]] = None,
        license: typing.Optional[typing.Union["ApiManagementApiLicense", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_authorization: typing.Optional[typing.Union["ApiManagementApiOauth2Authorization", typing.Dict[builtins.str, typing.Any]]] = None,
        openid_authentication: typing.Optional[typing.Union["ApiManagementApiOpenidAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        revision_description: typing.Optional[builtins.str] = None,
        service_url: typing.Optional[builtins.str] = None,
        source_api_id: typing.Optional[builtins.str] = None,
        subscription_key_parameter_names: typing.Optional[typing.Union["ApiManagementApiSubscriptionKeyParameterNames", typing.Dict[builtins.str, typing.Any]]] = None,
        subscription_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        terms_of_service_url: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementApiTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        version_description: typing.Optional[builtins.str] = None,
        version_set_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api azurerm_api_management_api} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#api_management_name ApiManagementApi#api_management_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#resource_group_name ApiManagementApi#resource_group_name}.
        :param revision: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#revision ApiManagementApi#revision}.
        :param api_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#api_type ApiManagementApi#api_type}.
        :param contact: contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#contact ApiManagementApi#contact}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#description ApiManagementApi#description}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#display_name ApiManagementApi#display_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#id ApiManagementApi#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_: import block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#import ApiManagementApi#import}
        :param license: license block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#license ApiManagementApi#license}
        :param oauth2_authorization: oauth2_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#oauth2_authorization ApiManagementApi#oauth2_authorization}
        :param openid_authentication: openid_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#openid_authentication ApiManagementApi#openid_authentication}
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#path ApiManagementApi#path}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#protocols ApiManagementApi#protocols}.
        :param revision_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#revision_description ApiManagementApi#revision_description}.
        :param service_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#service_url ApiManagementApi#service_url}.
        :param source_api_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#source_api_id ApiManagementApi#source_api_id}.
        :param subscription_key_parameter_names: subscription_key_parameter_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#subscription_key_parameter_names ApiManagementApi#subscription_key_parameter_names}
        :param subscription_required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#subscription_required ApiManagementApi#subscription_required}.
        :param terms_of_service_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#terms_of_service_url ApiManagementApi#terms_of_service_url}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#timeouts ApiManagementApi#timeouts}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version ApiManagementApi#version}.
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version_description ApiManagementApi#version_description}.
        :param version_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version_set_id ApiManagementApi#version_set_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d45ccc9a927ac6a18ca6e6d15fdf6d488bf0435af6abad86efd993e662a2b226)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiManagementApiConfig(
            api_management_name=api_management_name,
            name=name,
            resource_group_name=resource_group_name,
            revision=revision,
            api_type=api_type,
            contact=contact,
            description=description,
            display_name=display_name,
            id=id,
            import_=import_,
            license=license,
            oauth2_authorization=oauth2_authorization,
            openid_authentication=openid_authentication,
            path=path,
            protocols=protocols,
            revision_description=revision_description,
            service_url=service_url,
            source_api_id=source_api_id,
            subscription_key_parameter_names=subscription_key_parameter_names,
            subscription_required=subscription_required,
            terms_of_service_url=terms_of_service_url,
            timeouts=timeouts,
            version=version,
            version_description=version_description,
            version_set_id=version_set_id,
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
        '''Generates CDKTF code for importing a ApiManagementApi resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiManagementApi to import.
        :param import_from_id: The id of the existing ApiManagementApi that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiManagementApi to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3c7e9439fe58be63b7cf4dc9fb3c5233f44e1240e3f6f11fb804b26691b19d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContact")
    def put_contact(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#email ApiManagementApi#email}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#url ApiManagementApi#url}.
        '''
        value = ApiManagementApiContact(email=email, name=name, url=url)

        return typing.cast(None, jsii.invoke(self, "putContact", [value]))

    @jsii.member(jsii_name="putImport")
    def put_import(
        self,
        *,
        content_format: builtins.str,
        content_value: builtins.str,
        wsdl_selector: typing.Optional[typing.Union["ApiManagementApiImportWsdlSelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param content_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#content_format ApiManagementApi#content_format}.
        :param content_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#content_value ApiManagementApi#content_value}.
        :param wsdl_selector: wsdl_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#wsdl_selector ApiManagementApi#wsdl_selector}
        '''
        value = ApiManagementApiImport(
            content_format=content_format,
            content_value=content_value,
            wsdl_selector=wsdl_selector,
        )

        return typing.cast(None, jsii.invoke(self, "putImport", [value]))

    @jsii.member(jsii_name="putLicense")
    def put_license(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#url ApiManagementApi#url}.
        '''
        value = ApiManagementApiLicense(name=name, url=url)

        return typing.cast(None, jsii.invoke(self, "putLicense", [value]))

    @jsii.member(jsii_name="putOauth2Authorization")
    def put_oauth2_authorization(
        self,
        *,
        authorization_server_name: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorization_server_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#authorization_server_name ApiManagementApi#authorization_server_name}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#scope ApiManagementApi#scope}.
        '''
        value = ApiManagementApiOauth2Authorization(
            authorization_server_name=authorization_server_name, scope=scope
        )

        return typing.cast(None, jsii.invoke(self, "putOauth2Authorization", [value]))

    @jsii.member(jsii_name="putOpenidAuthentication")
    def put_openid_authentication(
        self,
        *,
        openid_provider_name: builtins.str,
        bearer_token_sending_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param openid_provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#openid_provider_name ApiManagementApi#openid_provider_name}.
        :param bearer_token_sending_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#bearer_token_sending_methods ApiManagementApi#bearer_token_sending_methods}.
        '''
        value = ApiManagementApiOpenidAuthentication(
            openid_provider_name=openid_provider_name,
            bearer_token_sending_methods=bearer_token_sending_methods,
        )

        return typing.cast(None, jsii.invoke(self, "putOpenidAuthentication", [value]))

    @jsii.member(jsii_name="putSubscriptionKeyParameterNames")
    def put_subscription_key_parameter_names(
        self,
        *,
        header: builtins.str,
        query: builtins.str,
    ) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#header ApiManagementApi#header}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#query ApiManagementApi#query}.
        '''
        value = ApiManagementApiSubscriptionKeyParameterNames(
            header=header, query=query
        )

        return typing.cast(None, jsii.invoke(self, "putSubscriptionKeyParameterNames", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#create ApiManagementApi#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#delete ApiManagementApi#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#read ApiManagementApi#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#update ApiManagementApi#update}.
        '''
        value = ApiManagementApiTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiType")
    def reset_api_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiType", []))

    @jsii.member(jsii_name="resetContact")
    def reset_contact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContact", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImport")
    def reset_import(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImport", []))

    @jsii.member(jsii_name="resetLicense")
    def reset_license(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLicense", []))

    @jsii.member(jsii_name="resetOauth2Authorization")
    def reset_oauth2_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauth2Authorization", []))

    @jsii.member(jsii_name="resetOpenidAuthentication")
    def reset_openid_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenidAuthentication", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetProtocols")
    def reset_protocols(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocols", []))

    @jsii.member(jsii_name="resetRevisionDescription")
    def reset_revision_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevisionDescription", []))

    @jsii.member(jsii_name="resetServiceUrl")
    def reset_service_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceUrl", []))

    @jsii.member(jsii_name="resetSourceApiId")
    def reset_source_api_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceApiId", []))

    @jsii.member(jsii_name="resetSubscriptionKeyParameterNames")
    def reset_subscription_key_parameter_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriptionKeyParameterNames", []))

    @jsii.member(jsii_name="resetSubscriptionRequired")
    def reset_subscription_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriptionRequired", []))

    @jsii.member(jsii_name="resetTermsOfServiceUrl")
    def reset_terms_of_service_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTermsOfServiceUrl", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetVersionDescription")
    def reset_version_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionDescription", []))

    @jsii.member(jsii_name="resetVersionSetId")
    def reset_version_set_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionSetId", []))

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
    @jsii.member(jsii_name="contact")
    def contact(self) -> "ApiManagementApiContactOutputReference":
        return typing.cast("ApiManagementApiContactOutputReference", jsii.get(self, "contact"))

    @builtins.property
    @jsii.member(jsii_name="import")
    def import_(self) -> "ApiManagementApiImportOutputReference":
        return typing.cast("ApiManagementApiImportOutputReference", jsii.get(self, "import"))

    @builtins.property
    @jsii.member(jsii_name="isCurrent")
    def is_current(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isCurrent"))

    @builtins.property
    @jsii.member(jsii_name="isOnline")
    def is_online(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isOnline"))

    @builtins.property
    @jsii.member(jsii_name="license")
    def license(self) -> "ApiManagementApiLicenseOutputReference":
        return typing.cast("ApiManagementApiLicenseOutputReference", jsii.get(self, "license"))

    @builtins.property
    @jsii.member(jsii_name="oauth2Authorization")
    def oauth2_authorization(
        self,
    ) -> "ApiManagementApiOauth2AuthorizationOutputReference":
        return typing.cast("ApiManagementApiOauth2AuthorizationOutputReference", jsii.get(self, "oauth2Authorization"))

    @builtins.property
    @jsii.member(jsii_name="openidAuthentication")
    def openid_authentication(
        self,
    ) -> "ApiManagementApiOpenidAuthenticationOutputReference":
        return typing.cast("ApiManagementApiOpenidAuthenticationOutputReference", jsii.get(self, "openidAuthentication"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionKeyParameterNames")
    def subscription_key_parameter_names(
        self,
    ) -> "ApiManagementApiSubscriptionKeyParameterNamesOutputReference":
        return typing.cast("ApiManagementApiSubscriptionKeyParameterNamesOutputReference", jsii.get(self, "subscriptionKeyParameterNames"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApiManagementApiTimeoutsOutputReference":
        return typing.cast("ApiManagementApiTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementNameInput")
    def api_management_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiManagementNameInput"))

    @builtins.property
    @jsii.member(jsii_name="apiTypeInput")
    def api_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="contactInput")
    def contact_input(self) -> typing.Optional["ApiManagementApiContact"]:
        return typing.cast(typing.Optional["ApiManagementApiContact"], jsii.get(self, "contactInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importInput")
    def import_input(self) -> typing.Optional["ApiManagementApiImport"]:
        return typing.cast(typing.Optional["ApiManagementApiImport"], jsii.get(self, "importInput"))

    @builtins.property
    @jsii.member(jsii_name="licenseInput")
    def license_input(self) -> typing.Optional["ApiManagementApiLicense"]:
        return typing.cast(typing.Optional["ApiManagementApiLicense"], jsii.get(self, "licenseInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauth2AuthorizationInput")
    def oauth2_authorization_input(
        self,
    ) -> typing.Optional["ApiManagementApiOauth2Authorization"]:
        return typing.cast(typing.Optional["ApiManagementApiOauth2Authorization"], jsii.get(self, "oauth2AuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="openidAuthenticationInput")
    def openid_authentication_input(
        self,
    ) -> typing.Optional["ApiManagementApiOpenidAuthentication"]:
        return typing.cast(typing.Optional["ApiManagementApiOpenidAuthentication"], jsii.get(self, "openidAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionDescriptionInput")
    def revision_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceUrlInput")
    def service_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceApiIdInput")
    def source_api_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceApiIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionKeyParameterNamesInput")
    def subscription_key_parameter_names_input(
        self,
    ) -> typing.Optional["ApiManagementApiSubscriptionKeyParameterNames"]:
        return typing.cast(typing.Optional["ApiManagementApiSubscriptionKeyParameterNames"], jsii.get(self, "subscriptionKeyParameterNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionRequiredInput")
    def subscription_required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "subscriptionRequiredInput"))

    @builtins.property
    @jsii.member(jsii_name="termsOfServiceUrlInput")
    def terms_of_service_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "termsOfServiceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementApiTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementApiTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionDescriptionInput")
    def version_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="versionSetIdInput")
    def version_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementName")
    def api_management_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementName"))

    @api_management_name.setter
    def api_management_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7383989e85952571d26e9a8622d9ec7a48bd26e515edb4a3cf7fc3371f315a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiType")
    def api_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiType"))

    @api_type.setter
    def api_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c89c28fc67dd3920f0c1ffc433a60220555fb317581bb3ba2f4571e5f2e511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d423b52ab228c9082e67d1288b937eadae94bf9400f1226fdc0a052a626c233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b74c7ba188f9831d385d815b0656f97acff034b13a6b61f2ff8350a5a58c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfbef39a0367608fda17deb7b2135f46a56323356566cfd07a1f9f35702b2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e0a3c1b2a905d014ac6528ed127d074db4967072938ea4065b19fea34fd73d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b386e2ead31f1d1ff4e86dffcd9c9569c3e0524faed441ecb8e78a829b5e141f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513aa9daefbc3be964a826442b6d61ebc8e4b49d64521c339e45396a1b2b38b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ef32e0979d7b4be4565f5a4685d9cc48132a4608316205319e962db571d4e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2835d5bc2a216fb2efb18530dd36854ffee0ef762d841be6bcb6f14679caad64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revisionDescription")
    def revision_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionDescription"))

    @revision_description.setter
    def revision_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d8b7a5e2f86614075dd6394306d7e0893b4099af5f7563fd90c7abd0d57956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revisionDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceUrl")
    def service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceUrl"))

    @service_url.setter
    def service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43f4c5a9df2f1ed41b84acf4a710f7235cd632c9c96bbf9f5b011638a16ad98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceApiId")
    def source_api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceApiId"))

    @source_api_id.setter
    def source_api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb161668c121f47d067e516c46ba6ecbe4a489ddb8309e7a26f64d728689ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceApiId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionRequired")
    def subscription_required(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "subscriptionRequired"))

    @subscription_required.setter
    def subscription_required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35222fe7525c5dc44e0ec6e711c8226f5e3c5a872bdc97e03cf77e8b3bb78868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionRequired", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="termsOfServiceUrl")
    def terms_of_service_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "termsOfServiceUrl"))

    @terms_of_service_url.setter
    def terms_of_service_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bc289674b0c02f35f3489f966b622b120a2033c72ec7ae699c729e2d9919965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "termsOfServiceUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84498ec6622fa9018c3b720874354ce5a04c64b7c1a1fa38ba7e94d047a329b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionDescription")
    def version_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionDescription"))

    @version_description.setter
    def version_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e54728df17afa351d3de96d98eff84e7738d27849a373b366cf966414395eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="versionSetId")
    def version_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionSetId"))

    @version_set_id.setter
    def version_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b164c3a1906d83625547dd6a226306ec79bc9342dadf002a197fefce8ebab8aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionSetId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_management_name": "apiManagementName",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "revision": "revision",
        "api_type": "apiType",
        "contact": "contact",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "import_": "import",
        "license": "license",
        "oauth2_authorization": "oauth2Authorization",
        "openid_authentication": "openidAuthentication",
        "path": "path",
        "protocols": "protocols",
        "revision_description": "revisionDescription",
        "service_url": "serviceUrl",
        "source_api_id": "sourceApiId",
        "subscription_key_parameter_names": "subscriptionKeyParameterNames",
        "subscription_required": "subscriptionRequired",
        "terms_of_service_url": "termsOfServiceUrl",
        "timeouts": "timeouts",
        "version": "version",
        "version_description": "versionDescription",
        "version_set_id": "versionSetId",
    },
)
class ApiManagementApiConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_management_name: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        revision: builtins.str,
        api_type: typing.Optional[builtins.str] = None,
        contact: typing.Optional[typing.Union["ApiManagementApiContact", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        import_: typing.Optional[typing.Union["ApiManagementApiImport", typing.Dict[builtins.str, typing.Any]]] = None,
        license: typing.Optional[typing.Union["ApiManagementApiLicense", typing.Dict[builtins.str, typing.Any]]] = None,
        oauth2_authorization: typing.Optional[typing.Union["ApiManagementApiOauth2Authorization", typing.Dict[builtins.str, typing.Any]]] = None,
        openid_authentication: typing.Optional[typing.Union["ApiManagementApiOpenidAuthentication", typing.Dict[builtins.str, typing.Any]]] = None,
        path: typing.Optional[builtins.str] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        revision_description: typing.Optional[builtins.str] = None,
        service_url: typing.Optional[builtins.str] = None,
        source_api_id: typing.Optional[builtins.str] = None,
        subscription_key_parameter_names: typing.Optional[typing.Union["ApiManagementApiSubscriptionKeyParameterNames", typing.Dict[builtins.str, typing.Any]]] = None,
        subscription_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        terms_of_service_url: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementApiTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        version_description: typing.Optional[builtins.str] = None,
        version_set_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#api_management_name ApiManagementApi#api_management_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#resource_group_name ApiManagementApi#resource_group_name}.
        :param revision: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#revision ApiManagementApi#revision}.
        :param api_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#api_type ApiManagementApi#api_type}.
        :param contact: contact block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#contact ApiManagementApi#contact}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#description ApiManagementApi#description}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#display_name ApiManagementApi#display_name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#id ApiManagementApi#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param import_: import block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#import ApiManagementApi#import}
        :param license: license block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#license ApiManagementApi#license}
        :param oauth2_authorization: oauth2_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#oauth2_authorization ApiManagementApi#oauth2_authorization}
        :param openid_authentication: openid_authentication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#openid_authentication ApiManagementApi#openid_authentication}
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#path ApiManagementApi#path}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#protocols ApiManagementApi#protocols}.
        :param revision_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#revision_description ApiManagementApi#revision_description}.
        :param service_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#service_url ApiManagementApi#service_url}.
        :param source_api_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#source_api_id ApiManagementApi#source_api_id}.
        :param subscription_key_parameter_names: subscription_key_parameter_names block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#subscription_key_parameter_names ApiManagementApi#subscription_key_parameter_names}
        :param subscription_required: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#subscription_required ApiManagementApi#subscription_required}.
        :param terms_of_service_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#terms_of_service_url ApiManagementApi#terms_of_service_url}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#timeouts ApiManagementApi#timeouts}
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version ApiManagementApi#version}.
        :param version_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version_description ApiManagementApi#version_description}.
        :param version_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version_set_id ApiManagementApi#version_set_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(contact, dict):
            contact = ApiManagementApiContact(**contact)
        if isinstance(import_, dict):
            import_ = ApiManagementApiImport(**import_)
        if isinstance(license, dict):
            license = ApiManagementApiLicense(**license)
        if isinstance(oauth2_authorization, dict):
            oauth2_authorization = ApiManagementApiOauth2Authorization(**oauth2_authorization)
        if isinstance(openid_authentication, dict):
            openid_authentication = ApiManagementApiOpenidAuthentication(**openid_authentication)
        if isinstance(subscription_key_parameter_names, dict):
            subscription_key_parameter_names = ApiManagementApiSubscriptionKeyParameterNames(**subscription_key_parameter_names)
        if isinstance(timeouts, dict):
            timeouts = ApiManagementApiTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d0aa337bfc9aa257b138065007ba534cd840a9444d8a25c37e7f25c1d3d126)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_management_name", value=api_management_name, expected_type=type_hints["api_management_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            check_type(argname="argument api_type", value=api_type, expected_type=type_hints["api_type"])
            check_type(argname="argument contact", value=contact, expected_type=type_hints["contact"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument import_", value=import_, expected_type=type_hints["import_"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument oauth2_authorization", value=oauth2_authorization, expected_type=type_hints["oauth2_authorization"])
            check_type(argname="argument openid_authentication", value=openid_authentication, expected_type=type_hints["openid_authentication"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument revision_description", value=revision_description, expected_type=type_hints["revision_description"])
            check_type(argname="argument service_url", value=service_url, expected_type=type_hints["service_url"])
            check_type(argname="argument source_api_id", value=source_api_id, expected_type=type_hints["source_api_id"])
            check_type(argname="argument subscription_key_parameter_names", value=subscription_key_parameter_names, expected_type=type_hints["subscription_key_parameter_names"])
            check_type(argname="argument subscription_required", value=subscription_required, expected_type=type_hints["subscription_required"])
            check_type(argname="argument terms_of_service_url", value=terms_of_service_url, expected_type=type_hints["terms_of_service_url"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
            check_type(argname="argument version_set_id", value=version_set_id, expected_type=type_hints["version_set_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_management_name": api_management_name,
            "name": name,
            "resource_group_name": resource_group_name,
            "revision": revision,
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
        if api_type is not None:
            self._values["api_type"] = api_type
        if contact is not None:
            self._values["contact"] = contact
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if import_ is not None:
            self._values["import_"] = import_
        if license is not None:
            self._values["license"] = license
        if oauth2_authorization is not None:
            self._values["oauth2_authorization"] = oauth2_authorization
        if openid_authentication is not None:
            self._values["openid_authentication"] = openid_authentication
        if path is not None:
            self._values["path"] = path
        if protocols is not None:
            self._values["protocols"] = protocols
        if revision_description is not None:
            self._values["revision_description"] = revision_description
        if service_url is not None:
            self._values["service_url"] = service_url
        if source_api_id is not None:
            self._values["source_api_id"] = source_api_id
        if subscription_key_parameter_names is not None:
            self._values["subscription_key_parameter_names"] = subscription_key_parameter_names
        if subscription_required is not None:
            self._values["subscription_required"] = subscription_required
        if terms_of_service_url is not None:
            self._values["terms_of_service_url"] = terms_of_service_url
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version
        if version_description is not None:
            self._values["version_description"] = version_description
        if version_set_id is not None:
            self._values["version_set_id"] = version_set_id

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
    def api_management_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#api_management_name ApiManagementApi#api_management_name}.'''
        result = self._values.get("api_management_name")
        assert result is not None, "Required property 'api_management_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#resource_group_name ApiManagementApi#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def revision(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#revision ApiManagementApi#revision}.'''
        result = self._values.get("revision")
        assert result is not None, "Required property 'revision' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#api_type ApiManagementApi#api_type}.'''
        result = self._values.get("api_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contact(self) -> typing.Optional["ApiManagementApiContact"]:
        '''contact block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#contact ApiManagementApi#contact}
        '''
        result = self._values.get("contact")
        return typing.cast(typing.Optional["ApiManagementApiContact"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#description ApiManagementApi#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#display_name ApiManagementApi#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#id ApiManagementApi#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def import_(self) -> typing.Optional["ApiManagementApiImport"]:
        '''import block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#import ApiManagementApi#import}
        '''
        result = self._values.get("import_")
        return typing.cast(typing.Optional["ApiManagementApiImport"], result)

    @builtins.property
    def license(self) -> typing.Optional["ApiManagementApiLicense"]:
        '''license block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#license ApiManagementApi#license}
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional["ApiManagementApiLicense"], result)

    @builtins.property
    def oauth2_authorization(
        self,
    ) -> typing.Optional["ApiManagementApiOauth2Authorization"]:
        '''oauth2_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#oauth2_authorization ApiManagementApi#oauth2_authorization}
        '''
        result = self._values.get("oauth2_authorization")
        return typing.cast(typing.Optional["ApiManagementApiOauth2Authorization"], result)

    @builtins.property
    def openid_authentication(
        self,
    ) -> typing.Optional["ApiManagementApiOpenidAuthentication"]:
        '''openid_authentication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#openid_authentication ApiManagementApi#openid_authentication}
        '''
        result = self._values.get("openid_authentication")
        return typing.cast(typing.Optional["ApiManagementApiOpenidAuthentication"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#path ApiManagementApi#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#protocols ApiManagementApi#protocols}.'''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def revision_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#revision_description ApiManagementApi#revision_description}.'''
        result = self._values.get("revision_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#service_url ApiManagementApi#service_url}.'''
        result = self._values.get("service_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_api_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#source_api_id ApiManagementApi#source_api_id}.'''
        result = self._values.get("source_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription_key_parameter_names(
        self,
    ) -> typing.Optional["ApiManagementApiSubscriptionKeyParameterNames"]:
        '''subscription_key_parameter_names block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#subscription_key_parameter_names ApiManagementApi#subscription_key_parameter_names}
        '''
        result = self._values.get("subscription_key_parameter_names")
        return typing.cast(typing.Optional["ApiManagementApiSubscriptionKeyParameterNames"], result)

    @builtins.property
    def subscription_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#subscription_required ApiManagementApi#subscription_required}.'''
        result = self._values.get("subscription_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def terms_of_service_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#terms_of_service_url ApiManagementApi#terms_of_service_url}.'''
        result = self._values.get("terms_of_service_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApiManagementApiTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#timeouts ApiManagementApi#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApiManagementApiTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version ApiManagementApi#version}.'''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version_description ApiManagementApi#version_description}.'''
        result = self._values.get("version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_set_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#version_set_id ApiManagementApi#version_set_id}.'''
        result = self._values.get("version_set_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiContact",
    jsii_struct_bases=[],
    name_mapping={"email": "email", "name": "name", "url": "url"},
)
class ApiManagementApiContact:
    def __init__(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#email ApiManagementApi#email}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#url ApiManagementApi#url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2a14ba1d4d0003356f7ab773207a3056a45b36b308bbefef89d43ffa334228)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if name is not None:
            self._values["name"] = name
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#email ApiManagementApi#email}.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#url ApiManagementApi#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiContact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiContactOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiContactOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__956eb48b90dd7d63363924f97602d0a31bf0d50b8432c44822e11f64c9158f3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEmail")
    def reset_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmail", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="emailInput")
    def email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @email.setter
    def email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97214e635352b013d4477049bb2c3bbf751b68b84f1fb0f59773faa3a7334d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "email", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc3fc1e576fd8f4e4544ae957f3e6fc49d62b97d2c972a2fe5b78ee0f07a341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882a0282d0765d98b8bcd51decd48ced8d867a58d8b738a6a5c49594c8cb9816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementApiContact]:
        return typing.cast(typing.Optional[ApiManagementApiContact], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementApiContact]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac63c1c6ee2837a72c0a4d575cc1ad0642954e92e3812508fb287c6791904555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiImport",
    jsii_struct_bases=[],
    name_mapping={
        "content_format": "contentFormat",
        "content_value": "contentValue",
        "wsdl_selector": "wsdlSelector",
    },
)
class ApiManagementApiImport:
    def __init__(
        self,
        *,
        content_format: builtins.str,
        content_value: builtins.str,
        wsdl_selector: typing.Optional[typing.Union["ApiManagementApiImportWsdlSelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param content_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#content_format ApiManagementApi#content_format}.
        :param content_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#content_value ApiManagementApi#content_value}.
        :param wsdl_selector: wsdl_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#wsdl_selector ApiManagementApi#wsdl_selector}
        '''
        if isinstance(wsdl_selector, dict):
            wsdl_selector = ApiManagementApiImportWsdlSelector(**wsdl_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0397dc2a8d92163a55cc4b37a10db1b1e01545da33cf4375ea3b4970eb4680a5)
            check_type(argname="argument content_format", value=content_format, expected_type=type_hints["content_format"])
            check_type(argname="argument content_value", value=content_value, expected_type=type_hints["content_value"])
            check_type(argname="argument wsdl_selector", value=wsdl_selector, expected_type=type_hints["wsdl_selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_format": content_format,
            "content_value": content_value,
        }
        if wsdl_selector is not None:
            self._values["wsdl_selector"] = wsdl_selector

    @builtins.property
    def content_format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#content_format ApiManagementApi#content_format}.'''
        result = self._values.get("content_format")
        assert result is not None, "Required property 'content_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#content_value ApiManagementApi#content_value}.'''
        result = self._values.get("content_value")
        assert result is not None, "Required property 'content_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def wsdl_selector(self) -> typing.Optional["ApiManagementApiImportWsdlSelector"]:
        '''wsdl_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#wsdl_selector ApiManagementApi#wsdl_selector}
        '''
        result = self._values.get("wsdl_selector")
        return typing.cast(typing.Optional["ApiManagementApiImportWsdlSelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiImport(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiImportOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiImportOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__033ebbc772fb0ce69b3ff5e44b92b4424e6212f8769612c90118af3fa3768bc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putWsdlSelector")
    def put_wsdl_selector(
        self,
        *,
        endpoint_name: builtins.str,
        service_name: builtins.str,
    ) -> None:
        '''
        :param endpoint_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#endpoint_name ApiManagementApi#endpoint_name}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#service_name ApiManagementApi#service_name}.
        '''
        value = ApiManagementApiImportWsdlSelector(
            endpoint_name=endpoint_name, service_name=service_name
        )

        return typing.cast(None, jsii.invoke(self, "putWsdlSelector", [value]))

    @jsii.member(jsii_name="resetWsdlSelector")
    def reset_wsdl_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWsdlSelector", []))

    @builtins.property
    @jsii.member(jsii_name="wsdlSelector")
    def wsdl_selector(self) -> "ApiManagementApiImportWsdlSelectorOutputReference":
        return typing.cast("ApiManagementApiImportWsdlSelectorOutputReference", jsii.get(self, "wsdlSelector"))

    @builtins.property
    @jsii.member(jsii_name="contentFormatInput")
    def content_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="contentValueInput")
    def content_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentValueInput"))

    @builtins.property
    @jsii.member(jsii_name="wsdlSelectorInput")
    def wsdl_selector_input(
        self,
    ) -> typing.Optional["ApiManagementApiImportWsdlSelector"]:
        return typing.cast(typing.Optional["ApiManagementApiImportWsdlSelector"], jsii.get(self, "wsdlSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="contentFormat")
    def content_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentFormat"))

    @content_format.setter
    def content_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7acc760bc5110e2f7304b7fe67f5455fb7cb9c747d88fb128475296634fde533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentValue")
    def content_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contentValue"))

    @content_value.setter
    def content_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538f9b6198ff901636f877bff7078514e16f13231a89524f1caef9ef6a80e703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementApiImport]:
        return typing.cast(typing.Optional[ApiManagementApiImport], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementApiImport]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ea9dfa65a95010bd1bf0f65dd35e1ab7a67d87312dda6b5b547cad56c66819b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiImportWsdlSelector",
    jsii_struct_bases=[],
    name_mapping={"endpoint_name": "endpointName", "service_name": "serviceName"},
)
class ApiManagementApiImportWsdlSelector:
    def __init__(
        self,
        *,
        endpoint_name: builtins.str,
        service_name: builtins.str,
    ) -> None:
        '''
        :param endpoint_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#endpoint_name ApiManagementApi#endpoint_name}.
        :param service_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#service_name ApiManagementApi#service_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c91dd770b812dd739ecbe388c8085b2a92b4629f22f112a6cde6eb35747d41)
            check_type(argname="argument endpoint_name", value=endpoint_name, expected_type=type_hints["endpoint_name"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_name": endpoint_name,
            "service_name": service_name,
        }

    @builtins.property
    def endpoint_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#endpoint_name ApiManagementApi#endpoint_name}.'''
        result = self._values.get("endpoint_name")
        assert result is not None, "Required property 'endpoint_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#service_name ApiManagementApi#service_name}.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiImportWsdlSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiImportWsdlSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiImportWsdlSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f6e362443ef65b1dd45e8e69514c4e4c750697014fca931acfff0d50930c036)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endpointNameInput")
    def endpoint_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointName")
    def endpoint_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointName"))

    @endpoint_name.setter
    def endpoint_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bad0d89885ef908e262ed43da7322ac3f119ca04d0898a74873aadd9ff0227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313e1793b8a996ce6808ee5782d1cab5608f333deb9de28839e23fd6956e63a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementApiImportWsdlSelector]:
        return typing.cast(typing.Optional[ApiManagementApiImportWsdlSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiImportWsdlSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fec7612498f261cf02e573f350dda94c9c9146e55b68db116b869dbda97ae09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiLicense",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class ApiManagementApiLicense:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#url ApiManagementApi#url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7b2fa20716471190ce2b29193746c9e923fa6dd7ba87991fb1173bdabb45ad)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#name ApiManagementApi#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#url ApiManagementApi#url}.'''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiLicense(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiLicenseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiLicenseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cbb23e1217a939a4ea3e3fb05b0c6a66edf054d199b6bf48db17c504d185294)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetUrl")
    def reset_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrl", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c789bd81c84b5cb582e284d79997c304c0c7f712f6b597e4c563b62c8d413a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dc8e444b36e44f2f5b3c46c93efcf021ac243bfda33dfa3467e994d0634470e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementApiLicense]:
        return typing.cast(typing.Optional[ApiManagementApiLicense], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementApiLicense]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696ad261e90aa23ee2e0cd79eab9747b2e348a0bc8fb8f8bd5fac9314fd8d401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiOauth2Authorization",
    jsii_struct_bases=[],
    name_mapping={
        "authorization_server_name": "authorizationServerName",
        "scope": "scope",
    },
)
class ApiManagementApiOauth2Authorization:
    def __init__(
        self,
        *,
        authorization_server_name: builtins.str,
        scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param authorization_server_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#authorization_server_name ApiManagementApi#authorization_server_name}.
        :param scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#scope ApiManagementApi#scope}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e01d1ca22f3139e4cd886c1e95ab02b2f267e368a1fb612b22a519efa911ac7)
            check_type(argname="argument authorization_server_name", value=authorization_server_name, expected_type=type_hints["authorization_server_name"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authorization_server_name": authorization_server_name,
        }
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def authorization_server_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#authorization_server_name ApiManagementApi#authorization_server_name}.'''
        result = self._values.get("authorization_server_name")
        assert result is not None, "Required property 'authorization_server_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#scope ApiManagementApi#scope}.'''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiOauth2Authorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiOauth2AuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiOauth2AuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__583058abe7eefafa4a86196cdd09def49869ef545d9bf451ecb744b8f12e88f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

    @builtins.property
    @jsii.member(jsii_name="authorizationServerNameInput")
    def authorization_server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authorizationServerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizationServerName")
    def authorization_server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorizationServerName"))

    @authorization_server_name.setter
    def authorization_server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d8e56ffbc233e6d11cbb75b3a63ac6ee479dee8d0b9075a5cd112ccbc53e616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizationServerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a729527222d0fac4529071cf74e0bc171bdc3b129d374ced6e5482a307476f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementApiOauth2Authorization]:
        return typing.cast(typing.Optional[ApiManagementApiOauth2Authorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiOauth2Authorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd32dcabbc38e2720112619b891581c030169f23370738ee9b6d823f4ed59a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiOpenidAuthentication",
    jsii_struct_bases=[],
    name_mapping={
        "openid_provider_name": "openidProviderName",
        "bearer_token_sending_methods": "bearerTokenSendingMethods",
    },
)
class ApiManagementApiOpenidAuthentication:
    def __init__(
        self,
        *,
        openid_provider_name: builtins.str,
        bearer_token_sending_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param openid_provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#openid_provider_name ApiManagementApi#openid_provider_name}.
        :param bearer_token_sending_methods: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#bearer_token_sending_methods ApiManagementApi#bearer_token_sending_methods}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af1c2b6c8d900992aa4e6c80216b9a4f8121afe118ef7e28ce97fc834e30e51)
            check_type(argname="argument openid_provider_name", value=openid_provider_name, expected_type=type_hints["openid_provider_name"])
            check_type(argname="argument bearer_token_sending_methods", value=bearer_token_sending_methods, expected_type=type_hints["bearer_token_sending_methods"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "openid_provider_name": openid_provider_name,
        }
        if bearer_token_sending_methods is not None:
            self._values["bearer_token_sending_methods"] = bearer_token_sending_methods

    @builtins.property
    def openid_provider_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#openid_provider_name ApiManagementApi#openid_provider_name}.'''
        result = self._values.get("openid_provider_name")
        assert result is not None, "Required property 'openid_provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bearer_token_sending_methods(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#bearer_token_sending_methods ApiManagementApi#bearer_token_sending_methods}.'''
        result = self._values.get("bearer_token_sending_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiOpenidAuthentication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiOpenidAuthenticationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiOpenidAuthenticationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48d0d5f3218a372ee771d59df93daef01f082e5006047f30a99071d30a27ba98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBearerTokenSendingMethods")
    def reset_bearer_token_sending_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBearerTokenSendingMethods", []))

    @builtins.property
    @jsii.member(jsii_name="bearerTokenSendingMethodsInput")
    def bearer_token_sending_methods_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "bearerTokenSendingMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="openidProviderNameInput")
    def openid_provider_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "openidProviderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bearerTokenSendingMethods")
    def bearer_token_sending_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "bearerTokenSendingMethods"))

    @bearer_token_sending_methods.setter
    def bearer_token_sending_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b312ac44bb6cc14e154b4cc958ffe390e772739c8c5415fbb28c8777eb0f0b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bearerTokenSendingMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="openidProviderName")
    def openid_provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openidProviderName"))

    @openid_provider_name.setter
    def openid_provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74584e957c567a40aacc7636ec1a15c929f842ab9d88fb619b20ac0f9be285b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openidProviderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementApiOpenidAuthentication]:
        return typing.cast(typing.Optional[ApiManagementApiOpenidAuthentication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiOpenidAuthentication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef85a3feca6d0f4c63f41952decebdb2255d58aa51a5e502af1503d1870e9a89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiSubscriptionKeyParameterNames",
    jsii_struct_bases=[],
    name_mapping={"header": "header", "query": "query"},
)
class ApiManagementApiSubscriptionKeyParameterNames:
    def __init__(self, *, header: builtins.str, query: builtins.str) -> None:
        '''
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#header ApiManagementApi#header}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#query ApiManagementApi#query}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13e8ff35bc8cf79b4b478fa937956b52160828d5a763c643df1953fdb1cf5ce)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
            "query": query,
        }

    @builtins.property
    def header(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#header ApiManagementApi#header}.'''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#query ApiManagementApi#query}.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiSubscriptionKeyParameterNames(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiSubscriptionKeyParameterNamesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiSubscriptionKeyParameterNamesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cc42e364f08f9367523f5f58a3b149b63224a4453f06dd2f0fb1f663422eee5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b85b25ecdd9e74c5b2f3917108668973bd81fedd4ddab622f70e1ce7ad4af3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693c3e6a15b20964cea414921b62c22c1cc7f82554d5f96dee7933fe70bf306f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiSubscriptionKeyParameterNames]:
        return typing.cast(typing.Optional[ApiManagementApiSubscriptionKeyParameterNames], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiSubscriptionKeyParameterNames],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5fe59684aff0eff4d92858f22d8e91481f0f95d2bc7c68af4e694b028ed1553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApiManagementApiTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#create ApiManagementApi#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#delete ApiManagementApi#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#read ApiManagementApi#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#update ApiManagementApi#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0da2083f154a02291e577a0dbc4c85ede39aa9a3ba2bdd1da6ab9d6e4aa039d0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#create ApiManagementApi#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#delete ApiManagementApi#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#read ApiManagementApi#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api#update ApiManagementApi#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApi.ApiManagementApiTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46e023f14355f6e8717b6f5d641d211c00a927acd516f76157d0fa9a7ab2ab22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b61c04c91372041e647f188ebfb44c560cc1e943ebfb5aff76ae8def24ce3472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e97c378e8da2f6bf94068012ad42fc04ec6daaeb902dd2d5d32ec90af2fb860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee6c9062a41dacea363f4d31c47f5810b3aba1d603dc05d45b166eb22f35c640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a65b98c8a4d78d7555a705d0f10ee9d191e2c7ce83dbc68fc20577447920aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123b95e5bd5f5ff09ebede6288edc7ffd219357c0bfee235d12d93e9c9fe23ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiManagementApi",
    "ApiManagementApiConfig",
    "ApiManagementApiContact",
    "ApiManagementApiContactOutputReference",
    "ApiManagementApiImport",
    "ApiManagementApiImportOutputReference",
    "ApiManagementApiImportWsdlSelector",
    "ApiManagementApiImportWsdlSelectorOutputReference",
    "ApiManagementApiLicense",
    "ApiManagementApiLicenseOutputReference",
    "ApiManagementApiOauth2Authorization",
    "ApiManagementApiOauth2AuthorizationOutputReference",
    "ApiManagementApiOpenidAuthentication",
    "ApiManagementApiOpenidAuthenticationOutputReference",
    "ApiManagementApiSubscriptionKeyParameterNames",
    "ApiManagementApiSubscriptionKeyParameterNamesOutputReference",
    "ApiManagementApiTimeouts",
    "ApiManagementApiTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d45ccc9a927ac6a18ca6e6d15fdf6d488bf0435af6abad86efd993e662a2b226(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_management_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    revision: builtins.str,
    api_type: typing.Optional[builtins.str] = None,
    contact: typing.Optional[typing.Union[ApiManagementApiContact, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    import_: typing.Optional[typing.Union[ApiManagementApiImport, typing.Dict[builtins.str, typing.Any]]] = None,
    license: typing.Optional[typing.Union[ApiManagementApiLicense, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_authorization: typing.Optional[typing.Union[ApiManagementApiOauth2Authorization, typing.Dict[builtins.str, typing.Any]]] = None,
    openid_authentication: typing.Optional[typing.Union[ApiManagementApiOpenidAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    revision_description: typing.Optional[builtins.str] = None,
    service_url: typing.Optional[builtins.str] = None,
    source_api_id: typing.Optional[builtins.str] = None,
    subscription_key_parameter_names: typing.Optional[typing.Union[ApiManagementApiSubscriptionKeyParameterNames, typing.Dict[builtins.str, typing.Any]]] = None,
    subscription_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    terms_of_service_url: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementApiTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    version_description: typing.Optional[builtins.str] = None,
    version_set_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__8d3c7e9439fe58be63b7cf4dc9fb3c5233f44e1240e3f6f11fb804b26691b19d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7383989e85952571d26e9a8622d9ec7a48bd26e515edb4a3cf7fc3371f315a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c89c28fc67dd3920f0c1ffc433a60220555fb317581bb3ba2f4571e5f2e511(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d423b52ab228c9082e67d1288b937eadae94bf9400f1226fdc0a052a626c233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b74c7ba188f9831d385d815b0656f97acff034b13a6b61f2ff8350a5a58c63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfbef39a0367608fda17deb7b2135f46a56323356566cfd07a1f9f35702b2f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e0a3c1b2a905d014ac6528ed127d074db4967072938ea4065b19fea34fd73d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b386e2ead31f1d1ff4e86dffcd9c9569c3e0524faed441ecb8e78a829b5e141f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513aa9daefbc3be964a826442b6d61ebc8e4b49d64521c339e45396a1b2b38b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef32e0979d7b4be4565f5a4685d9cc48132a4608316205319e962db571d4e9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2835d5bc2a216fb2efb18530dd36854ffee0ef762d841be6bcb6f14679caad64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d8b7a5e2f86614075dd6394306d7e0893b4099af5f7563fd90c7abd0d57956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43f4c5a9df2f1ed41b84acf4a710f7235cd632c9c96bbf9f5b011638a16ad98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb161668c121f47d067e516c46ba6ecbe4a489ddb8309e7a26f64d728689ba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35222fe7525c5dc44e0ec6e711c8226f5e3c5a872bdc97e03cf77e8b3bb78868(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bc289674b0c02f35f3489f966b622b120a2033c72ec7ae699c729e2d9919965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84498ec6622fa9018c3b720874354ce5a04c64b7c1a1fa38ba7e94d047a329b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e54728df17afa351d3de96d98eff84e7738d27849a373b366cf966414395eb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b164c3a1906d83625547dd6a226306ec79bc9342dadf002a197fefce8ebab8aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d0aa337bfc9aa257b138065007ba534cd840a9444d8a25c37e7f25c1d3d126(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_management_name: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    revision: builtins.str,
    api_type: typing.Optional[builtins.str] = None,
    contact: typing.Optional[typing.Union[ApiManagementApiContact, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    import_: typing.Optional[typing.Union[ApiManagementApiImport, typing.Dict[builtins.str, typing.Any]]] = None,
    license: typing.Optional[typing.Union[ApiManagementApiLicense, typing.Dict[builtins.str, typing.Any]]] = None,
    oauth2_authorization: typing.Optional[typing.Union[ApiManagementApiOauth2Authorization, typing.Dict[builtins.str, typing.Any]]] = None,
    openid_authentication: typing.Optional[typing.Union[ApiManagementApiOpenidAuthentication, typing.Dict[builtins.str, typing.Any]]] = None,
    path: typing.Optional[builtins.str] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    revision_description: typing.Optional[builtins.str] = None,
    service_url: typing.Optional[builtins.str] = None,
    source_api_id: typing.Optional[builtins.str] = None,
    subscription_key_parameter_names: typing.Optional[typing.Union[ApiManagementApiSubscriptionKeyParameterNames, typing.Dict[builtins.str, typing.Any]]] = None,
    subscription_required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    terms_of_service_url: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementApiTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
    version_description: typing.Optional[builtins.str] = None,
    version_set_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2a14ba1d4d0003356f7ab773207a3056a45b36b308bbefef89d43ffa334228(
    *,
    email: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956eb48b90dd7d63363924f97602d0a31bf0d50b8432c44822e11f64c9158f3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97214e635352b013d4477049bb2c3bbf751b68b84f1fb0f59773faa3a7334d61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc3fc1e576fd8f4e4544ae957f3e6fc49d62b97d2c972a2fe5b78ee0f07a341(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882a0282d0765d98b8bcd51decd48ced8d867a58d8b738a6a5c49594c8cb9816(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac63c1c6ee2837a72c0a4d575cc1ad0642954e92e3812508fb287c6791904555(
    value: typing.Optional[ApiManagementApiContact],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0397dc2a8d92163a55cc4b37a10db1b1e01545da33cf4375ea3b4970eb4680a5(
    *,
    content_format: builtins.str,
    content_value: builtins.str,
    wsdl_selector: typing.Optional[typing.Union[ApiManagementApiImportWsdlSelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033ebbc772fb0ce69b3ff5e44b92b4424e6212f8769612c90118af3fa3768bc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7acc760bc5110e2f7304b7fe67f5455fb7cb9c747d88fb128475296634fde533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538f9b6198ff901636f877bff7078514e16f13231a89524f1caef9ef6a80e703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ea9dfa65a95010bd1bf0f65dd35e1ab7a67d87312dda6b5b547cad56c66819b(
    value: typing.Optional[ApiManagementApiImport],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c91dd770b812dd739ecbe388c8085b2a92b4629f22f112a6cde6eb35747d41(
    *,
    endpoint_name: builtins.str,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6e362443ef65b1dd45e8e69514c4e4c750697014fca931acfff0d50930c036(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bad0d89885ef908e262ed43da7322ac3f119ca04d0898a74873aadd9ff0227(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313e1793b8a996ce6808ee5782d1cab5608f333deb9de28839e23fd6956e63a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fec7612498f261cf02e573f350dda94c9c9146e55b68db116b869dbda97ae09d(
    value: typing.Optional[ApiManagementApiImportWsdlSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7b2fa20716471190ce2b29193746c9e923fa6dd7ba87991fb1173bdabb45ad(
    *,
    name: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbb23e1217a939a4ea3e3fb05b0c6a66edf054d199b6bf48db17c504d185294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c789bd81c84b5cb582e284d79997c304c0c7f712f6b597e4c563b62c8d413a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dc8e444b36e44f2f5b3c46c93efcf021ac243bfda33dfa3467e994d0634470e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696ad261e90aa23ee2e0cd79eab9747b2e348a0bc8fb8f8bd5fac9314fd8d401(
    value: typing.Optional[ApiManagementApiLicense],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e01d1ca22f3139e4cd886c1e95ab02b2f267e368a1fb612b22a519efa911ac7(
    *,
    authorization_server_name: builtins.str,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583058abe7eefafa4a86196cdd09def49869ef545d9bf451ecb744b8f12e88f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8e56ffbc233e6d11cbb75b3a63ac6ee479dee8d0b9075a5cd112ccbc53e616(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a729527222d0fac4529071cf74e0bc171bdc3b129d374ced6e5482a307476f60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd32dcabbc38e2720112619b891581c030169f23370738ee9b6d823f4ed59a14(
    value: typing.Optional[ApiManagementApiOauth2Authorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af1c2b6c8d900992aa4e6c80216b9a4f8121afe118ef7e28ce97fc834e30e51(
    *,
    openid_provider_name: builtins.str,
    bearer_token_sending_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d0d5f3218a372ee771d59df93daef01f082e5006047f30a99071d30a27ba98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b312ac44bb6cc14e154b4cc958ffe390e772739c8c5415fbb28c8777eb0f0b3d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74584e957c567a40aacc7636ec1a15c929f842ab9d88fb619b20ac0f9be285b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef85a3feca6d0f4c63f41952decebdb2255d58aa51a5e502af1503d1870e9a89(
    value: typing.Optional[ApiManagementApiOpenidAuthentication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13e8ff35bc8cf79b4b478fa937956b52160828d5a763c643df1953fdb1cf5ce(
    *,
    header: builtins.str,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc42e364f08f9367523f5f58a3b149b63224a4453f06dd2f0fb1f663422eee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b85b25ecdd9e74c5b2f3917108668973bd81fedd4ddab622f70e1ce7ad4af3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693c3e6a15b20964cea414921b62c22c1cc7f82554d5f96dee7933fe70bf306f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5fe59684aff0eff4d92858f22d8e91481f0f95d2bc7c68af4e694b028ed1553(
    value: typing.Optional[ApiManagementApiSubscriptionKeyParameterNames],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da2083f154a02291e577a0dbc4c85ede39aa9a3ba2bdd1da6ab9d6e4aa039d0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e023f14355f6e8717b6f5d641d211c00a927acd516f76157d0fa9a7ab2ab22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61c04c91372041e647f188ebfb44c560cc1e943ebfb5aff76ae8def24ce3472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e97c378e8da2f6bf94068012ad42fc04ec6daaeb902dd2d5d32ec90af2fb860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6c9062a41dacea363f4d31c47f5810b3aba1d603dc05d45b166eb22f35c640(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a65b98c8a4d78d7555a705d0f10ee9d191e2c7ce83dbc68fc20577447920aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123b95e5bd5f5ff09ebede6288edc7ffd219357c0bfee235d12d93e9c9fe23ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `azurerm_api_management_backend`

Refer to the Terraform Registry for docs: [`azurerm_api_management_backend`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend).
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


class ApiManagementBackend(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackend",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend azurerm_api_management_backend}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_management_name: builtins.str,
        name: builtins.str,
        protocol: builtins.str,
        resource_group_name: builtins.str,
        url: builtins.str,
        credentials: typing.Optional[typing.Union["ApiManagementBackendCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["ApiManagementBackendProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_id: typing.Optional[builtins.str] = None,
        service_fabric_cluster: typing.Optional[typing.Union["ApiManagementBackendServiceFabricCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementBackendTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
        tls: typing.Optional[typing.Union["ApiManagementBackendTls", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend azurerm_api_management_backend} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#api_management_name ApiManagementBackend#api_management_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#name ApiManagementBackend#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#protocol ApiManagementBackend#protocol}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#resource_group_name ApiManagementBackend#resource_group_name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#url ApiManagementBackend#url}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#credentials ApiManagementBackend#credentials}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#description ApiManagementBackend#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#id ApiManagementBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#proxy ApiManagementBackend#proxy}
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#resource_id ApiManagementBackend#resource_id}.
        :param service_fabric_cluster: service_fabric_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#service_fabric_cluster ApiManagementBackend#service_fabric_cluster}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#timeouts ApiManagementBackend#timeouts}
        :param title: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#title ApiManagementBackend#title}.
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#tls ApiManagementBackend#tls}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8169f87e71bac7fdd3f8627e246c53dac466a60f045f72d47e40adb849f67d40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiManagementBackendConfig(
            api_management_name=api_management_name,
            name=name,
            protocol=protocol,
            resource_group_name=resource_group_name,
            url=url,
            credentials=credentials,
            description=description,
            id=id,
            proxy=proxy,
            resource_id=resource_id,
            service_fabric_cluster=service_fabric_cluster,
            timeouts=timeouts,
            title=title,
            tls=tls,
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
        '''Generates CDKTF code for importing a ApiManagementBackend resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiManagementBackend to import.
        :param import_from_id: The id of the existing ApiManagementBackend that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiManagementBackend to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c131f8c75fe8a88529e75fde18a2d915607f975ba5e493cd858e8d786b0f4176)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(
        self,
        *,
        authorization: typing.Optional[typing.Union["ApiManagementBackendCredentialsAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Sequence[builtins.str]] = None,
        header: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#authorization ApiManagementBackend#authorization}
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#certificate ApiManagementBackend#certificate}.
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#header ApiManagementBackend#header}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#query ApiManagementBackend#query}.
        '''
        value = ApiManagementBackendCredentials(
            authorization=authorization,
            certificate=certificate,
            header=header,
            query=query,
        )

        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="putProxy")
    def put_proxy(
        self,
        *,
        url: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#url ApiManagementBackend#url}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#username ApiManagementBackend#username}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#password ApiManagementBackend#password}.
        '''
        value = ApiManagementBackendProxy(
            url=url, username=username, password=password
        )

        return typing.cast(None, jsii.invoke(self, "putProxy", [value]))

    @jsii.member(jsii_name="putServiceFabricCluster")
    def put_service_fabric_cluster(
        self,
        *,
        management_endpoints: typing.Sequence[builtins.str],
        max_partition_resolution_retries: jsii.Number,
        client_certificate_id: typing.Optional[builtins.str] = None,
        client_certificate_thumbprint: typing.Optional[builtins.str] = None,
        server_certificate_thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_x509_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementBackendServiceFabricClusterServerX509Name", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param management_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#management_endpoints ApiManagementBackend#management_endpoints}.
        :param max_partition_resolution_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#max_partition_resolution_retries ApiManagementBackend#max_partition_resolution_retries}.
        :param client_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#client_certificate_id ApiManagementBackend#client_certificate_id}.
        :param client_certificate_thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#client_certificate_thumbprint ApiManagementBackend#client_certificate_thumbprint}.
        :param server_certificate_thumbprints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#server_certificate_thumbprints ApiManagementBackend#server_certificate_thumbprints}.
        :param server_x509_name: server_x509_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#server_x509_name ApiManagementBackend#server_x509_name}
        '''
        value = ApiManagementBackendServiceFabricCluster(
            management_endpoints=management_endpoints,
            max_partition_resolution_retries=max_partition_resolution_retries,
            client_certificate_id=client_certificate_id,
            client_certificate_thumbprint=client_certificate_thumbprint,
            server_certificate_thumbprints=server_certificate_thumbprints,
            server_x509_name=server_x509_name,
        )

        return typing.cast(None, jsii.invoke(self, "putServiceFabricCluster", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#create ApiManagementBackend#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#delete ApiManagementBackend#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#read ApiManagementBackend#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#update ApiManagementBackend#update}.
        '''
        value = ApiManagementBackendTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTls")
    def put_tls(
        self,
        *,
        validate_certificate_chain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validate_certificate_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param validate_certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#validate_certificate_chain ApiManagementBackend#validate_certificate_chain}.
        :param validate_certificate_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#validate_certificate_name ApiManagementBackend#validate_certificate_name}.
        '''
        value = ApiManagementBackendTls(
            validate_certificate_chain=validate_certificate_chain,
            validate_certificate_name=validate_certificate_name,
        )

        return typing.cast(None, jsii.invoke(self, "putTls", [value]))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

    @jsii.member(jsii_name="resetResourceId")
    def reset_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceId", []))

    @jsii.member(jsii_name="resetServiceFabricCluster")
    def reset_service_fabric_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceFabricCluster", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

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
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> "ApiManagementBackendCredentialsOutputReference":
        return typing.cast("ApiManagementBackendCredentialsOutputReference", jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> "ApiManagementBackendProxyOutputReference":
        return typing.cast("ApiManagementBackendProxyOutputReference", jsii.get(self, "proxy"))

    @builtins.property
    @jsii.member(jsii_name="serviceFabricCluster")
    def service_fabric_cluster(
        self,
    ) -> "ApiManagementBackendServiceFabricClusterOutputReference":
        return typing.cast("ApiManagementBackendServiceFabricClusterOutputReference", jsii.get(self, "serviceFabricCluster"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApiManagementBackendTimeoutsOutputReference":
        return typing.cast("ApiManagementBackendTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> "ApiManagementBackendTlsOutputReference":
        return typing.cast("ApiManagementBackendTlsOutputReference", jsii.get(self, "tls"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementNameInput")
    def api_management_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiManagementNameInput"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(self) -> typing.Optional["ApiManagementBackendCredentials"]:
        return typing.cast(typing.Optional["ApiManagementBackendCredentials"], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(self) -> typing.Optional["ApiManagementBackendProxy"]:
        return typing.cast(typing.Optional["ApiManagementBackendProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceFabricClusterInput")
    def service_fabric_cluster_input(
        self,
    ) -> typing.Optional["ApiManagementBackendServiceFabricCluster"]:
        return typing.cast(typing.Optional["ApiManagementBackendServiceFabricCluster"], jsii.get(self, "serviceFabricClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementBackendTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementBackendTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(self) -> typing.Optional["ApiManagementBackendTls"]:
        return typing.cast(typing.Optional["ApiManagementBackendTls"], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementName")
    def api_management_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementName"))

    @api_management_name.setter
    def api_management_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3c2e8c03a7e1123f9915b2e0ec9e9decb3bff3e1d21ba5aba64041df137bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__981d6e09bc46150c197d9d0c755e3b950412b45ba57efe4f09d413ca07ef23d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08835ff30450941ca05dd63627e191816b790df8d5cb9b80bc11f1ed270fc5e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86fa765d54b9049695272e5640ed2511b265a8b7bb1e31e28bf77a35e16e9a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832025441d909e0c08b911bf7cd161cbf4aaf5eb2b3cebb4190ea9b22e033689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbdc3073b462275255d238fb00c072895747cd85aa7cc3754bab29b25541112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7420813b9f531008d6afab74e9cec39ca4c159d7ab1312a4959ca7ad71c80f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe480441bedc060337bb9c73f6fe9ecc3288a96ff942ec71eece1413cfcf498f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e097f305d707ea1baf48ab3b869fa9abb9558f1e72fb8c0576a645c3948054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendConfig",
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
        "protocol": "protocol",
        "resource_group_name": "resourceGroupName",
        "url": "url",
        "credentials": "credentials",
        "description": "description",
        "id": "id",
        "proxy": "proxy",
        "resource_id": "resourceId",
        "service_fabric_cluster": "serviceFabricCluster",
        "timeouts": "timeouts",
        "title": "title",
        "tls": "tls",
    },
)
class ApiManagementBackendConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        protocol: builtins.str,
        resource_group_name: builtins.str,
        url: builtins.str,
        credentials: typing.Optional[typing.Union["ApiManagementBackendCredentials", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["ApiManagementBackendProxy", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_id: typing.Optional[builtins.str] = None,
        service_fabric_cluster: typing.Optional[typing.Union["ApiManagementBackendServiceFabricCluster", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementBackendTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
        tls: typing.Optional[typing.Union["ApiManagementBackendTls", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#api_management_name ApiManagementBackend#api_management_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#name ApiManagementBackend#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#protocol ApiManagementBackend#protocol}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#resource_group_name ApiManagementBackend#resource_group_name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#url ApiManagementBackend#url}.
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#credentials ApiManagementBackend#credentials}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#description ApiManagementBackend#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#id ApiManagementBackend#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#proxy ApiManagementBackend#proxy}
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#resource_id ApiManagementBackend#resource_id}.
        :param service_fabric_cluster: service_fabric_cluster block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#service_fabric_cluster ApiManagementBackend#service_fabric_cluster}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#timeouts ApiManagementBackend#timeouts}
        :param title: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#title ApiManagementBackend#title}.
        :param tls: tls block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#tls ApiManagementBackend#tls}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(credentials, dict):
            credentials = ApiManagementBackendCredentials(**credentials)
        if isinstance(proxy, dict):
            proxy = ApiManagementBackendProxy(**proxy)
        if isinstance(service_fabric_cluster, dict):
            service_fabric_cluster = ApiManagementBackendServiceFabricCluster(**service_fabric_cluster)
        if isinstance(timeouts, dict):
            timeouts = ApiManagementBackendTimeouts(**timeouts)
        if isinstance(tls, dict):
            tls = ApiManagementBackendTls(**tls)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0980c82cd9314550102cbca14e5ca7db7c539efb2a8d3dd09c5da41fb9ccc58c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_management_name", value=api_management_name, expected_type=type_hints["api_management_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument service_fabric_cluster", value=service_fabric_cluster, expected_type=type_hints["service_fabric_cluster"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_management_name": api_management_name,
            "name": name,
            "protocol": protocol,
            "resource_group_name": resource_group_name,
            "url": url,
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
        if credentials is not None:
            self._values["credentials"] = credentials
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if proxy is not None:
            self._values["proxy"] = proxy
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if service_fabric_cluster is not None:
            self._values["service_fabric_cluster"] = service_fabric_cluster
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if title is not None:
            self._values["title"] = title
        if tls is not None:
            self._values["tls"] = tls

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#api_management_name ApiManagementBackend#api_management_name}.'''
        result = self._values.get("api_management_name")
        assert result is not None, "Required property 'api_management_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#name ApiManagementBackend#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#protocol ApiManagementBackend#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#resource_group_name ApiManagementBackend#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#url ApiManagementBackend#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(self) -> typing.Optional["ApiManagementBackendCredentials"]:
        '''credentials block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#credentials ApiManagementBackend#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional["ApiManagementBackendCredentials"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#description ApiManagementBackend#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#id ApiManagementBackend#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional["ApiManagementBackendProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#proxy ApiManagementBackend#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["ApiManagementBackendProxy"], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#resource_id ApiManagementBackend#resource_id}.'''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_fabric_cluster(
        self,
    ) -> typing.Optional["ApiManagementBackendServiceFabricCluster"]:
        '''service_fabric_cluster block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#service_fabric_cluster ApiManagementBackend#service_fabric_cluster}
        '''
        result = self._values.get("service_fabric_cluster")
        return typing.cast(typing.Optional["ApiManagementBackendServiceFabricCluster"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApiManagementBackendTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#timeouts ApiManagementBackend#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApiManagementBackendTimeouts"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#title ApiManagementBackend#title}.'''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls(self) -> typing.Optional["ApiManagementBackendTls"]:
        '''tls block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#tls ApiManagementBackend#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional["ApiManagementBackendTls"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "authorization": "authorization",
        "certificate": "certificate",
        "header": "header",
        "query": "query",
    },
)
class ApiManagementBackendCredentials:
    def __init__(
        self,
        *,
        authorization: typing.Optional[typing.Union["ApiManagementBackendCredentialsAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        certificate: typing.Optional[typing.Sequence[builtins.str]] = None,
        header: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param authorization: authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#authorization ApiManagementBackend#authorization}
        :param certificate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#certificate ApiManagementBackend#certificate}.
        :param header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#header ApiManagementBackend#header}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#query ApiManagementBackend#query}.
        '''
        if isinstance(authorization, dict):
            authorization = ApiManagementBackendCredentialsAuthorization(**authorization)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__167b5946b1cb3e8da3e19ce22545c852e41e0aa986590d941f3d1cd86b96b3c2)
            check_type(argname="argument authorization", value=authorization, expected_type=type_hints["authorization"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorization is not None:
            self._values["authorization"] = authorization
        if certificate is not None:
            self._values["certificate"] = certificate
        if header is not None:
            self._values["header"] = header
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def authorization(
        self,
    ) -> typing.Optional["ApiManagementBackendCredentialsAuthorization"]:
        '''authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#authorization ApiManagementBackend#authorization}
        '''
        result = self._values.get("authorization")
        return typing.cast(typing.Optional["ApiManagementBackendCredentialsAuthorization"], result)

    @builtins.property
    def certificate(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#certificate ApiManagementBackend#certificate}.'''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def header(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#header ApiManagementBackend#header}.'''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#query ApiManagementBackend#query}.'''
        result = self._values.get("query")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementBackendCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendCredentialsAuthorization",
    jsii_struct_bases=[],
    name_mapping={"parameter": "parameter", "scheme": "scheme"},
)
class ApiManagementBackendCredentialsAuthorization:
    def __init__(
        self,
        *,
        parameter: typing.Optional[builtins.str] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#parameter ApiManagementBackend#parameter}.
        :param scheme: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#scheme ApiManagementBackend#scheme}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75e7ff760ba7370dcb3ca2d73e772ab9d532ee4c6e28bd98c7ca3b33468ad01)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument scheme", value=scheme, expected_type=type_hints["scheme"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameter is not None:
            self._values["parameter"] = parameter
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def parameter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#parameter ApiManagementBackend#parameter}.'''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheme(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#scheme ApiManagementBackend#scheme}.'''
        result = self._values.get("scheme")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementBackendCredentialsAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementBackendCredentialsAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendCredentialsAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80344c2a0b86064e6059bcdb53ad104d87e04be8de4b19fdd4ba3d7a13903b8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetScheme")
    def reset_scheme(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheme", []))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="schemeInput")
    def scheme_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemeInput"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameter"))

    @parameter.setter
    def parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc5a417c3f3c40d64bb842f6dce3c81aedfdf2eaec7136e7dd43ee06087bdb61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scheme")
    def scheme(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scheme"))

    @scheme.setter
    def scheme(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3738df068848bd41bb44dfed7f716d4407be11ae8886913f59e3d626b4d5852f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scheme", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementBackendCredentialsAuthorization]:
        return typing.cast(typing.Optional[ApiManagementBackendCredentialsAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementBackendCredentialsAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6752b23bceaaae6812bf79a027374a398e1e07ed2f31c348b6ad5bf720ce661b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementBackendCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92794822ed0fdcdcb3aa41cb8b2ab23a5dc06d98288fa0aa1005112685654d39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthorization")
    def put_authorization(
        self,
        *,
        parameter: typing.Optional[builtins.str] = None,
        scheme: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#parameter ApiManagementBackend#parameter}.
        :param scheme: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#scheme ApiManagementBackend#scheme}.
        '''
        value = ApiManagementBackendCredentialsAuthorization(
            parameter=parameter, scheme=scheme
        )

        return typing.cast(None, jsii.invoke(self, "putAuthorization", [value]))

    @jsii.member(jsii_name="resetAuthorization")
    def reset_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorization", []))

    @jsii.member(jsii_name="resetCertificate")
    def reset_certificate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCertificate", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="authorization")
    def authorization(
        self,
    ) -> ApiManagementBackendCredentialsAuthorizationOutputReference:
        return typing.cast(ApiManagementBackendCredentialsAuthorizationOutputReference, jsii.get(self, "authorization"))

    @builtins.property
    @jsii.member(jsii_name="authorizationInput")
    def authorization_input(
        self,
    ) -> typing.Optional[ApiManagementBackendCredentialsAuthorization]:
        return typing.cast(typing.Optional[ApiManagementBackendCredentialsAuthorization], jsii.get(self, "authorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="certificateInput")
    def certificate_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "certificateInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7684c386de20d108b39ab3ef1b7759881742b4e052cdae16cddc2563f6ff9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "header"))

    @header.setter
    def header(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e80b2f45f19a796df7c5be7dd6ce82b4eeff276783d2568ed3727c0f95f9a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "query"))

    @query.setter
    def query(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0737ae43d6ec942a3e4c74420a5041a460f339ba9614ff7f8e30851daba3ee1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementBackendCredentials]:
        return typing.cast(typing.Optional[ApiManagementBackendCredentials], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementBackendCredentials],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6c133880d612548ee2cc1d88f810fba0e39ae22c9ae909661a63971d041b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendProxy",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "username": "username", "password": "password"},
)
class ApiManagementBackendProxy:
    def __init__(
        self,
        *,
        url: builtins.str,
        username: builtins.str,
        password: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#url ApiManagementBackend#url}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#username ApiManagementBackend#username}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#password ApiManagementBackend#password}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8178c48da5ceba7b66d08549e73e6bf1c007ba456887ebb98660ff48dfc3b3)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
            "username": username,
        }
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#url ApiManagementBackend#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#username ApiManagementBackend#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#password ApiManagementBackend#password}.'''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementBackendProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementBackendProxyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendProxyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22f41fd336ae0a79084e00637297b679d7c9b72a3940d35e330f3e8d744e43cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597bd2832d45b1fe43ff67b66cf78caabfd7e89c9fc1f8266a134d83945e12a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643d564310209f1bc47bd075f277f12a3f52f1c5cc808f783a7252f936898956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39d8b65d1dd4bd97237e6e083bca7aafede90632c224f9cb1920985a24f5cae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementBackendProxy]:
        return typing.cast(typing.Optional[ApiManagementBackendProxy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementBackendProxy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4647434f94442303c2cb1b86e745bf5a5bb599ba4d31fb362dd7d15d92c0fbaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendServiceFabricCluster",
    jsii_struct_bases=[],
    name_mapping={
        "management_endpoints": "managementEndpoints",
        "max_partition_resolution_retries": "maxPartitionResolutionRetries",
        "client_certificate_id": "clientCertificateId",
        "client_certificate_thumbprint": "clientCertificateThumbprint",
        "server_certificate_thumbprints": "serverCertificateThumbprints",
        "server_x509_name": "serverX509Name",
    },
)
class ApiManagementBackendServiceFabricCluster:
    def __init__(
        self,
        *,
        management_endpoints: typing.Sequence[builtins.str],
        max_partition_resolution_retries: jsii.Number,
        client_certificate_id: typing.Optional[builtins.str] = None,
        client_certificate_thumbprint: typing.Optional[builtins.str] = None,
        server_certificate_thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_x509_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementBackendServiceFabricClusterServerX509Name", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param management_endpoints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#management_endpoints ApiManagementBackend#management_endpoints}.
        :param max_partition_resolution_retries: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#max_partition_resolution_retries ApiManagementBackend#max_partition_resolution_retries}.
        :param client_certificate_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#client_certificate_id ApiManagementBackend#client_certificate_id}.
        :param client_certificate_thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#client_certificate_thumbprint ApiManagementBackend#client_certificate_thumbprint}.
        :param server_certificate_thumbprints: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#server_certificate_thumbprints ApiManagementBackend#server_certificate_thumbprints}.
        :param server_x509_name: server_x509_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#server_x509_name ApiManagementBackend#server_x509_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94cdfc08c8e2d10a9a03e51bb13e0ac5771fc419cf2f05994727512f84692502)
            check_type(argname="argument management_endpoints", value=management_endpoints, expected_type=type_hints["management_endpoints"])
            check_type(argname="argument max_partition_resolution_retries", value=max_partition_resolution_retries, expected_type=type_hints["max_partition_resolution_retries"])
            check_type(argname="argument client_certificate_id", value=client_certificate_id, expected_type=type_hints["client_certificate_id"])
            check_type(argname="argument client_certificate_thumbprint", value=client_certificate_thumbprint, expected_type=type_hints["client_certificate_thumbprint"])
            check_type(argname="argument server_certificate_thumbprints", value=server_certificate_thumbprints, expected_type=type_hints["server_certificate_thumbprints"])
            check_type(argname="argument server_x509_name", value=server_x509_name, expected_type=type_hints["server_x509_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "management_endpoints": management_endpoints,
            "max_partition_resolution_retries": max_partition_resolution_retries,
        }
        if client_certificate_id is not None:
            self._values["client_certificate_id"] = client_certificate_id
        if client_certificate_thumbprint is not None:
            self._values["client_certificate_thumbprint"] = client_certificate_thumbprint
        if server_certificate_thumbprints is not None:
            self._values["server_certificate_thumbprints"] = server_certificate_thumbprints
        if server_x509_name is not None:
            self._values["server_x509_name"] = server_x509_name

    @builtins.property
    def management_endpoints(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#management_endpoints ApiManagementBackend#management_endpoints}.'''
        result = self._values.get("management_endpoints")
        assert result is not None, "Required property 'management_endpoints' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def max_partition_resolution_retries(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#max_partition_resolution_retries ApiManagementBackend#max_partition_resolution_retries}.'''
        result = self._values.get("max_partition_resolution_retries")
        assert result is not None, "Required property 'max_partition_resolution_retries' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def client_certificate_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#client_certificate_id ApiManagementBackend#client_certificate_id}.'''
        result = self._values.get("client_certificate_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_thumbprint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#client_certificate_thumbprint ApiManagementBackend#client_certificate_thumbprint}.'''
        result = self._values.get("client_certificate_thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_certificate_thumbprints(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#server_certificate_thumbprints ApiManagementBackend#server_certificate_thumbprints}.'''
        result = self._values.get("server_certificate_thumbprints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def server_x509_name(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementBackendServiceFabricClusterServerX509Name"]]]:
        '''server_x509_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#server_x509_name ApiManagementBackend#server_x509_name}
        '''
        result = self._values.get("server_x509_name")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementBackendServiceFabricClusterServerX509Name"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementBackendServiceFabricCluster(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementBackendServiceFabricClusterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendServiceFabricClusterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59b9c53bdcfa8befd7c0a6e0fbb0e9eecbb92677b12b170709afe6b5ed6e1fe1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putServerX509Name")
    def put_server_x509_name(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementBackendServiceFabricClusterServerX509Name", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7434f9d4cab4eef0dfc2e0f4aeada769f1f76ad2b6b7934b81b29280f1565cca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServerX509Name", [value]))

    @jsii.member(jsii_name="resetClientCertificateId")
    def reset_client_certificate_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateId", []))

    @jsii.member(jsii_name="resetClientCertificateThumbprint")
    def reset_client_certificate_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateThumbprint", []))

    @jsii.member(jsii_name="resetServerCertificateThumbprints")
    def reset_server_certificate_thumbprints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerCertificateThumbprints", []))

    @jsii.member(jsii_name="resetServerX509Name")
    def reset_server_x509_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServerX509Name", []))

    @builtins.property
    @jsii.member(jsii_name="serverX509Name")
    def server_x509_name(
        self,
    ) -> "ApiManagementBackendServiceFabricClusterServerX509NameList":
        return typing.cast("ApiManagementBackendServiceFabricClusterServerX509NameList", jsii.get(self, "serverX509Name"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateIdInput")
    def client_certificate_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateThumbprintInput")
    def client_certificate_thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateThumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="managementEndpointsInput")
    def management_endpoints_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "managementEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxPartitionResolutionRetriesInput")
    def max_partition_resolution_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxPartitionResolutionRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="serverCertificateThumbprintsInput")
    def server_certificate_thumbprints_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "serverCertificateThumbprintsInput"))

    @builtins.property
    @jsii.member(jsii_name="serverX509NameInput")
    def server_x509_name_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementBackendServiceFabricClusterServerX509Name"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementBackendServiceFabricClusterServerX509Name"]]], jsii.get(self, "serverX509NameInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateId")
    def client_certificate_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateId"))

    @client_certificate_id.setter
    def client_certificate_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76070792f87d91366f8b3b5930cd5effc2e2fa6c16822623b4bad3919c4a0225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateThumbprint")
    def client_certificate_thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateThumbprint"))

    @client_certificate_thumbprint.setter
    def client_certificate_thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4f4edc2d108faba1f815216a3ba5438c7acda7d2ad108511f1fd93aa972314a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateThumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managementEndpoints")
    def management_endpoints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "managementEndpoints"))

    @management_endpoints.setter
    def management_endpoints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6edbd07fc52585bc5877b5679d007da1000bafc59fce640a04773fb9605c4a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managementEndpoints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxPartitionResolutionRetries")
    def max_partition_resolution_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxPartitionResolutionRetries"))

    @max_partition_resolution_retries.setter
    def max_partition_resolution_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f0b21ee5e9822ce482df3e1afa6f8073b11994dd981c58d9a5d2f17004665a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxPartitionResolutionRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serverCertificateThumbprints")
    def server_certificate_thumbprints(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "serverCertificateThumbprints"))

    @server_certificate_thumbprints.setter
    def server_certificate_thumbprints(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d644f466ae36aa362152bb1e4a433c6fd4e523b38833da75d752f287d9f2806a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCertificateThumbprints", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementBackendServiceFabricCluster]:
        return typing.cast(typing.Optional[ApiManagementBackendServiceFabricCluster], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementBackendServiceFabricCluster],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249ac09a196b2c79d53e6512fdb4bae38a8656b94bf4258f47982cb187ba78d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendServiceFabricClusterServerX509Name",
    jsii_struct_bases=[],
    name_mapping={
        "issuer_certificate_thumbprint": "issuerCertificateThumbprint",
        "name": "name",
    },
)
class ApiManagementBackendServiceFabricClusterServerX509Name:
    def __init__(
        self,
        *,
        issuer_certificate_thumbprint: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param issuer_certificate_thumbprint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#issuer_certificate_thumbprint ApiManagementBackend#issuer_certificate_thumbprint}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#name ApiManagementBackend#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48d9f8b8b3bdfafc9508a13b56033fe128c21b124c00a66ac107f1d3e48fbad)
            check_type(argname="argument issuer_certificate_thumbprint", value=issuer_certificate_thumbprint, expected_type=type_hints["issuer_certificate_thumbprint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "issuer_certificate_thumbprint": issuer_certificate_thumbprint,
            "name": name,
        }

    @builtins.property
    def issuer_certificate_thumbprint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#issuer_certificate_thumbprint ApiManagementBackend#issuer_certificate_thumbprint}.'''
        result = self._values.get("issuer_certificate_thumbprint")
        assert result is not None, "Required property 'issuer_certificate_thumbprint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#name ApiManagementBackend#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementBackendServiceFabricClusterServerX509Name(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementBackendServiceFabricClusterServerX509NameList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendServiceFabricClusterServerX509NameList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa2b43080c98ce5fcf794b9720e2718981022a27fb12d21f173fbe3c44799ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementBackendServiceFabricClusterServerX509NameOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95c28e8ffc9b1f599ee7097c354b997198139a84b5da4aac256e6ac042dd24c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementBackendServiceFabricClusterServerX509NameOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c009c14dc36c74e1ae51130a2335a213bc60e25f5e0a9b207935cd97de7af9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c0b9a1737986e94b993cc169723d7ef33658a4e78f7f3c2c5645fd0aa1ea820)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa01f155e887d72acd08faf087797f607185795187aa3170c584e7d78ea790c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementBackendServiceFabricClusterServerX509Name]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementBackendServiceFabricClusterServerX509Name]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementBackendServiceFabricClusterServerX509Name]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd4c4cce5469778e0929ea69b0c3961ba90653278144ffcd740d6852d0ebac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementBackendServiceFabricClusterServerX509NameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendServiceFabricClusterServerX509NameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df4a073d185a042fd961b47ce2829bb15da0d2f9e54dcade25a11140800fbdae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="issuerCertificateThumbprintInput")
    def issuer_certificate_thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerCertificateThumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerCertificateThumbprint")
    def issuer_certificate_thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerCertificateThumbprint"))

    @issuer_certificate_thumbprint.setter
    def issuer_certificate_thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866de75438f2da7bc5b3beb01e5ddd5ef6e62606d3cc162a9918635901f570e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerCertificateThumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc2c78d76f45a913454134b06c26b4e39c97a66f02c881c077fdba402a14d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementBackendServiceFabricClusterServerX509Name]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementBackendServiceFabricClusterServerX509Name]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementBackendServiceFabricClusterServerX509Name]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c348ae89ff9489c86a29d4ff9daeed82e0a259ebb8cab63c7148efa3a785fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApiManagementBackendTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#create ApiManagementBackend#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#delete ApiManagementBackend#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#read ApiManagementBackend#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#update ApiManagementBackend#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4b48bd817d4c0004f6151138206f24563b96cd6183a7a8254380fdb921b81a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#create ApiManagementBackend#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#delete ApiManagementBackend#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#read ApiManagementBackend#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#update ApiManagementBackend#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementBackendTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementBackendTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f71035e3770373a6b9f7c15180cfcd662265cbcaf632de6eb706c21308a2ecd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b9ac0b9fb44e013de6e4b17ef636b0ac49e2e02e02dad75ff5495bbef3d101e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94dab792fe46305e5de590feeb2ad3c78a1e8fc1b2cc8b77eb80a420b2cc4656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500a9dc6d8704d9859777adb129c7e35630463502ac2a24102bcbe83cdd48c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6fdb7b00f700335811fd96bd536def67649ce5c0e437da38133ab52085b3fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementBackendTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementBackendTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementBackendTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c192a5820b293c1a0fe62f501eebdfebda7c271688fb729e9b8ba56b2514b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendTls",
    jsii_struct_bases=[],
    name_mapping={
        "validate_certificate_chain": "validateCertificateChain",
        "validate_certificate_name": "validateCertificateName",
    },
)
class ApiManagementBackendTls:
    def __init__(
        self,
        *,
        validate_certificate_chain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        validate_certificate_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param validate_certificate_chain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#validate_certificate_chain ApiManagementBackend#validate_certificate_chain}.
        :param validate_certificate_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#validate_certificate_name ApiManagementBackend#validate_certificate_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836c0f1250db6a943d929c0e2266ec5953d68a5a627b73d7eff3cab47b403e3e)
            check_type(argname="argument validate_certificate_chain", value=validate_certificate_chain, expected_type=type_hints["validate_certificate_chain"])
            check_type(argname="argument validate_certificate_name", value=validate_certificate_name, expected_type=type_hints["validate_certificate_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if validate_certificate_chain is not None:
            self._values["validate_certificate_chain"] = validate_certificate_chain
        if validate_certificate_name is not None:
            self._values["validate_certificate_name"] = validate_certificate_name

    @builtins.property
    def validate_certificate_chain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#validate_certificate_chain ApiManagementBackend#validate_certificate_chain}.'''
        result = self._values.get("validate_certificate_chain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def validate_certificate_name(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_backend#validate_certificate_name ApiManagementBackend#validate_certificate_name}.'''
        result = self._values.get("validate_certificate_name")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementBackendTls(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementBackendTlsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementBackend.ApiManagementBackendTlsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee5fb93cd5d57c845a549970bf3090b25fc6e0cbdcd099c5620469b01f79f3cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetValidateCertificateChain")
    def reset_validate_certificate_chain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateCertificateChain", []))

    @jsii.member(jsii_name="resetValidateCertificateName")
    def reset_validate_certificate_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateCertificateName", []))

    @builtins.property
    @jsii.member(jsii_name="validateCertificateChainInput")
    def validate_certificate_chain_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateCertificateChainInput"))

    @builtins.property
    @jsii.member(jsii_name="validateCertificateNameInput")
    def validate_certificate_name_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateCertificateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="validateCertificateChain")
    def validate_certificate_chain(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validateCertificateChain"))

    @validate_certificate_chain.setter
    def validate_certificate_chain(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faebf4a661e1af6b6c44e6881664ef206d959f039b04e4c9a05cc95c85d53e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateCertificateChain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateCertificateName")
    def validate_certificate_name(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validateCertificateName"))

    @validate_certificate_name.setter
    def validate_certificate_name(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44930579e33745ea9bb4064c71b8cad96216353be42e366ae6d1ac8528fcdbf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateCertificateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementBackendTls]:
        return typing.cast(typing.Optional[ApiManagementBackendTls], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ApiManagementBackendTls]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0009b580dc7b39f07f5e1f73304e955be63c22e61930057ceaf395bcc15b0e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiManagementBackend",
    "ApiManagementBackendConfig",
    "ApiManagementBackendCredentials",
    "ApiManagementBackendCredentialsAuthorization",
    "ApiManagementBackendCredentialsAuthorizationOutputReference",
    "ApiManagementBackendCredentialsOutputReference",
    "ApiManagementBackendProxy",
    "ApiManagementBackendProxyOutputReference",
    "ApiManagementBackendServiceFabricCluster",
    "ApiManagementBackendServiceFabricClusterOutputReference",
    "ApiManagementBackendServiceFabricClusterServerX509Name",
    "ApiManagementBackendServiceFabricClusterServerX509NameList",
    "ApiManagementBackendServiceFabricClusterServerX509NameOutputReference",
    "ApiManagementBackendTimeouts",
    "ApiManagementBackendTimeoutsOutputReference",
    "ApiManagementBackendTls",
    "ApiManagementBackendTlsOutputReference",
]

publication.publish()

def _typecheckingstub__8169f87e71bac7fdd3f8627e246c53dac466a60f045f72d47e40adb849f67d40(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_management_name: builtins.str,
    name: builtins.str,
    protocol: builtins.str,
    resource_group_name: builtins.str,
    url: builtins.str,
    credentials: typing.Optional[typing.Union[ApiManagementBackendCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[ApiManagementBackendProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_id: typing.Optional[builtins.str] = None,
    service_fabric_cluster: typing.Optional[typing.Union[ApiManagementBackendServiceFabricCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementBackendTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
    tls: typing.Optional[typing.Union[ApiManagementBackendTls, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c131f8c75fe8a88529e75fde18a2d915607f975ba5e493cd858e8d786b0f4176(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3c2e8c03a7e1123f9915b2e0ec9e9decb3bff3e1d21ba5aba64041df137bcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981d6e09bc46150c197d9d0c755e3b950412b45ba57efe4f09d413ca07ef23d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08835ff30450941ca05dd63627e191816b790df8d5cb9b80bc11f1ed270fc5e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86fa765d54b9049695272e5640ed2511b265a8b7bb1e31e28bf77a35e16e9a5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832025441d909e0c08b911bf7cd161cbf4aaf5eb2b3cebb4190ea9b22e033689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbdc3073b462275255d238fb00c072895747cd85aa7cc3754bab29b25541112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7420813b9f531008d6afab74e9cec39ca4c159d7ab1312a4959ca7ad71c80f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe480441bedc060337bb9c73f6fe9ecc3288a96ff942ec71eece1413cfcf498f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e097f305d707ea1baf48ab3b869fa9abb9558f1e72fb8c0576a645c3948054(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0980c82cd9314550102cbca14e5ca7db7c539efb2a8d3dd09c5da41fb9ccc58c(
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
    protocol: builtins.str,
    resource_group_name: builtins.str,
    url: builtins.str,
    credentials: typing.Optional[typing.Union[ApiManagementBackendCredentials, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[ApiManagementBackendProxy, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_id: typing.Optional[builtins.str] = None,
    service_fabric_cluster: typing.Optional[typing.Union[ApiManagementBackendServiceFabricCluster, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementBackendTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
    tls: typing.Optional[typing.Union[ApiManagementBackendTls, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167b5946b1cb3e8da3e19ce22545c852e41e0aa986590d941f3d1cd86b96b3c2(
    *,
    authorization: typing.Optional[typing.Union[ApiManagementBackendCredentialsAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    certificate: typing.Optional[typing.Sequence[builtins.str]] = None,
    header: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75e7ff760ba7370dcb3ca2d73e772ab9d532ee4c6e28bd98c7ca3b33468ad01(
    *,
    parameter: typing.Optional[builtins.str] = None,
    scheme: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80344c2a0b86064e6059bcdb53ad104d87e04be8de4b19fdd4ba3d7a13903b8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5a417c3f3c40d64bb842f6dce3c81aedfdf2eaec7136e7dd43ee06087bdb61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3738df068848bd41bb44dfed7f716d4407be11ae8886913f59e3d626b4d5852f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6752b23bceaaae6812bf79a027374a398e1e07ed2f31c348b6ad5bf720ce661b(
    value: typing.Optional[ApiManagementBackendCredentialsAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92794822ed0fdcdcb3aa41cb8b2ab23a5dc06d98288fa0aa1005112685654d39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7684c386de20d108b39ab3ef1b7759881742b4e052cdae16cddc2563f6ff9cb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e80b2f45f19a796df7c5be7dd6ce82b4eeff276783d2568ed3727c0f95f9a64(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0737ae43d6ec942a3e4c74420a5041a460f339ba9614ff7f8e30851daba3ee1f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6c133880d612548ee2cc1d88f810fba0e39ae22c9ae909661a63971d041b1d(
    value: typing.Optional[ApiManagementBackendCredentials],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8178c48da5ceba7b66d08549e73e6bf1c007ba456887ebb98660ff48dfc3b3(
    *,
    url: builtins.str,
    username: builtins.str,
    password: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f41fd336ae0a79084e00637297b679d7c9b72a3940d35e330f3e8d744e43cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597bd2832d45b1fe43ff67b66cf78caabfd7e89c9fc1f8266a134d83945e12a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643d564310209f1bc47bd075f277f12a3f52f1c5cc808f783a7252f936898956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39d8b65d1dd4bd97237e6e083bca7aafede90632c224f9cb1920985a24f5cae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4647434f94442303c2cb1b86e745bf5a5bb599ba4d31fb362dd7d15d92c0fbaa(
    value: typing.Optional[ApiManagementBackendProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94cdfc08c8e2d10a9a03e51bb13e0ac5771fc419cf2f05994727512f84692502(
    *,
    management_endpoints: typing.Sequence[builtins.str],
    max_partition_resolution_retries: jsii.Number,
    client_certificate_id: typing.Optional[builtins.str] = None,
    client_certificate_thumbprint: typing.Optional[builtins.str] = None,
    server_certificate_thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    server_x509_name: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementBackendServiceFabricClusterServerX509Name, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b9c53bdcfa8befd7c0a6e0fbb0e9eecbb92677b12b170709afe6b5ed6e1fe1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7434f9d4cab4eef0dfc2e0f4aeada769f1f76ad2b6b7934b81b29280f1565cca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementBackendServiceFabricClusterServerX509Name, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76070792f87d91366f8b3b5930cd5effc2e2fa6c16822623b4bad3919c4a0225(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f4edc2d108faba1f815216a3ba5438c7acda7d2ad108511f1fd93aa972314a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6edbd07fc52585bc5877b5679d007da1000bafc59fce640a04773fb9605c4a25(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0b21ee5e9822ce482df3e1afa6f8073b11994dd981c58d9a5d2f17004665a6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d644f466ae36aa362152bb1e4a433c6fd4e523b38833da75d752f287d9f2806a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249ac09a196b2c79d53e6512fdb4bae38a8656b94bf4258f47982cb187ba78d0(
    value: typing.Optional[ApiManagementBackendServiceFabricCluster],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48d9f8b8b3bdfafc9508a13b56033fe128c21b124c00a66ac107f1d3e48fbad(
    *,
    issuer_certificate_thumbprint: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa2b43080c98ce5fcf794b9720e2718981022a27fb12d21f173fbe3c44799ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95c28e8ffc9b1f599ee7097c354b997198139a84b5da4aac256e6ac042dd24c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c009c14dc36c74e1ae51130a2335a213bc60e25f5e0a9b207935cd97de7af9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0b9a1737986e94b993cc169723d7ef33658a4e78f7f3c2c5645fd0aa1ea820(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa01f155e887d72acd08faf087797f607185795187aa3170c584e7d78ea790c9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd4c4cce5469778e0929ea69b0c3961ba90653278144ffcd740d6852d0ebac3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementBackendServiceFabricClusterServerX509Name]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4a073d185a042fd961b47ce2829bb15da0d2f9e54dcade25a11140800fbdae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866de75438f2da7bc5b3beb01e5ddd5ef6e62606d3cc162a9918635901f570e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc2c78d76f45a913454134b06c26b4e39c97a66f02c881c077fdba402a14d10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c348ae89ff9489c86a29d4ff9daeed82e0a259ebb8cab63c7148efa3a785fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementBackendServiceFabricClusterServerX509Name]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4b48bd817d4c0004f6151138206f24563b96cd6183a7a8254380fdb921b81a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f71035e3770373a6b9f7c15180cfcd662265cbcaf632de6eb706c21308a2ecd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9ac0b9fb44e013de6e4b17ef636b0ac49e2e02e02dad75ff5495bbef3d101e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94dab792fe46305e5de590feeb2ad3c78a1e8fc1b2cc8b77eb80a420b2cc4656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500a9dc6d8704d9859777adb129c7e35630463502ac2a24102bcbe83cdd48c68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6fdb7b00f700335811fd96bd536def67649ce5c0e437da38133ab52085b3fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c192a5820b293c1a0fe62f501eebdfebda7c271688fb729e9b8ba56b2514b19(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementBackendTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836c0f1250db6a943d929c0e2266ec5953d68a5a627b73d7eff3cab47b403e3e(
    *,
    validate_certificate_chain: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    validate_certificate_name: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5fb93cd5d57c845a549970bf3090b25fc6e0cbdcd099c5620469b01f79f3cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faebf4a661e1af6b6c44e6881664ef206d959f039b04e4c9a05cc95c85d53e4c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44930579e33745ea9bb4064c71b8cad96216353be42e366ae6d1ac8528fcdbf9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0009b580dc7b39f07f5e1f73304e955be63c22e61930057ceaf395bcc15b0e73(
    value: typing.Optional[ApiManagementBackendTls],
) -> None:
    """Type checking stubs"""
    pass

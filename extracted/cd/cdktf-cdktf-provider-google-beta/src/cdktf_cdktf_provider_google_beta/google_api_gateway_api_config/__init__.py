r'''
# `google_api_gateway_api_config`

Refer to the Terraform Registry for docs: [`google_api_gateway_api_config`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config).
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


class GoogleApiGatewayApiConfigA(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigA",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config google_api_gateway_api_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api: builtins.str,
        api_config_id: typing.Optional[builtins.str] = None,
        api_config_id_prefix: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        gateway_config: typing.Optional[typing.Union["GoogleApiGatewayApiConfigGatewayConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_services: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigGrpcServices", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        managed_service_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigManagedServiceConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        openapi_documents: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigOpenapiDocuments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApiGatewayApiConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config google_api_gateway_api_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api: The API to attach the config to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api GoogleApiGatewayApiConfigA#api}
        :param api_config_id: Identifier to assign to the API Config. Must be unique within scope of the parent resource(api). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api_config_id GoogleApiGatewayApiConfigA#api_config_id}
        :param api_config_id_prefix: Creates a unique name beginning with the specified prefix. If this and api_config_id are unspecified, a random value is chosen for the name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api_config_id_prefix GoogleApiGatewayApiConfigA#api_config_id_prefix}
        :param display_name: A user-visible name for the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#display_name GoogleApiGatewayApiConfigA#display_name}
        :param gateway_config: gateway_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#gateway_config GoogleApiGatewayApiConfigA#gateway_config}
        :param grpc_services: grpc_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#grpc_services GoogleApiGatewayApiConfigA#grpc_services}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#id GoogleApiGatewayApiConfigA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#labels GoogleApiGatewayApiConfigA#labels}
        :param managed_service_configs: managed_service_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#managed_service_configs GoogleApiGatewayApiConfigA#managed_service_configs}
        :param openapi_documents: openapi_documents block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#openapi_documents GoogleApiGatewayApiConfigA#openapi_documents}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#project GoogleApiGatewayApiConfigA#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#timeouts GoogleApiGatewayApiConfigA#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4e5bc490c9ccec8697eb1c3e5463dd0c20b78cd6dcb7780516c5aee5d54fb7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleApiGatewayApiConfigAConfig(
            api=api,
            api_config_id=api_config_id,
            api_config_id_prefix=api_config_id_prefix,
            display_name=display_name,
            gateway_config=gateway_config,
            grpc_services=grpc_services,
            id=id,
            labels=labels,
            managed_service_configs=managed_service_configs,
            openapi_documents=openapi_documents,
            project=project,
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
        '''Generates CDKTF code for importing a GoogleApiGatewayApiConfigA resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleApiGatewayApiConfigA to import.
        :param import_from_id: The id of the existing GoogleApiGatewayApiConfigA that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleApiGatewayApiConfigA to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101dd6fbd235b0e6a089677e25ad57ddf42bb47be7eb54ee25aa463127c0dcb8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putGatewayConfig")
    def put_gateway_config(
        self,
        *,
        backend_config: typing.Union["GoogleApiGatewayApiConfigGatewayConfigBackendConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param backend_config: backend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#backend_config GoogleApiGatewayApiConfigA#backend_config}
        '''
        value = GoogleApiGatewayApiConfigGatewayConfig(backend_config=backend_config)

        return typing.cast(None, jsii.invoke(self, "putGatewayConfig", [value]))

    @jsii.member(jsii_name="putGrpcServices")
    def put_grpc_services(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigGrpcServices", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee2c6b57f432189c29a6d6e3de874dd46f3e8c7215f8c887fd8719a5d0a665ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGrpcServices", [value]))

    @jsii.member(jsii_name="putManagedServiceConfigs")
    def put_managed_service_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigManagedServiceConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1910edf6d3d0e3201b3a62170724aaf970affbb2d8deed4a5ba440f676278f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putManagedServiceConfigs", [value]))

    @jsii.member(jsii_name="putOpenapiDocuments")
    def put_openapi_documents(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigOpenapiDocuments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0541a126ad8f33db94a6f0143d1ecfd50f2805fade069095c46fe76f30c6f4e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOpenapiDocuments", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#create GoogleApiGatewayApiConfigA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#delete GoogleApiGatewayApiConfigA#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#update GoogleApiGatewayApiConfigA#update}.
        '''
        value = GoogleApiGatewayApiConfigTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiConfigId")
    def reset_api_config_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiConfigId", []))

    @jsii.member(jsii_name="resetApiConfigIdPrefix")
    def reset_api_config_id_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiConfigIdPrefix", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGatewayConfig")
    def reset_gateway_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayConfig", []))

    @jsii.member(jsii_name="resetGrpcServices")
    def reset_grpc_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpcServices", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetManagedServiceConfigs")
    def reset_managed_service_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedServiceConfigs", []))

    @jsii.member(jsii_name="resetOpenapiDocuments")
    def reset_openapi_documents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenapiDocuments", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="gatewayConfig")
    def gateway_config(self) -> "GoogleApiGatewayApiConfigGatewayConfigOutputReference":
        return typing.cast("GoogleApiGatewayApiConfigGatewayConfigOutputReference", jsii.get(self, "gatewayConfig"))

    @builtins.property
    @jsii.member(jsii_name="grpcServices")
    def grpc_services(self) -> "GoogleApiGatewayApiConfigGrpcServicesList":
        return typing.cast("GoogleApiGatewayApiConfigGrpcServicesList", jsii.get(self, "grpcServices"))

    @builtins.property
    @jsii.member(jsii_name="managedServiceConfigs")
    def managed_service_configs(
        self,
    ) -> "GoogleApiGatewayApiConfigManagedServiceConfigsList":
        return typing.cast("GoogleApiGatewayApiConfigManagedServiceConfigsList", jsii.get(self, "managedServiceConfigs"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="openapiDocuments")
    def openapi_documents(self) -> "GoogleApiGatewayApiConfigOpenapiDocumentsList":
        return typing.cast("GoogleApiGatewayApiConfigOpenapiDocumentsList", jsii.get(self, "openapiDocuments"))

    @builtins.property
    @jsii.member(jsii_name="serviceConfigId")
    def service_config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceConfigId"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleApiGatewayApiConfigTimeoutsOutputReference":
        return typing.cast("GoogleApiGatewayApiConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiConfigIdInput")
    def api_config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiConfigIdInput"))

    @builtins.property
    @jsii.member(jsii_name="apiConfigIdPrefixInput")
    def api_config_id_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiConfigIdPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="apiInput")
    def api_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayConfigInput")
    def gateway_config_input(
        self,
    ) -> typing.Optional["GoogleApiGatewayApiConfigGatewayConfig"]:
        return typing.cast(typing.Optional["GoogleApiGatewayApiConfigGatewayConfig"], jsii.get(self, "gatewayConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcServicesInput")
    def grpc_services_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigGrpcServices"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigGrpcServices"]]], jsii.get(self, "grpcServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="managedServiceConfigsInput")
    def managed_service_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigManagedServiceConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigManagedServiceConfigs"]]], jsii.get(self, "managedServiceConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="openapiDocumentsInput")
    def openapi_documents_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigOpenapiDocuments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigOpenapiDocuments"]]], jsii.get(self, "openapiDocumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApiGatewayApiConfigTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleApiGatewayApiConfigTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="api")
    def api(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "api"))

    @api.setter
    def api(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f88860a33bf1a75ed52e10f09219c3ee4ccbd79eda5a1bf9d20878ccf4abba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "api", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiConfigId")
    def api_config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiConfigId"))

    @api_config_id.setter
    def api_config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0e8c6c071cb96393a7c3e40163d4a0ae95743edd0b4d223a4bbbcd172f5083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiConfigId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiConfigIdPrefix")
    def api_config_id_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiConfigIdPrefix"))

    @api_config_id_prefix.setter
    def api_config_id_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59a91953fee47640ce8d5680c92b9cde2bb53fc96e721393ea520ef933e8e4e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiConfigIdPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddc9c5f646029f70f67e0512a007e20fb6ce2160ea5d4b084b293744899fbb5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d524f7ec8cadcc39f024f7183c8aacaf1639948676874c0ddad8809449fb201d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3139636dbf5e27fe66915ecf89e555658892543b191704aa42b81571dd2ab20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f854c3ac2a457a0c75ce3b20d0357b3ec60ca79ca348569362e08cc34e2fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigAConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api": "api",
        "api_config_id": "apiConfigId",
        "api_config_id_prefix": "apiConfigIdPrefix",
        "display_name": "displayName",
        "gateway_config": "gatewayConfig",
        "grpc_services": "grpcServices",
        "id": "id",
        "labels": "labels",
        "managed_service_configs": "managedServiceConfigs",
        "openapi_documents": "openapiDocuments",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GoogleApiGatewayApiConfigAConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api: builtins.str,
        api_config_id: typing.Optional[builtins.str] = None,
        api_config_id_prefix: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        gateway_config: typing.Optional[typing.Union["GoogleApiGatewayApiConfigGatewayConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        grpc_services: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigGrpcServices", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        managed_service_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigManagedServiceConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        openapi_documents: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigOpenapiDocuments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleApiGatewayApiConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api: The API to attach the config to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api GoogleApiGatewayApiConfigA#api}
        :param api_config_id: Identifier to assign to the API Config. Must be unique within scope of the parent resource(api). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api_config_id GoogleApiGatewayApiConfigA#api_config_id}
        :param api_config_id_prefix: Creates a unique name beginning with the specified prefix. If this and api_config_id are unspecified, a random value is chosen for the name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api_config_id_prefix GoogleApiGatewayApiConfigA#api_config_id_prefix}
        :param display_name: A user-visible name for the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#display_name GoogleApiGatewayApiConfigA#display_name}
        :param gateway_config: gateway_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#gateway_config GoogleApiGatewayApiConfigA#gateway_config}
        :param grpc_services: grpc_services block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#grpc_services GoogleApiGatewayApiConfigA#grpc_services}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#id GoogleApiGatewayApiConfigA#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Resource labels to represent user-provided metadata. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#labels GoogleApiGatewayApiConfigA#labels}
        :param managed_service_configs: managed_service_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#managed_service_configs GoogleApiGatewayApiConfigA#managed_service_configs}
        :param openapi_documents: openapi_documents block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#openapi_documents GoogleApiGatewayApiConfigA#openapi_documents}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#project GoogleApiGatewayApiConfigA#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#timeouts GoogleApiGatewayApiConfigA#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(gateway_config, dict):
            gateway_config = GoogleApiGatewayApiConfigGatewayConfig(**gateway_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleApiGatewayApiConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d046a4370b8fc82401f492aac75a7eb179f05fdfaf567122a629185f5c8f5f5a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument api_config_id", value=api_config_id, expected_type=type_hints["api_config_id"])
            check_type(argname="argument api_config_id_prefix", value=api_config_id_prefix, expected_type=type_hints["api_config_id_prefix"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gateway_config", value=gateway_config, expected_type=type_hints["gateway_config"])
            check_type(argname="argument grpc_services", value=grpc_services, expected_type=type_hints["grpc_services"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument managed_service_configs", value=managed_service_configs, expected_type=type_hints["managed_service_configs"])
            check_type(argname="argument openapi_documents", value=openapi_documents, expected_type=type_hints["openapi_documents"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
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
        if api_config_id is not None:
            self._values["api_config_id"] = api_config_id
        if api_config_id_prefix is not None:
            self._values["api_config_id_prefix"] = api_config_id_prefix
        if display_name is not None:
            self._values["display_name"] = display_name
        if gateway_config is not None:
            self._values["gateway_config"] = gateway_config
        if grpc_services is not None:
            self._values["grpc_services"] = grpc_services
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if managed_service_configs is not None:
            self._values["managed_service_configs"] = managed_service_configs
        if openapi_documents is not None:
            self._values["openapi_documents"] = openapi_documents
        if project is not None:
            self._values["project"] = project
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
    def api(self) -> builtins.str:
        '''The API to attach the config to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api GoogleApiGatewayApiConfigA#api}
        '''
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_config_id(self) -> typing.Optional[builtins.str]:
        '''Identifier to assign to the API Config. Must be unique within scope of the parent resource(api).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api_config_id GoogleApiGatewayApiConfigA#api_config_id}
        '''
        result = self._values.get("api_config_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_config_id_prefix(self) -> typing.Optional[builtins.str]:
        '''Creates a unique name beginning with the specified prefix.

        If this and api_config_id are unspecified, a random value is chosen for the name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#api_config_id_prefix GoogleApiGatewayApiConfigA#api_config_id_prefix}
        '''
        result = self._values.get("api_config_id_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''A user-visible name for the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#display_name GoogleApiGatewayApiConfigA#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_config(
        self,
    ) -> typing.Optional["GoogleApiGatewayApiConfigGatewayConfig"]:
        '''gateway_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#gateway_config GoogleApiGatewayApiConfigA#gateway_config}
        '''
        result = self._values.get("gateway_config")
        return typing.cast(typing.Optional["GoogleApiGatewayApiConfigGatewayConfig"], result)

    @builtins.property
    def grpc_services(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigGrpcServices"]]]:
        '''grpc_services block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#grpc_services GoogleApiGatewayApiConfigA#grpc_services}
        '''
        result = self._values.get("grpc_services")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigGrpcServices"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#id GoogleApiGatewayApiConfigA#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Resource labels to represent user-provided metadata.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#labels GoogleApiGatewayApiConfigA#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def managed_service_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigManagedServiceConfigs"]]]:
        '''managed_service_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#managed_service_configs GoogleApiGatewayApiConfigA#managed_service_configs}
        '''
        result = self._values.get("managed_service_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigManagedServiceConfigs"]]], result)

    @builtins.property
    def openapi_documents(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigOpenapiDocuments"]]]:
        '''openapi_documents block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#openapi_documents GoogleApiGatewayApiConfigA#openapi_documents}
        '''
        result = self._values.get("openapi_documents")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigOpenapiDocuments"]]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#project GoogleApiGatewayApiConfigA#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleApiGatewayApiConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#timeouts GoogleApiGatewayApiConfigA#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleApiGatewayApiConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigAConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGatewayConfig",
    jsii_struct_bases=[],
    name_mapping={"backend_config": "backendConfig"},
)
class GoogleApiGatewayApiConfigGatewayConfig:
    def __init__(
        self,
        *,
        backend_config: typing.Union["GoogleApiGatewayApiConfigGatewayConfigBackendConfig", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param backend_config: backend_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#backend_config GoogleApiGatewayApiConfigA#backend_config}
        '''
        if isinstance(backend_config, dict):
            backend_config = GoogleApiGatewayApiConfigGatewayConfigBackendConfig(**backend_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57df74adfc4804a56dc5355a91b56b059b0f309063c61f7df341427e48b98f28)
            check_type(argname="argument backend_config", value=backend_config, expected_type=type_hints["backend_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "backend_config": backend_config,
        }

    @builtins.property
    def backend_config(self) -> "GoogleApiGatewayApiConfigGatewayConfigBackendConfig":
        '''backend_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#backend_config GoogleApiGatewayApiConfigA#backend_config}
        '''
        result = self._values.get("backend_config")
        assert result is not None, "Required property 'backend_config' is missing"
        return typing.cast("GoogleApiGatewayApiConfigGatewayConfigBackendConfig", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigGatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGatewayConfigBackendConfig",
    jsii_struct_bases=[],
    name_mapping={"google_service_account": "googleServiceAccount"},
)
class GoogleApiGatewayApiConfigGatewayConfigBackendConfig:
    def __init__(self, *, google_service_account: builtins.str) -> None:
        '''
        :param google_service_account: Google Cloud IAM service account used to sign OIDC tokens for backends that have authentication configured (https://cloud.google.com/service-infrastructure/docs/service-management/reference/rest/v1/services.configs#backend). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#google_service_account GoogleApiGatewayApiConfigA#google_service_account}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18098f35687191bd5855aca437f3a0cce79724f1154ad0aeeb11c74ae4437378)
            check_type(argname="argument google_service_account", value=google_service_account, expected_type=type_hints["google_service_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "google_service_account": google_service_account,
        }

    @builtins.property
    def google_service_account(self) -> builtins.str:
        '''Google Cloud IAM service account used to sign OIDC tokens for backends that have authentication configured (https://cloud.google.com/service-infrastructure/docs/service-management/reference/rest/v1/services.configs#backend).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#google_service_account GoogleApiGatewayApiConfigA#google_service_account}
        '''
        result = self._values.get("google_service_account")
        assert result is not None, "Required property 'google_service_account' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigGatewayConfigBackendConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApiGatewayApiConfigGatewayConfigBackendConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGatewayConfigBackendConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d68172032bf372a8f5e2b962c22af38fece1d313d5904b3af706b850103a6b2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccountInput")
    def google_service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "googleServiceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="googleServiceAccount")
    def google_service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "googleServiceAccount"))

    @google_service_account.setter
    def google_service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6a9853fcdceab47ec41a9e338514b8e39eff2ae071304040e1666bb0610fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "googleServiceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApiGatewayApiConfigGatewayConfigBackendConfig]:
        return typing.cast(typing.Optional[GoogleApiGatewayApiConfigGatewayConfigBackendConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApiGatewayApiConfigGatewayConfigBackendConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c119b64e50f20a3658ca301961f8e4ea6dc94553d3313fab3eea4a88d82d4a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApiGatewayApiConfigGatewayConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGatewayConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f713f2042219625bf5b2a4f8b2a830dfdcaa2d51031abaf5cde05aa941f7b800)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBackendConfig")
    def put_backend_config(self, *, google_service_account: builtins.str) -> None:
        '''
        :param google_service_account: Google Cloud IAM service account used to sign OIDC tokens for backends that have authentication configured (https://cloud.google.com/service-infrastructure/docs/service-management/reference/rest/v1/services.configs#backend). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#google_service_account GoogleApiGatewayApiConfigA#google_service_account}
        '''
        value = GoogleApiGatewayApiConfigGatewayConfigBackendConfig(
            google_service_account=google_service_account
        )

        return typing.cast(None, jsii.invoke(self, "putBackendConfig", [value]))

    @builtins.property
    @jsii.member(jsii_name="backendConfig")
    def backend_config(
        self,
    ) -> GoogleApiGatewayApiConfigGatewayConfigBackendConfigOutputReference:
        return typing.cast(GoogleApiGatewayApiConfigGatewayConfigBackendConfigOutputReference, jsii.get(self, "backendConfig"))

    @builtins.property
    @jsii.member(jsii_name="backendConfigInput")
    def backend_config_input(
        self,
    ) -> typing.Optional[GoogleApiGatewayApiConfigGatewayConfigBackendConfig]:
        return typing.cast(typing.Optional[GoogleApiGatewayApiConfigGatewayConfigBackendConfig], jsii.get(self, "backendConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleApiGatewayApiConfigGatewayConfig]:
        return typing.cast(typing.Optional[GoogleApiGatewayApiConfigGatewayConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApiGatewayApiConfigGatewayConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5713cefc5eb49945e9fbfae09faa032570567184b4a5df87d690b88725196713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGrpcServices",
    jsii_struct_bases=[],
    name_mapping={"file_descriptor_set": "fileDescriptorSet", "source": "source"},
)
class GoogleApiGatewayApiConfigGrpcServices:
    def __init__(
        self,
        *,
        file_descriptor_set: typing.Union["GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet", typing.Dict[builtins.str, typing.Any]],
        source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigGrpcServicesSource", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param file_descriptor_set: file_descriptor_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#file_descriptor_set GoogleApiGatewayApiConfigA#file_descriptor_set}
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#source GoogleApiGatewayApiConfigA#source}
        '''
        if isinstance(file_descriptor_set, dict):
            file_descriptor_set = GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet(**file_descriptor_set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1e68cf30b71bfd44524b01c2972adbab8cd53c99bdab355119a5109cd17cd7)
            check_type(argname="argument file_descriptor_set", value=file_descriptor_set, expected_type=type_hints["file_descriptor_set"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file_descriptor_set": file_descriptor_set,
        }
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def file_descriptor_set(
        self,
    ) -> "GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet":
        '''file_descriptor_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#file_descriptor_set GoogleApiGatewayApiConfigA#file_descriptor_set}
        '''
        result = self._values.get("file_descriptor_set")
        assert result is not None, "Required property 'file_descriptor_set' is missing"
        return typing.cast("GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet", result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigGrpcServicesSource"]]]:
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#source GoogleApiGatewayApiConfigA#source}
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigGrpcServicesSource"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigGrpcServices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet",
    jsii_struct_bases=[],
    name_mapping={"contents": "contents", "path": "path"},
)
class GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet:
    def __init__(self, *, contents: builtins.str, path: builtins.str) -> None:
        '''
        :param contents: Base64 encoded content of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        :param path: The file path (full or relative path). This is typically the path of the file when it is uploaded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8ae88cb9e486ba5c888dc70cad0e209421ea5a183b187b0c6765bde43a4f9e9)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contents": contents,
            "path": path,
        }

    @builtins.property
    def contents(self) -> builtins.str:
        '''Base64 encoded content of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        '''
        result = self._values.get("contents")
        assert result is not None, "Required property 'contents' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The file path (full or relative path). This is typically the path of the file when it is uploaded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbb6469122ac9bed3233d3867eca767a103fdacab99d96a0f807356f8c731d1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentsInput")
    def contents_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9157a63e5e42e34b63164a3972821f1f70d2fce7179021ac7fb68079fd6984f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54704d2811417bfbdb8c94d13e61e1cf706a45e8a59b1b2febc1f733b4efcdaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet]:
        return typing.cast(typing.Optional[GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d9f0fa8455027c1b57123d510e899f4bdfb48eab05af89df59a398560832e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApiGatewayApiConfigGrpcServicesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGrpcServicesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22d0bba5b2fffdb74e0cf5e2ec5929f65f24b4aa7b15675b4f5bd810a7ea13a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApiGatewayApiConfigGrpcServicesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fe824c440a0192989f69d55dc1bb6812153f6170c05132b1aefcc54751828e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApiGatewayApiConfigGrpcServicesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a22e9551d3b97d4c2c3a317a22de3013cecaa16f5d74d39f1e61f7a9da8cd1b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ce8377b38923109b8f3ddcbc1828e2165740b41876856fca2188c055f2383d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7a58ae7320ea01344f852bfe6341120b1e0607c1cb09c4213f16abfce0e52e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigGrpcServices]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigGrpcServices]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigGrpcServices]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9bc6e3a2fa46b5dd53671960757b461a3b142d427b67d588d95b21796f1b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApiGatewayApiConfigGrpcServicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGrpcServicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d88ae9aac16c5ec49e093feb1cf4c222c6f3afe07d3328a5b461eb84c709e695)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putFileDescriptorSet")
    def put_file_descriptor_set(
        self,
        *,
        contents: builtins.str,
        path: builtins.str,
    ) -> None:
        '''
        :param contents: Base64 encoded content of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        :param path: The file path (full or relative path). This is typically the path of the file when it is uploaded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        value = GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet(
            contents=contents, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putFileDescriptorSet", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleApiGatewayApiConfigGrpcServicesSource", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efe3e4db381614c1b6091ee1a8e149a9b992b73f75f3f8ab1c91954aac976809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @builtins.property
    @jsii.member(jsii_name="fileDescriptorSet")
    def file_descriptor_set(
        self,
    ) -> GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSetOutputReference:
        return typing.cast(GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSetOutputReference, jsii.get(self, "fileDescriptorSet"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "GoogleApiGatewayApiConfigGrpcServicesSourceList":
        return typing.cast("GoogleApiGatewayApiConfigGrpcServicesSourceList", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="fileDescriptorSetInput")
    def file_descriptor_set_input(
        self,
    ) -> typing.Optional[GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet]:
        return typing.cast(typing.Optional[GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet], jsii.get(self, "fileDescriptorSetInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigGrpcServicesSource"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleApiGatewayApiConfigGrpcServicesSource"]]], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigGrpcServices]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigGrpcServices]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigGrpcServices]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5b553b136befe6daad2ea7a91c0d6f52351e453ebc0a4a3a2c9e475f76fadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGrpcServicesSource",
    jsii_struct_bases=[],
    name_mapping={"contents": "contents", "path": "path"},
)
class GoogleApiGatewayApiConfigGrpcServicesSource:
    def __init__(self, *, contents: builtins.str, path: builtins.str) -> None:
        '''
        :param contents: Base64 encoded content of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        :param path: The file path (full or relative path). This is typically the path of the file when it is uploaded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c16aef09cc95077f27808e8cc0c6ca014f5d2b6a0620d0dabb2d1d6c486557)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contents": contents,
            "path": path,
        }

    @builtins.property
    def contents(self) -> builtins.str:
        '''Base64 encoded content of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        '''
        result = self._values.get("contents")
        assert result is not None, "Required property 'contents' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The file path (full or relative path). This is typically the path of the file when it is uploaded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigGrpcServicesSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApiGatewayApiConfigGrpcServicesSourceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGrpcServicesSourceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e1f87b43d11b1648a675c4fbed3949b9243cc06a48f1463e95b40f75aec946)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApiGatewayApiConfigGrpcServicesSourceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a0c8822563522999761f5f0b974f35e5ea9751a7289314f336fad08e012bc0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApiGatewayApiConfigGrpcServicesSourceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d005dd0e100cdfafe34b1da751c048cee58f8220ffe1f68918247ce48d0027e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3d765f7584ed8feb61c304613d2c35b86748849fa7cf4a736c44de6d032f379)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88a0fdafc7ccca77bb3bb0863823e6e6b98022b825aa613d53bf794f86236fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigGrpcServicesSource]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigGrpcServicesSource]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigGrpcServicesSource]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ca8842ba3979ee5edc3ee2273b7c2568ca7f23be10ae159d1169ec83abe532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApiGatewayApiConfigGrpcServicesSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigGrpcServicesSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d3fafd7c11636701e693a1f4bc353cc5c72333a24f4a302fd30b961fff32851)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentsInput")
    def contents_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cec57817e731e8cf3809137fdd1aee73898824ae37467aeca1ccef84784ec26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab7bc06dd0d589c1dfbca10e9f24c37d2352015cd74e7a3be15c89463945e39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigGrpcServicesSource]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigGrpcServicesSource]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigGrpcServicesSource]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572bad46bfe184d9974171b49c3a4df3845b588f70b74c3524ebb67d330e1e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigManagedServiceConfigs",
    jsii_struct_bases=[],
    name_mapping={"contents": "contents", "path": "path"},
)
class GoogleApiGatewayApiConfigManagedServiceConfigs:
    def __init__(self, *, contents: builtins.str, path: builtins.str) -> None:
        '''
        :param contents: Base64 encoded content of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        :param path: The file path (full or relative path). This is typically the path of the file when it is uploaded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e56ae100f531e0f7510712d5f43c0bcdc94e43c91658fb0fbfb966efb8d687e)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contents": contents,
            "path": path,
        }

    @builtins.property
    def contents(self) -> builtins.str:
        '''Base64 encoded content of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        '''
        result = self._values.get("contents")
        assert result is not None, "Required property 'contents' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The file path (full or relative path). This is typically the path of the file when it is uploaded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigManagedServiceConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApiGatewayApiConfigManagedServiceConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigManagedServiceConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7255c6747895ea06590b4e08aefcc154e7be80957c5389634a984a76ab6d829b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApiGatewayApiConfigManagedServiceConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b21a5b5944a51758234d45a016c20cc523108670138e65b1ea53ca86ef2696)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApiGatewayApiConfigManagedServiceConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8252883194b0f0718f751c9c0dadec94c905f245f349485ad21002a50cd6ba82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe17eb01bf7fd0435261d49062504ad993c8b89b08bc0ad533ef4a738a19c3a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05d7178f90e0074543295cdaa06ae65d79ecdefe132a8956d141bf63aef68fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigManagedServiceConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigManagedServiceConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigManagedServiceConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e687243a42a3666965f310789dfb863a4d4746b5a79f80768ef3bee88dfd49be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApiGatewayApiConfigManagedServiceConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigManagedServiceConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebba2d89d337ebc14cee129a8b0e55995fdc142c77f36b37425d350dc1a27db0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contentsInput")
    def contents_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208107bb86db7b144e8714cf6d3b160298f243ca6b355099dd799237b8731bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742549b1e4fb1ecd719962a66fcb82c9c7bb4a2c8b717b83fa2d9f36c3da4655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigManagedServiceConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigManagedServiceConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigManagedServiceConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854af8271b4184c0cb08fca25b236895c6d04fdb149b2f6ac6733387eddf1ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigOpenapiDocuments",
    jsii_struct_bases=[],
    name_mapping={"document": "document"},
)
class GoogleApiGatewayApiConfigOpenapiDocuments:
    def __init__(
        self,
        *,
        document: typing.Union["GoogleApiGatewayApiConfigOpenapiDocumentsDocument", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param document: document block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#document GoogleApiGatewayApiConfigA#document}
        '''
        if isinstance(document, dict):
            document = GoogleApiGatewayApiConfigOpenapiDocumentsDocument(**document)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a210877c433930436f2690ef80042d9bcc47ab99f601ddef1b6fc6636e33a48c)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "document": document,
        }

    @builtins.property
    def document(self) -> "GoogleApiGatewayApiConfigOpenapiDocumentsDocument":
        '''document block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#document GoogleApiGatewayApiConfigA#document}
        '''
        result = self._values.get("document")
        assert result is not None, "Required property 'document' is missing"
        return typing.cast("GoogleApiGatewayApiConfigOpenapiDocumentsDocument", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigOpenapiDocuments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigOpenapiDocumentsDocument",
    jsii_struct_bases=[],
    name_mapping={"contents": "contents", "path": "path"},
)
class GoogleApiGatewayApiConfigOpenapiDocumentsDocument:
    def __init__(self, *, contents: builtins.str, path: builtins.str) -> None:
        '''
        :param contents: Base64 encoded content of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        :param path: The file path (full or relative path). This is typically the path of the file when it is uploaded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9086b2aaf878a119d3f9100c0753b351bbf21c886224aaf5cfb69cd63e4fd6b4)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "contents": contents,
            "path": path,
        }

    @builtins.property
    def contents(self) -> builtins.str:
        '''Base64 encoded content of the file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        '''
        result = self._values.get("contents")
        assert result is not None, "Required property 'contents' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''The file path (full or relative path). This is typically the path of the file when it is uploaded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigOpenapiDocumentsDocument(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApiGatewayApiConfigOpenapiDocumentsDocumentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigOpenapiDocumentsDocumentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bcc8d733e906ceff0d9a8a98d624ce4a3395850e9b87a970e8203914a78944a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="contentsInput")
    def contents_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentsInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba1f1e10a37af79e7535e85acd365a3f32096c873fc8a7d3102422189e18143)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767015ec56f0af5631005c46b24f2327933358d3429021ef6c20c1a0f19c1bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleApiGatewayApiConfigOpenapiDocumentsDocument]:
        return typing.cast(typing.Optional[GoogleApiGatewayApiConfigOpenapiDocumentsDocument], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleApiGatewayApiConfigOpenapiDocumentsDocument],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822648f01eccecd8bd3f41d8ef6275068c0b8c881a5cd5eeb101a78f448d1ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApiGatewayApiConfigOpenapiDocumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigOpenapiDocumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef14fc3e0ef409a221019ea54600bb0fffe5d519dce403cd4d73449c4a31a0cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleApiGatewayApiConfigOpenapiDocumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2099cb191a9bb4b8f4783683c9e9c90fbf219fe9322542d946fd0dab8bf9666a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleApiGatewayApiConfigOpenapiDocumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67002b5b4bcd084806f54d5cce34da844dda098cada3a84c8315ff28815e3c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b0ebc627408622148aa5e0928cbf4387d2102b8b47a41eb53463522a79fabee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5c46ae4bd94ed9134db91167cc1a9f8076fb6b2c1dd0037c47e378d9f040d1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigOpenapiDocuments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigOpenapiDocuments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigOpenapiDocuments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c7b2d61a7deabdbbd0a4870a9e97575c1e9035332d493617cb4943a8eb9621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleApiGatewayApiConfigOpenapiDocumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigOpenapiDocumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__463b916efa714a472e9842549b87dde84159a9eb794a90a2aef0a01af3632523)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDocument")
    def put_document(self, *, contents: builtins.str, path: builtins.str) -> None:
        '''
        :param contents: Base64 encoded content of the file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#contents GoogleApiGatewayApiConfigA#contents}
        :param path: The file path (full or relative path). This is typically the path of the file when it is uploaded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#path GoogleApiGatewayApiConfigA#path}
        '''
        value = GoogleApiGatewayApiConfigOpenapiDocumentsDocument(
            contents=contents, path=path
        )

        return typing.cast(None, jsii.invoke(self, "putDocument", [value]))

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(
        self,
    ) -> GoogleApiGatewayApiConfigOpenapiDocumentsDocumentOutputReference:
        return typing.cast(GoogleApiGatewayApiConfigOpenapiDocumentsDocumentOutputReference, jsii.get(self, "document"))

    @builtins.property
    @jsii.member(jsii_name="documentInput")
    def document_input(
        self,
    ) -> typing.Optional[GoogleApiGatewayApiConfigOpenapiDocumentsDocument]:
        return typing.cast(typing.Optional[GoogleApiGatewayApiConfigOpenapiDocumentsDocument], jsii.get(self, "documentInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigOpenapiDocuments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigOpenapiDocuments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigOpenapiDocuments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad3dcda7f76af3f54be57e4d439289235bd76cfeb3cde789bd3a5a7dfdaef89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleApiGatewayApiConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#create GoogleApiGatewayApiConfigA#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#delete GoogleApiGatewayApiConfigA#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#update GoogleApiGatewayApiConfigA#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b030316fc72b4519e16b8aebc33cc712c32743235f8d82bad5b3b0c5418c8023)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#create GoogleApiGatewayApiConfigA#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#delete GoogleApiGatewayApiConfigA#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_api_gateway_api_config#update GoogleApiGatewayApiConfigA#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleApiGatewayApiConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleApiGatewayApiConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleApiGatewayApiConfig.GoogleApiGatewayApiConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e252d624be005f9483da41c8c8786f444ee0702183929d0b0e921f8b963faa24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd0c4776254078ca3177b20d62958952d24447829dfdbba37f1a947aae90a461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6445be1001173c5a9e9ede6bd24e452709c5333d21c4fdf6a0a31234fbb3a9fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e18cf67b1a1a7d214a2e35a9b0810aed588b3e4b1577eee7cab54661eb6584c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f4668b160794b4fae3ec0778a48589f775fdd0afa1b078a6685a6861bddbc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleApiGatewayApiConfigA",
    "GoogleApiGatewayApiConfigAConfig",
    "GoogleApiGatewayApiConfigGatewayConfig",
    "GoogleApiGatewayApiConfigGatewayConfigBackendConfig",
    "GoogleApiGatewayApiConfigGatewayConfigBackendConfigOutputReference",
    "GoogleApiGatewayApiConfigGatewayConfigOutputReference",
    "GoogleApiGatewayApiConfigGrpcServices",
    "GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet",
    "GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSetOutputReference",
    "GoogleApiGatewayApiConfigGrpcServicesList",
    "GoogleApiGatewayApiConfigGrpcServicesOutputReference",
    "GoogleApiGatewayApiConfigGrpcServicesSource",
    "GoogleApiGatewayApiConfigGrpcServicesSourceList",
    "GoogleApiGatewayApiConfigGrpcServicesSourceOutputReference",
    "GoogleApiGatewayApiConfigManagedServiceConfigs",
    "GoogleApiGatewayApiConfigManagedServiceConfigsList",
    "GoogleApiGatewayApiConfigManagedServiceConfigsOutputReference",
    "GoogleApiGatewayApiConfigOpenapiDocuments",
    "GoogleApiGatewayApiConfigOpenapiDocumentsDocument",
    "GoogleApiGatewayApiConfigOpenapiDocumentsDocumentOutputReference",
    "GoogleApiGatewayApiConfigOpenapiDocumentsList",
    "GoogleApiGatewayApiConfigOpenapiDocumentsOutputReference",
    "GoogleApiGatewayApiConfigTimeouts",
    "GoogleApiGatewayApiConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0f4e5bc490c9ccec8697eb1c3e5463dd0c20b78cd6dcb7780516c5aee5d54fb7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api: builtins.str,
    api_config_id: typing.Optional[builtins.str] = None,
    api_config_id_prefix: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    gateway_config: typing.Optional[typing.Union[GoogleApiGatewayApiConfigGatewayConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_services: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigGrpcServices, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    managed_service_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigManagedServiceConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    openapi_documents: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigOpenapiDocuments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApiGatewayApiConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__101dd6fbd235b0e6a089677e25ad57ddf42bb47be7eb54ee25aa463127c0dcb8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee2c6b57f432189c29a6d6e3de874dd46f3e8c7215f8c887fd8719a5d0a665ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigGrpcServices, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1910edf6d3d0e3201b3a62170724aaf970affbb2d8deed4a5ba440f676278f1e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigManagedServiceConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0541a126ad8f33db94a6f0143d1ecfd50f2805fade069095c46fe76f30c6f4e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigOpenapiDocuments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f88860a33bf1a75ed52e10f09219c3ee4ccbd79eda5a1bf9d20878ccf4abba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0e8c6c071cb96393a7c3e40163d4a0ae95743edd0b4d223a4bbbcd172f5083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59a91953fee47640ce8d5680c92b9cde2bb53fc96e721393ea520ef933e8e4e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddc9c5f646029f70f67e0512a007e20fb6ce2160ea5d4b084b293744899fbb5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d524f7ec8cadcc39f024f7183c8aacaf1639948676874c0ddad8809449fb201d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3139636dbf5e27fe66915ecf89e555658892543b191704aa42b81571dd2ab20(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f854c3ac2a457a0c75ce3b20d0357b3ec60ca79ca348569362e08cc34e2fd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d046a4370b8fc82401f492aac75a7eb179f05fdfaf567122a629185f5c8f5f5a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api: builtins.str,
    api_config_id: typing.Optional[builtins.str] = None,
    api_config_id_prefix: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    gateway_config: typing.Optional[typing.Union[GoogleApiGatewayApiConfigGatewayConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    grpc_services: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigGrpcServices, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    managed_service_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigManagedServiceConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    openapi_documents: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigOpenapiDocuments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleApiGatewayApiConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57df74adfc4804a56dc5355a91b56b059b0f309063c61f7df341427e48b98f28(
    *,
    backend_config: typing.Union[GoogleApiGatewayApiConfigGatewayConfigBackendConfig, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18098f35687191bd5855aca437f3a0cce79724f1154ad0aeeb11c74ae4437378(
    *,
    google_service_account: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68172032bf372a8f5e2b962c22af38fece1d313d5904b3af706b850103a6b2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6a9853fcdceab47ec41a9e338514b8e39eff2ae071304040e1666bb0610fc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c119b64e50f20a3658ca301961f8e4ea6dc94553d3313fab3eea4a88d82d4a3a(
    value: typing.Optional[GoogleApiGatewayApiConfigGatewayConfigBackendConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f713f2042219625bf5b2a4f8b2a830dfdcaa2d51031abaf5cde05aa941f7b800(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5713cefc5eb49945e9fbfae09faa032570567184b4a5df87d690b88725196713(
    value: typing.Optional[GoogleApiGatewayApiConfigGatewayConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1e68cf30b71bfd44524b01c2972adbab8cd53c99bdab355119a5109cd17cd7(
    *,
    file_descriptor_set: typing.Union[GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet, typing.Dict[builtins.str, typing.Any]],
    source: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigGrpcServicesSource, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ae88cb9e486ba5c888dc70cad0e209421ea5a183b187b0c6765bde43a4f9e9(
    *,
    contents: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbb6469122ac9bed3233d3867eca767a103fdacab99d96a0f807356f8c731d1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9157a63e5e42e34b63164a3972821f1f70d2fce7179021ac7fb68079fd6984f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54704d2811417bfbdb8c94d13e61e1cf706a45e8a59b1b2febc1f733b4efcdaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d9f0fa8455027c1b57123d510e899f4bdfb48eab05af89df59a398560832e00(
    value: typing.Optional[GoogleApiGatewayApiConfigGrpcServicesFileDescriptorSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d0bba5b2fffdb74e0cf5e2ec5929f65f24b4aa7b15675b4f5bd810a7ea13a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fe824c440a0192989f69d55dc1bb6812153f6170c05132b1aefcc54751828e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a22e9551d3b97d4c2c3a317a22de3013cecaa16f5d74d39f1e61f7a9da8cd1b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce8377b38923109b8f3ddcbc1828e2165740b41876856fca2188c055f2383d0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a58ae7320ea01344f852bfe6341120b1e0607c1cb09c4213f16abfce0e52e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9bc6e3a2fa46b5dd53671960757b461a3b142d427b67d588d95b21796f1b8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigGrpcServices]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88ae9aac16c5ec49e093feb1cf4c222c6f3afe07d3328a5b461eb84c709e695(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efe3e4db381614c1b6091ee1a8e149a9b992b73f75f3f8ab1c91954aac976809(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleApiGatewayApiConfigGrpcServicesSource, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5b553b136befe6daad2ea7a91c0d6f52351e453ebc0a4a3a2c9e475f76fadb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigGrpcServices]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c16aef09cc95077f27808e8cc0c6ca014f5d2b6a0620d0dabb2d1d6c486557(
    *,
    contents: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e1f87b43d11b1648a675c4fbed3949b9243cc06a48f1463e95b40f75aec946(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a0c8822563522999761f5f0b974f35e5ea9751a7289314f336fad08e012bc0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d005dd0e100cdfafe34b1da751c048cee58f8220ffe1f68918247ce48d0027e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d765f7584ed8feb61c304613d2c35b86748849fa7cf4a736c44de6d032f379(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a0fdafc7ccca77bb3bb0863823e6e6b98022b825aa613d53bf794f86236fb2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ca8842ba3979ee5edc3ee2273b7c2568ca7f23be10ae159d1169ec83abe532(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigGrpcServicesSource]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d3fafd7c11636701e693a1f4bc353cc5c72333a24f4a302fd30b961fff32851(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cec57817e731e8cf3809137fdd1aee73898824ae37467aeca1ccef84784ec26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab7bc06dd0d589c1dfbca10e9f24c37d2352015cd74e7a3be15c89463945e39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572bad46bfe184d9974171b49c3a4df3845b588f70b74c3524ebb67d330e1e48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigGrpcServicesSource]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e56ae100f531e0f7510712d5f43c0bcdc94e43c91658fb0fbfb966efb8d687e(
    *,
    contents: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7255c6747895ea06590b4e08aefcc154e7be80957c5389634a984a76ab6d829b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b21a5b5944a51758234d45a016c20cc523108670138e65b1ea53ca86ef2696(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8252883194b0f0718f751c9c0dadec94c905f245f349485ad21002a50cd6ba82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe17eb01bf7fd0435261d49062504ad993c8b89b08bc0ad533ef4a738a19c3a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d7178f90e0074543295cdaa06ae65d79ecdefe132a8956d141bf63aef68fa7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e687243a42a3666965f310789dfb863a4d4746b5a79f80768ef3bee88dfd49be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigManagedServiceConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebba2d89d337ebc14cee129a8b0e55995fdc142c77f36b37425d350dc1a27db0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208107bb86db7b144e8714cf6d3b160298f243ca6b355099dd799237b8731bba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742549b1e4fb1ecd719962a66fcb82c9c7bb4a2c8b717b83fa2d9f36c3da4655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854af8271b4184c0cb08fca25b236895c6d04fdb149b2f6ac6733387eddf1ce7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigManagedServiceConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a210877c433930436f2690ef80042d9bcc47ab99f601ddef1b6fc6636e33a48c(
    *,
    document: typing.Union[GoogleApiGatewayApiConfigOpenapiDocumentsDocument, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9086b2aaf878a119d3f9100c0753b351bbf21c886224aaf5cfb69cd63e4fd6b4(
    *,
    contents: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcc8d733e906ceff0d9a8a98d624ce4a3395850e9b87a970e8203914a78944a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba1f1e10a37af79e7535e85acd365a3f32096c873fc8a7d3102422189e18143(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767015ec56f0af5631005c46b24f2327933358d3429021ef6c20c1a0f19c1bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822648f01eccecd8bd3f41d8ef6275068c0b8c881a5cd5eeb101a78f448d1ff8(
    value: typing.Optional[GoogleApiGatewayApiConfigOpenapiDocumentsDocument],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef14fc3e0ef409a221019ea54600bb0fffe5d519dce403cd4d73449c4a31a0cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2099cb191a9bb4b8f4783683c9e9c90fbf219fe9322542d946fd0dab8bf9666a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67002b5b4bcd084806f54d5cce34da844dda098cada3a84c8315ff28815e3c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0ebc627408622148aa5e0928cbf4387d2102b8b47a41eb53463522a79fabee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c46ae4bd94ed9134db91167cc1a9f8076fb6b2c1dd0037c47e378d9f040d1a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c7b2d61a7deabdbbd0a4870a9e97575c1e9035332d493617cb4943a8eb9621(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleApiGatewayApiConfigOpenapiDocuments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463b916efa714a472e9842549b87dde84159a9eb794a90a2aef0a01af3632523(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad3dcda7f76af3f54be57e4d439289235bd76cfeb3cde789bd3a5a7dfdaef89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigOpenapiDocuments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b030316fc72b4519e16b8aebc33cc712c32743235f8d82bad5b3b0c5418c8023(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e252d624be005f9483da41c8c8786f444ee0702183929d0b0e921f8b963faa24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0c4776254078ca3177b20d62958952d24447829dfdbba37f1a947aae90a461(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6445be1001173c5a9e9ede6bd24e452709c5333d21c4fdf6a0a31234fbb3a9fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e18cf67b1a1a7d214a2e35a9b0810aed588b3e4b1577eee7cab54661eb6584c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f4668b160794b4fae3ec0778a48589f775fdd0afa1b078a6685a6861bddbc7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleApiGatewayApiConfigTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `azurerm_api_management_api_diagnostic`

Refer to the Terraform Registry for docs: [`azurerm_api_management_api_diagnostic`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic).
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


class ApiManagementApiDiagnostic(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnostic",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic azurerm_api_management_api_diagnostic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_management_logger_id: builtins.str,
        api_management_name: builtins.str,
        api_name: builtins.str,
        identifier: builtins.str,
        resource_group_name: builtins.str,
        always_log_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_request: typing.Optional[typing.Union["ApiManagementApiDiagnosticBackendRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        backend_response: typing.Optional[typing.Union["ApiManagementApiDiagnosticBackendResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_request: typing.Optional[typing.Union["ApiManagementApiDiagnosticFrontendRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_response: typing.Optional[typing.Union["ApiManagementApiDiagnosticFrontendResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        http_correlation_protocol: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_client_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operation_name_format: typing.Optional[builtins.str] = None,
        sampling_percentage: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementApiDiagnosticTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        verbosity: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic azurerm_api_management_api_diagnostic} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_management_logger_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_management_logger_id ApiManagementApiDiagnostic#api_management_logger_id}.
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_management_name ApiManagementApiDiagnostic#api_management_name}.
        :param api_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_name ApiManagementApiDiagnostic#api_name}.
        :param identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#identifier ApiManagementApiDiagnostic#identifier}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#resource_group_name ApiManagementApiDiagnostic#resource_group_name}.
        :param always_log_errors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#always_log_errors ApiManagementApiDiagnostic#always_log_errors}.
        :param backend_request: backend_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#backend_request ApiManagementApiDiagnostic#backend_request}
        :param backend_response: backend_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#backend_response ApiManagementApiDiagnostic#backend_response}
        :param frontend_request: frontend_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#frontend_request ApiManagementApiDiagnostic#frontend_request}
        :param frontend_response: frontend_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#frontend_response ApiManagementApiDiagnostic#frontend_response}
        :param http_correlation_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#http_correlation_protocol ApiManagementApiDiagnostic#http_correlation_protocol}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#id ApiManagementApiDiagnostic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_client_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#log_client_ip ApiManagementApiDiagnostic#log_client_ip}.
        :param operation_name_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#operation_name_format ApiManagementApiDiagnostic#operation_name_format}.
        :param sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#sampling_percentage ApiManagementApiDiagnostic#sampling_percentage}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#timeouts ApiManagementApiDiagnostic#timeouts}
        :param verbosity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#verbosity ApiManagementApiDiagnostic#verbosity}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db95a2bb470a01d6be674f3513f2ee9b6e5796b041dd63f667024a745ae9e2ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiManagementApiDiagnosticConfig(
            api_management_logger_id=api_management_logger_id,
            api_management_name=api_management_name,
            api_name=api_name,
            identifier=identifier,
            resource_group_name=resource_group_name,
            always_log_errors=always_log_errors,
            backend_request=backend_request,
            backend_response=backend_response,
            frontend_request=frontend_request,
            frontend_response=frontend_response,
            http_correlation_protocol=http_correlation_protocol,
            id=id,
            log_client_ip=log_client_ip,
            operation_name_format=operation_name_format,
            sampling_percentage=sampling_percentage,
            timeouts=timeouts,
            verbosity=verbosity,
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
        '''Generates CDKTF code for importing a ApiManagementApiDiagnostic resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiManagementApiDiagnostic to import.
        :param import_from_id: The id of the existing ApiManagementApiDiagnostic that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiManagementApiDiagnostic to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e8faac6b6a7e073240dd69adb1b25de23a8388a6374f527d78bfe8a868c6ed6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBackendRequest")
    def put_backend_request(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementApiDiagnosticBackendRequestDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.
        '''
        value = ApiManagementApiDiagnosticBackendRequest(
            body_bytes=body_bytes,
            data_masking=data_masking,
            headers_to_log=headers_to_log,
        )

        return typing.cast(None, jsii.invoke(self, "putBackendRequest", [value]))

    @jsii.member(jsii_name="putBackendResponse")
    def put_backend_response(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementApiDiagnosticBackendResponseDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.
        '''
        value = ApiManagementApiDiagnosticBackendResponse(
            body_bytes=body_bytes,
            data_masking=data_masking,
            headers_to_log=headers_to_log,
        )

        return typing.cast(None, jsii.invoke(self, "putBackendResponse", [value]))

    @jsii.member(jsii_name="putFrontendRequest")
    def put_frontend_request(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementApiDiagnosticFrontendRequestDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.
        '''
        value = ApiManagementApiDiagnosticFrontendRequest(
            body_bytes=body_bytes,
            data_masking=data_masking,
            headers_to_log=headers_to_log,
        )

        return typing.cast(None, jsii.invoke(self, "putFrontendRequest", [value]))

    @jsii.member(jsii_name="putFrontendResponse")
    def put_frontend_response(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementApiDiagnosticFrontendResponseDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.
        '''
        value = ApiManagementApiDiagnosticFrontendResponse(
            body_bytes=body_bytes,
            data_masking=data_masking,
            headers_to_log=headers_to_log,
        )

        return typing.cast(None, jsii.invoke(self, "putFrontendResponse", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#create ApiManagementApiDiagnostic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#delete ApiManagementApiDiagnostic#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#read ApiManagementApiDiagnostic#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#update ApiManagementApiDiagnostic#update}.
        '''
        value = ApiManagementApiDiagnosticTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlwaysLogErrors")
    def reset_always_log_errors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysLogErrors", []))

    @jsii.member(jsii_name="resetBackendRequest")
    def reset_backend_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendRequest", []))

    @jsii.member(jsii_name="resetBackendResponse")
    def reset_backend_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackendResponse", []))

    @jsii.member(jsii_name="resetFrontendRequest")
    def reset_frontend_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontendRequest", []))

    @jsii.member(jsii_name="resetFrontendResponse")
    def reset_frontend_response(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrontendResponse", []))

    @jsii.member(jsii_name="resetHttpCorrelationProtocol")
    def reset_http_correlation_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpCorrelationProtocol", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogClientIp")
    def reset_log_client_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogClientIp", []))

    @jsii.member(jsii_name="resetOperationNameFormat")
    def reset_operation_name_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationNameFormat", []))

    @jsii.member(jsii_name="resetSamplingPercentage")
    def reset_sampling_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamplingPercentage", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVerbosity")
    def reset_verbosity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerbosity", []))

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
    @jsii.member(jsii_name="backendRequest")
    def backend_request(
        self,
    ) -> "ApiManagementApiDiagnosticBackendRequestOutputReference":
        return typing.cast("ApiManagementApiDiagnosticBackendRequestOutputReference", jsii.get(self, "backendRequest"))

    @builtins.property
    @jsii.member(jsii_name="backendResponse")
    def backend_response(
        self,
    ) -> "ApiManagementApiDiagnosticBackendResponseOutputReference":
        return typing.cast("ApiManagementApiDiagnosticBackendResponseOutputReference", jsii.get(self, "backendResponse"))

    @builtins.property
    @jsii.member(jsii_name="frontendRequest")
    def frontend_request(
        self,
    ) -> "ApiManagementApiDiagnosticFrontendRequestOutputReference":
        return typing.cast("ApiManagementApiDiagnosticFrontendRequestOutputReference", jsii.get(self, "frontendRequest"))

    @builtins.property
    @jsii.member(jsii_name="frontendResponse")
    def frontend_response(
        self,
    ) -> "ApiManagementApiDiagnosticFrontendResponseOutputReference":
        return typing.cast("ApiManagementApiDiagnosticFrontendResponseOutputReference", jsii.get(self, "frontendResponse"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApiManagementApiDiagnosticTimeoutsOutputReference":
        return typing.cast("ApiManagementApiDiagnosticTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alwaysLogErrorsInput")
    def always_log_errors_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alwaysLogErrorsInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementLoggerIdInput")
    def api_management_logger_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiManagementLoggerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementNameInput")
    def api_management_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiManagementNameInput"))

    @builtins.property
    @jsii.member(jsii_name="apiNameInput")
    def api_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiNameInput"))

    @builtins.property
    @jsii.member(jsii_name="backendRequestInput")
    def backend_request_input(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticBackendRequest"]:
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticBackendRequest"], jsii.get(self, "backendRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="backendResponseInput")
    def backend_response_input(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticBackendResponse"]:
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticBackendResponse"], jsii.get(self, "backendResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendRequestInput")
    def frontend_request_input(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticFrontendRequest"]:
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticFrontendRequest"], jsii.get(self, "frontendRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendResponseInput")
    def frontend_response_input(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticFrontendResponse"]:
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticFrontendResponse"], jsii.get(self, "frontendResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="httpCorrelationProtocolInput")
    def http_correlation_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpCorrelationProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logClientIpInput")
    def log_client_ip_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logClientIpInput"))

    @builtins.property
    @jsii.member(jsii_name="operationNameFormatInput")
    def operation_name_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationNameFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingPercentageInput")
    def sampling_percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingPercentageInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementApiDiagnosticTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementApiDiagnosticTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="verbosityInput")
    def verbosity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "verbosityInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysLogErrors")
    def always_log_errors(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alwaysLogErrors"))

    @always_log_errors.setter
    def always_log_errors(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94eb3d3101dd74b24f24b40c36150833a19ccbaa642b39cb022a6fb8f545811e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysLogErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiManagementLoggerId")
    def api_management_logger_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementLoggerId"))

    @api_management_logger_id.setter
    def api_management_logger_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148d383f1b7f129a56238d42ddf1fefa12254cb19b697bc17c4a5350f16e0253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementLoggerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiManagementName")
    def api_management_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementName"))

    @api_management_name.setter
    def api_management_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e10dc0219d222aa551d4a2bd5bcf732221b1e7b754cbb7926aebc255621703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiName")
    def api_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiName"))

    @api_name.setter
    def api_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08897ff8c5424afe4c907e3de405b86500c87fec58ef44146e6a609e30d5efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCorrelationProtocol")
    def http_correlation_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCorrelationProtocol"))

    @http_correlation_protocol.setter
    def http_correlation_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637c70c9abd3bd7eadaf98da9307544b31da390195e046ae5ef43e3e1c143898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCorrelationProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29404bc38749a3dfd2e55c1fcada4882dc85d6668b38e603927579a1bc9c5cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffa368dbe0f3e4c70519451dafaf7da71c2b9b312b485972fbd8812ceb584c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logClientIp")
    def log_client_ip(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logClientIp"))

    @log_client_ip.setter
    def log_client_ip(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc6b6fc9e836c5f67020b9b97759545af79f306556e89e7f639ad9eb20184b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logClientIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationNameFormat")
    def operation_name_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationNameFormat"))

    @operation_name_format.setter
    def operation_name_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7265567df0d4275593d7d93dd847a1b23b25b2cee620f35ed508b6bce568e3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationNameFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee79612d2206c1c33b1c7ec40c74aedc086f7eeb1fc12c0ea8fe83a6194a757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingPercentage")
    def sampling_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingPercentage"))

    @sampling_percentage.setter
    def sampling_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32142e0c8b09694db669e705641e41573887866ed765261f823df6066af85abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verbosity")
    def verbosity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verbosity"))

    @verbosity.setter
    def verbosity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58d153b89c7165a2ff680e665f07d962eb7a0733b6d58809ea027692bd57f47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verbosity", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequest",
    jsii_struct_bases=[],
    name_mapping={
        "body_bytes": "bodyBytes",
        "data_masking": "dataMasking",
        "headers_to_log": "headersToLog",
    },
)
class ApiManagementApiDiagnosticBackendRequest:
    def __init__(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementApiDiagnosticBackendRequestDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.
        '''
        if isinstance(data_masking, dict):
            data_masking = ApiManagementApiDiagnosticBackendRequestDataMasking(**data_masking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06260e3e1c660b850b91db9a17156a4c16bb22af85490365ad7891f0acd0f9cb)
            check_type(argname="argument body_bytes", value=body_bytes, expected_type=type_hints["body_bytes"])
            check_type(argname="argument data_masking", value=data_masking, expected_type=type_hints["data_masking"])
            check_type(argname="argument headers_to_log", value=headers_to_log, expected_type=type_hints["headers_to_log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body_bytes is not None:
            self._values["body_bytes"] = body_bytes
        if data_masking is not None:
            self._values["data_masking"] = data_masking
        if headers_to_log is not None:
            self._values["headers_to_log"] = headers_to_log

    @builtins.property
    def body_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.'''
        result = self._values.get("body_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_masking(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticBackendRequestDataMasking"]:
        '''data_masking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        '''
        result = self._values.get("data_masking")
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticBackendRequestDataMasking"], result)

    @builtins.property
    def headers_to_log(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.'''
        result = self._values.get("headers_to_log")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticBackendRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestDataMasking",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "query_params": "queryParams"},
)
class ApiManagementApiDiagnosticBackendRequestDataMasking:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b071e89261f2ec92452d1bc052413e682e23e87d4c64bfc4cf54fa845c3c8462)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument query_params", value=query_params, expected_type=type_hints["query_params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers
        if query_params is not None:
            self._values["query_params"] = query_params

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders"]]], result)

    @builtins.property
    def query_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams"]]]:
        '''query_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticBackendRequestDataMasking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640d78506755a8ba9b2029071353cb6ece01ad5287d75aed87275c381aadaf77)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7db8b8706230f587fb733598f5c0c6756f0036891c44fb1f782cf5a5844e097f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874b6dc22d784c6ebc08ed0dfc328c03958ade1a4c5dcc96a6a05488b3014c68)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3320fb11b74958db2d3e0028ae37754e717b2be10a8ad07a587c7d8b9de47d90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df894f068daeed9b3f58a3f1846322d75d80161a791310d25eb2a806abddfbbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20a9825b4496efaa4f2d71ca805bfdc52f6f237815a69c604ec43e9b8d23c2bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bda963a2206c153b8688860c5e94d74bde35d7465facdc9c05396bd2455644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c77701e4a7149dedaaf2d56bbb6044e79cde3f8dbe38fa0465cfe99b622434)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65b1974b92d505ab885878db2c6cf1038498175ca9775e0896f27f5cf944de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07109c92481ebc02551e8382916c0b27a4a32689b5a928b3a68ae495e35b10c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f916f26e72eefbf99f9d15a873bf5243a278e77bc23787e8af4b33134942fb6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticBackendRequestDataMaskingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestDataMaskingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7404654c263cd48d5f2f4daa2d8c901eaa4a1e31addc90238230d32aec64a02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d786c51882e58983f6a238fe33331c7eb3f088eba196b611e1a3fee9765eba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParams")
    def put_query_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383a8c518525762a366f55df7af6edff9f61d1db86adbd2a8606f7e943a97b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParams", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetQueryParams")
    def reset_query_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParams", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersList:
        return typing.cast(ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(
        self,
    ) -> "ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsList":
        return typing.cast("ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsList", jsii.get(self, "queryParams"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams"]]], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticBackendRequestDataMasking]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticBackendRequestDataMasking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiDiagnosticBackendRequestDataMasking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408b32cb66476d636a77c41ad1cf00151cba99b52de419b8232fb995c8673f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048b93cae3e7a7ebfe620703a9319675e9b922bd1206fd933a674f387713f60d)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b13e1b51cffb5e0719f9e6c583e4c19b0b71e10b3e67a2a73118aa54d93ea1f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18454ddf73290c31c69a4245e8cb8d3098fab992f9689623e3a4c2c1fa1a3cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c3c9ed553c01ae8f558a65bf2fe6a244e82b5204915236b10f18ceb7387cfb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19849d8270c1338785aad20ce29ae228746cc66503f2a133e92217a12c451369)
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
            type_hints = typing.get_type_hints(_typecheckingstub__185631156f947126c2c1cc045fb6d81a4e4c1ef3cef94206dbaa113dfc7c78eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1535038dbbe5c84549f4439bae019cdd1ee4d43012c45030abe330c3dfc0bf19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f20b29e87dbe632ed79c9c47c790e40706349d290abd2c1f95d1b280dad02a39)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59af17e6fd6a93ba044f3ed2d370f5a7bda93952faf30364a890456262400d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6855aba43969296b0b8118604e1a5c3f380b4c1aa7a8afd5b644c234e19b5f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd47f1389ec60d9644f6579e87e5199f7a0269915d383221de66ac2bc2885e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticBackendRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cbb18c4302e677e66b4b7b68cce45d0616494a0ea4afc5095794db16a2f1dc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataMasking")
    def put_data_masking(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        value = ApiManagementApiDiagnosticBackendRequestDataMasking(
            headers=headers, query_params=query_params
        )

        return typing.cast(None, jsii.invoke(self, "putDataMasking", [value]))

    @jsii.member(jsii_name="resetBodyBytes")
    def reset_body_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyBytes", []))

    @jsii.member(jsii_name="resetDataMasking")
    def reset_data_masking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataMasking", []))

    @jsii.member(jsii_name="resetHeadersToLog")
    def reset_headers_to_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadersToLog", []))

    @builtins.property
    @jsii.member(jsii_name="dataMasking")
    def data_masking(
        self,
    ) -> ApiManagementApiDiagnosticBackendRequestDataMaskingOutputReference:
        return typing.cast(ApiManagementApiDiagnosticBackendRequestDataMaskingOutputReference, jsii.get(self, "dataMasking"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytesInput")
    def body_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bodyBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMaskingInput")
    def data_masking_input(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticBackendRequestDataMasking]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticBackendRequestDataMasking], jsii.get(self, "dataMaskingInput"))

    @builtins.property
    @jsii.member(jsii_name="headersToLogInput")
    def headers_to_log_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headersToLogInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytes")
    def body_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bodyBytes"))

    @body_bytes.setter
    def body_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2893a24a4e5775a7bed5d99a1fc73e56dfc0f03f5f277607673d427b50c5091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersToLog")
    def headers_to_log(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersToLog"))

    @headers_to_log.setter
    def headers_to_log(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6c7a072fa729055f270aa147ebc544b17a4685ad393b9aa4854f717678942d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersToLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticBackendRequest]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticBackendRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiDiagnosticBackendRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89cbd2f8c5f4918082e8812802d741ecc609b444f71b38532908ca42fc7992a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponse",
    jsii_struct_bases=[],
    name_mapping={
        "body_bytes": "bodyBytes",
        "data_masking": "dataMasking",
        "headers_to_log": "headersToLog",
    },
)
class ApiManagementApiDiagnosticBackendResponse:
    def __init__(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementApiDiagnosticBackendResponseDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.
        '''
        if isinstance(data_masking, dict):
            data_masking = ApiManagementApiDiagnosticBackendResponseDataMasking(**data_masking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dd607d79aaecc47549f0b8b61ad70bbfe3b9fd4a60a3bd11afd7adde77cbee)
            check_type(argname="argument body_bytes", value=body_bytes, expected_type=type_hints["body_bytes"])
            check_type(argname="argument data_masking", value=data_masking, expected_type=type_hints["data_masking"])
            check_type(argname="argument headers_to_log", value=headers_to_log, expected_type=type_hints["headers_to_log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body_bytes is not None:
            self._values["body_bytes"] = body_bytes
        if data_masking is not None:
            self._values["data_masking"] = data_masking
        if headers_to_log is not None:
            self._values["headers_to_log"] = headers_to_log

    @builtins.property
    def body_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.'''
        result = self._values.get("body_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_masking(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticBackendResponseDataMasking"]:
        '''data_masking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        '''
        result = self._values.get("data_masking")
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticBackendResponseDataMasking"], result)

    @builtins.property
    def headers_to_log(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.'''
        result = self._values.get("headers_to_log")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticBackendResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseDataMasking",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "query_params": "queryParams"},
)
class ApiManagementApiDiagnosticBackendResponseDataMasking:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03314da5eabba0e7383d55977b2f6ef09a203cc0c44db11937207a55fb50f5ee)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument query_params", value=query_params, expected_type=type_hints["query_params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers
        if query_params is not None:
            self._values["query_params"] = query_params

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders"]]], result)

    @builtins.property
    def query_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams"]]]:
        '''query_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticBackendResponseDataMasking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89f38e7b17a3ba9fffe17f348b3e59dd61d23ead5cb620174a8f81c40ab01b27)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5281b00035d66f42191d8edc121fa56156518e4b683594dd7a6c2ce7c479f452)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc4780c940e927901975a616ad570ef2a95091889eac272d893fb5bb3645dec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802294b039672329acfa0cee39b8ee5065f91e228305bc3036a5b9149e022007)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e397a8150b00675fd38ba7e821f72cd90189c8872e684af68d8796accaf1120)
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
            type_hints = typing.get_type_hints(_typecheckingstub__501e0c7e0b5e699f2579dad363d60d9cee048c87148479a0ee8689629ddcc451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32296493a24961089b787dcc34d05cbf15db52457c089beb21f2c6f464000d20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3a532838c3a7eabbc2560b6690d60758377d2762f4a71b19448d089a97758ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1144482cb677cac9bf236c47128a32f4304588a2f996e5d6b494d659f2bc87ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267a38188419c12f29d31cb9c1664040fba44df2c7c3f6cfb67a5f1b4cc18d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3465ef2c26d8cb721e6ba5930751ba36ed0344dea9ba735005c537fa3a29a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticBackendResponseDataMaskingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseDataMaskingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea8a125b9712d5ea98edce8e01fc8b33ddaf87a250fdee7ddfb759a10794c2d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a6d891fe9b92c2089aff3458eac956638042bc038f7f824743bf859887d577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParams")
    def put_query_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__298308bc5962a3d92aab09f347535d48cf642386edffabfd0185c4a604a18d81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParams", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetQueryParams")
    def reset_query_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParams", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(
        self,
    ) -> ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersList:
        return typing.cast(ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(
        self,
    ) -> "ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsList":
        return typing.cast("ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsList", jsii.get(self, "queryParams"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams"]]], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticBackendResponseDataMasking]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticBackendResponseDataMasking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiDiagnosticBackendResponseDataMasking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc7b102f5f15a3fdfce7fd3eaabdc63956f0fc3316361898bace1187370710f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff07c2617748af8ada4032ac2bfaedba2e5c21eeedb19153198d178ea19b9c99)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2641026760f029c0995affb811f25177fa79ae4466f72d3e2e4937ee133d2083)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce625f808624f0c2a5334e555be82e29da710620a4cf0a2be7bb81c32c832d4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865609add8a932aeadfafce3360511eccb0c85b0c56d30b747adae3e536c8c29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0c48beb1342d39a311e69d33bb5a044da92c995d7d1516310fd403b119621fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a97d69cefd16d30e56b4a4be69b45e149824ead53c13d8e041b228c8cea50fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c224c4c5ef7a552b5ee4928481cb01ccec3b3da1fd960f70486c146fd33a7fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5bd4b9edef2d8b3ac427ade246d34d022d4051f30b92878c7255b11baae1639)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b719c9bfea079dcbc1d0550dd27acc39799776b6d0ba73e7603f1f16ea56ccd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59630cac74ef4454a1ea58c7ffb47ae167b27b664c7533f7396788d5b1cf5b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39ef1822a08c540201a3ef0052d356d3678b146712ba8d808599563faf0a1ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticBackendResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticBackendResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4eb24e8083c17b452f34247da5eee17c0264b2fe9495bf553d4a15a75441fc8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataMasking")
    def put_data_masking(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        value = ApiManagementApiDiagnosticBackendResponseDataMasking(
            headers=headers, query_params=query_params
        )

        return typing.cast(None, jsii.invoke(self, "putDataMasking", [value]))

    @jsii.member(jsii_name="resetBodyBytes")
    def reset_body_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyBytes", []))

    @jsii.member(jsii_name="resetDataMasking")
    def reset_data_masking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataMasking", []))

    @jsii.member(jsii_name="resetHeadersToLog")
    def reset_headers_to_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadersToLog", []))

    @builtins.property
    @jsii.member(jsii_name="dataMasking")
    def data_masking(
        self,
    ) -> ApiManagementApiDiagnosticBackendResponseDataMaskingOutputReference:
        return typing.cast(ApiManagementApiDiagnosticBackendResponseDataMaskingOutputReference, jsii.get(self, "dataMasking"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytesInput")
    def body_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bodyBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMaskingInput")
    def data_masking_input(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticBackendResponseDataMasking]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticBackendResponseDataMasking], jsii.get(self, "dataMaskingInput"))

    @builtins.property
    @jsii.member(jsii_name="headersToLogInput")
    def headers_to_log_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headersToLogInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytes")
    def body_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bodyBytes"))

    @body_bytes.setter
    def body_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afba268e5b632d8c256c98a1f11a557a283a48fdf119bca5d6bd544a802dbbf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersToLog")
    def headers_to_log(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersToLog"))

    @headers_to_log.setter
    def headers_to_log(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b586b03e068849c088ad89eec7b11f99d30e67c2a2dcc9f0a2d48e5c0e8896ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersToLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticBackendResponse]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticBackendResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiDiagnosticBackendResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5b46c4dc77b3201fd903e5b3548515d65730f7fd873ca1bd56940317bd2150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_management_logger_id": "apiManagementLoggerId",
        "api_management_name": "apiManagementName",
        "api_name": "apiName",
        "identifier": "identifier",
        "resource_group_name": "resourceGroupName",
        "always_log_errors": "alwaysLogErrors",
        "backend_request": "backendRequest",
        "backend_response": "backendResponse",
        "frontend_request": "frontendRequest",
        "frontend_response": "frontendResponse",
        "http_correlation_protocol": "httpCorrelationProtocol",
        "id": "id",
        "log_client_ip": "logClientIp",
        "operation_name_format": "operationNameFormat",
        "sampling_percentage": "samplingPercentage",
        "timeouts": "timeouts",
        "verbosity": "verbosity",
    },
)
class ApiManagementApiDiagnosticConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_management_logger_id: builtins.str,
        api_management_name: builtins.str,
        api_name: builtins.str,
        identifier: builtins.str,
        resource_group_name: builtins.str,
        always_log_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_request: typing.Optional[typing.Union[ApiManagementApiDiagnosticBackendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        backend_response: typing.Optional[typing.Union[ApiManagementApiDiagnosticBackendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_request: typing.Optional[typing.Union["ApiManagementApiDiagnosticFrontendRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_response: typing.Optional[typing.Union["ApiManagementApiDiagnosticFrontendResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        http_correlation_protocol: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_client_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operation_name_format: typing.Optional[builtins.str] = None,
        sampling_percentage: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementApiDiagnosticTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        verbosity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_management_logger_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_management_logger_id ApiManagementApiDiagnostic#api_management_logger_id}.
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_management_name ApiManagementApiDiagnostic#api_management_name}.
        :param api_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_name ApiManagementApiDiagnostic#api_name}.
        :param identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#identifier ApiManagementApiDiagnostic#identifier}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#resource_group_name ApiManagementApiDiagnostic#resource_group_name}.
        :param always_log_errors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#always_log_errors ApiManagementApiDiagnostic#always_log_errors}.
        :param backend_request: backend_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#backend_request ApiManagementApiDiagnostic#backend_request}
        :param backend_response: backend_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#backend_response ApiManagementApiDiagnostic#backend_response}
        :param frontend_request: frontend_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#frontend_request ApiManagementApiDiagnostic#frontend_request}
        :param frontend_response: frontend_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#frontend_response ApiManagementApiDiagnostic#frontend_response}
        :param http_correlation_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#http_correlation_protocol ApiManagementApiDiagnostic#http_correlation_protocol}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#id ApiManagementApiDiagnostic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_client_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#log_client_ip ApiManagementApiDiagnostic#log_client_ip}.
        :param operation_name_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#operation_name_format ApiManagementApiDiagnostic#operation_name_format}.
        :param sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#sampling_percentage ApiManagementApiDiagnostic#sampling_percentage}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#timeouts ApiManagementApiDiagnostic#timeouts}
        :param verbosity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#verbosity ApiManagementApiDiagnostic#verbosity}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backend_request, dict):
            backend_request = ApiManagementApiDiagnosticBackendRequest(**backend_request)
        if isinstance(backend_response, dict):
            backend_response = ApiManagementApiDiagnosticBackendResponse(**backend_response)
        if isinstance(frontend_request, dict):
            frontend_request = ApiManagementApiDiagnosticFrontendRequest(**frontend_request)
        if isinstance(frontend_response, dict):
            frontend_response = ApiManagementApiDiagnosticFrontendResponse(**frontend_response)
        if isinstance(timeouts, dict):
            timeouts = ApiManagementApiDiagnosticTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95d977fdfd0739cfb51f2689fb5963789929a273bde8f8380a9af98f0d35d7e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_management_logger_id", value=api_management_logger_id, expected_type=type_hints["api_management_logger_id"])
            check_type(argname="argument api_management_name", value=api_management_name, expected_type=type_hints["api_management_name"])
            check_type(argname="argument api_name", value=api_name, expected_type=type_hints["api_name"])
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument always_log_errors", value=always_log_errors, expected_type=type_hints["always_log_errors"])
            check_type(argname="argument backend_request", value=backend_request, expected_type=type_hints["backend_request"])
            check_type(argname="argument backend_response", value=backend_response, expected_type=type_hints["backend_response"])
            check_type(argname="argument frontend_request", value=frontend_request, expected_type=type_hints["frontend_request"])
            check_type(argname="argument frontend_response", value=frontend_response, expected_type=type_hints["frontend_response"])
            check_type(argname="argument http_correlation_protocol", value=http_correlation_protocol, expected_type=type_hints["http_correlation_protocol"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_client_ip", value=log_client_ip, expected_type=type_hints["log_client_ip"])
            check_type(argname="argument operation_name_format", value=operation_name_format, expected_type=type_hints["operation_name_format"])
            check_type(argname="argument sampling_percentage", value=sampling_percentage, expected_type=type_hints["sampling_percentage"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument verbosity", value=verbosity, expected_type=type_hints["verbosity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_management_logger_id": api_management_logger_id,
            "api_management_name": api_management_name,
            "api_name": api_name,
            "identifier": identifier,
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
        if always_log_errors is not None:
            self._values["always_log_errors"] = always_log_errors
        if backend_request is not None:
            self._values["backend_request"] = backend_request
        if backend_response is not None:
            self._values["backend_response"] = backend_response
        if frontend_request is not None:
            self._values["frontend_request"] = frontend_request
        if frontend_response is not None:
            self._values["frontend_response"] = frontend_response
        if http_correlation_protocol is not None:
            self._values["http_correlation_protocol"] = http_correlation_protocol
        if id is not None:
            self._values["id"] = id
        if log_client_ip is not None:
            self._values["log_client_ip"] = log_client_ip
        if operation_name_format is not None:
            self._values["operation_name_format"] = operation_name_format
        if sampling_percentage is not None:
            self._values["sampling_percentage"] = sampling_percentage
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if verbosity is not None:
            self._values["verbosity"] = verbosity

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
    def api_management_logger_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_management_logger_id ApiManagementApiDiagnostic#api_management_logger_id}.'''
        result = self._values.get("api_management_logger_id")
        assert result is not None, "Required property 'api_management_logger_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_management_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_management_name ApiManagementApiDiagnostic#api_management_name}.'''
        result = self._values.get("api_management_name")
        assert result is not None, "Required property 'api_management_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#api_name ApiManagementApiDiagnostic#api_name}.'''
        result = self._values.get("api_name")
        assert result is not None, "Required property 'api_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#identifier ApiManagementApiDiagnostic#identifier}.'''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#resource_group_name ApiManagementApiDiagnostic#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_log_errors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#always_log_errors ApiManagementApiDiagnostic#always_log_errors}.'''
        result = self._values.get("always_log_errors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backend_request(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticBackendRequest]:
        '''backend_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#backend_request ApiManagementApiDiagnostic#backend_request}
        '''
        result = self._values.get("backend_request")
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticBackendRequest], result)

    @builtins.property
    def backend_response(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticBackendResponse]:
        '''backend_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#backend_response ApiManagementApiDiagnostic#backend_response}
        '''
        result = self._values.get("backend_response")
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticBackendResponse], result)

    @builtins.property
    def frontend_request(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticFrontendRequest"]:
        '''frontend_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#frontend_request ApiManagementApiDiagnostic#frontend_request}
        '''
        result = self._values.get("frontend_request")
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticFrontendRequest"], result)

    @builtins.property
    def frontend_response(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticFrontendResponse"]:
        '''frontend_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#frontend_response ApiManagementApiDiagnostic#frontend_response}
        '''
        result = self._values.get("frontend_response")
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticFrontendResponse"], result)

    @builtins.property
    def http_correlation_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#http_correlation_protocol ApiManagementApiDiagnostic#http_correlation_protocol}.'''
        result = self._values.get("http_correlation_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#id ApiManagementApiDiagnostic#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_client_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#log_client_ip ApiManagementApiDiagnostic#log_client_ip}.'''
        result = self._values.get("log_client_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operation_name_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#operation_name_format ApiManagementApiDiagnostic#operation_name_format}.'''
        result = self._values.get("operation_name_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sampling_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#sampling_percentage ApiManagementApiDiagnostic#sampling_percentage}.'''
        result = self._values.get("sampling_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApiManagementApiDiagnosticTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#timeouts ApiManagementApiDiagnostic#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticTimeouts"], result)

    @builtins.property
    def verbosity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#verbosity ApiManagementApiDiagnostic#verbosity}.'''
        result = self._values.get("verbosity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequest",
    jsii_struct_bases=[],
    name_mapping={
        "body_bytes": "bodyBytes",
        "data_masking": "dataMasking",
        "headers_to_log": "headersToLog",
    },
)
class ApiManagementApiDiagnosticFrontendRequest:
    def __init__(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementApiDiagnosticFrontendRequestDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.
        '''
        if isinstance(data_masking, dict):
            data_masking = ApiManagementApiDiagnosticFrontendRequestDataMasking(**data_masking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85920ed057cc9ba8fc783694ac7a254bb45b7a60b65792a4692e2fb42c074428)
            check_type(argname="argument body_bytes", value=body_bytes, expected_type=type_hints["body_bytes"])
            check_type(argname="argument data_masking", value=data_masking, expected_type=type_hints["data_masking"])
            check_type(argname="argument headers_to_log", value=headers_to_log, expected_type=type_hints["headers_to_log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body_bytes is not None:
            self._values["body_bytes"] = body_bytes
        if data_masking is not None:
            self._values["data_masking"] = data_masking
        if headers_to_log is not None:
            self._values["headers_to_log"] = headers_to_log

    @builtins.property
    def body_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.'''
        result = self._values.get("body_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_masking(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticFrontendRequestDataMasking"]:
        '''data_masking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        '''
        result = self._values.get("data_masking")
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticFrontendRequestDataMasking"], result)

    @builtins.property
    def headers_to_log(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.'''
        result = self._values.get("headers_to_log")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticFrontendRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestDataMasking",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "query_params": "queryParams"},
)
class ApiManagementApiDiagnosticFrontendRequestDataMasking:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__084bd8c5a629638424a361777f3373b72fb0c68d1e4261d3aad189f639a04f76)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument query_params", value=query_params, expected_type=type_hints["query_params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers
        if query_params is not None:
            self._values["query_params"] = query_params

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders"]]], result)

    @builtins.property
    def query_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams"]]]:
        '''query_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticFrontendRequestDataMasking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34f6cc788d534c4b11e6057e1364223144b2a8cede095c941b21aab984a1e98)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5603519613c98ecea20b613574674f62a8298496da64de8ed415c181edac68c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63485909d6ab86b760043141dc240d98d0136011ba32bf171097f43b27cf35a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64d4affcd7f6ddc17c72348faa03312d102f3422b914425f7fc3475da609586)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41247734249afe1a047bcdfe545dc7bc08550fcfcde66af178d9714ab06f96ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08341e165609e52aa1fb94d29af763857b428b26dc8ce3f344741fdae6db7b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65069b0864b1ca49bd3bdf019b2216a8da0fa5f9bb3164df25ae6a03f3b1ce1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f13a9138c89b18ec12543225c149e4fe6a77e2a9341cd1036ad9d29c8260c4fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__974d0657a706410e99af17a0d6baa63bcec500f038499e529bc6c817de6f5de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f5b5ad60a931f28766afde2bd562defbd57d4a0d49c558070198c5e441d208a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00c523fc9beef0a57ff039675681ed050d7d57355318f67facace858c1c38f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticFrontendRequestDataMaskingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestDataMaskingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d367bd0463d68047e65b0cea7620a78261fc67129190c0f5c4819760db9f8fd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bbf6ac305c3f3ae3ffa5b73c0f007e1de2515b9a088f58ae2333971a39be0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParams")
    def put_query_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16cd3a39f3f18de43c7ce826517ac8c48a9488f15dd6f84e575f47d65b523258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParams", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetQueryParams")
    def reset_query_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParams", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(
        self,
    ) -> ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersList:
        return typing.cast(ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(
        self,
    ) -> "ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsList":
        return typing.cast("ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsList", jsii.get(self, "queryParams"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams"]]], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticFrontendRequestDataMasking]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticFrontendRequestDataMasking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiDiagnosticFrontendRequestDataMasking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b17cf78ee54757bb789b92a25684f0e7fcb27d6c3567d86808e26069831237)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db78afe4d798eb8855b1e2db14b9502d2a34440bd335930598fa8e58a3113c5)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edf1400844d6e91be10703fb500175728abc861053bb8ba4fac9f113c023d936)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4eb08ccc8810c78d7428b77566a469af11754e945451af68db6e16ef28eb743)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d262b962f02483ea92899c62222723a0b7370d4c17b246817525da9de31ce5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec17cceff91d8b9081f9af934bc3c63bcc08d71d9ff506dfb2e2175032fd9c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c25446f97b0f82b1bbac62424217771644b5f46202ad595fa0d634454ec66984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06d0a82b2593685dbb2d73f645f344232712b5204bf6b8fad2cf44f3b48f0910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe6457ccb74e1100a038080f26b55802e43ed617b77e2059bc45ea4ee0dfc896)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae5fc361a3cb24467e20581d42b58261e05039ef5abfff1b2aeb56e676702cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051bfae3a9b585031adcad329715082d3424a7a5c9af2d86656f4791d403b7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfc3627f67a5fa6d81d548fa8ca0668a2ef0c34848ff9bde7a4e85543b25c47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticFrontendRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bb38d13c500ce748947a8a2643825d748c978b5e2ad2ae326aacec6643f4994)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataMasking")
    def put_data_masking(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        value = ApiManagementApiDiagnosticFrontendRequestDataMasking(
            headers=headers, query_params=query_params
        )

        return typing.cast(None, jsii.invoke(self, "putDataMasking", [value]))

    @jsii.member(jsii_name="resetBodyBytes")
    def reset_body_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyBytes", []))

    @jsii.member(jsii_name="resetDataMasking")
    def reset_data_masking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataMasking", []))

    @jsii.member(jsii_name="resetHeadersToLog")
    def reset_headers_to_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadersToLog", []))

    @builtins.property
    @jsii.member(jsii_name="dataMasking")
    def data_masking(
        self,
    ) -> ApiManagementApiDiagnosticFrontendRequestDataMaskingOutputReference:
        return typing.cast(ApiManagementApiDiagnosticFrontendRequestDataMaskingOutputReference, jsii.get(self, "dataMasking"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytesInput")
    def body_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bodyBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMaskingInput")
    def data_masking_input(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticFrontendRequestDataMasking]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticFrontendRequestDataMasking], jsii.get(self, "dataMaskingInput"))

    @builtins.property
    @jsii.member(jsii_name="headersToLogInput")
    def headers_to_log_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headersToLogInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytes")
    def body_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bodyBytes"))

    @body_bytes.setter
    def body_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e1eb6d28d159e60ff32016d9dfa65c3e6f62f05222015f724e5bec3a7770c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersToLog")
    def headers_to_log(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersToLog"))

    @headers_to_log.setter
    def headers_to_log(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c7e5abb1a23104c77efed2bd9e6235ce814227024e4d290b6474d14bfcfcf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersToLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticFrontendRequest]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticFrontendRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiDiagnosticFrontendRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ecd7c23fa85877331881e1132c1b45e0f771504c7f0eb2a09c7d622397174d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponse",
    jsii_struct_bases=[],
    name_mapping={
        "body_bytes": "bodyBytes",
        "data_masking": "dataMasking",
        "headers_to_log": "headersToLog",
    },
)
class ApiManagementApiDiagnosticFrontendResponse:
    def __init__(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementApiDiagnosticFrontendResponseDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.
        '''
        if isinstance(data_masking, dict):
            data_masking = ApiManagementApiDiagnosticFrontendResponseDataMasking(**data_masking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba0659224c33b821af16153708c6ca13b322cd15ede04f8fe7df7d557959ccc)
            check_type(argname="argument body_bytes", value=body_bytes, expected_type=type_hints["body_bytes"])
            check_type(argname="argument data_masking", value=data_masking, expected_type=type_hints["data_masking"])
            check_type(argname="argument headers_to_log", value=headers_to_log, expected_type=type_hints["headers_to_log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if body_bytes is not None:
            self._values["body_bytes"] = body_bytes
        if data_masking is not None:
            self._values["data_masking"] = data_masking
        if headers_to_log is not None:
            self._values["headers_to_log"] = headers_to_log

    @builtins.property
    def body_bytes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#body_bytes ApiManagementApiDiagnostic#body_bytes}.'''
        result = self._values.get("body_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_masking(
        self,
    ) -> typing.Optional["ApiManagementApiDiagnosticFrontendResponseDataMasking"]:
        '''data_masking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#data_masking ApiManagementApiDiagnostic#data_masking}
        '''
        result = self._values.get("data_masking")
        return typing.cast(typing.Optional["ApiManagementApiDiagnosticFrontendResponseDataMasking"], result)

    @builtins.property
    def headers_to_log(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers_to_log ApiManagementApiDiagnostic#headers_to_log}.'''
        result = self._values.get("headers_to_log")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticFrontendResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseDataMasking",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "query_params": "queryParams"},
)
class ApiManagementApiDiagnosticFrontendResponseDataMasking:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e5535bcfa600a9b27dac4e9c5442ff00a888b3b5d12c203c21f5973754279c)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument query_params", value=query_params, expected_type=type_hints["query_params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers
        if query_params is not None:
            self._values["query_params"] = query_params

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders"]]], result)

    @builtins.property
    def query_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams"]]]:
        '''query_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticFrontendResponseDataMasking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde6ece82de1592c3b06cbf08e06daf34c8c4442d53a406b5f8ede52c0f27eee)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed04135dfa34ad33aabea57be42f45875a6153bb48ed579ef7d2a71e00bd2c43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b16de26e8769381f2b00310acedb8299d2284760615f4132cf040b3fa3864c9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07128a859693464fb94c9d63ff926153d1ddb2dcdd8a3468113f75346f0599f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cf09a17977c963d8ecaf29b44617e5c3a1ce2b1dec51c5973605a286d98cd5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__357694f481a8e8ceba8a6b1743ffabfc23be2f5c6f88ff873f4e451f201aa00c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba83e0dd9a6936d6c3baf1658174394903810d429a36cc9cd942c3b1d2504af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46c327b08b5b6daafd91c6cc22db63f65afa1a7fb262410a8af4c59090bce8fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029f77bd453147c34f0afcb6b203b918ec7d66564aba458a5d1d7a4df9abba48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae62182d388bbe9df2ff33149706b1fbf6fc37dd9e825cd044b85aa4fb55f758)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a35e6ce27c34b6bde0b8a528bdac5038f355bf24610fdd4afa90ee0d67d34fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticFrontendResponseDataMaskingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseDataMaskingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7807286f3fadd72ef28c4b89779bf0584b00b5a69476ea2fe70bf72e15ad9ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83a443b244d55aa036481d34be562f96028325bea24fbadf5d7e770a9390152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParams")
    def put_query_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd996b399ae23810390ec190259df3e44c207f5cf8d5f8fd65d9cdc8102646f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParams", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetQueryParams")
    def reset_query_params(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParams", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(
        self,
    ) -> ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersList:
        return typing.cast(ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(
        self,
    ) -> "ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsList":
        return typing.cast("ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsList", jsii.get(self, "queryParams"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams"]]], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticFrontendResponseDataMasking]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticFrontendResponseDataMasking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiDiagnosticFrontendResponseDataMasking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bd54081ebf9ade698285d22d124ad539cca26b9f16b8698bf21e39283d60ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514e82eb6fc932405d8a7f66cd0e74399e6841e8a6f9a22c21997bf5c9fe3618)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#mode ApiManagementApiDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#value ApiManagementApiDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34415537d2049e7b7ff28522e06b062f8e4d71082179cc0daa51c0f452df4543)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c91938e64453fdf4e96363d935d44b6d5815827cac78b90e62dfff2726e35a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__128c8732587bd7695c99895edbf0aa3ed40808c9411a0913709d5901e025e9d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23491ae0eb3341646d79cdad47beaf983cef0e4a0c95dea6f10c530872159dce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf2154929b1fad8e83aae52fc9f0eccfc4c9ea5bb0545484e17f7aef629600ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a05c17821c1b078d8ead70e417cbea68fa8489fa7fb30403b69eb0e3217cf65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__960de71fd4981067f43ed9cf323481e56c0b02ca752e8b7481c17fa737dfb4f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2115c6f3a7997a051b7c5b14497371def53b6073944aa6d2747f227cc15275f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec3dddb4b0e6ec0943a54bb4d3dddadd0e39cb2f9574193602e57a9ac5222b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83bf9723bb21d2c3ba0a66d880ba62e23ceafd35eb9b5fa3a800944e648a4844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementApiDiagnosticFrontendResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticFrontendResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24be1aeda1cccafea5c9d7609b8fc67da80c084a04bddc6fd98550c1ec17e9e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataMasking")
    def put_data_masking(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#headers ApiManagementApiDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#query_params ApiManagementApiDiagnostic#query_params}
        '''
        value = ApiManagementApiDiagnosticFrontendResponseDataMasking(
            headers=headers, query_params=query_params
        )

        return typing.cast(None, jsii.invoke(self, "putDataMasking", [value]))

    @jsii.member(jsii_name="resetBodyBytes")
    def reset_body_bytes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBodyBytes", []))

    @jsii.member(jsii_name="resetDataMasking")
    def reset_data_masking(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataMasking", []))

    @jsii.member(jsii_name="resetHeadersToLog")
    def reset_headers_to_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeadersToLog", []))

    @builtins.property
    @jsii.member(jsii_name="dataMasking")
    def data_masking(
        self,
    ) -> ApiManagementApiDiagnosticFrontendResponseDataMaskingOutputReference:
        return typing.cast(ApiManagementApiDiagnosticFrontendResponseDataMaskingOutputReference, jsii.get(self, "dataMasking"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytesInput")
    def body_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bodyBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMaskingInput")
    def data_masking_input(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticFrontendResponseDataMasking]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticFrontendResponseDataMasking], jsii.get(self, "dataMaskingInput"))

    @builtins.property
    @jsii.member(jsii_name="headersToLogInput")
    def headers_to_log_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "headersToLogInput"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytes")
    def body_bytes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bodyBytes"))

    @body_bytes.setter
    def body_bytes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__245ff6952c67a5a09717a209c2142c2ddf51bf268ef5e34112ae734084db4721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersToLog")
    def headers_to_log(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersToLog"))

    @headers_to_log.setter
    def headers_to_log(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9f45b4a35fccc6c8bf7806c4663017b275a3191b056e78685690d884bda25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersToLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementApiDiagnosticFrontendResponse]:
        return typing.cast(typing.Optional[ApiManagementApiDiagnosticFrontendResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementApiDiagnosticFrontendResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c81f82936a0b8c4436417856e0ee7ed980255fe6dd5d900e1b2cc642fb29fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApiManagementApiDiagnosticTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#create ApiManagementApiDiagnostic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#delete ApiManagementApiDiagnostic#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#read ApiManagementApiDiagnostic#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#update ApiManagementApiDiagnostic#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fbc888cf4b26152cfb11bc3b52f09c579fbefd90b41220eca3822c58d75a2f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#create ApiManagementApiDiagnostic#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#delete ApiManagementApiDiagnostic#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#read ApiManagementApiDiagnostic#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_api_diagnostic#update ApiManagementApiDiagnostic#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementApiDiagnosticTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementApiDiagnosticTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementApiDiagnostic.ApiManagementApiDiagnosticTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__013d20e750c5219a961ac58a939d00e8b51748ce3e01dc3361afe1ed6e058fd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cfd64ab07604fb67d80508c823c64e5e458a353e39901bba50dcaa2fcdc6fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0baa062301c5b31c6a9266c74e435b9b5fab0f4982cdfd8f54194c6c774a8dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a9bd2dd70185da1251e3824d0c670e6663fe578e46caefb0af0db40457bab21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cff914d20e63b9621ed264f5c9f3a88fcc36695b75012ec259027fe72fbabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b471b32c66136c291371aef3c1c8641ada6525136a6ee01074d3166d515d0e0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiManagementApiDiagnostic",
    "ApiManagementApiDiagnosticBackendRequest",
    "ApiManagementApiDiagnosticBackendRequestDataMasking",
    "ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders",
    "ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersList",
    "ApiManagementApiDiagnosticBackendRequestDataMaskingHeadersOutputReference",
    "ApiManagementApiDiagnosticBackendRequestDataMaskingOutputReference",
    "ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams",
    "ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsList",
    "ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParamsOutputReference",
    "ApiManagementApiDiagnosticBackendRequestOutputReference",
    "ApiManagementApiDiagnosticBackendResponse",
    "ApiManagementApiDiagnosticBackendResponseDataMasking",
    "ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders",
    "ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersList",
    "ApiManagementApiDiagnosticBackendResponseDataMaskingHeadersOutputReference",
    "ApiManagementApiDiagnosticBackendResponseDataMaskingOutputReference",
    "ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams",
    "ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsList",
    "ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParamsOutputReference",
    "ApiManagementApiDiagnosticBackendResponseOutputReference",
    "ApiManagementApiDiagnosticConfig",
    "ApiManagementApiDiagnosticFrontendRequest",
    "ApiManagementApiDiagnosticFrontendRequestDataMasking",
    "ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders",
    "ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersList",
    "ApiManagementApiDiagnosticFrontendRequestDataMaskingHeadersOutputReference",
    "ApiManagementApiDiagnosticFrontendRequestDataMaskingOutputReference",
    "ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams",
    "ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsList",
    "ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference",
    "ApiManagementApiDiagnosticFrontendRequestOutputReference",
    "ApiManagementApiDiagnosticFrontendResponse",
    "ApiManagementApiDiagnosticFrontendResponseDataMasking",
    "ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders",
    "ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersList",
    "ApiManagementApiDiagnosticFrontendResponseDataMaskingHeadersOutputReference",
    "ApiManagementApiDiagnosticFrontendResponseDataMaskingOutputReference",
    "ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams",
    "ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsList",
    "ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference",
    "ApiManagementApiDiagnosticFrontendResponseOutputReference",
    "ApiManagementApiDiagnosticTimeouts",
    "ApiManagementApiDiagnosticTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__db95a2bb470a01d6be674f3513f2ee9b6e5796b041dd63f667024a745ae9e2ca(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_management_logger_id: builtins.str,
    api_management_name: builtins.str,
    api_name: builtins.str,
    identifier: builtins.str,
    resource_group_name: builtins.str,
    always_log_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backend_request: typing.Optional[typing.Union[ApiManagementApiDiagnosticBackendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    backend_response: typing.Optional[typing.Union[ApiManagementApiDiagnosticBackendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_request: typing.Optional[typing.Union[ApiManagementApiDiagnosticFrontendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_response: typing.Optional[typing.Union[ApiManagementApiDiagnosticFrontendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    http_correlation_protocol: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_client_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operation_name_format: typing.Optional[builtins.str] = None,
    sampling_percentage: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementApiDiagnosticTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    verbosity: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__5e8faac6b6a7e073240dd69adb1b25de23a8388a6374f527d78bfe8a868c6ed6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94eb3d3101dd74b24f24b40c36150833a19ccbaa642b39cb022a6fb8f545811e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148d383f1b7f129a56238d42ddf1fefa12254cb19b697bc17c4a5350f16e0253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e10dc0219d222aa551d4a2bd5bcf732221b1e7b754cbb7926aebc255621703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08897ff8c5424afe4c907e3de405b86500c87fec58ef44146e6a609e30d5efb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637c70c9abd3bd7eadaf98da9307544b31da390195e046ae5ef43e3e1c143898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29404bc38749a3dfd2e55c1fcada4882dc85d6668b38e603927579a1bc9c5cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffa368dbe0f3e4c70519451dafaf7da71c2b9b312b485972fbd8812ceb584c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc6b6fc9e836c5f67020b9b97759545af79f306556e89e7f639ad9eb20184b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7265567df0d4275593d7d93dd847a1b23b25b2cee620f35ed508b6bce568e3a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee79612d2206c1c33b1c7ec40c74aedc086f7eeb1fc12c0ea8fe83a6194a757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32142e0c8b09694db669e705641e41573887866ed765261f823df6066af85abb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58d153b89c7165a2ff680e665f07d962eb7a0733b6d58809ea027692bd57f47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06260e3e1c660b850b91db9a17156a4c16bb22af85490365ad7891f0acd0f9cb(
    *,
    body_bytes: typing.Optional[jsii.Number] = None,
    data_masking: typing.Optional[typing.Union[ApiManagementApiDiagnosticBackendRequestDataMasking, typing.Dict[builtins.str, typing.Any]]] = None,
    headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b071e89261f2ec92452d1bc052413e682e23e87d4c64bfc4cf54fa845c3c8462(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640d78506755a8ba9b2029071353cb6ece01ad5287d75aed87275c381aadaf77(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db8b8706230f587fb733598f5c0c6756f0036891c44fb1f782cf5a5844e097f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874b6dc22d784c6ebc08ed0dfc328c03958ade1a4c5dcc96a6a05488b3014c68(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3320fb11b74958db2d3e0028ae37754e717b2be10a8ad07a587c7d8b9de47d90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df894f068daeed9b3f58a3f1846322d75d80161a791310d25eb2a806abddfbbc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a9825b4496efaa4f2d71ca805bfdc52f6f237815a69c604ec43e9b8d23c2bb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bda963a2206c153b8688860c5e94d74bde35d7465facdc9c05396bd2455644(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c77701e4a7149dedaaf2d56bbb6044e79cde3f8dbe38fa0465cfe99b622434(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65b1974b92d505ab885878db2c6cf1038498175ca9775e0896f27f5cf944de4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07109c92481ebc02551e8382916c0b27a4a32689b5a928b3a68ae495e35b10c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f916f26e72eefbf99f9d15a873bf5243a278e77bc23787e8af4b33134942fb6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7404654c263cd48d5f2f4daa2d8c901eaa4a1e31addc90238230d32aec64a02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d786c51882e58983f6a238fe33331c7eb3f088eba196b611e1a3fee9765eba8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383a8c518525762a366f55df7af6edff9f61d1db86adbd2a8606f7e943a97b98(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408b32cb66476d636a77c41ad1cf00151cba99b52de419b8232fb995c8673f6c(
    value: typing.Optional[ApiManagementApiDiagnosticBackendRequestDataMasking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048b93cae3e7a7ebfe620703a9319675e9b922bd1206fd933a674f387713f60d(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b13e1b51cffb5e0719f9e6c583e4c19b0b71e10b3e67a2a73118aa54d93ea1f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18454ddf73290c31c69a4245e8cb8d3098fab992f9689623e3a4c2c1fa1a3cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3c9ed553c01ae8f558a65bf2fe6a244e82b5204915236b10f18ceb7387cfb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19849d8270c1338785aad20ce29ae228746cc66503f2a133e92217a12c451369(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185631156f947126c2c1cc045fb6d81a4e4c1ef3cef94206dbaa113dfc7c78eb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1535038dbbe5c84549f4439bae019cdd1ee4d43012c45030abe330c3dfc0bf19(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20b29e87dbe632ed79c9c47c790e40706349d290abd2c1f95d1b280dad02a39(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59af17e6fd6a93ba044f3ed2d370f5a7bda93952faf30364a890456262400d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6855aba43969296b0b8118604e1a5c3f380b4c1aa7a8afd5b644c234e19b5f59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd47f1389ec60d9644f6579e87e5199f7a0269915d383221de66ac2bc2885e3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendRequestDataMaskingQueryParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbb18c4302e677e66b4b7b68cce45d0616494a0ea4afc5095794db16a2f1dc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2893a24a4e5775a7bed5d99a1fc73e56dfc0f03f5f277607673d427b50c5091(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6c7a072fa729055f270aa147ebc544b17a4685ad393b9aa4854f717678942d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cbd2f8c5f4918082e8812802d741ecc609b444f71b38532908ca42fc7992a2(
    value: typing.Optional[ApiManagementApiDiagnosticBackendRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dd607d79aaecc47549f0b8b61ad70bbfe3b9fd4a60a3bd11afd7adde77cbee(
    *,
    body_bytes: typing.Optional[jsii.Number] = None,
    data_masking: typing.Optional[typing.Union[ApiManagementApiDiagnosticBackendResponseDataMasking, typing.Dict[builtins.str, typing.Any]]] = None,
    headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03314da5eabba0e7383d55977b2f6ef09a203cc0c44db11937207a55fb50f5ee(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89f38e7b17a3ba9fffe17f348b3e59dd61d23ead5cb620174a8f81c40ab01b27(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5281b00035d66f42191d8edc121fa56156518e4b683594dd7a6c2ce7c479f452(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc4780c940e927901975a616ad570ef2a95091889eac272d893fb5bb3645dec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802294b039672329acfa0cee39b8ee5065f91e228305bc3036a5b9149e022007(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e397a8150b00675fd38ba7e821f72cd90189c8872e684af68d8796accaf1120(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501e0c7e0b5e699f2579dad363d60d9cee048c87148479a0ee8689629ddcc451(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32296493a24961089b787dcc34d05cbf15db52457c089beb21f2c6f464000d20(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a532838c3a7eabbc2560b6690d60758377d2762f4a71b19448d089a97758ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1144482cb677cac9bf236c47128a32f4304588a2f996e5d6b494d659f2bc87ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267a38188419c12f29d31cb9c1664040fba44df2c7c3f6cfb67a5f1b4cc18d36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3465ef2c26d8cb721e6ba5930751ba36ed0344dea9ba735005c537fa3a29a5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8a125b9712d5ea98edce8e01fc8b33ddaf87a250fdee7ddfb759a10794c2d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a6d891fe9b92c2089aff3458eac956638042bc038f7f824743bf859887d577(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__298308bc5962a3d92aab09f347535d48cf642386edffabfd0185c4a604a18d81(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc7b102f5f15a3fdfce7fd3eaabdc63956f0fc3316361898bace1187370710f(
    value: typing.Optional[ApiManagementApiDiagnosticBackendResponseDataMasking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff07c2617748af8ada4032ac2bfaedba2e5c21eeedb19153198d178ea19b9c99(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2641026760f029c0995affb811f25177fa79ae4466f72d3e2e4937ee133d2083(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce625f808624f0c2a5334e555be82e29da710620a4cf0a2be7bb81c32c832d4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865609add8a932aeadfafce3360511eccb0c85b0c56d30b747adae3e536c8c29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c48beb1342d39a311e69d33bb5a044da92c995d7d1516310fd403b119621fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a97d69cefd16d30e56b4a4be69b45e149824ead53c13d8e041b228c8cea50fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c224c4c5ef7a552b5ee4928481cb01ccec3b3da1fd960f70486c146fd33a7fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bd4b9edef2d8b3ac427ade246d34d022d4051f30b92878c7255b11baae1639(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b719c9bfea079dcbc1d0550dd27acc39799776b6d0ba73e7603f1f16ea56ccd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59630cac74ef4454a1ea58c7ffb47ae167b27b664c7533f7396788d5b1cf5b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39ef1822a08c540201a3ef0052d356d3678b146712ba8d808599563faf0a1ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticBackendResponseDataMaskingQueryParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb24e8083c17b452f34247da5eee17c0264b2fe9495bf553d4a15a75441fc8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afba268e5b632d8c256c98a1f11a557a283a48fdf119bca5d6bd544a802dbbf0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b586b03e068849c088ad89eec7b11f99d30e67c2a2dcc9f0a2d48e5c0e8896ba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5b46c4dc77b3201fd903e5b3548515d65730f7fd873ca1bd56940317bd2150(
    value: typing.Optional[ApiManagementApiDiagnosticBackendResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95d977fdfd0739cfb51f2689fb5963789929a273bde8f8380a9af98f0d35d7e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_management_logger_id: builtins.str,
    api_management_name: builtins.str,
    api_name: builtins.str,
    identifier: builtins.str,
    resource_group_name: builtins.str,
    always_log_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backend_request: typing.Optional[typing.Union[ApiManagementApiDiagnosticBackendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    backend_response: typing.Optional[typing.Union[ApiManagementApiDiagnosticBackendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_request: typing.Optional[typing.Union[ApiManagementApiDiagnosticFrontendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_response: typing.Optional[typing.Union[ApiManagementApiDiagnosticFrontendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    http_correlation_protocol: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_client_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operation_name_format: typing.Optional[builtins.str] = None,
    sampling_percentage: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementApiDiagnosticTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    verbosity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85920ed057cc9ba8fc783694ac7a254bb45b7a60b65792a4692e2fb42c074428(
    *,
    body_bytes: typing.Optional[jsii.Number] = None,
    data_masking: typing.Optional[typing.Union[ApiManagementApiDiagnosticFrontendRequestDataMasking, typing.Dict[builtins.str, typing.Any]]] = None,
    headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__084bd8c5a629638424a361777f3373b72fb0c68d1e4261d3aad189f639a04f76(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34f6cc788d534c4b11e6057e1364223144b2a8cede095c941b21aab984a1e98(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5603519613c98ecea20b613574674f62a8298496da64de8ed415c181edac68c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63485909d6ab86b760043141dc240d98d0136011ba32bf171097f43b27cf35a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64d4affcd7f6ddc17c72348faa03312d102f3422b914425f7fc3475da609586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41247734249afe1a047bcdfe545dc7bc08550fcfcde66af178d9714ab06f96ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08341e165609e52aa1fb94d29af763857b428b26dc8ce3f344741fdae6db7b0c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65069b0864b1ca49bd3bdf019b2216a8da0fa5f9bb3164df25ae6a03f3b1ce1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f13a9138c89b18ec12543225c149e4fe6a77e2a9341cd1036ad9d29c8260c4fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__974d0657a706410e99af17a0d6baa63bcec500f038499e529bc6c817de6f5de0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f5b5ad60a931f28766afde2bd562defbd57d4a0d49c558070198c5e441d208a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00c523fc9beef0a57ff039675681ed050d7d57355318f67facace858c1c38f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d367bd0463d68047e65b0cea7620a78261fc67129190c0f5c4819760db9f8fd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bbf6ac305c3f3ae3ffa5b73c0f007e1de2515b9a088f58ae2333971a39be0ef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cd3a39f3f18de43c7ce826517ac8c48a9488f15dd6f84e575f47d65b523258(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b17cf78ee54757bb789b92a25684f0e7fcb27d6c3567d86808e26069831237(
    value: typing.Optional[ApiManagementApiDiagnosticFrontendRequestDataMasking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db78afe4d798eb8855b1e2db14b9502d2a34440bd335930598fa8e58a3113c5(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf1400844d6e91be10703fb500175728abc861053bb8ba4fac9f113c023d936(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4eb08ccc8810c78d7428b77566a469af11754e945451af68db6e16ef28eb743(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d262b962f02483ea92899c62222723a0b7370d4c17b246817525da9de31ce5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec17cceff91d8b9081f9af934bc3c63bcc08d71d9ff506dfb2e2175032fd9c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25446f97b0f82b1bbac62424217771644b5f46202ad595fa0d634454ec66984(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d0a82b2593685dbb2d73f645f344232712b5204bf6b8fad2cf44f3b48f0910(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6457ccb74e1100a038080f26b55802e43ed617b77e2059bc45ea4ee0dfc896(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae5fc361a3cb24467e20581d42b58261e05039ef5abfff1b2aeb56e676702cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051bfae3a9b585031adcad329715082d3424a7a5c9af2d86656f4791d403b7ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfc3627f67a5fa6d81d548fa8ca0668a2ef0c34848ff9bde7a4e85543b25c47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendRequestDataMaskingQueryParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bb38d13c500ce748947a8a2643825d748c978b5e2ad2ae326aacec6643f4994(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e1eb6d28d159e60ff32016d9dfa65c3e6f62f05222015f724e5bec3a7770c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c7e5abb1a23104c77efed2bd9e6235ce814227024e4d290b6474d14bfcfcf0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ecd7c23fa85877331881e1132c1b45e0f771504c7f0eb2a09c7d622397174d(
    value: typing.Optional[ApiManagementApiDiagnosticFrontendRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba0659224c33b821af16153708c6ca13b322cd15ede04f8fe7df7d557959ccc(
    *,
    body_bytes: typing.Optional[jsii.Number] = None,
    data_masking: typing.Optional[typing.Union[ApiManagementApiDiagnosticFrontendResponseDataMasking, typing.Dict[builtins.str, typing.Any]]] = None,
    headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e5535bcfa600a9b27dac4e9c5442ff00a888b3b5d12c203c21f5973754279c(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde6ece82de1592c3b06cbf08e06daf34c8c4442d53a406b5f8ede52c0f27eee(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed04135dfa34ad33aabea57be42f45875a6153bb48ed579ef7d2a71e00bd2c43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b16de26e8769381f2b00310acedb8299d2284760615f4132cf040b3fa3864c9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07128a859693464fb94c9d63ff926153d1ddb2dcdd8a3468113f75346f0599f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf09a17977c963d8ecaf29b44617e5c3a1ce2b1dec51c5973605a286d98cd5f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357694f481a8e8ceba8a6b1743ffabfc23be2f5c6f88ff873f4e451f201aa00c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba83e0dd9a6936d6c3baf1658174394903810d429a36cc9cd942c3b1d2504af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c327b08b5b6daafd91c6cc22db63f65afa1a7fb262410a8af4c59090bce8fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029f77bd453147c34f0afcb6b203b918ec7d66564aba458a5d1d7a4df9abba48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae62182d388bbe9df2ff33149706b1fbf6fc37dd9e825cd044b85aa4fb55f758(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35e6ce27c34b6bde0b8a528bdac5038f355bf24610fdd4afa90ee0d67d34fa1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7807286f3fadd72ef28c4b89779bf0584b00b5a69476ea2fe70bf72e15ad9ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83a443b244d55aa036481d34be562f96028325bea24fbadf5d7e770a9390152(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd996b399ae23810390ec190259df3e44c207f5cf8d5f8fd65d9cdc8102646f8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bd54081ebf9ade698285d22d124ad539cca26b9f16b8698bf21e39283d60ea(
    value: typing.Optional[ApiManagementApiDiagnosticFrontendResponseDataMasking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514e82eb6fc932405d8a7f66cd0e74399e6841e8a6f9a22c21997bf5c9fe3618(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34415537d2049e7b7ff28522e06b062f8e4d71082179cc0daa51c0f452df4543(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c91938e64453fdf4e96363d935d44b6d5815827cac78b90e62dfff2726e35a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128c8732587bd7695c99895edbf0aa3ed40808c9411a0913709d5901e025e9d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23491ae0eb3341646d79cdad47beaf983cef0e4a0c95dea6f10c530872159dce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2154929b1fad8e83aae52fc9f0eccfc4c9ea5bb0545484e17f7aef629600ff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a05c17821c1b078d8ead70e417cbea68fa8489fa7fb30403b69eb0e3217cf65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960de71fd4981067f43ed9cf323481e56c0b02ca752e8b7481c17fa737dfb4f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2115c6f3a7997a051b7c5b14497371def53b6073944aa6d2747f227cc15275f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec3dddb4b0e6ec0943a54bb4d3dddadd0e39cb2f9574193602e57a9ac5222b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bf9723bb21d2c3ba0a66d880ba62e23ceafd35eb9b5fa3a800944e648a4844(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticFrontendResponseDataMaskingQueryParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24be1aeda1cccafea5c9d7609b8fc67da80c084a04bddc6fd98550c1ec17e9e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__245ff6952c67a5a09717a209c2142c2ddf51bf268ef5e34112ae734084db4721(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9f45b4a35fccc6c8bf7806c4663017b275a3191b056e78685690d884bda25d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c81f82936a0b8c4436417856e0ee7ed980255fe6dd5d900e1b2cc642fb29fa(
    value: typing.Optional[ApiManagementApiDiagnosticFrontendResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fbc888cf4b26152cfb11bc3b52f09c579fbefd90b41220eca3822c58d75a2f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013d20e750c5219a961ac58a939d00e8b51748ce3e01dc3361afe1ed6e058fd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cfd64ab07604fb67d80508c823c64e5e458a353e39901bba50dcaa2fcdc6fd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0baa062301c5b31c6a9266c74e435b9b5fab0f4982cdfd8f54194c6c774a8dad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a9bd2dd70185da1251e3824d0c670e6663fe578e46caefb0af0db40457bab21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cff914d20e63b9621ed264f5c9f3a88fcc36695b75012ec259027fe72fbabb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b471b32c66136c291371aef3c1c8641ada6525136a6ee01074d3166d515d0e0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementApiDiagnosticTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

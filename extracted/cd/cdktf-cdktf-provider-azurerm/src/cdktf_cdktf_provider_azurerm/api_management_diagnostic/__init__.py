r'''
# `azurerm_api_management_diagnostic`

Refer to the Terraform Registry for docs: [`azurerm_api_management_diagnostic`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic).
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


class ApiManagementDiagnostic(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnostic",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic azurerm_api_management_diagnostic}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_management_logger_id: builtins.str,
        api_management_name: builtins.str,
        identifier: builtins.str,
        resource_group_name: builtins.str,
        always_log_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_request: typing.Optional[typing.Union["ApiManagementDiagnosticBackendRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        backend_response: typing.Optional[typing.Union["ApiManagementDiagnosticBackendResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_request: typing.Optional[typing.Union["ApiManagementDiagnosticFrontendRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_response: typing.Optional[typing.Union["ApiManagementDiagnosticFrontendResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        http_correlation_protocol: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_client_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operation_name_format: typing.Optional[builtins.str] = None,
        sampling_percentage: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementDiagnosticTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        verbosity: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic azurerm_api_management_diagnostic} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_management_logger_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#api_management_logger_id ApiManagementDiagnostic#api_management_logger_id}.
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#api_management_name ApiManagementDiagnostic#api_management_name}.
        :param identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#identifier ApiManagementDiagnostic#identifier}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#resource_group_name ApiManagementDiagnostic#resource_group_name}.
        :param always_log_errors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#always_log_errors ApiManagementDiagnostic#always_log_errors}.
        :param backend_request: backend_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#backend_request ApiManagementDiagnostic#backend_request}
        :param backend_response: backend_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#backend_response ApiManagementDiagnostic#backend_response}
        :param frontend_request: frontend_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#frontend_request ApiManagementDiagnostic#frontend_request}
        :param frontend_response: frontend_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#frontend_response ApiManagementDiagnostic#frontend_response}
        :param http_correlation_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#http_correlation_protocol ApiManagementDiagnostic#http_correlation_protocol}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#id ApiManagementDiagnostic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_client_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#log_client_ip ApiManagementDiagnostic#log_client_ip}.
        :param operation_name_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#operation_name_format ApiManagementDiagnostic#operation_name_format}.
        :param sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#sampling_percentage ApiManagementDiagnostic#sampling_percentage}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#timeouts ApiManagementDiagnostic#timeouts}
        :param verbosity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#verbosity ApiManagementDiagnostic#verbosity}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b1922c39db2525d16960a97bdede5b8f80e268ec8cb31642ea86a64e7430d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApiManagementDiagnosticConfig(
            api_management_logger_id=api_management_logger_id,
            api_management_name=api_management_name,
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
        '''Generates CDKTF code for importing a ApiManagementDiagnostic resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ApiManagementDiagnostic to import.
        :param import_from_id: The id of the existing ApiManagementDiagnostic that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ApiManagementDiagnostic to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a2daadbc61e959ecbc104b0a1f7975d5daf4c3849cf66a478239b340dacd532)
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
        data_masking: typing.Optional[typing.Union["ApiManagementDiagnosticBackendRequestDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.
        '''
        value = ApiManagementDiagnosticBackendRequest(
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
        data_masking: typing.Optional[typing.Union["ApiManagementDiagnosticBackendResponseDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.
        '''
        value = ApiManagementDiagnosticBackendResponse(
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
        data_masking: typing.Optional[typing.Union["ApiManagementDiagnosticFrontendRequestDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.
        '''
        value = ApiManagementDiagnosticFrontendRequest(
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
        data_masking: typing.Optional[typing.Union["ApiManagementDiagnosticFrontendResponseDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.
        '''
        value = ApiManagementDiagnosticFrontendResponse(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#create ApiManagementDiagnostic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#delete ApiManagementDiagnostic#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#read ApiManagementDiagnostic#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#update ApiManagementDiagnostic#update}.
        '''
        value = ApiManagementDiagnosticTimeouts(
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
    def backend_request(self) -> "ApiManagementDiagnosticBackendRequestOutputReference":
        return typing.cast("ApiManagementDiagnosticBackendRequestOutputReference", jsii.get(self, "backendRequest"))

    @builtins.property
    @jsii.member(jsii_name="backendResponse")
    def backend_response(
        self,
    ) -> "ApiManagementDiagnosticBackendResponseOutputReference":
        return typing.cast("ApiManagementDiagnosticBackendResponseOutputReference", jsii.get(self, "backendResponse"))

    @builtins.property
    @jsii.member(jsii_name="frontendRequest")
    def frontend_request(
        self,
    ) -> "ApiManagementDiagnosticFrontendRequestOutputReference":
        return typing.cast("ApiManagementDiagnosticFrontendRequestOutputReference", jsii.get(self, "frontendRequest"))

    @builtins.property
    @jsii.member(jsii_name="frontendResponse")
    def frontend_response(
        self,
    ) -> "ApiManagementDiagnosticFrontendResponseOutputReference":
        return typing.cast("ApiManagementDiagnosticFrontendResponseOutputReference", jsii.get(self, "frontendResponse"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ApiManagementDiagnosticTimeoutsOutputReference":
        return typing.cast("ApiManagementDiagnosticTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="backendRequestInput")
    def backend_request_input(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticBackendRequest"]:
        return typing.cast(typing.Optional["ApiManagementDiagnosticBackendRequest"], jsii.get(self, "backendRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="backendResponseInput")
    def backend_response_input(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticBackendResponse"]:
        return typing.cast(typing.Optional["ApiManagementDiagnosticBackendResponse"], jsii.get(self, "backendResponseInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendRequestInput")
    def frontend_request_input(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticFrontendRequest"]:
        return typing.cast(typing.Optional["ApiManagementDiagnosticFrontendRequest"], jsii.get(self, "frontendRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="frontendResponseInput")
    def frontend_response_input(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticFrontendResponse"]:
        return typing.cast(typing.Optional["ApiManagementDiagnosticFrontendResponse"], jsii.get(self, "frontendResponseInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementDiagnosticTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ApiManagementDiagnosticTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d3c844c4f57e2141f48df90d3d5a3da96eed6c7d81b94e55433fc5dd6881804d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysLogErrors", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiManagementLoggerId")
    def api_management_logger_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementLoggerId"))

    @api_management_logger_id.setter
    def api_management_logger_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835ce427b79738d876be0af3a9c4a759e0fd9ed0955100a8a634f4029699ac98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementLoggerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiManagementName")
    def api_management_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementName"))

    @api_management_name.setter
    def api_management_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ca82cbac9e6b1e721e957675827441470b1a55a80093fcac104cb6cef85ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpCorrelationProtocol")
    def http_correlation_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpCorrelationProtocol"))

    @http_correlation_protocol.setter
    def http_correlation_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe3dcfd5f6c57728d8b45563c267630e87cf9f1bb196193efd9528e60f2799a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpCorrelationProtocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb1487bf02d229bd05ea382a30aa80a097c74c0d6771cbaeef8519175e17067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a8f81a36939b87a277196c0cf82d2fd328b1fbcc2ffd532d29dde240e7434d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67eb8e3a6e6a2e085b84544df6a773ed7214876ad603bcb90ad04c91972a544d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logClientIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operationNameFormat")
    def operation_name_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationNameFormat"))

    @operation_name_format.setter
    def operation_name_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cc97c51b2180ca05e62e5aedd17a5ab794ad208c72c19c72454abd9110ad409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationNameFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5b03fa70c27e3ddd807ac14ea83d14c91ff7e1ca45ec084c5eb77637aad59d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingPercentage")
    def sampling_percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingPercentage"))

    @sampling_percentage.setter
    def sampling_percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56074dc97e9ebccb3270e627e66a9a8270bbb44cce97311dfc52a0f0ad590f21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingPercentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verbosity")
    def verbosity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "verbosity"))

    @verbosity.setter
    def verbosity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a02ae47b549d33bd1ea59a5f7b076403b9d33bd021ac91da4fe653976339fc35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verbosity", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequest",
    jsii_struct_bases=[],
    name_mapping={
        "body_bytes": "bodyBytes",
        "data_masking": "dataMasking",
        "headers_to_log": "headersToLog",
    },
)
class ApiManagementDiagnosticBackendRequest:
    def __init__(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementDiagnosticBackendRequestDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.
        '''
        if isinstance(data_masking, dict):
            data_masking = ApiManagementDiagnosticBackendRequestDataMasking(**data_masking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3cf6e0f2c75a1e9e304a175874436c4e3dfaabf2cf0086135d1a0dd8b943e51)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.'''
        result = self._values.get("body_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_masking(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticBackendRequestDataMasking"]:
        '''data_masking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        '''
        result = self._values.get("data_masking")
        return typing.cast(typing.Optional["ApiManagementDiagnosticBackendRequestDataMasking"], result)

    @builtins.property
    def headers_to_log(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.'''
        result = self._values.get("headers_to_log")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticBackendRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestDataMasking",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "query_params": "queryParams"},
)
class ApiManagementDiagnosticBackendRequestDataMasking:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticBackendRequestDataMaskingHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticBackendRequestDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8464d633b799a9462b420ff1bb2f848fd71cd74afe1cc983d4b43f5db9dffad3)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendRequestDataMaskingHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendRequestDataMaskingHeaders"]]], result)

    @builtins.property
    def query_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendRequestDataMaskingQueryParams"]]]:
        '''query_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendRequestDataMaskingQueryParams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticBackendRequestDataMasking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestDataMaskingHeaders",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementDiagnosticBackendRequestDataMaskingHeaders:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c3ffe416865b4061faa4e25332849feb844bc9f0124657745c2b0099b1ab36)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticBackendRequestDataMaskingHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticBackendRequestDataMaskingHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestDataMaskingHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25ccdd6a12d836cbcd22a2f9452e43b748443f285a5ab9e94d32b74c4f38bc7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementDiagnosticBackendRequestDataMaskingHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241d8161638e4cdd0f481c2a88cfac7390a192b864edf7fa95f54c791d957faa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementDiagnosticBackendRequestDataMaskingHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75cdd7926639c84bf3415e1ef4d314b718ba258fe3d27baa20996dd3f2a8927a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12fe2afbdf7bc0ca925ffe4885959acc56793dba017161b2b5c697ba4eac6466)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f09e501cc7cbef620a3a4b40aed014c60d204a4ff79151066f20e70dfad299f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19cd985a482568da97431a6123b683135e744e44679c5c8b9c6690913be5e211)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticBackendRequestDataMaskingHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestDataMaskingHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d2362c1225a9e2fc401d3f9ec5b0d28f7c1d3ca720a3be71ec3cb7bb43859b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7822a9ea9b952a1920fcc4f8f90d90e5dd2e6c6543ddb1e85ba06255ffc962f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82726debc58370a31b111aede9340fb3444936d39ff2c0838fbb0aef73c93d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendRequestDataMaskingHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendRequestDataMaskingHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendRequestDataMaskingHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b2d27f7cfe041d9050f7ef8679af298ec9cb4583ddad7a19801783579312ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticBackendRequestDataMaskingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestDataMaskingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b3dc943ae85a37dfd15a7dfe7712703a9a5d8472be97618fd99881dada5b71c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91125a5254b9c5cfe8c413fb11593ae593b401c15d4134c03ae4cf449ec99850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParams")
    def put_query_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticBackendRequestDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9842ee7c80e83970089995a3ad35778952865ef55e7d262f36d4fcf51379ce)
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
    def headers(self) -> ApiManagementDiagnosticBackendRequestDataMaskingHeadersList:
        return typing.cast(ApiManagementDiagnosticBackendRequestDataMaskingHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(
        self,
    ) -> "ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsList":
        return typing.cast("ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsList", jsii.get(self, "queryParams"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendRequestDataMaskingQueryParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendRequestDataMaskingQueryParams"]]], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticBackendRequestDataMasking]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticBackendRequestDataMasking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementDiagnosticBackendRequestDataMasking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45bf9e021cd511d581271be9ff40235a29b1d6095344157500907e878e449d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestDataMaskingQueryParams",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementDiagnosticBackendRequestDataMaskingQueryParams:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a917bd607d2181cfaa59f8ac64a0d140c9694e5457219a2184502e27cd59dd35)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticBackendRequestDataMaskingQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c82e9103cebeb740d3a541d69646422cb8c06709e5bca7ce89a68a1f244ef09c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29e41a2d82c4c65a359b9161ea33c8c3bc13a36625d35b7f3b91a84a87c274b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db45bd621930be62d58d614908e561644ccc4843a5413cee90523536d934562)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6acdd638afda17aa40ad9a27079ee6de5d6d611ce2d456924774751b1dd13f12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3f1ece46636fdb9b7b21cad14796bca04047623427e4a7d2c4efe0329380494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingQueryParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingQueryParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingQueryParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee7034b88cca464a8f95987766ebfe7e31adfa8e2461461fb79409c7c839e65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__425fa036010c9921bc1b6ca12bb38b38b9c7d540b2e28781b43f3095e20fc08d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a64035cac94ee01f2d4686c09feb121656624f93e13df66ad3d836f60a77d4c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a20bfa03c5eab0c3e5cc4d1fdd40d4464d9c6a82f1284e28f90fdb9d1b93da59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendRequestDataMaskingQueryParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendRequestDataMaskingQueryParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendRequestDataMaskingQueryParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a741e23f0bbc2ceb21fb5f4179f71f2f9d6c795c1bb400426d9c4e219029c48e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticBackendRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8eeb433fb8b35d3ff91be78109dc1b5babb73d8b7be8d3737e3655662d00ace)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataMasking")
    def put_data_masking(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        value = ApiManagementDiagnosticBackendRequestDataMasking(
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
    ) -> ApiManagementDiagnosticBackendRequestDataMaskingOutputReference:
        return typing.cast(ApiManagementDiagnosticBackendRequestDataMaskingOutputReference, jsii.get(self, "dataMasking"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytesInput")
    def body_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bodyBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMaskingInput")
    def data_masking_input(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticBackendRequestDataMasking]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticBackendRequestDataMasking], jsii.get(self, "dataMaskingInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f5f94f6c87f1966ff6c7bd4bbf24e891cbbd83dc7d08b899dc62095b36f5e116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersToLog")
    def headers_to_log(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersToLog"))

    @headers_to_log.setter
    def headers_to_log(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a070271806316dc134407424bc6a9459c97cd5337e692b4918fa3d5555d948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersToLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementDiagnosticBackendRequest]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticBackendRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementDiagnosticBackendRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d92a1375f9d1809837fc51a44719d12a9118c92f1eefc5e0a8bde2241c432bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponse",
    jsii_struct_bases=[],
    name_mapping={
        "body_bytes": "bodyBytes",
        "data_masking": "dataMasking",
        "headers_to_log": "headersToLog",
    },
)
class ApiManagementDiagnosticBackendResponse:
    def __init__(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementDiagnosticBackendResponseDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.
        '''
        if isinstance(data_masking, dict):
            data_masking = ApiManagementDiagnosticBackendResponseDataMasking(**data_masking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39ce265bad9ae3b48826ae15ac08e88480f977a2ff5cb56a455bfa2318e2048d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.'''
        result = self._values.get("body_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_masking(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticBackendResponseDataMasking"]:
        '''data_masking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        '''
        result = self._values.get("data_masking")
        return typing.cast(typing.Optional["ApiManagementDiagnosticBackendResponseDataMasking"], result)

    @builtins.property
    def headers_to_log(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.'''
        result = self._values.get("headers_to_log")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticBackendResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseDataMasking",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "query_params": "queryParams"},
)
class ApiManagementDiagnosticBackendResponseDataMasking:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticBackendResponseDataMaskingHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticBackendResponseDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3ad2187cfe78560508ecfdd4d29e98743d771ce95e3941d1eee4ebeeaa6b8c)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendResponseDataMaskingHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendResponseDataMaskingHeaders"]]], result)

    @builtins.property
    def query_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendResponseDataMaskingQueryParams"]]]:
        '''query_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendResponseDataMaskingQueryParams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticBackendResponseDataMasking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseDataMaskingHeaders",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementDiagnosticBackendResponseDataMaskingHeaders:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a0f340c5dc395c9ca5789be6d781a87690ac4a4b6c13fd3c20470bc9c390e1)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticBackendResponseDataMaskingHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticBackendResponseDataMaskingHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseDataMaskingHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26d2fc59472358925a42d5364961be6b4bcc7d9bdd325dc1eda521c5f6726f1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementDiagnosticBackendResponseDataMaskingHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75fb61b833f0c952245e79979737c32da6b8a609775ca6ea0ab08750cad08426)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementDiagnosticBackendResponseDataMaskingHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4f355aa04dff5ee58ae00102c594e03d6bdef4e3740efb807c1f5c3c87156f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d05062ccc8ec02f77b66e0a36e15a16714cf57069dfff3d475ef7662fdbaca5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3b0fd486ada7fe952f649bc02f4e1aa7704292b5370f41917bceca5a04d9a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf3526f722dabea7139c3c2c5e6feaf5495886528dd8b8deb833dde51634aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticBackendResponseDataMaskingHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseDataMaskingHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70195050e16445459e18758577a3c1846e0103aaae75ce74ad7b23058c0d4d2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05c12a4957aa135113d2867c23d29c878ded5d8be9735f0f81aadfb265ade950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff4a91ce61f5a245809fc074325b6e4434af16e4bd1f5c884f813b9975172c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendResponseDataMaskingHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendResponseDataMaskingHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendResponseDataMaskingHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd76d39fd26c8c2d3ab7616b08d111150a5267a2c31bad8fd25b17271cf99ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticBackendResponseDataMaskingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseDataMaskingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a24c5aad7ab6cc341f856dc34543b5f2c13a98c2392ece402e4b2330e936a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98bb26afeca2754474564bba654cc6777d4a4f1c7aae0764469c4c7b59722c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParams")
    def put_query_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticBackendResponseDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdfdb691a88ca9ddf5034594aaea975d6aaa690d12e6e57e3425ff43a983e9ea)
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
    def headers(self) -> ApiManagementDiagnosticBackendResponseDataMaskingHeadersList:
        return typing.cast(ApiManagementDiagnosticBackendResponseDataMaskingHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(
        self,
    ) -> "ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsList":
        return typing.cast("ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsList", jsii.get(self, "queryParams"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendResponseDataMaskingQueryParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticBackendResponseDataMaskingQueryParams"]]], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticBackendResponseDataMasking]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticBackendResponseDataMasking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementDiagnosticBackendResponseDataMasking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fd2f5fb22a7d0745cc6e86313bc9ef1c53f89c008a7316d6faac8628d548cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseDataMaskingQueryParams",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementDiagnosticBackendResponseDataMaskingQueryParams:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea198b8ad723b3e144a365c884443a65909ac0b16ad22757556375e2043a31c1)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticBackendResponseDataMaskingQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b75faf892be0f5894a08b169845d69af500bfd76ff7de542ee4e86c7fd2bb14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42094ef22ba5939580eeafd669a18739030869882f8b65317d888ba9075e97e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1bb1bdfd169aefa06ea9cb79e11d5c600fc8fe421ec358d97b9c03732c66c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71c416850d297a69fb32023f3884f6e16b2a8bb832790d5f5e8b96109d3ec702)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d64915922d835a9dc92fe407f643860e3889be41ccfb62db612a797b2bad5660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingQueryParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingQueryParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingQueryParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa42bfec194ce7d274e3c4cc728030665cd81efedfef89c77e9236cc811b32d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dff9cd113b8d9ce43a3c2cb5bf30350e0d6a8e2d9fcfff6a8aab676f1bfd3e0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6dd493e952231521d603efd5b9b21595e2b7b5373ea6158b84e703f5e4dbddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793274c1529ec8e69e5b24f9d1dca9ca7578a167d29a1008aebf0cd116253450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendResponseDataMaskingQueryParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendResponseDataMaskingQueryParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendResponseDataMaskingQueryParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7daaf9eba33a15a3e146cf47664b2a79bcc3637c56e806ae49e6cf10584a2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticBackendResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticBackendResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c08bf66b78aff830c912382d1a3eab8097505d5cbf8ea7838d0e76a19e9292a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataMasking")
    def put_data_masking(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        value = ApiManagementDiagnosticBackendResponseDataMasking(
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
    ) -> ApiManagementDiagnosticBackendResponseDataMaskingOutputReference:
        return typing.cast(ApiManagementDiagnosticBackendResponseDataMaskingOutputReference, jsii.get(self, "dataMasking"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytesInput")
    def body_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bodyBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMaskingInput")
    def data_masking_input(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticBackendResponseDataMasking]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticBackendResponseDataMasking], jsii.get(self, "dataMaskingInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__21ea1bbc81fe7b67c689a4f1aad7cfd3048f212258e08336a1a3d77202710e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersToLog")
    def headers_to_log(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersToLog"))

    @headers_to_log.setter
    def headers_to_log(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fdcea01bae15a022cdd69f02be4497cd70c1278de747b5c5fba13a1d890774)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersToLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementDiagnosticBackendResponse]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticBackendResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementDiagnosticBackendResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a5c1bda9e501852a1b2923791b342ea248f0606830fb43160d2b1edea0e86c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticConfig",
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
class ApiManagementDiagnosticConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        identifier: builtins.str,
        resource_group_name: builtins.str,
        always_log_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        backend_request: typing.Optional[typing.Union[ApiManagementDiagnosticBackendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
        backend_response: typing.Optional[typing.Union[ApiManagementDiagnosticBackendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_request: typing.Optional[typing.Union["ApiManagementDiagnosticFrontendRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend_response: typing.Optional[typing.Union["ApiManagementDiagnosticFrontendResponse", typing.Dict[builtins.str, typing.Any]]] = None,
        http_correlation_protocol: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_client_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        operation_name_format: typing.Optional[builtins.str] = None,
        sampling_percentage: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["ApiManagementDiagnosticTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param api_management_logger_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#api_management_logger_id ApiManagementDiagnostic#api_management_logger_id}.
        :param api_management_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#api_management_name ApiManagementDiagnostic#api_management_name}.
        :param identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#identifier ApiManagementDiagnostic#identifier}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#resource_group_name ApiManagementDiagnostic#resource_group_name}.
        :param always_log_errors: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#always_log_errors ApiManagementDiagnostic#always_log_errors}.
        :param backend_request: backend_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#backend_request ApiManagementDiagnostic#backend_request}
        :param backend_response: backend_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#backend_response ApiManagementDiagnostic#backend_response}
        :param frontend_request: frontend_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#frontend_request ApiManagementDiagnostic#frontend_request}
        :param frontend_response: frontend_response block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#frontend_response ApiManagementDiagnostic#frontend_response}
        :param http_correlation_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#http_correlation_protocol ApiManagementDiagnostic#http_correlation_protocol}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#id ApiManagementDiagnostic#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_client_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#log_client_ip ApiManagementDiagnostic#log_client_ip}.
        :param operation_name_format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#operation_name_format ApiManagementDiagnostic#operation_name_format}.
        :param sampling_percentage: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#sampling_percentage ApiManagementDiagnostic#sampling_percentage}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#timeouts ApiManagementDiagnostic#timeouts}
        :param verbosity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#verbosity ApiManagementDiagnostic#verbosity}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(backend_request, dict):
            backend_request = ApiManagementDiagnosticBackendRequest(**backend_request)
        if isinstance(backend_response, dict):
            backend_response = ApiManagementDiagnosticBackendResponse(**backend_response)
        if isinstance(frontend_request, dict):
            frontend_request = ApiManagementDiagnosticFrontendRequest(**frontend_request)
        if isinstance(frontend_response, dict):
            frontend_response = ApiManagementDiagnosticFrontendResponse(**frontend_response)
        if isinstance(timeouts, dict):
            timeouts = ApiManagementDiagnosticTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2495fdab480b2d6f09e213943c9f73150ce26ae4c191e62937445eff18657f39)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_management_logger_id", value=api_management_logger_id, expected_type=type_hints["api_management_logger_id"])
            check_type(argname="argument api_management_name", value=api_management_name, expected_type=type_hints["api_management_name"])
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#api_management_logger_id ApiManagementDiagnostic#api_management_logger_id}.'''
        result = self._values.get("api_management_logger_id")
        assert result is not None, "Required property 'api_management_logger_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_management_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#api_management_name ApiManagementDiagnostic#api_management_name}.'''
        result = self._values.get("api_management_name")
        assert result is not None, "Required property 'api_management_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#identifier ApiManagementDiagnostic#identifier}.'''
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#resource_group_name ApiManagementDiagnostic#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_log_errors(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#always_log_errors ApiManagementDiagnostic#always_log_errors}.'''
        result = self._values.get("always_log_errors")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def backend_request(self) -> typing.Optional[ApiManagementDiagnosticBackendRequest]:
        '''backend_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#backend_request ApiManagementDiagnostic#backend_request}
        '''
        result = self._values.get("backend_request")
        return typing.cast(typing.Optional[ApiManagementDiagnosticBackendRequest], result)

    @builtins.property
    def backend_response(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticBackendResponse]:
        '''backend_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#backend_response ApiManagementDiagnostic#backend_response}
        '''
        result = self._values.get("backend_response")
        return typing.cast(typing.Optional[ApiManagementDiagnosticBackendResponse], result)

    @builtins.property
    def frontend_request(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticFrontendRequest"]:
        '''frontend_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#frontend_request ApiManagementDiagnostic#frontend_request}
        '''
        result = self._values.get("frontend_request")
        return typing.cast(typing.Optional["ApiManagementDiagnosticFrontendRequest"], result)

    @builtins.property
    def frontend_response(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticFrontendResponse"]:
        '''frontend_response block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#frontend_response ApiManagementDiagnostic#frontend_response}
        '''
        result = self._values.get("frontend_response")
        return typing.cast(typing.Optional["ApiManagementDiagnosticFrontendResponse"], result)

    @builtins.property
    def http_correlation_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#http_correlation_protocol ApiManagementDiagnostic#http_correlation_protocol}.'''
        result = self._values.get("http_correlation_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#id ApiManagementDiagnostic#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_client_ip(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#log_client_ip ApiManagementDiagnostic#log_client_ip}.'''
        result = self._values.get("log_client_ip")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def operation_name_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#operation_name_format ApiManagementDiagnostic#operation_name_format}.'''
        result = self._values.get("operation_name_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sampling_percentage(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#sampling_percentage ApiManagementDiagnostic#sampling_percentage}.'''
        result = self._values.get("sampling_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ApiManagementDiagnosticTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#timeouts ApiManagementDiagnostic#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ApiManagementDiagnosticTimeouts"], result)

    @builtins.property
    def verbosity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#verbosity ApiManagementDiagnostic#verbosity}.'''
        result = self._values.get("verbosity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequest",
    jsii_struct_bases=[],
    name_mapping={
        "body_bytes": "bodyBytes",
        "data_masking": "dataMasking",
        "headers_to_log": "headersToLog",
    },
)
class ApiManagementDiagnosticFrontendRequest:
    def __init__(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementDiagnosticFrontendRequestDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.
        '''
        if isinstance(data_masking, dict):
            data_masking = ApiManagementDiagnosticFrontendRequestDataMasking(**data_masking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d88236074e3be0cdd2050aab28a4c3a6724d502acad32f8570362ae73b1d956)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.'''
        result = self._values.get("body_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_masking(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticFrontendRequestDataMasking"]:
        '''data_masking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        '''
        result = self._values.get("data_masking")
        return typing.cast(typing.Optional["ApiManagementDiagnosticFrontendRequestDataMasking"], result)

    @builtins.property
    def headers_to_log(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.'''
        result = self._values.get("headers_to_log")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticFrontendRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestDataMasking",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "query_params": "queryParams"},
)
class ApiManagementDiagnosticFrontendRequestDataMasking:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticFrontendRequestDataMaskingHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052f729fa296d06256da75dffdc3908dd8298e0a6ffd166390f3a14a944f238e)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendRequestDataMaskingHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendRequestDataMaskingHeaders"]]], result)

    @builtins.property
    def query_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams"]]]:
        '''query_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticFrontendRequestDataMasking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestDataMaskingHeaders",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementDiagnosticFrontendRequestDataMaskingHeaders:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3c97ed64c57b2e9048f7794cffc16d73779ea0aca911576c98855e0c432000)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticFrontendRequestDataMaskingHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticFrontendRequestDataMaskingHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestDataMaskingHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26ceadcb98423587c9cebc790592d86b9d0ac10b10a69a529695a115fac33558)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementDiagnosticFrontendRequestDataMaskingHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a78b299f894822af56e9b390e0c964934c4d959e4727286e6acd1414892cb1e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementDiagnosticFrontendRequestDataMaskingHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940ba840481c1f6e1c4235fd5ea46ec6b8114144956d6b60404b99a04b9b293a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__723d821625389fbe4480163323b32ecacf95bb8b7c2c8882b4bebae594783ab4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d93645ae134f3a8105e921cbaafd4dbcc54d4d2d2b9542c5f7af4f5986a875aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30ef486c34077ec75ad849fdf8b6f98742c1e3b35bd94cc8bba878d3477f9bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticFrontendRequestDataMaskingHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestDataMaskingHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a34f52e530eaa4e07870d96655541b7135a0db9f29ffc5f77fcdf0872119bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab3e3adbef9d944ecfaabc30e6a7402d66fb6580e3f2beb8086e5b52c2261a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db30d0332b5a15e90fe1d4175efeb759241cc7283c26a78a2264305865ef2977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28eea5d6a493e9be14468fcd20e56dc1190aaf1c4af040f616623050e661b388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticFrontendRequestDataMaskingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestDataMaskingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2aa81133002681ec71e1ba591a1c495708cacdcfb882c602d632fe57ff70028d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24104229d83018ca37b57d95fca5459deab63446ecc258e3ad161a6dcd2ba110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParams")
    def put_query_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dae76c8a6df201d9b55ce0531be31e3a24f98975c7fd89b494577dac2639ceb)
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
    def headers(self) -> ApiManagementDiagnosticFrontendRequestDataMaskingHeadersList:
        return typing.cast(ApiManagementDiagnosticFrontendRequestDataMaskingHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(
        self,
    ) -> "ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsList":
        return typing.cast("ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsList", jsii.get(self, "queryParams"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams"]]], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticFrontendRequestDataMasking]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticFrontendRequestDataMasking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementDiagnosticFrontendRequestDataMasking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7480c53b7c650443dd9e446a36a3d1b61c0cbb13d06ab42a45d99867581ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e76f8ef536ec0aa9f428992571867ecf4592e58709ab0ddf8a1159fec8c7623)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__136f76ffab271d99064ac27311d30d803494b3a64189a65c454226b55c38cd8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd64bb106f4d4b4274d03164c6bc4094db20ea909b32eec448123694cc4c8088)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e44466e2ab768d30c088348c15e64b7b83f141237a893d4cd7bdd40179bf265)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0cb92fa73545dd8a55b44cbf79e8fb8505ee8b177dc7af93b69b4424e22d364)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c71a9e13ffd63fe4c72c45525dfb2f5f001407249e395b9e20e53eb5c2222625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f6ea1fc81884faebc1015a43454c2d581314349dc6a3f944bce3f4bb15ba97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aaa0f436f876254430a3b54392c0dd3fe15e9e788945ace6bf7441ab90e3cfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__831447d42fe53f44afb1b7ae8f382d8b16b8a20de372032da85484ef387cc9c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d3cba51d86d2718057f953f7c877cc643a472cb74e7a8f4b8ddb0ac3e6b342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ec27a5dc6cc4ad977c20c5b84f0bb02d3c47e17baf23e04b093c2c84556b261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticFrontendRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8effd2ea4eb16d3cbb9b11c091c6fa598fa44eea530cc7fe592b0fb490167c56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataMasking")
    def put_data_masking(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        value = ApiManagementDiagnosticFrontendRequestDataMasking(
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
    ) -> ApiManagementDiagnosticFrontendRequestDataMaskingOutputReference:
        return typing.cast(ApiManagementDiagnosticFrontendRequestDataMaskingOutputReference, jsii.get(self, "dataMasking"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytesInput")
    def body_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bodyBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMaskingInput")
    def data_masking_input(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticFrontendRequestDataMasking]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticFrontendRequestDataMasking], jsii.get(self, "dataMaskingInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7ee685925a779c949e3291253833265a513ca29f9aac91afaaa3ae74e11d5a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersToLog")
    def headers_to_log(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersToLog"))

    @headers_to_log.setter
    def headers_to_log(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a66e882ef66d02400079ec652d931ee677ac2b6e9374b1113f2782aade10949)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersToLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ApiManagementDiagnosticFrontendRequest]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticFrontendRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementDiagnosticFrontendRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42dfdc9391a6211727f9c6d5c28ad937939f2e266bcab6b734709a34b4d3a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponse",
    jsii_struct_bases=[],
    name_mapping={
        "body_bytes": "bodyBytes",
        "data_masking": "dataMasking",
        "headers_to_log": "headersToLog",
    },
)
class ApiManagementDiagnosticFrontendResponse:
    def __init__(
        self,
        *,
        body_bytes: typing.Optional[jsii.Number] = None,
        data_masking: typing.Optional[typing.Union["ApiManagementDiagnosticFrontendResponseDataMasking", typing.Dict[builtins.str, typing.Any]]] = None,
        headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param body_bytes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.
        :param data_masking: data_masking block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        :param headers_to_log: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.
        '''
        if isinstance(data_masking, dict):
            data_masking = ApiManagementDiagnosticFrontendResponseDataMasking(**data_masking)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c2d602882615b2cacdfc02a04d8257d2114df17d1427c164f9d9cbd3ab45f3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#body_bytes ApiManagementDiagnostic#body_bytes}.'''
        result = self._values.get("body_bytes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data_masking(
        self,
    ) -> typing.Optional["ApiManagementDiagnosticFrontendResponseDataMasking"]:
        '''data_masking block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#data_masking ApiManagementDiagnostic#data_masking}
        '''
        result = self._values.get("data_masking")
        return typing.cast(typing.Optional["ApiManagementDiagnosticFrontendResponseDataMasking"], result)

    @builtins.property
    def headers_to_log(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers_to_log ApiManagementDiagnostic#headers_to_log}.'''
        result = self._values.get("headers_to_log")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticFrontendResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseDataMasking",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "query_params": "queryParams"},
)
class ApiManagementDiagnosticFrontendResponseDataMasking:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticFrontendResponseDataMaskingHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ade6eb62525ba60d8c6ea9b1b83d917ab52f3c45601544b1da7955943b2f33)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendResponseDataMaskingHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendResponseDataMaskingHeaders"]]], result)

    @builtins.property
    def query_params(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams"]]]:
        '''query_params block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        result = self._values.get("query_params")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticFrontendResponseDataMasking(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseDataMaskingHeaders",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementDiagnosticFrontendResponseDataMaskingHeaders:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3bd6876e7b917cf52a042121c437c746c2d748a7854008912e78373c398bcc1)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticFrontendResponseDataMaskingHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticFrontendResponseDataMaskingHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseDataMaskingHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3186b0b9b252fe14bef7daed6414cee99c35eb7189ac4c5eb51b17962939b3ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementDiagnosticFrontendResponseDataMaskingHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325bc0d5f8b03b44c5c194841649848ffe3d202040ac4b41d2d4c8e6bcde80cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementDiagnosticFrontendResponseDataMaskingHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523b89480444ff2bdb55a85d0c5967622ac50bc527a8cd8f20ad1c89fe5ac9e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__661c8165ac372eb517e5a697ec9c6321c7c8e3a6739084f48b731cdbef5d2159)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d01c9b8c6d036cb827d057df9289887dad0f911ce5e04d0ab6074b29a5403b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361ed0556f887c8a103d48dcef1e15a9cae76fe1b829a0a2c95ded54abd0e23d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticFrontendResponseDataMaskingHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseDataMaskingHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__773676990ed650e5a7fed5c8807da878cc3968e51db32fec72cd1dd61e93d03d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b77b73bcd99343591302fcadb806cfb4fc12d3d54c4e7ff0668f4923ff1e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f20069a8a85306e7780dc9a181a7d84b82d81a27ed6269c2fed7c358a9e5f82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9c3b310701476226cf3532ac5292e31b19b3eed9081e7e2bbb8fa8d647b3553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticFrontendResponseDataMaskingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseDataMaskingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b48b34429908ae315515ea4aa1011498bd6940a90a36a2b8e787d134234914e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897e3951035ad9b9367eaefd8885db9018bd07fc696c53b473730bbe8844d4a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParams")
    def put_query_params(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b491d8f8e038f538b6d64e91f9d38b8b869678c03074cd0658b2347dcc1f94)
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
    def headers(self) -> ApiManagementDiagnosticFrontendResponseDataMaskingHeadersList:
        return typing.cast(ApiManagementDiagnosticFrontendResponseDataMaskingHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParams")
    def query_params(
        self,
    ) -> "ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsList":
        return typing.cast("ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsList", jsii.get(self, "queryParams"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParamsInput")
    def query_params_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams"]]], jsii.get(self, "queryParamsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticFrontendResponseDataMasking]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticFrontendResponseDataMasking], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementDiagnosticFrontendResponseDataMasking],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64530676d35a72e41608e7ffe29e904412f8fd8b3292d19851afb21926bf4edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "value": "value"},
)
class ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams:
    def __init__(self, *, mode: builtins.str, value: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cdbb92ab8cb7823612dffe25581b2210db8136e48f78e2c36f1b6a77c886962)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
            "value": value,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#mode ApiManagementDiagnostic#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#value ApiManagementDiagnostic#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01b437a159e7ae6455559576fff61d1d46315d61b5a71c476aba4ce2144c55f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ddb375c18c1cdd555b5d505d470c091e6f39aab89eb619409f9bb3a1d2e04d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9db1f061def14e63c2b1e9aaf5457f72146a402b92f16373cad85475db1bd8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51c05742dc7768a7380309f1bac0d95f2e3e5004b34f476446f9cfcd23deba92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b79a9eb52381e148afada21796c42a0dc31f2cf81391bf7efa838255524bb836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4183f44bdf457aa4db00d85bf1c0bd65832810c868e52e1dd1ff2ffa22c811)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__015738bea66f1d3621ebb54475a48d6fcd2165b1bfe52c41575807e506a184d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63dc41a384d26318817c49d703e8a67101be3c862312e7a8aa8f8eb5d44a0f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82610cf931cd764fb50ea884e7cf42fb8c2bace5cb7898910373ed4204e08902)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a171548e1b384748987d9e48e12fae4f40f4a65348c50ec96c819e3e65fe9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ApiManagementDiagnosticFrontendResponseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticFrontendResponseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1db941e50880967e3b09d696f9753381863ba428fb88ad10aaae4bc056a576cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDataMasking")
    def put_data_masking(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#headers ApiManagementDiagnostic#headers}
        :param query_params: query_params block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#query_params ApiManagementDiagnostic#query_params}
        '''
        value = ApiManagementDiagnosticFrontendResponseDataMasking(
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
    ) -> ApiManagementDiagnosticFrontendResponseDataMaskingOutputReference:
        return typing.cast(ApiManagementDiagnosticFrontendResponseDataMaskingOutputReference, jsii.get(self, "dataMasking"))

    @builtins.property
    @jsii.member(jsii_name="bodyBytesInput")
    def body_bytes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bodyBytesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataMaskingInput")
    def data_masking_input(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticFrontendResponseDataMasking]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticFrontendResponseDataMasking], jsii.get(self, "dataMaskingInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fb5718acaa9453781d867b0fbbddefe930cf55120b0cd25501389c5b670006d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bodyBytes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="headersToLog")
    def headers_to_log(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "headersToLog"))

    @headers_to_log.setter
    def headers_to_log(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e58792319c815e94072b32a5fb263f8dbfd99acd4a5bf54eb22556a9459505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "headersToLog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ApiManagementDiagnosticFrontendResponse]:
        return typing.cast(typing.Optional[ApiManagementDiagnosticFrontendResponse], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ApiManagementDiagnosticFrontendResponse],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65c1466e28cf1a1dbdf77e7e78d674bac99541ac56bce580116c1144802856a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ApiManagementDiagnosticTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#create ApiManagementDiagnostic#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#delete ApiManagementDiagnostic#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#read ApiManagementDiagnostic#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#update ApiManagementDiagnostic#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32fafc6382ca030494d72ec042d9f66c4e94abf98b46d40adc45890c79470e0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#create ApiManagementDiagnostic#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#delete ApiManagementDiagnostic#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#read ApiManagementDiagnostic#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/api_management_diagnostic#update ApiManagementDiagnostic#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiManagementDiagnosticTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApiManagementDiagnosticTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.apiManagementDiagnostic.ApiManagementDiagnosticTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e87fa1e5c95893d2b3a965da0d3eb24ea37a3628556d7f737212bd87cc079e0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74ca24f3944613ce3f89fe53598701b17c0bb67435bc195407ca2b8668e3a7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__521f238fc2e66c42cf1b16a5b583bfd0ef8e35d805e0f1ac458e47f92c08efe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96512dc0e688ef777c28c5496065160f3d43eb20dd36df577d2fffe9e7d168ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f276b586dba8e5a61c86f13982026082d7ae986a42a55a119089f61a6ce53ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9369ed990ab6f50cb6348ef3812405d786b51ce56986070c939db45351879b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ApiManagementDiagnostic",
    "ApiManagementDiagnosticBackendRequest",
    "ApiManagementDiagnosticBackendRequestDataMasking",
    "ApiManagementDiagnosticBackendRequestDataMaskingHeaders",
    "ApiManagementDiagnosticBackendRequestDataMaskingHeadersList",
    "ApiManagementDiagnosticBackendRequestDataMaskingHeadersOutputReference",
    "ApiManagementDiagnosticBackendRequestDataMaskingOutputReference",
    "ApiManagementDiagnosticBackendRequestDataMaskingQueryParams",
    "ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsList",
    "ApiManagementDiagnosticBackendRequestDataMaskingQueryParamsOutputReference",
    "ApiManagementDiagnosticBackendRequestOutputReference",
    "ApiManagementDiagnosticBackendResponse",
    "ApiManagementDiagnosticBackendResponseDataMasking",
    "ApiManagementDiagnosticBackendResponseDataMaskingHeaders",
    "ApiManagementDiagnosticBackendResponseDataMaskingHeadersList",
    "ApiManagementDiagnosticBackendResponseDataMaskingHeadersOutputReference",
    "ApiManagementDiagnosticBackendResponseDataMaskingOutputReference",
    "ApiManagementDiagnosticBackendResponseDataMaskingQueryParams",
    "ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsList",
    "ApiManagementDiagnosticBackendResponseDataMaskingQueryParamsOutputReference",
    "ApiManagementDiagnosticBackendResponseOutputReference",
    "ApiManagementDiagnosticConfig",
    "ApiManagementDiagnosticFrontendRequest",
    "ApiManagementDiagnosticFrontendRequestDataMasking",
    "ApiManagementDiagnosticFrontendRequestDataMaskingHeaders",
    "ApiManagementDiagnosticFrontendRequestDataMaskingHeadersList",
    "ApiManagementDiagnosticFrontendRequestDataMaskingHeadersOutputReference",
    "ApiManagementDiagnosticFrontendRequestDataMaskingOutputReference",
    "ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams",
    "ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsList",
    "ApiManagementDiagnosticFrontendRequestDataMaskingQueryParamsOutputReference",
    "ApiManagementDiagnosticFrontendRequestOutputReference",
    "ApiManagementDiagnosticFrontendResponse",
    "ApiManagementDiagnosticFrontendResponseDataMasking",
    "ApiManagementDiagnosticFrontendResponseDataMaskingHeaders",
    "ApiManagementDiagnosticFrontendResponseDataMaskingHeadersList",
    "ApiManagementDiagnosticFrontendResponseDataMaskingHeadersOutputReference",
    "ApiManagementDiagnosticFrontendResponseDataMaskingOutputReference",
    "ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams",
    "ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsList",
    "ApiManagementDiagnosticFrontendResponseDataMaskingQueryParamsOutputReference",
    "ApiManagementDiagnosticFrontendResponseOutputReference",
    "ApiManagementDiagnosticTimeouts",
    "ApiManagementDiagnosticTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__78b1922c39db2525d16960a97bdede5b8f80e268ec8cb31642ea86a64e7430d0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_management_logger_id: builtins.str,
    api_management_name: builtins.str,
    identifier: builtins.str,
    resource_group_name: builtins.str,
    always_log_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backend_request: typing.Optional[typing.Union[ApiManagementDiagnosticBackendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    backend_response: typing.Optional[typing.Union[ApiManagementDiagnosticBackendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_request: typing.Optional[typing.Union[ApiManagementDiagnosticFrontendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_response: typing.Optional[typing.Union[ApiManagementDiagnosticFrontendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    http_correlation_protocol: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_client_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operation_name_format: typing.Optional[builtins.str] = None,
    sampling_percentage: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementDiagnosticTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8a2daadbc61e959ecbc104b0a1f7975d5daf4c3849cf66a478239b340dacd532(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c844c4f57e2141f48df90d3d5a3da96eed6c7d81b94e55433fc5dd6881804d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835ce427b79738d876be0af3a9c4a759e0fd9ed0955100a8a634f4029699ac98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ca82cbac9e6b1e721e957675827441470b1a55a80093fcac104cb6cef85ea0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe3dcfd5f6c57728d8b45563c267630e87cf9f1bb196193efd9528e60f2799a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb1487bf02d229bd05ea382a30aa80a097c74c0d6771cbaeef8519175e17067(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8f81a36939b87a277196c0cf82d2fd328b1fbcc2ffd532d29dde240e7434d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67eb8e3a6e6a2e085b84544df6a773ed7214876ad603bcb90ad04c91972a544d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc97c51b2180ca05e62e5aedd17a5ab794ad208c72c19c72454abd9110ad409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5b03fa70c27e3ddd807ac14ea83d14c91ff7e1ca45ec084c5eb77637aad59d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56074dc97e9ebccb3270e627e66a9a8270bbb44cce97311dfc52a0f0ad590f21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a02ae47b549d33bd1ea59a5f7b076403b9d33bd021ac91da4fe653976339fc35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3cf6e0f2c75a1e9e304a175874436c4e3dfaabf2cf0086135d1a0dd8b943e51(
    *,
    body_bytes: typing.Optional[jsii.Number] = None,
    data_masking: typing.Optional[typing.Union[ApiManagementDiagnosticBackendRequestDataMasking, typing.Dict[builtins.str, typing.Any]]] = None,
    headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8464d633b799a9462b420ff1bb2f848fd71cd74afe1cc983d4b43f5db9dffad3(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c3ffe416865b4061faa4e25332849feb844bc9f0124657745c2b0099b1ab36(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ccdd6a12d836cbcd22a2f9452e43b748443f285a5ab9e94d32b74c4f38bc7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241d8161638e4cdd0f481c2a88cfac7390a192b864edf7fa95f54c791d957faa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75cdd7926639c84bf3415e1ef4d314b718ba258fe3d27baa20996dd3f2a8927a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12fe2afbdf7bc0ca925ffe4885959acc56793dba017161b2b5c697ba4eac6466(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f09e501cc7cbef620a3a4b40aed014c60d204a4ff79151066f20e70dfad299f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cd985a482568da97431a6123b683135e744e44679c5c8b9c6690913be5e211(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2362c1225a9e2fc401d3f9ec5b0d28f7c1d3ca720a3be71ec3cb7bb43859b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7822a9ea9b952a1920fcc4f8f90d90e5dd2e6c6543ddb1e85ba06255ffc962f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82726debc58370a31b111aede9340fb3444936d39ff2c0838fbb0aef73c93d00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b2d27f7cfe041d9050f7ef8679af298ec9cb4583ddad7a19801783579312ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendRequestDataMaskingHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3dc943ae85a37dfd15a7dfe7712703a9a5d8472be97618fd99881dada5b71c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91125a5254b9c5cfe8c413fb11593ae593b401c15d4134c03ae4cf449ec99850(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9842ee7c80e83970089995a3ad35778952865ef55e7d262f36d4fcf51379ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45bf9e021cd511d581271be9ff40235a29b1d6095344157500907e878e449d70(
    value: typing.Optional[ApiManagementDiagnosticBackendRequestDataMasking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a917bd607d2181cfaa59f8ac64a0d140c9694e5457219a2184502e27cd59dd35(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82e9103cebeb740d3a541d69646422cb8c06709e5bca7ce89a68a1f244ef09c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29e41a2d82c4c65a359b9161ea33c8c3bc13a36625d35b7f3b91a84a87c274b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db45bd621930be62d58d614908e561644ccc4843a5413cee90523536d934562(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acdd638afda17aa40ad9a27079ee6de5d6d611ce2d456924774751b1dd13f12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f1ece46636fdb9b7b21cad14796bca04047623427e4a7d2c4efe0329380494(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee7034b88cca464a8f95987766ebfe7e31adfa8e2461461fb79409c7c839e65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendRequestDataMaskingQueryParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425fa036010c9921bc1b6ca12bb38b38b9c7d540b2e28781b43f3095e20fc08d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64035cac94ee01f2d4686c09feb121656624f93e13df66ad3d836f60a77d4c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20bfa03c5eab0c3e5cc4d1fdd40d4464d9c6a82f1284e28f90fdb9d1b93da59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a741e23f0bbc2ceb21fb5f4179f71f2f9d6c795c1bb400426d9c4e219029c48e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendRequestDataMaskingQueryParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8eeb433fb8b35d3ff91be78109dc1b5babb73d8b7be8d3737e3655662d00ace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f94f6c87f1966ff6c7bd4bbf24e891cbbd83dc7d08b899dc62095b36f5e116(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a070271806316dc134407424bc6a9459c97cd5337e692b4918fa3d5555d948(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d92a1375f9d1809837fc51a44719d12a9118c92f1eefc5e0a8bde2241c432bc(
    value: typing.Optional[ApiManagementDiagnosticBackendRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39ce265bad9ae3b48826ae15ac08e88480f977a2ff5cb56a455bfa2318e2048d(
    *,
    body_bytes: typing.Optional[jsii.Number] = None,
    data_masking: typing.Optional[typing.Union[ApiManagementDiagnosticBackendResponseDataMasking, typing.Dict[builtins.str, typing.Any]]] = None,
    headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3ad2187cfe78560508ecfdd4d29e98743d771ce95e3941d1eee4ebeeaa6b8c(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a0f340c5dc395c9ca5789be6d781a87690ac4a4b6c13fd3c20470bc9c390e1(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d2fc59472358925a42d5364961be6b4bcc7d9bdd325dc1eda521c5f6726f1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75fb61b833f0c952245e79979737c32da6b8a609775ca6ea0ab08750cad08426(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4f355aa04dff5ee58ae00102c594e03d6bdef4e3740efb807c1f5c3c87156f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d05062ccc8ec02f77b66e0a36e15a16714cf57069dfff3d475ef7662fdbaca5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b0fd486ada7fe952f649bc02f4e1aa7704292b5370f41917bceca5a04d9a6e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf3526f722dabea7139c3c2c5e6feaf5495886528dd8b8deb833dde51634aa6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70195050e16445459e18758577a3c1846e0103aaae75ce74ad7b23058c0d4d2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c12a4957aa135113d2867c23d29c878ded5d8be9735f0f81aadfb265ade950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff4a91ce61f5a245809fc074325b6e4434af16e4bd1f5c884f813b9975172c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd76d39fd26c8c2d3ab7616b08d111150a5267a2c31bad8fd25b17271cf99ec0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendResponseDataMaskingHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a24c5aad7ab6cc341f856dc34543b5f2c13a98c2392ece402e4b2330e936a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bb26afeca2754474564bba654cc6777d4a4f1c7aae0764469c4c7b59722c3b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfdb691a88ca9ddf5034594aaea975d6aaa690d12e6e57e3425ff43a983e9ea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticBackendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fd2f5fb22a7d0745cc6e86313bc9ef1c53f89c008a7316d6faac8628d548cd(
    value: typing.Optional[ApiManagementDiagnosticBackendResponseDataMasking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea198b8ad723b3e144a365c884443a65909ac0b16ad22757556375e2043a31c1(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b75faf892be0f5894a08b169845d69af500bfd76ff7de542ee4e86c7fd2bb14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42094ef22ba5939580eeafd669a18739030869882f8b65317d888ba9075e97e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1bb1bdfd169aefa06ea9cb79e11d5c600fc8fe421ec358d97b9c03732c66c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c416850d297a69fb32023f3884f6e16b2a8bb832790d5f5e8b96109d3ec702(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64915922d835a9dc92fe407f643860e3889be41ccfb62db612a797b2bad5660(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa42bfec194ce7d274e3c4cc728030665cd81efedfef89c77e9236cc811b32d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticBackendResponseDataMaskingQueryParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff9cd113b8d9ce43a3c2cb5bf30350e0d6a8e2d9fcfff6a8aab676f1bfd3e0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6dd493e952231521d603efd5b9b21595e2b7b5373ea6158b84e703f5e4dbddd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793274c1529ec8e69e5b24f9d1dca9ca7578a167d29a1008aebf0cd116253450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7daaf9eba33a15a3e146cf47664b2a79bcc3637c56e806ae49e6cf10584a2ca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticBackendResponseDataMaskingQueryParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c08bf66b78aff830c912382d1a3eab8097505d5cbf8ea7838d0e76a19e9292a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ea1bbc81fe7b67c689a4f1aad7cfd3048f212258e08336a1a3d77202710e37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fdcea01bae15a022cdd69f02be4497cd70c1278de747b5c5fba13a1d890774(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a5c1bda9e501852a1b2923791b342ea248f0606830fb43160d2b1edea0e86c(
    value: typing.Optional[ApiManagementDiagnosticBackendResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2495fdab480b2d6f09e213943c9f73150ce26ae4c191e62937445eff18657f39(
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
    identifier: builtins.str,
    resource_group_name: builtins.str,
    always_log_errors: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    backend_request: typing.Optional[typing.Union[ApiManagementDiagnosticBackendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    backend_response: typing.Optional[typing.Union[ApiManagementDiagnosticBackendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_request: typing.Optional[typing.Union[ApiManagementDiagnosticFrontendRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend_response: typing.Optional[typing.Union[ApiManagementDiagnosticFrontendResponse, typing.Dict[builtins.str, typing.Any]]] = None,
    http_correlation_protocol: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_client_ip: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    operation_name_format: typing.Optional[builtins.str] = None,
    sampling_percentage: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[ApiManagementDiagnosticTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    verbosity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d88236074e3be0cdd2050aab28a4c3a6724d502acad32f8570362ae73b1d956(
    *,
    body_bytes: typing.Optional[jsii.Number] = None,
    data_masking: typing.Optional[typing.Union[ApiManagementDiagnosticFrontendRequestDataMasking, typing.Dict[builtins.str, typing.Any]]] = None,
    headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052f729fa296d06256da75dffdc3908dd8298e0a6ffd166390f3a14a944f238e(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3c97ed64c57b2e9048f7794cffc16d73779ea0aca911576c98855e0c432000(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ceadcb98423587c9cebc790592d86b9d0ac10b10a69a529695a115fac33558(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a78b299f894822af56e9b390e0c964934c4d959e4727286e6acd1414892cb1e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940ba840481c1f6e1c4235fd5ea46ec6b8114144956d6b60404b99a04b9b293a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723d821625389fbe4480163323b32ecacf95bb8b7c2c8882b4bebae594783ab4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93645ae134f3a8105e921cbaafd4dbcc54d4d2d2b9542c5f7af4f5986a875aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30ef486c34077ec75ad849fdf8b6f98742c1e3b35bd94cc8bba878d3477f9bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a34f52e530eaa4e07870d96655541b7135a0db9f29ffc5f77fcdf0872119bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab3e3adbef9d944ecfaabc30e6a7402d66fb6580e3f2beb8086e5b52c2261a04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db30d0332b5a15e90fe1d4175efeb759241cc7283c26a78a2264305865ef2977(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28eea5d6a493e9be14468fcd20e56dc1190aaf1c4af040f616623050e661b388(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendRequestDataMaskingHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa81133002681ec71e1ba591a1c495708cacdcfb882c602d632fe57ff70028d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24104229d83018ca37b57d95fca5459deab63446ecc258e3ad161a6dcd2ba110(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendRequestDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dae76c8a6df201d9b55ce0531be31e3a24f98975c7fd89b494577dac2639ceb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7480c53b7c650443dd9e446a36a3d1b61c0cbb13d06ab42a45d99867581ff0(
    value: typing.Optional[ApiManagementDiagnosticFrontendRequestDataMasking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e76f8ef536ec0aa9f428992571867ecf4592e58709ab0ddf8a1159fec8c7623(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136f76ffab271d99064ac27311d30d803494b3a64189a65c454226b55c38cd8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd64bb106f4d4b4274d03164c6bc4094db20ea909b32eec448123694cc4c8088(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e44466e2ab768d30c088348c15e64b7b83f141237a893d4cd7bdd40179bf265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cb92fa73545dd8a55b44cbf79e8fb8505ee8b177dc7af93b69b4424e22d364(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71a9e13ffd63fe4c72c45525dfb2f5f001407249e395b9e20e53eb5c2222625(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f6ea1fc81884faebc1015a43454c2d581314349dc6a3f944bce3f4bb15ba97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aaa0f436f876254430a3b54392c0dd3fe15e9e788945ace6bf7441ab90e3cfd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831447d42fe53f44afb1b7ae8f382d8b16b8a20de372032da85484ef387cc9c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d3cba51d86d2718057f953f7c877cc643a472cb74e7a8f4b8ddb0ac3e6b342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ec27a5dc6cc4ad977c20c5b84f0bb02d3c47e17baf23e04b093c2c84556b261(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendRequestDataMaskingQueryParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8effd2ea4eb16d3cbb9b11c091c6fa598fa44eea530cc7fe592b0fb490167c56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee685925a779c949e3291253833265a513ca29f9aac91afaaa3ae74e11d5a53(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a66e882ef66d02400079ec652d931ee677ac2b6e9374b1113f2782aade10949(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42dfdc9391a6211727f9c6d5c28ad937939f2e266bcab6b734709a34b4d3a8b(
    value: typing.Optional[ApiManagementDiagnosticFrontendRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c2d602882615b2cacdfc02a04d8257d2114df17d1427c164f9d9cbd3ab45f3(
    *,
    body_bytes: typing.Optional[jsii.Number] = None,
    data_masking: typing.Optional[typing.Union[ApiManagementDiagnosticFrontendResponseDataMasking, typing.Dict[builtins.str, typing.Any]]] = None,
    headers_to_log: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ade6eb62525ba60d8c6ea9b1b83d917ab52f3c45601544b1da7955943b2f33(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    query_params: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bd6876e7b917cf52a042121c437c746c2d748a7854008912e78373c398bcc1(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3186b0b9b252fe14bef7daed6414cee99c35eb7189ac4c5eb51b17962939b3ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325bc0d5f8b03b44c5c194841649848ffe3d202040ac4b41d2d4c8e6bcde80cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523b89480444ff2bdb55a85d0c5967622ac50bc527a8cd8f20ad1c89fe5ac9e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661c8165ac372eb517e5a697ec9c6321c7c8e3a6739084f48b731cdbef5d2159(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d01c9b8c6d036cb827d057df9289887dad0f911ce5e04d0ab6074b29a5403b07(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361ed0556f887c8a103d48dcef1e15a9cae76fe1b829a0a2c95ded54abd0e23d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773676990ed650e5a7fed5c8807da878cc3968e51db32fec72cd1dd61e93d03d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b77b73bcd99343591302fcadb806cfb4fc12d3d54c4e7ff0668f4923ff1e9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f20069a8a85306e7780dc9a181a7d84b82d81a27ed6269c2fed7c358a9e5f82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c3b310701476226cf3532ac5292e31b19b3eed9081e7e2bbb8fa8d647b3553(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendResponseDataMaskingHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48b34429908ae315515ea4aa1011498bd6940a90a36a2b8e787d134234914e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897e3951035ad9b9367eaefd8885db9018bd07fc696c53b473730bbe8844d4a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendResponseDataMaskingHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b491d8f8e038f538b6d64e91f9d38b8b869678c03074cd0658b2347dcc1f94(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64530676d35a72e41608e7ffe29e904412f8fd8b3292d19851afb21926bf4edd(
    value: typing.Optional[ApiManagementDiagnosticFrontendResponseDataMasking],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cdbb92ab8cb7823612dffe25581b2210db8136e48f78e2c36f1b6a77c886962(
    *,
    mode: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b437a159e7ae6455559576fff61d1d46315d61b5a71c476aba4ce2144c55f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddb375c18c1cdd555b5d505d470c091e6f39aab89eb619409f9bb3a1d2e04d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9db1f061def14e63c2b1e9aaf5457f72146a402b92f16373cad85475db1bd8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c05742dc7768a7380309f1bac0d95f2e3e5004b34f476446f9cfcd23deba92(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79a9eb52381e148afada21796c42a0dc31f2cf81391bf7efa838255524bb836(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4183f44bdf457aa4db00d85bf1c0bd65832810c868e52e1dd1ff2ffa22c811(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015738bea66f1d3621ebb54475a48d6fcd2165b1bfe52c41575807e506a184d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63dc41a384d26318817c49d703e8a67101be3c862312e7a8aa8f8eb5d44a0f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82610cf931cd764fb50ea884e7cf42fb8c2bace5cb7898910373ed4204e08902(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a171548e1b384748987d9e48e12fae4f40f4a65348c50ec96c819e3e65fe9f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticFrontendResponseDataMaskingQueryParams]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1db941e50880967e3b09d696f9753381863ba428fb88ad10aaae4bc056a576cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5718acaa9453781d867b0fbbddefe930cf55120b0cd25501389c5b670006d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e58792319c815e94072b32a5fb263f8dbfd99acd4a5bf54eb22556a9459505(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65c1466e28cf1a1dbdf77e7e78d674bac99541ac56bce580116c1144802856a(
    value: typing.Optional[ApiManagementDiagnosticFrontendResponse],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32fafc6382ca030494d72ec042d9f66c4e94abf98b46d40adc45890c79470e0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87fa1e5c95893d2b3a965da0d3eb24ea37a3628556d7f737212bd87cc079e0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ca24f3944613ce3f89fe53598701b17c0bb67435bc195407ca2b8668e3a7fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__521f238fc2e66c42cf1b16a5b583bfd0ef8e35d805e0f1ac458e47f92c08efe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96512dc0e688ef777c28c5496065160f3d43eb20dd36df577d2fffe9e7d168ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f276b586dba8e5a61c86f13982026082d7ae986a42a55a119089f61a6ce53ffc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9369ed990ab6f50cb6348ef3812405d786b51ce56986070c939db45351879b37(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ApiManagementDiagnosticTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

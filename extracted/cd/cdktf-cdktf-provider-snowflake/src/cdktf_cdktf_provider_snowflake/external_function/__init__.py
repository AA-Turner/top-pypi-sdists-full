r'''
# `snowflake_external_function`

Refer to the Terraform Registry for docs: [`snowflake_external_function`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function).
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


class ExternalFunction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalFunction.ExternalFunction",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function snowflake_external_function}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        api_integration: builtins.str,
        database: builtins.str,
        name: builtins.str,
        return_behavior: builtins.str,
        return_type: builtins.str,
        schema: builtins.str,
        url_of_proxy_and_resource: builtins.str,
        arg: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalFunctionArg", typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        compression: typing.Optional[builtins.str] = None,
        context_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalFunctionHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        max_batch_rows: typing.Optional[jsii.Number] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        request_translator: typing.Optional[builtins.str] = None,
        response_translator: typing.Optional[builtins.str] = None,
        return_null_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function snowflake_external_function} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param api_integration: The name of the API integration object that should be used to authenticate the call to the proxy service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#api_integration ExternalFunction#api_integration}
        :param database: The database in which to create the external function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#database ExternalFunction#database}
        :param name: Specifies the identifier for the external function. The identifier can contain the schema name and database name, as well as the function name. The function's signature (name and argument data types) must be unique within the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#name ExternalFunction#name}
        :param return_behavior: Specifies the behavior of the function when returning results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_behavior ExternalFunction#return_behavior}
        :param return_type: Specifies the data type returned by the external function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_type ExternalFunction#return_type}
        :param schema: The schema in which to create the external function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#schema ExternalFunction#schema}
        :param url_of_proxy_and_resource: This is the invocation URL of the proxy service and resource through which Snowflake calls the remote service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#url_of_proxy_and_resource ExternalFunction#url_of_proxy_and_resource}
        :param arg: arg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#arg ExternalFunction#arg}
        :param comment: A description of the external function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#comment ExternalFunction#comment}
        :param compression: If specified, the JSON payload is compressed when sent from Snowflake to the proxy service, and when sent back from the proxy service to Snowflake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#compression ExternalFunction#compression}
        :param context_headers: Binds Snowflake context function results to HTTP headers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#context_headers ExternalFunction#context_headers}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#header ExternalFunction#header}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#id ExternalFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_batch_rows: This specifies the maximum number of rows in each batch sent to the proxy service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#max_batch_rows ExternalFunction#max_batch_rows}
        :param null_input_behavior: Specifies the behavior of the external function when called with null inputs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#null_input_behavior ExternalFunction#null_input_behavior}
        :param request_translator: This specifies the name of the request translator function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#request_translator ExternalFunction#request_translator}
        :param response_translator: This specifies the name of the response translator function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#response_translator ExternalFunction#response_translator}
        :param return_null_allowed: Indicates whether the function can return NULL values (true) or must return only NON-NULL values (false). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_null_allowed ExternalFunction#return_null_allowed}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f1e6377f90568ad737f9b2baba668e6a1f65589c77bec4fa5c3d72d408dba9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ExternalFunctionConfig(
            api_integration=api_integration,
            database=database,
            name=name,
            return_behavior=return_behavior,
            return_type=return_type,
            schema=schema,
            url_of_proxy_and_resource=url_of_proxy_and_resource,
            arg=arg,
            comment=comment,
            compression=compression,
            context_headers=context_headers,
            header=header,
            id=id,
            max_batch_rows=max_batch_rows,
            null_input_behavior=null_input_behavior,
            request_translator=request_translator,
            response_translator=response_translator,
            return_null_allowed=return_null_allowed,
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
        '''Generates CDKTF code for importing a ExternalFunction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ExternalFunction to import.
        :param import_from_id: The id of the existing ExternalFunction that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ExternalFunction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ee7b7c009ea1c28bee01f4726a0bffe5fc3994d97ad42d3e93e5c4d7a70a93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArg")
    def put_arg(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalFunctionArg", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e88ebc2c2ef1d0e1b35bccd022abbf8ca3294ebd0b58d8ebef02bed024bbc995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArg", [value]))

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalFunctionHeader", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7474455547fd227724769b61f2fd987e8552d128dbb3772a5d83cb8e00411a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetArg")
    def reset_arg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArg", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetCompression")
    def reset_compression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompression", []))

    @jsii.member(jsii_name="resetContextHeaders")
    def reset_context_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextHeaders", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaxBatchRows")
    def reset_max_batch_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBatchRows", []))

    @jsii.member(jsii_name="resetNullInputBehavior")
    def reset_null_input_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullInputBehavior", []))

    @jsii.member(jsii_name="resetRequestTranslator")
    def reset_request_translator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestTranslator", []))

    @jsii.member(jsii_name="resetResponseTranslator")
    def reset_response_translator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseTranslator", []))

    @jsii.member(jsii_name="resetReturnNullAllowed")
    def reset_return_null_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnNullAllowed", []))

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
    @jsii.member(jsii_name="arg")
    def arg(self) -> "ExternalFunctionArgList":
        return typing.cast("ExternalFunctionArgList", jsii.get(self, "arg"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> "ExternalFunctionHeaderList":
        return typing.cast("ExternalFunctionHeaderList", jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="apiIntegrationInput")
    def api_integration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiIntegrationInput"))

    @builtins.property
    @jsii.member(jsii_name="argInput")
    def arg_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalFunctionArg"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalFunctionArg"]]], jsii.get(self, "argInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="compressionInput")
    def compression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compressionInput"))

    @builtins.property
    @jsii.member(jsii_name="contextHeadersInput")
    def context_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contextHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalFunctionHeader"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalFunctionHeader"]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBatchRowsInput")
    def max_batch_rows_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBatchRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nullInputBehaviorInput")
    def null_input_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nullInputBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="requestTranslatorInput")
    def request_translator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestTranslatorInput"))

    @builtins.property
    @jsii.member(jsii_name="responseTranslatorInput")
    def response_translator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseTranslatorInput"))

    @builtins.property
    @jsii.member(jsii_name="returnBehaviorInput")
    def return_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="returnNullAllowedInput")
    def return_null_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "returnNullAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="returnTypeInput")
    def return_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="urlOfProxyAndResourceInput")
    def url_of_proxy_and_resource_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlOfProxyAndResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="apiIntegration")
    def api_integration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiIntegration"))

    @api_integration.setter
    def api_integration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1685316d18cb98f85ec7c1ff542429fa79fcd66f20a174eab02a59e6b4ead41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiIntegration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f24a1c91512751b789383dc74363230723c06b1c59ff1cef51e8ca71ddef145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="compression")
    def compression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compression"))

    @compression.setter
    def compression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1fc3966b86fc467aa7b71dcdb81665837ce3d99a7c9baf06b120965e0e95cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contextHeaders")
    def context_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contextHeaders"))

    @context_headers.setter
    def context_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb352b9883b2dc3a2c9860d616ec99b795850d3f326d73936f8265e365194a55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__030863b89e777c26ca64b375fd542a59955629f66a7e75535bfa602d1a70c69d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae240673c9f4145c9707ebeec2e4762fcde8c8d7ac9c5667ec7220563d186169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBatchRows")
    def max_batch_rows(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxBatchRows"))

    @max_batch_rows.setter
    def max_batch_rows(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c556ac5b6d42edc7182a2ce5138adf6245965230636414405dd4707b0aa01b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBatchRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdaac7e611c38b476c15c22879ceb413c7005521915c7a6063e4179b7884efd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullInputBehavior")
    def null_input_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullInputBehavior"))

    @null_input_behavior.setter
    def null_input_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0827def83f41cc4c142c67b2de1d0362ab85b2382f1a3b311ba3ff9ae3dfb53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullInputBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requestTranslator")
    def request_translator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestTranslator"))

    @request_translator.setter
    def request_translator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02fc6ea2a7d8d0b9163e20bcceac1274b654eb780992df3044e28a46ddd2643b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestTranslator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseTranslator")
    def response_translator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseTranslator"))

    @response_translator.setter
    def response_translator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31431d7f2ee9654e23d0143e9cdf4c48a78beb131190f084c7863634d9b25e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseTranslator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnBehavior")
    def return_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnBehavior"))

    @return_behavior.setter
    def return_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37224c672c455891bc336474f1132dd9ac9a96eb2c682c4b34b2f31e35f07472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnNullAllowed")
    def return_null_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "returnNullAllowed"))

    @return_null_allowed.setter
    def return_null_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b3a9d20b7b5ed172343dd78123f0d0d54c8ab233f7060c49cebedd030cceff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnNullAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b915e7d673afdfdaf5b1f6a46f02d16de0f89d5014c4b7210fb0dba17b473a1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f485c0ccb63545168c6b1ed04daa7d6a36bc1fedd303d7b774c9f4099f6ce92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlOfProxyAndResource")
    def url_of_proxy_and_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlOfProxyAndResource"))

    @url_of_proxy_and_resource.setter
    def url_of_proxy_and_resource(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b729e73ad688b19a67455b76bd3ad8bb02285f9c8864f355b816660514d9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlOfProxyAndResource", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalFunction.ExternalFunctionArg",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class ExternalFunctionArg:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Argument name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#name ExternalFunction#name}
        :param type: Argument type, e.g. VARCHAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#type ExternalFunction#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa91adf443b0e58389feed0315ed7e3e773c128d2264d70e586fc48a6636b7a9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Argument name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#name ExternalFunction#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Argument type, e.g. VARCHAR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#type ExternalFunction#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalFunctionArg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalFunctionArgList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalFunction.ExternalFunctionArgList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15f544d0231e6d741c25f95172a13a5a44d93eb7ead251c31367071d207a72e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ExternalFunctionArgOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a95d9fb3df0c27b10438515c42c2f4052acd195becadbc3a0147dfea2cd7253)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalFunctionArgOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c1a40fd6123b62381a6286a5c0742091c441dfd9ee3093e83c7f4309547e8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ef34fce6ecf40c850165f4b31c74d2a9befe0ebf31eb7d720058fcbe43592d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e231785dda13597285615943f3985ae2894056c635e07d22aa48cd67310b5f73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionArg]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionArg]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionArg]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bd8fa2ed397d7ca378db2f22218e35aa014aa0ca7fcccddd61863560e878f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ExternalFunctionArgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalFunction.ExternalFunctionArgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f414bcacae8440b938c36bb262ae29dd0444de91b52e921e3e9eb25a2ccdf14)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__554c08544579461458f45a57a6394c16ce79a44adb8e11497c0a126253b709a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f622a02a50822ec48e844e39b1c9ed196a969711fb2a75568066a0efffefa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalFunctionArg]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalFunctionArg]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalFunctionArg]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f6ae4c907da45273ffe9db2ecfad20033a6d0fb3c71c7a90bbaa28202a71f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalFunction.ExternalFunctionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "api_integration": "apiIntegration",
        "database": "database",
        "name": "name",
        "return_behavior": "returnBehavior",
        "return_type": "returnType",
        "schema": "schema",
        "url_of_proxy_and_resource": "urlOfProxyAndResource",
        "arg": "arg",
        "comment": "comment",
        "compression": "compression",
        "context_headers": "contextHeaders",
        "header": "header",
        "id": "id",
        "max_batch_rows": "maxBatchRows",
        "null_input_behavior": "nullInputBehavior",
        "request_translator": "requestTranslator",
        "response_translator": "responseTranslator",
        "return_null_allowed": "returnNullAllowed",
    },
)
class ExternalFunctionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        api_integration: builtins.str,
        database: builtins.str,
        name: builtins.str,
        return_behavior: builtins.str,
        return_type: builtins.str,
        schema: builtins.str,
        url_of_proxy_and_resource: builtins.str,
        arg: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalFunctionArg, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        compression: typing.Optional[builtins.str] = None,
        context_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ExternalFunctionHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        max_batch_rows: typing.Optional[jsii.Number] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        request_translator: typing.Optional[builtins.str] = None,
        response_translator: typing.Optional[builtins.str] = None,
        return_null_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param api_integration: The name of the API integration object that should be used to authenticate the call to the proxy service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#api_integration ExternalFunction#api_integration}
        :param database: The database in which to create the external function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#database ExternalFunction#database}
        :param name: Specifies the identifier for the external function. The identifier can contain the schema name and database name, as well as the function name. The function's signature (name and argument data types) must be unique within the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#name ExternalFunction#name}
        :param return_behavior: Specifies the behavior of the function when returning results. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_behavior ExternalFunction#return_behavior}
        :param return_type: Specifies the data type returned by the external function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_type ExternalFunction#return_type}
        :param schema: The schema in which to create the external function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#schema ExternalFunction#schema}
        :param url_of_proxy_and_resource: This is the invocation URL of the proxy service and resource through which Snowflake calls the remote service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#url_of_proxy_and_resource ExternalFunction#url_of_proxy_and_resource}
        :param arg: arg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#arg ExternalFunction#arg}
        :param comment: A description of the external function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#comment ExternalFunction#comment}
        :param compression: If specified, the JSON payload is compressed when sent from Snowflake to the proxy service, and when sent back from the proxy service to Snowflake. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#compression ExternalFunction#compression}
        :param context_headers: Binds Snowflake context function results to HTTP headers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#context_headers ExternalFunction#context_headers}
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#header ExternalFunction#header}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#id ExternalFunction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param max_batch_rows: This specifies the maximum number of rows in each batch sent to the proxy service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#max_batch_rows ExternalFunction#max_batch_rows}
        :param null_input_behavior: Specifies the behavior of the external function when called with null inputs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#null_input_behavior ExternalFunction#null_input_behavior}
        :param request_translator: This specifies the name of the request translator function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#request_translator ExternalFunction#request_translator}
        :param response_translator: This specifies the name of the response translator function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#response_translator ExternalFunction#response_translator}
        :param return_null_allowed: Indicates whether the function can return NULL values (true) or must return only NON-NULL values (false). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_null_allowed ExternalFunction#return_null_allowed}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e682723f6096db49b629b164e1596e63b85a35fccd9ecf2df69658061b203273)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument api_integration", value=api_integration, expected_type=type_hints["api_integration"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument return_behavior", value=return_behavior, expected_type=type_hints["return_behavior"])
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument url_of_proxy_and_resource", value=url_of_proxy_and_resource, expected_type=type_hints["url_of_proxy_and_resource"])
            check_type(argname="argument arg", value=arg, expected_type=type_hints["arg"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
            check_type(argname="argument context_headers", value=context_headers, expected_type=type_hints["context_headers"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument max_batch_rows", value=max_batch_rows, expected_type=type_hints["max_batch_rows"])
            check_type(argname="argument null_input_behavior", value=null_input_behavior, expected_type=type_hints["null_input_behavior"])
            check_type(argname="argument request_translator", value=request_translator, expected_type=type_hints["request_translator"])
            check_type(argname="argument response_translator", value=response_translator, expected_type=type_hints["response_translator"])
            check_type(argname="argument return_null_allowed", value=return_null_allowed, expected_type=type_hints["return_null_allowed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_integration": api_integration,
            "database": database,
            "name": name,
            "return_behavior": return_behavior,
            "return_type": return_type,
            "schema": schema,
            "url_of_proxy_and_resource": url_of_proxy_and_resource,
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
        if arg is not None:
            self._values["arg"] = arg
        if comment is not None:
            self._values["comment"] = comment
        if compression is not None:
            self._values["compression"] = compression
        if context_headers is not None:
            self._values["context_headers"] = context_headers
        if header is not None:
            self._values["header"] = header
        if id is not None:
            self._values["id"] = id
        if max_batch_rows is not None:
            self._values["max_batch_rows"] = max_batch_rows
        if null_input_behavior is not None:
            self._values["null_input_behavior"] = null_input_behavior
        if request_translator is not None:
            self._values["request_translator"] = request_translator
        if response_translator is not None:
            self._values["response_translator"] = response_translator
        if return_null_allowed is not None:
            self._values["return_null_allowed"] = return_null_allowed

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
    def api_integration(self) -> builtins.str:
        '''The name of the API integration object that should be used to authenticate the call to the proxy service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#api_integration ExternalFunction#api_integration}
        '''
        result = self._values.get("api_integration")
        assert result is not None, "Required property 'api_integration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database(self) -> builtins.str:
        '''The database in which to create the external function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#database ExternalFunction#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the identifier for the external function.

        The identifier can contain the schema name and database name, as well as the function name. The function's signature (name and argument data types) must be unique within the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#name ExternalFunction#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def return_behavior(self) -> builtins.str:
        '''Specifies the behavior of the function when returning results.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_behavior ExternalFunction#return_behavior}
        '''
        result = self._values.get("return_behavior")
        assert result is not None, "Required property 'return_behavior' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def return_type(self) -> builtins.str:
        '''Specifies the data type returned by the external function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_type ExternalFunction#return_type}
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the external function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#schema ExternalFunction#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url_of_proxy_and_resource(self) -> builtins.str:
        '''This is the invocation URL of the proxy service and resource through which Snowflake calls the remote service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#url_of_proxy_and_resource ExternalFunction#url_of_proxy_and_resource}
        '''
        result = self._values.get("url_of_proxy_and_resource")
        assert result is not None, "Required property 'url_of_proxy_and_resource' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionArg]]]:
        '''arg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#arg ExternalFunction#arg}
        '''
        result = self._values.get("arg")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionArg]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''A description of the external function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#comment ExternalFunction#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compression(self) -> typing.Optional[builtins.str]:
        '''If specified, the JSON payload is compressed when sent from Snowflake to the proxy service, and when sent back from the proxy service to Snowflake.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#compression ExternalFunction#compression}
        '''
        result = self._values.get("compression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Binds Snowflake context function results to HTTP headers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#context_headers ExternalFunction#context_headers}
        '''
        result = self._values.get("context_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalFunctionHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#header ExternalFunction#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ExternalFunctionHeader"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#id ExternalFunction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_batch_rows(self) -> typing.Optional[jsii.Number]:
        '''This specifies the maximum number of rows in each batch sent to the proxy service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#max_batch_rows ExternalFunction#max_batch_rows}
        '''
        result = self._values.get("max_batch_rows")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def null_input_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the external function when called with null inputs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#null_input_behavior ExternalFunction#null_input_behavior}
        '''
        result = self._values.get("null_input_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_translator(self) -> typing.Optional[builtins.str]:
        '''This specifies the name of the request translator function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#request_translator ExternalFunction#request_translator}
        '''
        result = self._values.get("request_translator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_translator(self) -> typing.Optional[builtins.str]:
        '''This specifies the name of the response translator function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#response_translator ExternalFunction#response_translator}
        '''
        result = self._values.get("response_translator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def return_null_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the function can return NULL values (true) or must return only NON-NULL values (false).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#return_null_allowed ExternalFunction#return_null_allowed}
        '''
        result = self._values.get("return_null_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalFunctionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.externalFunction.ExternalFunctionHeader",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class ExternalFunctionHeader:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Header name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#name ExternalFunction#name}
        :param value: Header value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#value ExternalFunction#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a9332a4b1f73bdc42756b03e408e206af9f4d76f19feefd3567b866df4afa77)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Header name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#name ExternalFunction#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Header value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/external_function#value ExternalFunction#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalFunctionHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalFunctionHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalFunction.ExternalFunctionHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__204bfa33881bbe602961d7c200aec5c3d8ec10ac05290bfdec85149c52214684)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ExternalFunctionHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28055e9ff8046becf24328a999108dfca025dedafea0c20fc6693fc752fcb9c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ExternalFunctionHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a8b894af965d12077d40a4427ea0aacc851973a6de193eaefdb2b118669762)
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
            type_hints = typing.get_type_hints(_typecheckingstub__028bd3dced10be2457c21e3e0efc3844d2eb342f1b0ca553f612bda220580552)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb408c86d80ac2540dbc4d0e0ae25052dbe26e1d012129140e4ecd48736c0033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9b09a772e6d0dd2bd84a1668a7ed3156965b95f72235811ae8334f705abd18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ExternalFunctionHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.externalFunction.ExternalFunctionHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__712a2ab42239f1a9c41d86885485804ba9d58624d1da0869d7f8593d53d04f04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca87f266b476fe82015aac06f6d068b2bd288665e2ffbc3ddf2f87b04d8a263)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d61f0d4ed662524939ef679a41d55aba07a91e57e745c1f33803b55c27a7df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalFunctionHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalFunctionHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalFunctionHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05cca51610e4817a43e91541b530392431550de94f91e62f2960b7b3e54ff49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ExternalFunction",
    "ExternalFunctionArg",
    "ExternalFunctionArgList",
    "ExternalFunctionArgOutputReference",
    "ExternalFunctionConfig",
    "ExternalFunctionHeader",
    "ExternalFunctionHeaderList",
    "ExternalFunctionHeaderOutputReference",
]

publication.publish()

def _typecheckingstub__37f1e6377f90568ad737f9b2baba668e6a1f65589c77bec4fa5c3d72d408dba9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    api_integration: builtins.str,
    database: builtins.str,
    name: builtins.str,
    return_behavior: builtins.str,
    return_type: builtins.str,
    schema: builtins.str,
    url_of_proxy_and_resource: builtins.str,
    arg: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalFunctionArg, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    compression: typing.Optional[builtins.str] = None,
    context_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalFunctionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    max_batch_rows: typing.Optional[jsii.Number] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    request_translator: typing.Optional[builtins.str] = None,
    response_translator: typing.Optional[builtins.str] = None,
    return_null_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__84ee7b7c009ea1c28bee01f4726a0bffe5fc3994d97ad42d3e93e5c4d7a70a93(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88ebc2c2ef1d0e1b35bccd022abbf8ca3294ebd0b58d8ebef02bed024bbc995(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalFunctionArg, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7474455547fd227724769b61f2fd987e8552d128dbb3772a5d83cb8e00411a58(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalFunctionHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1685316d18cb98f85ec7c1ff542429fa79fcd66f20a174eab02a59e6b4ead41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f24a1c91512751b789383dc74363230723c06b1c59ff1cef51e8ca71ddef145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1fc3966b86fc467aa7b71dcdb81665837ce3d99a7c9baf06b120965e0e95cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb352b9883b2dc3a2c9860d616ec99b795850d3f326d73936f8265e365194a55(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030863b89e777c26ca64b375fd542a59955629f66a7e75535bfa602d1a70c69d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae240673c9f4145c9707ebeec2e4762fcde8c8d7ac9c5667ec7220563d186169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c556ac5b6d42edc7182a2ce5138adf6245965230636414405dd4707b0aa01b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdaac7e611c38b476c15c22879ceb413c7005521915c7a6063e4179b7884efd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0827def83f41cc4c142c67b2de1d0362ab85b2382f1a3b311ba3ff9ae3dfb53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fc6ea2a7d8d0b9163e20bcceac1274b654eb780992df3044e28a46ddd2643b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31431d7f2ee9654e23d0143e9cdf4c48a78beb131190f084c7863634d9b25e88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37224c672c455891bc336474f1132dd9ac9a96eb2c682c4b34b2f31e35f07472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b3a9d20b7b5ed172343dd78123f0d0d54c8ab233f7060c49cebedd030cceff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b915e7d673afdfdaf5b1f6a46f02d16de0f89d5014c4b7210fb0dba17b473a1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f485c0ccb63545168c6b1ed04daa7d6a36bc1fedd303d7b774c9f4099f6ce92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b729e73ad688b19a67455b76bd3ad8bb02285f9c8864f355b816660514d9a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa91adf443b0e58389feed0315ed7e3e773c128d2264d70e586fc48a6636b7a9(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f544d0231e6d741c25f95172a13a5a44d93eb7ead251c31367071d207a72e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a95d9fb3df0c27b10438515c42c2f4052acd195becadbc3a0147dfea2cd7253(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c1a40fd6123b62381a6286a5c0742091c441dfd9ee3093e83c7f4309547e8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef34fce6ecf40c850165f4b31c74d2a9befe0ebf31eb7d720058fcbe43592d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e231785dda13597285615943f3985ae2894056c635e07d22aa48cd67310b5f73(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0bd8fa2ed397d7ca378db2f22218e35aa014aa0ca7fcccddd61863560e878f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionArg]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f414bcacae8440b938c36bb262ae29dd0444de91b52e921e3e9eb25a2ccdf14(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554c08544579461458f45a57a6394c16ce79a44adb8e11497c0a126253b709a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f622a02a50822ec48e844e39b1c9ed196a969711fb2a75568066a0efffefa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f6ae4c907da45273ffe9db2ecfad20033a6d0fb3c71c7a90bbaa28202a71f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalFunctionArg]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e682723f6096db49b629b164e1596e63b85a35fccd9ecf2df69658061b203273(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    api_integration: builtins.str,
    database: builtins.str,
    name: builtins.str,
    return_behavior: builtins.str,
    return_type: builtins.str,
    schema: builtins.str,
    url_of_proxy_and_resource: builtins.str,
    arg: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalFunctionArg, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    compression: typing.Optional[builtins.str] = None,
    context_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ExternalFunctionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    max_batch_rows: typing.Optional[jsii.Number] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    request_translator: typing.Optional[builtins.str] = None,
    response_translator: typing.Optional[builtins.str] = None,
    return_null_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a9332a4b1f73bdc42756b03e408e206af9f4d76f19feefd3567b866df4afa77(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__204bfa33881bbe602961d7c200aec5c3d8ec10ac05290bfdec85149c52214684(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28055e9ff8046becf24328a999108dfca025dedafea0c20fc6693fc752fcb9c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a8b894af965d12077d40a4427ea0aacc851973a6de193eaefdb2b118669762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__028bd3dced10be2457c21e3e0efc3844d2eb342f1b0ca553f612bda220580552(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb408c86d80ac2540dbc4d0e0ae25052dbe26e1d012129140e4ecd48736c0033(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9b09a772e6d0dd2bd84a1668a7ed3156965b95f72235811ae8334f705abd18(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ExternalFunctionHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712a2ab42239f1a9c41d86885485804ba9d58624d1da0869d7f8593d53d04f04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ca87f266b476fe82015aac06f6d068b2bd288665e2ffbc3ddf2f87b04d8a263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d61f0d4ed662524939ef679a41d55aba07a91e57e745c1f33803b55c27a7df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05cca51610e4817a43e91541b530392431550de94f91e62f2960b7b3e54ff49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ExternalFunctionHeader]],
) -> None:
    """Type checking stubs"""
    pass

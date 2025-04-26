r'''
# `snowflake_function_javascript`

Refer to the Terraform Registry for docs: [`snowflake_function_javascript`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript).
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


class FunctionJavascript(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascript",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript snowflake_function_javascript}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        function_definition: builtins.str,
        name: builtins.str,
        return_type: builtins.str,
        schema: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavascriptArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        return_results_behavior: typing.Optional[builtins.str] = None,
        trace_level: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript snowflake_function_javascript} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#database FunctionJavascript#database}
        :param function_definition: Defines the handler code executed when the UDF is called. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be JavaScript source code. For more information, see `Introduction to JavaScript UDFs <https://docs.snowflake.com/en/developer-guide/udf/javascript/udf-javascript-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#function_definition FunctionJavascript#function_definition}
        :param name: The name of the function; the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#name FunctionJavascript#name}
        :param return_type: Specifies the results returned by the UDF, which determines the UDF type. Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#return_type FunctionJavascript#return_type}
        :param schema: The schema in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#schema FunctionJavascript#schema}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arguments FunctionJavascript#arguments}
        :param comment: Specifies a comment for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#comment FunctionJavascript#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#enable_console_output FunctionJavascript#enable_console_output}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#id FunctionJavascript#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_secure: Specifies that the function is secure. By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#is_secure FunctionJavascript#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#log_level FunctionJavascript#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#metric_level FunctionJavascript#metric_level}
        :param null_input_behavior: Specifies the behavior of the function when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#null_input_behavior FunctionJavascript#null_input_behavior}
        :param return_results_behavior: Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#return_results_behavior FunctionJavascript#return_results_behavior}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#trace_level FunctionJavascript#trace_level}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189fdd9146a4c8a1f3c139274457e13f0a4796813e3c9b5b367f562bac47eca1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FunctionJavascriptConfig(
            database=database,
            function_definition=function_definition,
            name=name,
            return_type=return_type,
            schema=schema,
            arguments=arguments,
            comment=comment,
            enable_console_output=enable_console_output,
            id=id,
            is_secure=is_secure,
            log_level=log_level,
            metric_level=metric_level,
            null_input_behavior=null_input_behavior,
            return_results_behavior=return_results_behavior,
            trace_level=trace_level,
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
        '''Generates CDKTF code for importing a FunctionJavascript resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FunctionJavascript to import.
        :param import_from_id: The id of the existing FunctionJavascript that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FunctionJavascript to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3365539fbd62fc58232a0801f6262c9b1947b63b3a43744d7e7affcaa813c4b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavascriptArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103fefa7db636be7941bb32d042fd9df0a4205b5a71ed0204c85bfe38b3ac446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArguments", [value]))

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetEnableConsoleOutput")
    def reset_enable_console_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConsoleOutput", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsSecure")
    def reset_is_secure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSecure", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetMetricLevel")
    def reset_metric_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricLevel", []))

    @jsii.member(jsii_name="resetNullInputBehavior")
    def reset_null_input_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNullInputBehavior", []))

    @jsii.member(jsii_name="resetReturnResultsBehavior")
    def reset_return_results_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnResultsBehavior", []))

    @jsii.member(jsii_name="resetTraceLevel")
    def reset_trace_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraceLevel", []))

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
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> "FunctionJavascriptArgumentsList":
        return typing.cast("FunctionJavascriptArgumentsList", jsii.get(self, "arguments"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="functionLanguage")
    def function_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionLanguage"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "FunctionJavascriptParametersList":
        return typing.cast("FunctionJavascriptParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "FunctionJavascriptShowOutputList":
        return typing.cast("FunctionJavascriptShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavascriptArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavascriptArguments"]]], jsii.get(self, "argumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutputInput")
    def enable_console_output_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConsoleOutputInput"))

    @builtins.property
    @jsii.member(jsii_name="functionDefinitionInput")
    def function_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isSecureInput")
    def is_secure_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "isSecureInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="metricLevelInput")
    def metric_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nullInputBehaviorInput")
    def null_input_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nullInputBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="returnResultsBehaviorInput")
    def return_results_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnResultsBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="returnTypeInput")
    def return_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="traceLevelInput")
    def trace_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "traceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e90c495ccf3e5e5f9dc7a0e315549581eed4a8e93e62ad84eb64dd5948ae49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79229edf51a6643138ee94761eb97fa93927252e3b64487b874c20d7f09b9eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConsoleOutput"))

    @enable_console_output.setter
    def enable_console_output(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef40f64884c867e0e230a615513611e31f19123a578db5d8b01d20d1a84076a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsoleOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionDefinition")
    def function_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionDefinition"))

    @function_definition.setter
    def function_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180c35a338246cc29b98e1a8ff90aa6bfc8dbcd08aee15b4a6881c8f9398ec58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54861d4990d224ec5ac50da9420960d9130d1cafc4d05940c1040cf47260f093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isSecure"))

    @is_secure.setter
    def is_secure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a013d743deead32d49447f4fe7f671e7c08230bf746e72a50907087093a8cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03728b91e262c256571338678d936bd274876b91afa99e16ec7ba1b6fbddbefc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricLevel"))

    @metric_level.setter
    def metric_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce2a5cddc31ca5bfdcf230a0edc0f67380ebafdbf3e8f22cda982d9ccbf2d99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf6a62621d407ae308f0265c63987dbf398b002322efdc08b24b72fc9dd2d10e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullInputBehavior")
    def null_input_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullInputBehavior"))

    @null_input_behavior.setter
    def null_input_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74416cb38c17ea3457d55c86766ced56f43d2dbe5f5454e79e013ce356abe921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullInputBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnResultsBehavior")
    def return_results_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnResultsBehavior"))

    @return_results_behavior.setter
    def return_results_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb58f28d53980a48c7ba4c70eda01818c17518bdbb02a305939e5d61797d34fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnResultsBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89eda88a1cc0135a56468bf02c6caab7130170cf89483e7509f1c9eb0852b83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34a2a47a812b12ae1590c81206d944a4fd69b44a3f74b3cf827759b7c76ee2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffc33e18259da718e34afe9425726a02b03b0358e6bfdafa4c66fa54d97f4c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptArguments",
    jsii_struct_bases=[],
    name_mapping={
        "arg_data_type": "argDataType",
        "arg_name": "argName",
        "arg_default_value": "argDefaultValue",
    },
)
class FunctionJavascriptArguments:
    def __init__(
        self,
        *,
        arg_data_type: builtins.str,
        arg_name: builtins.str,
        arg_default_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arg_data_type: The argument type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arg_data_type FunctionJavascript#arg_data_type}
        :param arg_name: The argument name. The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the function definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arg_name FunctionJavascript#arg_name}
        :param arg_default_value: Optional default value for the argument. For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arg_default_value FunctionJavascript#arg_default_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4684b4f21d2bb85dfeeede36f7cca5f8082ad5d4d616c2884a29dcdd0ecd55)
            check_type(argname="argument arg_data_type", value=arg_data_type, expected_type=type_hints["arg_data_type"])
            check_type(argname="argument arg_name", value=arg_name, expected_type=type_hints["arg_name"])
            check_type(argname="argument arg_default_value", value=arg_default_value, expected_type=type_hints["arg_default_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arg_data_type": arg_data_type,
            "arg_name": arg_name,
        }
        if arg_default_value is not None:
            self._values["arg_default_value"] = arg_default_value

    @builtins.property
    def arg_data_type(self) -> builtins.str:
        '''The argument type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arg_data_type FunctionJavascript#arg_data_type}
        '''
        result = self._values.get("arg_data_type")
        assert result is not None, "Required property 'arg_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_name(self) -> builtins.str:
        '''The argument name.

        The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the function definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arg_name FunctionJavascript#arg_name}
        '''
        result = self._values.get("arg_name")
        assert result is not None, "Required property 'arg_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_default_value(self) -> typing.Optional[builtins.str]:
        '''Optional default value for the argument.

        For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arg_default_value FunctionJavascript#arg_default_value}
        '''
        result = self._values.get("arg_default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavascriptArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavascriptArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptArgumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3af67c1109074464ce3ad5aabca470f05cd2fba928f991ed854997173fe8af6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionJavascriptArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa14b7eaa5bda2513af6a6ac6ac0f0627db07777152f214f4d0a09122fe27d39)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavascriptArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3799fde111f084e30c8b457cb68b9d126435ded5d4e66f080fbadff3c855c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83be06ae8800f67cbbedd5ee70f6022ff1857d687075f732524e04b9d39d151d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d59e46bec38395d3f17041d0468dd94bfe8c519960266cc8c8c956fe9aefdab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavascriptArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavascriptArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavascriptArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82955031024af5fde456796baddcb96193b3aae831491cb132ffc0ab6b6d9a94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionJavascriptArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptArgumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da8e760397d2b311ad75670affd3808cd901a6218943bd537b99e83e3a48f23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetArgDefaultValue")
    def reset_arg_default_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgDefaultValue", []))

    @builtins.property
    @jsii.member(jsii_name="argDataTypeInput")
    def arg_data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argDataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="argDefaultValueInput")
    def arg_default_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argDefaultValueInput"))

    @builtins.property
    @jsii.member(jsii_name="argNameInput")
    def arg_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argNameInput"))

    @builtins.property
    @jsii.member(jsii_name="argDataType")
    def arg_data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argDataType"))

    @arg_data_type.setter
    def arg_data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a53f6d1ce3e12f47ed88d0d54b36deb04927e574fff150f00790859b51ab8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argDefaultValue")
    def arg_default_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argDefaultValue"))

    @arg_default_value.setter
    def arg_default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831ea9708776f9a60e7648271191daa241d289c7afdb0bbbd652fb4b49184573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDefaultValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argName")
    def arg_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argName"))

    @arg_name.setter
    def arg_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b676745b9d31d92ce3d0c96056845b731ec290b48621d83510665baca04690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavascriptArguments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavascriptArguments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavascriptArguments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dce54704637a51036780f8932d3c8b154abfc2b0e545134e9eacf8b5bfffe328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "database": "database",
        "function_definition": "functionDefinition",
        "name": "name",
        "return_type": "returnType",
        "schema": "schema",
        "arguments": "arguments",
        "comment": "comment",
        "enable_console_output": "enableConsoleOutput",
        "id": "id",
        "is_secure": "isSecure",
        "log_level": "logLevel",
        "metric_level": "metricLevel",
        "null_input_behavior": "nullInputBehavior",
        "return_results_behavior": "returnResultsBehavior",
        "trace_level": "traceLevel",
    },
)
class FunctionJavascriptConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        database: builtins.str,
        function_definition: builtins.str,
        name: builtins.str,
        return_type: builtins.str,
        schema: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavascriptArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        return_results_behavior: typing.Optional[builtins.str] = None,
        trace_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param database: The database in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#database FunctionJavascript#database}
        :param function_definition: Defines the handler code executed when the UDF is called. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be JavaScript source code. For more information, see `Introduction to JavaScript UDFs <https://docs.snowflake.com/en/developer-guide/udf/javascript/udf-javascript-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#function_definition FunctionJavascript#function_definition}
        :param name: The name of the function; the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#name FunctionJavascript#name}
        :param return_type: Specifies the results returned by the UDF, which determines the UDF type. Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#return_type FunctionJavascript#return_type}
        :param schema: The schema in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#schema FunctionJavascript#schema}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arguments FunctionJavascript#arguments}
        :param comment: Specifies a comment for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#comment FunctionJavascript#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#enable_console_output FunctionJavascript#enable_console_output}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#id FunctionJavascript#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_secure: Specifies that the function is secure. By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#is_secure FunctionJavascript#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#log_level FunctionJavascript#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#metric_level FunctionJavascript#metric_level}
        :param null_input_behavior: Specifies the behavior of the function when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#null_input_behavior FunctionJavascript#null_input_behavior}
        :param return_results_behavior: Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#return_results_behavior FunctionJavascript#return_results_behavior}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#trace_level FunctionJavascript#trace_level}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7cf20932a2562d16b8440c61250e3b4cd16928008a5cf58f90d11b7256cf9fb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument function_definition", value=function_definition, expected_type=type_hints["function_definition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enable_console_output", value=enable_console_output, expected_type=type_hints["enable_console_output"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_secure", value=is_secure, expected_type=type_hints["is_secure"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument metric_level", value=metric_level, expected_type=type_hints["metric_level"])
            check_type(argname="argument null_input_behavior", value=null_input_behavior, expected_type=type_hints["null_input_behavior"])
            check_type(argname="argument return_results_behavior", value=return_results_behavior, expected_type=type_hints["return_results_behavior"])
            check_type(argname="argument trace_level", value=trace_level, expected_type=type_hints["trace_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "function_definition": function_definition,
            "name": name,
            "return_type": return_type,
            "schema": schema,
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
        if arguments is not None:
            self._values["arguments"] = arguments
        if comment is not None:
            self._values["comment"] = comment
        if enable_console_output is not None:
            self._values["enable_console_output"] = enable_console_output
        if id is not None:
            self._values["id"] = id
        if is_secure is not None:
            self._values["is_secure"] = is_secure
        if log_level is not None:
            self._values["log_level"] = log_level
        if metric_level is not None:
            self._values["metric_level"] = metric_level
        if null_input_behavior is not None:
            self._values["null_input_behavior"] = null_input_behavior
        if return_results_behavior is not None:
            self._values["return_results_behavior"] = return_results_behavior
        if trace_level is not None:
            self._values["trace_level"] = trace_level

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
    def database(self) -> builtins.str:
        '''The database in which to create the function.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#database FunctionJavascript#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_definition(self) -> builtins.str:
        '''Defines the handler code executed when the UDF is called.

        Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be JavaScript source code. For more information, see `Introduction to JavaScript UDFs <https://docs.snowflake.com/en/developer-guide/udf/javascript/udf-javascript-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#function_definition FunctionJavascript#function_definition}
        '''
        result = self._values.get("function_definition")
        assert result is not None, "Required property 'function_definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the function;

        the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#name FunctionJavascript#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def return_type(self) -> builtins.str:
        '''Specifies the results returned by the UDF, which determines the UDF type.

        Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#return_type FunctionJavascript#return_type}
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the function.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#schema FunctionJavascript#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavascriptArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#arguments FunctionJavascript#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavascriptArguments]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#comment FunctionJavascript#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_console_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable stdout/stderr fast path logging for anonyous stored procs.

        This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#enable_console_output FunctionJavascript#enable_console_output}
        '''
        result = self._values.get("enable_console_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#id FunctionJavascript#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_secure(self) -> typing.Optional[builtins.str]:
        '''Specifies that the function is secure.

        By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#is_secure FunctionJavascript#is_secure}
        '''
        result = self._values.get("is_secure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#log_level FunctionJavascript#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_level(self) -> typing.Optional[builtins.str]:
        '''METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#metric_level FunctionJavascript#metric_level}
        '''
        result = self._values.get("metric_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def null_input_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the function when called with null inputs.

        Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#null_input_behavior FunctionJavascript#null_input_behavior}
        '''
        result = self._values.get("null_input_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def return_results_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#return_results_behavior FunctionJavascript#return_results_behavior}
        '''
        result = self._values.get("return_results_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_javascript#trace_level FunctionJavascript#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavascriptConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavascriptParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavascriptParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersEnableConsoleOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavascriptParametersEnableConsoleOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavascriptParametersEnableConsoleOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavascriptParametersEnableConsoleOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersEnableConsoleOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5bed0f25c88d3c7d517622ea68bd8d98adf8e5e3d683b8263ffbfe2c8a86405)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionJavascriptParametersEnableConsoleOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f93d9af8323338bec9acfe5fc9f1b8c01677948b63d502fc01db26cf27ad7e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavascriptParametersEnableConsoleOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05568279f71fdf6dfd01b8243702787ec825bc9e9f265cd54e251f9bf8a6ad14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42c103fb0d434e82efac176ab5d03f9acbf2eb9c984d26028c9d964eecd31011)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a18c980a586cdf06e2a2aad93e085906d369ee466654b9fcb08ddb7871d3a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavascriptParametersEnableConsoleOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersEnableConsoleOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5610a5b66d404592951366c08fa67a88acff406ae6bf8f730da003cbee454d8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionJavascriptParametersEnableConsoleOutput]:
        return typing.cast(typing.Optional[FunctionJavascriptParametersEnableConsoleOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavascriptParametersEnableConsoleOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015f81c10b39f43a15b34127136395b56e0ac6ed8d2333d89def027546291ec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionJavascriptParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__676b3049bbbb61668cbf4b5728a886bd0374f5704309b8ef1d429a04864052d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionJavascriptParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__488395c7a22c3b4f0bf08d80a8978d5a344a8a53455a973b2937c8b7d0f87742)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavascriptParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8c0743fb4bf274e4b5a4543dbfe57f519bfe9ee7643c2e482f1066af29a9e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63b1bba8d09f36465411bf0651edfb0a5fb177c0c8ef14705315daa9f446ee1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ed15f0f271aaf61e055f6d0380053356f71c753c70aeea5334f5ccb72feedf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavascriptParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavascriptParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavascriptParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa75dd363ad0802163ef6e68d24698aa1a034122a9b77d6cbff096ff522f1003)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionJavascriptParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d02537187cb97478cdbc82088a20567ea7db7a76fd8015f3a77d5bb64085d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavascriptParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1761e59ed7aa86a039d0a2a8a7b2c0ba90325e16bc195f23e84c0dc67505101b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfb8d31f1a18f5d28e5423e368e59dbabed9d76787ed99e9fb46ba967e148556)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2de1612e745b850db4dc1e90bea77d0b66df1120d9a055c3aa4130d1224a9680)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavascriptParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c23952babf2551c9a0adb32643312d48682fe7658f3fad68de0dd967313f7fef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionJavascriptParametersLogLevel]:
        return typing.cast(typing.Optional[FunctionJavascriptParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavascriptParametersLogLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb51049d86d34764a90a5878c4db1bf7b006741b046efa75efce61289688332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersMetricLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavascriptParametersMetricLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavascriptParametersMetricLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavascriptParametersMetricLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersMetricLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4132713790a0d9d185d6f82e701aec9432930c32303498b7d1f7168244eb9ba2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionJavascriptParametersMetricLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97edf265050df1167b44618ca22c4ee03b94c95c91353661ec2ff2e4901ea2af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavascriptParametersMetricLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be4baca056a8dcdf88627d25850a0a9fc0468fa350208bfd0675d4b99014fb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75fe49265785913c33f4125279a0e1e033bcec83c063e0206b1c1f79c093951a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76b56a13777f371352a70a6186ee6a0d1eb61f546e5b0e948b7eb8a7f919c259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavascriptParametersMetricLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersMetricLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90213b861ba6bb02601a7626b8179aad20d5712991bd625dea027f561f20f985)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionJavascriptParametersMetricLevel]:
        return typing.cast(typing.Optional[FunctionJavascriptParametersMetricLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavascriptParametersMetricLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a4cd395ce7ad03ff740ff3f83cb7923efa8c09ebcf4120853d3bec18ecd334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionJavascriptParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c37efc476850de370cda24a799f42ae53c035d904ac87001c4acaedf958bbc3b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(
        self,
    ) -> FunctionJavascriptParametersEnableConsoleOutputList:
        return typing.cast(FunctionJavascriptParametersEnableConsoleOutputList, jsii.get(self, "enableConsoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> FunctionJavascriptParametersLogLevelList:
        return typing.cast(FunctionJavascriptParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> FunctionJavascriptParametersMetricLevelList:
        return typing.cast(FunctionJavascriptParametersMetricLevelList, jsii.get(self, "metricLevel"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "FunctionJavascriptParametersTraceLevelList":
        return typing.cast("FunctionJavascriptParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionJavascriptParameters]:
        return typing.cast(typing.Optional[FunctionJavascriptParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavascriptParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d292f880718248a05a99d4efe5266bd3d5280a07f33f8aa247fb531e581e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavascriptParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavascriptParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavascriptParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d264d93a520a61cedcbc80b5373703b5b6fc86f5bbb3a90ed4b65acff5a630b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionJavascriptParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0aea72c74000bb3740b3604f5c48479c23fd0ea640d01893293ec8200122f66)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavascriptParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cdff50eaa3f850c5ab407c2bd9654b7852c773651484bd37c722d38c49b77ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7e950e681d384d47c0db46223a62e834a5b8f4b05ece2bad8a9935d2a285d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0f56630cd30b16c3a56178400c8858466b55bf4a0f7c456ee7a10478027a092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavascriptParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__feb8cb4bb1e33f5810e3b1f5273f13d96f5ef66cccdf39a871cb80adfad650b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "default"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionJavascriptParametersTraceLevel]:
        return typing.cast(typing.Optional[FunctionJavascriptParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavascriptParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a68d3b276219d88b5c7938b38ee8a57f6a90a2634329affd44cedf7f8e862e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavascriptShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavascriptShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavascriptShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6d2dfee4c8e4521fafd36d48c48f993b5ad05df965ef4e84da5e5b6afcdde02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionJavascriptShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3287fb231d35b5f946e605cb15c8531c96398bbf12ecf2d17c39aeeddacf3f8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavascriptShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015f8a7bb151935eb5e77892b6009a51d269e79931d0331bc16da7c6a6cc897a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86d1de414f17758e4ec23d8cec3310c36dcc5e50f2bfa1d63c3ebe867f25f157)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09a2e83f8a9907d2b502ccda9b8109481db251aae924e8b867d5b037e0edfe7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavascriptShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJavascript.FunctionJavascriptShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f71adebb43b6d7b161cf17136d8cdd8ef59bf7bd0fc573318461bd44d2a8c793)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="argumentsRaw")
    def arguments_raw(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argumentsRaw"))

    @builtins.property
    @jsii.member(jsii_name="catalogName")
    def catalog_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalogName"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrations")
    def external_access_integrations(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalAccessIntegrations"))

    @builtins.property
    @jsii.member(jsii_name="isAggregate")
    def is_aggregate(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isAggregate"))

    @builtins.property
    @jsii.member(jsii_name="isAnsi")
    def is_ansi(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isAnsi"))

    @builtins.property
    @jsii.member(jsii_name="isBuiltin")
    def is_builtin(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isBuiltin"))

    @builtins.property
    @jsii.member(jsii_name="isDataMetric")
    def is_data_metric(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isDataMetric"))

    @builtins.property
    @jsii.member(jsii_name="isExternalFunction")
    def is_external_function(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isExternalFunction"))

    @builtins.property
    @jsii.member(jsii_name="isMemoizable")
    def is_memoizable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isMemoizable"))

    @builtins.property
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isSecure"))

    @builtins.property
    @jsii.member(jsii_name="isTableFunction")
    def is_table_function(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isTableFunction"))

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @builtins.property
    @jsii.member(jsii_name="maxNumArguments")
    def max_num_arguments(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxNumArguments"))

    @builtins.property
    @jsii.member(jsii_name="minNumArguments")
    def min_num_arguments(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNumArguments"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="schemaName")
    def schema_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schemaName"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="validForClustering")
    def valid_for_clustering(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "validForClustering"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionJavascriptShowOutput]:
        return typing.cast(typing.Optional[FunctionJavascriptShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavascriptShowOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd74c92b843d032a3e35a978cbe766bc93c239400a0590bd9556c130d94c2ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FunctionJavascript",
    "FunctionJavascriptArguments",
    "FunctionJavascriptArgumentsList",
    "FunctionJavascriptArgumentsOutputReference",
    "FunctionJavascriptConfig",
    "FunctionJavascriptParameters",
    "FunctionJavascriptParametersEnableConsoleOutput",
    "FunctionJavascriptParametersEnableConsoleOutputList",
    "FunctionJavascriptParametersEnableConsoleOutputOutputReference",
    "FunctionJavascriptParametersList",
    "FunctionJavascriptParametersLogLevel",
    "FunctionJavascriptParametersLogLevelList",
    "FunctionJavascriptParametersLogLevelOutputReference",
    "FunctionJavascriptParametersMetricLevel",
    "FunctionJavascriptParametersMetricLevelList",
    "FunctionJavascriptParametersMetricLevelOutputReference",
    "FunctionJavascriptParametersOutputReference",
    "FunctionJavascriptParametersTraceLevel",
    "FunctionJavascriptParametersTraceLevelList",
    "FunctionJavascriptParametersTraceLevelOutputReference",
    "FunctionJavascriptShowOutput",
    "FunctionJavascriptShowOutputList",
    "FunctionJavascriptShowOutputOutputReference",
]

publication.publish()

def _typecheckingstub__189fdd9146a4c8a1f3c139274457e13f0a4796813e3c9b5b367f562bac47eca1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    function_definition: builtins.str,
    name: builtins.str,
    return_type: builtins.str,
    schema: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavascriptArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    return_results_behavior: typing.Optional[builtins.str] = None,
    trace_level: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__3365539fbd62fc58232a0801f6262c9b1947b63b3a43744d7e7affcaa813c4b7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103fefa7db636be7941bb32d042fd9df0a4205b5a71ed0204c85bfe38b3ac446(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavascriptArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e90c495ccf3e5e5f9dc7a0e315549581eed4a8e93e62ad84eb64dd5948ae49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79229edf51a6643138ee94761eb97fa93927252e3b64487b874c20d7f09b9eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef40f64884c867e0e230a615513611e31f19123a578db5d8b01d20d1a84076a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180c35a338246cc29b98e1a8ff90aa6bfc8dbcd08aee15b4a6881c8f9398ec58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54861d4990d224ec5ac50da9420960d9130d1cafc4d05940c1040cf47260f093(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a013d743deead32d49447f4fe7f671e7c08230bf746e72a50907087093a8cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03728b91e262c256571338678d936bd274876b91afa99e16ec7ba1b6fbddbefc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2a5cddc31ca5bfdcf230a0edc0f67380ebafdbf3e8f22cda982d9ccbf2d99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf6a62621d407ae308f0265c63987dbf398b002322efdc08b24b72fc9dd2d10e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74416cb38c17ea3457d55c86766ced56f43d2dbe5f5454e79e013ce356abe921(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb58f28d53980a48c7ba4c70eda01818c17518bdbb02a305939e5d61797d34fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89eda88a1cc0135a56468bf02c6caab7130170cf89483e7509f1c9eb0852b83a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34a2a47a812b12ae1590c81206d944a4fd69b44a3f74b3cf827759b7c76ee2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc33e18259da718e34afe9425726a02b03b0358e6bfdafa4c66fa54d97f4c76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4684b4f21d2bb85dfeeede36f7cca5f8082ad5d4d616c2884a29dcdd0ecd55(
    *,
    arg_data_type: builtins.str,
    arg_name: builtins.str,
    arg_default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af67c1109074464ce3ad5aabca470f05cd2fba928f991ed854997173fe8af6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa14b7eaa5bda2513af6a6ac6ac0f0627db07777152f214f4d0a09122fe27d39(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3799fde111f084e30c8b457cb68b9d126435ded5d4e66f080fbadff3c855c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83be06ae8800f67cbbedd5ee70f6022ff1857d687075f732524e04b9d39d151d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d59e46bec38395d3f17041d0468dd94bfe8c519960266cc8c8c956fe9aefdab(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82955031024af5fde456796baddcb96193b3aae831491cb132ffc0ab6b6d9a94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavascriptArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da8e760397d2b311ad75670affd3808cd901a6218943bd537b99e83e3a48f23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a53f6d1ce3e12f47ed88d0d54b36deb04927e574fff150f00790859b51ab8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831ea9708776f9a60e7648271191daa241d289c7afdb0bbbd652fb4b49184573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b676745b9d31d92ce3d0c96056845b731ec290b48621d83510665baca04690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce54704637a51036780f8932d3c8b154abfc2b0e545134e9eacf8b5bfffe328(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavascriptArguments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cf20932a2562d16b8440c61250e3b4cd16928008a5cf58f90d11b7256cf9fb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    function_definition: builtins.str,
    name: builtins.str,
    return_type: builtins.str,
    schema: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavascriptArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    return_results_behavior: typing.Optional[builtins.str] = None,
    trace_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5bed0f25c88d3c7d517622ea68bd8d98adf8e5e3d683b8263ffbfe2c8a86405(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f93d9af8323338bec9acfe5fc9f1b8c01677948b63d502fc01db26cf27ad7e8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05568279f71fdf6dfd01b8243702787ec825bc9e9f265cd54e251f9bf8a6ad14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c103fb0d434e82efac176ab5d03f9acbf2eb9c984d26028c9d964eecd31011(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a18c980a586cdf06e2a2aad93e085906d369ee466654b9fcb08ddb7871d3a06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5610a5b66d404592951366c08fa67a88acff406ae6bf8f730da003cbee454d8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015f81c10b39f43a15b34127136395b56e0ac6ed8d2333d89def027546291ec8(
    value: typing.Optional[FunctionJavascriptParametersEnableConsoleOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676b3049bbbb61668cbf4b5728a886bd0374f5704309b8ef1d429a04864052d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__488395c7a22c3b4f0bf08d80a8978d5a344a8a53455a973b2937c8b7d0f87742(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8c0743fb4bf274e4b5a4543dbfe57f519bfe9ee7643c2e482f1066af29a9e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63b1bba8d09f36465411bf0651edfb0a5fb177c0c8ef14705315daa9f446ee1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed15f0f271aaf61e055f6d0380053356f71c753c70aeea5334f5ccb72feedf7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa75dd363ad0802163ef6e68d24698aa1a034122a9b77d6cbff096ff522f1003(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d02537187cb97478cdbc82088a20567ea7db7a76fd8015f3a77d5bb64085d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1761e59ed7aa86a039d0a2a8a7b2c0ba90325e16bc195f23e84c0dc67505101b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb8d31f1a18f5d28e5423e368e59dbabed9d76787ed99e9fb46ba967e148556(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de1612e745b850db4dc1e90bea77d0b66df1120d9a055c3aa4130d1224a9680(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23952babf2551c9a0adb32643312d48682fe7658f3fad68de0dd967313f7fef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb51049d86d34764a90a5878c4db1bf7b006741b046efa75efce61289688332(
    value: typing.Optional[FunctionJavascriptParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4132713790a0d9d185d6f82e701aec9432930c32303498b7d1f7168244eb9ba2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97edf265050df1167b44618ca22c4ee03b94c95c91353661ec2ff2e4901ea2af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be4baca056a8dcdf88627d25850a0a9fc0468fa350208bfd0675d4b99014fb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75fe49265785913c33f4125279a0e1e033bcec83c063e0206b1c1f79c093951a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b56a13777f371352a70a6186ee6a0d1eb61f546e5b0e948b7eb8a7f919c259(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90213b861ba6bb02601a7626b8179aad20d5712991bd625dea027f561f20f985(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a4cd395ce7ad03ff740ff3f83cb7923efa8c09ebcf4120853d3bec18ecd334(
    value: typing.Optional[FunctionJavascriptParametersMetricLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37efc476850de370cda24a799f42ae53c035d904ac87001c4acaedf958bbc3b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d292f880718248a05a99d4efe5266bd3d5280a07f33f8aa247fb531e581e88(
    value: typing.Optional[FunctionJavascriptParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d264d93a520a61cedcbc80b5373703b5b6fc86f5bbb3a90ed4b65acff5a630b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0aea72c74000bb3740b3604f5c48479c23fd0ea640d01893293ec8200122f66(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cdff50eaa3f850c5ab407c2bd9654b7852c773651484bd37c722d38c49b77ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7e950e681d384d47c0db46223a62e834a5b8f4b05ece2bad8a9935d2a285d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f56630cd30b16c3a56178400c8858466b55bf4a0f7c456ee7a10478027a092(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb8cb4bb1e33f5810e3b1f5273f13d96f5ef66cccdf39a871cb80adfad650b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a68d3b276219d88b5c7938b38ee8a57f6a90a2634329affd44cedf7f8e862e8(
    value: typing.Optional[FunctionJavascriptParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d2dfee4c8e4521fafd36d48c48f993b5ad05df965ef4e84da5e5b6afcdde02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3287fb231d35b5f946e605cb15c8531c96398bbf12ecf2d17c39aeeddacf3f8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015f8a7bb151935eb5e77892b6009a51d269e79931d0331bc16da7c6a6cc897a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d1de414f17758e4ec23d8cec3310c36dcc5e50f2bfa1d63c3ebe867f25f157(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a2e83f8a9907d2b502ccda9b8109481db251aae924e8b867d5b037e0edfe7c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71adebb43b6d7b161cf17136d8cdd8ef59bf7bd0fc573318461bd44d2a8c793(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd74c92b843d032a3e35a978cbe766bc93c239400a0590bd9556c130d94c2ec(
    value: typing.Optional[FunctionJavascriptShowOutput],
) -> None:
    """Type checking stubs"""
    pass

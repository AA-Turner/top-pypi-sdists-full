r'''
# `snowflake_function_java`

Refer to the Terraform Registry for docs: [`snowflake_function_java`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java).
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


class FunctionJava(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJava",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java snowflake_function_java}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        handler: builtins.str,
        name: builtins.str,
        return_type: builtins.str,
        schema: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavaArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        function_definition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavaImports", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        return_results_behavior: typing.Optional[builtins.str] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavaSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_path: typing.Optional[typing.Union["FunctionJavaTargetPath", typing.Dict[builtins.str, typing.Any]]] = None,
        trace_level: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java snowflake_function_java} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#database FunctionJava#database}
        :param handler: The name of the handler method or class. If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a method name, as in the following form: ``MyClass.myMethod``. If the handler is for a tabular UDF, the HANDLER value should be the name of a handler class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#handler FunctionJava#handler}
        :param name: The name of the function; the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#name FunctionJava#name}
        :param return_type: Specifies the results returned by the UDF, which determines the UDF type. Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#return_type FunctionJava#return_type}
        :param schema: The schema in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#schema FunctionJava#schema}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arguments FunctionJava#arguments}
        :param comment: Specifies a comment for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#comment FunctionJava#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#enable_console_output FunctionJava#enable_console_output}
        :param external_access_integrations: The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this function’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#external_access_integrations FunctionJava#external_access_integrations}
        :param function_definition: Defines the handler code executed when the UDF is called. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be Java source code. For more information, see `Introduction to Java UDFs <https://docs.snowflake.com/en/developer-guide/udf/java/udf-java-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#function_definition FunctionJava#function_definition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#id FunctionJava#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: imports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#imports FunctionJava#imports}
        :param is_secure: Specifies that the function is secure. By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#is_secure FunctionJava#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#log_level FunctionJava#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#metric_level FunctionJava#metric_level}
        :param null_input_behavior: Specifies the behavior of the function when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#null_input_behavior FunctionJava#null_input_behavior}
        :param packages: The name and version number of Snowflake system packages required as dependencies. The value should be of the form ``package_name:version_number``, where ``package_name`` is ``snowflake_domain:package``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#packages FunctionJava#packages}
        :param return_results_behavior: Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#return_results_behavior FunctionJava#return_results_behavior}
        :param runtime_version: Specifies the Java JDK runtime version to use. The supported versions of Java are 11.x and 17.x. If RUNTIME_VERSION is not set, Java JDK 11 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#runtime_version FunctionJava#runtime_version}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#secrets FunctionJava#secrets}
        :param target_path: target_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#target_path FunctionJava#target_path}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#trace_level FunctionJava#trace_level}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22afeb6cf4af18e7a4914f8b1a23098516db9232cf41ec5eeb4955952bf6297e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FunctionJavaConfig(
            database=database,
            handler=handler,
            name=name,
            return_type=return_type,
            schema=schema,
            arguments=arguments,
            comment=comment,
            enable_console_output=enable_console_output,
            external_access_integrations=external_access_integrations,
            function_definition=function_definition,
            id=id,
            imports=imports,
            is_secure=is_secure,
            log_level=log_level,
            metric_level=metric_level,
            null_input_behavior=null_input_behavior,
            packages=packages,
            return_results_behavior=return_results_behavior,
            runtime_version=runtime_version,
            secrets=secrets,
            target_path=target_path,
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
        '''Generates CDKTF code for importing a FunctionJava resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FunctionJava to import.
        :param import_from_id: The id of the existing FunctionJava that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FunctionJava to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__992a0037b165566141295a88d9efbb101de815dc34d29728f964b58da1a496b7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavaArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f4dabfc7f8e4b35c317c2aaaa74314d6989994f6ee31499ceb4c05c0073f94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArguments", [value]))

    @jsii.member(jsii_name="putImports")
    def put_imports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavaImports", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13597aecd048881d177daca072bf75b7e0476b80d90fa83e1284564706848ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putImports", [value]))

    @jsii.member(jsii_name="putSecrets")
    def put_secrets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavaSecrets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a2a37a69d129e854ece5e87872a1ef9f1d70b3438e92111a122e00c701da06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSecrets", [value]))

    @jsii.member(jsii_name="putTargetPath")
    def put_target_path(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#path_on_stage FunctionJava#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#stage_location FunctionJava#stage_location}
        '''
        value = FunctionJavaTargetPath(
            path_on_stage=path_on_stage, stage_location=stage_location
        )

        return typing.cast(None, jsii.invoke(self, "putTargetPath", [value]))

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @jsii.member(jsii_name="resetEnableConsoleOutput")
    def reset_enable_console_output(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConsoleOutput", []))

    @jsii.member(jsii_name="resetExternalAccessIntegrations")
    def reset_external_access_integrations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAccessIntegrations", []))

    @jsii.member(jsii_name="resetFunctionDefinition")
    def reset_function_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionDefinition", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImports")
    def reset_imports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImports", []))

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

    @jsii.member(jsii_name="resetPackages")
    def reset_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPackages", []))

    @jsii.member(jsii_name="resetReturnResultsBehavior")
    def reset_return_results_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnResultsBehavior", []))

    @jsii.member(jsii_name="resetRuntimeVersion")
    def reset_runtime_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeVersion", []))

    @jsii.member(jsii_name="resetSecrets")
    def reset_secrets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecrets", []))

    @jsii.member(jsii_name="resetTargetPath")
    def reset_target_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetPath", []))

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
    def arguments(self) -> "FunctionJavaArgumentsList":
        return typing.cast("FunctionJavaArgumentsList", jsii.get(self, "arguments"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="functionLanguage")
    def function_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionLanguage"))

    @builtins.property
    @jsii.member(jsii_name="imports")
    def imports(self) -> "FunctionJavaImportsList":
        return typing.cast("FunctionJavaImportsList", jsii.get(self, "imports"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "FunctionJavaParametersList":
        return typing.cast("FunctionJavaParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "FunctionJavaSecretsList":
        return typing.cast("FunctionJavaSecretsList", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "FunctionJavaShowOutputList":
        return typing.cast("FunctionJavaShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="targetPath")
    def target_path(self) -> "FunctionJavaTargetPathOutputReference":
        return typing.cast("FunctionJavaTargetPathOutputReference", jsii.get(self, "targetPath"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaArguments"]]], jsii.get(self, "argumentsInput"))

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
    @jsii.member(jsii_name="externalAccessIntegrationsInput")
    def external_access_integrations_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalAccessIntegrationsInput"))

    @builtins.property
    @jsii.member(jsii_name="functionDefinitionInput")
    def function_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionDefinitionInput"))

    @builtins.property
    @jsii.member(jsii_name="handlerInput")
    def handler_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "handlerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importsInput")
    def imports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaImports"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaImports"]]], jsii.get(self, "importsInput"))

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
    @jsii.member(jsii_name="packagesInput")
    def packages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "packagesInput"))

    @builtins.property
    @jsii.member(jsii_name="returnResultsBehaviorInput")
    def return_results_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnResultsBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="returnTypeInput")
    def return_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="secretsInput")
    def secrets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaSecrets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaSecrets"]]], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPathInput")
    def target_path_input(self) -> typing.Optional["FunctionJavaTargetPath"]:
        return typing.cast(typing.Optional["FunctionJavaTargetPath"], jsii.get(self, "targetPathInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a1486ef707a6c61bc62d2df2e54e940cb4ec000d701d98241e1df860f9334b73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731e07e10eb61dd3561efd0df35da1d582ef70c11858a3bbc1c3d324ba7a19fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a162cbf599d87d067b3cdc62ba4c9e8342ffb15612086c6faacb5b265eb92acf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsoleOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrations")
    def external_access_integrations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalAccessIntegrations"))

    @external_access_integrations.setter
    def external_access_integrations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3e70fb0331942ef9235d0de2d65458609f843a3af3fbeab2d24dd50bcc14f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAccessIntegrations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionDefinition")
    def function_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionDefinition"))

    @function_definition.setter
    def function_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06f0ef1b7292f709b122ba7c8014d0963657afef30854bafa8d013e59f8bbff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050226d94329af043ed3fac8f1afef1974ae592b18d675a3cecf871b8bfaf5f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb985d9522ecaa4ceeba62142b878532311fd5f14ad87b28723aaf2cf2a5fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isSecure"))

    @is_secure.setter
    def is_secure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19334e0162640f622ae68567533ff148dedecc06ae23e931ce9afa5c50388a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a89d85674d42585065c34104698e14ffbe64e8818be758ef2a75de94e448da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricLevel"))

    @metric_level.setter
    def metric_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253ade4019a6d1c767d2c25a5c7db01a6c62f3b93efa6fd5424fdd99f763a0a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510eca69b84df320ace228a37126f79590ff44d92b59de710161baf34578dc9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullInputBehavior")
    def null_input_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullInputBehavior"))

    @null_input_behavior.setter
    def null_input_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b3620223c2787553eebac7a4a31118100ab95690faae2ecd4c0e229d8c809a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullInputBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packages")
    def packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packages"))

    @packages.setter
    def packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3db1d5f9b87ab53b9631f143abe05ba08c1f3aaea327f87fcd543b46aea4eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnResultsBehavior")
    def return_results_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnResultsBehavior"))

    @return_results_behavior.setter
    def return_results_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4288c66c1b79fea8e29eb50b2a0210cc407801508dac446cb2cfc57c66482f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnResultsBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9371dcb115a59dd8d307cf8835620103b42ca33501878cccfd0f76a8ab82bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccd427797e1315151744986a33630fde001bb07aaea04ca9698266d1da8e0ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fdb3489c5d5ec888a94483f5b50ab95aff90465dbb975600f689e1d6b686b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d1824813b19a6fe1adabd8d9aea058d99462c43debb246db653606a68ac4868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaArguments",
    jsii_struct_bases=[],
    name_mapping={
        "arg_data_type": "argDataType",
        "arg_name": "argName",
        "arg_default_value": "argDefaultValue",
    },
)
class FunctionJavaArguments:
    def __init__(
        self,
        *,
        arg_data_type: builtins.str,
        arg_name: builtins.str,
        arg_default_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arg_data_type: The argument type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arg_data_type FunctionJava#arg_data_type}
        :param arg_name: The argument name. The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the function definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arg_name FunctionJava#arg_name}
        :param arg_default_value: Optional default value for the argument. For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arg_default_value FunctionJava#arg_default_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b94e6f99976bfbfa68d4285b9058d6f498f445aaf109409427cffd969db9039)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arg_data_type FunctionJava#arg_data_type}
        '''
        result = self._values.get("arg_data_type")
        assert result is not None, "Required property 'arg_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_name(self) -> builtins.str:
        '''The argument name.

        The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the function definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arg_name FunctionJava#arg_name}
        '''
        result = self._values.get("arg_name")
        assert result is not None, "Required property 'arg_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_default_value(self) -> typing.Optional[builtins.str]:
        '''Optional default value for the argument.

        For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arg_default_value FunctionJava#arg_default_value}
        '''
        result = self._values.get("arg_default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaArgumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2fb7b27faf9ee9a924590564289427c1c68a9299ffd86b83c1d950288d30618)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionJavaArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b216142b82e4f90b3b80a4f0e3ba61f100c08729212cc1e4f34f4b684a9455c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3572fb2f3b8e510ff8da295a6fca65e9556bf67e00756608717f2e084c77741f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da7ce4e28cbe14b895290c317da5171850df9d5fec00b1e7987b219af3fde82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2097c821e6d5945c789be5651e9daa943c5f612cb0dffc3c0953cb418e08ee54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae013d98ec13cd615ab792c7cd29ac764d8b965cf92d9e337e81acc9374080b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionJavaArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaArgumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d1227bf859739eeae110f3ecb4b369bc451b1aa451b3f2c13545688e7dc2612)
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
            type_hints = typing.get_type_hints(_typecheckingstub__742d9a47041d6409e0645ed3b9c289a07d63bf9b022203c910cd5bccda590efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argDefaultValue")
    def arg_default_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argDefaultValue"))

    @arg_default_value.setter
    def arg_default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca84500a447d2c912a895995a1eac1098735f0bdb1c184e1c2a465ebedfc0f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDefaultValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argName")
    def arg_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argName"))

    @arg_name.setter
    def arg_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c631ee4b13378c32224ed906cb9fe629e0ab410c54d9528d58ee4c707db2582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaArguments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaArguments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaArguments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d08ee06821367e5824ed6a7bf3fed0ab793fee08f670f60ef10bf37327018af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaConfig",
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
        "handler": "handler",
        "name": "name",
        "return_type": "returnType",
        "schema": "schema",
        "arguments": "arguments",
        "comment": "comment",
        "enable_console_output": "enableConsoleOutput",
        "external_access_integrations": "externalAccessIntegrations",
        "function_definition": "functionDefinition",
        "id": "id",
        "imports": "imports",
        "is_secure": "isSecure",
        "log_level": "logLevel",
        "metric_level": "metricLevel",
        "null_input_behavior": "nullInputBehavior",
        "packages": "packages",
        "return_results_behavior": "returnResultsBehavior",
        "runtime_version": "runtimeVersion",
        "secrets": "secrets",
        "target_path": "targetPath",
        "trace_level": "traceLevel",
    },
)
class FunctionJavaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        handler: builtins.str,
        name: builtins.str,
        return_type: builtins.str,
        schema: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        function_definition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavaImports", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        return_results_behavior: typing.Optional[builtins.str] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionJavaSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_path: typing.Optional[typing.Union["FunctionJavaTargetPath", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param database: The database in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#database FunctionJava#database}
        :param handler: The name of the handler method or class. If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a method name, as in the following form: ``MyClass.myMethod``. If the handler is for a tabular UDF, the HANDLER value should be the name of a handler class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#handler FunctionJava#handler}
        :param name: The name of the function; the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#name FunctionJava#name}
        :param return_type: Specifies the results returned by the UDF, which determines the UDF type. Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#return_type FunctionJava#return_type}
        :param schema: The schema in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#schema FunctionJava#schema}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arguments FunctionJava#arguments}
        :param comment: Specifies a comment for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#comment FunctionJava#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#enable_console_output FunctionJava#enable_console_output}
        :param external_access_integrations: The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this function’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#external_access_integrations FunctionJava#external_access_integrations}
        :param function_definition: Defines the handler code executed when the UDF is called. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be Java source code. For more information, see `Introduction to Java UDFs <https://docs.snowflake.com/en/developer-guide/udf/java/udf-java-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#function_definition FunctionJava#function_definition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#id FunctionJava#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: imports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#imports FunctionJava#imports}
        :param is_secure: Specifies that the function is secure. By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#is_secure FunctionJava#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#log_level FunctionJava#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#metric_level FunctionJava#metric_level}
        :param null_input_behavior: Specifies the behavior of the function when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#null_input_behavior FunctionJava#null_input_behavior}
        :param packages: The name and version number of Snowflake system packages required as dependencies. The value should be of the form ``package_name:version_number``, where ``package_name`` is ``snowflake_domain:package``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#packages FunctionJava#packages}
        :param return_results_behavior: Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#return_results_behavior FunctionJava#return_results_behavior}
        :param runtime_version: Specifies the Java JDK runtime version to use. The supported versions of Java are 11.x and 17.x. If RUNTIME_VERSION is not set, Java JDK 11 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#runtime_version FunctionJava#runtime_version}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#secrets FunctionJava#secrets}
        :param target_path: target_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#target_path FunctionJava#target_path}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#trace_level FunctionJava#trace_level}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(target_path, dict):
            target_path = FunctionJavaTargetPath(**target_path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b192f611a3b78f973dd3de602a2812b1164e5bc00d21d3593d9b2f31d2b97655)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enable_console_output", value=enable_console_output, expected_type=type_hints["enable_console_output"])
            check_type(argname="argument external_access_integrations", value=external_access_integrations, expected_type=type_hints["external_access_integrations"])
            check_type(argname="argument function_definition", value=function_definition, expected_type=type_hints["function_definition"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument imports", value=imports, expected_type=type_hints["imports"])
            check_type(argname="argument is_secure", value=is_secure, expected_type=type_hints["is_secure"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument metric_level", value=metric_level, expected_type=type_hints["metric_level"])
            check_type(argname="argument null_input_behavior", value=null_input_behavior, expected_type=type_hints["null_input_behavior"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument return_results_behavior", value=return_results_behavior, expected_type=type_hints["return_results_behavior"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument target_path", value=target_path, expected_type=type_hints["target_path"])
            check_type(argname="argument trace_level", value=trace_level, expected_type=type_hints["trace_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "handler": handler,
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
        if external_access_integrations is not None:
            self._values["external_access_integrations"] = external_access_integrations
        if function_definition is not None:
            self._values["function_definition"] = function_definition
        if id is not None:
            self._values["id"] = id
        if imports is not None:
            self._values["imports"] = imports
        if is_secure is not None:
            self._values["is_secure"] = is_secure
        if log_level is not None:
            self._values["log_level"] = log_level
        if metric_level is not None:
            self._values["metric_level"] = metric_level
        if null_input_behavior is not None:
            self._values["null_input_behavior"] = null_input_behavior
        if packages is not None:
            self._values["packages"] = packages
        if return_results_behavior is not None:
            self._values["return_results_behavior"] = return_results_behavior
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version
        if secrets is not None:
            self._values["secrets"] = secrets
        if target_path is not None:
            self._values["target_path"] = target_path
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#database FunctionJava#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''The name of the handler method or class.

        If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a method name, as in the following form: ``MyClass.myMethod``. If the handler is for a tabular UDF, the HANDLER value should be the name of a handler class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#handler FunctionJava#handler}
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the function;

        the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#name FunctionJava#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def return_type(self) -> builtins.str:
        '''Specifies the results returned by the UDF, which determines the UDF type.

        Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#return_type FunctionJava#return_type}
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the function.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#schema FunctionJava#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#arguments FunctionJava#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaArguments]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#comment FunctionJava#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_console_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable stdout/stderr fast path logging for anonyous stored procs.

        This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#enable_console_output FunctionJava#enable_console_output}
        '''
        result = self._values.get("enable_console_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_access_integrations(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this function’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#external_access_integrations FunctionJava#external_access_integrations}
        '''
        result = self._values.get("external_access_integrations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def function_definition(self) -> typing.Optional[builtins.str]:
        '''Defines the handler code executed when the UDF is called.

        Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be Java source code. For more information, see `Introduction to Java UDFs <https://docs.snowflake.com/en/developer-guide/udf/java/udf-java-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#function_definition FunctionJava#function_definition}
        '''
        result = self._values.get("function_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#id FunctionJava#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaImports"]]]:
        '''imports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#imports FunctionJava#imports}
        '''
        result = self._values.get("imports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaImports"]]], result)

    @builtins.property
    def is_secure(self) -> typing.Optional[builtins.str]:
        '''Specifies that the function is secure.

        By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#is_secure FunctionJava#is_secure}
        '''
        result = self._values.get("is_secure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#log_level FunctionJava#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_level(self) -> typing.Optional[builtins.str]:
        '''METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#metric_level FunctionJava#metric_level}
        '''
        result = self._values.get("metric_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def null_input_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the function when called with null inputs.

        Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#null_input_behavior FunctionJava#null_input_behavior}
        '''
        result = self._values.get("null_input_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name and version number of Snowflake system packages required as dependencies.

        The value should be of the form ``package_name:version_number``, where ``package_name`` is ``snowflake_domain:package``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#packages FunctionJava#packages}
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def return_results_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#return_results_behavior FunctionJava#return_results_behavior}
        '''
        result = self._values.get("return_results_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''Specifies the Java JDK runtime version to use.

        The supported versions of Java are 11.x and 17.x. If RUNTIME_VERSION is not set, Java JDK 11 is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#runtime_version FunctionJava#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaSecrets"]]]:
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#secrets FunctionJava#secrets}
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionJavaSecrets"]]], result)

    @builtins.property
    def target_path(self) -> typing.Optional["FunctionJavaTargetPath"]:
        '''target_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#target_path FunctionJava#target_path}
        '''
        result = self._values.get("target_path")
        return typing.cast(typing.Optional["FunctionJavaTargetPath"], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#trace_level FunctionJava#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaImports",
    jsii_struct_bases=[],
    name_mapping={"path_on_stage": "pathOnStage", "stage_location": "stageLocation"},
)
class FunctionJavaImports:
    def __init__(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#path_on_stage FunctionJava#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#stage_location FunctionJava#stage_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2938b79bce26ce1548357bc7d23b17db6db2144d51867b5934d18bfb074b309)
            check_type(argname="argument path_on_stage", value=path_on_stage, expected_type=type_hints["path_on_stage"])
            check_type(argname="argument stage_location", value=stage_location, expected_type=type_hints["stage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_on_stage": path_on_stage,
            "stage_location": stage_location,
        }

    @builtins.property
    def path_on_stage(self) -> builtins.str:
        '''Path for import on stage, without the leading ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#path_on_stage FunctionJava#path_on_stage}
        '''
        result = self._values.get("path_on_stage")
        assert result is not None, "Required property 'path_on_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_location(self) -> builtins.str:
        '''Stage location without leading ``@``.

        To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#stage_location FunctionJava#stage_location}
        '''
        result = self._values.get("stage_location")
        assert result is not None, "Required property 'stage_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaImports(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaImportsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaImportsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a91d8c4523193fa6b1f55c2e5ee2680572cb226eb160b8861cfb2cbf9df349a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionJavaImportsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c86038c888194cac25143df0d68008717f833e3b10c4b8ab68f2f58dbb59db00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaImportsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad35e2b13e33322f41d35b4ecf6c00b91ab85fd09234d1d68b71601762d3d09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7dc9fee21b990d32a822c1992b4f481503fd79d1364a1a6cc408b41314c948b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d545a48838ae7613b2a0bcf7cad0e913a9e129197e49f9726263ae8055295e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaImports]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaImports]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaImports]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb64df23459ecd5cbcde6d47e303e1fe9ed5e03a87b13169da8137ff35c1e137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionJavaImportsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaImportsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__149fdbcde1f517adec3ca8bb673b9a3cfaab20e911b140f0cd69dcc952d52188)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="pathOnStageInput")
    def path_on_stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathOnStageInput"))

    @builtins.property
    @jsii.member(jsii_name="stageLocationInput")
    def stage_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="pathOnStage")
    def path_on_stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathOnStage"))

    @path_on_stage.setter
    def path_on_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338f714512266d58c9c25fd5038d9d4444caec9befc134b281b96c61fcb722ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathOnStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stageLocation")
    def stage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stageLocation"))

    @stage_location.setter
    def stage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad8b70a21b8385ba483e1006c05b48937db3925cb6105ec52348bad55c3d441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaImports]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaImports]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaImports]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4d1bc36bf86f979483b46def05f81eeb99fa595aba0cdcd30838e929b7a8f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavaParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersEnableConsoleOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavaParametersEnableConsoleOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaParametersEnableConsoleOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaParametersEnableConsoleOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersEnableConsoleOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1c98a883a8a189e051ac59d8dc4c949af67a03f47c9a37e2808f17c7cc95af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionJavaParametersEnableConsoleOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fbfa32e3f4d49de9a73493090156041c2c5cf60577768377eee3fd6b8822375)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaParametersEnableConsoleOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cea0db273b6c8d68ebb0625ec21846e80b6fc0d115acc6e6dbe6e6306b0d6e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8fa8fdaffbca412c059f2aadb5332b4d02d562752fb33f453388e2abf9e111f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91e82d8ad38e0fcacff9be9b4761a849992d706fd59223ece650fb501a09e071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavaParametersEnableConsoleOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersEnableConsoleOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fe4b809c85bb6ddb9b4d82e3fa90fc134169e8623308fc1b535c6fd8a6c6b75)
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
    ) -> typing.Optional[FunctionJavaParametersEnableConsoleOutput]:
        return typing.cast(typing.Optional[FunctionJavaParametersEnableConsoleOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavaParametersEnableConsoleOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e932e1816fd5c7257f9c30db12d87c554675baa4ed5f9937ff1deb0dfdbd3efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionJavaParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32aec4a59e79398a5aaf3f9dcd3fe854b012cd0c790313e63114f750fba94df1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionJavaParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9367fab5fe63697a8cd35a76c12bc5c203344abba1f63434186f44f97cfebee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72af1cbe7688ee2feb9bfd91d076581940a9da4bc8deb620a5f66c0a488e55c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaea35c9ca5bded4fa4e72290f2ee04646032c34160f6f6c192e0e5849ec1d79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d46c8fc36a543c40f63dc5ab57866d9c9049b583b00b8805cf3851b13ee3b47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavaParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff18867ec9b1d8b4847dd1f0922210cc9c61f9e1d847b6fe156dae6ae0505632)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionJavaParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0059b8a3666bb8f4b64a61aed197c8cea9ef590eba3d0c65ae5d80d71db881)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca0596e8b2dffa4bbdfa219bce7b87d21f7ab521f4c5cb2f428f20cf00d13de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a44928c4c2050892478bd8803d92da0dfc7e2fa2b1c37330698ef09e2827c5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c22493892f318a6b8f36ad21e7da6fedb8daa5acfac98cd35a4501f699261b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavaParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0057b4ce0f3568ea11b995131f46c6f3c0f9218e3858cb9aaeaa1cd213710354)
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
    def internal_value(self) -> typing.Optional[FunctionJavaParametersLogLevel]:
        return typing.cast(typing.Optional[FunctionJavaParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavaParametersLogLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a598c4e7491378837a927ee12551b1bebb9d73123abf6f70407ceb5014f23cd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersMetricLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavaParametersMetricLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaParametersMetricLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaParametersMetricLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersMetricLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d246d7c419cedd3775c15fdadcc225d7dd222c0850e452ad602e84a72ac98563)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionJavaParametersMetricLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6139e663326b383a69d3fa1ec075788aa52cb0085461d3c43cfa8a48e79361)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaParametersMetricLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da572d0d2b85aed293cf104632cd44378d99aec5cf7c3f694c30d2c553206505)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1c2f94cf1b9ddc7d9379a3e6bfaf133c3961a2cb2c45678ef0fc6a28a0b0d75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8490a643ad0e8a048dcfb3ce632a42209c3c03268bd2376c5ea972d3a8420272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavaParametersMetricLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersMetricLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04438d3cb56aa03c3515ab8645dc1406cb431ec80026e3b3b5633c695e6a3277)
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
    def internal_value(self) -> typing.Optional[FunctionJavaParametersMetricLevel]:
        return typing.cast(typing.Optional[FunctionJavaParametersMetricLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavaParametersMetricLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae7a64acee31f98c46ea28097ec2311b671d007ffe59dae2565dabc301446f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionJavaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__684235d0778e39f75f8422946c62a67947e87f792b9fbb4ce2e79a201bb7611a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(self) -> FunctionJavaParametersEnableConsoleOutputList:
        return typing.cast(FunctionJavaParametersEnableConsoleOutputList, jsii.get(self, "enableConsoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> FunctionJavaParametersLogLevelList:
        return typing.cast(FunctionJavaParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> FunctionJavaParametersMetricLevelList:
        return typing.cast(FunctionJavaParametersMetricLevelList, jsii.get(self, "metricLevel"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "FunctionJavaParametersTraceLevelList":
        return typing.cast("FunctionJavaParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionJavaParameters]:
        return typing.cast(typing.Optional[FunctionJavaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FunctionJavaParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782b324a7e5e8a02abdc628ba2ac9bb71785029b3ae3ebd0e8ffce3fcc4654d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavaParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf9175a3ba8f689c47e400bf6269259fb80efe6afb88975072e0fe3b71eb80c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionJavaParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30dc07d24ef50126f5b3e098296309b005f987ff4bde925d552ac7cbbab8dd2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b392754f0b0f1e0d5676004a26aa26b123a90260582d2ffaf9c335b2651e44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31b19371e3b472bc443edb5cfbed399d63b4c0f27af1e92c1c212e680d6d9d1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e16635fed5b9be96732ce5e0fdfe70b86d84281329ade1979b4e8861990eb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavaParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a29d767ed9c702dfab8eeb576a899f2635af9a4cc9c8ef2db248437d3aeae71b)
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
    def internal_value(self) -> typing.Optional[FunctionJavaParametersTraceLevel]:
        return typing.cast(typing.Optional[FunctionJavaParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionJavaParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f2a65e890b2b80ff17997b3da3bf88cf6e1e36539119cee0b2453dacc6ca0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "secret_variable_name": "secretVariableName",
    },
)
class FunctionJavaSecrets:
    def __init__(
        self,
        *,
        secret_id: builtins.str,
        secret_variable_name: builtins.str,
    ) -> None:
        '''
        :param secret_id: Fully qualified name of the allowed `secret <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_. You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the EXTERNAL_ACCESS_INTEGRATIONS parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#secret_id FunctionJava#secret_id}
        :param secret_variable_name: The variable that will be used in handler code when retrieving information from the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#secret_variable_name FunctionJava#secret_variable_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c52f6a663141096fa31c6842f52512b9af56b99137b866fb2b0d9b40d90d5d5)
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument secret_variable_name", value=secret_variable_name, expected_type=type_hints["secret_variable_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_id": secret_id,
            "secret_variable_name": secret_variable_name,
        }

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''Fully qualified name of the allowed `secret <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_. You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the EXTERNAL_ACCESS_INTEGRATIONS parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#secret_id FunctionJava#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_variable_name(self) -> builtins.str:
        '''The variable that will be used in handler code when retrieving information from the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#secret_variable_name FunctionJava#secret_variable_name}
        '''
        result = self._values.get("secret_variable_name")
        assert result is not None, "Required property 'secret_variable_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaSecretsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaSecretsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c53d4b6e1def66397894ffd80e69d19aacc17e2f43971fd127010af0a47b5c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionJavaSecretsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ad6cfab3937378bcd9819eca166a122efd29f5c2d13ad48bacc45e74afce92)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaSecretsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f1586ac345bfdf28c7e93245780699bd633cb73dfb981dff683580692c992a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0c4cb43024bb0eee0b81ed6d8b0cccfd02526bceffa287e055afcedb9181c87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e84ad98b59a8c7a632333d08be7b2c210a1131ecc3c2b24debc2f4a421e3e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaSecrets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaSecrets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaSecrets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883f47576ecf391263bfb2151c2aa8b19907f17aab957fed175904a2238528e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionJavaSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f516077590da0ba2de4f5a05ddb64f450636e28d3d7c308e94356bfa7ef3d74)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="secretIdInput")
    def secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="secretVariableNameInput")
    def secret_variable_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretVariableNameInput"))

    @builtins.property
    @jsii.member(jsii_name="secretId")
    def secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretId"))

    @secret_id.setter
    def secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79baba01eeb06f3c65cf4965ecc01565cebc93f968610160b190c6b38fe2b9cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVariableName")
    def secret_variable_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVariableName"))

    @secret_variable_name.setter
    def secret_variable_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393b84278fb69ca795d89edb41d95c0177cace2efe5490a302061afef31e2569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVariableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaSecrets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaSecrets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaSecrets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e42e1e5fb750eb05a353870b53b17de444f04d6bc9c55a3f95f61fd16adfa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionJavaShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__310c7c69f5e67d78a3ca9fac5adfa90a7727a812b1df6d084b7fb7d64c948aff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionJavaShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb3084a4d6b89a04e83566f33a7b5099fc46ca7b5a865c86c88bcd32606ae9c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionJavaShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a9d6ae19cdcaf26f28f7f65b2a2865ad3426231eff5e8eaa0ae73f3f079211)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3ed6bb8057cb688ef2a3cae6e91964b981917aaa31a0fd18fd950f88572f8bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__581b4dd6499d4866f146dd29f0699c6dc7790f156b7f6f6ca66725c9af06069b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionJavaShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaab05bc138da66cffe5dd6327cb2020529495fefaf6a02989cece93e08581a6)
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
    def internal_value(self) -> typing.Optional[FunctionJavaShowOutput]:
        return typing.cast(typing.Optional[FunctionJavaShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FunctionJavaShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7597b0f45e12122a6a6079a7d01590425ee21b61c1c9a329e1afada6166ce245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaTargetPath",
    jsii_struct_bases=[],
    name_mapping={"path_on_stage": "pathOnStage", "stage_location": "stageLocation"},
)
class FunctionJavaTargetPath:
    def __init__(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#path_on_stage FunctionJava#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#stage_location FunctionJava#stage_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736becd83439bb3edf0c54e1283a637b8c8654dceb1c8377c75a4c063f3b3ba6)
            check_type(argname="argument path_on_stage", value=path_on_stage, expected_type=type_hints["path_on_stage"])
            check_type(argname="argument stage_location", value=stage_location, expected_type=type_hints["stage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_on_stage": path_on_stage,
            "stage_location": stage_location,
        }

    @builtins.property
    def path_on_stage(self) -> builtins.str:
        '''Path for import on stage, without the leading ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#path_on_stage FunctionJava#path_on_stage}
        '''
        result = self._values.get("path_on_stage")
        assert result is not None, "Required property 'path_on_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_location(self) -> builtins.str:
        '''Stage location without leading ``@``.

        To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_java#stage_location FunctionJava#stage_location}
        '''
        result = self._values.get("stage_location")
        assert result is not None, "Required property 'stage_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionJavaTargetPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionJavaTargetPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionJava.FunctionJavaTargetPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97216a2e721574d4b4bb4f83949db757246fbf110e1781801e51c3d69156c8ed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="pathOnStageInput")
    def path_on_stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathOnStageInput"))

    @builtins.property
    @jsii.member(jsii_name="stageLocationInput")
    def stage_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stageLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="pathOnStage")
    def path_on_stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathOnStage"))

    @path_on_stage.setter
    def path_on_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__168e11913fcfd2a84b3b3b07a493919e17ff38354a43d9c4cd348f56037eab48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathOnStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stageLocation")
    def stage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stageLocation"))

    @stage_location.setter
    def stage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457646347c7d4a77d8408caa0517222123ae4400779a9de122c6b9c93af57bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionJavaTargetPath]:
        return typing.cast(typing.Optional[FunctionJavaTargetPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FunctionJavaTargetPath]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e59b6decfc063db43d2302d8e3e692a1f881153bb7e77973c3e38102b70455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FunctionJava",
    "FunctionJavaArguments",
    "FunctionJavaArgumentsList",
    "FunctionJavaArgumentsOutputReference",
    "FunctionJavaConfig",
    "FunctionJavaImports",
    "FunctionJavaImportsList",
    "FunctionJavaImportsOutputReference",
    "FunctionJavaParameters",
    "FunctionJavaParametersEnableConsoleOutput",
    "FunctionJavaParametersEnableConsoleOutputList",
    "FunctionJavaParametersEnableConsoleOutputOutputReference",
    "FunctionJavaParametersList",
    "FunctionJavaParametersLogLevel",
    "FunctionJavaParametersLogLevelList",
    "FunctionJavaParametersLogLevelOutputReference",
    "FunctionJavaParametersMetricLevel",
    "FunctionJavaParametersMetricLevelList",
    "FunctionJavaParametersMetricLevelOutputReference",
    "FunctionJavaParametersOutputReference",
    "FunctionJavaParametersTraceLevel",
    "FunctionJavaParametersTraceLevelList",
    "FunctionJavaParametersTraceLevelOutputReference",
    "FunctionJavaSecrets",
    "FunctionJavaSecretsList",
    "FunctionJavaSecretsOutputReference",
    "FunctionJavaShowOutput",
    "FunctionJavaShowOutputList",
    "FunctionJavaShowOutputOutputReference",
    "FunctionJavaTargetPath",
    "FunctionJavaTargetPathOutputReference",
]

publication.publish()

def _typecheckingstub__22afeb6cf4af18e7a4914f8b1a23098516db9232cf41ec5eeb4955952bf6297e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    handler: builtins.str,
    name: builtins.str,
    return_type: builtins.str,
    schema: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    function_definition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaImports, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    return_results_behavior: typing.Optional[builtins.str] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_path: typing.Optional[typing.Union[FunctionJavaTargetPath, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__992a0037b165566141295a88d9efbb101de815dc34d29728f964b58da1a496b7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f4dabfc7f8e4b35c317c2aaaa74314d6989994f6ee31499ceb4c05c0073f94(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13597aecd048881d177daca072bf75b7e0476b80d90fa83e1284564706848ef6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaImports, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a2a37a69d129e854ece5e87872a1ef9f1d70b3438e92111a122e00c701da06(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaSecrets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1486ef707a6c61bc62d2df2e54e940cb4ec000d701d98241e1df860f9334b73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731e07e10eb61dd3561efd0df35da1d582ef70c11858a3bbc1c3d324ba7a19fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a162cbf599d87d067b3cdc62ba4c9e8342ffb15612086c6faacb5b265eb92acf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3e70fb0331942ef9235d0de2d65458609f843a3af3fbeab2d24dd50bcc14f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06f0ef1b7292f709b122ba7c8014d0963657afef30854bafa8d013e59f8bbff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050226d94329af043ed3fac8f1afef1974ae592b18d675a3cecf871b8bfaf5f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb985d9522ecaa4ceeba62142b878532311fd5f14ad87b28723aaf2cf2a5fe3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19334e0162640f622ae68567533ff148dedecc06ae23e931ce9afa5c50388a0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a89d85674d42585065c34104698e14ffbe64e8818be758ef2a75de94e448da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253ade4019a6d1c767d2c25a5c7db01a6c62f3b93efa6fd5424fdd99f763a0a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510eca69b84df320ace228a37126f79590ff44d92b59de710161baf34578dc9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b3620223c2787553eebac7a4a31118100ab95690faae2ecd4c0e229d8c809a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3db1d5f9b87ab53b9631f143abe05ba08c1f3aaea327f87fcd543b46aea4eb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4288c66c1b79fea8e29eb50b2a0210cc407801508dac446cb2cfc57c66482f7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9371dcb115a59dd8d307cf8835620103b42ca33501878cccfd0f76a8ab82bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccd427797e1315151744986a33630fde001bb07aaea04ca9698266d1da8e0ddd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fdb3489c5d5ec888a94483f5b50ab95aff90465dbb975600f689e1d6b686b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1824813b19a6fe1adabd8d9aea058d99462c43debb246db653606a68ac4868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b94e6f99976bfbfa68d4285b9058d6f498f445aaf109409427cffd969db9039(
    *,
    arg_data_type: builtins.str,
    arg_name: builtins.str,
    arg_default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fb7b27faf9ee9a924590564289427c1c68a9299ffd86b83c1d950288d30618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b216142b82e4f90b3b80a4f0e3ba61f100c08729212cc1e4f34f4b684a9455c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3572fb2f3b8e510ff8da295a6fca65e9556bf67e00756608717f2e084c77741f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da7ce4e28cbe14b895290c317da5171850df9d5fec00b1e7987b219af3fde82(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2097c821e6d5945c789be5651e9daa943c5f612cb0dffc3c0953cb418e08ee54(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae013d98ec13cd615ab792c7cd29ac764d8b965cf92d9e337e81acc9374080b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1227bf859739eeae110f3ecb4b369bc451b1aa451b3f2c13545688e7dc2612(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742d9a47041d6409e0645ed3b9c289a07d63bf9b022203c910cd5bccda590efc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca84500a447d2c912a895995a1eac1098735f0bdb1c184e1c2a465ebedfc0f78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c631ee4b13378c32224ed906cb9fe629e0ab410c54d9528d58ee4c707db2582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d08ee06821367e5824ed6a7bf3fed0ab793fee08f670f60ef10bf37327018af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaArguments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b192f611a3b78f973dd3de602a2812b1164e5bc00d21d3593d9b2f31d2b97655(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    database: builtins.str,
    handler: builtins.str,
    name: builtins.str,
    return_type: builtins.str,
    schema: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    function_definition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaImports, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    return_results_behavior: typing.Optional[builtins.str] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionJavaSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_path: typing.Optional[typing.Union[FunctionJavaTargetPath, typing.Dict[builtins.str, typing.Any]]] = None,
    trace_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2938b79bce26ce1548357bc7d23b17db6db2144d51867b5934d18bfb074b309(
    *,
    path_on_stage: builtins.str,
    stage_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91d8c4523193fa6b1f55c2e5ee2680572cb226eb160b8861cfb2cbf9df349a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c86038c888194cac25143df0d68008717f833e3b10c4b8ab68f2f58dbb59db00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad35e2b13e33322f41d35b4ecf6c00b91ab85fd09234d1d68b71601762d3d09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7dc9fee21b990d32a822c1992b4f481503fd79d1364a1a6cc408b41314c948b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d545a48838ae7613b2a0bcf7cad0e913a9e129197e49f9726263ae8055295e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb64df23459ecd5cbcde6d47e303e1fe9ed5e03a87b13169da8137ff35c1e137(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaImports]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149fdbcde1f517adec3ca8bb673b9a3cfaab20e911b140f0cd69dcc952d52188(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338f714512266d58c9c25fd5038d9d4444caec9befc134b281b96c61fcb722ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad8b70a21b8385ba483e1006c05b48937db3925cb6105ec52348bad55c3d441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4d1bc36bf86f979483b46def05f81eeb99fa595aba0cdcd30838e929b7a8f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaImports]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1c98a883a8a189e051ac59d8dc4c949af67a03f47c9a37e2808f17c7cc95af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbfa32e3f4d49de9a73493090156041c2c5cf60577768377eee3fd6b8822375(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cea0db273b6c8d68ebb0625ec21846e80b6fc0d115acc6e6dbe6e6306b0d6e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8fa8fdaffbca412c059f2aadb5332b4d02d562752fb33f453388e2abf9e111f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e82d8ad38e0fcacff9be9b4761a849992d706fd59223ece650fb501a09e071(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe4b809c85bb6ddb9b4d82e3fa90fc134169e8623308fc1b535c6fd8a6c6b75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e932e1816fd5c7257f9c30db12d87c554675baa4ed5f9937ff1deb0dfdbd3efd(
    value: typing.Optional[FunctionJavaParametersEnableConsoleOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32aec4a59e79398a5aaf3f9dcd3fe854b012cd0c790313e63114f750fba94df1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9367fab5fe63697a8cd35a76c12bc5c203344abba1f63434186f44f97cfebee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72af1cbe7688ee2feb9bfd91d076581940a9da4bc8deb620a5f66c0a488e55c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaea35c9ca5bded4fa4e72290f2ee04646032c34160f6f6c192e0e5849ec1d79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d46c8fc36a543c40f63dc5ab57866d9c9049b583b00b8805cf3851b13ee3b47(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff18867ec9b1d8b4847dd1f0922210cc9c61f9e1d847b6fe156dae6ae0505632(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0059b8a3666bb8f4b64a61aed197c8cea9ef590eba3d0c65ae5d80d71db881(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca0596e8b2dffa4bbdfa219bce7b87d21f7ab521f4c5cb2f428f20cf00d13de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a44928c4c2050892478bd8803d92da0dfc7e2fa2b1c37330698ef09e2827c5a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22493892f318a6b8f36ad21e7da6fedb8daa5acfac98cd35a4501f699261b7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0057b4ce0f3568ea11b995131f46c6f3c0f9218e3858cb9aaeaa1cd213710354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a598c4e7491378837a927ee12551b1bebb9d73123abf6f70407ceb5014f23cd9(
    value: typing.Optional[FunctionJavaParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d246d7c419cedd3775c15fdadcc225d7dd222c0850e452ad602e84a72ac98563(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6139e663326b383a69d3fa1ec075788aa52cb0085461d3c43cfa8a48e79361(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da572d0d2b85aed293cf104632cd44378d99aec5cf7c3f694c30d2c553206505(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c2f94cf1b9ddc7d9379a3e6bfaf133c3961a2cb2c45678ef0fc6a28a0b0d75(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8490a643ad0e8a048dcfb3ce632a42209c3c03268bd2376c5ea972d3a8420272(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04438d3cb56aa03c3515ab8645dc1406cb431ec80026e3b3b5633c695e6a3277(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae7a64acee31f98c46ea28097ec2311b671d007ffe59dae2565dabc301446f4(
    value: typing.Optional[FunctionJavaParametersMetricLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684235d0778e39f75f8422946c62a67947e87f792b9fbb4ce2e79a201bb7611a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782b324a7e5e8a02abdc628ba2ac9bb71785029b3ae3ebd0e8ffce3fcc4654d3(
    value: typing.Optional[FunctionJavaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf9175a3ba8f689c47e400bf6269259fb80efe6afb88975072e0fe3b71eb80c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30dc07d24ef50126f5b3e098296309b005f987ff4bde925d552ac7cbbab8dd2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b392754f0b0f1e0d5676004a26aa26b123a90260582d2ffaf9c335b2651e44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b19371e3b472bc443edb5cfbed399d63b4c0f27af1e92c1c212e680d6d9d1b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e16635fed5b9be96732ce5e0fdfe70b86d84281329ade1979b4e8861990eb62(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a29d767ed9c702dfab8eeb576a899f2635af9a4cc9c8ef2db248437d3aeae71b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f2a65e890b2b80ff17997b3da3bf88cf6e1e36539119cee0b2453dacc6ca0c(
    value: typing.Optional[FunctionJavaParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c52f6a663141096fa31c6842f52512b9af56b99137b866fb2b0d9b40d90d5d5(
    *,
    secret_id: builtins.str,
    secret_variable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c53d4b6e1def66397894ffd80e69d19aacc17e2f43971fd127010af0a47b5c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ad6cfab3937378bcd9819eca166a122efd29f5c2d13ad48bacc45e74afce92(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f1586ac345bfdf28c7e93245780699bd633cb73dfb981dff683580692c992a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c4cb43024bb0eee0b81ed6d8b0cccfd02526bceffa287e055afcedb9181c87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e84ad98b59a8c7a632333d08be7b2c210a1131ecc3c2b24debc2f4a421e3e2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883f47576ecf391263bfb2151c2aa8b19907f17aab957fed175904a2238528e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionJavaSecrets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f516077590da0ba2de4f5a05ddb64f450636e28d3d7c308e94356bfa7ef3d74(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79baba01eeb06f3c65cf4965ecc01565cebc93f968610160b190c6b38fe2b9cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393b84278fb69ca795d89edb41d95c0177cace2efe5490a302061afef31e2569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e42e1e5fb750eb05a353870b53b17de444f04d6bc9c55a3f95f61fd16adfa2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionJavaSecrets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310c7c69f5e67d78a3ca9fac5adfa90a7727a812b1df6d084b7fb7d64c948aff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3084a4d6b89a04e83566f33a7b5099fc46ca7b5a865c86c88bcd32606ae9c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a9d6ae19cdcaf26f28f7f65b2a2865ad3426231eff5e8eaa0ae73f3f079211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ed6bb8057cb688ef2a3cae6e91964b981917aaa31a0fd18fd950f88572f8bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581b4dd6499d4866f146dd29f0699c6dc7790f156b7f6f6ca66725c9af06069b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaab05bc138da66cffe5dd6327cb2020529495fefaf6a02989cece93e08581a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7597b0f45e12122a6a6079a7d01590425ee21b61c1c9a329e1afada6166ce245(
    value: typing.Optional[FunctionJavaShowOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736becd83439bb3edf0c54e1283a637b8c8654dceb1c8377c75a4c063f3b3ba6(
    *,
    path_on_stage: builtins.str,
    stage_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97216a2e721574d4b4bb4f83949db757246fbf110e1781801e51c3d69156c8ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168e11913fcfd2a84b3b3b07a493919e17ff38354a43d9c4cd348f56037eab48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457646347c7d4a77d8408caa0517222123ae4400779a9de122c6b9c93af57bde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e59b6decfc063db43d2302d8e3e692a1f881153bb7e77973c3e38102b70455(
    value: typing.Optional[FunctionJavaTargetPath],
) -> None:
    """Type checking stubs"""
    pass

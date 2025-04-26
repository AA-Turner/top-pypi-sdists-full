r'''
# `snowflake_function_scala`

Refer to the Terraform Registry for docs: [`snowflake_function_scala`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala).
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


class FunctionScala(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScala",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala snowflake_function_scala}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        database: builtins.str,
        handler: builtins.str,
        name: builtins.str,
        return_type: builtins.str,
        runtime_version: builtins.str,
        schema: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionScalaArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        function_definition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionScalaImports", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        return_results_behavior: typing.Optional[builtins.str] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionScalaSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_path: typing.Optional[typing.Union["FunctionScalaTargetPath", typing.Dict[builtins.str, typing.Any]]] = None,
        trace_level: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala snowflake_function_scala} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#database FunctionScala#database}
        :param handler: The name of the handler method or class. If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a method name, as in the following form: ``MyClass.myMethod``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#handler FunctionScala#handler}
        :param name: The name of the function; the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#name FunctionScala#name}
        :param return_type: Specifies the results returned by the UDF, which determines the UDF type. Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#return_type FunctionScala#return_type}
        :param runtime_version: Specifies the Scala runtime version to use. The supported versions of Scala are: 2.12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#runtime_version FunctionScala#runtime_version}
        :param schema: The schema in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#schema FunctionScala#schema}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arguments FunctionScala#arguments}
        :param comment: Specifies a comment for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#comment FunctionScala#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#enable_console_output FunctionScala#enable_console_output}
        :param external_access_integrations: The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this function’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#external_access_integrations FunctionScala#external_access_integrations}
        :param function_definition: Defines the handler code executed when the UDF is called. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be Scala source code. For more information, see `Introduction to Scala UDFs <https://docs.snowflake.com/en/developer-guide/udf/scala/udf-scala-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#function_definition FunctionScala#function_definition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#id FunctionScala#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: imports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#imports FunctionScala#imports}
        :param is_secure: Specifies that the function is secure. By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#is_secure FunctionScala#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#log_level FunctionScala#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#metric_level FunctionScala#metric_level}
        :param null_input_behavior: Specifies the behavior of the function when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#null_input_behavior FunctionScala#null_input_behavior}
        :param packages: The name and version number of Snowflake system packages required as dependencies. The value should be of the form ``package_name:version_number``, where ``package_name`` is ``snowflake_domain:package``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#packages FunctionScala#packages}
        :param return_results_behavior: Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#return_results_behavior FunctionScala#return_results_behavior}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#secrets FunctionScala#secrets}
        :param target_path: target_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#target_path FunctionScala#target_path}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#trace_level FunctionScala#trace_level}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958e139092a0894d47f1aa7fcc2cbcfa3e794abf5d07b03ab30c1231d6b653bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FunctionScalaConfig(
            database=database,
            handler=handler,
            name=name,
            return_type=return_type,
            runtime_version=runtime_version,
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
        '''Generates CDKTF code for importing a FunctionScala resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FunctionScala to import.
        :param import_from_id: The id of the existing FunctionScala that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FunctionScala to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8c2d0a20561ddee397fdec302643f26407c69ff4ac936f9cb3607095de3eb0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionScalaArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5876b842672afc87158c6e061d93907c1925c0474cf2ad24d9e6d9d2bae492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArguments", [value]))

    @jsii.member(jsii_name="putImports")
    def put_imports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionScalaImports", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0239cee6814d754d8028c6364a64024d0e6c778d0d2f1da19ab6641dc3f9452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putImports", [value]))

    @jsii.member(jsii_name="putSecrets")
    def put_secrets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionScalaSecrets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd36e73c3169a30d5a05184d7459290f20364c3666effc58a0e41e1475dab47)
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
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#path_on_stage FunctionScala#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#stage_location FunctionScala#stage_location}
        '''
        value = FunctionScalaTargetPath(
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
    def arguments(self) -> "FunctionScalaArgumentsList":
        return typing.cast("FunctionScalaArgumentsList", jsii.get(self, "arguments"))

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
    def imports(self) -> "FunctionScalaImportsList":
        return typing.cast("FunctionScalaImportsList", jsii.get(self, "imports"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "FunctionScalaParametersList":
        return typing.cast("FunctionScalaParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "FunctionScalaSecretsList":
        return typing.cast("FunctionScalaSecretsList", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "FunctionScalaShowOutputList":
        return typing.cast("FunctionScalaShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="targetPath")
    def target_path(self) -> "FunctionScalaTargetPathOutputReference":
        return typing.cast("FunctionScalaTargetPathOutputReference", jsii.get(self, "targetPath"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaArguments"]]], jsii.get(self, "argumentsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaImports"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaImports"]]], jsii.get(self, "importsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaSecrets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaSecrets"]]], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPathInput")
    def target_path_input(self) -> typing.Optional["FunctionScalaTargetPath"]:
        return typing.cast(typing.Optional["FunctionScalaTargetPath"], jsii.get(self, "targetPathInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4b5bdead7fa8ef1718827d53449d9c784144c88ab5dafd0bc90a401bb3bb031a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bea8d3b7e37c4d9d3911593dc1b986c7dd30f035c73015ed636ef0e1d5cfdd26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4fbea82fbad4a787a90d58da3c4f1a1c0fe334b5d1edee055e2d250465a61a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsoleOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrations")
    def external_access_integrations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalAccessIntegrations"))

    @external_access_integrations.setter
    def external_access_integrations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85cc00c2ce05283f37e17847c0781e1401a1810aa8b6303b8393a7e07203b3f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAccessIntegrations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionDefinition")
    def function_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionDefinition"))

    @function_definition.setter
    def function_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6546f73d084a5f26fe083139d47eea9079fe51837ca8a7e25a841e1ef5382c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0bdcc1d803947d7b341f17e3a2e0f65298db4aec27962e070fcc343493099b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b399bcfb1730ba0d0d9ae21d5c4018fcd87861ea4632aaa19159f7441410f449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isSecure"))

    @is_secure.setter
    def is_secure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6464b5dc510025bc0ae3cba417d1fded6d3822bb5792061c4752ba0a3fcb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d136cbe89e86a440be39969ed22937e0a466a0850c537da3c29e429dffbc55b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricLevel"))

    @metric_level.setter
    def metric_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bdf54d41221a83b1abd084c63a6a2ee9fcaa6b2409ead5f4b104f4a5266f78c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465dc2f645b160f8366b92f430bccc09ffb1894b817124e1999d7e4a0467ec2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullInputBehavior")
    def null_input_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullInputBehavior"))

    @null_input_behavior.setter
    def null_input_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f666673f6905591ccd043f9794bb6c8bbfae6965ff10f4ff82b559a1332ad20b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullInputBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packages")
    def packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packages"))

    @packages.setter
    def packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abafa06a0e9e2e8e584f4f78ff0c854c3e98be8b6ce1e8744d877df09fccfc01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnResultsBehavior")
    def return_results_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnResultsBehavior"))

    @return_results_behavior.setter
    def return_results_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16564fa1aa7c0ddf57ffd7e08990ef4fb23ada1ffffb0b1516e67f0a2487597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnResultsBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed8ef0306c3d3ef2be62d6499c91050e159fe966b6f5def64160a8cc0fa3ed1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c4cb7ff00b8b28df267efbcbb9b43170692142598c5958fafdef7de04959cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3098be5d2ebc98639c40183ec6234a5efc60427d13ea88fd318a60d458d8403b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__093433ce066c991f5397b3f2556ff18b2509ea5b0b8b9c7ae1c1c74222b4fde5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaArguments",
    jsii_struct_bases=[],
    name_mapping={
        "arg_data_type": "argDataType",
        "arg_name": "argName",
        "arg_default_value": "argDefaultValue",
    },
)
class FunctionScalaArguments:
    def __init__(
        self,
        *,
        arg_data_type: builtins.str,
        arg_name: builtins.str,
        arg_default_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arg_data_type: The argument type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arg_data_type FunctionScala#arg_data_type}
        :param arg_name: The argument name. The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the function definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arg_name FunctionScala#arg_name}
        :param arg_default_value: Optional default value for the argument. For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arg_default_value FunctionScala#arg_default_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542f8ce70f93bb30b0df9688f572a76b7ff7570a619ee07beb50ee11bd8f736b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arg_data_type FunctionScala#arg_data_type}
        '''
        result = self._values.get("arg_data_type")
        assert result is not None, "Required property 'arg_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_name(self) -> builtins.str:
        '''The argument name.

        The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the function definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arg_name FunctionScala#arg_name}
        '''
        result = self._values.get("arg_name")
        assert result is not None, "Required property 'arg_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_default_value(self) -> typing.Optional[builtins.str]:
        '''Optional default value for the argument.

        For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arg_default_value FunctionScala#arg_default_value}
        '''
        result = self._values.get("arg_default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaArgumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5665673f8353e8529d3ff63c9f1909355015ebe4283da41d34a045684107dee6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionScalaArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5317c6ecc9dfd421934f76f305d6e4822dc28ae78881e69f46969a7ae4f68b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a38422d4420465bde2e445f05fbd3f66cbc3fef50c982a4acd124d5dafff8e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea72fb2c0db57475419bb61001c8057363ed4a4727e4ba1db30715c4f91209a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f952a6b933cbe04c7f197c5ac8dde15e95a9b54c59e3c036f65d952ce52f125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27d20189ffabab42363f1c0f760554e3d0ae58b2bd395c3cee05092429840c1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionScalaArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaArgumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__641df5fac62e2a9517838a16ff4a2c198eaeb9360501990c1e95378332019b89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f50f55970220c6830080c3a4b7194b83b30b9f4444d6f15c4ab1ab2c3bd26e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argDefaultValue")
    def arg_default_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argDefaultValue"))

    @arg_default_value.setter
    def arg_default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60508ac35969671d834a93ce4199e261438ee449aa3f39d6f4843c39270101e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDefaultValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argName")
    def arg_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argName"))

    @arg_name.setter
    def arg_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be4f57dc87765a0ec565f271e2710cc7629d411f8078a9dbdfe9c24dd9fbea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaArguments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaArguments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaArguments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7440916ffd459171d818993df680b30fe5b5b3f36e929b81d620f725983cfb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaConfig",
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
        "runtime_version": "runtimeVersion",
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
        "secrets": "secrets",
        "target_path": "targetPath",
        "trace_level": "traceLevel",
    },
)
class FunctionScalaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        runtime_version: builtins.str,
        schema: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        function_definition: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionScalaImports", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        return_results_behavior: typing.Optional[builtins.str] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionScalaSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_path: typing.Optional[typing.Union["FunctionScalaTargetPath", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param database: The database in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#database FunctionScala#database}
        :param handler: The name of the handler method or class. If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a method name, as in the following form: ``MyClass.myMethod``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#handler FunctionScala#handler}
        :param name: The name of the function; the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#name FunctionScala#name}
        :param return_type: Specifies the results returned by the UDF, which determines the UDF type. Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#return_type FunctionScala#return_type}
        :param runtime_version: Specifies the Scala runtime version to use. The supported versions of Scala are: 2.12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#runtime_version FunctionScala#runtime_version}
        :param schema: The schema in which to create the function. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#schema FunctionScala#schema}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arguments FunctionScala#arguments}
        :param comment: Specifies a comment for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#comment FunctionScala#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#enable_console_output FunctionScala#enable_console_output}
        :param external_access_integrations: The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this function’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#external_access_integrations FunctionScala#external_access_integrations}
        :param function_definition: Defines the handler code executed when the UDF is called. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be Scala source code. For more information, see `Introduction to Scala UDFs <https://docs.snowflake.com/en/developer-guide/udf/scala/udf-scala-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#function_definition FunctionScala#function_definition}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#id FunctionScala#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: imports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#imports FunctionScala#imports}
        :param is_secure: Specifies that the function is secure. By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#is_secure FunctionScala#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#log_level FunctionScala#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#metric_level FunctionScala#metric_level}
        :param null_input_behavior: Specifies the behavior of the function when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#null_input_behavior FunctionScala#null_input_behavior}
        :param packages: The name and version number of Snowflake system packages required as dependencies. The value should be of the form ``package_name:version_number``, where ``package_name`` is ``snowflake_domain:package``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#packages FunctionScala#packages}
        :param return_results_behavior: Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#return_results_behavior FunctionScala#return_results_behavior}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#secrets FunctionScala#secrets}
        :param target_path: target_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#target_path FunctionScala#target_path}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#trace_level FunctionScala#trace_level}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(target_path, dict):
            target_path = FunctionScalaTargetPath(**target_path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d742b8fa184c56a088bbe625619af784280bc3f36a22d9dca672f3f492d7bba)
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
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
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
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument target_path", value=target_path, expected_type=type_hints["target_path"])
            check_type(argname="argument trace_level", value=trace_level, expected_type=type_hints["trace_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "database": database,
            "handler": handler,
            "name": name,
            "return_type": return_type,
            "runtime_version": runtime_version,
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#database FunctionScala#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''The name of the handler method or class.

        If the handler is for a scalar UDF, returning a non-tabular value, the HANDLER value should be a method name, as in the following form: ``MyClass.myMethod``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#handler FunctionScala#handler}
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the function;

        the identifier does not need to be unique for the schema in which the function is created because UDFs are identified and resolved by the combination of the name and argument types. Check the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#name FunctionScala#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def return_type(self) -> builtins.str:
        '''Specifies the results returned by the UDF, which determines the UDF type.

        Use ``<result_data_type>`` to create a scalar UDF that returns a single value with the specified data type. Use ``TABLE (col_name col_data_type, ...)`` to creates a table UDF that returns tabular results with the specified table column(s) and column type(s). For the details, consult the `docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#all-languages>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#return_type FunctionScala#return_type}
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''Specifies the Scala runtime version to use. The supported versions of Scala are: 2.12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#runtime_version FunctionScala#runtime_version}
        '''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the function.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#schema FunctionScala#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#arguments FunctionScala#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaArguments]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#comment FunctionScala#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_console_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable stdout/stderr fast path logging for anonyous stored procs.

        This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#enable_console_output FunctionScala#enable_console_output}
        '''
        result = self._values.get("enable_console_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def external_access_integrations(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this function’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#external_access_integrations FunctionScala#external_access_integrations}
        '''
        result = self._values.get("external_access_integrations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def function_definition(self) -> typing.Optional[builtins.str]:
        '''Defines the handler code executed when the UDF is called.

        Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``function_definition`` value must be Scala source code. For more information, see `Introduction to Scala UDFs <https://docs.snowflake.com/en/developer-guide/udf/scala/udf-scala-introduction>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#function_definition FunctionScala#function_definition}
        '''
        result = self._values.get("function_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#id FunctionScala#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaImports"]]]:
        '''imports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#imports FunctionScala#imports}
        '''
        result = self._values.get("imports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaImports"]]], result)

    @builtins.property
    def is_secure(self) -> typing.Optional[builtins.str]:
        '''Specifies that the function is secure.

        By design, the Snowflake's ``SHOW FUNCTIONS`` command does not provide information about secure functions (consult `function docs <https://docs.snowflake.com/en/sql-reference/sql/create-function#id1>`_ and `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_) which is essential to manage/import function with Terraform. Use the role owning the function while managing secure functions. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#is_secure FunctionScala#is_secure}
        '''
        result = self._values.get("is_secure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#log_level FunctionScala#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_level(self) -> typing.Optional[builtins.str]:
        '''METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#metric_level FunctionScala#metric_level}
        '''
        result = self._values.get("metric_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def null_input_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the function when called with null inputs.

        Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#null_input_behavior FunctionScala#null_input_behavior}
        '''
        result = self._values.get("null_input_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name and version number of Snowflake system packages required as dependencies.

        The value should be of the form ``package_name:version_number``, where ``package_name`` is ``snowflake_domain:package``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#packages FunctionScala#packages}
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def return_results_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the function when returning results. Valid values are (case-insensitive): ``VOLATILE`` | ``IMMUTABLE``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#return_results_behavior FunctionScala#return_results_behavior}
        '''
        result = self._values.get("return_results_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaSecrets"]]]:
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#secrets FunctionScala#secrets}
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionScalaSecrets"]]], result)

    @builtins.property
    def target_path(self) -> typing.Optional["FunctionScalaTargetPath"]:
        '''target_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#target_path FunctionScala#target_path}
        '''
        result = self._values.get("target_path")
        return typing.cast(typing.Optional["FunctionScalaTargetPath"], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#trace_level FunctionScala#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaImports",
    jsii_struct_bases=[],
    name_mapping={"path_on_stage": "pathOnStage", "stage_location": "stageLocation"},
)
class FunctionScalaImports:
    def __init__(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#path_on_stage FunctionScala#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#stage_location FunctionScala#stage_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ee4e34be1591f376d54d3acb876210f1eda2add8e9af12bf34df73880f4d063)
            check_type(argname="argument path_on_stage", value=path_on_stage, expected_type=type_hints["path_on_stage"])
            check_type(argname="argument stage_location", value=stage_location, expected_type=type_hints["stage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_on_stage": path_on_stage,
            "stage_location": stage_location,
        }

    @builtins.property
    def path_on_stage(self) -> builtins.str:
        '''Path for import on stage, without the leading ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#path_on_stage FunctionScala#path_on_stage}
        '''
        result = self._values.get("path_on_stage")
        assert result is not None, "Required property 'path_on_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_location(self) -> builtins.str:
        '''Stage location without leading ``@``.

        To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#stage_location FunctionScala#stage_location}
        '''
        result = self._values.get("stage_location")
        assert result is not None, "Required property 'stage_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaImports(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaImportsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaImportsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a8527e7c9b3f27ce3195382e733a2054a1fa7e836f4c504ac10dfefb0a133f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionScalaImportsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086a1eb87790a8c128d53c117bf4127288bb12a45849dfbaf90edcd0875eca6e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaImportsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89261d8214c4ee8f974f8e2b732f61fc32ad8945825287b3216239169e9729b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e41f175bb8a53efa65823c7358ddb7400ba709e799b8a582183f2f1e286f738)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04cc87ef7f6438b6c701491ddb22ff42ab34b694b5e824bec650957ea899e841)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaImports]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaImports]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaImports]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2668307b8210de08f91423636c91d524e46f8dfda9c967f1f22f47f4ff3498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionScalaImportsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaImportsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41da8c693b62cd7c24cf0b775ecb32fce080ab9b980cfeee633af62d577f11f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5c97063b0f7c5d2f6be0fe5f62397f688a99e386700451ccfd632a65ce98a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathOnStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stageLocation")
    def stage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stageLocation"))

    @stage_location.setter
    def stage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d072b59442e57d2fc12d50e91746cf51acb3de0ee5331e36d5bdfc87f7bcc74a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaImports]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaImports]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaImports]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f8d306b42bd72bc67b4ce85c6b672279f542713ec35f9ffb108782f73916d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionScalaParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersEnableConsoleOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionScalaParametersEnableConsoleOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaParametersEnableConsoleOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaParametersEnableConsoleOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersEnableConsoleOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__248a406f787ee23b271d1e79fde24948f539afc27b77953892537f22fb37502a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionScalaParametersEnableConsoleOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a9715f5ef7c1e53f181bfd679d01924b685f7727886a9c38e699a57db24c00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaParametersEnableConsoleOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43692000db54cedea4483e3394f1dcc4a99267573b285737f98669a657a9e06c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__863a083fb37df0faff341b11a9e7004a2458b4802dd2c88a292c360adb83b3df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e51f50f79593f7e36ad5c2aa05fcec9243271b3d0362ecc2f6d5bdb0de881d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionScalaParametersEnableConsoleOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersEnableConsoleOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec9ad16be43ece1e0ac993e5f9c0cf8e6bc2d8f2f182119c5a7abd83713def37)
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
    ) -> typing.Optional[FunctionScalaParametersEnableConsoleOutput]:
        return typing.cast(typing.Optional[FunctionScalaParametersEnableConsoleOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionScalaParametersEnableConsoleOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b403d5b1fa45f7bdd80e56999511d8d18da1ca67e2f54a13b0e014b87adf956a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionScalaParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf7d5d17df24a770c9108dd229ba8215e1b8336d09447bc53dc230cbd462dd7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionScalaParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__109e1894972c8fc928121c030e921cda870779015a261008b0443d1d095c2965)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6721f4223428aa295a45ea65608cc2b5c2536f1e3ce34da9fffd8b93a18e69c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fed5f5222c5cacc5f4bcdf09efb4cce1cf6aff0ef8c6e2802085ac17f8fdb38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fbd1d485e9adcf87f96c50925c4e047bf997a7e4a53a46149591c8d6d865738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionScalaParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdb6e462a6cbfffa7c8c9d2066028d2f31674363d695f23272bd2ba42cbdf4f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionScalaParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4596c4e3f8371e8b2a98046e104a6f8d73bc7633b9714d9e09d320ecb53b4911)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73fb8c8bd5e3bee9aa15327f55fc5db82fdd0f7356bb6bd62c57b86932cb8cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fa77a884f94bb600a65261c080dc0ddd57c64086a0c3151c6a223162f8c28f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8ac59be92e60f2c42db125d80667a53d189a216e2c3a17927685c9f7d93b82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionScalaParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b966c11401f38af37702d5dab34de87474cc47ad907fb10df6494ed4dfdd5be4)
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
    def internal_value(self) -> typing.Optional[FunctionScalaParametersLogLevel]:
        return typing.cast(typing.Optional[FunctionScalaParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionScalaParametersLogLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f75f404db623c910672fac572dc7b4b93fbf3dea88894c7c9ec0c964daa3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersMetricLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionScalaParametersMetricLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaParametersMetricLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaParametersMetricLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersMetricLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3d7efe0c63bc88f652a88e11f5dd8556c76000b1b15178f6b7b1f4f4eb2cfe6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionScalaParametersMetricLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec97c76a7fdccfc014d96e24b7b0efeb0cc97c54e5de9b41a905a67b8718f449)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaParametersMetricLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b609c309f50618e272324e101abb6e107b39187487efca072c3358f64f966ea6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af695b819b0a9608a83bb380b7efebfe81fa5d11e8c7e570a28c8659289a54ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4ac27e05ad437f0090a44f4cf3fe25050bc808f36515629f9494d61b48ccaa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionScalaParametersMetricLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersMetricLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__915d7905a904ef45ba1bca1be06035cb087ad6288c358b7dacbc14d59346e860)
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
    def internal_value(self) -> typing.Optional[FunctionScalaParametersMetricLevel]:
        return typing.cast(typing.Optional[FunctionScalaParametersMetricLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionScalaParametersMetricLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fdce64f93f73f7314e8d6e44ffc54822116dcc174d502bc66dccca08adc622c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionScalaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa804c2b352801988d8d37a704da1b25c6b5f971a6059d7015bcf0b31b60594)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(self) -> FunctionScalaParametersEnableConsoleOutputList:
        return typing.cast(FunctionScalaParametersEnableConsoleOutputList, jsii.get(self, "enableConsoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> FunctionScalaParametersLogLevelList:
        return typing.cast(FunctionScalaParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> FunctionScalaParametersMetricLevelList:
        return typing.cast(FunctionScalaParametersMetricLevelList, jsii.get(self, "metricLevel"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "FunctionScalaParametersTraceLevelList":
        return typing.cast("FunctionScalaParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionScalaParameters]:
        return typing.cast(typing.Optional[FunctionScalaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FunctionScalaParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419ce3c7b2d6e0e4be8d3695a831e7728de5a13bf08742850d383148d821aa2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionScalaParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e89f554fd10e67fd64ad070297a8af8690bd81ab749eadd960552937844652e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionScalaParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d652e8d18e2713ca63ad3b83281f4f20a0a2ebe4802f79bca674b85ba7b62e54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45854392cbf189f9a61c891af86392dba64fde126a56b2cebabb1feead7eaad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3934afe5281d9c335333bb0a2cd737f7774b2bd8b88c6d4981772474fcc4f47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11f91ffa4c7ec1af62a2dcac5ef794f8994eb32ee653a08e358367ac0fcc4aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionScalaParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25f3f88850d50c19ad7e17ce0b3a340d00ce96ad3183fe2cf2b7459405f52ae4)
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
    def internal_value(self) -> typing.Optional[FunctionScalaParametersTraceLevel]:
        return typing.cast(typing.Optional[FunctionScalaParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionScalaParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f01c9447caf7dd41dd3e03bcc242a67028666a532cf5d51cda9e063fb0d4eb35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "secret_variable_name": "secretVariableName",
    },
)
class FunctionScalaSecrets:
    def __init__(
        self,
        *,
        secret_id: builtins.str,
        secret_variable_name: builtins.str,
    ) -> None:
        '''
        :param secret_id: Fully qualified name of the allowed `secret <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_. You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the EXTERNAL_ACCESS_INTEGRATIONS parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#secret_id FunctionScala#secret_id}
        :param secret_variable_name: The variable that will be used in handler code when retrieving information from the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#secret_variable_name FunctionScala#secret_variable_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73daece52fc7f9ac71faa002143873af0b9df7eb88d07357e7431b4acb6d4c9)
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument secret_variable_name", value=secret_variable_name, expected_type=type_hints["secret_variable_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_id": secret_id,
            "secret_variable_name": secret_variable_name,
        }

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''Fully qualified name of the allowed `secret <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_. You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the EXTERNAL_ACCESS_INTEGRATIONS parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#secret_id FunctionScala#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_variable_name(self) -> builtins.str:
        '''The variable that will be used in handler code when retrieving information from the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#secret_variable_name FunctionScala#secret_variable_name}
        '''
        result = self._values.get("secret_variable_name")
        assert result is not None, "Required property 'secret_variable_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaSecretsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaSecretsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d0789a9fa53b4542b53fe567aa2e0cd5bd3b7662a727bc4e360608a4375fe98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionScalaSecretsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c75696c5e08f9019ed9e1d95dff9fa7998adf5fac956e3a4d31e855dad70016)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaSecretsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fffae9534ba09f1e6b0c82bcf72eba58400dde5f3cb7da034c3befb76ee46ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3368ae0f09a0efc352450490ea7f870215532014da4e18c538bcce08edf65459)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77b5ea4f5e1bb75f5679753c0d397837436d4406f6fa09ed79327455e2e452b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaSecrets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaSecrets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaSecrets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__960d560bb8515de6f215ccf4eb80a53eeb14815333d0dc87e6a5716947a6ba61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionScalaSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93d99a856f660d78cf5dee89ffe9a90d5d0013ff62db33f1942dfc3c43602866)
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
            type_hints = typing.get_type_hints(_typecheckingstub__319200f4a88a5ded8aeb7a910536e4cb0aa6b998d29cbc4040e70910cceee12e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVariableName")
    def secret_variable_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVariableName"))

    @secret_variable_name.setter
    def secret_variable_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d8c896af73256e2c29fd9f625af33cde9e9013be9e09499a6398d42a16119b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVariableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaSecrets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaSecrets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaSecrets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880e7c4700ae44852f633b9604bea7cfba3acaab530c6fe56d1e7361306940ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionScalaShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dee75dbd0292b8eae8565a713a7a982b90230a121f431c57a3eddd0c0bcab38d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FunctionScalaShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c49894584338ffc86a5f8ba310efad51b762462f8449688ac3fe7fd7b1ae097)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionScalaShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4681f696d1f4f6435802b22ee8fbf06eac85ec0cb0a8a0b318365ca43c38bdee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7123255361f231c4d75d9d7b2b9b9b067468fae3beb0b68d674bdd20d403059)
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
            type_hints = typing.get_type_hints(_typecheckingstub__271768d0f33ee35777b27b9b7d7d790020e62220d0851065b96da98553698eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionScalaShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5106f4564419369fa33c63854a98d28844fb0782e01cf7bdb817cfe9ec5bb6ff)
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
    def internal_value(self) -> typing.Optional[FunctionScalaShowOutput]:
        return typing.cast(typing.Optional[FunctionScalaShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FunctionScalaShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd1ac51c052169df91bffcc6af3991f1380477aadf102b2de336a2d7ad57c89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaTargetPath",
    jsii_struct_bases=[],
    name_mapping={"path_on_stage": "pathOnStage", "stage_location": "stageLocation"},
)
class FunctionScalaTargetPath:
    def __init__(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#path_on_stage FunctionScala#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#stage_location FunctionScala#stage_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a84919a7ba70cdd62ec0c75e57a707613388d8a87ae81e080e0024cd508952)
            check_type(argname="argument path_on_stage", value=path_on_stage, expected_type=type_hints["path_on_stage"])
            check_type(argname="argument stage_location", value=stage_location, expected_type=type_hints["stage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_on_stage": path_on_stage,
            "stage_location": stage_location,
        }

    @builtins.property
    def path_on_stage(self) -> builtins.str:
        '''Path for import on stage, without the leading ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#path_on_stage FunctionScala#path_on_stage}
        '''
        result = self._values.get("path_on_stage")
        assert result is not None, "Required property 'path_on_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_location(self) -> builtins.str:
        '''Stage location without leading ``@``.

        To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/function_scala#stage_location FunctionScala#stage_location}
        '''
        result = self._values.get("stage_location")
        assert result is not None, "Required property 'stage_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionScalaTargetPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionScalaTargetPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.functionScala.FunctionScalaTargetPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f325b04fa405f440757dfcfcdc1ee6cdde1fd95dd9f64d0aa777ccbe11308ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__169da18414026462a6dd8d4fb5240757e3f54ef4ab0ee67c4ba53237d9765d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathOnStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stageLocation")
    def stage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stageLocation"))

    @stage_location.setter
    def stage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fef709fd8a5984dd424ec21ee5e1c0399672eecc959dfc8bea1b8b0697aa039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionScalaTargetPath]:
        return typing.cast(typing.Optional[FunctionScalaTargetPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FunctionScalaTargetPath]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a9b2b11157508b16f0ef7fd1ac0eea1e5fa37e6e6fe80a3a362eb8a485ff11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FunctionScala",
    "FunctionScalaArguments",
    "FunctionScalaArgumentsList",
    "FunctionScalaArgumentsOutputReference",
    "FunctionScalaConfig",
    "FunctionScalaImports",
    "FunctionScalaImportsList",
    "FunctionScalaImportsOutputReference",
    "FunctionScalaParameters",
    "FunctionScalaParametersEnableConsoleOutput",
    "FunctionScalaParametersEnableConsoleOutputList",
    "FunctionScalaParametersEnableConsoleOutputOutputReference",
    "FunctionScalaParametersList",
    "FunctionScalaParametersLogLevel",
    "FunctionScalaParametersLogLevelList",
    "FunctionScalaParametersLogLevelOutputReference",
    "FunctionScalaParametersMetricLevel",
    "FunctionScalaParametersMetricLevelList",
    "FunctionScalaParametersMetricLevelOutputReference",
    "FunctionScalaParametersOutputReference",
    "FunctionScalaParametersTraceLevel",
    "FunctionScalaParametersTraceLevelList",
    "FunctionScalaParametersTraceLevelOutputReference",
    "FunctionScalaSecrets",
    "FunctionScalaSecretsList",
    "FunctionScalaSecretsOutputReference",
    "FunctionScalaShowOutput",
    "FunctionScalaShowOutputList",
    "FunctionScalaShowOutputOutputReference",
    "FunctionScalaTargetPath",
    "FunctionScalaTargetPathOutputReference",
]

publication.publish()

def _typecheckingstub__958e139092a0894d47f1aa7fcc2cbcfa3e794abf5d07b03ab30c1231d6b653bb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    handler: builtins.str,
    name: builtins.str,
    return_type: builtins.str,
    runtime_version: builtins.str,
    schema: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    function_definition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaImports, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    return_results_behavior: typing.Optional[builtins.str] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_path: typing.Optional[typing.Union[FunctionScalaTargetPath, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1d8c2d0a20561ddee397fdec302643f26407c69ff4ac936f9cb3607095de3eb0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5876b842672afc87158c6e061d93907c1925c0474cf2ad24d9e6d9d2bae492(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0239cee6814d754d8028c6364a64024d0e6c778d0d2f1da19ab6641dc3f9452(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaImports, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd36e73c3169a30d5a05184d7459290f20364c3666effc58a0e41e1475dab47(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaSecrets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5bdead7fa8ef1718827d53449d9c784144c88ab5dafd0bc90a401bb3bb031a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea8d3b7e37c4d9d3911593dc1b986c7dd30f035c73015ed636ef0e1d5cfdd26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fbea82fbad4a787a90d58da3c4f1a1c0fe334b5d1edee055e2d250465a61a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cc00c2ce05283f37e17847c0781e1401a1810aa8b6303b8393a7e07203b3f2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6546f73d084a5f26fe083139d47eea9079fe51837ca8a7e25a841e1ef5382c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0bdcc1d803947d7b341f17e3a2e0f65298db4aec27962e070fcc343493099b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b399bcfb1730ba0d0d9ae21d5c4018fcd87861ea4632aaa19159f7441410f449(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6464b5dc510025bc0ae3cba417d1fded6d3822bb5792061c4752ba0a3fcb0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d136cbe89e86a440be39969ed22937e0a466a0850c537da3c29e429dffbc55b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdf54d41221a83b1abd084c63a6a2ee9fcaa6b2409ead5f4b104f4a5266f78c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465dc2f645b160f8366b92f430bccc09ffb1894b817124e1999d7e4a0467ec2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f666673f6905591ccd043f9794bb6c8bbfae6965ff10f4ff82b559a1332ad20b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abafa06a0e9e2e8e584f4f78ff0c854c3e98be8b6ce1e8744d877df09fccfc01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16564fa1aa7c0ddf57ffd7e08990ef4fb23ada1ffffb0b1516e67f0a2487597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed8ef0306c3d3ef2be62d6499c91050e159fe966b6f5def64160a8cc0fa3ed1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c4cb7ff00b8b28df267efbcbb9b43170692142598c5958fafdef7de04959cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3098be5d2ebc98639c40183ec6234a5efc60427d13ea88fd318a60d458d8403b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__093433ce066c991f5397b3f2556ff18b2509ea5b0b8b9c7ae1c1c74222b4fde5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542f8ce70f93bb30b0df9688f572a76b7ff7570a619ee07beb50ee11bd8f736b(
    *,
    arg_data_type: builtins.str,
    arg_name: builtins.str,
    arg_default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5665673f8353e8529d3ff63c9f1909355015ebe4283da41d34a045684107dee6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5317c6ecc9dfd421934f76f305d6e4822dc28ae78881e69f46969a7ae4f68b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a38422d4420465bde2e445f05fbd3f66cbc3fef50c982a4acd124d5dafff8e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea72fb2c0db57475419bb61001c8057363ed4a4727e4ba1db30715c4f91209a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f952a6b933cbe04c7f197c5ac8dde15e95a9b54c59e3c036f65d952ce52f125(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d20189ffabab42363f1c0f760554e3d0ae58b2bd395c3cee05092429840c1d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641df5fac62e2a9517838a16ff4a2c198eaeb9360501990c1e95378332019b89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f50f55970220c6830080c3a4b7194b83b30b9f4444d6f15c4ab1ab2c3bd26e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60508ac35969671d834a93ce4199e261438ee449aa3f39d6f4843c39270101e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be4f57dc87765a0ec565f271e2710cc7629d411f8078a9dbdfe9c24dd9fbea7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7440916ffd459171d818993df680b30fe5b5b3f36e929b81d620f725983cfb1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaArguments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d742b8fa184c56a088bbe625619af784280bc3f36a22d9dca672f3f492d7bba(
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
    runtime_version: builtins.str,
    schema: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    function_definition: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaImports, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    return_results_behavior: typing.Optional[builtins.str] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionScalaSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_path: typing.Optional[typing.Union[FunctionScalaTargetPath, typing.Dict[builtins.str, typing.Any]]] = None,
    trace_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ee4e34be1591f376d54d3acb876210f1eda2add8e9af12bf34df73880f4d063(
    *,
    path_on_stage: builtins.str,
    stage_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8527e7c9b3f27ce3195382e733a2054a1fa7e836f4c504ac10dfefb0a133f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086a1eb87790a8c128d53c117bf4127288bb12a45849dfbaf90edcd0875eca6e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89261d8214c4ee8f974f8e2b732f61fc32ad8945825287b3216239169e9729b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e41f175bb8a53efa65823c7358ddb7400ba709e799b8a582183f2f1e286f738(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04cc87ef7f6438b6c701491ddb22ff42ab34b694b5e824bec650957ea899e841(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2668307b8210de08f91423636c91d524e46f8dfda9c967f1f22f47f4ff3498(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaImports]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41da8c693b62cd7c24cf0b775ecb32fce080ab9b980cfeee633af62d577f11f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c97063b0f7c5d2f6be0fe5f62397f688a99e386700451ccfd632a65ce98a78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d072b59442e57d2fc12d50e91746cf51acb3de0ee5331e36d5bdfc87f7bcc74a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f8d306b42bd72bc67b4ce85c6b672279f542713ec35f9ffb108782f73916d74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaImports]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248a406f787ee23b271d1e79fde24948f539afc27b77953892537f22fb37502a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a9715f5ef7c1e53f181bfd679d01924b685f7727886a9c38e699a57db24c00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43692000db54cedea4483e3394f1dcc4a99267573b285737f98669a657a9e06c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863a083fb37df0faff341b11a9e7004a2458b4802dd2c88a292c360adb83b3df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e51f50f79593f7e36ad5c2aa05fcec9243271b3d0362ecc2f6d5bdb0de881d8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9ad16be43ece1e0ac993e5f9c0cf8e6bc2d8f2f182119c5a7abd83713def37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b403d5b1fa45f7bdd80e56999511d8d18da1ca67e2f54a13b0e014b87adf956a(
    value: typing.Optional[FunctionScalaParametersEnableConsoleOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7d5d17df24a770c9108dd229ba8215e1b8336d09447bc53dc230cbd462dd7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109e1894972c8fc928121c030e921cda870779015a261008b0443d1d095c2965(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6721f4223428aa295a45ea65608cc2b5c2536f1e3ce34da9fffd8b93a18e69c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fed5f5222c5cacc5f4bcdf09efb4cce1cf6aff0ef8c6e2802085ac17f8fdb38(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbd1d485e9adcf87f96c50925c4e047bf997a7e4a53a46149591c8d6d865738(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdb6e462a6cbfffa7c8c9d2066028d2f31674363d695f23272bd2ba42cbdf4f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4596c4e3f8371e8b2a98046e104a6f8d73bc7633b9714d9e09d320ecb53b4911(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73fb8c8bd5e3bee9aa15327f55fc5db82fdd0f7356bb6bd62c57b86932cb8cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa77a884f94bb600a65261c080dc0ddd57c64086a0c3151c6a223162f8c28f0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ac59be92e60f2c42db125d80667a53d189a216e2c3a17927685c9f7d93b82d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b966c11401f38af37702d5dab34de87474cc47ad907fb10df6494ed4dfdd5be4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f75f404db623c910672fac572dc7b4b93fbf3dea88894c7c9ec0c964daa3c1(
    value: typing.Optional[FunctionScalaParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d7efe0c63bc88f652a88e11f5dd8556c76000b1b15178f6b7b1f4f4eb2cfe6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec97c76a7fdccfc014d96e24b7b0efeb0cc97c54e5de9b41a905a67b8718f449(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b609c309f50618e272324e101abb6e107b39187487efca072c3358f64f966ea6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af695b819b0a9608a83bb380b7efebfe81fa5d11e8c7e570a28c8659289a54ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ac27e05ad437f0090a44f4cf3fe25050bc808f36515629f9494d61b48ccaa5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__915d7905a904ef45ba1bca1be06035cb087ad6288c358b7dacbc14d59346e860(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fdce64f93f73f7314e8d6e44ffc54822116dcc174d502bc66dccca08adc622c(
    value: typing.Optional[FunctionScalaParametersMetricLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa804c2b352801988d8d37a704da1b25c6b5f971a6059d7015bcf0b31b60594(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419ce3c7b2d6e0e4be8d3695a831e7728de5a13bf08742850d383148d821aa2f(
    value: typing.Optional[FunctionScalaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e89f554fd10e67fd64ad070297a8af8690bd81ab749eadd960552937844652e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d652e8d18e2713ca63ad3b83281f4f20a0a2ebe4802f79bca674b85ba7b62e54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45854392cbf189f9a61c891af86392dba64fde126a56b2cebabb1feead7eaad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3934afe5281d9c335333bb0a2cd737f7774b2bd8b88c6d4981772474fcc4f47(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f91ffa4c7ec1af62a2dcac5ef794f8994eb32ee653a08e358367ac0fcc4aed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f3f88850d50c19ad7e17ce0b3a340d00ce96ad3183fe2cf2b7459405f52ae4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f01c9447caf7dd41dd3e03bcc242a67028666a532cf5d51cda9e063fb0d4eb35(
    value: typing.Optional[FunctionScalaParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73daece52fc7f9ac71faa002143873af0b9df7eb88d07357e7431b4acb6d4c9(
    *,
    secret_id: builtins.str,
    secret_variable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0789a9fa53b4542b53fe567aa2e0cd5bd3b7662a727bc4e360608a4375fe98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c75696c5e08f9019ed9e1d95dff9fa7998adf5fac956e3a4d31e855dad70016(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fffae9534ba09f1e6b0c82bcf72eba58400dde5f3cb7da034c3befb76ee46ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3368ae0f09a0efc352450490ea7f870215532014da4e18c538bcce08edf65459(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b5ea4f5e1bb75f5679753c0d397837436d4406f6fa09ed79327455e2e452b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960d560bb8515de6f215ccf4eb80a53eeb14815333d0dc87e6a5716947a6ba61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionScalaSecrets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d99a856f660d78cf5dee89ffe9a90d5d0013ff62db33f1942dfc3c43602866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319200f4a88a5ded8aeb7a910536e4cb0aa6b998d29cbc4040e70910cceee12e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d8c896af73256e2c29fd9f625af33cde9e9013be9e09499a6398d42a16119b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880e7c4700ae44852f633b9604bea7cfba3acaab530c6fe56d1e7361306940ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionScalaSecrets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee75dbd0292b8eae8565a713a7a982b90230a121f431c57a3eddd0c0bcab38d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c49894584338ffc86a5f8ba310efad51b762462f8449688ac3fe7fd7b1ae097(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4681f696d1f4f6435802b22ee8fbf06eac85ec0cb0a8a0b318365ca43c38bdee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7123255361f231c4d75d9d7b2b9b9b067468fae3beb0b68d674bdd20d403059(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271768d0f33ee35777b27b9b7d7d790020e62220d0851065b96da98553698eb9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5106f4564419369fa33c63854a98d28844fb0782e01cf7bdb817cfe9ec5bb6ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd1ac51c052169df91bffcc6af3991f1380477aadf102b2de336a2d7ad57c89(
    value: typing.Optional[FunctionScalaShowOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a84919a7ba70cdd62ec0c75e57a707613388d8a87ae81e080e0024cd508952(
    *,
    path_on_stage: builtins.str,
    stage_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f325b04fa405f440757dfcfcdc1ee6cdde1fd95dd9f64d0aa777ccbe11308ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169da18414026462a6dd8d4fb5240757e3f54ef4ab0ee67c4ba53237d9765d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fef709fd8a5984dd424ec21ee5e1c0399672eecc959dfc8bea1b8b0697aa039(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a9b2b11157508b16f0ef7fd1ac0eea1e5fa37e6e6fe80a3a362eb8a485ff11(
    value: typing.Optional[FunctionScalaTargetPath],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `snowflake_procedure_java`

Refer to the Terraform Registry for docs: [`snowflake_procedure_java`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java).
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


class ProcedureJava(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJava",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java snowflake_procedure_java}.'''

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
        snowpark_package: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureJavaArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        execute_as: typing.Optional[builtins.str] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureJavaImports", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        procedure_definition: typing.Optional[builtins.str] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureJavaSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_path: typing.Optional[typing.Union["ProcedureJavaTargetPath", typing.Dict[builtins.str, typing.Any]]] = None,
        trace_level: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java snowflake_procedure_java} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the procedure. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#database ProcedureJava#database}
        :param handler: Use the fully qualified name of the method or function for the stored procedure. This is typically in the following form ``com.my_company.my_package.MyClass.myMethod`` where ``com.my_company.my_package`` corresponds to the package containing the object or class: ``package com.my_company.my_package;``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#handler ProcedureJava#handler}
        :param name: The name of the procedure; the identifier does not need to be unique for the schema in which the procedure is created because stored procedures are `identified and resolved by the combination of the name and argument types <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-naming-conventions.html#label-procedure-function-name-overloading>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#name ProcedureJava#name}
        :param return_type: Specifies the type of the result returned by the stored procedure. For ``<result_data_type>``, use the Snowflake data type that corresponds to the type of the language that you are using (see `SQL-Java Data Type Mappings <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-data-type-mapping.html#label-sql-java-data-type-mappings>`_). For ``RETURNS TABLE ( [ col_name col_data_type [ , ... ] ] )``, if you know the Snowflake data types of the columns in the returned table, specify the column names and types. Otherwise (e.g. if you are determining the column types during run time), you can omit the column names and types (i.e. ``TABLE ()``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#return_type ProcedureJava#return_type}
        :param runtime_version: The language runtime version to use. Currently, the supported versions are: 11. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#runtime_version ProcedureJava#runtime_version}
        :param schema: The schema in which to create the procedure. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#schema ProcedureJava#schema}
        :param snowpark_package: The Snowpark package is required for stored procedures, so it must always be present. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#snowpark_package ProcedureJava#snowpark_package}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arguments ProcedureJava#arguments}
        :param comment: Specifies a comment for the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#comment ProcedureJava#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#enable_console_output ProcedureJava#enable_console_output}
        :param execute_as: Specifies whether the stored procedure executes with the privileges of the owner (an “owner’s rights” stored procedure) or with the privileges of the caller (a “caller’s rights” stored procedure). If you execute the statement CREATE PROCEDURE … EXECUTE AS CALLER, then in the future the procedure will execute as a caller’s rights procedure. If you execute CREATE PROCEDURE … EXECUTE AS OWNER, then the procedure will execute as an owner’s rights procedure. For more information, see `Understanding caller’s rights and owner’s rights stored procedures <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_. Valid values are (case-insensitive): ``CALLER`` | ``OWNER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#execute_as ProcedureJava#execute_as}
        :param external_access_integrations: The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this procedure’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#external_access_integrations ProcedureJava#external_access_integrations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#id ProcedureJava#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: imports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#imports ProcedureJava#imports}
        :param is_secure: Specifies that the procedure is secure. For more information about secure procedures, see `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#is_secure ProcedureJava#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#log_level ProcedureJava#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#metric_level ProcedureJava#metric_level}
        :param null_input_behavior: Specifies the behavior of the procedure when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#null_input_behavior ProcedureJava#null_input_behavior}
        :param packages: List of the names of packages deployed in Snowflake that should be included in the handler code’s execution environment. The Snowpark package is required for stored procedures, but is specified in the ``snowpark_package`` attribute. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#packages ProcedureJava#packages}
        :param procedure_definition: Defines the code executed by the stored procedure. The definition can consist of any valid code. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``procedure_definition`` value must be Java source code. For more information, see `Java (using Snowpark) <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-java>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#procedure_definition ProcedureJava#procedure_definition}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#secrets ProcedureJava#secrets}
        :param target_path: target_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#target_path ProcedureJava#target_path}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#trace_level ProcedureJava#trace_level}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__163c416553ac38d2252f2d2caa055f421f952c20efa9c0e75bfb9e891dab116e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProcedureJavaConfig(
            database=database,
            handler=handler,
            name=name,
            return_type=return_type,
            runtime_version=runtime_version,
            schema=schema,
            snowpark_package=snowpark_package,
            arguments=arguments,
            comment=comment,
            enable_console_output=enable_console_output,
            execute_as=execute_as,
            external_access_integrations=external_access_integrations,
            id=id,
            imports=imports,
            is_secure=is_secure,
            log_level=log_level,
            metric_level=metric_level,
            null_input_behavior=null_input_behavior,
            packages=packages,
            procedure_definition=procedure_definition,
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
        '''Generates CDKTF code for importing a ProcedureJava resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProcedureJava to import.
        :param import_from_id: The id of the existing ProcedureJava that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProcedureJava to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a65c81a4984a83ac300a14360e880a22dcce6c7a28e372dd5f90ebd6b07c880)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureJavaArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef09e63c0249c92cb4dce3055bd62f29bb5c1b54d314270e5cf85c82e73b3301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArguments", [value]))

    @jsii.member(jsii_name="putImports")
    def put_imports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureJavaImports", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7472653bc6c4ca1e777867180501f75fd2cb043eb2a5f1969bf0d24ff5df9e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putImports", [value]))

    @jsii.member(jsii_name="putSecrets")
    def put_secrets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureJavaSecrets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7914d4d014404313f1aeee3bc7064a997171bae7219d181a40ce42050357e3ab)
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
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#path_on_stage ProcedureJava#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#stage_location ProcedureJava#stage_location}
        '''
        value = ProcedureJavaTargetPath(
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

    @jsii.member(jsii_name="resetExecuteAs")
    def reset_execute_as(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecuteAs", []))

    @jsii.member(jsii_name="resetExternalAccessIntegrations")
    def reset_external_access_integrations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalAccessIntegrations", []))

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

    @jsii.member(jsii_name="resetProcedureDefinition")
    def reset_procedure_definition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcedureDefinition", []))

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
    def arguments(self) -> "ProcedureJavaArgumentsList":
        return typing.cast("ProcedureJavaArgumentsList", jsii.get(self, "arguments"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="imports")
    def imports(self) -> "ProcedureJavaImportsList":
        return typing.cast("ProcedureJavaImportsList", jsii.get(self, "imports"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "ProcedureJavaParametersList":
        return typing.cast("ProcedureJavaParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="procedureLanguage")
    def procedure_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "procedureLanguage"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "ProcedureJavaSecretsList":
        return typing.cast("ProcedureJavaSecretsList", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ProcedureJavaShowOutputList":
        return typing.cast("ProcedureJavaShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="targetPath")
    def target_path(self) -> "ProcedureJavaTargetPathOutputReference":
        return typing.cast("ProcedureJavaTargetPathOutputReference", jsii.get(self, "targetPath"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaArguments"]]], jsii.get(self, "argumentsInput"))

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
    @jsii.member(jsii_name="executeAsInput")
    def execute_as_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executeAsInput"))

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrationsInput")
    def external_access_integrations_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalAccessIntegrationsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaImports"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaImports"]]], jsii.get(self, "importsInput"))

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
    @jsii.member(jsii_name="procedureDefinitionInput")
    def procedure_definition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "procedureDefinitionInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaSecrets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaSecrets"]]], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="snowparkPackageInput")
    def snowpark_package_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowparkPackageInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPathInput")
    def target_path_input(self) -> typing.Optional["ProcedureJavaTargetPath"]:
        return typing.cast(typing.Optional["ProcedureJavaTargetPath"], jsii.get(self, "targetPathInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9a0507764ba4cc07353c20655673977838ef2ed5847722d1143d04785fbef6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d3de65a60b3d41e394a6f4db5ace603a5eb6e2cd0a30fcb57d3eedd9fef600d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1402911cf183084b571900f07bbacc3a952dd5815a5c5c0204f6ae42be6db514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsoleOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executeAs")
    def execute_as(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executeAs"))

    @execute_as.setter
    def execute_as(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d297db2bf88ca898b30d19e70c338883004b7bc44751f584627442c9be12a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeAs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrations")
    def external_access_integrations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalAccessIntegrations"))

    @external_access_integrations.setter
    def external_access_integrations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f89a3125364220c2504d3d283e5db1a45c0d8775d81625bd14a5a2bb9e8a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAccessIntegrations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965c803e75f31fe8fce908f70a73e3c80e1ce0564243589a41dbc1fbeec24da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4fafdbde9cc4939efd422cf672b42b868f9af59524f19297f4b5f3ceb63a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isSecure"))

    @is_secure.setter
    def is_secure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86483a646dffa4f797eac547c7f7f200fc49cbd8a3c4212e243162630aee248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8651547304b4d242dc91624fc8f93ed118d4eb8c168bdf1d2af82b3d08ff5aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricLevel"))

    @metric_level.setter
    def metric_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e81f8cf134ac282468c9de3901f35b59aa31ec153fc684dafe070a6e8f695b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dda2faba22342b8784987bb764b2bccc1c3cf055c07a8a004d40237daf57825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullInputBehavior")
    def null_input_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullInputBehavior"))

    @null_input_behavior.setter
    def null_input_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e927d531d744157a0a157f3eec5c8b1f435e2b99f0ab8c6029b1c5134018760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullInputBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packages")
    def packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packages"))

    @packages.setter
    def packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701e07bb237e03bc6a2f3119851e0af0bffecc37244acf81c19b040ddc62f3b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="procedureDefinition")
    def procedure_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "procedureDefinition"))

    @procedure_definition.setter
    def procedure_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8857d650400dfa5abb240863391b1186071fc4e3e4901e906f1157dfb09d72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "procedureDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db41ad7e1bf472a051128aaefaa55996c345769427b149e40108c3bb43854151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3a4fe063dac70ca4d2b294623426a5946004030aeb3f9f67b99c2e0bf2276e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d6094f67f368cb377b51ee5f9059a162a7fbdaba07022eb34797aaa09411510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snowparkPackage")
    def snowpark_package(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowparkPackage"))

    @snowpark_package.setter
    def snowpark_package(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101b9b611e5bbc55410a389db56577cdffd8ff0b2d340b124b6827dfb6bed03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowparkPackage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f46624064a2a3668a0c30f5b633937de5b4ba33a94fd965bc2469ef29dfb2f60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaArguments",
    jsii_struct_bases=[],
    name_mapping={
        "arg_data_type": "argDataType",
        "arg_name": "argName",
        "arg_default_value": "argDefaultValue",
    },
)
class ProcedureJavaArguments:
    def __init__(
        self,
        *,
        arg_data_type: builtins.str,
        arg_name: builtins.str,
        arg_default_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arg_data_type: The argument type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arg_data_type ProcedureJava#arg_data_type}
        :param arg_name: The argument name. The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the procedure definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arg_name ProcedureJava#arg_name}
        :param arg_default_value: Optional default value for the argument. For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arg_default_value ProcedureJava#arg_default_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f5d71391e883bd57d576ea657844126cc9c8f7fce2cd2edd229d8146f3fdef2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arg_data_type ProcedureJava#arg_data_type}
        '''
        result = self._values.get("arg_data_type")
        assert result is not None, "Required property 'arg_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_name(self) -> builtins.str:
        '''The argument name.

        The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the procedure definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arg_name ProcedureJava#arg_name}
        '''
        result = self._values.get("arg_name")
        assert result is not None, "Required property 'arg_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_default_value(self) -> typing.Optional[builtins.str]:
        '''Optional default value for the argument.

        For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arg_default_value ProcedureJava#arg_default_value}
        '''
        result = self._values.get("arg_default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaArgumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eb36f2c48fefe951d755189879eb45fd3f5efe054f88bd3f3f4388ac0645060)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureJavaArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefe0533ae61fe6583e977d1a7e9af2e34e181af8373ff22873cd86f39547f72)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2046dbf4f15f46b3ccf66d3239b4f7dcbf87c6183ac481205b93cb336a1928d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65d2e6b270d1ca368d27b30ba5d949bd7e86644008017c229da9673273f817a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff4554e57e785b070c9caeb6f9a52150d620a43ebe4fa25df7890c52659bab56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23545003101cc174e3d953dc94228f7c9013a93828d811fda652210814fd6458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaArgumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91e62c5bf47f997abe438b2605c11c1694608b8be5589ae67070c297d23ebee6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a24598132c7b878202f23b9a4c38b54fb9a6c990550f30404f6b02fd249c155)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argDefaultValue")
    def arg_default_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argDefaultValue"))

    @arg_default_value.setter
    def arg_default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d70f67d5a78d6c24af0c59989478629ca16387ba93e83f719ac03b791f2008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDefaultValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argName")
    def arg_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argName"))

    @arg_name.setter
    def arg_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63bc9386703ed5131fa7f43dd39c08b5c15d5d2fae0b50d6397ebed30f440ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaArguments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaArguments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaArguments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1344235d3ee6e7afd19dfda81fddb488cf48823dfa67b209532b01ccceaedd0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaConfig",
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
        "snowpark_package": "snowparkPackage",
        "arguments": "arguments",
        "comment": "comment",
        "enable_console_output": "enableConsoleOutput",
        "execute_as": "executeAs",
        "external_access_integrations": "externalAccessIntegrations",
        "id": "id",
        "imports": "imports",
        "is_secure": "isSecure",
        "log_level": "logLevel",
        "metric_level": "metricLevel",
        "null_input_behavior": "nullInputBehavior",
        "packages": "packages",
        "procedure_definition": "procedureDefinition",
        "secrets": "secrets",
        "target_path": "targetPath",
        "trace_level": "traceLevel",
    },
)
class ProcedureJavaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        snowpark_package: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        execute_as: typing.Optional[builtins.str] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureJavaImports", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        procedure_definition: typing.Optional[builtins.str] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureJavaSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_path: typing.Optional[typing.Union["ProcedureJavaTargetPath", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param database: The database in which to create the procedure. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#database ProcedureJava#database}
        :param handler: Use the fully qualified name of the method or function for the stored procedure. This is typically in the following form ``com.my_company.my_package.MyClass.myMethod`` where ``com.my_company.my_package`` corresponds to the package containing the object or class: ``package com.my_company.my_package;``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#handler ProcedureJava#handler}
        :param name: The name of the procedure; the identifier does not need to be unique for the schema in which the procedure is created because stored procedures are `identified and resolved by the combination of the name and argument types <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-naming-conventions.html#label-procedure-function-name-overloading>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#name ProcedureJava#name}
        :param return_type: Specifies the type of the result returned by the stored procedure. For ``<result_data_type>``, use the Snowflake data type that corresponds to the type of the language that you are using (see `SQL-Java Data Type Mappings <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-data-type-mapping.html#label-sql-java-data-type-mappings>`_). For ``RETURNS TABLE ( [ col_name col_data_type [ , ... ] ] )``, if you know the Snowflake data types of the columns in the returned table, specify the column names and types. Otherwise (e.g. if you are determining the column types during run time), you can omit the column names and types (i.e. ``TABLE ()``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#return_type ProcedureJava#return_type}
        :param runtime_version: The language runtime version to use. Currently, the supported versions are: 11. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#runtime_version ProcedureJava#runtime_version}
        :param schema: The schema in which to create the procedure. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#schema ProcedureJava#schema}
        :param snowpark_package: The Snowpark package is required for stored procedures, so it must always be present. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#snowpark_package ProcedureJava#snowpark_package}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arguments ProcedureJava#arguments}
        :param comment: Specifies a comment for the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#comment ProcedureJava#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#enable_console_output ProcedureJava#enable_console_output}
        :param execute_as: Specifies whether the stored procedure executes with the privileges of the owner (an “owner’s rights” stored procedure) or with the privileges of the caller (a “caller’s rights” stored procedure). If you execute the statement CREATE PROCEDURE … EXECUTE AS CALLER, then in the future the procedure will execute as a caller’s rights procedure. If you execute CREATE PROCEDURE … EXECUTE AS OWNER, then the procedure will execute as an owner’s rights procedure. For more information, see `Understanding caller’s rights and owner’s rights stored procedures <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_. Valid values are (case-insensitive): ``CALLER`` | ``OWNER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#execute_as ProcedureJava#execute_as}
        :param external_access_integrations: The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this procedure’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#external_access_integrations ProcedureJava#external_access_integrations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#id ProcedureJava#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: imports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#imports ProcedureJava#imports}
        :param is_secure: Specifies that the procedure is secure. For more information about secure procedures, see `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#is_secure ProcedureJava#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#log_level ProcedureJava#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#metric_level ProcedureJava#metric_level}
        :param null_input_behavior: Specifies the behavior of the procedure when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#null_input_behavior ProcedureJava#null_input_behavior}
        :param packages: List of the names of packages deployed in Snowflake that should be included in the handler code’s execution environment. The Snowpark package is required for stored procedures, but is specified in the ``snowpark_package`` attribute. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#packages ProcedureJava#packages}
        :param procedure_definition: Defines the code executed by the stored procedure. The definition can consist of any valid code. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``procedure_definition`` value must be Java source code. For more information, see `Java (using Snowpark) <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-java>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#procedure_definition ProcedureJava#procedure_definition}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#secrets ProcedureJava#secrets}
        :param target_path: target_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#target_path ProcedureJava#target_path}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#trace_level ProcedureJava#trace_level}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(target_path, dict):
            target_path = ProcedureJavaTargetPath(**target_path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77f50f1ba8493312d0b22bb18d92c3cc1c0dee633488253d27fe0d5e95f90de)
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
            check_type(argname="argument snowpark_package", value=snowpark_package, expected_type=type_hints["snowpark_package"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument enable_console_output", value=enable_console_output, expected_type=type_hints["enable_console_output"])
            check_type(argname="argument execute_as", value=execute_as, expected_type=type_hints["execute_as"])
            check_type(argname="argument external_access_integrations", value=external_access_integrations, expected_type=type_hints["external_access_integrations"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument imports", value=imports, expected_type=type_hints["imports"])
            check_type(argname="argument is_secure", value=is_secure, expected_type=type_hints["is_secure"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument metric_level", value=metric_level, expected_type=type_hints["metric_level"])
            check_type(argname="argument null_input_behavior", value=null_input_behavior, expected_type=type_hints["null_input_behavior"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument procedure_definition", value=procedure_definition, expected_type=type_hints["procedure_definition"])
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
            "snowpark_package": snowpark_package,
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
        if execute_as is not None:
            self._values["execute_as"] = execute_as
        if external_access_integrations is not None:
            self._values["external_access_integrations"] = external_access_integrations
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
        if procedure_definition is not None:
            self._values["procedure_definition"] = procedure_definition
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
        '''The database in which to create the procedure.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#database ProcedureJava#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''Use the fully qualified name of the method or function for the stored procedure.

        This is typically in the following form ``com.my_company.my_package.MyClass.myMethod`` where ``com.my_company.my_package`` corresponds to the package containing the object or class: ``package com.my_company.my_package;``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#handler ProcedureJava#handler}
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the procedure;

        the identifier does not need to be unique for the schema in which the procedure is created because stored procedures are `identified and resolved by the combination of the name and argument types <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-naming-conventions.html#label-procedure-function-name-overloading>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#name ProcedureJava#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def return_type(self) -> builtins.str:
        '''Specifies the type of the result returned by the stored procedure.

        For ``<result_data_type>``, use the Snowflake data type that corresponds to the type of the language that you are using (see `SQL-Java Data Type Mappings <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-data-type-mapping.html#label-sql-java-data-type-mappings>`_). For ``RETURNS TABLE ( [ col_name col_data_type [ , ... ] ] )``, if you know the Snowflake data types of the columns in the returned table, specify the column names and types. Otherwise (e.g. if you are determining the column types during run time), you can omit the column names and types (i.e. ``TABLE ()``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#return_type ProcedureJava#return_type}
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''The language runtime version to use. Currently, the supported versions are: 11.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#runtime_version ProcedureJava#runtime_version}
        '''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the procedure.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#schema ProcedureJava#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snowpark_package(self) -> builtins.str:
        '''The Snowpark package is required for stored procedures, so it must always be present.

        For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#snowpark_package ProcedureJava#snowpark_package}
        '''
        result = self._values.get("snowpark_package")
        assert result is not None, "Required property 'snowpark_package' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#arguments ProcedureJava#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaArguments]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the procedure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#comment ProcedureJava#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_console_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable stdout/stderr fast path logging for anonyous stored procs.

        This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#enable_console_output ProcedureJava#enable_console_output}
        '''
        result = self._values.get("enable_console_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def execute_as(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the stored procedure executes with the privileges of the owner (an “owner’s rights” stored procedure) or with the privileges of the caller (a “caller’s rights” stored procedure).

        If you execute the statement CREATE PROCEDURE … EXECUTE AS CALLER, then in the future the procedure will execute as a caller’s rights procedure. If you execute CREATE PROCEDURE … EXECUTE AS OWNER, then the procedure will execute as an owner’s rights procedure. For more information, see `Understanding caller’s rights and owner’s rights stored procedures <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_. Valid values are (case-insensitive): ``CALLER`` | ``OWNER``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#execute_as ProcedureJava#execute_as}
        '''
        result = self._values.get("execute_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_access_integrations(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this procedure’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#external_access_integrations ProcedureJava#external_access_integrations}
        '''
        result = self._values.get("external_access_integrations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#id ProcedureJava#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaImports"]]]:
        '''imports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#imports ProcedureJava#imports}
        '''
        result = self._values.get("imports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaImports"]]], result)

    @builtins.property
    def is_secure(self) -> typing.Optional[builtins.str]:
        '''Specifies that the procedure is secure.

        For more information about secure procedures, see `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#is_secure ProcedureJava#is_secure}
        '''
        result = self._values.get("is_secure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#log_level ProcedureJava#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_level(self) -> typing.Optional[builtins.str]:
        '''METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#metric_level ProcedureJava#metric_level}
        '''
        result = self._values.get("metric_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def null_input_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the procedure when called with null inputs.

        Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#null_input_behavior ProcedureJava#null_input_behavior}
        '''
        result = self._values.get("null_input_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of the names of packages deployed in Snowflake that should be included in the handler code’s execution environment.

        The Snowpark package is required for stored procedures, but is specified in the ``snowpark_package`` attribute. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#packages ProcedureJava#packages}
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def procedure_definition(self) -> typing.Optional[builtins.str]:
        '''Defines the code executed by the stored procedure.

        The definition can consist of any valid code. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``procedure_definition`` value must be Java source code. For more information, see `Java (using Snowpark) <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-java>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#procedure_definition ProcedureJava#procedure_definition}
        '''
        result = self._values.get("procedure_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaSecrets"]]]:
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#secrets ProcedureJava#secrets}
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureJavaSecrets"]]], result)

    @builtins.property
    def target_path(self) -> typing.Optional["ProcedureJavaTargetPath"]:
        '''target_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#target_path ProcedureJava#target_path}
        '''
        result = self._values.get("target_path")
        return typing.cast(typing.Optional["ProcedureJavaTargetPath"], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#trace_level ProcedureJava#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaImports",
    jsii_struct_bases=[],
    name_mapping={"path_on_stage": "pathOnStage", "stage_location": "stageLocation"},
)
class ProcedureJavaImports:
    def __init__(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#path_on_stage ProcedureJava#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#stage_location ProcedureJava#stage_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbad3cfd5678d71f454a0375333773a75bb1dcacf8dcf0c6ec059f8663c6b6ea)
            check_type(argname="argument path_on_stage", value=path_on_stage, expected_type=type_hints["path_on_stage"])
            check_type(argname="argument stage_location", value=stage_location, expected_type=type_hints["stage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_on_stage": path_on_stage,
            "stage_location": stage_location,
        }

    @builtins.property
    def path_on_stage(self) -> builtins.str:
        '''Path for import on stage, without the leading ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#path_on_stage ProcedureJava#path_on_stage}
        '''
        result = self._values.get("path_on_stage")
        assert result is not None, "Required property 'path_on_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_location(self) -> builtins.str:
        '''Stage location without leading ``@``.

        To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#stage_location ProcedureJava#stage_location}
        '''
        result = self._values.get("stage_location")
        assert result is not None, "Required property 'stage_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaImports(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaImportsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaImportsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35b17ebc1fa55ddef36b81d43033fd2a3f0715aa9ec10b37befd24b22a0faa88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureJavaImportsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e52f5a593cccaec6a153e0196d1d12389d4536ff6632bdf30a63fffe1d6e48)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaImportsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a6dffa703f2946388d3fee01399da8cf2f9b5dd4ab0034c71226d1b839a9e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86955848da16bad9e5ff4350e42b3ada21163c8bbe93ec3ccf3e32712676c48f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad620707626e949e2653c576f83fc781fe456ef0f4d12fe6bbcadd012c8e849b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaImports]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaImports]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaImports]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7a6f90133fc17cb57ce056054bb3517d38acb45e9b0c44a8a35d48a424842a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaImportsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaImportsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__195313080867fac6830c0ecb9b92df042287c14bb1a8db7622b8309f85386f6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__427075812237f9f9deaad9b72f67ce3fb53b113182df81546c6195592102c10c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathOnStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stageLocation")
    def stage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stageLocation"))

    @stage_location.setter
    def stage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462b3f696a23bb3d48025fad58946a92cc8b37bfb047248cba61523495094d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaImports]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaImports]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaImports]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd968545806d8d0d7fb1dd19c46a59a26ef820de703b1fa0f163395239ecd3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureJavaParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersEnableConsoleOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureJavaParametersEnableConsoleOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaParametersEnableConsoleOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaParametersEnableConsoleOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersEnableConsoleOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f2553711f6f1c676460784b2c40fc9d6977e0caf8d028a7d31ae238a03a7c90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProcedureJavaParametersEnableConsoleOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07764bfc6276cf4a147f5c0cf166ec16b515315629eb6a639d0a146762d03af3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaParametersEnableConsoleOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c203ab8159908d2e5d3dee59106c823f67c3de87e0d1082353e3fe545e8878)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6f1aeb3e3099acca8d8871313ca07cc0290f88ff994acfe8e162371232804fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85cb6c2529f685c718a638ae5da9a9c838660f81ed1190bddf7dfc196769ec11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaParametersEnableConsoleOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersEnableConsoleOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__faaec32d134d2073f85d4a8c3db1f2aa1d342c5bcbb87cf580488b68aac4445c)
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
    ) -> typing.Optional[ProcedureJavaParametersEnableConsoleOutput]:
        return typing.cast(typing.Optional[ProcedureJavaParametersEnableConsoleOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProcedureJavaParametersEnableConsoleOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__144b95875b04a2c48c6b95471b93f5f1d273603540b15aad91b3ed5fd74ebe4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39b1ec65660babd40b470ca0874a378389863971ea183a6b231adfbe51cb4730)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureJavaParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70edeb0c0843284436e32a3216cf896cedde3dedaef40ef1068f8747a7488b69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717a3cee6b6f8be8184a7c75014c092e30cc6ce4758bbe16ffeb84ddff035211)
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
            type_hints = typing.get_type_hints(_typecheckingstub__849ef7af80579957a0ab667ebcd662e4b1d7a5e62bc76ebebbcc119a3fe5c102)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40d004c2349e44fc4a68df7cf9a38d148dcb036663a236ada71665564e52e36d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureJavaParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__22132bc32583fc5cc515b883403e527e99fb2a40977e58309dcedecea272fe10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProcedureJavaParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c90e8b0eced5d391219797e1cf4c5dfef62e660700209831020728f169d23ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296665af977127b0355bd6cd24f48aef46049dd8b11d1b2f434acd9cba483f67)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0a7547ef7b9fb67875c1268ec47fadf4776763dcdd8e7374ef2c28eced00f02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfec7d2c39d1b93f0a16b154a350ee2c491d1b70b7d9662b1ccb5a84fdd3c38a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f4412255e3aeeb5721acbd26a3a27fe57684bfd0e1a11c04757fa6f21d1599c)
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
    def internal_value(self) -> typing.Optional[ProcedureJavaParametersLogLevel]:
        return typing.cast(typing.Optional[ProcedureJavaParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProcedureJavaParametersLogLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f0c6746a423ac333966769196fa82ca9a1ef30c73e063d4caa95309ed778ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersMetricLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureJavaParametersMetricLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaParametersMetricLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaParametersMetricLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersMetricLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fc7deac6e40de39fff819bf36870e758953dc63c25db7a252acacaa229274ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProcedureJavaParametersMetricLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71cbafab3c7de2cc74e0146ad71ccd5752f98e9dde38ecf93194b765b6b4e31d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaParametersMetricLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445acca907738d96cf6a6caf4f6c41be3711a4250d52ff14df3e4e4924f0314f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2826b22ba4b1da6203697970962ead1b23df37e3ed80d4b9a539af238766611a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c5c9c8be9f22f24a688e2697f08a6e0ad3745cced17a935bfb16875a32f977)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaParametersMetricLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersMetricLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc90bb60ddeab3f41be02edc5c0a8fba3344d988006f8073e1141890b9ea8778)
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
    def internal_value(self) -> typing.Optional[ProcedureJavaParametersMetricLevel]:
        return typing.cast(typing.Optional[ProcedureJavaParametersMetricLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProcedureJavaParametersMetricLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cc1c293c225119d7a55b8b6593c9f6e4eb74c51acb9a5cbe7be3586a8778a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df13fcbd0c1634114ac96006dbc58a067d69b9c860f8c38f83f4981a569b3e2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(self) -> ProcedureJavaParametersEnableConsoleOutputList:
        return typing.cast(ProcedureJavaParametersEnableConsoleOutputList, jsii.get(self, "enableConsoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> ProcedureJavaParametersLogLevelList:
        return typing.cast(ProcedureJavaParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> ProcedureJavaParametersMetricLevelList:
        return typing.cast(ProcedureJavaParametersMetricLevelList, jsii.get(self, "metricLevel"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "ProcedureJavaParametersTraceLevelList":
        return typing.cast("ProcedureJavaParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProcedureJavaParameters]:
        return typing.cast(typing.Optional[ProcedureJavaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ProcedureJavaParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d7201b992cee7d0ce7d0c28380f5020f39a18c6c026340cb07ea48cfb89e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureJavaParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__592679b81d09e61e6851f6fb8de1194914368b31587ff11abf3bf3193e65d34c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProcedureJavaParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5262ef120b28ce1123b2caec94620bba45db0768e1ca3e4702cd2be483dc7fec)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5773d36b3affd2d328a6d4967a0f886f6f43b7a334df45cc80a6ebde4e65869f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff62a547d970fff212d577e6b831edbe0081e1b2ed56e532c9914bb910df352)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1bd56d75a63b08772c2b8fdba4dcf860ef971e34aed31435ffba10e6fa1769e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60d1c48d9460c8d5406786a558933e88f4504818e65134dac301e5d5248c6644)
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
    def internal_value(self) -> typing.Optional[ProcedureJavaParametersTraceLevel]:
        return typing.cast(typing.Optional[ProcedureJavaParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProcedureJavaParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd9d17daa2e46f4e1b70e756ce83dc61de09344dc9490436ad3bf6ea12b12d92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "secret_variable_name": "secretVariableName",
    },
)
class ProcedureJavaSecrets:
    def __init__(
        self,
        *,
        secret_id: builtins.str,
        secret_variable_name: builtins.str,
    ) -> None:
        '''
        :param secret_id: Fully qualified name of the allowed `secret <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_. You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the EXTERNAL_ACCESS_INTEGRATIONS parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#secret_id ProcedureJava#secret_id}
        :param secret_variable_name: The variable that will be used in handler code when retrieving information from the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#secret_variable_name ProcedureJava#secret_variable_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f34a118b1ee27e60546d9b143c507f6aac47315b01af1fe0cbf81451fce90d2)
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument secret_variable_name", value=secret_variable_name, expected_type=type_hints["secret_variable_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_id": secret_id,
            "secret_variable_name": secret_variable_name,
        }

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''Fully qualified name of the allowed `secret <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_. You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the EXTERNAL_ACCESS_INTEGRATIONS parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#secret_id ProcedureJava#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_variable_name(self) -> builtins.str:
        '''The variable that will be used in handler code when retrieving information from the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#secret_variable_name ProcedureJava#secret_variable_name}
        '''
        result = self._values.get("secret_variable_name")
        assert result is not None, "Required property 'secret_variable_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaSecretsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaSecretsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dc05359fe2490deb5a6d829d347dbde452ff8c1e2269de598f2688d96dcfa9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureJavaSecretsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0807189aaf5a553f9d6d4ec4881de3ee3823421f8ce692dc5e546efc35ce8d3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaSecretsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1785033bef1826a6c8867b2a21487ad697051235213cfe9cd0a6aa778f97175)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba9fb103612b89aff1cfbc078a4c1a4bb189078890dd69e0d3736362238ad6a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ec4b318e9b1ee2473b331939a54f54709ed2fbe0fd53756f47a1483651efb8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaSecrets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaSecrets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaSecrets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cc6f70b64dfe0b6f0df305c127a275700594d206f5824dd3816de10f30eb79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8524ce5d8944042655b3f27b4079ecee14812ec9788b31d44c902d13b4983a34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acbdb1d87112187479aecce7c6885add209e84207c4b212e7c0a52fdfdc5b5c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVariableName")
    def secret_variable_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVariableName"))

    @secret_variable_name.setter
    def secret_variable_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3634394a9433b4afc61a14a056a2981fe5164884b8c094cd2bbc009b2266dbc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVariableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaSecrets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaSecrets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaSecrets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c08dc69c5e005057cba3d64acd4468273b8102f251e0114af8641a669672aa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureJavaShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baa9c29d4c93dfc13a6a354be88b1bf6f8570485a5921994eb766179ebd0bd06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureJavaShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cefb32c6303b2b3c9258ec453dbbc0f5cdd7bfeced823b12cc7038eea55be4e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureJavaShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e49bdd1abdcbaf68dd3e7390dc87d81c254388673a41b903bdc1b162e33c89a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82bdb641708f1be45e01ad5c50de79645b102b920a69a58032ac065e336d647c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d78e94c9849a870142ac053f1126561bc623ca13f5568ba17f9cf4aecebfb9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureJavaShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98e1feb8852098cf9b1a4926a9fceeb0f07e7e617f39d152cd2bd5564f4e8df3)
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
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isSecure"))

    @builtins.property
    @jsii.member(jsii_name="isTableFunction")
    def is_table_function(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isTableFunction"))

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
    def internal_value(self) -> typing.Optional[ProcedureJavaShowOutput]:
        return typing.cast(typing.Optional[ProcedureJavaShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ProcedureJavaShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac407a431c9dc96fbd86fc697ef6bfe3b51ad38c2d67b946c3613e757c66d939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaTargetPath",
    jsii_struct_bases=[],
    name_mapping={"path_on_stage": "pathOnStage", "stage_location": "stageLocation"},
)
class ProcedureJavaTargetPath:
    def __init__(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#path_on_stage ProcedureJava#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#stage_location ProcedureJava#stage_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8d1bda1d724c5c511e3fc1feeebeb56163c8d8747a7da30240459cf924d1d3)
            check_type(argname="argument path_on_stage", value=path_on_stage, expected_type=type_hints["path_on_stage"])
            check_type(argname="argument stage_location", value=stage_location, expected_type=type_hints["stage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_on_stage": path_on_stage,
            "stage_location": stage_location,
        }

    @builtins.property
    def path_on_stage(self) -> builtins.str:
        '''Path for import on stage, without the leading ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#path_on_stage ProcedureJava#path_on_stage}
        '''
        result = self._values.get("path_on_stage")
        assert result is not None, "Required property 'path_on_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_location(self) -> builtins.str:
        '''Stage location without leading ``@``.

        To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_java#stage_location ProcedureJava#stage_location}
        '''
        result = self._values.get("stage_location")
        assert result is not None, "Required property 'stage_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureJavaTargetPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureJavaTargetPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureJava.ProcedureJavaTargetPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__711742dec4264ecf27658bc420caf6c4f96e93f6df1d1d6969cf906f8203749c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5d2aaff15a9d918a8ca53d10d22ecb5641e412de20d7e8b8b391f4850d2ac65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathOnStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stageLocation")
    def stage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stageLocation"))

    @stage_location.setter
    def stage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6298c2652930fe8c94b91a2ba324870dc60d6155a0438d2ac3dbfbaec7160c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProcedureJavaTargetPath]:
        return typing.cast(typing.Optional[ProcedureJavaTargetPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ProcedureJavaTargetPath]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0583e4adcd565b17f122a444d8f40e798322180ac41d227d8b0396dcf7c033a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ProcedureJava",
    "ProcedureJavaArguments",
    "ProcedureJavaArgumentsList",
    "ProcedureJavaArgumentsOutputReference",
    "ProcedureJavaConfig",
    "ProcedureJavaImports",
    "ProcedureJavaImportsList",
    "ProcedureJavaImportsOutputReference",
    "ProcedureJavaParameters",
    "ProcedureJavaParametersEnableConsoleOutput",
    "ProcedureJavaParametersEnableConsoleOutputList",
    "ProcedureJavaParametersEnableConsoleOutputOutputReference",
    "ProcedureJavaParametersList",
    "ProcedureJavaParametersLogLevel",
    "ProcedureJavaParametersLogLevelList",
    "ProcedureJavaParametersLogLevelOutputReference",
    "ProcedureJavaParametersMetricLevel",
    "ProcedureJavaParametersMetricLevelList",
    "ProcedureJavaParametersMetricLevelOutputReference",
    "ProcedureJavaParametersOutputReference",
    "ProcedureJavaParametersTraceLevel",
    "ProcedureJavaParametersTraceLevelList",
    "ProcedureJavaParametersTraceLevelOutputReference",
    "ProcedureJavaSecrets",
    "ProcedureJavaSecretsList",
    "ProcedureJavaSecretsOutputReference",
    "ProcedureJavaShowOutput",
    "ProcedureJavaShowOutputList",
    "ProcedureJavaShowOutputOutputReference",
    "ProcedureJavaTargetPath",
    "ProcedureJavaTargetPathOutputReference",
]

publication.publish()

def _typecheckingstub__163c416553ac38d2252f2d2caa055f421f952c20efa9c0e75bfb9e891dab116e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    database: builtins.str,
    handler: builtins.str,
    name: builtins.str,
    return_type: builtins.str,
    runtime_version: builtins.str,
    schema: builtins.str,
    snowpark_package: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    execute_as: typing.Optional[builtins.str] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaImports, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    procedure_definition: typing.Optional[builtins.str] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_path: typing.Optional[typing.Union[ProcedureJavaTargetPath, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3a65c81a4984a83ac300a14360e880a22dcce6c7a28e372dd5f90ebd6b07c880(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef09e63c0249c92cb4dce3055bd62f29bb5c1b54d314270e5cf85c82e73b3301(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7472653bc6c4ca1e777867180501f75fd2cb043eb2a5f1969bf0d24ff5df9e3e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaImports, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7914d4d014404313f1aeee3bc7064a997171bae7219d181a40ce42050357e3ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaSecrets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0507764ba4cc07353c20655673977838ef2ed5847722d1143d04785fbef6d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d3de65a60b3d41e394a6f4db5ace603a5eb6e2cd0a30fcb57d3eedd9fef600d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1402911cf183084b571900f07bbacc3a952dd5815a5c5c0204f6ae42be6db514(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d297db2bf88ca898b30d19e70c338883004b7bc44751f584627442c9be12a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f89a3125364220c2504d3d283e5db1a45c0d8775d81625bd14a5a2bb9e8a5d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965c803e75f31fe8fce908f70a73e3c80e1ce0564243589a41dbc1fbeec24da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4fafdbde9cc4939efd422cf672b42b868f9af59524f19297f4b5f3ceb63a2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86483a646dffa4f797eac547c7f7f200fc49cbd8a3c4212e243162630aee248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8651547304b4d242dc91624fc8f93ed118d4eb8c168bdf1d2af82b3d08ff5aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e81f8cf134ac282468c9de3901f35b59aa31ec153fc684dafe070a6e8f695b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dda2faba22342b8784987bb764b2bccc1c3cf055c07a8a004d40237daf57825(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e927d531d744157a0a157f3eec5c8b1f435e2b99f0ab8c6029b1c5134018760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701e07bb237e03bc6a2f3119851e0af0bffecc37244acf81c19b040ddc62f3b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8857d650400dfa5abb240863391b1186071fc4e3e4901e906f1157dfb09d72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db41ad7e1bf472a051128aaefaa55996c345769427b149e40108c3bb43854151(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3a4fe063dac70ca4d2b294623426a5946004030aeb3f9f67b99c2e0bf2276e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6094f67f368cb377b51ee5f9059a162a7fbdaba07022eb34797aaa09411510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101b9b611e5bbc55410a389db56577cdffd8ff0b2d340b124b6827dfb6bed03c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46624064a2a3668a0c30f5b633937de5b4ba33a94fd965bc2469ef29dfb2f60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f5d71391e883bd57d576ea657844126cc9c8f7fce2cd2edd229d8146f3fdef2(
    *,
    arg_data_type: builtins.str,
    arg_name: builtins.str,
    arg_default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb36f2c48fefe951d755189879eb45fd3f5efe054f88bd3f3f4388ac0645060(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefe0533ae61fe6583e977d1a7e9af2e34e181af8373ff22873cd86f39547f72(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2046dbf4f15f46b3ccf66d3239b4f7dcbf87c6183ac481205b93cb336a1928d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d2e6b270d1ca368d27b30ba5d949bd7e86644008017c229da9673273f817a7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4554e57e785b070c9caeb6f9a52150d620a43ebe4fa25df7890c52659bab56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23545003101cc174e3d953dc94228f7c9013a93828d811fda652210814fd6458(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e62c5bf47f997abe438b2605c11c1694608b8be5589ae67070c297d23ebee6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a24598132c7b878202f23b9a4c38b54fb9a6c990550f30404f6b02fd249c155(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d70f67d5a78d6c24af0c59989478629ca16387ba93e83f719ac03b791f2008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63bc9386703ed5131fa7f43dd39c08b5c15d5d2fae0b50d6397ebed30f440ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1344235d3ee6e7afd19dfda81fddb488cf48823dfa67b209532b01ccceaedd0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaArguments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77f50f1ba8493312d0b22bb18d92c3cc1c0dee633488253d27fe0d5e95f90de(
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
    snowpark_package: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    execute_as: typing.Optional[builtins.str] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaImports, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    procedure_definition: typing.Optional[builtins.str] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureJavaSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_path: typing.Optional[typing.Union[ProcedureJavaTargetPath, typing.Dict[builtins.str, typing.Any]]] = None,
    trace_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbad3cfd5678d71f454a0375333773a75bb1dcacf8dcf0c6ec059f8663c6b6ea(
    *,
    path_on_stage: builtins.str,
    stage_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b17ebc1fa55ddef36b81d43033fd2a3f0715aa9ec10b37befd24b22a0faa88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e52f5a593cccaec6a153e0196d1d12389d4536ff6632bdf30a63fffe1d6e48(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a6dffa703f2946388d3fee01399da8cf2f9b5dd4ab0034c71226d1b839a9e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86955848da16bad9e5ff4350e42b3ada21163c8bbe93ec3ccf3e32712676c48f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad620707626e949e2653c576f83fc781fe456ef0f4d12fe6bbcadd012c8e849b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7a6f90133fc17cb57ce056054bb3517d38acb45e9b0c44a8a35d48a424842a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaImports]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195313080867fac6830c0ecb9b92df042287c14bb1a8db7622b8309f85386f6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427075812237f9f9deaad9b72f67ce3fb53b113182df81546c6195592102c10c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462b3f696a23bb3d48025fad58946a92cc8b37bfb047248cba61523495094d1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd968545806d8d0d7fb1dd19c46a59a26ef820de703b1fa0f163395239ecd3b8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaImports]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2553711f6f1c676460784b2c40fc9d6977e0caf8d028a7d31ae238a03a7c90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07764bfc6276cf4a147f5c0cf166ec16b515315629eb6a639d0a146762d03af3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c203ab8159908d2e5d3dee59106c823f67c3de87e0d1082353e3fe545e8878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f1aeb3e3099acca8d8871313ca07cc0290f88ff994acfe8e162371232804fa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cb6c2529f685c718a638ae5da9a9c838660f81ed1190bddf7dfc196769ec11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faaec32d134d2073f85d4a8c3db1f2aa1d342c5bcbb87cf580488b68aac4445c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__144b95875b04a2c48c6b95471b93f5f1d273603540b15aad91b3ed5fd74ebe4c(
    value: typing.Optional[ProcedureJavaParametersEnableConsoleOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b1ec65660babd40b470ca0874a378389863971ea183a6b231adfbe51cb4730(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70edeb0c0843284436e32a3216cf896cedde3dedaef40ef1068f8747a7488b69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717a3cee6b6f8be8184a7c75014c092e30cc6ce4758bbe16ffeb84ddff035211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849ef7af80579957a0ab667ebcd662e4b1d7a5e62bc76ebebbcc119a3fe5c102(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d004c2349e44fc4a68df7cf9a38d148dcb036663a236ada71665564e52e36d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22132bc32583fc5cc515b883403e527e99fb2a40977e58309dcedecea272fe10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c90e8b0eced5d391219797e1cf4c5dfef62e660700209831020728f169d23ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296665af977127b0355bd6cd24f48aef46049dd8b11d1b2f434acd9cba483f67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a7547ef7b9fb67875c1268ec47fadf4776763dcdd8e7374ef2c28eced00f02(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfec7d2c39d1b93f0a16b154a350ee2c491d1b70b7d9662b1ccb5a84fdd3c38a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4412255e3aeeb5721acbd26a3a27fe57684bfd0e1a11c04757fa6f21d1599c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f0c6746a423ac333966769196fa82ca9a1ef30c73e063d4caa95309ed778ff(
    value: typing.Optional[ProcedureJavaParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc7deac6e40de39fff819bf36870e758953dc63c25db7a252acacaa229274ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71cbafab3c7de2cc74e0146ad71ccd5752f98e9dde38ecf93194b765b6b4e31d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445acca907738d96cf6a6caf4f6c41be3711a4250d52ff14df3e4e4924f0314f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2826b22ba4b1da6203697970962ead1b23df37e3ed80d4b9a539af238766611a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c5c9c8be9f22f24a688e2697f08a6e0ad3745cced17a935bfb16875a32f977(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc90bb60ddeab3f41be02edc5c0a8fba3344d988006f8073e1141890b9ea8778(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cc1c293c225119d7a55b8b6593c9f6e4eb74c51acb9a5cbe7be3586a8778a4(
    value: typing.Optional[ProcedureJavaParametersMetricLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df13fcbd0c1634114ac96006dbc58a067d69b9c860f8c38f83f4981a569b3e2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d7201b992cee7d0ce7d0c28380f5020f39a18c6c026340cb07ea48cfb89e68(
    value: typing.Optional[ProcedureJavaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592679b81d09e61e6851f6fb8de1194914368b31587ff11abf3bf3193e65d34c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5262ef120b28ce1123b2caec94620bba45db0768e1ca3e4702cd2be483dc7fec(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5773d36b3affd2d328a6d4967a0f886f6f43b7a334df45cc80a6ebde4e65869f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff62a547d970fff212d577e6b831edbe0081e1b2ed56e532c9914bb910df352(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bd56d75a63b08772c2b8fdba4dcf860ef971e34aed31435ffba10e6fa1769e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d1c48d9460c8d5406786a558933e88f4504818e65134dac301e5d5248c6644(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd9d17daa2e46f4e1b70e756ce83dc61de09344dc9490436ad3bf6ea12b12d92(
    value: typing.Optional[ProcedureJavaParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f34a118b1ee27e60546d9b143c507f6aac47315b01af1fe0cbf81451fce90d2(
    *,
    secret_id: builtins.str,
    secret_variable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc05359fe2490deb5a6d829d347dbde452ff8c1e2269de598f2688d96dcfa9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0807189aaf5a553f9d6d4ec4881de3ee3823421f8ce692dc5e546efc35ce8d3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1785033bef1826a6c8867b2a21487ad697051235213cfe9cd0a6aa778f97175(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9fb103612b89aff1cfbc078a4c1a4bb189078890dd69e0d3736362238ad6a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec4b318e9b1ee2473b331939a54f54709ed2fbe0fd53756f47a1483651efb8f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cc6f70b64dfe0b6f0df305c127a275700594d206f5824dd3816de10f30eb79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureJavaSecrets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8524ce5d8944042655b3f27b4079ecee14812ec9788b31d44c902d13b4983a34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acbdb1d87112187479aecce7c6885add209e84207c4b212e7c0a52fdfdc5b5c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3634394a9433b4afc61a14a056a2981fe5164884b8c094cd2bbc009b2266dbc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c08dc69c5e005057cba3d64acd4468273b8102f251e0114af8641a669672aa5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureJavaSecrets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa9c29d4c93dfc13a6a354be88b1bf6f8570485a5921994eb766179ebd0bd06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cefb32c6303b2b3c9258ec453dbbc0f5cdd7bfeced823b12cc7038eea55be4e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e49bdd1abdcbaf68dd3e7390dc87d81c254388673a41b903bdc1b162e33c89a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bdb641708f1be45e01ad5c50de79645b102b920a69a58032ac065e336d647c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d78e94c9849a870142ac053f1126561bc623ca13f5568ba17f9cf4aecebfb9c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e1feb8852098cf9b1a4926a9fceeb0f07e7e617f39d152cd2bd5564f4e8df3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac407a431c9dc96fbd86fc697ef6bfe3b51ad38c2d67b946c3613e757c66d939(
    value: typing.Optional[ProcedureJavaShowOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8d1bda1d724c5c511e3fc1feeebeb56163c8d8747a7da30240459cf924d1d3(
    *,
    path_on_stage: builtins.str,
    stage_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711742dec4264ecf27658bc420caf6c4f96e93f6df1d1d6969cf906f8203749c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5d2aaff15a9d918a8ca53d10d22ecb5641e412de20d7e8b8b391f4850d2ac65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6298c2652930fe8c94b91a2ba324870dc60d6155a0438d2ac3dbfbaec7160c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0583e4adcd565b17f122a444d8f40e798322180ac41d227d8b0396dcf7c033a4(
    value: typing.Optional[ProcedureJavaTargetPath],
) -> None:
    """Type checking stubs"""
    pass

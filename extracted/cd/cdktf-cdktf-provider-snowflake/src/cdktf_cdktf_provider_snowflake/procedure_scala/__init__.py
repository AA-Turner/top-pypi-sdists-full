r'''
# `snowflake_procedure_scala`

Refer to the Terraform Registry for docs: [`snowflake_procedure_scala`](https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala).
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


class ProcedureScala(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScala",
):
    '''Represents a {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala snowflake_procedure_scala}.'''

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
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureScalaArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        execute_as: typing.Optional[builtins.str] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureScalaImports", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        procedure_definition: typing.Optional[builtins.str] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureScalaSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_path: typing.Optional[typing.Union["ProcedureScalaTargetPath", typing.Dict[builtins.str, typing.Any]]] = None,
        trace_level: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala snowflake_procedure_scala} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param database: The database in which to create the procedure. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#database ProcedureScala#database}
        :param handler: Use the fully qualified name of the method or function for the stored procedure. This is typically in the following form: ``com.my_company.my_package.MyClass.myMethod`` where ``com.my_company.my_package`` corresponds to the package containing the object or class: ``package com.my_company.my_package;``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#handler ProcedureScala#handler}
        :param name: The name of the procedure; the identifier does not need to be unique for the schema in which the procedure is created because stored procedures are `identified and resolved by the combination of the name and argument types <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-naming-conventions.html#label-procedure-function-name-overloading>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#name ProcedureScala#name}
        :param return_type: Specifies the type of the result returned by the stored procedure. For ``<result_data_type>``, use the Snowflake data type that corresponds to the type of the language that you are using (see `SQL-Scala Data Type Mappings <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-data-type-mapping.html#label-sql-types-to-scala-types>`_). For ``RETURNS TABLE ( [ col_name col_data_type [ , ... ] ] )``, if you know the Snowflake data types of the columns in the returned table, specify the column names and types. Otherwise (e.g. if you are determining the column types during run time), you can omit the column names and types (i.e. ``TABLE ()``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#return_type ProcedureScala#return_type}
        :param runtime_version: The language runtime version to use. Currently, the supported versions are: 2.12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#runtime_version ProcedureScala#runtime_version}
        :param schema: The schema in which to create the procedure. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#schema ProcedureScala#schema}
        :param snowpark_package: The Snowpark package is required for stored procedures, so it must always be present. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#snowpark_package ProcedureScala#snowpark_package}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arguments ProcedureScala#arguments}
        :param comment: Specifies a comment for the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#comment ProcedureScala#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#enable_console_output ProcedureScala#enable_console_output}
        :param execute_as: Specifies whether the stored procedure executes with the privileges of the owner (an “owner’s rights” stored procedure) or with the privileges of the caller (a “caller’s rights” stored procedure). If you execute the statement CREATE PROCEDURE … EXECUTE AS CALLER, then in the future the procedure will execute as a caller’s rights procedure. If you execute CREATE PROCEDURE … EXECUTE AS OWNER, then the procedure will execute as an owner’s rights procedure. For more information, see `Understanding caller’s rights and owner’s rights stored procedures <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_. Valid values are (case-insensitive): ``CALLER`` | ``OWNER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#execute_as ProcedureScala#execute_as}
        :param external_access_integrations: The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this procedure’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#external_access_integrations ProcedureScala#external_access_integrations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#id ProcedureScala#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: imports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#imports ProcedureScala#imports}
        :param is_secure: Specifies that the procedure is secure. For more information about secure procedures, see `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#is_secure ProcedureScala#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#log_level ProcedureScala#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#metric_level ProcedureScala#metric_level}
        :param null_input_behavior: Specifies the behavior of the procedure when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#null_input_behavior ProcedureScala#null_input_behavior}
        :param packages: List of the names of packages deployed in Snowflake that should be included in the handler code’s execution environment. The Snowpark package is required for stored procedures, but is specified in the ``snowpark_package`` attribute. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#packages ProcedureScala#packages}
        :param procedure_definition: Defines the code executed by the stored procedure. The definition can consist of any valid code. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``procedure_definition`` value must be Scala source code. For more information, see `Scala (using Snowpark) <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-scala>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#procedure_definition ProcedureScala#procedure_definition}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#secrets ProcedureScala#secrets}
        :param target_path: target_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#target_path ProcedureScala#target_path}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#trace_level ProcedureScala#trace_level}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2874513c85c83a000af1cbf3589a2c09f8379d1996ea64e5cebe2d287e8e6f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProcedureScalaConfig(
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
        '''Generates CDKTF code for importing a ProcedureScala resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ProcedureScala to import.
        :param import_from_id: The id of the existing ProcedureScala that should be imported. Refer to the {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ProcedureScala to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79f96b68302b64fb78c0238e16532f843b1b520f4c3d527f1bd5803f8671984)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureScalaArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58934cfefe2c7ef58ecb6e29c6cbc831561af0faee08519fa78646ff4c8536bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArguments", [value]))

    @jsii.member(jsii_name="putImports")
    def put_imports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureScalaImports", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b65386e34dc7636492dc53c7149e757d230ae90cad09a523d65172bc920328b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putImports", [value]))

    @jsii.member(jsii_name="putSecrets")
    def put_secrets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureScalaSecrets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e780cb3e2b0599a507d31e96b1cc7d86d03d07dfd6db3c0af7f9a477231a306)
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
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#path_on_stage ProcedureScala#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#stage_location ProcedureScala#stage_location}
        '''
        value = ProcedureScalaTargetPath(
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
    def arguments(self) -> "ProcedureScalaArgumentsList":
        return typing.cast("ProcedureScalaArgumentsList", jsii.get(self, "arguments"))

    @builtins.property
    @jsii.member(jsii_name="fullyQualifiedName")
    def fully_qualified_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullyQualifiedName"))

    @builtins.property
    @jsii.member(jsii_name="imports")
    def imports(self) -> "ProcedureScalaImportsList":
        return typing.cast("ProcedureScalaImportsList", jsii.get(self, "imports"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "ProcedureScalaParametersList":
        return typing.cast("ProcedureScalaParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="procedureLanguage")
    def procedure_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "procedureLanguage"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> "ProcedureScalaSecretsList":
        return typing.cast("ProcedureScalaSecretsList", jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="showOutput")
    def show_output(self) -> "ProcedureScalaShowOutputList":
        return typing.cast("ProcedureScalaShowOutputList", jsii.get(self, "showOutput"))

    @builtins.property
    @jsii.member(jsii_name="targetPath")
    def target_path(self) -> "ProcedureScalaTargetPathOutputReference":
        return typing.cast("ProcedureScalaTargetPathOutputReference", jsii.get(self, "targetPath"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaArguments"]]], jsii.get(self, "argumentsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaImports"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaImports"]]], jsii.get(self, "importsInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaSecrets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaSecrets"]]], jsii.get(self, "secretsInput"))

    @builtins.property
    @jsii.member(jsii_name="snowparkPackageInput")
    def snowpark_package_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snowparkPackageInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPathInput")
    def target_path_input(self) -> typing.Optional["ProcedureScalaTargetPath"]:
        return typing.cast(typing.Optional["ProcedureScalaTargetPath"], jsii.get(self, "targetPathInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__f4f1ecd2cfd7c86020eae2b589501db506c71df5007700761199061b4649b651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0a9b33c0d4cb5e3f3a4f7c54be4ce595a54f1bd8ccb865afb9f0674ef5058d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7182cc2032d39061dc12104ce08341e03ac56627449cca4142785e2d7576fefb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsoleOutput", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executeAs")
    def execute_as(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executeAs"))

    @execute_as.setter
    def execute_as(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ac76fc02b9ed1e35207276e981df4d2a287d3d7314ddfd1a216bfae6bcf5c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executeAs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalAccessIntegrations")
    def external_access_integrations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalAccessIntegrations"))

    @external_access_integrations.setter
    def external_access_integrations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1037be18aedd329adc1fbae891e38d11f3512adb0f5847bc3d782e7caf8060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalAccessIntegrations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "handler"))

    @handler.setter
    def handler(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee8672767f8dc53d7630d2e522d478df17283eaed1279cf101a28371c53f1ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "handler", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d1bdbdbf8fab46e7b195430b5f1e54c2dfe7ebc60e44e718dc602d354765363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isSecure")
    def is_secure(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "isSecure"))

    @is_secure.setter
    def is_secure(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c731f39385bf9f112918419d456bad32ddd5ed592fd2fb0b497c84d4a8349f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12ffc256869afa11d5da2610a4a779acec62cd9e8001604f0e83e2b45f8a30c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricLevel"))

    @metric_level.setter
    def metric_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2915c9b1a3424ff20032b4ce8b11f81956956adc5771fa111fb1dda658dfd204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c2ef57d561113aeca44623d8cccdc135350c425bf2ce5087dba7bb6f0bc60d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nullInputBehavior")
    def null_input_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nullInputBehavior"))

    @null_input_behavior.setter
    def null_input_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff68ae42ad11d16573ea4458ee8ad811271916e9b6750baa87c8cdef8247912e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nullInputBehavior", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="packages")
    def packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "packages"))

    @packages.setter
    def packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203851754a3d67f08a96c157d3d291cb0931eeaa5d08d10de9519572f2ee6262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="procedureDefinition")
    def procedure_definition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "procedureDefinition"))

    @procedure_definition.setter
    def procedure_definition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd08eba56de35f3eac5945d65fee7e1ac273dccef51fdbc8357b075aa97f524d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "procedureDefinition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b5263abf90ac5203ecf653f54d4f31cbe3496f7e96de90af65effebe96e719)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601fe0d7db992f955b4c55ba0e0644c8b773d66bc4ffec2574313e6ab355acd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23f16334127d6bc9ed5796c8d72e4a30ed632dbf14ad1f2cb8869ca70165283e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snowparkPackage")
    def snowpark_package(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snowparkPackage"))

    @snowpark_package.setter
    def snowpark_package(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69963194ed4541d23df71073b8dd5b165dabfda645a716fca20707ef1d6cb55f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snowparkPackage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "traceLevel"))

    @trace_level.setter
    def trace_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27432b425de9cda20c4417df529c189399479f84e763255a87981217e433bce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "traceLevel", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaArguments",
    jsii_struct_bases=[],
    name_mapping={
        "arg_data_type": "argDataType",
        "arg_name": "argName",
        "arg_default_value": "argDefaultValue",
    },
)
class ProcedureScalaArguments:
    def __init__(
        self,
        *,
        arg_data_type: builtins.str,
        arg_name: builtins.str,
        arg_default_value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arg_data_type: The argument type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arg_data_type ProcedureScala#arg_data_type}
        :param arg_name: The argument name. The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the procedure definition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arg_name ProcedureScala#arg_name}
        :param arg_default_value: Optional default value for the argument. For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arg_default_value ProcedureScala#arg_default_value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eacb3101556438dcc95da2ffd836daca499154437fe131d8ccb72afcdbf90f7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arg_data_type ProcedureScala#arg_data_type}
        '''
        result = self._values.get("arg_data_type")
        assert result is not None, "Required property 'arg_data_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_name(self) -> builtins.str:
        '''The argument name.

        The provider wraps it in double quotes by default, so be aware of that while referencing the argument in the procedure definition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arg_name ProcedureScala#arg_name}
        '''
        result = self._values.get("arg_name")
        assert result is not None, "Required property 'arg_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arg_default_value(self) -> typing.Optional[builtins.str]:
        '''Optional default value for the argument.

        For text values use single quotes. Numeric values can be unquoted. External changes for this field won't be detected. In case you want to apply external changes, you can re-create the resource manually using "terraform taint".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arg_default_value ProcedureScala#arg_default_value}
        '''
        result = self._values.get("arg_default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaArgumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b2c7805807f71b4d30d8315f9217ff5387816c38df68c7c404c7d02657c9905)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureScalaArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__306906a95be0200c2add87a12fc28d27391aeb067f9fe52575fa92f7e414016b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523e898d4a905175e3cbd7ae6ff7bcde8c80450fdc0d6be171e421904dcadfba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a79f0d9a07e68c78af6b244ce7488b760ff8de49ccb857078c5abfad0b4b41ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54c51fa4f673934b0c12210cb0c2155935f52b3a30deeb072c4dbeb287614ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23bf9c4ba700fe640d5fb153531756fbc3cd43966a05cc50b72615997d7817f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaArgumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1afe57b9b91969cedb84bb6a54b3c397047c3698d6e38af4b72a28385ce9a9d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__154c41ac47bd092ea358deaa08d59566c2ce1615c2635a951b7f91ed4ad52018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argDefaultValue")
    def arg_default_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argDefaultValue"))

    @arg_default_value.setter
    def arg_default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7131e21b92fceba74a6976b708e99723a97023d00b305c17a8f1711391bd22d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argDefaultValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="argName")
    def arg_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argName"))

    @arg_name.setter
    def arg_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de08e398c7b7df08dfd11c49d953042b9989e8865dffaaa599b90ce69c9069e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaArguments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaArguments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaArguments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a845209dc95ba588fb0e14605ee884983fe275716c6c63c6d3225f021ef215d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaConfig",
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
class ProcedureScalaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        comment: typing.Optional[builtins.str] = None,
        enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        execute_as: typing.Optional[builtins.str] = None,
        external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureScalaImports", typing.Dict[builtins.str, typing.Any]]]]] = None,
        is_secure: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        metric_level: typing.Optional[builtins.str] = None,
        null_input_behavior: typing.Optional[builtins.str] = None,
        packages: typing.Optional[typing.Sequence[builtins.str]] = None,
        procedure_definition: typing.Optional[builtins.str] = None,
        secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProcedureScalaSecrets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        target_path: typing.Optional[typing.Union["ProcedureScalaTargetPath", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param database: The database in which to create the procedure. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#database ProcedureScala#database}
        :param handler: Use the fully qualified name of the method or function for the stored procedure. This is typically in the following form: ``com.my_company.my_package.MyClass.myMethod`` where ``com.my_company.my_package`` corresponds to the package containing the object or class: ``package com.my_company.my_package;``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#handler ProcedureScala#handler}
        :param name: The name of the procedure; the identifier does not need to be unique for the schema in which the procedure is created because stored procedures are `identified and resolved by the combination of the name and argument types <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-naming-conventions.html#label-procedure-function-name-overloading>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#name ProcedureScala#name}
        :param return_type: Specifies the type of the result returned by the stored procedure. For ``<result_data_type>``, use the Snowflake data type that corresponds to the type of the language that you are using (see `SQL-Scala Data Type Mappings <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-data-type-mapping.html#label-sql-types-to-scala-types>`_). For ``RETURNS TABLE ( [ col_name col_data_type [ , ... ] ] )``, if you know the Snowflake data types of the columns in the returned table, specify the column names and types. Otherwise (e.g. if you are determining the column types during run time), you can omit the column names and types (i.e. ``TABLE ()``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#return_type ProcedureScala#return_type}
        :param runtime_version: The language runtime version to use. Currently, the supported versions are: 2.12. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#runtime_version ProcedureScala#runtime_version}
        :param schema: The schema in which to create the procedure. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#schema ProcedureScala#schema}
        :param snowpark_package: The Snowpark package is required for stored procedures, so it must always be present. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#snowpark_package ProcedureScala#snowpark_package}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arguments ProcedureScala#arguments}
        :param comment: Specifies a comment for the procedure. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#comment ProcedureScala#comment}
        :param enable_console_output: Enable stdout/stderr fast path logging for anonyous stored procs. This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#enable_console_output ProcedureScala#enable_console_output}
        :param execute_as: Specifies whether the stored procedure executes with the privileges of the owner (an “owner’s rights” stored procedure) or with the privileges of the caller (a “caller’s rights” stored procedure). If you execute the statement CREATE PROCEDURE … EXECUTE AS CALLER, then in the future the procedure will execute as a caller’s rights procedure. If you execute CREATE PROCEDURE … EXECUTE AS OWNER, then the procedure will execute as an owner’s rights procedure. For more information, see `Understanding caller’s rights and owner’s rights stored procedures <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_. Valid values are (case-insensitive): ``CALLER`` | ``OWNER``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#execute_as ProcedureScala#execute_as}
        :param external_access_integrations: The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this procedure’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#external_access_integrations ProcedureScala#external_access_integrations}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#id ProcedureScala#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imports: imports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#imports ProcedureScala#imports}
        :param is_secure: Specifies that the procedure is secure. For more information about secure procedures, see `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#is_secure ProcedureScala#is_secure}
        :param log_level: LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#log_level ProcedureScala#log_level}
        :param metric_level: METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#metric_level ProcedureScala#metric_level}
        :param null_input_behavior: Specifies the behavior of the procedure when called with null inputs. Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#null_input_behavior ProcedureScala#null_input_behavior}
        :param packages: List of the names of packages deployed in Snowflake that should be included in the handler code’s execution environment. The Snowpark package is required for stored procedures, but is specified in the ``snowpark_package`` attribute. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#packages ProcedureScala#packages}
        :param procedure_definition: Defines the code executed by the stored procedure. The definition can consist of any valid code. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``procedure_definition`` value must be Scala source code. For more information, see `Scala (using Snowpark) <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-scala>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#procedure_definition ProcedureScala#procedure_definition}
        :param secrets: secrets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#secrets ProcedureScala#secrets}
        :param target_path: target_path block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#target_path ProcedureScala#target_path}
        :param trace_level: Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#trace_level ProcedureScala#trace_level}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(target_path, dict):
            target_path = ProcedureScalaTargetPath(**target_path)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c3f9ab79eb1ed3d030f24db1feadef58b1c115d34ee45c842b000203fb37ea)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#database ProcedureScala#database}
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''Use the fully qualified name of the method or function for the stored procedure.

        This is typically in the following form: ``com.my_company.my_package.MyClass.myMethod`` where ``com.my_company.my_package`` corresponds to the package containing the object or class: ``package com.my_company.my_package;``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#handler ProcedureScala#handler}
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the procedure;

        the identifier does not need to be unique for the schema in which the procedure is created because stored procedures are `identified and resolved by the combination of the name and argument types <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-naming-conventions.html#label-procedure-function-name-overloading>`_. Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#name ProcedureScala#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def return_type(self) -> builtins.str:
        '''Specifies the type of the result returned by the stored procedure.

        For ``<result_data_type>``, use the Snowflake data type that corresponds to the type of the language that you are using (see `SQL-Scala Data Type Mappings <https://docs.snowflake.com/en/developer-guide/udf-stored-procedure-data-type-mapping.html#label-sql-types-to-scala-types>`_). For ``RETURNS TABLE ( [ col_name col_data_type [ , ... ] ] )``, if you know the Snowflake data types of the columns in the returned table, specify the column names and types. Otherwise (e.g. if you are determining the column types during run time), you can omit the column names and types (i.e. ``TABLE ()``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#return_type ProcedureScala#return_type}
        '''
        result = self._values.get("return_type")
        assert result is not None, "Required property 'return_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''The language runtime version to use. Currently, the supported versions are: 2.12.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#runtime_version ProcedureScala#runtime_version}
        '''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schema(self) -> builtins.str:
        '''The schema in which to create the procedure.

        Due to technical limitations (read more `here <../guides/identifiers_rework_design_decisions#known-limitations-and-identifier-recommendations>`_), avoid using the following characters: ``|``, ``.``, ``"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#schema ProcedureScala#schema}
        '''
        result = self._values.get("schema")
        assert result is not None, "Required property 'schema' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snowpark_package(self) -> builtins.str:
        '''The Snowpark package is required for stored procedures, so it must always be present.

        For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#snowpark_package ProcedureScala#snowpark_package}
        '''
        result = self._values.get("snowpark_package")
        assert result is not None, "Required property 'snowpark_package' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#arguments ProcedureScala#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaArguments]]], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Specifies a comment for the procedure.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#comment ProcedureScala#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_console_output(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable stdout/stderr fast path logging for anonyous stored procs.

        This is a public parameter (similar to LOG_LEVEL). For more information, check `ENABLE_CONSOLE_OUTPUT docs <https://docs.snowflake.com/en/sql-reference/parameters#enable-console-output>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#enable_console_output ProcedureScala#enable_console_output}
        '''
        result = self._values.get("enable_console_output")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def execute_as(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the stored procedure executes with the privileges of the owner (an “owner’s rights” stored procedure) or with the privileges of the caller (a “caller’s rights” stored procedure).

        If you execute the statement CREATE PROCEDURE … EXECUTE AS CALLER, then in the future the procedure will execute as a caller’s rights procedure. If you execute CREATE PROCEDURE … EXECUTE AS OWNER, then the procedure will execute as an owner’s rights procedure. For more information, see `Understanding caller’s rights and owner’s rights stored procedures <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-rights>`_. Valid values are (case-insensitive): ``CALLER`` | ``OWNER``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#execute_as ProcedureScala#execute_as}
        '''
        result = self._values.get("execute_as")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_access_integrations(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The names of `external access integrations <https://docs.snowflake.com/en/sql-reference/sql/create-external-access-integration>`_ needed in order for this procedure’s handler code to access external networks. An external access integration specifies `network rules <https://docs.snowflake.com/en/sql-reference/sql/create-network-rule>`_ and `secrets <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_ that specify external locations and credentials (if any) allowed for use by handler code when making requests of an external network, such as an external REST API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#external_access_integrations ProcedureScala#external_access_integrations}
        '''
        result = self._values.get("external_access_integrations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#id ProcedureScala#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaImports"]]]:
        '''imports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#imports ProcedureScala#imports}
        '''
        result = self._values.get("imports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaImports"]]], result)

    @builtins.property
    def is_secure(self) -> typing.Optional[builtins.str]:
        '''Specifies that the procedure is secure.

        For more information about secure procedures, see `Protecting Sensitive Information with Secure UDFs and Stored Procedures <https://docs.snowflake.com/en/developer-guide/secure-udf-procedure>`_. Available options are: "true" or "false". When the value is not set in the configuration the provider will put "default" there which means to use the Snowflake default for this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#is_secure ProcedureScala#is_secure}
        '''
        result = self._values.get("is_secure")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''LOG_LEVEL to use when filtering events For more information, check `LOG_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#log-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#log_level ProcedureScala#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_level(self) -> typing.Optional[builtins.str]:
        '''METRIC_LEVEL value to control whether to emit metrics to Event Table For more information, check `METRIC_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#metric-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#metric_level ProcedureScala#metric_level}
        '''
        result = self._values.get("metric_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def null_input_behavior(self) -> typing.Optional[builtins.str]:
        '''Specifies the behavior of the procedure when called with null inputs.

        Valid values are (case-insensitive): ``CALLED ON NULL INPUT`` | ``RETURNS NULL ON NULL INPUT``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#null_input_behavior ProcedureScala#null_input_behavior}
        '''
        result = self._values.get("null_input_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of the names of packages deployed in Snowflake that should be included in the handler code’s execution environment.

        The Snowpark package is required for stored procedures, but is specified in the ``snowpark_package`` attribute. For more information about Snowpark, see `Snowpark API <https://docs.snowflake.com/en/developer-guide/snowpark/index>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#packages ProcedureScala#packages}
        '''
        result = self._values.get("packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def procedure_definition(self) -> typing.Optional[builtins.str]:
        '''Defines the code executed by the stored procedure.

        The definition can consist of any valid code. Wrapping ``$$`` signs are added by the provider automatically; do not include them. The ``procedure_definition`` value must be Scala source code. For more information, see `Scala (using Snowpark) <https://docs.snowflake.com/en/developer-guide/stored-procedure/stored-procedures-scala>`_. To mitigate permadiff on this field, the provider replaces blank characters with a space. This can lead to false positives in cases where a change in case or run of whitespace is semantically significant.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#procedure_definition ProcedureScala#procedure_definition}
        '''
        result = self._values.get("procedure_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secrets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaSecrets"]]]:
        '''secrets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#secrets ProcedureScala#secrets}
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProcedureScalaSecrets"]]], result)

    @builtins.property
    def target_path(self) -> typing.Optional["ProcedureScalaTargetPath"]:
        '''target_path block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#target_path ProcedureScala#target_path}
        '''
        result = self._values.get("target_path")
        return typing.cast(typing.Optional["ProcedureScalaTargetPath"], result)

    @builtins.property
    def trace_level(self) -> typing.Optional[builtins.str]:
        '''Trace level value to use when generating/filtering trace events For more information, check `TRACE_LEVEL docs <https://docs.snowflake.com/en/sql-reference/parameters#trace-level>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#trace_level ProcedureScala#trace_level}
        '''
        result = self._values.get("trace_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaImports",
    jsii_struct_bases=[],
    name_mapping={"path_on_stage": "pathOnStage", "stage_location": "stageLocation"},
)
class ProcedureScalaImports:
    def __init__(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#path_on_stage ProcedureScala#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#stage_location ProcedureScala#stage_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8084dd599aacff97f0682c86f4d87fcaaaf537c276996381aeed2283889fa1)
            check_type(argname="argument path_on_stage", value=path_on_stage, expected_type=type_hints["path_on_stage"])
            check_type(argname="argument stage_location", value=stage_location, expected_type=type_hints["stage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_on_stage": path_on_stage,
            "stage_location": stage_location,
        }

    @builtins.property
    def path_on_stage(self) -> builtins.str:
        '''Path for import on stage, without the leading ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#path_on_stage ProcedureScala#path_on_stage}
        '''
        result = self._values.get("path_on_stage")
        assert result is not None, "Required property 'path_on_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_location(self) -> builtins.str:
        '''Stage location without leading ``@``.

        To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#stage_location ProcedureScala#stage_location}
        '''
        result = self._values.get("stage_location")
        assert result is not None, "Required property 'stage_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaImports(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaImportsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaImportsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57a797a083de4c8f33fc69a2eb2a3fd1ad928b6acc6626e0a4f97a3418ab1601)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureScalaImportsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0728331e3b96fb079bb48e4d25d2390d4244221dab48e684d4394a14ad5441d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaImportsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1dc78e016ae4b7462d3816eab03143fbcdca0e53bcff9ceef863235ffe6765b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0872d8e6921bfd391e10b8b2cc924e67d0f10c15af4db58477e139dba19401ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c85257790fcea95ee0bfee037143c483f873c2a4afbfe3f5a28905ea422991b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaImports]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaImports]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaImports]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea6e9cc34e6c8869583df7d05a273572e781b884ddd0df10726bdef91d6ecb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaImportsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaImportsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__455fd50555e156a66b703761f21d21b2a6705f582e0f6f6ae158a8eaf77d99d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2260f8234ab762f813f67a344ccd70f75bf87cb6b87560331a537278af5abaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathOnStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stageLocation")
    def stage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stageLocation"))

    @stage_location.setter
    def stage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6851ea3f19f5cc36fbf71f52cd1d07b3beac8f43965375bdfac54e1ae7c278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaImports]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaImports]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaImports]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e39de1d4b2c4330aac2955b46e04aa7208a4a5514158156d587afb8380e72b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParameters",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureScalaParameters:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersEnableConsoleOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureScalaParametersEnableConsoleOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaParametersEnableConsoleOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaParametersEnableConsoleOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersEnableConsoleOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a27a914170d120ded875328de2c7dbd3b0c2a21d007adf2929af1dedc64f53e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProcedureScalaParametersEnableConsoleOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de154b0648a9cfb95158adca6ee15cb5129799e578eeedbe051eef0e790bc81c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaParametersEnableConsoleOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbffc80a8512217a394e5a8138151d81c89e18daa003024c8e34e509585044b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15af5c62dca56821c1d13554e5082ab52a0d2a1a86df4d0290aa8c78e68db801)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03b8c23d6f26e7a741381cc5e8fdf40041a810824af233956952295ffe479822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaParametersEnableConsoleOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersEnableConsoleOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9157ae877af943cbe647b5e93b68a31f18880e2a6fa9b98abfbd977959a2bcfc)
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
    ) -> typing.Optional[ProcedureScalaParametersEnableConsoleOutput]:
        return typing.cast(typing.Optional[ProcedureScalaParametersEnableConsoleOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProcedureScalaParametersEnableConsoleOutput],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61ee7d291d8c1bddfd76855a5816745a17444490d1f5ee1713c57abc649bbdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75119dd85f0eb0cf85eb151ded82e914c4941fb0def9a339f909f8f976bac3f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureScalaParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d708b551082b56364af0d99abff572c8eb0e1a4b930db827e0bf476613eee7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b85a95984e59960ddee0b239f50cd781fbf603330061c740b7eaa1b206691e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce04610e28c38a160fefe2f2939c14ce7457563609e099814d4511c65d1c8bbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13bb3b9ca908a4680f19f0e408121813c15efccd403adb53963bd825b4ad0480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersLogLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureScalaParametersLogLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaParametersLogLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaParametersLogLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersLogLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31becdb58c58101a928429a9778ce0720b7199e4e76cb1d9a7f7c718450e370b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProcedureScalaParametersLogLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ea1e027a360f30f7cd40e559249dc1891a388e93ac309d3c90e53ef0f2aef9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaParametersLogLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f136eb7200654226ff29993e1f093afdf7b74a56cd026db7def85dabaa28ad1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b97c2d158cf8141e34509cad5b08f1b2cd125b189f9adca7749734b4f503ec0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f6da3f5f4262abe20ebbc4d83b9d1295d4f9bc805d062cd7b2a4bb6a59dd2fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaParametersLogLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersLogLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6055f6321434bc12c4680a6c1ad791dae22e3ff06e5e1453531ad38034304081)
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
    def internal_value(self) -> typing.Optional[ProcedureScalaParametersLogLevel]:
        return typing.cast(typing.Optional[ProcedureScalaParametersLogLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProcedureScalaParametersLogLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828c3886b7c8c1ea4a5a5beb3d6f50debbdd480b36a99177613654b2c84da49a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersMetricLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureScalaParametersMetricLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaParametersMetricLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaParametersMetricLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersMetricLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0abc53c702df2c31cc7d51b3ce6ab448023b50cb5b009a8c125172f3592493f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProcedureScalaParametersMetricLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c6d99411940952d203de5d84f8c1fbca2a0b37ae81c08887f3529c50a33f97c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaParametersMetricLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1001d3e75fc50e9d2dd02af9d05fa4024fb93f95976e9ba4030ac78db9be1c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05345601843fdc9f71efaedec6020405ee7413182fc63e06489752825be9ff50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5bd0ea874de58c0c7eb18a9679e0f825775744d290748cdc4462c5b753390fb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaParametersMetricLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersMetricLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__852473272afae0eee365a57398d485c087ec1fab8a5a5b474d262cd9a39399cb)
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
    def internal_value(self) -> typing.Optional[ProcedureScalaParametersMetricLevel]:
        return typing.cast(typing.Optional[ProcedureScalaParametersMetricLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProcedureScalaParametersMetricLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37329a24487df6c5059763286b3f0c39efc7cb2f8f3f47f5235a850c98983bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__541f1e5591863f36a041698d7c49dcad88d7b4ba0f51ad13c77c66108420a81d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enableConsoleOutput")
    def enable_console_output(self) -> ProcedureScalaParametersEnableConsoleOutputList:
        return typing.cast(ProcedureScalaParametersEnableConsoleOutputList, jsii.get(self, "enableConsoleOutput"))

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> ProcedureScalaParametersLogLevelList:
        return typing.cast(ProcedureScalaParametersLogLevelList, jsii.get(self, "logLevel"))

    @builtins.property
    @jsii.member(jsii_name="metricLevel")
    def metric_level(self) -> ProcedureScalaParametersMetricLevelList:
        return typing.cast(ProcedureScalaParametersMetricLevelList, jsii.get(self, "metricLevel"))

    @builtins.property
    @jsii.member(jsii_name="traceLevel")
    def trace_level(self) -> "ProcedureScalaParametersTraceLevelList":
        return typing.cast("ProcedureScalaParametersTraceLevelList", jsii.get(self, "traceLevel"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProcedureScalaParameters]:
        return typing.cast(typing.Optional[ProcedureScalaParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ProcedureScalaParameters]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799f9592007542de06d8e4b49e73eb86377eeebe17f2baffbca5ce0ac1812c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersTraceLevel",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureScalaParametersTraceLevel:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaParametersTraceLevel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaParametersTraceLevelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersTraceLevelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c839b843fba51042743214340d91ea804b2dcf60a3e57d582ec78f66bac338)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProcedureScalaParametersTraceLevelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087e47726119a530ab6b87c4fd24141b751863fd559f7d3bbc9362773f075743)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaParametersTraceLevelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bb0ccfd663e796b8d58d07c3a30bb8dbf1344b13b26ad64e7ce62ffdb2c6a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba34e594d069839ec999931e1db152e125bfad7da00d786d83da03b6adbfcba3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__089058ef5755cab168c7cab100de0cfdedfe8bfc8fd7bad680b068e11863e55d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaParametersTraceLevelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaParametersTraceLevelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5a7d09ab0c7bd9ecb4fb0f4d2d01615df81569b2b2f82aef61b7822d6bed487)
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
    def internal_value(self) -> typing.Optional[ProcedureScalaParametersTraceLevel]:
        return typing.cast(typing.Optional[ProcedureScalaParametersTraceLevel], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ProcedureScalaParametersTraceLevel],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9701810a79acafc2a18d870d29317ad845058317e759944a40fb1031783602dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "secret_id": "secretId",
        "secret_variable_name": "secretVariableName",
    },
)
class ProcedureScalaSecrets:
    def __init__(
        self,
        *,
        secret_id: builtins.str,
        secret_variable_name: builtins.str,
    ) -> None:
        '''
        :param secret_id: Fully qualified name of the allowed `secret <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_. You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the EXTERNAL_ACCESS_INTEGRATIONS parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#secret_id ProcedureScala#secret_id}
        :param secret_variable_name: The variable that will be used in handler code when retrieving information from the secret. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#secret_variable_name ProcedureScala#secret_variable_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d7202e45e87f5221bf049ad0fb56180b323327ac85562d53d2d6d6847bef24)
            check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            check_type(argname="argument secret_variable_name", value=secret_variable_name, expected_type=type_hints["secret_variable_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret_id": secret_id,
            "secret_variable_name": secret_variable_name,
        }

    @builtins.property
    def secret_id(self) -> builtins.str:
        '''Fully qualified name of the allowed `secret <https://docs.snowflake.com/en/sql-reference/sql/create-secret>`_. You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the EXTERNAL_ACCESS_INTEGRATIONS parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#secret_id ProcedureScala#secret_id}
        '''
        result = self._values.get("secret_id")
        assert result is not None, "Required property 'secret_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_variable_name(self) -> builtins.str:
        '''The variable that will be used in handler code when retrieving information from the secret.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#secret_variable_name ProcedureScala#secret_variable_name}
        '''
        result = self._values.get("secret_variable_name")
        assert result is not None, "Required property 'secret_variable_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaSecretsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaSecretsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1d1155c25d8d5ca670b81231bc5728b4b667f1c090422e394a3029c98bb7ba6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureScalaSecretsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db27e9f4ee5c607c96d1e5431f749335fbea3350b9e055d04552b9bbd46e9c66)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaSecretsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aaad5a3d5104d76e0aba9eb007fa94eb22c47f8407c7797ecbb7e81af179c97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e588db7fc6cb9b414318adb148833915ccb63d68b95e6e31688a04b0da111c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d3cfe6becd6dd9dd265d68314c496fecbe600fe249e41ce2c699a8b8cbee49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaSecrets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaSecrets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaSecrets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b86c7b4ef559ec6e8343c540dafe8bce60c5f3f5f28e4aaeaf54910fb20e120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaSecretsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaSecretsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50c5fdf0eac9ae91ad71a62fc47cadd8e19f27d2aa5e3667b7865f29e75867f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef0259e98ec885ef13041003734e596d0bda0f381c00bd182efdc9c031b3f5fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secretVariableName")
    def secret_variable_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretVariableName"))

    @secret_variable_name.setter
    def secret_variable_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f7d04f8369d4cd21bef03e8fbecb082db90820e00447ab7d73c5f4e9423d01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretVariableName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaSecrets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaSecrets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaSecrets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f44308ff312ed279e25d20786e6ccb447974f336ae75af7269cc5d2dffb60622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaShowOutput",
    jsii_struct_bases=[],
    name_mapping={},
)
class ProcedureScalaShowOutput:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaShowOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaShowOutputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaShowOutputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__732bb8ea5ea33f433442bb116633277b1ff04a972a97245440ddbc95b6b66a03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProcedureScalaShowOutputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5573b582c5177aed83b4e0a6f4ef566e7528ec03d4ed45982884a04c26301d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProcedureScalaShowOutputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a33c7dff27afd7e048cfde866f72a92ea37992de76ea13c825ebcac8ca8b7a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e24a12b7c1ecdea5facb367e3cb3c86fe25d18a1aed6740da2f8395ef2195dc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba57749ab9ef55d047a9e91b0aa714405a3785090f774ed2f05b707a306b606b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class ProcedureScalaShowOutputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaShowOutputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ba325fb6d1b739e47d3c7bf2b640c3516df53a50c60332266189bb8a03a47d5)
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
    def internal_value(self) -> typing.Optional[ProcedureScalaShowOutput]:
        return typing.cast(typing.Optional[ProcedureScalaShowOutput], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ProcedureScalaShowOutput]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7946b4ce7ac87896f2ca76a23c1a72e2c19be3c6921515d43bbf6ab626de6c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaTargetPath",
    jsii_struct_bases=[],
    name_mapping={"path_on_stage": "pathOnStage", "stage_location": "stageLocation"},
)
class ProcedureScalaTargetPath:
    def __init__(
        self,
        *,
        path_on_stage: builtins.str,
        stage_location: builtins.str,
    ) -> None:
        '''
        :param path_on_stage: Path for import on stage, without the leading ``/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#path_on_stage ProcedureScala#path_on_stage}
        :param stage_location: Stage location without leading ``@``. To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#stage_location ProcedureScala#stage_location}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3eda247fd058b45e129de55c1292beda3b89abd7b95045f20dfac4d334b9ae)
            check_type(argname="argument path_on_stage", value=path_on_stage, expected_type=type_hints["path_on_stage"])
            check_type(argname="argument stage_location", value=stage_location, expected_type=type_hints["stage_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path_on_stage": path_on_stage,
            "stage_location": stage_location,
        }

    @builtins.property
    def path_on_stage(self) -> builtins.str:
        '''Path for import on stage, without the leading ``/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#path_on_stage ProcedureScala#path_on_stage}
        '''
        result = self._values.get("path_on_stage")
        assert result is not None, "Required property 'path_on_stage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_location(self) -> builtins.str:
        '''Stage location without leading ``@``.

        To use your user's stage set this to ``~``, otherwise pass fully qualified name of the stage (with every part contained in double quotes or use ``snowflake_stage.<your stage's resource name>.fully_qualified_name`` if you manage this stage through terraform).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/snowflake-labs/snowflake/1.0.5/docs/resources/procedure_scala#stage_location ProcedureScala#stage_location}
        '''
        result = self._values.get("stage_location")
        assert result is not None, "Required property 'stage_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcedureScalaTargetPath(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProcedureScalaTargetPathOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-snowflake.procedureScala.ProcedureScalaTargetPathOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cff5b37fb67b6f60123fac273cc37441240e7035455a16e4e9dd5f67f40f59f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53e4ab496c463baecb668a33f829a5881567aa783582ebeb972cc03cb422cd65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathOnStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stageLocation")
    def stage_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stageLocation"))

    @stage_location.setter
    def stage_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf35856915b1185db4fad5b21b152051c062a35712d4157c553ff26c5da4c89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stageLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ProcedureScalaTargetPath]:
        return typing.cast(typing.Optional[ProcedureScalaTargetPath], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ProcedureScalaTargetPath]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d031caa4dd8f80d3891714b1a49b799b7493047dfa3177e95f9a6f6e408c572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ProcedureScala",
    "ProcedureScalaArguments",
    "ProcedureScalaArgumentsList",
    "ProcedureScalaArgumentsOutputReference",
    "ProcedureScalaConfig",
    "ProcedureScalaImports",
    "ProcedureScalaImportsList",
    "ProcedureScalaImportsOutputReference",
    "ProcedureScalaParameters",
    "ProcedureScalaParametersEnableConsoleOutput",
    "ProcedureScalaParametersEnableConsoleOutputList",
    "ProcedureScalaParametersEnableConsoleOutputOutputReference",
    "ProcedureScalaParametersList",
    "ProcedureScalaParametersLogLevel",
    "ProcedureScalaParametersLogLevelList",
    "ProcedureScalaParametersLogLevelOutputReference",
    "ProcedureScalaParametersMetricLevel",
    "ProcedureScalaParametersMetricLevelList",
    "ProcedureScalaParametersMetricLevelOutputReference",
    "ProcedureScalaParametersOutputReference",
    "ProcedureScalaParametersTraceLevel",
    "ProcedureScalaParametersTraceLevelList",
    "ProcedureScalaParametersTraceLevelOutputReference",
    "ProcedureScalaSecrets",
    "ProcedureScalaSecretsList",
    "ProcedureScalaSecretsOutputReference",
    "ProcedureScalaShowOutput",
    "ProcedureScalaShowOutputList",
    "ProcedureScalaShowOutputOutputReference",
    "ProcedureScalaTargetPath",
    "ProcedureScalaTargetPathOutputReference",
]

publication.publish()

def _typecheckingstub__f2874513c85c83a000af1cbf3589a2c09f8379d1996ea64e5cebe2d287e8e6f7(
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
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    execute_as: typing.Optional[builtins.str] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaImports, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    procedure_definition: typing.Optional[builtins.str] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_path: typing.Optional[typing.Union[ProcedureScalaTargetPath, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e79f96b68302b64fb78c0238e16532f843b1b520f4c3d527f1bd5803f8671984(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58934cfefe2c7ef58ecb6e29c6cbc831561af0faee08519fa78646ff4c8536bf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b65386e34dc7636492dc53c7149e757d230ae90cad09a523d65172bc920328b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaImports, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e780cb3e2b0599a507d31e96b1cc7d86d03d07dfd6db3c0af7f9a477231a306(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaSecrets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f1ecd2cfd7c86020eae2b589501db506c71df5007700761199061b4649b651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0a9b33c0d4cb5e3f3a4f7c54be4ce595a54f1bd8ccb865afb9f0674ef5058d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7182cc2032d39061dc12104ce08341e03ac56627449cca4142785e2d7576fefb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ac76fc02b9ed1e35207276e981df4d2a287d3d7314ddfd1a216bfae6bcf5c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1037be18aedd329adc1fbae891e38d11f3512adb0f5847bc3d782e7caf8060(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee8672767f8dc53d7630d2e522d478df17283eaed1279cf101a28371c53f1ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1bdbdbf8fab46e7b195430b5f1e54c2dfe7ebc60e44e718dc602d354765363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c731f39385bf9f112918419d456bad32ddd5ed592fd2fb0b497c84d4a8349f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12ffc256869afa11d5da2610a4a779acec62cd9e8001604f0e83e2b45f8a30c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2915c9b1a3424ff20032b4ce8b11f81956956adc5771fa111fb1dda658dfd204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c2ef57d561113aeca44623d8cccdc135350c425bf2ce5087dba7bb6f0bc60d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff68ae42ad11d16573ea4458ee8ad811271916e9b6750baa87c8cdef8247912e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203851754a3d67f08a96c157d3d291cb0931eeaa5d08d10de9519572f2ee6262(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd08eba56de35f3eac5945d65fee7e1ac273dccef51fdbc8357b075aa97f524d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b5263abf90ac5203ecf653f54d4f31cbe3496f7e96de90af65effebe96e719(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601fe0d7db992f955b4c55ba0e0644c8b773d66bc4ffec2574313e6ab355acd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23f16334127d6bc9ed5796c8d72e4a30ed632dbf14ad1f2cb8869ca70165283e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69963194ed4541d23df71073b8dd5b165dabfda645a716fca20707ef1d6cb55f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27432b425de9cda20c4417df529c189399479f84e763255a87981217e433bce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eacb3101556438dcc95da2ffd836daca499154437fe131d8ccb72afcdbf90f7(
    *,
    arg_data_type: builtins.str,
    arg_name: builtins.str,
    arg_default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2c7805807f71b4d30d8315f9217ff5387816c38df68c7c404c7d02657c9905(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306906a95be0200c2add87a12fc28d27391aeb067f9fe52575fa92f7e414016b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523e898d4a905175e3cbd7ae6ff7bcde8c80450fdc0d6be171e421904dcadfba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79f0d9a07e68c78af6b244ce7488b760ff8de49ccb857078c5abfad0b4b41ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54c51fa4f673934b0c12210cb0c2155935f52b3a30deeb072c4dbeb287614ea2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23bf9c4ba700fe640d5fb153531756fbc3cd43966a05cc50b72615997d7817f6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1afe57b9b91969cedb84bb6a54b3c397047c3698d6e38af4b72a28385ce9a9d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154c41ac47bd092ea358deaa08d59566c2ce1615c2635a951b7f91ed4ad52018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7131e21b92fceba74a6976b708e99723a97023d00b305c17a8f1711391bd22d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de08e398c7b7df08dfd11c49d953042b9989e8865dffaaa599b90ce69c9069e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a845209dc95ba588fb0e14605ee884983fe275716c6c63c6d3225f021ef215d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaArguments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c3f9ab79eb1ed3d030f24db1feadef58b1c115d34ee45c842b000203fb37ea(
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
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    comment: typing.Optional[builtins.str] = None,
    enable_console_output: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    execute_as: typing.Optional[builtins.str] = None,
    external_access_integrations: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    imports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaImports, typing.Dict[builtins.str, typing.Any]]]]] = None,
    is_secure: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    metric_level: typing.Optional[builtins.str] = None,
    null_input_behavior: typing.Optional[builtins.str] = None,
    packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    procedure_definition: typing.Optional[builtins.str] = None,
    secrets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProcedureScalaSecrets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    target_path: typing.Optional[typing.Union[ProcedureScalaTargetPath, typing.Dict[builtins.str, typing.Any]]] = None,
    trace_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8084dd599aacff97f0682c86f4d87fcaaaf537c276996381aeed2283889fa1(
    *,
    path_on_stage: builtins.str,
    stage_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a797a083de4c8f33fc69a2eb2a3fd1ad928b6acc6626e0a4f97a3418ab1601(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0728331e3b96fb079bb48e4d25d2390d4244221dab48e684d4394a14ad5441d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1dc78e016ae4b7462d3816eab03143fbcdca0e53bcff9ceef863235ffe6765b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0872d8e6921bfd391e10b8b2cc924e67d0f10c15af4db58477e139dba19401ab(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85257790fcea95ee0bfee037143c483f873c2a4afbfe3f5a28905ea422991b9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea6e9cc34e6c8869583df7d05a273572e781b884ddd0df10726bdef91d6ecb0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaImports]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455fd50555e156a66b703761f21d21b2a6705f582e0f6f6ae158a8eaf77d99d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2260f8234ab762f813f67a344ccd70f75bf87cb6b87560331a537278af5abaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6851ea3f19f5cc36fbf71f52cd1d07b3beac8f43965375bdfac54e1ae7c278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39de1d4b2c4330aac2955b46e04aa7208a4a5514158156d587afb8380e72b07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaImports]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27a914170d120ded875328de2c7dbd3b0c2a21d007adf2929af1dedc64f53e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de154b0648a9cfb95158adca6ee15cb5129799e578eeedbe051eef0e790bc81c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbffc80a8512217a394e5a8138151d81c89e18daa003024c8e34e509585044b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15af5c62dca56821c1d13554e5082ab52a0d2a1a86df4d0290aa8c78e68db801(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b8c23d6f26e7a741381cc5e8fdf40041a810824af233956952295ffe479822(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9157ae877af943cbe647b5e93b68a31f18880e2a6fa9b98abfbd977959a2bcfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61ee7d291d8c1bddfd76855a5816745a17444490d1f5ee1713c57abc649bbdc(
    value: typing.Optional[ProcedureScalaParametersEnableConsoleOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75119dd85f0eb0cf85eb151ded82e914c4941fb0def9a339f909f8f976bac3f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d708b551082b56364af0d99abff572c8eb0e1a4b930db827e0bf476613eee7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b85a95984e59960ddee0b239f50cd781fbf603330061c740b7eaa1b206691e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce04610e28c38a160fefe2f2939c14ce7457563609e099814d4511c65d1c8bbf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13bb3b9ca908a4680f19f0e408121813c15efccd403adb53963bd825b4ad0480(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31becdb58c58101a928429a9778ce0720b7199e4e76cb1d9a7f7c718450e370b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ea1e027a360f30f7cd40e559249dc1891a388e93ac309d3c90e53ef0f2aef9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f136eb7200654226ff29993e1f093afdf7b74a56cd026db7def85dabaa28ad1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b97c2d158cf8141e34509cad5b08f1b2cd125b189f9adca7749734b4f503ec0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f6da3f5f4262abe20ebbc4d83b9d1295d4f9bc805d062cd7b2a4bb6a59dd2fc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6055f6321434bc12c4680a6c1ad791dae22e3ff06e5e1453531ad38034304081(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828c3886b7c8c1ea4a5a5beb3d6f50debbdd480b36a99177613654b2c84da49a(
    value: typing.Optional[ProcedureScalaParametersLogLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abc53c702df2c31cc7d51b3ce6ab448023b50cb5b009a8c125172f3592493f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c6d99411940952d203de5d84f8c1fbca2a0b37ae81c08887f3529c50a33f97c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1001d3e75fc50e9d2dd02af9d05fa4024fb93f95976e9ba4030ac78db9be1c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05345601843fdc9f71efaedec6020405ee7413182fc63e06489752825be9ff50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd0ea874de58c0c7eb18a9679e0f825775744d290748cdc4462c5b753390fb4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__852473272afae0eee365a57398d485c087ec1fab8a5a5b474d262cd9a39399cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37329a24487df6c5059763286b3f0c39efc7cb2f8f3f47f5235a850c98983bed(
    value: typing.Optional[ProcedureScalaParametersMetricLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541f1e5591863f36a041698d7c49dcad88d7b4ba0f51ad13c77c66108420a81d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799f9592007542de06d8e4b49e73eb86377eeebe17f2baffbca5ce0ac1812c25(
    value: typing.Optional[ProcedureScalaParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c839b843fba51042743214340d91ea804b2dcf60a3e57d582ec78f66bac338(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087e47726119a530ab6b87c4fd24141b751863fd559f7d3bbc9362773f075743(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bb0ccfd663e796b8d58d07c3a30bb8dbf1344b13b26ad64e7ce62ffdb2c6a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba34e594d069839ec999931e1db152e125bfad7da00d786d83da03b6adbfcba3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089058ef5755cab168c7cab100de0cfdedfe8bfc8fd7bad680b068e11863e55d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a7d09ab0c7bd9ecb4fb0f4d2d01615df81569b2b2f82aef61b7822d6bed487(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9701810a79acafc2a18d870d29317ad845058317e759944a40fb1031783602dd(
    value: typing.Optional[ProcedureScalaParametersTraceLevel],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d7202e45e87f5221bf049ad0fb56180b323327ac85562d53d2d6d6847bef24(
    *,
    secret_id: builtins.str,
    secret_variable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d1155c25d8d5ca670b81231bc5728b4b667f1c090422e394a3029c98bb7ba6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db27e9f4ee5c607c96d1e5431f749335fbea3350b9e055d04552b9bbd46e9c66(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aaad5a3d5104d76e0aba9eb007fa94eb22c47f8407c7797ecbb7e81af179c97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e588db7fc6cb9b414318adb148833915ccb63d68b95e6e31688a04b0da111c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3cfe6becd6dd9dd265d68314c496fecbe600fe249e41ce2c699a8b8cbee49b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b86c7b4ef559ec6e8343c540dafe8bce60c5f3f5f28e4aaeaf54910fb20e120(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProcedureScalaSecrets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c5fdf0eac9ae91ad71a62fc47cadd8e19f27d2aa5e3667b7865f29e75867f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0259e98ec885ef13041003734e596d0bda0f381c00bd182efdc9c031b3f5fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f7d04f8369d4cd21bef03e8fbecb082db90820e00447ab7d73c5f4e9423d01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44308ff312ed279e25d20786e6ccb447974f336ae75af7269cc5d2dffb60622(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProcedureScalaSecrets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__732bb8ea5ea33f433442bb116633277b1ff04a972a97245440ddbc95b6b66a03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5573b582c5177aed83b4e0a6f4ef566e7528ec03d4ed45982884a04c26301d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a33c7dff27afd7e048cfde866f72a92ea37992de76ea13c825ebcac8ca8b7a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24a12b7c1ecdea5facb367e3cb3c86fe25d18a1aed6740da2f8395ef2195dc9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba57749ab9ef55d047a9e91b0aa714405a3785090f774ed2f05b707a306b606b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba325fb6d1b739e47d3c7bf2b640c3516df53a50c60332266189bb8a03a47d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7946b4ce7ac87896f2ca76a23c1a72e2c19be3c6921515d43bbf6ab626de6c7(
    value: typing.Optional[ProcedureScalaShowOutput],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3eda247fd058b45e129de55c1292beda3b89abd7b95045f20dfac4d334b9ae(
    *,
    path_on_stage: builtins.str,
    stage_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cff5b37fb67b6f60123fac273cc37441240e7035455a16e4e9dd5f67f40f59f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e4ab496c463baecb668a33f829a5881567aa783582ebeb972cc03cb422cd65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf35856915b1185db4fad5b21b152051c062a35712d4157c553ff26c5da4c89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d031caa4dd8f80d3891714b1a49b799b7493047dfa3177e95f9a6f6e408c572(
    value: typing.Optional[ProcedureScalaTargetPath],
) -> None:
    """Type checking stubs"""
    pass

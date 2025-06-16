r'''
# `google_bigquery_routine`

Refer to the Terraform Registry for docs: [`google_bigquery_routine`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine).
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


class GoogleBigqueryRoutine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine google_bigquery_routine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_id: builtins.str,
        definition_body: builtins.str,
        routine_id: builtins.str,
        routine_type: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryRoutineArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_governance_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        determinism_level: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
        language: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_function_options: typing.Optional[typing.Union["GoogleBigqueryRoutineRemoteFunctionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        return_table_type: typing.Optional[builtins.str] = None,
        return_type: typing.Optional[builtins.str] = None,
        security_mode: typing.Optional[builtins.str] = None,
        spark_options: typing.Optional[typing.Union["GoogleBigqueryRoutineSparkOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryRoutineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine google_bigquery_routine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_id: The ID of the dataset containing this routine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#dataset_id GoogleBigqueryRoutine#dataset_id}
        :param definition_body: The body of the routine. For functions, this is the expression in the AS clause. If language=SQL, it is the substring inside (but excluding) the parentheses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#definition_body GoogleBigqueryRoutine#definition_body}
        :param routine_id: The ID of the the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#routine_id GoogleBigqueryRoutine#routine_id}
        :param routine_type: The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#routine_type GoogleBigqueryRoutine#routine_type}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#arguments GoogleBigqueryRoutine#arguments}
        :param data_governance_type: If set to DATA_MASKING, the function is validated and made available as a masking function. For more information, see https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask Possible values: ["DATA_MASKING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#data_governance_type GoogleBigqueryRoutine#data_governance_type}
        :param description: The description of the routine if defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#description GoogleBigqueryRoutine#description}
        :param determinism_level: The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#determinism_level GoogleBigqueryRoutine#determinism_level}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#id GoogleBigqueryRoutine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imported_libraries: Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#imported_libraries GoogleBigqueryRoutine#imported_libraries}
        :param language: The language of the routine. Possible values: ["SQL", "JAVASCRIPT", "PYTHON", "JAVA", "SCALA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#language GoogleBigqueryRoutine#language}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#project GoogleBigqueryRoutine#project}.
        :param remote_function_options: remote_function_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#remote_function_options GoogleBigqueryRoutine#remote_function_options}
        :param return_table_type: Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION". If absent, the return table type is inferred from definitionBody at query time in each query that references this routine. If present, then the columns in the evaluated table result will be cast to match the column types specificed in return table type, at query time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#return_table_type GoogleBigqueryRoutine#return_table_type}
        :param return_type: A JSON schema for the return type. Optional if language = "SQL"; required otherwise. If absent, the return type is inferred from definitionBody at query time in each query that references this routine. If present, then the evaluated result will be cast to the specified returned type at query time. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switche d the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#return_type GoogleBigqueryRoutine#return_type}
        :param security_mode: Optional. The security mode of the routine, if defined. If not defined, the security mode is automatically determined from the routine's configuration. Possible values: ["DEFINER", "INVOKER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#security_mode GoogleBigqueryRoutine#security_mode}
        :param spark_options: spark_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#spark_options GoogleBigqueryRoutine#spark_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#timeouts GoogleBigqueryRoutine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76baa773e48f67c1721de738decf39e94c4f1f78245e4f111a0cbab24e68c88d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleBigqueryRoutineConfig(
            dataset_id=dataset_id,
            definition_body=definition_body,
            routine_id=routine_id,
            routine_type=routine_type,
            arguments=arguments,
            data_governance_type=data_governance_type,
            description=description,
            determinism_level=determinism_level,
            id=id,
            imported_libraries=imported_libraries,
            language=language,
            project=project,
            remote_function_options=remote_function_options,
            return_table_type=return_table_type,
            return_type=return_type,
            security_mode=security_mode,
            spark_options=spark_options,
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
        '''Generates CDKTF code for importing a GoogleBigqueryRoutine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleBigqueryRoutine to import.
        :param import_from_id: The id of the existing GoogleBigqueryRoutine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleBigqueryRoutine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a39152f4aebba08c4d501d88ca816828bf8fc603be86228fa20adfa6d791e9b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleBigqueryRoutineArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021aa711a9dd8a24245e6b1352995c6a6115762168623d8b6ea5242427693f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArguments", [value]))

    @jsii.member(jsii_name="putRemoteFunctionOptions")
    def put_remote_function_options(
        self,
        *,
        connection: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        max_batching_rows: typing.Optional[builtins.str] = None,
        user_defined_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: Fully qualified name of the user-provided connection object which holds the authentication information to send requests to the remote service. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#connection GoogleBigqueryRoutine#connection}
        :param endpoint: Endpoint of the user-provided remote service, e.g. 'https://us-east1-my_gcf_project.cloudfunctions.net/remote_add'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#endpoint GoogleBigqueryRoutine#endpoint}
        :param max_batching_rows: Max number of rows in each batch sent to the remote service. If absent or if 0, BigQuery dynamically decides the number of rows in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#max_batching_rows GoogleBigqueryRoutine#max_batching_rows}
        :param user_defined_context: User-defined context as a set of key/value pairs, which will be sent as function invocation context together with batched arguments in the requests to the remote service. The total number of bytes of keys and values must be less than 8KB. An object containing a list of "key": value pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#user_defined_context GoogleBigqueryRoutine#user_defined_context}
        '''
        value = GoogleBigqueryRoutineRemoteFunctionOptions(
            connection=connection,
            endpoint=endpoint,
            max_batching_rows=max_batching_rows,
            user_defined_context=user_defined_context,
        )

        return typing.cast(None, jsii.invoke(self, "putRemoteFunctionOptions", [value]))

    @jsii.member(jsii_name="putSparkOptions")
    def put_spark_options(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[builtins.str] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        py_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: Archive files to be extracted into the working directory of each executor. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#archive_uris GoogleBigqueryRoutine#archive_uris}
        :param connection: Fully qualified name of the user-provided Spark connection object. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#connection GoogleBigqueryRoutine#connection}
        :param container_image: Custom container image for the runtime environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#container_image GoogleBigqueryRoutine#container_image}
        :param file_uris: Files to be placed in the working directory of each executor. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#file_uris GoogleBigqueryRoutine#file_uris}
        :param jar_uris: JARs to include on the driver and executor CLASSPATH. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#jar_uris GoogleBigqueryRoutine#jar_uris}
        :param main_class: The fully qualified name of a class in jarUris, for example, com.example.wordcount. Exactly one of mainClass and main_jar_uri field should be set for Java/Scala language type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#main_class GoogleBigqueryRoutine#main_class}
        :param main_file_uri: The main file/jar URI of the Spark application. Exactly one of the definitionBody field and the mainFileUri field must be set for Python. Exactly one of mainClass and mainFileUri field should be set for Java/Scala language type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#main_file_uri GoogleBigqueryRoutine#main_file_uri}
        :param properties: Configuration properties as a set of key/value pairs, which will be passed on to the Spark application. For more information, see Apache Spark and the procedure option list. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#properties GoogleBigqueryRoutine#properties}
        :param py_file_uris: Python files to be placed on the PYTHONPATH for PySpark application. Supported file types: .py, .egg, and .zip. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#py_file_uris GoogleBigqueryRoutine#py_file_uris}
        :param runtime_version: Runtime version. If not specified, the default runtime version is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#runtime_version GoogleBigqueryRoutine#runtime_version}
        '''
        value = GoogleBigqueryRoutineSparkOptions(
            archive_uris=archive_uris,
            connection=connection,
            container_image=container_image,
            file_uris=file_uris,
            jar_uris=jar_uris,
            main_class=main_class,
            main_file_uri=main_file_uri,
            properties=properties,
            py_file_uris=py_file_uris,
            runtime_version=runtime_version,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkOptions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#create GoogleBigqueryRoutine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#delete GoogleBigqueryRoutine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#update GoogleBigqueryRoutine#update}.
        '''
        value = GoogleBigqueryRoutineTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetArguments")
    def reset_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArguments", []))

    @jsii.member(jsii_name="resetDataGovernanceType")
    def reset_data_governance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataGovernanceType", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDeterminismLevel")
    def reset_determinism_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeterminismLevel", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetImportedLibraries")
    def reset_imported_libraries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImportedLibraries", []))

    @jsii.member(jsii_name="resetLanguage")
    def reset_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguage", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRemoteFunctionOptions")
    def reset_remote_function_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteFunctionOptions", []))

    @jsii.member(jsii_name="resetReturnTableType")
    def reset_return_table_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnTableType", []))

    @jsii.member(jsii_name="resetReturnType")
    def reset_return_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnType", []))

    @jsii.member(jsii_name="resetSecurityMode")
    def reset_security_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityMode", []))

    @jsii.member(jsii_name="resetSparkOptions")
    def reset_spark_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkOptions", []))

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
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> "GoogleBigqueryRoutineArgumentsList":
        return typing.cast("GoogleBigqueryRoutineArgumentsList", jsii.get(self, "arguments"))

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creationTime"))

    @builtins.property
    @jsii.member(jsii_name="lastModifiedTime")
    def last_modified_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lastModifiedTime"))

    @builtins.property
    @jsii.member(jsii_name="remoteFunctionOptions")
    def remote_function_options(
        self,
    ) -> "GoogleBigqueryRoutineRemoteFunctionOptionsOutputReference":
        return typing.cast("GoogleBigqueryRoutineRemoteFunctionOptionsOutputReference", jsii.get(self, "remoteFunctionOptions"))

    @builtins.property
    @jsii.member(jsii_name="sparkOptions")
    def spark_options(self) -> "GoogleBigqueryRoutineSparkOptionsOutputReference":
        return typing.cast("GoogleBigqueryRoutineSparkOptionsOutputReference", jsii.get(self, "sparkOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleBigqueryRoutineTimeoutsOutputReference":
        return typing.cast("GoogleBigqueryRoutineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryRoutineArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleBigqueryRoutineArguments"]]], jsii.get(self, "argumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataGovernanceTypeInput")
    def data_governance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataGovernanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="datasetIdInput")
    def dataset_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "datasetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="definitionBodyInput")
    def definition_body_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definitionBodyInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="determinismLevelInput")
    def determinism_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "determinismLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importedLibrariesInput")
    def imported_libraries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "importedLibrariesInput"))

    @builtins.property
    @jsii.member(jsii_name="languageInput")
    def language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteFunctionOptionsInput")
    def remote_function_options_input(
        self,
    ) -> typing.Optional["GoogleBigqueryRoutineRemoteFunctionOptions"]:
        return typing.cast(typing.Optional["GoogleBigqueryRoutineRemoteFunctionOptions"], jsii.get(self, "remoteFunctionOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="returnTableTypeInput")
    def return_table_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnTableTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="returnTypeInput")
    def return_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "returnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="routineIdInput")
    def routine_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routineIdInput"))

    @builtins.property
    @jsii.member(jsii_name="routineTypeInput")
    def routine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="securityModeInput")
    def security_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityModeInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkOptionsInput")
    def spark_options_input(
        self,
    ) -> typing.Optional["GoogleBigqueryRoutineSparkOptions"]:
        return typing.cast(typing.Optional["GoogleBigqueryRoutineSparkOptions"], jsii.get(self, "sparkOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryRoutineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleBigqueryRoutineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataGovernanceType")
    def data_governance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataGovernanceType"))

    @data_governance_type.setter
    def data_governance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__553cbc928e34c637a87e00adbaead88ba2d037e5bc491ebdf1855cd82d410f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataGovernanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b55c3c6d3cc889163265877f12eed795a9e347addf9e08e3a6e629f259bf2936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="definitionBody")
    def definition_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "definitionBody"))

    @definition_body.setter
    def definition_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b37a6cbbafe9ea68f1ab9d4fb8701393e1a39cd0b8a664599d7f2eee855130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3965afb911726ed2c5e1367f69a6bd858c958de834913a8b2484861a590dcad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="determinismLevel")
    def determinism_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "determinismLevel"))

    @determinism_level.setter
    def determinism_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2dcf6027012bbb1342523d874f4bbb5023e0e74da357b49637a4c5a4956f2c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "determinismLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac889d9b12346d8521c5d694528b32f82ea5b80754e7c13dde24a853e4493e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importedLibraries")
    def imported_libraries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "importedLibraries"))

    @imported_libraries.setter
    def imported_libraries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53afc1bbf5ed2bbdaaf8303f6fab337cd56008d70fa48f9525ee9c69bbe8715c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importedLibraries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @language.setter
    def language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b662a0498fdfcf715fce340c2568ceb24e7484f1d2c6ed62877e6492a68cafc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "language", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5505e9c318a77d934007b3880fa6e712865a917cd22016790c50cfa7e4fca713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnTableType")
    def return_table_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnTableType"))

    @return_table_type.setter
    def return_table_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d34662efef8dba5656e0b0f674ea9c47da8011b9157cdf4ca0df65c2397ad8a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnTableType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec058399c64e693fb94473e176f411f7ee059c8c2d21529c8cb069901ef06c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routineId")
    def routine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routineId"))

    @routine_id.setter
    def routine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93c83deb87b0e7cff70055277a5393e4921ed9209708df020bd5077c3f6339a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routineType")
    def routine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routineType"))

    @routine_type.setter
    def routine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9cac2d93e40e8c157b3e91e58f0858735c8ce2156c7515e57792d17deac8b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityMode")
    def security_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityMode"))

    @security_mode.setter
    def security_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024f846a8a9756de913222a2f988abbdc30590d19b3d7df1bf92a0c553833c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineArguments",
    jsii_struct_bases=[],
    name_mapping={
        "argument_kind": "argumentKind",
        "data_type": "dataType",
        "mode": "mode",
        "name": "name",
    },
)
class GoogleBigqueryRoutineArguments:
    def __init__(
        self,
        *,
        argument_kind: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param argument_kind: Defaults to FIXED_TYPE. Default value: "FIXED_TYPE" Possible values: ["FIXED_TYPE", "ANY_TYPE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#argument_kind GoogleBigqueryRoutine#argument_kind}
        :param data_type: A JSON schema for the data type. Required unless argumentKind = ANY_TYPE. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switched the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#data_type GoogleBigqueryRoutine#data_type}
        :param mode: Specifies whether the argument is input or output. Can be set for procedures only. Possible values: ["IN", "OUT", "INOUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#mode GoogleBigqueryRoutine#mode}
        :param name: The name of this argument. Can be absent for function return argument. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#name GoogleBigqueryRoutine#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62a46e0ba5999d79bd81faa325bf7c3c66ed90c2e668a81304f6be2e915928b)
            check_type(argname="argument argument_kind", value=argument_kind, expected_type=type_hints["argument_kind"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if argument_kind is not None:
            self._values["argument_kind"] = argument_kind
        if data_type is not None:
            self._values["data_type"] = data_type
        if mode is not None:
            self._values["mode"] = mode
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def argument_kind(self) -> typing.Optional[builtins.str]:
        '''Defaults to FIXED_TYPE. Default value: "FIXED_TYPE" Possible values: ["FIXED_TYPE", "ANY_TYPE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#argument_kind GoogleBigqueryRoutine#argument_kind}
        '''
        result = self._values.get("argument_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_type(self) -> typing.Optional[builtins.str]:
        '''A JSON schema for the data type.

        Required unless argumentKind = ANY_TYPE.
        ~>**NOTE**: Because this field expects a JSON string, any changes to the string
        will create a diff, even if the JSON itself hasn't changed. If the API returns
        a different value for the same schema, e.g. it switched the order of values
        or replaced STRUCT field type with RECORD field type, we currently cannot
        suppress the recurring diff this causes. As a workaround, we recommend using
        the schema as returned by the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#data_type GoogleBigqueryRoutine#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the argument is input or output. Can be set for procedures only. Possible values: ["IN", "OUT", "INOUT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#mode GoogleBigqueryRoutine#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this argument. Can be absent for function return argument.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#name GoogleBigqueryRoutine#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryRoutineArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryRoutineArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineArgumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb75acd5856cf5dcc2c23f4004d2fe632b83533ae48ce1da03675841de8a5b29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleBigqueryRoutineArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb938d1bd9c49efc75a7963243921bc60c8f2addb5d9a653e55cb9025b068990)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleBigqueryRoutineArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f376fd35f4ad1b2c79ee2858049e13b14b539708d18c5d8942a34a61e1a6ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3db89d3a39081f26effb4a9185be7329f9a0263327f03fbc29cb23a0b42d07c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfbfbdc535fb080176e5bd6bb5c9de6e4a02975e14720b359d3b41963fc0120d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryRoutineArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryRoutineArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryRoutineArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d358471e0d0c3100b0805aec9f05a62e6046d97d2f72dea49371615703e4000d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleBigqueryRoutineArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineArgumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84b1ad065dd6c98b1f5427eda2d04d60a2b3c09393b3e4852d4c070cb46510e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetArgumentKind")
    def reset_argument_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgumentKind", []))

    @jsii.member(jsii_name="resetDataType")
    def reset_data_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataType", []))

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="argumentKindInput")
    def argument_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "argumentKindInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypeInput")
    def data_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="argumentKind")
    def argument_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "argumentKind"))

    @argument_kind.setter
    def argument_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d44abf6e102283f319dd2bf7aaf0e0fbdeb8887a424d81bd9f833eb0d27b50e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argumentKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a96899023786290ebccdf82f9270a829a37f889ba2a1c94b329893185ce209f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c5c0d67f7af22e93829c0415b6b5dad6f1f23cd986179eb92e85cdd1ff4760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff6e78e9fab589e2decff61c9e470ebcde4eb01cb27bf4d78feca001032c3071)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryRoutineArguments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryRoutineArguments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryRoutineArguments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773b718e09108989a7f2c17dcefcad36d84f157a83ef9baab4a158121fff5d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "dataset_id": "datasetId",
        "definition_body": "definitionBody",
        "routine_id": "routineId",
        "routine_type": "routineType",
        "arguments": "arguments",
        "data_governance_type": "dataGovernanceType",
        "description": "description",
        "determinism_level": "determinismLevel",
        "id": "id",
        "imported_libraries": "importedLibraries",
        "language": "language",
        "project": "project",
        "remote_function_options": "remoteFunctionOptions",
        "return_table_type": "returnTableType",
        "return_type": "returnType",
        "security_mode": "securityMode",
        "spark_options": "sparkOptions",
        "timeouts": "timeouts",
    },
)
class GoogleBigqueryRoutineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dataset_id: builtins.str,
        definition_body: builtins.str,
        routine_id: builtins.str,
        routine_type: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_governance_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        determinism_level: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
        language: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_function_options: typing.Optional[typing.Union["GoogleBigqueryRoutineRemoteFunctionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        return_table_type: typing.Optional[builtins.str] = None,
        return_type: typing.Optional[builtins.str] = None,
        security_mode: typing.Optional[builtins.str] = None,
        spark_options: typing.Optional[typing.Union["GoogleBigqueryRoutineSparkOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleBigqueryRoutineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_id: The ID of the dataset containing this routine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#dataset_id GoogleBigqueryRoutine#dataset_id}
        :param definition_body: The body of the routine. For functions, this is the expression in the AS clause. If language=SQL, it is the substring inside (but excluding) the parentheses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#definition_body GoogleBigqueryRoutine#definition_body}
        :param routine_id: The ID of the the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#routine_id GoogleBigqueryRoutine#routine_id}
        :param routine_type: The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#routine_type GoogleBigqueryRoutine#routine_type}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#arguments GoogleBigqueryRoutine#arguments}
        :param data_governance_type: If set to DATA_MASKING, the function is validated and made available as a masking function. For more information, see https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask Possible values: ["DATA_MASKING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#data_governance_type GoogleBigqueryRoutine#data_governance_type}
        :param description: The description of the routine if defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#description GoogleBigqueryRoutine#description}
        :param determinism_level: The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#determinism_level GoogleBigqueryRoutine#determinism_level}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#id GoogleBigqueryRoutine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imported_libraries: Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#imported_libraries GoogleBigqueryRoutine#imported_libraries}
        :param language: The language of the routine. Possible values: ["SQL", "JAVASCRIPT", "PYTHON", "JAVA", "SCALA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#language GoogleBigqueryRoutine#language}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#project GoogleBigqueryRoutine#project}.
        :param remote_function_options: remote_function_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#remote_function_options GoogleBigqueryRoutine#remote_function_options}
        :param return_table_type: Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION". If absent, the return table type is inferred from definitionBody at query time in each query that references this routine. If present, then the columns in the evaluated table result will be cast to match the column types specificed in return table type, at query time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#return_table_type GoogleBigqueryRoutine#return_table_type}
        :param return_type: A JSON schema for the return type. Optional if language = "SQL"; required otherwise. If absent, the return type is inferred from definitionBody at query time in each query that references this routine. If present, then the evaluated result will be cast to the specified returned type at query time. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switche d the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#return_type GoogleBigqueryRoutine#return_type}
        :param security_mode: Optional. The security mode of the routine, if defined. If not defined, the security mode is automatically determined from the routine's configuration. Possible values: ["DEFINER", "INVOKER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#security_mode GoogleBigqueryRoutine#security_mode}
        :param spark_options: spark_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#spark_options GoogleBigqueryRoutine#spark_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#timeouts GoogleBigqueryRoutine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(remote_function_options, dict):
            remote_function_options = GoogleBigqueryRoutineRemoteFunctionOptions(**remote_function_options)
        if isinstance(spark_options, dict):
            spark_options = GoogleBigqueryRoutineSparkOptions(**spark_options)
        if isinstance(timeouts, dict):
            timeouts = GoogleBigqueryRoutineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36f65d55167b638fe11b162b212bf4b43f3b85cfe0d4ed8b6c80bec8e7dd218)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument dataset_id", value=dataset_id, expected_type=type_hints["dataset_id"])
            check_type(argname="argument definition_body", value=definition_body, expected_type=type_hints["definition_body"])
            check_type(argname="argument routine_id", value=routine_id, expected_type=type_hints["routine_id"])
            check_type(argname="argument routine_type", value=routine_type, expected_type=type_hints["routine_type"])
            check_type(argname="argument arguments", value=arguments, expected_type=type_hints["arguments"])
            check_type(argname="argument data_governance_type", value=data_governance_type, expected_type=type_hints["data_governance_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument determinism_level", value=determinism_level, expected_type=type_hints["determinism_level"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument imported_libraries", value=imported_libraries, expected_type=type_hints["imported_libraries"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument remote_function_options", value=remote_function_options, expected_type=type_hints["remote_function_options"])
            check_type(argname="argument return_table_type", value=return_table_type, expected_type=type_hints["return_table_type"])
            check_type(argname="argument return_type", value=return_type, expected_type=type_hints["return_type"])
            check_type(argname="argument security_mode", value=security_mode, expected_type=type_hints["security_mode"])
            check_type(argname="argument spark_options", value=spark_options, expected_type=type_hints["spark_options"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataset_id": dataset_id,
            "definition_body": definition_body,
            "routine_id": routine_id,
            "routine_type": routine_type,
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
        if data_governance_type is not None:
            self._values["data_governance_type"] = data_governance_type
        if description is not None:
            self._values["description"] = description
        if determinism_level is not None:
            self._values["determinism_level"] = determinism_level
        if id is not None:
            self._values["id"] = id
        if imported_libraries is not None:
            self._values["imported_libraries"] = imported_libraries
        if language is not None:
            self._values["language"] = language
        if project is not None:
            self._values["project"] = project
        if remote_function_options is not None:
            self._values["remote_function_options"] = remote_function_options
        if return_table_type is not None:
            self._values["return_table_type"] = return_table_type
        if return_type is not None:
            self._values["return_type"] = return_type
        if security_mode is not None:
            self._values["security_mode"] = security_mode
        if spark_options is not None:
            self._values["spark_options"] = spark_options
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
    def dataset_id(self) -> builtins.str:
        '''The ID of the dataset containing this routine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#dataset_id GoogleBigqueryRoutine#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def definition_body(self) -> builtins.str:
        '''The body of the routine.

        For functions, this is the expression in the AS clause.
        If language=SQL, it is the substring inside (but excluding) the parentheses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#definition_body GoogleBigqueryRoutine#definition_body}
        '''
        result = self._values.get("definition_body")
        assert result is not None, "Required property 'definition_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routine_id(self) -> builtins.str:
        '''The ID of the the routine.

        The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#routine_id GoogleBigqueryRoutine#routine_id}
        '''
        result = self._values.get("routine_id")
        assert result is not None, "Required property 'routine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routine_type(self) -> builtins.str:
        '''The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#routine_type GoogleBigqueryRoutine#routine_type}
        '''
        result = self._values.get("routine_type")
        assert result is not None, "Required property 'routine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryRoutineArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#arguments GoogleBigqueryRoutine#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryRoutineArguments]]], result)

    @builtins.property
    def data_governance_type(self) -> typing.Optional[builtins.str]:
        '''If set to DATA_MASKING, the function is validated and made available as a masking function.

        For more information, see https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask Possible values: ["DATA_MASKING"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#data_governance_type GoogleBigqueryRoutine#data_governance_type}
        '''
        result = self._values.get("data_governance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the routine if defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#description GoogleBigqueryRoutine#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def determinism_level(self) -> typing.Optional[builtins.str]:
        '''The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#determinism_level GoogleBigqueryRoutine#determinism_level}
        '''
        result = self._values.get("determinism_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#id GoogleBigqueryRoutine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imported_libraries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#imported_libraries GoogleBigqueryRoutine#imported_libraries}
        '''
        result = self._values.get("imported_libraries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''The language of the routine. Possible values: ["SQL", "JAVASCRIPT", "PYTHON", "JAVA", "SCALA"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#language GoogleBigqueryRoutine#language}
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#project GoogleBigqueryRoutine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_function_options(
        self,
    ) -> typing.Optional["GoogleBigqueryRoutineRemoteFunctionOptions"]:
        '''remote_function_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#remote_function_options GoogleBigqueryRoutine#remote_function_options}
        '''
        result = self._values.get("remote_function_options")
        return typing.cast(typing.Optional["GoogleBigqueryRoutineRemoteFunctionOptions"], result)

    @builtins.property
    def return_table_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION".

        If absent, the return table type is inferred from definitionBody at query time in each query
        that references this routine. If present, then the columns in the evaluated table result will
        be cast to match the column types specificed in return table type, at query time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#return_table_type GoogleBigqueryRoutine#return_table_type}
        '''
        result = self._values.get("return_table_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def return_type(self) -> typing.Optional[builtins.str]:
        '''A JSON schema for the return type.

        Optional if language = "SQL"; required otherwise.
        If absent, the return type is inferred from definitionBody at query time in each query
        that references this routine. If present, then the evaluated result will be cast to
        the specified returned type at query time. ~>**NOTE**: Because this field expects a JSON
        string, any changes to the string will create a diff, even if the JSON itself hasn't
        changed. If the API returns a different value for the same schema, e.g. it switche
        d the order of values or replaced STRUCT field type with RECORD field type, we currently
        cannot suppress the recurring diff this causes. As a workaround, we recommend using
        the schema as returned by the API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#return_type GoogleBigqueryRoutine#return_type}
        '''
        result = self._values.get("return_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The security mode of the routine, if defined. If not defined, the security mode is automatically determined from the routine's configuration. Possible values: ["DEFINER", "INVOKER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#security_mode GoogleBigqueryRoutine#security_mode}
        '''
        result = self._values.get("security_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_options(self) -> typing.Optional["GoogleBigqueryRoutineSparkOptions"]:
        '''spark_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#spark_options GoogleBigqueryRoutine#spark_options}
        '''
        result = self._values.get("spark_options")
        return typing.cast(typing.Optional["GoogleBigqueryRoutineSparkOptions"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleBigqueryRoutineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#timeouts GoogleBigqueryRoutine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleBigqueryRoutineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryRoutineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineRemoteFunctionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "connection": "connection",
        "endpoint": "endpoint",
        "max_batching_rows": "maxBatchingRows",
        "user_defined_context": "userDefinedContext",
    },
)
class GoogleBigqueryRoutineRemoteFunctionOptions:
    def __init__(
        self,
        *,
        connection: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        max_batching_rows: typing.Optional[builtins.str] = None,
        user_defined_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: Fully qualified name of the user-provided connection object which holds the authentication information to send requests to the remote service. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#connection GoogleBigqueryRoutine#connection}
        :param endpoint: Endpoint of the user-provided remote service, e.g. 'https://us-east1-my_gcf_project.cloudfunctions.net/remote_add'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#endpoint GoogleBigqueryRoutine#endpoint}
        :param max_batching_rows: Max number of rows in each batch sent to the remote service. If absent or if 0, BigQuery dynamically decides the number of rows in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#max_batching_rows GoogleBigqueryRoutine#max_batching_rows}
        :param user_defined_context: User-defined context as a set of key/value pairs, which will be sent as function invocation context together with batched arguments in the requests to the remote service. The total number of bytes of keys and values must be less than 8KB. An object containing a list of "key": value pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#user_defined_context GoogleBigqueryRoutine#user_defined_context}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7ff73a6bd2735a4322f764c19ebbdcf37d3879eb3fecdb77fc4c680013a5d7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument max_batching_rows", value=max_batching_rows, expected_type=type_hints["max_batching_rows"])
            check_type(argname="argument user_defined_context", value=user_defined_context, expected_type=type_hints["user_defined_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection is not None:
            self._values["connection"] = connection
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if max_batching_rows is not None:
            self._values["max_batching_rows"] = max_batching_rows
        if user_defined_context is not None:
            self._values["user_defined_context"] = user_defined_context

    @builtins.property
    def connection(self) -> typing.Optional[builtins.str]:
        '''Fully qualified name of the user-provided connection object which holds the authentication information to send requests to the remote service.

        Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}"

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#connection GoogleBigqueryRoutine#connection}
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Endpoint of the user-provided remote service, e.g. 'https://us-east1-my_gcf_project.cloudfunctions.net/remote_add'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#endpoint GoogleBigqueryRoutine#endpoint}
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_batching_rows(self) -> typing.Optional[builtins.str]:
        '''Max number of rows in each batch sent to the remote service.

        If absent or if 0,
        BigQuery dynamically decides the number of rows in a batch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#max_batching_rows GoogleBigqueryRoutine#max_batching_rows}
        '''
        result = self._values.get("max_batching_rows")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_defined_context(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined context as a set of key/value pairs, which will be sent as function invocation context together with batched arguments in the requests to the remote service.

        The total number of bytes of keys and values must be less than 8KB.

        An object containing a list of "key": value pairs. Example:
        '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#user_defined_context GoogleBigqueryRoutine#user_defined_context}
        '''
        result = self._values.get("user_defined_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryRoutineRemoteFunctionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryRoutineRemoteFunctionOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineRemoteFunctionOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__886e327f81e3fa0fc497e12904b4e2383a2def586ed22ce601a177ccb6fc450d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConnection")
    def reset_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnection", []))

    @jsii.member(jsii_name="resetEndpoint")
    def reset_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoint", []))

    @jsii.member(jsii_name="resetMaxBatchingRows")
    def reset_max_batching_rows(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxBatchingRows", []))

    @jsii.member(jsii_name="resetUserDefinedContext")
    def reset_user_defined_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserDefinedContext", []))

    @builtins.property
    @jsii.member(jsii_name="connectionInput")
    def connection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="maxBatchingRowsInput")
    def max_batching_rows_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxBatchingRowsInput"))

    @builtins.property
    @jsii.member(jsii_name="userDefinedContextInput")
    def user_defined_context_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "userDefinedContextInput"))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connection"))

    @connection.setter
    def connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4010aa6dbaee132b99db84af5ecbfde6b31626fb4f4a1d02177d2f76879844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc31af4e98e2010c5ef6bc2bdbbc512003240e8badddbebacaa6f30f5e2ccada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBatchingRows")
    def max_batching_rows(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxBatchingRows"))

    @max_batching_rows.setter
    def max_batching_rows(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f5b9b2c3ed6094b2313ed943c789493a27ec7f9f3a31aab109b6bc92083dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBatchingRows", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userDefinedContext")
    def user_defined_context(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "userDefinedContext"))

    @user_defined_context.setter
    def user_defined_context(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd678cac9c9c0b7682b7df447c7246661ca0e38243b738c323e1a9798b9cc21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDefinedContext", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleBigqueryRoutineRemoteFunctionOptions]:
        return typing.cast(typing.Optional[GoogleBigqueryRoutineRemoteFunctionOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryRoutineRemoteFunctionOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39158f6ff322e5bb12dd06b6415c09b07057781ab406e758bd3ae5ab5153b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineSparkOptions",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "connection": "connection",
        "container_image": "containerImage",
        "file_uris": "fileUris",
        "jar_uris": "jarUris",
        "main_class": "mainClass",
        "main_file_uri": "mainFileUri",
        "properties": "properties",
        "py_file_uris": "pyFileUris",
        "runtime_version": "runtimeVersion",
    },
)
class GoogleBigqueryRoutineSparkOptions:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[builtins.str] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        py_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: Archive files to be extracted into the working directory of each executor. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#archive_uris GoogleBigqueryRoutine#archive_uris}
        :param connection: Fully qualified name of the user-provided Spark connection object. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#connection GoogleBigqueryRoutine#connection}
        :param container_image: Custom container image for the runtime environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#container_image GoogleBigqueryRoutine#container_image}
        :param file_uris: Files to be placed in the working directory of each executor. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#file_uris GoogleBigqueryRoutine#file_uris}
        :param jar_uris: JARs to include on the driver and executor CLASSPATH. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#jar_uris GoogleBigqueryRoutine#jar_uris}
        :param main_class: The fully qualified name of a class in jarUris, for example, com.example.wordcount. Exactly one of mainClass and main_jar_uri field should be set for Java/Scala language type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#main_class GoogleBigqueryRoutine#main_class}
        :param main_file_uri: The main file/jar URI of the Spark application. Exactly one of the definitionBody field and the mainFileUri field must be set for Python. Exactly one of mainClass and mainFileUri field should be set for Java/Scala language type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#main_file_uri GoogleBigqueryRoutine#main_file_uri}
        :param properties: Configuration properties as a set of key/value pairs, which will be passed on to the Spark application. For more information, see Apache Spark and the procedure option list. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#properties GoogleBigqueryRoutine#properties}
        :param py_file_uris: Python files to be placed on the PYTHONPATH for PySpark application. Supported file types: .py, .egg, and .zip. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#py_file_uris GoogleBigqueryRoutine#py_file_uris}
        :param runtime_version: Runtime version. If not specified, the default runtime version is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#runtime_version GoogleBigqueryRoutine#runtime_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91a650389e7651bf90d6e3b2eafbe82d87987839ef9d942bd030643ce356eb28)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_uris", value=jar_uris, expected_type=type_hints["jar_uris"])
            check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
            check_type(argname="argument main_file_uri", value=main_file_uri, expected_type=type_hints["main_file_uri"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument py_file_uris", value=py_file_uris, expected_type=type_hints["py_file_uris"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if connection is not None:
            self._values["connection"] = connection
        if container_image is not None:
            self._values["container_image"] = container_image
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_uris is not None:
            self._values["jar_uris"] = jar_uris
        if main_class is not None:
            self._values["main_class"] = main_class
        if main_file_uri is not None:
            self._values["main_file_uri"] = main_file_uri
        if properties is not None:
            self._values["properties"] = properties
        if py_file_uris is not None:
            self._values["py_file_uris"] = py_file_uris
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Archive files to be extracted into the working directory of each executor.

        For more information about Apache Spark, see Apache Spark.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#archive_uris GoogleBigqueryRoutine#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection(self) -> typing.Optional[builtins.str]:
        '''Fully qualified name of the user-provided Spark connection object. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#connection GoogleBigqueryRoutine#connection}
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_image(self) -> typing.Optional[builtins.str]:
        '''Custom container image for the runtime environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#container_image GoogleBigqueryRoutine#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Files to be placed in the working directory of each executor.

        For more information about Apache Spark, see Apache Spark.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#file_uris GoogleBigqueryRoutine#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''JARs to include on the driver and executor CLASSPATH. For more information about Apache Spark, see Apache Spark.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#jar_uris GoogleBigqueryRoutine#jar_uris}
        '''
        result = self._values.get("jar_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of a class in jarUris, for example, com.example.wordcount. Exactly one of mainClass and main_jar_uri field should be set for Java/Scala language type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#main_class GoogleBigqueryRoutine#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_file_uri(self) -> typing.Optional[builtins.str]:
        '''The main file/jar URI of the Spark application.

        Exactly one of the definitionBody field and the mainFileUri field must be set for Python.
        Exactly one of mainClass and mainFileUri field should be set for Java/Scala language type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#main_file_uri GoogleBigqueryRoutine#main_file_uri}
        '''
        result = self._values.get("main_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Configuration properties as a set of key/value pairs, which will be passed on to the Spark application.

        For more information, see Apache Spark and the procedure option list.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#properties GoogleBigqueryRoutine#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def py_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Python files to be placed on the PYTHONPATH for PySpark application.

        Supported file types: .py, .egg, and .zip. For more information about Apache Spark, see Apache Spark.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#py_file_uris GoogleBigqueryRoutine#py_file_uris}
        '''
        result = self._values.get("py_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''Runtime version. If not specified, the default runtime version is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#runtime_version GoogleBigqueryRoutine#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryRoutineSparkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryRoutineSparkOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineSparkOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbec24ce9580bc756a4e729d60ec79a389c7847b8108b029f6a32367c3c6efdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetConnection")
    def reset_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnection", []))

    @jsii.member(jsii_name="resetContainerImage")
    def reset_container_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImage", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetJarUris")
    def reset_jar_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarUris", []))

    @jsii.member(jsii_name="resetMainClass")
    def reset_main_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainClass", []))

    @jsii.member(jsii_name="resetMainFileUri")
    def reset_main_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainFileUri", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetPyFileUris")
    def reset_py_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPyFileUris", []))

    @jsii.member(jsii_name="resetRuntimeVersion")
    def reset_runtime_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeVersion", []))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionInput")
    def connection_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="jarUrisInput")
    def jar_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="mainClassInput")
    def main_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainClassInput"))

    @builtins.property
    @jsii.member(jsii_name="mainFileUriInput")
    def main_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="pyFileUrisInput")
    def py_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pyFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f6a890366829a8ed664d9c98b316c23bafa7675f151ce5fb8c79db9241c357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connection"))

    @connection.setter
    def connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a5aa3e7aae3d7bdfc665d020116080a3b758814b9675002d7bfb896db0a252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerImage"))

    @container_image.setter
    def container_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911c716d4c60af8cba9227b02d40c769e4552c888c6ad6cc2e139d09d5ef1fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310ae2806b3b25895208ffe35b6706d2e838722ab907145d48ba3517077a611a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarUris")
    def jar_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarUris"))

    @jar_uris.setter
    def jar_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c335f352afd49f3ab5c50c10a4ef19fd7191c7bfcedbca4367b2a015159cce1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6969722909ec88deb2aaa0429fa36085d088bdab243acd2020751ee71df88559)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainFileUri")
    def main_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainFileUri"))

    @main_file_uri.setter
    def main_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0331dd73a323142479e58e09c0e8cc5be0445f25c989abe7f239d701e41d1af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d87e427caf468c747085d1b6c6db6230b101bed9e3fcea6e6c1009f3697e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pyFileUris")
    def py_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pyFileUris"))

    @py_file_uris.setter
    def py_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a033d8a35bfce059fbc6030195b3e6f59741e68e0c151252d87e9c3efbab3691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pyFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6f207ff7f1005708998793bcae71b6539a2dbd85977d1371e4f27f1fbe4b0b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleBigqueryRoutineSparkOptions]:
        return typing.cast(typing.Optional[GoogleBigqueryRoutineSparkOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleBigqueryRoutineSparkOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5f24b84338ff77cbeeed73ab82a6e3f53570cc46d95eb8cad6885fe66c44a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleBigqueryRoutineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#create GoogleBigqueryRoutine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#delete GoogleBigqueryRoutine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#update GoogleBigqueryRoutine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589bfe79609a250e4897e660e2162837f5daa0458b4667ddba62afe3c045c5fd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#create GoogleBigqueryRoutine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#delete GoogleBigqueryRoutine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_bigquery_routine#update GoogleBigqueryRoutine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleBigqueryRoutineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleBigqueryRoutineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleBigqueryRoutine.GoogleBigqueryRoutineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e91e9fecc227959c80d1404b889e1ab09c6fb7e7887b20a8cb97a9f938c90e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c1a751d0e62d5326ff8ddc7ab05dea6c577174384b5553ff58745ba48f5b23a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463f1bde25006dfc24e6f03f5ed0b2464a324ea3ea36fa20427fa9eae9d081f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d32a69b4323f145599a02d6590720d307bc0dd0c6a963294e6c6f7589940da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryRoutineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryRoutineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryRoutineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3db586ad987fe7e47b04f8074b82adc5be37d1992f9f313af9e12b106c5071f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleBigqueryRoutine",
    "GoogleBigqueryRoutineArguments",
    "GoogleBigqueryRoutineArgumentsList",
    "GoogleBigqueryRoutineArgumentsOutputReference",
    "GoogleBigqueryRoutineConfig",
    "GoogleBigqueryRoutineRemoteFunctionOptions",
    "GoogleBigqueryRoutineRemoteFunctionOptionsOutputReference",
    "GoogleBigqueryRoutineSparkOptions",
    "GoogleBigqueryRoutineSparkOptionsOutputReference",
    "GoogleBigqueryRoutineTimeouts",
    "GoogleBigqueryRoutineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__76baa773e48f67c1721de738decf39e94c4f1f78245e4f111a0cbab24e68c88d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_id: builtins.str,
    definition_body: builtins.str,
    routine_id: builtins.str,
    routine_type: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_governance_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    determinism_level: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
    language: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_function_options: typing.Optional[typing.Union[GoogleBigqueryRoutineRemoteFunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    return_table_type: typing.Optional[builtins.str] = None,
    return_type: typing.Optional[builtins.str] = None,
    security_mode: typing.Optional[builtins.str] = None,
    spark_options: typing.Optional[typing.Union[GoogleBigqueryRoutineSparkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryRoutineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8a39152f4aebba08c4d501d88ca816828bf8fc603be86228fa20adfa6d791e9b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021aa711a9dd8a24245e6b1352995c6a6115762168623d8b6ea5242427693f0b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__553cbc928e34c637a87e00adbaead88ba2d037e5bc491ebdf1855cd82d410f0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b55c3c6d3cc889163265877f12eed795a9e347addf9e08e3a6e629f259bf2936(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b37a6cbbafe9ea68f1ab9d4fb8701393e1a39cd0b8a664599d7f2eee855130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3965afb911726ed2c5e1367f69a6bd858c958de834913a8b2484861a590dcad3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2dcf6027012bbb1342523d874f4bbb5023e0e74da357b49637a4c5a4956f2c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac889d9b12346d8521c5d694528b32f82ea5b80754e7c13dde24a853e4493e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53afc1bbf5ed2bbdaaf8303f6fab337cd56008d70fa48f9525ee9c69bbe8715c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b662a0498fdfcf715fce340c2568ceb24e7484f1d2c6ed62877e6492a68cafc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5505e9c318a77d934007b3880fa6e712865a917cd22016790c50cfa7e4fca713(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d34662efef8dba5656e0b0f674ea9c47da8011b9157cdf4ca0df65c2397ad8a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec058399c64e693fb94473e176f411f7ee059c8c2d21529c8cb069901ef06c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93c83deb87b0e7cff70055277a5393e4921ed9209708df020bd5077c3f6339a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9cac2d93e40e8c157b3e91e58f0858735c8ce2156c7515e57792d17deac8b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024f846a8a9756de913222a2f988abbdc30590d19b3d7df1bf92a0c553833c24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62a46e0ba5999d79bd81faa325bf7c3c66ed90c2e668a81304f6be2e915928b(
    *,
    argument_kind: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb75acd5856cf5dcc2c23f4004d2fe632b83533ae48ce1da03675841de8a5b29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb938d1bd9c49efc75a7963243921bc60c8f2addb5d9a653e55cb9025b068990(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f376fd35f4ad1b2c79ee2858049e13b14b539708d18c5d8942a34a61e1a6ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3db89d3a39081f26effb4a9185be7329f9a0263327f03fbc29cb23a0b42d07c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbfbdc535fb080176e5bd6bb5c9de6e4a02975e14720b359d3b41963fc0120d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d358471e0d0c3100b0805aec9f05a62e6046d97d2f72dea49371615703e4000d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleBigqueryRoutineArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b1ad065dd6c98b1f5427eda2d04d60a2b3c09393b3e4852d4c070cb46510e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d44abf6e102283f319dd2bf7aaf0e0fbdeb8887a424d81bd9f833eb0d27b50e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a96899023786290ebccdf82f9270a829a37f889ba2a1c94b329893185ce209f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c5c0d67f7af22e93829c0415b6b5dad6f1f23cd986179eb92e85cdd1ff4760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff6e78e9fab589e2decff61c9e470ebcde4eb01cb27bf4d78feca001032c3071(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773b718e09108989a7f2c17dcefcad36d84f157a83ef9baab4a158121fff5d14(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryRoutineArguments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36f65d55167b638fe11b162b212bf4b43f3b85cfe0d4ed8b6c80bec8e7dd218(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dataset_id: builtins.str,
    definition_body: builtins.str,
    routine_id: builtins.str,
    routine_type: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleBigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_governance_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    determinism_level: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
    language: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_function_options: typing.Optional[typing.Union[GoogleBigqueryRoutineRemoteFunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    return_table_type: typing.Optional[builtins.str] = None,
    return_type: typing.Optional[builtins.str] = None,
    security_mode: typing.Optional[builtins.str] = None,
    spark_options: typing.Optional[typing.Union[GoogleBigqueryRoutineSparkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleBigqueryRoutineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7ff73a6bd2735a4322f764c19ebbdcf37d3879eb3fecdb77fc4c680013a5d7(
    *,
    connection: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    max_batching_rows: typing.Optional[builtins.str] = None,
    user_defined_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886e327f81e3fa0fc497e12904b4e2383a2def586ed22ce601a177ccb6fc450d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4010aa6dbaee132b99db84af5ecbfde6b31626fb4f4a1d02177d2f76879844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc31af4e98e2010c5ef6bc2bdbbc512003240e8badddbebacaa6f30f5e2ccada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f5b9b2c3ed6094b2313ed943c789493a27ec7f9f3a31aab109b6bc92083dee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd678cac9c9c0b7682b7df447c7246661ca0e38243b738c323e1a9798b9cc21(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39158f6ff322e5bb12dd06b6415c09b07057781ab406e758bd3ae5ab5153b2d(
    value: typing.Optional[GoogleBigqueryRoutineRemoteFunctionOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a650389e7651bf90d6e3b2eafbe82d87987839ef9d942bd030643ce356eb28(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection: typing.Optional[builtins.str] = None,
    container_image: typing.Optional[builtins.str] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    main_class: typing.Optional[builtins.str] = None,
    main_file_uri: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    py_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    runtime_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbec24ce9580bc756a4e729d60ec79a389c7847b8108b029f6a32367c3c6efdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f6a890366829a8ed664d9c98b316c23bafa7675f151ce5fb8c79db9241c357(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a5aa3e7aae3d7bdfc665d020116080a3b758814b9675002d7bfb896db0a252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911c716d4c60af8cba9227b02d40c769e4552c888c6ad6cc2e139d09d5ef1fd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310ae2806b3b25895208ffe35b6706d2e838722ab907145d48ba3517077a611a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c335f352afd49f3ab5c50c10a4ef19fd7191c7bfcedbca4367b2a015159cce1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6969722909ec88deb2aaa0429fa36085d088bdab243acd2020751ee71df88559(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0331dd73a323142479e58e09c0e8cc5be0445f25c989abe7f239d701e41d1af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d87e427caf468c747085d1b6c6db6230b101bed9e3fcea6e6c1009f3697e48(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a033d8a35bfce059fbc6030195b3e6f59741e68e0c151252d87e9c3efbab3691(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f207ff7f1005708998793bcae71b6539a2dbd85977d1371e4f27f1fbe4b0b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5f24b84338ff77cbeeed73ab82a6e3f53570cc46d95eb8cad6885fe66c44a4(
    value: typing.Optional[GoogleBigqueryRoutineSparkOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589bfe79609a250e4897e660e2162837f5daa0458b4667ddba62afe3c045c5fd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e91e9fecc227959c80d1404b889e1ab09c6fb7e7887b20a8cb97a9f938c90e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1a751d0e62d5326ff8ddc7ab05dea6c577174384b5553ff58745ba48f5b23a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463f1bde25006dfc24e6f03f5ed0b2464a324ea3ea36fa20427fa9eae9d081f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d32a69b4323f145599a02d6590720d307bc0dd0c6a963294e6c6f7589940da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3db586ad987fe7e47b04f8074b82adc5be37d1992f9f313af9e12b106c5071f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleBigqueryRoutineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_bigquery_routine`

Refer to the Terraform Registry for docs: [`google_bigquery_routine`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine).
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


class BigqueryRoutine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutine",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine google_bigquery_routine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        dataset_id: builtins.str,
        definition_body: builtins.str,
        routine_id: builtins.str,
        routine_type: builtins.str,
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryRoutineArguments", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_governance_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        determinism_level: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
        language: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_function_options: typing.Optional[typing.Union["BigqueryRoutineRemoteFunctionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        return_table_type: typing.Optional[builtins.str] = None,
        return_type: typing.Optional[builtins.str] = None,
        security_mode: typing.Optional[builtins.str] = None,
        spark_options: typing.Optional[typing.Union["BigqueryRoutineSparkOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigqueryRoutineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine google_bigquery_routine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param dataset_id: The ID of the dataset containing this routine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#dataset_id BigqueryRoutine#dataset_id}
        :param definition_body: The body of the routine. For functions, this is the expression in the AS clause. If language=SQL, it is the substring inside (but excluding) the parentheses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#definition_body BigqueryRoutine#definition_body}
        :param routine_id: The ID of the the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#routine_id BigqueryRoutine#routine_id}
        :param routine_type: The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#routine_type BigqueryRoutine#routine_type}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#arguments BigqueryRoutine#arguments}
        :param data_governance_type: If set to DATA_MASKING, the function is validated and made available as a masking function. For more information, see https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask Possible values: ["DATA_MASKING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#data_governance_type BigqueryRoutine#data_governance_type}
        :param description: The description of the routine if defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#description BigqueryRoutine#description}
        :param determinism_level: The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#determinism_level BigqueryRoutine#determinism_level}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#id BigqueryRoutine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imported_libraries: Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#imported_libraries BigqueryRoutine#imported_libraries}
        :param language: The language of the routine. Possible values: ["SQL", "JAVASCRIPT", "PYTHON", "JAVA", "SCALA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#language BigqueryRoutine#language}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#project BigqueryRoutine#project}.
        :param remote_function_options: remote_function_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#remote_function_options BigqueryRoutine#remote_function_options}
        :param return_table_type: Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION". If absent, the return table type is inferred from definitionBody at query time in each query that references this routine. If present, then the columns in the evaluated table result will be cast to match the column types specificed in return table type, at query time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#return_table_type BigqueryRoutine#return_table_type}
        :param return_type: A JSON schema for the return type. Optional if language = "SQL"; required otherwise. If absent, the return type is inferred from definitionBody at query time in each query that references this routine. If present, then the evaluated result will be cast to the specified returned type at query time. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switche d the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#return_type BigqueryRoutine#return_type}
        :param security_mode: Optional. The security mode of the routine, if defined. If not defined, the security mode is automatically determined from the routine's configuration. Possible values: ["DEFINER", "INVOKER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#security_mode BigqueryRoutine#security_mode}
        :param spark_options: spark_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#spark_options BigqueryRoutine#spark_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#timeouts BigqueryRoutine#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2907b22fd5759f80f01d9a798bd9243e19ca0351d15c29df9e7188765463bb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BigqueryRoutineConfig(
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
        '''Generates CDKTF code for importing a BigqueryRoutine resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BigqueryRoutine to import.
        :param import_from_id: The id of the existing BigqueryRoutine that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BigqueryRoutine to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c49646c407e8a29b1bb5b43a81283bb5b53dd54eb2755355dedbb59284e2192)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArguments")
    def put_arguments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BigqueryRoutineArguments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2f7b7e522041c1c1697cfcfa536631bc1cfa7a3cabacfb64101917df161953)
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
        :param connection: Fully qualified name of the user-provided connection object which holds the authentication information to send requests to the remote service. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#connection BigqueryRoutine#connection}
        :param endpoint: Endpoint of the user-provided remote service, e.g. 'https://us-east1-my_gcf_project.cloudfunctions.net/remote_add'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#endpoint BigqueryRoutine#endpoint}
        :param max_batching_rows: Max number of rows in each batch sent to the remote service. If absent or if 0, BigQuery dynamically decides the number of rows in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#max_batching_rows BigqueryRoutine#max_batching_rows}
        :param user_defined_context: User-defined context as a set of key/value pairs, which will be sent as function invocation context together with batched arguments in the requests to the remote service. The total number of bytes of keys and values must be less than 8KB. An object containing a list of "key": value pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#user_defined_context BigqueryRoutine#user_defined_context}
        '''
        value = BigqueryRoutineRemoteFunctionOptions(
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
        :param archive_uris: Archive files to be extracted into the working directory of each executor. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#archive_uris BigqueryRoutine#archive_uris}
        :param connection: Fully qualified name of the user-provided Spark connection object. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#connection BigqueryRoutine#connection}
        :param container_image: Custom container image for the runtime environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#container_image BigqueryRoutine#container_image}
        :param file_uris: Files to be placed in the working directory of each executor. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#file_uris BigqueryRoutine#file_uris}
        :param jar_uris: JARs to include on the driver and executor CLASSPATH. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#jar_uris BigqueryRoutine#jar_uris}
        :param main_class: The fully qualified name of a class in jarUris, for example, com.example.wordcount. Exactly one of mainClass and main_jar_uri field should be set for Java/Scala language type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#main_class BigqueryRoutine#main_class}
        :param main_file_uri: The main file/jar URI of the Spark application. Exactly one of the definitionBody field and the mainFileUri field must be set for Python. Exactly one of mainClass and mainFileUri field should be set for Java/Scala language type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#main_file_uri BigqueryRoutine#main_file_uri}
        :param properties: Configuration properties as a set of key/value pairs, which will be passed on to the Spark application. For more information, see Apache Spark and the procedure option list. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#properties BigqueryRoutine#properties}
        :param py_file_uris: Python files to be placed on the PYTHONPATH for PySpark application. Supported file types: .py, .egg, and .zip. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#py_file_uris BigqueryRoutine#py_file_uris}
        :param runtime_version: Runtime version. If not specified, the default runtime version is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#runtime_version BigqueryRoutine#runtime_version}
        '''
        value = BigqueryRoutineSparkOptions(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#create BigqueryRoutine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#delete BigqueryRoutine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#update BigqueryRoutine#update}.
        '''
        value = BigqueryRoutineTimeouts(create=create, delete=delete, update=update)

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
    def arguments(self) -> "BigqueryRoutineArgumentsList":
        return typing.cast("BigqueryRoutineArgumentsList", jsii.get(self, "arguments"))

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
    ) -> "BigqueryRoutineRemoteFunctionOptionsOutputReference":
        return typing.cast("BigqueryRoutineRemoteFunctionOptionsOutputReference", jsii.get(self, "remoteFunctionOptions"))

    @builtins.property
    @jsii.member(jsii_name="sparkOptions")
    def spark_options(self) -> "BigqueryRoutineSparkOptionsOutputReference":
        return typing.cast("BigqueryRoutineSparkOptionsOutputReference", jsii.get(self, "sparkOptions"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BigqueryRoutineTimeoutsOutputReference":
        return typing.cast("BigqueryRoutineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="argumentsInput")
    def arguments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryRoutineArguments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BigqueryRoutineArguments"]]], jsii.get(self, "argumentsInput"))

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
    ) -> typing.Optional["BigqueryRoutineRemoteFunctionOptions"]:
        return typing.cast(typing.Optional["BigqueryRoutineRemoteFunctionOptions"], jsii.get(self, "remoteFunctionOptionsInput"))

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
    def spark_options_input(self) -> typing.Optional["BigqueryRoutineSparkOptions"]:
        return typing.cast(typing.Optional["BigqueryRoutineSparkOptions"], jsii.get(self, "sparkOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryRoutineTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BigqueryRoutineTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataGovernanceType")
    def data_governance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataGovernanceType"))

    @data_governance_type.setter
    def data_governance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c081a6cf384ba84de43a351c057546dfdefacc98386d18f08858209f970a510)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataGovernanceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "datasetId"))

    @dataset_id.setter
    def dataset_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cff6501d249d313195601eb0155a486bc666a5130267ed188b34597a9120d80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "datasetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="definitionBody")
    def definition_body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "definitionBody"))

    @definition_body.setter
    def definition_body(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dc1a7651b96c5805768f65a324ea3fe93b73bec617531eb89306824fed756f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionBody", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1fe9fce40933e824b293541ae4dbf9c7a6ff9b60a5124e9e520b694d75863a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="determinismLevel")
    def determinism_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "determinismLevel"))

    @determinism_level.setter
    def determinism_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c06c0054e7c9287f11395cd43c2831b2490713e5d9218d8673782c56513f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "determinismLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b9ae5cedf8ed9cf1237b3cdafba9e13758ee2969944857ba0b924094b18480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importedLibraries")
    def imported_libraries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "importedLibraries"))

    @imported_libraries.setter
    def imported_libraries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ca70e3ab22159138a552ed5dfab0ad617a9f2c90486d548d639355521234316)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importedLibraries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @language.setter
    def language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb466cec21a70820e16993f74aaa4fc83135e8c435d324743de5fd62cec3c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "language", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea935470f466b88c554aa3a1c68c913ad61210ae9f767d0983dbe1a9791020d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnTableType")
    def return_table_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnTableType"))

    @return_table_type.setter
    def return_table_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f386d1f2a423fa4f83385360c86c5f2f668863c7ef569e4ab10bbf596eb7ce86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnTableType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="returnType")
    def return_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "returnType"))

    @return_type.setter
    def return_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19dcd29628a6e63a26bcdf14d68286ed8d81823633606bf61ef5e4d9136ce45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routineId")
    def routine_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routineId"))

    @routine_id.setter
    def routine_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef251932690f5699123951b0376e05d9a98d1d93e562668d7157209fc0c994eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routineId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routineType")
    def routine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routineType"))

    @routine_type.setter
    def routine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa97bed511a2af66722dec9a27b5d425c27c91b732d681081a1f23b34d4f627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityMode")
    def security_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityMode"))

    @security_mode.setter
    def security_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c276058afec1b90e63445989ba84a6e913cec21cee87849ac070a8e2e1d281e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityMode", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineArguments",
    jsii_struct_bases=[],
    name_mapping={
        "argument_kind": "argumentKind",
        "data_type": "dataType",
        "mode": "mode",
        "name": "name",
    },
)
class BigqueryRoutineArguments:
    def __init__(
        self,
        *,
        argument_kind: typing.Optional[builtins.str] = None,
        data_type: typing.Optional[builtins.str] = None,
        mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param argument_kind: Defaults to FIXED_TYPE. Default value: "FIXED_TYPE" Possible values: ["FIXED_TYPE", "ANY_TYPE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#argument_kind BigqueryRoutine#argument_kind}
        :param data_type: A JSON schema for the data type. Required unless argumentKind = ANY_TYPE. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switched the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#data_type BigqueryRoutine#data_type}
        :param mode: Specifies whether the argument is input or output. Can be set for procedures only. Possible values: ["IN", "OUT", "INOUT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#mode BigqueryRoutine#mode}
        :param name: The name of this argument. Can be absent for function return argument. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#name BigqueryRoutine#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4093181fcf2153183e3c0bb280c5a75c627cf219dbf5a94805810747de6b863)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#argument_kind BigqueryRoutine#argument_kind}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#data_type BigqueryRoutine#data_type}
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the argument is input or output. Can be set for procedures only. Possible values: ["IN", "OUT", "INOUT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#mode BigqueryRoutine#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this argument. Can be absent for function return argument.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#name BigqueryRoutine#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryRoutineArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryRoutineArgumentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineArgumentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__394f50ac062eae259f62e3cbec03f7fde8dd3d23be78d901e287170529947e1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BigqueryRoutineArgumentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daae335688e57a471d89556aac00b4b5cf4c19a9afe75d383ca3ce12f7a3903f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BigqueryRoutineArgumentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b1d97fe5dcaa34a14a26f60c631b2d04d0c78c3fd8c770b7bb32761a9e1c88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de12b0d1762dc09778b15d6b66c4c60887babdf9f8ae36eafaeb5e756a973ca7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2096fea36d81f589dd47424fd3cb36078fbd62420a6383edd8094b201495e335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0643f02e04976e372885b752322a8ae556fb84b0bf559994f30cc27fc0c071a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class BigqueryRoutineArgumentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineArgumentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e17216ae6df5d3ea3c19c330c5e2219ed23f41176b34c2c53a50bcf9de21d90c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ded13f20c2b223b64d2dfae878c44f9a29e733d93854d49c132d5dccfaea324c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "argumentKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataType")
    def data_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataType"))

    @data_type.setter
    def data_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d006d33913b888ff2345034d41cce0fe63cc1343f413b28c7d63bd33c2e092)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a97a429799e3e11213d26274d23df35684697c2081f208e335c294dd593a5f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40aba7b888b901d13374dcc479a4fae84b493840563d353e3ad6f5b8c491f64b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryRoutineArguments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryRoutineArguments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryRoutineArguments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8045903ed5067a0787eeca695263f314090aa68a4c8713116caf2d0b6166418a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineConfig",
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
class BigqueryRoutineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_governance_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        determinism_level: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
        language: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        remote_function_options: typing.Optional[typing.Union["BigqueryRoutineRemoteFunctionOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        return_table_type: typing.Optional[builtins.str] = None,
        return_type: typing.Optional[builtins.str] = None,
        security_mode: typing.Optional[builtins.str] = None,
        spark_options: typing.Optional[typing.Union["BigqueryRoutineSparkOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["BigqueryRoutineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param dataset_id: The ID of the dataset containing this routine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#dataset_id BigqueryRoutine#dataset_id}
        :param definition_body: The body of the routine. For functions, this is the expression in the AS clause. If language=SQL, it is the substring inside (but excluding) the parentheses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#definition_body BigqueryRoutine#definition_body}
        :param routine_id: The ID of the the routine. The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#routine_id BigqueryRoutine#routine_id}
        :param routine_type: The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#routine_type BigqueryRoutine#routine_type}
        :param arguments: arguments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#arguments BigqueryRoutine#arguments}
        :param data_governance_type: If set to DATA_MASKING, the function is validated and made available as a masking function. For more information, see https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask Possible values: ["DATA_MASKING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#data_governance_type BigqueryRoutine#data_governance_type}
        :param description: The description of the routine if defined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#description BigqueryRoutine#description}
        :param determinism_level: The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#determinism_level BigqueryRoutine#determinism_level}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#id BigqueryRoutine#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param imported_libraries: Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#imported_libraries BigqueryRoutine#imported_libraries}
        :param language: The language of the routine. Possible values: ["SQL", "JAVASCRIPT", "PYTHON", "JAVA", "SCALA"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#language BigqueryRoutine#language}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#project BigqueryRoutine#project}.
        :param remote_function_options: remote_function_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#remote_function_options BigqueryRoutine#remote_function_options}
        :param return_table_type: Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION". If absent, the return table type is inferred from definitionBody at query time in each query that references this routine. If present, then the columns in the evaluated table result will be cast to match the column types specificed in return table type, at query time. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#return_table_type BigqueryRoutine#return_table_type}
        :param return_type: A JSON schema for the return type. Optional if language = "SQL"; required otherwise. If absent, the return type is inferred from definitionBody at query time in each query that references this routine. If present, then the evaluated result will be cast to the specified returned type at query time. ~>**NOTE**: Because this field expects a JSON string, any changes to the string will create a diff, even if the JSON itself hasn't changed. If the API returns a different value for the same schema, e.g. it switche d the order of values or replaced STRUCT field type with RECORD field type, we currently cannot suppress the recurring diff this causes. As a workaround, we recommend using the schema as returned by the API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#return_type BigqueryRoutine#return_type}
        :param security_mode: Optional. The security mode of the routine, if defined. If not defined, the security mode is automatically determined from the routine's configuration. Possible values: ["DEFINER", "INVOKER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#security_mode BigqueryRoutine#security_mode}
        :param spark_options: spark_options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#spark_options BigqueryRoutine#spark_options}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#timeouts BigqueryRoutine#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(remote_function_options, dict):
            remote_function_options = BigqueryRoutineRemoteFunctionOptions(**remote_function_options)
        if isinstance(spark_options, dict):
            spark_options = BigqueryRoutineSparkOptions(**spark_options)
        if isinstance(timeouts, dict):
            timeouts = BigqueryRoutineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5867934d3302d0c9e8d42e3e8b8cde5ee6b6c0909bdc5cfb590963f5e45bc1c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#dataset_id BigqueryRoutine#dataset_id}
        '''
        result = self._values.get("dataset_id")
        assert result is not None, "Required property 'dataset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def definition_body(self) -> builtins.str:
        '''The body of the routine.

        For functions, this is the expression in the AS clause.
        If language=SQL, it is the substring inside (but excluding) the parentheses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#definition_body BigqueryRoutine#definition_body}
        '''
        result = self._values.get("definition_body")
        assert result is not None, "Required property 'definition_body' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routine_id(self) -> builtins.str:
        '''The ID of the the routine.

        The ID must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_). The maximum length is 256 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#routine_id BigqueryRoutine#routine_id}
        '''
        result = self._values.get("routine_id")
        assert result is not None, "Required property 'routine_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def routine_type(self) -> builtins.str:
        '''The type of routine. Possible values: ["SCALAR_FUNCTION", "PROCEDURE", "TABLE_VALUED_FUNCTION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#routine_type BigqueryRoutine#routine_type}
        '''
        result = self._values.get("routine_type")
        assert result is not None, "Required property 'routine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]]:
        '''arguments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#arguments BigqueryRoutine#arguments}
        '''
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]], result)

    @builtins.property
    def data_governance_type(self) -> typing.Optional[builtins.str]:
        '''If set to DATA_MASKING, the function is validated and made available as a masking function.

        For more information, see https://cloud.google.com/bigquery/docs/user-defined-functions#custom-mask Possible values: ["DATA_MASKING"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#data_governance_type BigqueryRoutine#data_governance_type}
        '''
        result = self._values.get("data_governance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the routine if defined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#description BigqueryRoutine#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def determinism_level(self) -> typing.Optional[builtins.str]:
        '''The determinism level of the JavaScript UDF if defined. Possible values: ["DETERMINISM_LEVEL_UNSPECIFIED", "DETERMINISTIC", "NOT_DETERMINISTIC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#determinism_level BigqueryRoutine#determinism_level}
        '''
        result = self._values.get("determinism_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#id BigqueryRoutine#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imported_libraries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. If language = "JAVASCRIPT", this field stores the path of the imported JAVASCRIPT libraries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#imported_libraries BigqueryRoutine#imported_libraries}
        '''
        result = self._values.get("imported_libraries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''The language of the routine. Possible values: ["SQL", "JAVASCRIPT", "PYTHON", "JAVA", "SCALA"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#language BigqueryRoutine#language}
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#project BigqueryRoutine#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_function_options(
        self,
    ) -> typing.Optional["BigqueryRoutineRemoteFunctionOptions"]:
        '''remote_function_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#remote_function_options BigqueryRoutine#remote_function_options}
        '''
        result = self._values.get("remote_function_options")
        return typing.cast(typing.Optional["BigqueryRoutineRemoteFunctionOptions"], result)

    @builtins.property
    def return_table_type(self) -> typing.Optional[builtins.str]:
        '''Optional. Can be set only if routineType = "TABLE_VALUED_FUNCTION".

        If absent, the return table type is inferred from definitionBody at query time in each query
        that references this routine. If present, then the columns in the evaluated table result will
        be cast to match the column types specificed in return table type, at query time.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#return_table_type BigqueryRoutine#return_table_type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#return_type BigqueryRoutine#return_type}
        '''
        result = self._values.get("return_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_mode(self) -> typing.Optional[builtins.str]:
        '''Optional.

        The security mode of the routine, if defined. If not defined, the security mode is automatically determined from the routine's configuration. Possible values: ["DEFINER", "INVOKER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#security_mode BigqueryRoutine#security_mode}
        '''
        result = self._values.get("security_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_options(self) -> typing.Optional["BigqueryRoutineSparkOptions"]:
        '''spark_options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#spark_options BigqueryRoutine#spark_options}
        '''
        result = self._values.get("spark_options")
        return typing.cast(typing.Optional["BigqueryRoutineSparkOptions"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BigqueryRoutineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#timeouts BigqueryRoutine#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BigqueryRoutineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryRoutineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineRemoteFunctionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "connection": "connection",
        "endpoint": "endpoint",
        "max_batching_rows": "maxBatchingRows",
        "user_defined_context": "userDefinedContext",
    },
)
class BigqueryRoutineRemoteFunctionOptions:
    def __init__(
        self,
        *,
        connection: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        max_batching_rows: typing.Optional[builtins.str] = None,
        user_defined_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: Fully qualified name of the user-provided connection object which holds the authentication information to send requests to the remote service. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}" Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#connection BigqueryRoutine#connection}
        :param endpoint: Endpoint of the user-provided remote service, e.g. 'https://us-east1-my_gcf_project.cloudfunctions.net/remote_add'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#endpoint BigqueryRoutine#endpoint}
        :param max_batching_rows: Max number of rows in each batch sent to the remote service. If absent or if 0, BigQuery dynamically decides the number of rows in a batch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#max_batching_rows BigqueryRoutine#max_batching_rows}
        :param user_defined_context: User-defined context as a set of key/value pairs, which will be sent as function invocation context together with batched arguments in the requests to the remote service. The total number of bytes of keys and values must be less than 8KB. An object containing a list of "key": value pairs. Example: '{ "name": "wrench", "mass": "1.3kg", "count": "3" }'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#user_defined_context BigqueryRoutine#user_defined_context}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5aa719c5a74b8831bb094e730d9f0b031b660c573a5419fba687eed274316c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#connection BigqueryRoutine#connection}
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Endpoint of the user-provided remote service, e.g. 'https://us-east1-my_gcf_project.cloudfunctions.net/remote_add'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#endpoint BigqueryRoutine#endpoint}
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_batching_rows(self) -> typing.Optional[builtins.str]:
        '''Max number of rows in each batch sent to the remote service.

        If absent or if 0,
        BigQuery dynamically decides the number of rows in a batch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#max_batching_rows BigqueryRoutine#max_batching_rows}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#user_defined_context BigqueryRoutine#user_defined_context}
        '''
        result = self._values.get("user_defined_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryRoutineRemoteFunctionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryRoutineRemoteFunctionOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineRemoteFunctionOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60e1975cae8ef399f92fd97643f86ba329c1d5df2e2fdf91e17547cd2304da99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0dc8d22045e067237330d142d2b5af33a265262d395021dfb9c34d864eae7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57a52a3daee769cd4cbfc9214cc855d37b771db13bf6715ea9a18dd54a32421)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxBatchingRows")
    def max_batching_rows(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxBatchingRows"))

    @max_batching_rows.setter
    def max_batching_rows(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1fbbfc5d94c019120e82a2e546ead316de9229006943aed4777a2fb910d334)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87ae46adbc2ccc6d3b5dd24c39faaafdaba64c7697aaf63f3b04ab9c0d1387ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userDefinedContext", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryRoutineRemoteFunctionOptions]:
        return typing.cast(typing.Optional[BigqueryRoutineRemoteFunctionOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryRoutineRemoteFunctionOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1dac499296cd4adcd04ba1de2e7fbbe645db71b27c73aa99199ec9c8e6e24ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineSparkOptions",
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
class BigqueryRoutineSparkOptions:
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
        :param archive_uris: Archive files to be extracted into the working directory of each executor. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#archive_uris BigqueryRoutine#archive_uris}
        :param connection: Fully qualified name of the user-provided Spark connection object. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#connection BigqueryRoutine#connection}
        :param container_image: Custom container image for the runtime environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#container_image BigqueryRoutine#container_image}
        :param file_uris: Files to be placed in the working directory of each executor. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#file_uris BigqueryRoutine#file_uris}
        :param jar_uris: JARs to include on the driver and executor CLASSPATH. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#jar_uris BigqueryRoutine#jar_uris}
        :param main_class: The fully qualified name of a class in jarUris, for example, com.example.wordcount. Exactly one of mainClass and main_jar_uri field should be set for Java/Scala language type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#main_class BigqueryRoutine#main_class}
        :param main_file_uri: The main file/jar URI of the Spark application. Exactly one of the definitionBody field and the mainFileUri field must be set for Python. Exactly one of mainClass and mainFileUri field should be set for Java/Scala language type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#main_file_uri BigqueryRoutine#main_file_uri}
        :param properties: Configuration properties as a set of key/value pairs, which will be passed on to the Spark application. For more information, see Apache Spark and the procedure option list. An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#properties BigqueryRoutine#properties}
        :param py_file_uris: Python files to be placed on the PYTHONPATH for PySpark application. Supported file types: .py, .egg, and .zip. For more information about Apache Spark, see Apache Spark. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#py_file_uris BigqueryRoutine#py_file_uris}
        :param runtime_version: Runtime version. If not specified, the default runtime version is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#runtime_version BigqueryRoutine#runtime_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b97d571d0bf6779e8d3ee4f1aee65931607c05686ede411c09f05b67e5ed0b7a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#archive_uris BigqueryRoutine#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection(self) -> typing.Optional[builtins.str]:
        '''Fully qualified name of the user-provided Spark connection object. Format: "projects/{projectId}/locations/{locationId}/connections/{connectionId}".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#connection BigqueryRoutine#connection}
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_image(self) -> typing.Optional[builtins.str]:
        '''Custom container image for the runtime environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#container_image BigqueryRoutine#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Files to be placed in the working directory of each executor.

        For more information about Apache Spark, see Apache Spark.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#file_uris BigqueryRoutine#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''JARs to include on the driver and executor CLASSPATH. For more information about Apache Spark, see Apache Spark.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#jar_uris BigqueryRoutine#jar_uris}
        '''
        result = self._values.get("jar_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The fully qualified name of a class in jarUris, for example, com.example.wordcount. Exactly one of mainClass and main_jar_uri field should be set for Java/Scala language type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#main_class BigqueryRoutine#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_file_uri(self) -> typing.Optional[builtins.str]:
        '''The main file/jar URI of the Spark application.

        Exactly one of the definitionBody field and the mainFileUri field must be set for Python.
        Exactly one of mainClass and mainFileUri field should be set for Java/Scala language type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#main_file_uri BigqueryRoutine#main_file_uri}
        '''
        result = self._values.get("main_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Configuration properties as a set of key/value pairs, which will be passed on to the Spark application.

        For more information, see Apache Spark and the procedure option list.
        An object containing a list of "key": value pairs. Example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#properties BigqueryRoutine#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def py_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Python files to be placed on the PYTHONPATH for PySpark application.

        Supported file types: .py, .egg, and .zip. For more information about Apache Spark, see Apache Spark.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#py_file_uris BigqueryRoutine#py_file_uris}
        '''
        result = self._values.get("py_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''Runtime version. If not specified, the default runtime version is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#runtime_version BigqueryRoutine#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryRoutineSparkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryRoutineSparkOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineSparkOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a180a36ab2bff804ea370e8ee4be6db4df85c3f763f4b3fc2bb4781942cb1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ef536a8d7751753afe67e0442550140c1dd76d8613dba7e26e74a5500e23dc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connection"))

    @connection.setter
    def connection(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad294945e0b08160a8ac47975c866b7b43032f6ed50dbf67670f9d302a75d27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerImage"))

    @container_image.setter
    def container_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5e0994ad9391ad3ecbd45bca10eae9ee5b9f8d39d47a2052160cffba6d37b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2ed698fe67e36459af504b5cc135676fcc99edc9f19a45be6d42aebe2a0a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarUris")
    def jar_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarUris"))

    @jar_uris.setter
    def jar_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ba40954bb0a4bc8f7b040849ff49dd7a83f7200794e13d8626ecf3feccbc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fa8c2facc608dc580669d9467c7dd1a280582c8eacba996f6c9a6e2eaeeb1e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainFileUri")
    def main_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainFileUri"))

    @main_file_uri.setter
    def main_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4920ec4acd5d3a1afb5ccacb6137a506a6039e303ef358229ded7fe61d9de00b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0d41271b2ba9295bf5cfd35a79b09631594aa19b06f5a6c84bdca82b50df3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pyFileUris")
    def py_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pyFileUris"))

    @py_file_uris.setter
    def py_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf5b6c6a882b038fc984b1fe70da6cdb06acf523a3bb95ab36408d6be87cf9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pyFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809666a8c0b3deb0a61fd118e23eb5b97390ac76dcf93210ac384305fd010ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[BigqueryRoutineSparkOptions]:
        return typing.cast(typing.Optional[BigqueryRoutineSparkOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[BigqueryRoutineSparkOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9fef3a061e1ba5cd3314cd66cd5db7aa81c39b6f2cc8b3af255d21854f3bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class BigqueryRoutineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#create BigqueryRoutine#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#delete BigqueryRoutine#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#update BigqueryRoutine#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e618f69c17f3c34395c5961a6bb52fe58f02eb8a4f6aa4e15914d9aab1126b36)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#create BigqueryRoutine#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#delete BigqueryRoutine#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/bigquery_routine#update BigqueryRoutine#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BigqueryRoutineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BigqueryRoutineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.bigqueryRoutine.BigqueryRoutineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f417a409e286a0657c58b14103f0e825579b71849e59e2e9c2561f03b0dae7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f49832ac97c7792c9b6e8a089deecb0abc521777bf908f63d8554d8527f5364d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f183c21ee83c902ca1e36da441d035a3f526cb4e637b3e9a1d1990192aa52a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee97ad1a1bdba96b955a3ec3490a29b43651d4a7e08e366dfb221c357700c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryRoutineTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryRoutineTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryRoutineTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fe6991b9e5283efbe33558311dd2aba87f477b3cceef104ec5e7f139e9829e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BigqueryRoutine",
    "BigqueryRoutineArguments",
    "BigqueryRoutineArgumentsList",
    "BigqueryRoutineArgumentsOutputReference",
    "BigqueryRoutineConfig",
    "BigqueryRoutineRemoteFunctionOptions",
    "BigqueryRoutineRemoteFunctionOptionsOutputReference",
    "BigqueryRoutineSparkOptions",
    "BigqueryRoutineSparkOptionsOutputReference",
    "BigqueryRoutineTimeouts",
    "BigqueryRoutineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__d2907b22fd5759f80f01d9a798bd9243e19ca0351d15c29df9e7188765463bb2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    dataset_id: builtins.str,
    definition_body: builtins.str,
    routine_id: builtins.str,
    routine_type: builtins.str,
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_governance_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    determinism_level: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
    language: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_function_options: typing.Optional[typing.Union[BigqueryRoutineRemoteFunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    return_table_type: typing.Optional[builtins.str] = None,
    return_type: typing.Optional[builtins.str] = None,
    security_mode: typing.Optional[builtins.str] = None,
    spark_options: typing.Optional[typing.Union[BigqueryRoutineSparkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigqueryRoutineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1c49646c407e8a29b1bb5b43a81283bb5b53dd54eb2755355dedbb59284e2192(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2f7b7e522041c1c1697cfcfa536631bc1cfa7a3cabacfb64101917df161953(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c081a6cf384ba84de43a351c057546dfdefacc98386d18f08858209f970a510(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cff6501d249d313195601eb0155a486bc666a5130267ed188b34597a9120d80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dc1a7651b96c5805768f65a324ea3fe93b73bec617531eb89306824fed756f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1fe9fce40933e824b293541ae4dbf9c7a6ff9b60a5124e9e520b694d75863a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c06c0054e7c9287f11395cd43c2831b2490713e5d9218d8673782c56513f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b9ae5cedf8ed9cf1237b3cdafba9e13758ee2969944857ba0b924094b18480(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca70e3ab22159138a552ed5dfab0ad617a9f2c90486d548d639355521234316(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb466cec21a70820e16993f74aaa4fc83135e8c435d324743de5fd62cec3c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea935470f466b88c554aa3a1c68c913ad61210ae9f767d0983dbe1a9791020d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f386d1f2a423fa4f83385360c86c5f2f668863c7ef569e4ab10bbf596eb7ce86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19dcd29628a6e63a26bcdf14d68286ed8d81823633606bf61ef5e4d9136ce45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef251932690f5699123951b0376e05d9a98d1d93e562668d7157209fc0c994eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa97bed511a2af66722dec9a27b5d425c27c91b732d681081a1f23b34d4f627(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c276058afec1b90e63445989ba84a6e913cec21cee87849ac070a8e2e1d281e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4093181fcf2153183e3c0bb280c5a75c627cf219dbf5a94805810747de6b863(
    *,
    argument_kind: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394f50ac062eae259f62e3cbec03f7fde8dd3d23be78d901e287170529947e1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daae335688e57a471d89556aac00b4b5cf4c19a9afe75d383ca3ce12f7a3903f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b1d97fe5dcaa34a14a26f60c631b2d04d0c78c3fd8c770b7bb32761a9e1c88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de12b0d1762dc09778b15d6b66c4c60887babdf9f8ae36eafaeb5e756a973ca7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2096fea36d81f589dd47424fd3cb36078fbd62420a6383edd8094b201495e335(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0643f02e04976e372885b752322a8ae556fb84b0bf559994f30cc27fc0c071a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BigqueryRoutineArguments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e17216ae6df5d3ea3c19c330c5e2219ed23f41176b34c2c53a50bcf9de21d90c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded13f20c2b223b64d2dfae878c44f9a29e733d93854d49c132d5dccfaea324c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d006d33913b888ff2345034d41cce0fe63cc1343f413b28c7d63bd33c2e092(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a97a429799e3e11213d26274d23df35684697c2081f208e335c294dd593a5f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40aba7b888b901d13374dcc479a4fae84b493840563d353e3ad6f5b8c491f64b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8045903ed5067a0787eeca695263f314090aa68a4c8713116caf2d0b6166418a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryRoutineArguments]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5867934d3302d0c9e8d42e3e8b8cde5ee6b6c0909bdc5cfb590963f5e45bc1c(
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
    arguments: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BigqueryRoutineArguments, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_governance_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    determinism_level: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    imported_libraries: typing.Optional[typing.Sequence[builtins.str]] = None,
    language: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    remote_function_options: typing.Optional[typing.Union[BigqueryRoutineRemoteFunctionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    return_table_type: typing.Optional[builtins.str] = None,
    return_type: typing.Optional[builtins.str] = None,
    security_mode: typing.Optional[builtins.str] = None,
    spark_options: typing.Optional[typing.Union[BigqueryRoutineSparkOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[BigqueryRoutineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5aa719c5a74b8831bb094e730d9f0b031b660c573a5419fba687eed274316c(
    *,
    connection: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    max_batching_rows: typing.Optional[builtins.str] = None,
    user_defined_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60e1975cae8ef399f92fd97643f86ba329c1d5df2e2fdf91e17547cd2304da99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dc8d22045e067237330d142d2b5af33a265262d395021dfb9c34d864eae7c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57a52a3daee769cd4cbfc9214cc855d37b771db13bf6715ea9a18dd54a32421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1fbbfc5d94c019120e82a2e546ead316de9229006943aed4777a2fb910d334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ae46adbc2ccc6d3b5dd24c39faaafdaba64c7697aaf63f3b04ab9c0d1387ca(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1dac499296cd4adcd04ba1de2e7fbbe645db71b27c73aa99199ec9c8e6e24ef(
    value: typing.Optional[BigqueryRoutineRemoteFunctionOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97d571d0bf6779e8d3ee4f1aee65931607c05686ede411c09f05b67e5ed0b7a(
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

def _typecheckingstub__74a180a36ab2bff804ea370e8ee4be6db4df85c3f763f4b3fc2bb4781942cb1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef536a8d7751753afe67e0442550140c1dd76d8613dba7e26e74a5500e23dc4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad294945e0b08160a8ac47975c866b7b43032f6ed50dbf67670f9d302a75d27a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5e0994ad9391ad3ecbd45bca10eae9ee5b9f8d39d47a2052160cffba6d37b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2ed698fe67e36459af504b5cc135676fcc99edc9f19a45be6d42aebe2a0a7e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ba40954bb0a4bc8f7b040849ff49dd7a83f7200794e13d8626ecf3feccbc20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa8c2facc608dc580669d9467c7dd1a280582c8eacba996f6c9a6e2eaeeb1e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4920ec4acd5d3a1afb5ccacb6137a506a6039e303ef358229ded7fe61d9de00b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0d41271b2ba9295bf5cfd35a79b09631594aa19b06f5a6c84bdca82b50df3e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf5b6c6a882b038fc984b1fe70da6cdb06acf523a3bb95ab36408d6be87cf9e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809666a8c0b3deb0a61fd118e23eb5b97390ac76dcf93210ac384305fd010ed6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9fef3a061e1ba5cd3314cd66cd5db7aa81c39b6f2cc8b3af255d21854f3bde(
    value: typing.Optional[BigqueryRoutineSparkOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e618f69c17f3c34395c5961a6bb52fe58f02eb8a4f6aa4e15914d9aab1126b36(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f417a409e286a0657c58b14103f0e825579b71849e59e2e9c2561f03b0dae7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49832ac97c7792c9b6e8a089deecb0abc521777bf908f63d8554d8527f5364d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f183c21ee83c902ca1e36da441d035a3f526cb4e637b3e9a1d1990192aa52a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee97ad1a1bdba96b955a3ec3490a29b43651d4a7e08e366dfb221c357700c79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fe6991b9e5283efbe33558311dd2aba87f477b3cceef104ec5e7f139e9829e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BigqueryRoutineTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

r'''
# `google_dataproc_batch`

Refer to the Terraform Registry for docs: [`google_dataproc_batch`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch).
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


class GoogleDataprocBatch(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatch",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch google_dataproc_batch}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        batch_id: typing.Optional[builtins.str] = None,
        environment_config: typing.Optional[typing.Union["GoogleDataprocBatchEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        pyspark_batch: typing.Optional[typing.Union["GoogleDataprocBatchPysparkBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_config: typing.Optional[typing.Union["GoogleDataprocBatchRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_batch: typing.Optional[typing.Union["GoogleDataprocBatchSparkBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_batch: typing.Optional[typing.Union["GoogleDataprocBatchSparkRBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_batch: typing.Optional[typing.Union["GoogleDataprocBatchSparkSqlBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocBatchTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch google_dataproc_batch} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param batch_id: The ID to use for the batch, which will become the final component of the batch's resource name. This value must be 4-63 characters. Valid characters are /[a-z][0-9]-/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#batch_id GoogleDataprocBatch#batch_id}
        :param environment_config: environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#environment_config GoogleDataprocBatch#environment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#id GoogleDataprocBatch#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this batch. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#labels GoogleDataprocBatch#labels}
        :param location: The location in which the batch will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#location GoogleDataprocBatch#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#project GoogleDataprocBatch#project}.
        :param pyspark_batch: pyspark_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#pyspark_batch GoogleDataprocBatch#pyspark_batch}
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#runtime_config GoogleDataprocBatch#runtime_config}
        :param spark_batch: spark_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_batch GoogleDataprocBatch#spark_batch}
        :param spark_r_batch: spark_r_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_r_batch GoogleDataprocBatch#spark_r_batch}
        :param spark_sql_batch: spark_sql_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_sql_batch GoogleDataprocBatch#spark_sql_batch}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#timeouts GoogleDataprocBatch#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dee516aa821d1c4dfb7c6b9c0463a1990e8b7511f475a3185a10a00e4ddda7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataprocBatchConfig(
            batch_id=batch_id,
            environment_config=environment_config,
            id=id,
            labels=labels,
            location=location,
            project=project,
            pyspark_batch=pyspark_batch,
            runtime_config=runtime_config,
            spark_batch=spark_batch,
            spark_r_batch=spark_r_batch,
            spark_sql_batch=spark_sql_batch,
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
        '''Generates CDKTF code for importing a GoogleDataprocBatch resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataprocBatch to import.
        :param import_from_id: The id of the existing GoogleDataprocBatch that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataprocBatch to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe546fdad768fcda3f4d90d0f938698c5a09c05b15e67ac15f9311f4aec78ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnvironmentConfig")
    def put_environment_config(
        self,
        *,
        execution_config: typing.Optional[typing.Union["GoogleDataprocBatchEnvironmentConfigExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peripherals_config: typing.Optional[typing.Union["GoogleDataprocBatchEnvironmentConfigPeripheralsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_config: execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#execution_config GoogleDataprocBatch#execution_config}
        :param peripherals_config: peripherals_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#peripherals_config GoogleDataprocBatch#peripherals_config}
        '''
        value = GoogleDataprocBatchEnvironmentConfig(
            execution_config=execution_config, peripherals_config=peripherals_config
        )

        return typing.cast(None, jsii.invoke(self, "putEnvironmentConfig", [value]))

    @jsii.member(jsii_name="putPysparkBatch")
    def put_pyspark_batch(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_python_file_uri: typing.Optional[builtins.str] = None,
        python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        :param main_python_file_uri: The HCFS URI of the main Python file to use as the Spark driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_python_file_uri GoogleDataprocBatch#main_python_file_uri}
        :param python_file_uris: HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#python_file_uris GoogleDataprocBatch#python_file_uris}
        '''
        value = GoogleDataprocBatchPysparkBatch(
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            main_python_file_uri=main_python_file_uri,
            python_file_uris=python_file_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putPysparkBatch", [value]))

    @jsii.member(jsii_name="putRuntimeConfig")
    def put_runtime_config(
        self,
        *,
        autotuning_config: typing.Optional[typing.Union["GoogleDataprocBatchRuntimeConfigAutotuningConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cohort: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param autotuning_config: autotuning_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#autotuning_config GoogleDataprocBatch#autotuning_config}
        :param cohort: Optional. Cohort identifier. Identifies families of the workloads having the same shape, e.g. daily ETL jobs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#cohort GoogleDataprocBatch#cohort}
        :param container_image: Optional custom container image for the job runtime environment. If not specified, a default container image will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#container_image GoogleDataprocBatch#container_image}
        :param properties: A mapping of property names to values, which are used to configure workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#properties GoogleDataprocBatch#properties}
        :param version: Version of the batch runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#version GoogleDataprocBatch#version}
        '''
        value = GoogleDataprocBatchRuntimeConfig(
            autotuning_config=autotuning_config,
            cohort=cohort,
            container_image=container_image,
            properties=properties,
            version=version,
        )

        return typing.cast(None, jsii.invoke(self, "putRuntimeConfig", [value]))

    @jsii.member(jsii_name="putSparkBatch")
    def put_spark_batch(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        :param main_class: The name of the driver main class. The jar file that contains the class must be in the classpath or specified in jarFileUris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_class GoogleDataprocBatch#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_jar_file_uri GoogleDataprocBatch#main_jar_file_uri}
        '''
        value = GoogleDataprocBatchSparkBatch(
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            main_class=main_class,
            main_jar_file_uri=main_jar_file_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkBatch", [value]))

    @jsii.member(jsii_name="putSparkRBatch")
    def put_spark_r_batch(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_r_file_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        :param main_r_file_uri: The HCFS URI of the main R file to use as the driver. Must be a .R or .r file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_r_file_uri GoogleDataprocBatch#main_r_file_uri}
        '''
        value = GoogleDataprocBatchSparkRBatch(
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            main_r_file_uri=main_r_file_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkRBatch", [value]))

    @jsii.member(jsii_name="putSparkSqlBatch")
    def put_spark_sql_batch(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        :param query_file_uri: The HCFS URI of the script that contains Spark SQL queries to execute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#query_file_uri GoogleDataprocBatch#query_file_uri}
        :param query_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#query_variables GoogleDataprocBatch#query_variables}
        '''
        value = GoogleDataprocBatchSparkSqlBatch(
            jar_file_uris=jar_file_uris,
            query_file_uri=query_file_uri,
            query_variables=query_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkSqlBatch", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#create GoogleDataprocBatch#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#delete GoogleDataprocBatch#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#update GoogleDataprocBatch#update}.
        '''
        value = GoogleDataprocBatchTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBatchId")
    def reset_batch_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatchId", []))

    @jsii.member(jsii_name="resetEnvironmentConfig")
    def reset_environment_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPysparkBatch")
    def reset_pyspark_batch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPysparkBatch", []))

    @jsii.member(jsii_name="resetRuntimeConfig")
    def reset_runtime_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeConfig", []))

    @jsii.member(jsii_name="resetSparkBatch")
    def reset_spark_batch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkBatch", []))

    @jsii.member(jsii_name="resetSparkRBatch")
    def reset_spark_r_batch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkRBatch", []))

    @jsii.member(jsii_name="resetSparkSqlBatch")
    def reset_spark_sql_batch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkSqlBatch", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="creator")
    def creator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creator"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="environmentConfig")
    def environment_config(
        self,
    ) -> "GoogleDataprocBatchEnvironmentConfigOutputReference":
        return typing.cast("GoogleDataprocBatchEnvironmentConfigOutputReference", jsii.get(self, "environmentConfig"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="operation")
    def operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operation"))

    @builtins.property
    @jsii.member(jsii_name="pysparkBatch")
    def pyspark_batch(self) -> "GoogleDataprocBatchPysparkBatchOutputReference":
        return typing.cast("GoogleDataprocBatchPysparkBatchOutputReference", jsii.get(self, "pysparkBatch"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfig")
    def runtime_config(self) -> "GoogleDataprocBatchRuntimeConfigOutputReference":
        return typing.cast("GoogleDataprocBatchRuntimeConfigOutputReference", jsii.get(self, "runtimeConfig"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInfo")
    def runtime_info(self) -> "GoogleDataprocBatchRuntimeInfoList":
        return typing.cast("GoogleDataprocBatchRuntimeInfoList", jsii.get(self, "runtimeInfo"))

    @builtins.property
    @jsii.member(jsii_name="sparkBatch")
    def spark_batch(self) -> "GoogleDataprocBatchSparkBatchOutputReference":
        return typing.cast("GoogleDataprocBatchSparkBatchOutputReference", jsii.get(self, "sparkBatch"))

    @builtins.property
    @jsii.member(jsii_name="sparkRBatch")
    def spark_r_batch(self) -> "GoogleDataprocBatchSparkRBatchOutputReference":
        return typing.cast("GoogleDataprocBatchSparkRBatchOutputReference", jsii.get(self, "sparkRBatch"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlBatch")
    def spark_sql_batch(self) -> "GoogleDataprocBatchSparkSqlBatchOutputReference":
        return typing.cast("GoogleDataprocBatchSparkSqlBatchOutputReference", jsii.get(self, "sparkSqlBatch"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateHistory")
    def state_history(self) -> "GoogleDataprocBatchStateHistoryList":
        return typing.cast("GoogleDataprocBatchStateHistoryList", jsii.get(self, "stateHistory"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="stateTime")
    def state_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateTime"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleDataprocBatchTimeoutsOutputReference":
        return typing.cast("GoogleDataprocBatchTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

    @builtins.property
    @jsii.member(jsii_name="batchIdInput")
    def batch_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "batchIdInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentConfigInput")
    def environment_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocBatchEnvironmentConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocBatchEnvironmentConfig"], jsii.get(self, "environmentConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pysparkBatchInput")
    def pyspark_batch_input(self) -> typing.Optional["GoogleDataprocBatchPysparkBatch"]:
        return typing.cast(typing.Optional["GoogleDataprocBatchPysparkBatch"], jsii.get(self, "pysparkBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigInput")
    def runtime_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocBatchRuntimeConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocBatchRuntimeConfig"], jsii.get(self, "runtimeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkBatchInput")
    def spark_batch_input(self) -> typing.Optional["GoogleDataprocBatchSparkBatch"]:
        return typing.cast(typing.Optional["GoogleDataprocBatchSparkBatch"], jsii.get(self, "sparkBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkRBatchInput")
    def spark_r_batch_input(self) -> typing.Optional["GoogleDataprocBatchSparkRBatch"]:
        return typing.cast(typing.Optional["GoogleDataprocBatchSparkRBatch"], jsii.get(self, "sparkRBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlBatchInput")
    def spark_sql_batch_input(
        self,
    ) -> typing.Optional["GoogleDataprocBatchSparkSqlBatch"]:
        return typing.cast(typing.Optional["GoogleDataprocBatchSparkSqlBatch"], jsii.get(self, "sparkSqlBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocBatchTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocBatchTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="batchId")
    def batch_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchId"))

    @batch_id.setter
    def batch_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0a5b3e6ea0d701557e94aed746936fa443ef7e8a9fcb3978097df4f71c7632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45323daf847c44b90228615ae33272e213b7e2ea0254f8f205107286a54c94d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9340ea39cc0e13285d2f2243432de023feec9bd73b81aa8fb86a69349b8ed0b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0849fec3b46f74e2b743d91d73ffe9a81970fddb86760398e1600dadfd2bdbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855f1c56c68d6afdbb0c89af9d9c57429bda142be058d193c0f5cfa84cc45300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "batch_id": "batchId",
        "environment_config": "environmentConfig",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "project": "project",
        "pyspark_batch": "pysparkBatch",
        "runtime_config": "runtimeConfig",
        "spark_batch": "sparkBatch",
        "spark_r_batch": "sparkRBatch",
        "spark_sql_batch": "sparkSqlBatch",
        "timeouts": "timeouts",
    },
)
class GoogleDataprocBatchConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        batch_id: typing.Optional[builtins.str] = None,
        environment_config: typing.Optional[typing.Union["GoogleDataprocBatchEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        pyspark_batch: typing.Optional[typing.Union["GoogleDataprocBatchPysparkBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_config: typing.Optional[typing.Union["GoogleDataprocBatchRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_batch: typing.Optional[typing.Union["GoogleDataprocBatchSparkBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_batch: typing.Optional[typing.Union["GoogleDataprocBatchSparkRBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_batch: typing.Optional[typing.Union["GoogleDataprocBatchSparkSqlBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocBatchTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param batch_id: The ID to use for the batch, which will become the final component of the batch's resource name. This value must be 4-63 characters. Valid characters are /[a-z][0-9]-/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#batch_id GoogleDataprocBatch#batch_id}
        :param environment_config: environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#environment_config GoogleDataprocBatch#environment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#id GoogleDataprocBatch#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this batch. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#labels GoogleDataprocBatch#labels}
        :param location: The location in which the batch will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#location GoogleDataprocBatch#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#project GoogleDataprocBatch#project}.
        :param pyspark_batch: pyspark_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#pyspark_batch GoogleDataprocBatch#pyspark_batch}
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#runtime_config GoogleDataprocBatch#runtime_config}
        :param spark_batch: spark_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_batch GoogleDataprocBatch#spark_batch}
        :param spark_r_batch: spark_r_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_r_batch GoogleDataprocBatch#spark_r_batch}
        :param spark_sql_batch: spark_sql_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_sql_batch GoogleDataprocBatch#spark_sql_batch}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#timeouts GoogleDataprocBatch#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(environment_config, dict):
            environment_config = GoogleDataprocBatchEnvironmentConfig(**environment_config)
        if isinstance(pyspark_batch, dict):
            pyspark_batch = GoogleDataprocBatchPysparkBatch(**pyspark_batch)
        if isinstance(runtime_config, dict):
            runtime_config = GoogleDataprocBatchRuntimeConfig(**runtime_config)
        if isinstance(spark_batch, dict):
            spark_batch = GoogleDataprocBatchSparkBatch(**spark_batch)
        if isinstance(spark_r_batch, dict):
            spark_r_batch = GoogleDataprocBatchSparkRBatch(**spark_r_batch)
        if isinstance(spark_sql_batch, dict):
            spark_sql_batch = GoogleDataprocBatchSparkSqlBatch(**spark_sql_batch)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataprocBatchTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7523b4b2bdf6d3ded1eb0608a05585cae6908595fe5c1b8fec70c3bca6e644)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument batch_id", value=batch_id, expected_type=type_hints["batch_id"])
            check_type(argname="argument environment_config", value=environment_config, expected_type=type_hints["environment_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument pyspark_batch", value=pyspark_batch, expected_type=type_hints["pyspark_batch"])
            check_type(argname="argument runtime_config", value=runtime_config, expected_type=type_hints["runtime_config"])
            check_type(argname="argument spark_batch", value=spark_batch, expected_type=type_hints["spark_batch"])
            check_type(argname="argument spark_r_batch", value=spark_r_batch, expected_type=type_hints["spark_r_batch"])
            check_type(argname="argument spark_sql_batch", value=spark_sql_batch, expected_type=type_hints["spark_sql_batch"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if batch_id is not None:
            self._values["batch_id"] = batch_id
        if environment_config is not None:
            self._values["environment_config"] = environment_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if pyspark_batch is not None:
            self._values["pyspark_batch"] = pyspark_batch
        if runtime_config is not None:
            self._values["runtime_config"] = runtime_config
        if spark_batch is not None:
            self._values["spark_batch"] = spark_batch
        if spark_r_batch is not None:
            self._values["spark_r_batch"] = spark_r_batch
        if spark_sql_batch is not None:
            self._values["spark_sql_batch"] = spark_sql_batch
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
    def batch_id(self) -> typing.Optional[builtins.str]:
        '''The ID to use for the batch, which will become the final component of the batch's resource name.

        This value must be 4-63 characters. Valid characters are /[a-z][0-9]-/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#batch_id GoogleDataprocBatch#batch_id}
        '''
        result = self._values.get("batch_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_config(
        self,
    ) -> typing.Optional["GoogleDataprocBatchEnvironmentConfig"]:
        '''environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#environment_config GoogleDataprocBatch#environment_config}
        '''
        result = self._values.get("environment_config")
        return typing.cast(typing.Optional["GoogleDataprocBatchEnvironmentConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#id GoogleDataprocBatch#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels to associate with this batch.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#labels GoogleDataprocBatch#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location in which the batch will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#location GoogleDataprocBatch#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#project GoogleDataprocBatch#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pyspark_batch(self) -> typing.Optional["GoogleDataprocBatchPysparkBatch"]:
        '''pyspark_batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#pyspark_batch GoogleDataprocBatch#pyspark_batch}
        '''
        result = self._values.get("pyspark_batch")
        return typing.cast(typing.Optional["GoogleDataprocBatchPysparkBatch"], result)

    @builtins.property
    def runtime_config(self) -> typing.Optional["GoogleDataprocBatchRuntimeConfig"]:
        '''runtime_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#runtime_config GoogleDataprocBatch#runtime_config}
        '''
        result = self._values.get("runtime_config")
        return typing.cast(typing.Optional["GoogleDataprocBatchRuntimeConfig"], result)

    @builtins.property
    def spark_batch(self) -> typing.Optional["GoogleDataprocBatchSparkBatch"]:
        '''spark_batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_batch GoogleDataprocBatch#spark_batch}
        '''
        result = self._values.get("spark_batch")
        return typing.cast(typing.Optional["GoogleDataprocBatchSparkBatch"], result)

    @builtins.property
    def spark_r_batch(self) -> typing.Optional["GoogleDataprocBatchSparkRBatch"]:
        '''spark_r_batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_r_batch GoogleDataprocBatch#spark_r_batch}
        '''
        result = self._values.get("spark_r_batch")
        return typing.cast(typing.Optional["GoogleDataprocBatchSparkRBatch"], result)

    @builtins.property
    def spark_sql_batch(self) -> typing.Optional["GoogleDataprocBatchSparkSqlBatch"]:
        '''spark_sql_batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_sql_batch GoogleDataprocBatch#spark_sql_batch}
        '''
        result = self._values.get("spark_sql_batch")
        return typing.cast(typing.Optional["GoogleDataprocBatchSparkSqlBatch"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataprocBatchTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#timeouts GoogleDataprocBatch#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataprocBatchTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "execution_config": "executionConfig",
        "peripherals_config": "peripheralsConfig",
    },
)
class GoogleDataprocBatchEnvironmentConfig:
    def __init__(
        self,
        *,
        execution_config: typing.Optional[typing.Union["GoogleDataprocBatchEnvironmentConfigExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peripherals_config: typing.Optional[typing.Union["GoogleDataprocBatchEnvironmentConfigPeripheralsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_config: execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#execution_config GoogleDataprocBatch#execution_config}
        :param peripherals_config: peripherals_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#peripherals_config GoogleDataprocBatch#peripherals_config}
        '''
        if isinstance(execution_config, dict):
            execution_config = GoogleDataprocBatchEnvironmentConfigExecutionConfig(**execution_config)
        if isinstance(peripherals_config, dict):
            peripherals_config = GoogleDataprocBatchEnvironmentConfigPeripheralsConfig(**peripherals_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9408e89affcb18f9ed18cfaa75820d89833ead8be4d1d8cec54543ce763e3853)
            check_type(argname="argument execution_config", value=execution_config, expected_type=type_hints["execution_config"])
            check_type(argname="argument peripherals_config", value=peripherals_config, expected_type=type_hints["peripherals_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if execution_config is not None:
            self._values["execution_config"] = execution_config
        if peripherals_config is not None:
            self._values["peripherals_config"] = peripherals_config

    @builtins.property
    def execution_config(
        self,
    ) -> typing.Optional["GoogleDataprocBatchEnvironmentConfigExecutionConfig"]:
        '''execution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#execution_config GoogleDataprocBatch#execution_config}
        '''
        result = self._values.get("execution_config")
        return typing.cast(typing.Optional["GoogleDataprocBatchEnvironmentConfigExecutionConfig"], result)

    @builtins.property
    def peripherals_config(
        self,
    ) -> typing.Optional["GoogleDataprocBatchEnvironmentConfigPeripheralsConfig"]:
        '''peripherals_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#peripherals_config GoogleDataprocBatch#peripherals_config}
        '''
        result = self._values.get("peripherals_config")
        return typing.cast(typing.Optional["GoogleDataprocBatchEnvironmentConfigPeripheralsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchEnvironmentConfigExecutionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key": "kmsKey",
        "network_tags": "networkTags",
        "network_uri": "networkUri",
        "service_account": "serviceAccount",
        "staging_bucket": "stagingBucket",
        "subnetwork_uri": "subnetworkUri",
        "ttl": "ttl",
    },
)
class GoogleDataprocBatchEnvironmentConfigExecutionConfig:
    def __init__(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_uri: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        subnetwork_uri: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: The Cloud KMS key to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#kms_key GoogleDataprocBatch#kms_key}
        :param network_tags: Tags used for network traffic control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#network_tags GoogleDataprocBatch#network_tags}
        :param network_uri: Network configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#network_uri GoogleDataprocBatch#network_uri}
        :param service_account: Service account that used to execute workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#service_account GoogleDataprocBatch#service_account}
        :param staging_bucket: A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running, and then create and manage project-level, per-location staging and temporary buckets. This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#staging_bucket GoogleDataprocBatch#staging_bucket}
        :param subnetwork_uri: Subnetwork configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#subnetwork_uri GoogleDataprocBatch#subnetwork_uri}
        :param ttl: The duration after which the workload will be terminated. When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing work to finish. If ttl is not specified for a batch workload, the workload will be allowed to run until it exits naturally (or run forever without exiting). If ttl is not specified for an interactive session, it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours. Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session), the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or when ttl has been exceeded, whichever occurs first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#ttl GoogleDataprocBatch#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8b56d26ff63c476c09c1d632e1fafe2dc0911ca518a0198098b041ab5192b6)
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument network_tags", value=network_tags, expected_type=type_hints["network_tags"])
            check_type(argname="argument network_uri", value=network_uri, expected_type=type_hints["network_uri"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument staging_bucket", value=staging_bucket, expected_type=type_hints["staging_bucket"])
            check_type(argname="argument subnetwork_uri", value=subnetwork_uri, expected_type=type_hints["subnetwork_uri"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if network_tags is not None:
            self._values["network_tags"] = network_tags
        if network_uri is not None:
            self._values["network_uri"] = network_uri
        if service_account is not None:
            self._values["service_account"] = service_account
        if staging_bucket is not None:
            self._values["staging_bucket"] = staging_bucket
        if subnetwork_uri is not None:
            self._values["subnetwork_uri"] = subnetwork_uri
        if ttl is not None:
            self._values["ttl"] = ttl

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS key to use for encryption.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#kms_key GoogleDataprocBatch#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags used for network traffic control.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#network_tags GoogleDataprocBatch#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_uri(self) -> typing.Optional[builtins.str]:
        '''Network configuration for workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#network_uri GoogleDataprocBatch#network_uri}
        '''
        result = self._values.get("network_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Service account that used to execute workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#service_account GoogleDataprocBatch#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def staging_bucket(self) -> typing.Optional[builtins.str]:
        '''A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files.

        If you do not specify a staging bucket,
        Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running,
        and then create and manage project-level, per-location staging and temporary buckets.
        This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#staging_bucket GoogleDataprocBatch#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork_uri(self) -> typing.Optional[builtins.str]:
        '''Subnetwork configuration for workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#subnetwork_uri GoogleDataprocBatch#subnetwork_uri}
        '''
        result = self._values.get("subnetwork_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ttl(self) -> typing.Optional[builtins.str]:
        '''The duration after which the workload will be terminated.

        When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing
        work to finish. If ttl is not specified for a batch workload, the workload will be allowed to run until it
        exits naturally (or run forever without exiting). If ttl is not specified for an interactive session,
        it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours.
        Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session),
        the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or
        when ttl has been exceeded, whichever occurs first.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#ttl GoogleDataprocBatch#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchEnvironmentConfigExecutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchEnvironmentConfigExecutionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchEnvironmentConfigExecutionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a245ad0bb42682dc7e3d708a0fbab97c2fded9981d5a951c2bea911ce25b744a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetNetworkTags")
    def reset_network_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkTags", []))

    @jsii.member(jsii_name="resetNetworkUri")
    def reset_network_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkUri", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetStagingBucket")
    def reset_staging_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStagingBucket", []))

    @jsii.member(jsii_name="resetSubnetworkUri")
    def reset_subnetwork_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetworkUri", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTagsInput")
    def network_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="networkUriInput")
    def network_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkUriInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="stagingBucketInput")
    def staging_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stagingBucketInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkUriInput")
    def subnetwork_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkUriInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0833448bdabd0ffe7a7705a0e7fec9ef830748ae11bc4ea90f545a0b57a4c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6093d9e6ec8b34a5226a5c8e8b9992f62ff885a1ce75785418e887189d50468)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUri")
    def network_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUri"))

    @network_uri.setter
    def network_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9400c54128e6e8a083d117d03beb2da748c480c63450b06644aeba19fc686830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd89226324a0fc0b78e0d24f07792c9ae304d0a5932b7e95cda38862f5301fe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fff8301ad4d8e53105d65ac610a6cc2acdca318f50042dc56e8e28d1151472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkUri")
    def subnetwork_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkUri"))

    @subnetwork_uri.setter
    def subnetwork_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f452b0c3dfb1fe3025e4bb0eca6cb3a4988dad808b9e0a8f702639448ad9fa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ece41f45e6d2f6c6e40da7f32d8299f16854cc087d20a0f5975ec9785579bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocBatchEnvironmentConfigExecutionConfig]:
        return typing.cast(typing.Optional[GoogleDataprocBatchEnvironmentConfigExecutionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchEnvironmentConfigExecutionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d8fca77fc29f9996be71e71676644a7bd9359683e6a4ed537fcd905ad80200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocBatchEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14cc92c44334a89ee9c4ed3180dafdcbe0c742d849f15150881257b019f1bd6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExecutionConfig")
    def put_execution_config(
        self,
        *,
        kms_key: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_uri: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        staging_bucket: typing.Optional[builtins.str] = None,
        subnetwork_uri: typing.Optional[builtins.str] = None,
        ttl: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key: The Cloud KMS key to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#kms_key GoogleDataprocBatch#kms_key}
        :param network_tags: Tags used for network traffic control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#network_tags GoogleDataprocBatch#network_tags}
        :param network_uri: Network configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#network_uri GoogleDataprocBatch#network_uri}
        :param service_account: Service account that used to execute workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#service_account GoogleDataprocBatch#service_account}
        :param staging_bucket: A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running, and then create and manage project-level, per-location staging and temporary buckets. This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#staging_bucket GoogleDataprocBatch#staging_bucket}
        :param subnetwork_uri: Subnetwork configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#subnetwork_uri GoogleDataprocBatch#subnetwork_uri}
        :param ttl: The duration after which the workload will be terminated. When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing work to finish. If ttl is not specified for a batch workload, the workload will be allowed to run until it exits naturally (or run forever without exiting). If ttl is not specified for an interactive session, it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours. Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session), the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or when ttl has been exceeded, whichever occurs first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#ttl GoogleDataprocBatch#ttl}
        '''
        value = GoogleDataprocBatchEnvironmentConfigExecutionConfig(
            kms_key=kms_key,
            network_tags=network_tags,
            network_uri=network_uri,
            service_account=service_account,
            staging_bucket=staging_bucket,
            subnetwork_uri=subnetwork_uri,
            ttl=ttl,
        )

        return typing.cast(None, jsii.invoke(self, "putExecutionConfig", [value]))

    @jsii.member(jsii_name="putPeripheralsConfig")
    def put_peripherals_config(
        self,
        *,
        metastore_service: typing.Optional[builtins.str] = None,
        spark_history_server_config: typing.Optional[typing.Union["GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#metastore_service GoogleDataprocBatch#metastore_service}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_history_server_config GoogleDataprocBatch#spark_history_server_config}
        '''
        value = GoogleDataprocBatchEnvironmentConfigPeripheralsConfig(
            metastore_service=metastore_service,
            spark_history_server_config=spark_history_server_config,
        )

        return typing.cast(None, jsii.invoke(self, "putPeripheralsConfig", [value]))

    @jsii.member(jsii_name="resetExecutionConfig")
    def reset_execution_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionConfig", []))

    @jsii.member(jsii_name="resetPeripheralsConfig")
    def reset_peripherals_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeripheralsConfig", []))

    @builtins.property
    @jsii.member(jsii_name="executionConfig")
    def execution_config(
        self,
    ) -> GoogleDataprocBatchEnvironmentConfigExecutionConfigOutputReference:
        return typing.cast(GoogleDataprocBatchEnvironmentConfigExecutionConfigOutputReference, jsii.get(self, "executionConfig"))

    @builtins.property
    @jsii.member(jsii_name="peripheralsConfig")
    def peripherals_config(
        self,
    ) -> "GoogleDataprocBatchEnvironmentConfigPeripheralsConfigOutputReference":
        return typing.cast("GoogleDataprocBatchEnvironmentConfigPeripheralsConfigOutputReference", jsii.get(self, "peripheralsConfig"))

    @builtins.property
    @jsii.member(jsii_name="executionConfigInput")
    def execution_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocBatchEnvironmentConfigExecutionConfig]:
        return typing.cast(typing.Optional[GoogleDataprocBatchEnvironmentConfigExecutionConfig], jsii.get(self, "executionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="peripheralsConfigInput")
    def peripherals_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocBatchEnvironmentConfigPeripheralsConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocBatchEnvironmentConfigPeripheralsConfig"], jsii.get(self, "peripheralsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocBatchEnvironmentConfig]:
        return typing.cast(typing.Optional[GoogleDataprocBatchEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be76276a2b1acd4cc1eebea16375210ae6232aadeb44fa2ca8afbe75755cfb86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchEnvironmentConfigPeripheralsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metastore_service": "metastoreService",
        "spark_history_server_config": "sparkHistoryServerConfig",
    },
)
class GoogleDataprocBatchEnvironmentConfigPeripheralsConfig:
    def __init__(
        self,
        *,
        metastore_service: typing.Optional[builtins.str] = None,
        spark_history_server_config: typing.Optional[typing.Union["GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#metastore_service GoogleDataprocBatch#metastore_service}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_history_server_config GoogleDataprocBatch#spark_history_server_config}
        '''
        if isinstance(spark_history_server_config, dict):
            spark_history_server_config = GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(**spark_history_server_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0181b06adcd0549bd11d7663f6b580f1067d7b6209729bd74a22600829f325)
            check_type(argname="argument metastore_service", value=metastore_service, expected_type=type_hints["metastore_service"])
            check_type(argname="argument spark_history_server_config", value=spark_history_server_config, expected_type=type_hints["spark_history_server_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metastore_service is not None:
            self._values["metastore_service"] = metastore_service
        if spark_history_server_config is not None:
            self._values["spark_history_server_config"] = spark_history_server_config

    @builtins.property
    def metastore_service(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Metastore service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#metastore_service GoogleDataprocBatch#metastore_service}
        '''
        result = self._values.get("metastore_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_history_server_config(
        self,
    ) -> typing.Optional["GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"]:
        '''spark_history_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#spark_history_server_config GoogleDataprocBatch#spark_history_server_config}
        '''
        result = self._values.get("spark_history_server_config")
        return typing.cast(typing.Optional["GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchEnvironmentConfigPeripheralsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchEnvironmentConfigPeripheralsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchEnvironmentConfigPeripheralsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c626aa455ad65a47f089891c00027f21feddc0998f5eca0de56142fb28a2e9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSparkHistoryServerConfig")
    def put_spark_history_server_config(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#dataproc_cluster GoogleDataprocBatch#dataproc_cluster}
        '''
        value = GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(
            dataproc_cluster=dataproc_cluster
        )

        return typing.cast(None, jsii.invoke(self, "putSparkHistoryServerConfig", [value]))

    @jsii.member(jsii_name="resetMetastoreService")
    def reset_metastore_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastoreService", []))

    @jsii.member(jsii_name="resetSparkHistoryServerConfig")
    def reset_spark_history_server_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkHistoryServerConfig", []))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfig")
    def spark_history_server_config(
        self,
    ) -> "GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference":
        return typing.cast("GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference", jsii.get(self, "sparkHistoryServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreServiceInput")
    def metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfigInput")
    def spark_history_server_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"], jsii.get(self, "sparkHistoryServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreService")
    def metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metastoreService"))

    @metastore_service.setter
    def metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b0cb2f2053e0aaa2491965a73eeec41893c9a4f1409e87778b6b01739da441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metastoreService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocBatchEnvironmentConfigPeripheralsConfig]:
        return typing.cast(typing.Optional[GoogleDataprocBatchEnvironmentConfigPeripheralsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchEnvironmentConfigPeripheralsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b211e4b1e01ff98e414d3e376783b91fcb60453de56f6aaa04461c9c60645cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_cluster": "dataprocCluster"},
)
class GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig:
    def __init__(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#dataproc_cluster GoogleDataprocBatch#dataproc_cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b867cac6ed441b00c04dec94f910e73cfb56efa6c674d90cfd68e12e9bf572b)
            check_type(argname="argument dataproc_cluster", value=dataproc_cluster, expected_type=type_hints["dataproc_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_cluster is not None:
            self._values["dataproc_cluster"] = dataproc_cluster

    @builtins.property
    def dataproc_cluster(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#dataproc_cluster GoogleDataprocBatch#dataproc_cluster}
        '''
        result = self._values.get("dataproc_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b7a8c441ad07d6963628512bda6ae050da2aeff6994248d450240ea8e2e31f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDataprocCluster")
    def reset_dataproc_cluster(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataprocCluster", []))

    @builtins.property
    @jsii.member(jsii_name="dataprocClusterInput")
    def dataproc_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataprocClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="dataprocCluster")
    def dataproc_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataprocCluster"))

    @dataproc_cluster.setter
    def dataproc_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85543090118d74f5bf17122ad79fee486112c0d3780ed2209b21124b15e3df52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig]:
        return typing.cast(typing.Optional[GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa94719f876b05c372434f13a9abc5b91ec60df7716f1cefcf35b928f6d36a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchPysparkBatch",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "main_python_file_uri": "mainPythonFileUri",
        "python_file_uris": "pythonFileUris",
    },
)
class GoogleDataprocBatchPysparkBatch:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_python_file_uri: typing.Optional[builtins.str] = None,
        python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        :param main_python_file_uri: The HCFS URI of the main Python file to use as the Spark driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_python_file_uri GoogleDataprocBatch#main_python_file_uri}
        :param python_file_uris: HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#python_file_uris GoogleDataprocBatch#python_file_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b77c83462681c638f2d944e210099fb74f2aae7401bc390c0be8ba01e0e9bbb)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument main_python_file_uri", value=main_python_file_uri, expected_type=type_hints["main_python_file_uri"])
            check_type(argname="argument python_file_uris", value=python_file_uris, expected_type=type_hints["python_file_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if main_python_file_uri is not None:
            self._values["main_python_file_uri"] = main_python_file_uri
        if python_file_uris is not None:
            self._values["python_file_uris"] = python_file_uris

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments that can be set as batch
        properties, such as --conf, since a collision can occur that causes an incorrect batch submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the classpath of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_python_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the main Python file to use as the Spark driver. Must be a .py file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_python_file_uri GoogleDataprocBatch#main_python_file_uri}
        '''
        result = self._values.get("main_python_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#python_file_uris GoogleDataprocBatch#python_file_uris}
        '''
        result = self._values.get("python_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchPysparkBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchPysparkBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchPysparkBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca13696f1523d000f74890bdc26d3be7d93e8b613a3a3f190cca10213c869e27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetMainPythonFileUri")
    def reset_main_python_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainPythonFileUri", []))

    @jsii.member(jsii_name="resetPythonFileUris")
    def reset_python_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonFileUris", []))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUriInput")
    def main_python_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainPythonFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonFileUrisInput")
    def python_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pythonFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b5946e7599417202629e1ecaeed3ba9624f3d3bafde050b456a70dc0d73e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6eb06762ba5d8c669b3b02ffe2cb3a441d56d1cb1197d07f9fc927dcc476410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fad8fe303edf1162840b4d8341dd95e5e5d5bd20a4d185efaa0bafa7a8f237e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4af08a9310108714cb1c253192e35ac76d2bdbf6361374e0d669d6d3f1bc1ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUri")
    def main_python_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainPythonFileUri"))

    @main_python_file_uri.setter
    def main_python_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515dc43dcb32fd3e5f0fe44af613f393a9ca602f2fb37ae87658145846982b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainPythonFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonFileUris")
    def python_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonFileUris"))

    @python_file_uris.setter
    def python_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca86affb1c7b8607c9b113693049aed340efd0096e153f4e5a518c28326eead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocBatchPysparkBatch]:
        return typing.cast(typing.Optional[GoogleDataprocBatchPysparkBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchPysparkBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d99fb24def4bcc4966adf1eef83301d2c540bf461fbeac617fb28058916b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autotuning_config": "autotuningConfig",
        "cohort": "cohort",
        "container_image": "containerImage",
        "properties": "properties",
        "version": "version",
    },
)
class GoogleDataprocBatchRuntimeConfig:
    def __init__(
        self,
        *,
        autotuning_config: typing.Optional[typing.Union["GoogleDataprocBatchRuntimeConfigAutotuningConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cohort: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param autotuning_config: autotuning_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#autotuning_config GoogleDataprocBatch#autotuning_config}
        :param cohort: Optional. Cohort identifier. Identifies families of the workloads having the same shape, e.g. daily ETL jobs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#cohort GoogleDataprocBatch#cohort}
        :param container_image: Optional custom container image for the job runtime environment. If not specified, a default container image will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#container_image GoogleDataprocBatch#container_image}
        :param properties: A mapping of property names to values, which are used to configure workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#properties GoogleDataprocBatch#properties}
        :param version: Version of the batch runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#version GoogleDataprocBatch#version}
        '''
        if isinstance(autotuning_config, dict):
            autotuning_config = GoogleDataprocBatchRuntimeConfigAutotuningConfig(**autotuning_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff49119b8f8da83b92fddfca02cec7ea62d5a66e80f3eff528deca54988947cf)
            check_type(argname="argument autotuning_config", value=autotuning_config, expected_type=type_hints["autotuning_config"])
            check_type(argname="argument cohort", value=cohort, expected_type=type_hints["cohort"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if autotuning_config is not None:
            self._values["autotuning_config"] = autotuning_config
        if cohort is not None:
            self._values["cohort"] = cohort
        if container_image is not None:
            self._values["container_image"] = container_image
        if properties is not None:
            self._values["properties"] = properties
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def autotuning_config(
        self,
    ) -> typing.Optional["GoogleDataprocBatchRuntimeConfigAutotuningConfig"]:
        '''autotuning_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#autotuning_config GoogleDataprocBatch#autotuning_config}
        '''
        result = self._values.get("autotuning_config")
        return typing.cast(typing.Optional["GoogleDataprocBatchRuntimeConfigAutotuningConfig"], result)

    @builtins.property
    def cohort(self) -> typing.Optional[builtins.str]:
        '''Optional. Cohort identifier. Identifies families of the workloads having the same shape, e.g. daily ETL jobs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#cohort GoogleDataprocBatch#cohort}
        '''
        result = self._values.get("cohort")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_image(self) -> typing.Optional[builtins.str]:
        '''Optional custom container image for the job runtime environment. If not specified, a default container image will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#container_image GoogleDataprocBatch#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values, which are used to configure workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#properties GoogleDataprocBatch#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the batch runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#version GoogleDataprocBatch#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchRuntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeConfigAutotuningConfig",
    jsii_struct_bases=[],
    name_mapping={"scenarios": "scenarios"},
)
class GoogleDataprocBatchRuntimeConfigAutotuningConfig:
    def __init__(
        self,
        *,
        scenarios: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scenarios: Optional. Scenarios for which tunings are applied. Possible values: ["SCALING", "BROADCAST_HASH_JOIN", "MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#scenarios GoogleDataprocBatch#scenarios}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59fd30ca40c7faa1c3a4c7e224cae92b414ec055c9bcb5327160787e67d6403b)
            check_type(argname="argument scenarios", value=scenarios, expected_type=type_hints["scenarios"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scenarios is not None:
            self._values["scenarios"] = scenarios

    @builtins.property
    def scenarios(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Scenarios for which tunings are applied. Possible values: ["SCALING", "BROADCAST_HASH_JOIN", "MEMORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#scenarios GoogleDataprocBatch#scenarios}
        '''
        result = self._values.get("scenarios")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchRuntimeConfigAutotuningConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchRuntimeConfigAutotuningConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeConfigAutotuningConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d1741f19713e58b246d7a7b88308c3a685f8bcbc8b0b33742a59ea22745fd5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetScenarios")
    def reset_scenarios(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScenarios", []))

    @builtins.property
    @jsii.member(jsii_name="scenariosInput")
    def scenarios_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scenariosInput"))

    @builtins.property
    @jsii.member(jsii_name="scenarios")
    def scenarios(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scenarios"))

    @scenarios.setter
    def scenarios(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81464df2b9190dff67e3f93eb09f01b3335ec5d16931ea30f1f52c784b717fb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scenarios", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocBatchRuntimeConfigAutotuningConfig]:
        return typing.cast(typing.Optional[GoogleDataprocBatchRuntimeConfigAutotuningConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchRuntimeConfigAutotuningConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce4b45178635bad08c2811972839725d62ae94c98cd962cf62fc5a93a5c10d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocBatchRuntimeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef76bedbf1127c14c9dc6ac3dc065568fa5632dc2aa6d4d4516817547dc0ef86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutotuningConfig")
    def put_autotuning_config(
        self,
        *,
        scenarios: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scenarios: Optional. Scenarios for which tunings are applied. Possible values: ["SCALING", "BROADCAST_HASH_JOIN", "MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#scenarios GoogleDataprocBatch#scenarios}
        '''
        value = GoogleDataprocBatchRuntimeConfigAutotuningConfig(scenarios=scenarios)

        return typing.cast(None, jsii.invoke(self, "putAutotuningConfig", [value]))

    @jsii.member(jsii_name="resetAutotuningConfig")
    def reset_autotuning_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutotuningConfig", []))

    @jsii.member(jsii_name="resetCohort")
    def reset_cohort(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCohort", []))

    @jsii.member(jsii_name="resetContainerImage")
    def reset_container_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImage", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @builtins.property
    @jsii.member(jsii_name="autotuningConfig")
    def autotuning_config(
        self,
    ) -> GoogleDataprocBatchRuntimeConfigAutotuningConfigOutputReference:
        return typing.cast(GoogleDataprocBatchRuntimeConfigAutotuningConfigOutputReference, jsii.get(self, "autotuningConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveProperties")
    def effective_properties(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveProperties"))

    @builtins.property
    @jsii.member(jsii_name="autotuningConfigInput")
    def autotuning_config_input(
        self,
    ) -> typing.Optional[GoogleDataprocBatchRuntimeConfigAutotuningConfig]:
        return typing.cast(typing.Optional[GoogleDataprocBatchRuntimeConfigAutotuningConfig], jsii.get(self, "autotuningConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="cohortInput")
    def cohort_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cohortInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="cohort")
    def cohort(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cohort"))

    @cohort.setter
    def cohort(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8408d967f60a5a745f8910f47eb127fc1124aed82f804604b4ae2fba03d9d7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cohort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerImage"))

    @container_image.setter
    def container_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64760611c3a9a9fd7609f513df889935c168b84624038264af48eff32627363e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f9cf9821a463189e8a15e800e6a34f70bb0fc12b3cb52fd011521b64303966)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f878eb79215e06d12222b975e70f9c6c813fb467944c00b97e603c15fdc7e5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocBatchRuntimeConfig]:
        return typing.cast(typing.Optional[GoogleDataprocBatchRuntimeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchRuntimeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7002e9ad87a75110a063c02644bf1fa2f06999c1896004daf1a09b4fd33601bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataprocBatchRuntimeInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchRuntimeInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfoApproximateUsage",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataprocBatchRuntimeInfoApproximateUsage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchRuntimeInfoApproximateUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchRuntimeInfoApproximateUsageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfoApproximateUsageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4707a13757588a2ad058cc4a8b9612e0df783446358185ddbcd04d2bd0ac43e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocBatchRuntimeInfoApproximateUsageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2dbf5d7196ea1f87632dc5d1160f2f25b2501e2e13ef2c2e9ad5f9d949ea07a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocBatchRuntimeInfoApproximateUsageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae81d7ec8b09af2eb2df8ee4439ceae720aeec4f1889dc214e2b95203de66aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d574a3cbcb3be40d4e303dfddf4a71254a71c3aea0ef8a83d3a29d96fd1353cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52859a74b8d5de35c15420c933f2289b177d7267b8d00c860fa445ada747b83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocBatchRuntimeInfoApproximateUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfoApproximateUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6e618e5c107743b4b6738135bc9c235694ca6b2a724b9767349f150e15d5672)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @builtins.property
    @jsii.member(jsii_name="milliAcceleratorSeconds")
    def milli_accelerator_seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "milliAcceleratorSeconds"))

    @builtins.property
    @jsii.member(jsii_name="milliDcuSeconds")
    def milli_dcu_seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "milliDcuSeconds"))

    @builtins.property
    @jsii.member(jsii_name="shuffleStorageGbSeconds")
    def shuffle_storage_gb_seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shuffleStorageGbSeconds"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocBatchRuntimeInfoApproximateUsage]:
        return typing.cast(typing.Optional[GoogleDataprocBatchRuntimeInfoApproximateUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchRuntimeInfoApproximateUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30af8f977947e08a54780a2176856341e0f940eea6216f108c6e20dae8169c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfoCurrentUsage",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataprocBatchRuntimeInfoCurrentUsage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchRuntimeInfoCurrentUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchRuntimeInfoCurrentUsageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfoCurrentUsageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b52a7bc0fe335f0eba40d9728e81fa4e28af02c669f3e95f4be126b6d2c994b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocBatchRuntimeInfoCurrentUsageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c2795381630ba134602c0e245daa8d31bd66976260fc3818d9fdb87a9cef9e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocBatchRuntimeInfoCurrentUsageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d803b12e97ce8b683ec8837f268be4050ffc9855b8a1d783b88591fc31b5189)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1fb566f01dace0e57fe3fca10bc3963534b419a5a82635592aa415b1af659df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6799eb72c8db3922e5133477527cd6a19fae5ac649fa6584af8dfd9c0703f1cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocBatchRuntimeInfoCurrentUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfoCurrentUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79d1252ab2addbbc06b3d3436f3d4bcc3a370107a1d7891dc26b22c11f5d8510)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @builtins.property
    @jsii.member(jsii_name="milliAccelerator")
    def milli_accelerator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "milliAccelerator"))

    @builtins.property
    @jsii.member(jsii_name="milliDcu")
    def milli_dcu(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "milliDcu"))

    @builtins.property
    @jsii.member(jsii_name="milliDcuPremium")
    def milli_dcu_premium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "milliDcuPremium"))

    @builtins.property
    @jsii.member(jsii_name="shuffleStorageGb")
    def shuffle_storage_gb(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shuffleStorageGb"))

    @builtins.property
    @jsii.member(jsii_name="shuffleStorageGbPremium")
    def shuffle_storage_gb_premium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shuffleStorageGbPremium"))

    @builtins.property
    @jsii.member(jsii_name="snapshotTime")
    def snapshot_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocBatchRuntimeInfoCurrentUsage]:
        return typing.cast(typing.Optional[GoogleDataprocBatchRuntimeInfoCurrentUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchRuntimeInfoCurrentUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34889ed88fcdf4f3cc5ea535480d3663a384eef4f7a267d70ac2449d0aea06dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocBatchRuntimeInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e36dc4bfa9affd954701787a1923ba501a17bf4770ba52c2c29907d1cb50f009)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocBatchRuntimeInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347128bbbdbd99647a589a828d2ca49440c1631b461b264b07d364af115157ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocBatchRuntimeInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883d715d50e8a54ec4fcc231ecb6908f2c4da594fed6de9f11f3cc62f5d6d097)
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
            type_hints = typing.get_type_hints(_typecheckingstub__168b7a91e7b6575854f4459be9ac300eaab1010533dd2c5076d9dd0bbf0f8915)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7846ba6a215f9862b64f3a00609188616c4c87f01910f53cd431a1ea33bda8b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocBatchRuntimeInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchRuntimeInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fec2359b40dabb4602dd68341614d24b310d672bf867bc9210d0054bd217670)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="approximateUsage")
    def approximate_usage(self) -> GoogleDataprocBatchRuntimeInfoApproximateUsageList:
        return typing.cast(GoogleDataprocBatchRuntimeInfoApproximateUsageList, jsii.get(self, "approximateUsage"))

    @builtins.property
    @jsii.member(jsii_name="currentUsage")
    def current_usage(self) -> GoogleDataprocBatchRuntimeInfoCurrentUsageList:
        return typing.cast(GoogleDataprocBatchRuntimeInfoCurrentUsageList, jsii.get(self, "currentUsage"))

    @builtins.property
    @jsii.member(jsii_name="diagnosticOutputUri")
    def diagnostic_output_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "diagnosticOutputUri"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "endpoints"))

    @builtins.property
    @jsii.member(jsii_name="outputUri")
    def output_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputUri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocBatchRuntimeInfo]:
        return typing.cast(typing.Optional[GoogleDataprocBatchRuntimeInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchRuntimeInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c127d9507bbefbb4c64b64eb6e8bdbef9c32c9526a7d71717a43aba2d03b8a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchSparkBatch",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "main_class": "mainClass",
        "main_jar_file_uri": "mainJarFileUri",
    },
)
class GoogleDataprocBatchSparkBatch:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        :param main_class: The name of the driver main class. The jar file that contains the class must be in the classpath or specified in jarFileUris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_class GoogleDataprocBatch#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_jar_file_uri GoogleDataprocBatch#main_jar_file_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b0997ed51925db7c9d6140ab84f40bbace5c990c64ced3064310d1858cde0c)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
            check_type(argname="argument main_jar_file_uri", value=main_jar_file_uri, expected_type=type_hints["main_jar_file_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if main_class is not None:
            self._values["main_class"] = main_class
        if main_jar_file_uri is not None:
            self._values["main_jar_file_uri"] = main_jar_file_uri

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments that can be set as batch
        properties, such as --conf, since a collision can occur that causes an incorrect batch submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the classpath of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The name of the driver main class.

        The jar file that contains the class must be in the
        classpath or specified in jarFileUris.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_class GoogleDataprocBatch#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the jar file that contains the main class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_jar_file_uri GoogleDataprocBatch#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchSparkBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchSparkBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchSparkBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3b2829100bee5a6c550218f13b438797bb5f6b6014af93a734886fa1c3daab5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetMainClass")
    def reset_main_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainClass", []))

    @jsii.member(jsii_name="resetMainJarFileUri")
    def reset_main_jar_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainJarFileUri", []))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="mainClassInput")
    def main_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainClassInput"))

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUriInput")
    def main_jar_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainJarFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60c726ec36fa7954c55c0fa9bda1f50cc184e676fcf7764857704683dee315a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec8a891cba380df5379e3f3d2ef8d7b524cb17fe59461be340d6258db5029fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43bd70b14080944d648b51fd13fa30f5409673ca21ac22bb998bcb1ebbdb598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b72f831686d243564ecdcf1c652a3a4e9e2f21cdafae9034a897da7a8fd99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db435b9cd970597b73f18ef4d84f70983ff999e46a0fcb81b4079b997681b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__713bba1dc680948ca88fa0ec731d13bf09ee3f0c01f4217f43d65bf89064ccfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocBatchSparkBatch]:
        return typing.cast(typing.Optional[GoogleDataprocBatchSparkBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchSparkBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d60e209ba4dacafb89429fd0b68e4657c3100bd82279957e2e4736dfdfa471)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchSparkRBatch",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "main_r_file_uri": "mainRFileUri",
    },
)
class GoogleDataprocBatchSparkRBatch:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_r_file_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        :param main_r_file_uri: The HCFS URI of the main R file to use as the driver. Must be a .R or .r file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_r_file_uri GoogleDataprocBatch#main_r_file_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e92c168aa84cb92c0bc3915e455376de03baac8f092a22eda7af372fe872bdb)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument main_r_file_uri", value=main_r_file_uri, expected_type=type_hints["main_r_file_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if main_r_file_uri is not None:
            self._values["main_r_file_uri"] = main_r_file_uri

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#archive_uris GoogleDataprocBatch#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments that can be set as batch
        properties, such as --conf, since a collision can occur that causes an incorrect batch submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#args GoogleDataprocBatch#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#file_uris GoogleDataprocBatch#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_r_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the main R file to use as the driver.

        Must be a .R or .r file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#main_r_file_uri GoogleDataprocBatch#main_r_file_uri}
        '''
        result = self._values.get("main_r_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchSparkRBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchSparkRBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchSparkRBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ea9b339197c22a64692566602a7f1193a7c5815e2f81cda2dcc5d236d94bd6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetMainRFileUri")
    def reset_main_r_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainRFileUri", []))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="mainRFileUriInput")
    def main_r_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainRFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31689b34e7579b462f0dc64d72e01fd6ae1184fb6bb77e05c7338e2379864e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ddcbbb39c01c1495771bf170cd953d8dea29c74650c46a58391b45057b3447)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1bd06896a2cfa80bc48e2a69fd7302b93a1e77b424326b53cafaf37870c163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainRFileUri")
    def main_r_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainRFileUri"))

    @main_r_file_uri.setter
    def main_r_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cfff18e3439f798184fa4cb239156638778dc0ee1d02a1eba056a6490da571b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainRFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocBatchSparkRBatch]:
        return typing.cast(typing.Optional[GoogleDataprocBatchSparkRBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchSparkRBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab90930e73013d9159321702b0d8acc7ded94c778ed9b4513a923c8a917c9fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchSparkSqlBatch",
    jsii_struct_bases=[],
    name_mapping={
        "jar_file_uris": "jarFileUris",
        "query_file_uri": "queryFileUri",
        "query_variables": "queryVariables",
    },
)
class GoogleDataprocBatchSparkSqlBatch:
    def __init__(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        :param query_file_uri: The HCFS URI of the script that contains Spark SQL queries to execute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#query_file_uri GoogleDataprocBatch#query_file_uri}
        :param query_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#query_variables GoogleDataprocBatch#query_variables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91aaa8beb50a742fb3e007197b9777cd9d8ae64142060ba4f8cc2a301e76b144)
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_variables", value=query_variables, expected_type=type_hints["query_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_variables is not None:
            self._values["query_variables"] = query_variables

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to be added to the Spark CLASSPATH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#jar_file_uris GoogleDataprocBatch#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains Spark SQL queries to execute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#query_file_uri GoogleDataprocBatch#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#query_variables GoogleDataprocBatch#query_variables}
        '''
        result = self._values.get("query_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchSparkSqlBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchSparkSqlBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchSparkSqlBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd7e8859cc45099148e613b8fb366193d2e18b9791f832431101424fea0737b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetQueryFileUri")
    def reset_query_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryFileUri", []))

    @jsii.member(jsii_name="resetQueryVariables")
    def reset_query_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryVariables", []))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryVariablesInput")
    def query_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "queryVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__718fc535bfb8fb4e64228853374b36ba80cd2831d2dd61e0273363bdadfd98b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2267ac59243ef070a3c5c0c5529a8f278fed4e7e4d85b77f2b92b9a7d0edfb05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryVariables")
    def query_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "queryVariables"))

    @query_variables.setter
    def query_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8372e85fcec9b46ed477aee0cf095356c33cd55520027cb903594015ab4ced43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocBatchSparkSqlBatch]:
        return typing.cast(typing.Optional[GoogleDataprocBatchSparkSqlBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchSparkSqlBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa0d9a07568261966c8d80ce5fca4f257ce3f8a8ce7f76ba064a73dcd1050986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchStateHistory",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataprocBatchStateHistory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchStateHistory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchStateHistoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchStateHistoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28d571d82189ef0df0dc599ce0d9914b23b54d9a231791a7bba95063b6f30652)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataprocBatchStateHistoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395b4726638b2ec4ad32e015561e40f221214ead13bda4bd91b10c79338a4bac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataprocBatchStateHistoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ec357f031b1ce08f897743f0f2189d616c14c23af098da2912c69000a5d2ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b97741cbf4cf7233f6b3d02ccde1f81f73564801b4ba09a48094ce691574b693)
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
            type_hints = typing.get_type_hints(_typecheckingstub__17260b616543b452a5e9aea4d4bdbf67ce5d06197b92015cac77cfa9d4725ad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataprocBatchStateHistoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchStateHistoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__098d0291b1053ba3168b63085cef10f3a72cd87f79bb146a87e1c0443566feea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="stateStartTime")
    def state_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateStartTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataprocBatchStateHistory]:
        return typing.cast(typing.Optional[GoogleDataprocBatchStateHistory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocBatchStateHistory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ae3cfcd3b693638051227af8d0e09b476f250323598ab89812172f35919f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataprocBatchTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#create GoogleDataprocBatch#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#delete GoogleDataprocBatch#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#update GoogleDataprocBatch#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02861676f072a95659b4fde9475f5f98137bb5ecd8b5b855632dfe5bf57e1f5e)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#create GoogleDataprocBatch#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#delete GoogleDataprocBatch#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_batch#update GoogleDataprocBatch#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocBatchTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocBatchTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocBatch.GoogleDataprocBatchTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c785944ee8b36337c27ef41196d732ca04b54976bf6cf5cd0ccde839be2475ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df36845c3dfc816dd80205cb61b026db566283ee41e3b2e88878886958c5272a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d886fec40ee4386112d972d918b82ce6e8d794e2546e053b038019264eaecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e01e7ba660f1f4e5fc08bed7217267eaffb113914c04e267ea40bb1aa0627e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocBatchTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocBatchTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocBatchTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd16294a1d3721e88be17d54e05645c2b2492c50c762b86815087da77210bc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataprocBatch",
    "GoogleDataprocBatchConfig",
    "GoogleDataprocBatchEnvironmentConfig",
    "GoogleDataprocBatchEnvironmentConfigExecutionConfig",
    "GoogleDataprocBatchEnvironmentConfigExecutionConfigOutputReference",
    "GoogleDataprocBatchEnvironmentConfigOutputReference",
    "GoogleDataprocBatchEnvironmentConfigPeripheralsConfig",
    "GoogleDataprocBatchEnvironmentConfigPeripheralsConfigOutputReference",
    "GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig",
    "GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference",
    "GoogleDataprocBatchPysparkBatch",
    "GoogleDataprocBatchPysparkBatchOutputReference",
    "GoogleDataprocBatchRuntimeConfig",
    "GoogleDataprocBatchRuntimeConfigAutotuningConfig",
    "GoogleDataprocBatchRuntimeConfigAutotuningConfigOutputReference",
    "GoogleDataprocBatchRuntimeConfigOutputReference",
    "GoogleDataprocBatchRuntimeInfo",
    "GoogleDataprocBatchRuntimeInfoApproximateUsage",
    "GoogleDataprocBatchRuntimeInfoApproximateUsageList",
    "GoogleDataprocBatchRuntimeInfoApproximateUsageOutputReference",
    "GoogleDataprocBatchRuntimeInfoCurrentUsage",
    "GoogleDataprocBatchRuntimeInfoCurrentUsageList",
    "GoogleDataprocBatchRuntimeInfoCurrentUsageOutputReference",
    "GoogleDataprocBatchRuntimeInfoList",
    "GoogleDataprocBatchRuntimeInfoOutputReference",
    "GoogleDataprocBatchSparkBatch",
    "GoogleDataprocBatchSparkBatchOutputReference",
    "GoogleDataprocBatchSparkRBatch",
    "GoogleDataprocBatchSparkRBatchOutputReference",
    "GoogleDataprocBatchSparkSqlBatch",
    "GoogleDataprocBatchSparkSqlBatchOutputReference",
    "GoogleDataprocBatchStateHistory",
    "GoogleDataprocBatchStateHistoryList",
    "GoogleDataprocBatchStateHistoryOutputReference",
    "GoogleDataprocBatchTimeouts",
    "GoogleDataprocBatchTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1dee516aa821d1c4dfb7c6b9c0463a1990e8b7511f475a3185a10a00e4ddda7d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    batch_id: typing.Optional[builtins.str] = None,
    environment_config: typing.Optional[typing.Union[GoogleDataprocBatchEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    pyspark_batch: typing.Optional[typing.Union[GoogleDataprocBatchPysparkBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_config: typing.Optional[typing.Union[GoogleDataprocBatchRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_batch: typing.Optional[typing.Union[GoogleDataprocBatchSparkBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_batch: typing.Optional[typing.Union[GoogleDataprocBatchSparkRBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_batch: typing.Optional[typing.Union[GoogleDataprocBatchSparkSqlBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocBatchTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8fe546fdad768fcda3f4d90d0f938698c5a09c05b15e67ac15f9311f4aec78ed(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0a5b3e6ea0d701557e94aed746936fa443ef7e8a9fcb3978097df4f71c7632(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45323daf847c44b90228615ae33272e213b7e2ea0254f8f205107286a54c94d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9340ea39cc0e13285d2f2243432de023feec9bd73b81aa8fb86a69349b8ed0b1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0849fec3b46f74e2b743d91d73ffe9a81970fddb86760398e1600dadfd2bdbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__855f1c56c68d6afdbb0c89af9d9c57429bda142be058d193c0f5cfa84cc45300(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7523b4b2bdf6d3ded1eb0608a05585cae6908595fe5c1b8fec70c3bca6e644(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    batch_id: typing.Optional[builtins.str] = None,
    environment_config: typing.Optional[typing.Union[GoogleDataprocBatchEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    pyspark_batch: typing.Optional[typing.Union[GoogleDataprocBatchPysparkBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_config: typing.Optional[typing.Union[GoogleDataprocBatchRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_batch: typing.Optional[typing.Union[GoogleDataprocBatchSparkBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_batch: typing.Optional[typing.Union[GoogleDataprocBatchSparkRBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_batch: typing.Optional[typing.Union[GoogleDataprocBatchSparkSqlBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocBatchTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9408e89affcb18f9ed18cfaa75820d89833ead8be4d1d8cec54543ce763e3853(
    *,
    execution_config: typing.Optional[typing.Union[GoogleDataprocBatchEnvironmentConfigExecutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    peripherals_config: typing.Optional[typing.Union[GoogleDataprocBatchEnvironmentConfigPeripheralsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8b56d26ff63c476c09c1d632e1fafe2dc0911ca518a0198098b041ab5192b6(
    *,
    kms_key: typing.Optional[builtins.str] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_uri: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    staging_bucket: typing.Optional[builtins.str] = None,
    subnetwork_uri: typing.Optional[builtins.str] = None,
    ttl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a245ad0bb42682dc7e3d708a0fbab97c2fded9981d5a951c2bea911ce25b744a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0833448bdabd0ffe7a7705a0e7fec9ef830748ae11bc4ea90f545a0b57a4c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6093d9e6ec8b34a5226a5c8e8b9992f62ff885a1ce75785418e887189d50468(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9400c54128e6e8a083d117d03beb2da748c480c63450b06644aeba19fc686830(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd89226324a0fc0b78e0d24f07792c9ae304d0a5932b7e95cda38862f5301fe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fff8301ad4d8e53105d65ac610a6cc2acdca318f50042dc56e8e28d1151472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f452b0c3dfb1fe3025e4bb0eca6cb3a4988dad808b9e0a8f702639448ad9fa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ece41f45e6d2f6c6e40da7f32d8299f16854cc087d20a0f5975ec9785579bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d8fca77fc29f9996be71e71676644a7bd9359683e6a4ed537fcd905ad80200(
    value: typing.Optional[GoogleDataprocBatchEnvironmentConfigExecutionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cc92c44334a89ee9c4ed3180dafdcbe0c742d849f15150881257b019f1bd6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be76276a2b1acd4cc1eebea16375210ae6232aadeb44fa2ca8afbe75755cfb86(
    value: typing.Optional[GoogleDataprocBatchEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0181b06adcd0549bd11d7663f6b580f1067d7b6209729bd74a22600829f325(
    *,
    metastore_service: typing.Optional[builtins.str] = None,
    spark_history_server_config: typing.Optional[typing.Union[GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c626aa455ad65a47f089891c00027f21feddc0998f5eca0de56142fb28a2e9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18b0cb2f2053e0aaa2491965a73eeec41893c9a4f1409e87778b6b01739da441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b211e4b1e01ff98e414d3e376783b91fcb60453de56f6aaa04461c9c60645cb(
    value: typing.Optional[GoogleDataprocBatchEnvironmentConfigPeripheralsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b867cac6ed441b00c04dec94f910e73cfb56efa6c674d90cfd68e12e9bf572b(
    *,
    dataproc_cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b7a8c441ad07d6963628512bda6ae050da2aeff6994248d450240ea8e2e31f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85543090118d74f5bf17122ad79fee486112c0d3780ed2209b21124b15e3df52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa94719f876b05c372434f13a9abc5b91ec60df7716f1cefcf35b928f6d36a6(
    value: typing.Optional[GoogleDataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b77c83462681c638f2d944e210099fb74f2aae7401bc390c0be8ba01e0e9bbb(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    main_python_file_uri: typing.Optional[builtins.str] = None,
    python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca13696f1523d000f74890bdc26d3be7d93e8b613a3a3f190cca10213c869e27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b5946e7599417202629e1ecaeed3ba9624f3d3bafde050b456a70dc0d73e84(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6eb06762ba5d8c669b3b02ffe2cb3a441d56d1cb1197d07f9fc927dcc476410(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad8fe303edf1162840b4d8341dd95e5e5d5bd20a4d185efaa0bafa7a8f237e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4af08a9310108714cb1c253192e35ac76d2bdbf6361374e0d669d6d3f1bc1ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515dc43dcb32fd3e5f0fe44af613f393a9ca602f2fb37ae87658145846982b75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca86affb1c7b8607c9b113693049aed340efd0096e153f4e5a518c28326eead(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d99fb24def4bcc4966adf1eef83301d2c540bf461fbeac617fb28058916b62(
    value: typing.Optional[GoogleDataprocBatchPysparkBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff49119b8f8da83b92fddfca02cec7ea62d5a66e80f3eff528deca54988947cf(
    *,
    autotuning_config: typing.Optional[typing.Union[GoogleDataprocBatchRuntimeConfigAutotuningConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cohort: typing.Optional[builtins.str] = None,
    container_image: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59fd30ca40c7faa1c3a4c7e224cae92b414ec055c9bcb5327160787e67d6403b(
    *,
    scenarios: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1741f19713e58b246d7a7b88308c3a685f8bcbc8b0b33742a59ea22745fd5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81464df2b9190dff67e3f93eb09f01b3335ec5d16931ea30f1f52c784b717fb6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce4b45178635bad08c2811972839725d62ae94c98cd962cf62fc5a93a5c10d0(
    value: typing.Optional[GoogleDataprocBatchRuntimeConfigAutotuningConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef76bedbf1127c14c9dc6ac3dc065568fa5632dc2aa6d4d4516817547dc0ef86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8408d967f60a5a745f8910f47eb127fc1124aed82f804604b4ae2fba03d9d7f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64760611c3a9a9fd7609f513df889935c168b84624038264af48eff32627363e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f9cf9821a463189e8a15e800e6a34f70bb0fc12b3cb52fd011521b64303966(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f878eb79215e06d12222b975e70f9c6c813fb467944c00b97e603c15fdc7e5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7002e9ad87a75110a063c02644bf1fa2f06999c1896004daf1a09b4fd33601bf(
    value: typing.Optional[GoogleDataprocBatchRuntimeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4707a13757588a2ad058cc4a8b9612e0df783446358185ddbcd04d2bd0ac43e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dbf5d7196ea1f87632dc5d1160f2f25b2501e2e13ef2c2e9ad5f9d949ea07a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae81d7ec8b09af2eb2df8ee4439ceae720aeec4f1889dc214e2b95203de66aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d574a3cbcb3be40d4e303dfddf4a71254a71c3aea0ef8a83d3a29d96fd1353cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52859a74b8d5de35c15420c933f2289b177d7267b8d00c860fa445ada747b83e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e618e5c107743b4b6738135bc9c235694ca6b2a724b9767349f150e15d5672(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30af8f977947e08a54780a2176856341e0f940eea6216f108c6e20dae8169c19(
    value: typing.Optional[GoogleDataprocBatchRuntimeInfoApproximateUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b52a7bc0fe335f0eba40d9728e81fa4e28af02c669f3e95f4be126b6d2c994b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c2795381630ba134602c0e245daa8d31bd66976260fc3818d9fdb87a9cef9e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d803b12e97ce8b683ec8837f268be4050ffc9855b8a1d783b88591fc31b5189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fb566f01dace0e57fe3fca10bc3963534b419a5a82635592aa415b1af659df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6799eb72c8db3922e5133477527cd6a19fae5ac649fa6584af8dfd9c0703f1cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d1252ab2addbbc06b3d3436f3d4bcc3a370107a1d7891dc26b22c11f5d8510(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34889ed88fcdf4f3cc5ea535480d3663a384eef4f7a267d70ac2449d0aea06dd(
    value: typing.Optional[GoogleDataprocBatchRuntimeInfoCurrentUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36dc4bfa9affd954701787a1923ba501a17bf4770ba52c2c29907d1cb50f009(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347128bbbdbd99647a589a828d2ca49440c1631b461b264b07d364af115157ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883d715d50e8a54ec4fcc231ecb6908f2c4da594fed6de9f11f3cc62f5d6d097(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168b7a91e7b6575854f4459be9ac300eaab1010533dd2c5076d9dd0bbf0f8915(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7846ba6a215f9862b64f3a00609188616c4c87f01910f53cd431a1ea33bda8b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fec2359b40dabb4602dd68341614d24b310d672bf867bc9210d0054bd217670(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c127d9507bbefbb4c64b64eb6e8bdbef9c32c9526a7d71717a43aba2d03b8a8(
    value: typing.Optional[GoogleDataprocBatchRuntimeInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b0997ed51925db7c9d6140ab84f40bbace5c990c64ced3064310d1858cde0c(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    main_class: typing.Optional[builtins.str] = None,
    main_jar_file_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b2829100bee5a6c550218f13b438797bb5f6b6014af93a734886fa1c3daab5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60c726ec36fa7954c55c0fa9bda1f50cc184e676fcf7764857704683dee315a8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec8a891cba380df5379e3f3d2ef8d7b524cb17fe59461be340d6258db5029fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43bd70b14080944d648b51fd13fa30f5409673ca21ac22bb998bcb1ebbdb598(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b72f831686d243564ecdcf1c652a3a4e9e2f21cdafae9034a897da7a8fd99b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db435b9cd970597b73f18ef4d84f70983ff999e46a0fcb81b4079b997681b7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__713bba1dc680948ca88fa0ec731d13bf09ee3f0c01f4217f43d65bf89064ccfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d60e209ba4dacafb89429fd0b68e4657c3100bd82279957e2e4736dfdfa471(
    value: typing.Optional[GoogleDataprocBatchSparkBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e92c168aa84cb92c0bc3915e455376de03baac8f092a22eda7af372fe872bdb(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    main_r_file_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea9b339197c22a64692566602a7f1193a7c5815e2f81cda2dcc5d236d94bd6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31689b34e7579b462f0dc64d72e01fd6ae1184fb6bb77e05c7338e2379864e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ddcbbb39c01c1495771bf170cd953d8dea29c74650c46a58391b45057b3447(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1bd06896a2cfa80bc48e2a69fd7302b93a1e77b424326b53cafaf37870c163(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cfff18e3439f798184fa4cb239156638778dc0ee1d02a1eba056a6490da571b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab90930e73013d9159321702b0d8acc7ded94c778ed9b4513a923c8a917c9fd1(
    value: typing.Optional[GoogleDataprocBatchSparkRBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91aaa8beb50a742fb3e007197b9777cd9d8ae64142060ba4f8cc2a301e76b144(
    *,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7e8859cc45099148e613b8fb366193d2e18b9791f832431101424fea0737b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__718fc535bfb8fb4e64228853374b36ba80cd2831d2dd61e0273363bdadfd98b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2267ac59243ef070a3c5c0c5529a8f278fed4e7e4d85b77f2b92b9a7d0edfb05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8372e85fcec9b46ed477aee0cf095356c33cd55520027cb903594015ab4ced43(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0d9a07568261966c8d80ce5fca4f257ce3f8a8ce7f76ba064a73dcd1050986(
    value: typing.Optional[GoogleDataprocBatchSparkSqlBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d571d82189ef0df0dc599ce0d9914b23b54d9a231791a7bba95063b6f30652(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395b4726638b2ec4ad32e015561e40f221214ead13bda4bd91b10c79338a4bac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ec357f031b1ce08f897743f0f2189d616c14c23af098da2912c69000a5d2ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b97741cbf4cf7233f6b3d02ccde1f81f73564801b4ba09a48094ce691574b693(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17260b616543b452a5e9aea4d4bdbf67ce5d06197b92015cac77cfa9d4725ad4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098d0291b1053ba3168b63085cef10f3a72cd87f79bb146a87e1c0443566feea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ae3cfcd3b693638051227af8d0e09b476f250323598ab89812172f35919f63(
    value: typing.Optional[GoogleDataprocBatchStateHistory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02861676f072a95659b4fde9475f5f98137bb5ecd8b5b855632dfe5bf57e1f5e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c785944ee8b36337c27ef41196d732ca04b54976bf6cf5cd0ccde839be2475ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df36845c3dfc816dd80205cb61b026db566283ee41e3b2e88878886958c5272a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d886fec40ee4386112d972d918b82ce6e8d794e2546e053b038019264eaecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e01e7ba660f1f4e5fc08bed7217267eaffb113914c04e267ea40bb1aa0627e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd16294a1d3721e88be17d54e05645c2b2492c50c762b86815087da77210bc4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocBatchTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

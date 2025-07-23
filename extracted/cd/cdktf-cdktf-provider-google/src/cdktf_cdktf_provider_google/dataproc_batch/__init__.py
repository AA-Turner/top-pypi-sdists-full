r'''
# `google_dataproc_batch`

Refer to the Terraform Registry for docs: [`google_dataproc_batch`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch).
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


class DataprocBatch(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatch",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch google_dataproc_batch}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        batch_id: typing.Optional[builtins.str] = None,
        environment_config: typing.Optional[typing.Union["DataprocBatchEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        pyspark_batch: typing.Optional[typing.Union["DataprocBatchPysparkBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_config: typing.Optional[typing.Union["DataprocBatchRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_batch: typing.Optional[typing.Union["DataprocBatchSparkBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_batch: typing.Optional[typing.Union["DataprocBatchSparkRBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_batch: typing.Optional[typing.Union["DataprocBatchSparkSqlBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocBatchTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch google_dataproc_batch} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param batch_id: The ID to use for the batch, which will become the final component of the batch's resource name. This value must be 4-63 characters. Valid characters are /[a-z][0-9]-/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#batch_id DataprocBatch#batch_id}
        :param environment_config: environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#environment_config DataprocBatch#environment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#id DataprocBatch#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this batch. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#labels DataprocBatch#labels}
        :param location: The location in which the batch will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#location DataprocBatch#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#project DataprocBatch#project}.
        :param pyspark_batch: pyspark_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#pyspark_batch DataprocBatch#pyspark_batch}
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#runtime_config DataprocBatch#runtime_config}
        :param spark_batch: spark_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_batch DataprocBatch#spark_batch}
        :param spark_r_batch: spark_r_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_r_batch DataprocBatch#spark_r_batch}
        :param spark_sql_batch: spark_sql_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_sql_batch DataprocBatch#spark_sql_batch}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#timeouts DataprocBatch#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725de29c9d11fb44f4a1619714f1600b8c458787b6f9c2d0f3f6fe5ffa0f1a53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataprocBatchConfig(
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
        '''Generates CDKTF code for importing a DataprocBatch resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataprocBatch to import.
        :param import_from_id: The id of the existing DataprocBatch that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataprocBatch to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b7bd6d43b30304b989f63b127ba7701a4f0c24f647970aba16240f9daa47194)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEnvironmentConfig")
    def put_environment_config(
        self,
        *,
        execution_config: typing.Optional[typing.Union["DataprocBatchEnvironmentConfigExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peripherals_config: typing.Optional[typing.Union["DataprocBatchEnvironmentConfigPeripheralsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_config: execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#execution_config DataprocBatch#execution_config}
        :param peripherals_config: peripherals_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#peripherals_config DataprocBatch#peripherals_config}
        '''
        value = DataprocBatchEnvironmentConfig(
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        :param main_python_file_uri: The HCFS URI of the main Python file to use as the Spark driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_python_file_uri DataprocBatch#main_python_file_uri}
        :param python_file_uris: HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#python_file_uris DataprocBatch#python_file_uris}
        '''
        value = DataprocBatchPysparkBatch(
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
        autotuning_config: typing.Optional[typing.Union["DataprocBatchRuntimeConfigAutotuningConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cohort: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param autotuning_config: autotuning_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#autotuning_config DataprocBatch#autotuning_config}
        :param cohort: Optional. Cohort identifier. Identifies families of the workloads having the same shape, e.g. daily ETL jobs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#cohort DataprocBatch#cohort}
        :param container_image: Optional custom container image for the job runtime environment. If not specified, a default container image will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#container_image DataprocBatch#container_image}
        :param properties: A mapping of property names to values, which are used to configure workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#properties DataprocBatch#properties}
        :param version: Version of the batch runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#version DataprocBatch#version}
        '''
        value = DataprocBatchRuntimeConfig(
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        :param main_class: The name of the driver main class. The jar file that contains the class must be in the classpath or specified in jarFileUris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_class DataprocBatch#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_jar_file_uri DataprocBatch#main_jar_file_uri}
        '''
        value = DataprocBatchSparkBatch(
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        :param main_r_file_uri: The HCFS URI of the main R file to use as the driver. Must be a .R or .r file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_r_file_uri DataprocBatch#main_r_file_uri}
        '''
        value = DataprocBatchSparkRBatch(
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
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        :param query_file_uri: The HCFS URI of the script that contains Spark SQL queries to execute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#query_file_uri DataprocBatch#query_file_uri}
        :param query_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#query_variables DataprocBatch#query_variables}
        '''
        value = DataprocBatchSparkSqlBatch(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#create DataprocBatch#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#delete DataprocBatch#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#update DataprocBatch#update}.
        '''
        value = DataprocBatchTimeouts(create=create, delete=delete, update=update)

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
    def environment_config(self) -> "DataprocBatchEnvironmentConfigOutputReference":
        return typing.cast("DataprocBatchEnvironmentConfigOutputReference", jsii.get(self, "environmentConfig"))

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
    def pyspark_batch(self) -> "DataprocBatchPysparkBatchOutputReference":
        return typing.cast("DataprocBatchPysparkBatchOutputReference", jsii.get(self, "pysparkBatch"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfig")
    def runtime_config(self) -> "DataprocBatchRuntimeConfigOutputReference":
        return typing.cast("DataprocBatchRuntimeConfigOutputReference", jsii.get(self, "runtimeConfig"))

    @builtins.property
    @jsii.member(jsii_name="runtimeInfo")
    def runtime_info(self) -> "DataprocBatchRuntimeInfoList":
        return typing.cast("DataprocBatchRuntimeInfoList", jsii.get(self, "runtimeInfo"))

    @builtins.property
    @jsii.member(jsii_name="sparkBatch")
    def spark_batch(self) -> "DataprocBatchSparkBatchOutputReference":
        return typing.cast("DataprocBatchSparkBatchOutputReference", jsii.get(self, "sparkBatch"))

    @builtins.property
    @jsii.member(jsii_name="sparkRBatch")
    def spark_r_batch(self) -> "DataprocBatchSparkRBatchOutputReference":
        return typing.cast("DataprocBatchSparkRBatchOutputReference", jsii.get(self, "sparkRBatch"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlBatch")
    def spark_sql_batch(self) -> "DataprocBatchSparkSqlBatchOutputReference":
        return typing.cast("DataprocBatchSparkSqlBatchOutputReference", jsii.get(self, "sparkSqlBatch"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateHistory")
    def state_history(self) -> "DataprocBatchStateHistoryList":
        return typing.cast("DataprocBatchStateHistoryList", jsii.get(self, "stateHistory"))

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
    def timeouts(self) -> "DataprocBatchTimeoutsOutputReference":
        return typing.cast("DataprocBatchTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["DataprocBatchEnvironmentConfig"]:
        return typing.cast(typing.Optional["DataprocBatchEnvironmentConfig"], jsii.get(self, "environmentConfigInput"))

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
    def pyspark_batch_input(self) -> typing.Optional["DataprocBatchPysparkBatch"]:
        return typing.cast(typing.Optional["DataprocBatchPysparkBatch"], jsii.get(self, "pysparkBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeConfigInput")
    def runtime_config_input(self) -> typing.Optional["DataprocBatchRuntimeConfig"]:
        return typing.cast(typing.Optional["DataprocBatchRuntimeConfig"], jsii.get(self, "runtimeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkBatchInput")
    def spark_batch_input(self) -> typing.Optional["DataprocBatchSparkBatch"]:
        return typing.cast(typing.Optional["DataprocBatchSparkBatch"], jsii.get(self, "sparkBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkRBatchInput")
    def spark_r_batch_input(self) -> typing.Optional["DataprocBatchSparkRBatch"]:
        return typing.cast(typing.Optional["DataprocBatchSparkRBatch"], jsii.get(self, "sparkRBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlBatchInput")
    def spark_sql_batch_input(self) -> typing.Optional["DataprocBatchSparkSqlBatch"]:
        return typing.cast(typing.Optional["DataprocBatchSparkSqlBatch"], jsii.get(self, "sparkSqlBatchInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocBatchTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocBatchTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="batchId")
    def batch_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "batchId"))

    @batch_id.setter
    def batch_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d5c16b40f34fd44abcf260e6722c5effcbdd1cb078599addc019532561fffc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "batchId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3394fa37ab41d0a7268e3c15fd26c977ebf9d272254fcf7bc898f59fe10aebe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f0c7d79431162397e945d056cf933c54db9f103a9397303bc878eecb0839b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__061764b113e3791281f17a998a03f879ffbde169b2b5a5e6f2a56a38399f59ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a75de19a58913f5a991165962d498a7a58096f4e589fae8803dfe28cf2e659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchConfig",
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
class DataprocBatchConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        environment_config: typing.Optional[typing.Union["DataprocBatchEnvironmentConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        pyspark_batch: typing.Optional[typing.Union["DataprocBatchPysparkBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_config: typing.Optional[typing.Union["DataprocBatchRuntimeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_batch: typing.Optional[typing.Union["DataprocBatchSparkBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_batch: typing.Optional[typing.Union["DataprocBatchSparkRBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_batch: typing.Optional[typing.Union["DataprocBatchSparkSqlBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocBatchTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param batch_id: The ID to use for the batch, which will become the final component of the batch's resource name. This value must be 4-63 characters. Valid characters are /[a-z][0-9]-/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#batch_id DataprocBatch#batch_id}
        :param environment_config: environment_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#environment_config DataprocBatch#environment_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#id DataprocBatch#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this batch. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#labels DataprocBatch#labels}
        :param location: The location in which the batch will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#location DataprocBatch#location}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#project DataprocBatch#project}.
        :param pyspark_batch: pyspark_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#pyspark_batch DataprocBatch#pyspark_batch}
        :param runtime_config: runtime_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#runtime_config DataprocBatch#runtime_config}
        :param spark_batch: spark_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_batch DataprocBatch#spark_batch}
        :param spark_r_batch: spark_r_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_r_batch DataprocBatch#spark_r_batch}
        :param spark_sql_batch: spark_sql_batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_sql_batch DataprocBatch#spark_sql_batch}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#timeouts DataprocBatch#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(environment_config, dict):
            environment_config = DataprocBatchEnvironmentConfig(**environment_config)
        if isinstance(pyspark_batch, dict):
            pyspark_batch = DataprocBatchPysparkBatch(**pyspark_batch)
        if isinstance(runtime_config, dict):
            runtime_config = DataprocBatchRuntimeConfig(**runtime_config)
        if isinstance(spark_batch, dict):
            spark_batch = DataprocBatchSparkBatch(**spark_batch)
        if isinstance(spark_r_batch, dict):
            spark_r_batch = DataprocBatchSparkRBatch(**spark_r_batch)
        if isinstance(spark_sql_batch, dict):
            spark_sql_batch = DataprocBatchSparkSqlBatch(**spark_sql_batch)
        if isinstance(timeouts, dict):
            timeouts = DataprocBatchTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c68b64a05a87b3d483b326087e63b434e760d95f3c32bbad5fc06f4687d33a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#batch_id DataprocBatch#batch_id}
        '''
        result = self._values.get("batch_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_config(self) -> typing.Optional["DataprocBatchEnvironmentConfig"]:
        '''environment_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#environment_config DataprocBatch#environment_config}
        '''
        result = self._values.get("environment_config")
        return typing.cast(typing.Optional["DataprocBatchEnvironmentConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#id DataprocBatch#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#labels DataprocBatch#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location in which the batch will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#location DataprocBatch#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#project DataprocBatch#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pyspark_batch(self) -> typing.Optional["DataprocBatchPysparkBatch"]:
        '''pyspark_batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#pyspark_batch DataprocBatch#pyspark_batch}
        '''
        result = self._values.get("pyspark_batch")
        return typing.cast(typing.Optional["DataprocBatchPysparkBatch"], result)

    @builtins.property
    def runtime_config(self) -> typing.Optional["DataprocBatchRuntimeConfig"]:
        '''runtime_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#runtime_config DataprocBatch#runtime_config}
        '''
        result = self._values.get("runtime_config")
        return typing.cast(typing.Optional["DataprocBatchRuntimeConfig"], result)

    @builtins.property
    def spark_batch(self) -> typing.Optional["DataprocBatchSparkBatch"]:
        '''spark_batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_batch DataprocBatch#spark_batch}
        '''
        result = self._values.get("spark_batch")
        return typing.cast(typing.Optional["DataprocBatchSparkBatch"], result)

    @builtins.property
    def spark_r_batch(self) -> typing.Optional["DataprocBatchSparkRBatch"]:
        '''spark_r_batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_r_batch DataprocBatch#spark_r_batch}
        '''
        result = self._values.get("spark_r_batch")
        return typing.cast(typing.Optional["DataprocBatchSparkRBatch"], result)

    @builtins.property
    def spark_sql_batch(self) -> typing.Optional["DataprocBatchSparkSqlBatch"]:
        '''spark_sql_batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_sql_batch DataprocBatch#spark_sql_batch}
        '''
        result = self._values.get("spark_sql_batch")
        return typing.cast(typing.Optional["DataprocBatchSparkSqlBatch"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataprocBatchTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#timeouts DataprocBatch#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataprocBatchTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchEnvironmentConfig",
    jsii_struct_bases=[],
    name_mapping={
        "execution_config": "executionConfig",
        "peripherals_config": "peripheralsConfig",
    },
)
class DataprocBatchEnvironmentConfig:
    def __init__(
        self,
        *,
        execution_config: typing.Optional[typing.Union["DataprocBatchEnvironmentConfigExecutionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        peripherals_config: typing.Optional[typing.Union["DataprocBatchEnvironmentConfigPeripheralsConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_config: execution_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#execution_config DataprocBatch#execution_config}
        :param peripherals_config: peripherals_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#peripherals_config DataprocBatch#peripherals_config}
        '''
        if isinstance(execution_config, dict):
            execution_config = DataprocBatchEnvironmentConfigExecutionConfig(**execution_config)
        if isinstance(peripherals_config, dict):
            peripherals_config = DataprocBatchEnvironmentConfigPeripheralsConfig(**peripherals_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0555ea3eeb600c2ce28a1c2068d82bc9264e9bc79daf86e2ee45c0f43e8c8c2)
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
    ) -> typing.Optional["DataprocBatchEnvironmentConfigExecutionConfig"]:
        '''execution_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#execution_config DataprocBatch#execution_config}
        '''
        result = self._values.get("execution_config")
        return typing.cast(typing.Optional["DataprocBatchEnvironmentConfigExecutionConfig"], result)

    @builtins.property
    def peripherals_config(
        self,
    ) -> typing.Optional["DataprocBatchEnvironmentConfigPeripheralsConfig"]:
        '''peripherals_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#peripherals_config DataprocBatch#peripherals_config}
        '''
        result = self._values.get("peripherals_config")
        return typing.cast(typing.Optional["DataprocBatchEnvironmentConfigPeripheralsConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchEnvironmentConfigExecutionConfig",
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
class DataprocBatchEnvironmentConfigExecutionConfig:
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
        :param kms_key: The Cloud KMS key to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#kms_key DataprocBatch#kms_key}
        :param network_tags: Tags used for network traffic control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#network_tags DataprocBatch#network_tags}
        :param network_uri: Network configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#network_uri DataprocBatch#network_uri}
        :param service_account: Service account that used to execute workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#service_account DataprocBatch#service_account}
        :param staging_bucket: A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running, and then create and manage project-level, per-location staging and temporary buckets. This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#staging_bucket DataprocBatch#staging_bucket}
        :param subnetwork_uri: Subnetwork configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#subnetwork_uri DataprocBatch#subnetwork_uri}
        :param ttl: The duration after which the workload will be terminated. When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing work to finish. If ttl is not specified for a batch workload, the workload will be allowed to run until it exits naturally (or run forever without exiting). If ttl is not specified for an interactive session, it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours. Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session), the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or when ttl has been exceeded, whichever occurs first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#ttl DataprocBatch#ttl}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8a8fae405e7ec873f2e8dc4c8f521894610c2a4f4341df7d5e7ec99d99124e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#kms_key DataprocBatch#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags used for network traffic control.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#network_tags DataprocBatch#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_uri(self) -> typing.Optional[builtins.str]:
        '''Network configuration for workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#network_uri DataprocBatch#network_uri}
        '''
        result = self._values.get("network_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Service account that used to execute workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#service_account DataprocBatch#service_account}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#staging_bucket DataprocBatch#staging_bucket}
        '''
        result = self._values.get("staging_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork_uri(self) -> typing.Optional[builtins.str]:
        '''Subnetwork configuration for workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#subnetwork_uri DataprocBatch#subnetwork_uri}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#ttl DataprocBatch#ttl}
        '''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchEnvironmentConfigExecutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchEnvironmentConfigExecutionConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchEnvironmentConfigExecutionConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__096ae0ad3687307130ab575b382601d9bf6a07b29bf23696db0120f9124547c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af8027e0b1785d4e1bee0150a75c924b8d2024860d77f0801235133a8d8b1d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc7eee489dcf75a57b7587c882e921bb63feab3a12dd977a91a2cc01a2a1a6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkUri")
    def network_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkUri"))

    @network_uri.setter
    def network_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625934dd0a201f71b7ab241cfaf921c7ef5f89294588894bcbc491f3bae26c8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0117f0027147607595d38327948a0ca44ede813cc98335a1a8fdf91081dc45b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stagingBucket")
    def staging_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stagingBucket"))

    @staging_bucket.setter
    def staging_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a154ab2278c9ee784e1f818554e1f186c4b5f2ab8f54d4daf63a12a6ec95669c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stagingBucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetworkUri")
    def subnetwork_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetworkUri"))

    @subnetwork_uri.setter
    def subnetwork_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c478c5c37ffa6456b1d9f18ad227fc94f51b3ed7ecad084db90d684b86d275eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetworkUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b2ce51089ffa12e964774d79921bbc46517ff54f47953c5b6cdf728e54ff10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocBatchEnvironmentConfigExecutionConfig]:
        return typing.cast(typing.Optional[DataprocBatchEnvironmentConfigExecutionConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchEnvironmentConfigExecutionConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1a2b551c645278221cc8c2e3d1465c355753c0052822f95a3a2cb9ce207e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocBatchEnvironmentConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchEnvironmentConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f7dc7f47bcc5beaf69ac51690cc251e51817dcb8438f19419dc8b6f6d295e7a)
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
        :param kms_key: The Cloud KMS key to use for encryption. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#kms_key DataprocBatch#kms_key}
        :param network_tags: Tags used for network traffic control. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#network_tags DataprocBatch#network_tags}
        :param network_uri: Network configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#network_uri DataprocBatch#network_uri}
        :param service_account: Service account that used to execute workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#service_account DataprocBatch#service_account}
        :param staging_bucket: A Cloud Storage bucket used to stage workload dependencies, config files, and store workload output and other ephemeral data, such as Spark history files. If you do not specify a staging bucket, Cloud Dataproc will determine a Cloud Storage location according to the region where your workload is running, and then create and manage project-level, per-location staging and temporary buckets. This field requires a Cloud Storage bucket name, not a gs://... URI to a Cloud Storage bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#staging_bucket DataprocBatch#staging_bucket}
        :param subnetwork_uri: Subnetwork configuration for workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#subnetwork_uri DataprocBatch#subnetwork_uri}
        :param ttl: The duration after which the workload will be terminated. When the workload exceeds this duration, it will be unconditionally terminated without waiting for ongoing work to finish. If ttl is not specified for a batch workload, the workload will be allowed to run until it exits naturally (or run forever without exiting). If ttl is not specified for an interactive session, it defaults to 24 hours. If ttl is not specified for a batch that uses 2.1+ runtime version, it defaults to 4 hours. Minimum value is 10 minutes; maximum value is 14 days. If both ttl and idleTtl are specified (for an interactive session), the conditions are treated as OR conditions: the workload will be terminated when it has been idle for idleTtl or when ttl has been exceeded, whichever occurs first. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#ttl DataprocBatch#ttl}
        '''
        value = DataprocBatchEnvironmentConfigExecutionConfig(
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
        spark_history_server_config: typing.Optional[typing.Union["DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#metastore_service DataprocBatch#metastore_service}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_history_server_config DataprocBatch#spark_history_server_config}
        '''
        value = DataprocBatchEnvironmentConfigPeripheralsConfig(
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
    ) -> DataprocBatchEnvironmentConfigExecutionConfigOutputReference:
        return typing.cast(DataprocBatchEnvironmentConfigExecutionConfigOutputReference, jsii.get(self, "executionConfig"))

    @builtins.property
    @jsii.member(jsii_name="peripheralsConfig")
    def peripherals_config(
        self,
    ) -> "DataprocBatchEnvironmentConfigPeripheralsConfigOutputReference":
        return typing.cast("DataprocBatchEnvironmentConfigPeripheralsConfigOutputReference", jsii.get(self, "peripheralsConfig"))

    @builtins.property
    @jsii.member(jsii_name="executionConfigInput")
    def execution_config_input(
        self,
    ) -> typing.Optional[DataprocBatchEnvironmentConfigExecutionConfig]:
        return typing.cast(typing.Optional[DataprocBatchEnvironmentConfigExecutionConfig], jsii.get(self, "executionConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="peripheralsConfigInput")
    def peripherals_config_input(
        self,
    ) -> typing.Optional["DataprocBatchEnvironmentConfigPeripheralsConfig"]:
        return typing.cast(typing.Optional["DataprocBatchEnvironmentConfigPeripheralsConfig"], jsii.get(self, "peripheralsConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocBatchEnvironmentConfig]:
        return typing.cast(typing.Optional[DataprocBatchEnvironmentConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchEnvironmentConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da2000b2dcfefd653cd9a9dfd21c6b70e2622119041169abfb03c1fea78ff441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchEnvironmentConfigPeripheralsConfig",
    jsii_struct_bases=[],
    name_mapping={
        "metastore_service": "metastoreService",
        "spark_history_server_config": "sparkHistoryServerConfig",
    },
)
class DataprocBatchEnvironmentConfigPeripheralsConfig:
    def __init__(
        self,
        *,
        metastore_service: typing.Optional[builtins.str] = None,
        spark_history_server_config: typing.Optional[typing.Union["DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param metastore_service: Resource name of an existing Dataproc Metastore service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#metastore_service DataprocBatch#metastore_service}
        :param spark_history_server_config: spark_history_server_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_history_server_config DataprocBatch#spark_history_server_config}
        '''
        if isinstance(spark_history_server_config, dict):
            spark_history_server_config = DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(**spark_history_server_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100edde5643f533d359805642a869dffdf7b691597044f505b06daef5dd6ad8b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#metastore_service DataprocBatch#metastore_service}
        '''
        result = self._values.get("metastore_service")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_history_server_config(
        self,
    ) -> typing.Optional["DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"]:
        '''spark_history_server_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#spark_history_server_config DataprocBatch#spark_history_server_config}
        '''
        result = self._values.get("spark_history_server_config")
        return typing.cast(typing.Optional["DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchEnvironmentConfigPeripheralsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchEnvironmentConfigPeripheralsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchEnvironmentConfigPeripheralsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6cbc058a147ccd95824ba39eecfd9721b947aef7971c9c735d09a005b75bd3)
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
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#dataproc_cluster DataprocBatch#dataproc_cluster}
        '''
        value = DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(
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
    ) -> "DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference":
        return typing.cast("DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference", jsii.get(self, "sparkHistoryServerConfig"))

    @builtins.property
    @jsii.member(jsii_name="metastoreServiceInput")
    def metastore_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metastoreServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkHistoryServerConfigInput")
    def spark_history_server_config_input(
        self,
    ) -> typing.Optional["DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"]:
        return typing.cast(typing.Optional["DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig"], jsii.get(self, "sparkHistoryServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreService")
    def metastore_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metastoreService"))

    @metastore_service.setter
    def metastore_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37130bfbf9fde3e8da658a9cfa338f5eda6777862d7f71b3042cf65f6e2ff6bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metastoreService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocBatchEnvironmentConfigPeripheralsConfig]:
        return typing.cast(typing.Optional[DataprocBatchEnvironmentConfigPeripheralsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchEnvironmentConfigPeripheralsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a07f5ed80e17ed619cb0c540038d89ff06c69c614f40f62e86250e434115d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig",
    jsii_struct_bases=[],
    name_mapping={"dataproc_cluster": "dataprocCluster"},
)
class DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig:
    def __init__(
        self,
        *,
        dataproc_cluster: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dataproc_cluster: Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#dataproc_cluster DataprocBatch#dataproc_cluster}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1d8793206a74b9ef918ed7e5a1df6179e82fdcf728151f6420d43aff780d65)
            check_type(argname="argument dataproc_cluster", value=dataproc_cluster, expected_type=type_hints["dataproc_cluster"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataproc_cluster is not None:
            self._values["dataproc_cluster"] = dataproc_cluster

    @builtins.property
    def dataproc_cluster(self) -> typing.Optional[builtins.str]:
        '''Resource name of an existing Dataproc Cluster to act as a Spark History Server for the workload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#dataproc_cluster DataprocBatch#dataproc_cluster}
        '''
        result = self._values.get("dataproc_cluster")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59d19ecaa6bc66da62497bbb9ca5714d1ff7960cba3e6320622d2ecdb4382dd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__060e324e0ac12c97571e1d297fb6f17e1b356d1a32cc86be735ceac784b4b607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataprocCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig]:
        return typing.cast(typing.Optional[DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7fb544f5b71c88cd8fcd5131708d70dd215b87ef9e8cc0e9cf5bfdee2cc67e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchPysparkBatch",
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
class DataprocBatchPysparkBatch:
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        :param main_python_file_uri: The HCFS URI of the main Python file to use as the Spark driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_python_file_uri DataprocBatch#main_python_file_uri}
        :param python_file_uris: HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#python_file_uris DataprocBatch#python_file_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef14e04ce4a4b6819a6df6bb32aa091b128c1035e787f732bb6fd33c267c2262)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments that can be set as batch
        properties, such as --conf, since a collision can occur that causes an incorrect batch submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the classpath of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_python_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the main Python file to use as the Spark driver. Must be a .py file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_python_file_uri DataprocBatch#main_python_file_uri}
        '''
        result = self._values.get("main_python_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#python_file_uris DataprocBatch#python_file_uris}
        '''
        result = self._values.get("python_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchPysparkBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchPysparkBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchPysparkBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca7d212e66860c68d29b84d511f95887ce7e1fab274efa3a2812a1392a7d855e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__58831538b28532d4b17e0faaef761f3cacc66e10c100782fbc93f55cc67286f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eacc394ea0d0af4070bec61b53ef87be4260dfa0b0a146cf0c91936d06579307)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee82a085d4104ec07fcb0ddd712363212d3712a41f3f5993491ba79b4c986e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88df5b5a45da80abce093274bbf9e86b280699caf23080b6038d3d298c40000b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUri")
    def main_python_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainPythonFileUri"))

    @main_python_file_uri.setter
    def main_python_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__024e6fec372ff08a288bb169ce3ce4e56b1cd8fd5ace86b9693c97d6e32c728a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainPythonFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonFileUris")
    def python_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonFileUris"))

    @python_file_uris.setter
    def python_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1687301891c1319089d0ca07023a60d5ecdbb5fba054f3259fd64d3878f12d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocBatchPysparkBatch]:
        return typing.cast(typing.Optional[DataprocBatchPysparkBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocBatchPysparkBatch]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c7d23ee265075636ccf91f9c79de8b92f9faa041425ea28942f48fec883f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "autotuning_config": "autotuningConfig",
        "cohort": "cohort",
        "container_image": "containerImage",
        "properties": "properties",
        "version": "version",
    },
)
class DataprocBatchRuntimeConfig:
    def __init__(
        self,
        *,
        autotuning_config: typing.Optional[typing.Union["DataprocBatchRuntimeConfigAutotuningConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        cohort: typing.Optional[builtins.str] = None,
        container_image: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param autotuning_config: autotuning_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#autotuning_config DataprocBatch#autotuning_config}
        :param cohort: Optional. Cohort identifier. Identifies families of the workloads having the same shape, e.g. daily ETL jobs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#cohort DataprocBatch#cohort}
        :param container_image: Optional custom container image for the job runtime environment. If not specified, a default container image will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#container_image DataprocBatch#container_image}
        :param properties: A mapping of property names to values, which are used to configure workload execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#properties DataprocBatch#properties}
        :param version: Version of the batch runtime. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#version DataprocBatch#version}
        '''
        if isinstance(autotuning_config, dict):
            autotuning_config = DataprocBatchRuntimeConfigAutotuningConfig(**autotuning_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8830ab03df5b23036e5793fc94b7e0aea522d284cd8ce0ba68f71638c3f0ec8d)
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
    ) -> typing.Optional["DataprocBatchRuntimeConfigAutotuningConfig"]:
        '''autotuning_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#autotuning_config DataprocBatch#autotuning_config}
        '''
        result = self._values.get("autotuning_config")
        return typing.cast(typing.Optional["DataprocBatchRuntimeConfigAutotuningConfig"], result)

    @builtins.property
    def cohort(self) -> typing.Optional[builtins.str]:
        '''Optional. Cohort identifier. Identifies families of the workloads having the same shape, e.g. daily ETL jobs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#cohort DataprocBatch#cohort}
        '''
        result = self._values.get("cohort")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_image(self) -> typing.Optional[builtins.str]:
        '''Optional custom container image for the job runtime environment. If not specified, a default container image will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#container_image DataprocBatch#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values, which are used to configure workload execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#properties DataprocBatch#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''Version of the batch runtime.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#version DataprocBatch#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchRuntimeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeConfigAutotuningConfig",
    jsii_struct_bases=[],
    name_mapping={"scenarios": "scenarios"},
)
class DataprocBatchRuntimeConfigAutotuningConfig:
    def __init__(
        self,
        *,
        scenarios: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scenarios: Optional. Scenarios for which tunings are applied. Possible values: ["SCALING", "BROADCAST_HASH_JOIN", "MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#scenarios DataprocBatch#scenarios}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7e9a949bbddd324dcf55886f4b92a66bed3062c1e69fa3b3bc353ce6f7b97fa)
            check_type(argname="argument scenarios", value=scenarios, expected_type=type_hints["scenarios"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scenarios is not None:
            self._values["scenarios"] = scenarios

    @builtins.property
    def scenarios(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Scenarios for which tunings are applied. Possible values: ["SCALING", "BROADCAST_HASH_JOIN", "MEMORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#scenarios DataprocBatch#scenarios}
        '''
        result = self._values.get("scenarios")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchRuntimeConfigAutotuningConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchRuntimeConfigAutotuningConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeConfigAutotuningConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de42d528d97f699bea56fef1132958143942584bf449962885a9300b560b6686)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4b9405faf77885e734d872f8e7cf25d56771d0197f62ca8c92493e585c0c030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scenarios", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocBatchRuntimeConfigAutotuningConfig]:
        return typing.cast(typing.Optional[DataprocBatchRuntimeConfigAutotuningConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchRuntimeConfigAutotuningConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d33dbde1a9b4f115a63633a021d77afe1e2fe60e17660725af4801bfda536f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocBatchRuntimeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c7f06d8af8162e2723198d81f039b90ebfabe31a6e383c7d39bc1d609c22d98)
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
        :param scenarios: Optional. Scenarios for which tunings are applied. Possible values: ["SCALING", "BROADCAST_HASH_JOIN", "MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#scenarios DataprocBatch#scenarios}
        '''
        value = DataprocBatchRuntimeConfigAutotuningConfig(scenarios=scenarios)

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
    ) -> DataprocBatchRuntimeConfigAutotuningConfigOutputReference:
        return typing.cast(DataprocBatchRuntimeConfigAutotuningConfigOutputReference, jsii.get(self, "autotuningConfig"))

    @builtins.property
    @jsii.member(jsii_name="effectiveProperties")
    def effective_properties(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveProperties"))

    @builtins.property
    @jsii.member(jsii_name="autotuningConfigInput")
    def autotuning_config_input(
        self,
    ) -> typing.Optional[DataprocBatchRuntimeConfigAutotuningConfig]:
        return typing.cast(typing.Optional[DataprocBatchRuntimeConfigAutotuningConfig], jsii.get(self, "autotuningConfigInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4d3ec67d6e3ee73c56c370ffa34d0a276908c90a17a3e83bee2fb6c24c3520ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cohort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerImage"))

    @container_image.setter
    def container_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab582d51ebf3d8a4fbffd45f83ce35fe6ff3fc479f2e524c828d03e17dc94c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17508f2492806092ed4a4ab2a56be4839bafe1d4b88537f66790f519d158ace)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78049b951d863a980d065860a1f0b86e5eb66cb7c2307fe08cb30ca05e4ecf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocBatchRuntimeConfig]:
        return typing.cast(typing.Optional[DataprocBatchRuntimeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchRuntimeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18d3c35645db693690fa4d5aad35ba46681dd8b0df62f1db4554da99ed2e076)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocBatchRuntimeInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchRuntimeInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfoApproximateUsage",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocBatchRuntimeInfoApproximateUsage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchRuntimeInfoApproximateUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchRuntimeInfoApproximateUsageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfoApproximateUsageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e9db00b7b80d154bd3ce5af49ea149119fc4e5923582d095d195c2cfa8efade)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocBatchRuntimeInfoApproximateUsageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad34a49dd7bee48352f49065961670e0a10938cb1691253dcaa3e1b462e1a510)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocBatchRuntimeInfoApproximateUsageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e3ea5d687e70a0144293a124a90e78d027f537838d4412f530634653e1d782)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08b8c8197e1f359a35c1a4742f8e5b57939a415f7622e032789c8f30f394233e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82dd2d3949348c22a79ba38a5582cbc4b8fcf50111160fd448a527327f57ba6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataprocBatchRuntimeInfoApproximateUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfoApproximateUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79ba9d99af54999bba2abfe51a0827b2fe6cdc7c265f54e36964c1122b032adc)
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
    ) -> typing.Optional[DataprocBatchRuntimeInfoApproximateUsage]:
        return typing.cast(typing.Optional[DataprocBatchRuntimeInfoApproximateUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchRuntimeInfoApproximateUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af63554dda03094b706890db8770f0b57e57082123d0de5d1ed7f4554a158739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfoCurrentUsage",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocBatchRuntimeInfoCurrentUsage:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchRuntimeInfoCurrentUsage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchRuntimeInfoCurrentUsageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfoCurrentUsageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f351e5a5ef8590db6015586da0103c5f275bfdfd859724b31a1f8968f8706af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataprocBatchRuntimeInfoCurrentUsageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72335fc0c506b45822a94b87f73ee8dafb0b0a0e1394624f602b2ec05c43434d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocBatchRuntimeInfoCurrentUsageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ca81054cb761f749b8287c32e267daeb5f0faf40c9e018c0fa644033fb3500)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bc112a00151a461f8093e6d852af85a231f309172cd88f7634f889285e8449e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67b78ed824f5a11dafe89c407cdc8dd964599d24c18bd8d227b55fbe9da67ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataprocBatchRuntimeInfoCurrentUsageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfoCurrentUsageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac999defa40588d7b7e09ba2d982da9855e7f28801f534324b78795ead6831ff)
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
    def internal_value(self) -> typing.Optional[DataprocBatchRuntimeInfoCurrentUsage]:
        return typing.cast(typing.Optional[DataprocBatchRuntimeInfoCurrentUsage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchRuntimeInfoCurrentUsage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325332593b53ecb85e0db007d03ca96183b442e1cd6f0bfbd21e67eec0638bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocBatchRuntimeInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2066222debb039bb185f410a3ce96276ff47c69bc04c70012e780af55f7e0ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataprocBatchRuntimeInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c1b05080f03d26af12d078cb3d7237537d497eabe1d2159da7cd547ab9a333)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocBatchRuntimeInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7863bc076c1c8583b43957f3bd9762a22d44e9a3fba558b9b38d67bb2927e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc0d54f40e3b1c474e69e490b97230887157e28b04e173ac21a4b2080b0d33ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__596e05198393cb797502b6d81c82585b4cd4f9baafbefa5efe82e2c40a58fe3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataprocBatchRuntimeInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchRuntimeInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__894846021dd6547a28df0c94ddb63e5137049bf45deca360306aa863e8f1d363)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="approximateUsage")
    def approximate_usage(self) -> DataprocBatchRuntimeInfoApproximateUsageList:
        return typing.cast(DataprocBatchRuntimeInfoApproximateUsageList, jsii.get(self, "approximateUsage"))

    @builtins.property
    @jsii.member(jsii_name="currentUsage")
    def current_usage(self) -> DataprocBatchRuntimeInfoCurrentUsageList:
        return typing.cast(DataprocBatchRuntimeInfoCurrentUsageList, jsii.get(self, "currentUsage"))

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
    def internal_value(self) -> typing.Optional[DataprocBatchRuntimeInfo]:
        return typing.cast(typing.Optional[DataprocBatchRuntimeInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocBatchRuntimeInfo]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d93f3d9064d70400ef7e1bff5b06070a9bcbe776cd8308a3da785fe7f3af673c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchSparkBatch",
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
class DataprocBatchSparkBatch:
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        :param main_class: The name of the driver main class. The jar file that contains the class must be in the classpath or specified in jarFileUris. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_class DataprocBatch#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_jar_file_uri DataprocBatch#main_jar_file_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c67d4e5ab4f9f13b02560b7dd676d4c03b33883aa4b6590e23b729f6a9126c5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments that can be set as batch
        properties, such as --conf, since a collision can occur that causes an incorrect batch submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the classpath of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The name of the driver main class.

        The jar file that contains the class must be in the
        classpath or specified in jarFileUris.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_class DataprocBatch#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the jar file that contains the main class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_jar_file_uri DataprocBatch#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchSparkBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchSparkBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchSparkBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b2912fd5aa75adf3ac97c1f693f95953d40f7498e7408db8b165987c312bf87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61c1acb74e0cc046561a41fb4c8af45a8fce090a31473fc6349dd74f6b8c22d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4979c2edb4da9ebfbadea574088f05c4fa260223ac10c5993b178bbc935c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0227096103963757744d3893a38a6071018a70bebc90d9277c980324ef55b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1c6ced6f90c874761fa142b036f34579baf657c5e53024be9add3aabedbc20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a668189b63ca4c1b7d6a2328156c663e9b432ec36f296b0b08c9b148334bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b0caa5cb738194c7ea1edaba1c3d809df16aace7768e64120565c62a2fdd683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocBatchSparkBatch]:
        return typing.cast(typing.Optional[DataprocBatchSparkBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocBatchSparkBatch]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d29e163755d4ce94770ce03cbfef030a87e00f54a5e72e14f7f42bff284a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchSparkRBatch",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "main_r_file_uri": "mainRFileUri",
    },
)
class DataprocBatchSparkRBatch:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        main_r_file_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as batch properties, such as --conf, since a collision can occur that causes an incorrect batch submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        :param main_r_file_uri: The HCFS URI of the main R file to use as the driver. Must be a .R or .r file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_r_file_uri DataprocBatch#main_r_file_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a694fb2499ad62836030e5edf27855d85d91cf6d7b40e8d4a355ae29b791f292)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#archive_uris DataprocBatch#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments that can be set as batch
        properties, such as --conf, since a collision can occur that causes an incorrect batch submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#args DataprocBatch#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#file_uris DataprocBatch#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_r_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the main R file to use as the driver.

        Must be a .R or .r file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#main_r_file_uri DataprocBatch#main_r_file_uri}
        '''
        result = self._values.get("main_r_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchSparkRBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchSparkRBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchSparkRBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5ff78053370135ae72118bf80bddaa16ac746cb295b55eafb4830cfa3e686b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86abe8a57661236447ab8b5e041271b1564ca9ae995471db3767c4932fc16618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca21c729edc4beca44eeed7c09c5a8b2ea6852ed8c4ca85d706687dae7f23fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8890067bad6a191053c29d6609c0d34a068892b1edc3efbcea50d4c7ac278b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainRFileUri")
    def main_r_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainRFileUri"))

    @main_r_file_uri.setter
    def main_r_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a744734202c6519a4dbcd926518d738ce1f020f0f1c9c1fdffdfec7bdcecc14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainRFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocBatchSparkRBatch]:
        return typing.cast(typing.Optional[DataprocBatchSparkRBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocBatchSparkRBatch]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2612c3b9b9d5b9ea7126f0e64ee1d4e9fe53c3a9f242c1e95487a82462daa727)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchSparkSqlBatch",
    jsii_struct_bases=[],
    name_mapping={
        "jar_file_uris": "jarFileUris",
        "query_file_uri": "queryFileUri",
        "query_variables": "queryVariables",
    },
)
class DataprocBatchSparkSqlBatch:
    def __init__(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        :param query_file_uri: The HCFS URI of the script that contains Spark SQL queries to execute. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#query_file_uri DataprocBatch#query_file_uri}
        :param query_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#query_variables DataprocBatch#query_variables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73aa713a8568a0fd4a751546142a33cb0bc0ae5a7526724d9b4afdf33482e11e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#jar_file_uris DataprocBatch#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains Spark SQL queries to execute.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#query_file_uri DataprocBatch#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#query_variables DataprocBatch#query_variables}
        '''
        result = self._values.get("query_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchSparkSqlBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchSparkSqlBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchSparkSqlBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7553ab11c243d006d6437c2fa2a060f570645dc7307c415189911706405e9064)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdad41669111c647709b7b160457b14e6b617c0b2865d4f25f651f3597f55bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2467a54768082890a59e183b36d3fff7a334ce059802c321a1070ab0f1be76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcead1ad5fda55279c82e5609f3e0a5bc874f7c0aa8ccc7f082bd529310ed67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocBatchSparkSqlBatch]:
        return typing.cast(typing.Optional[DataprocBatchSparkSqlBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocBatchSparkSqlBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b399835af1e9cbdeb20b34b1befd9cf3c5cc51199980b2bd37a3dfaabda26392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchStateHistory",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocBatchStateHistory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchStateHistory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchStateHistoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchStateHistoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a57c40a6dbc3cfac32076d21f7881fafe299ae3847e76b72c6df1b23648572e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataprocBatchStateHistoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14dca1c18e793dad9f8c56938e774db5f2a6515dfd423c4329765a376cbd3d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocBatchStateHistoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d8114c95318053d30317c2f9c839cc4836539eec7273c0e43fc1d58216ec53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb74fa9282756230302c28a82b66e8d207ca67a724b9ad43751ee7ba8baa7c5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbbf2accec1dc8bed4148b3246ddb36d19888fd3d6286e4ae972f64579d6e5ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataprocBatchStateHistoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchStateHistoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3f9d5131dacfb43eb781084d4dba1e1f08f3ea59af34dd4008fb4eeee7e5bc3)
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
    def internal_value(self) -> typing.Optional[DataprocBatchStateHistory]:
        return typing.cast(typing.Optional[DataprocBatchStateHistory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocBatchStateHistory]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d11b882721b6df679b54de32d0c1c2183093029157b7a76f4ca941e178f0591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataprocBatchTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#create DataprocBatch#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#delete DataprocBatch#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#update DataprocBatch#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7b3137fafaebc0896b6ead65f2284bf10f2072270a20be657b53177b557065)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#create DataprocBatch#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#delete DataprocBatch#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_batch#update DataprocBatch#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocBatchTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocBatchTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocBatch.DataprocBatchTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e9f9010836dece130ffd1f61423b3f85104d3b32380ea2fdbba5a6bba0268b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3629f37cd19f7bffe05a3a845be07548894d806dbe0201c739266740868948e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a701c2d3a209289664f43a0d353bd2d8ee953f52df2d461514b8715cba9b292b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e10edcc03275cb8a1391a5dbc4224454f41d2740c59046fc26e49f028616f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocBatchTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocBatchTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocBatchTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de389ab73225efa987e7996d5ebef3ca5f4a083cec1abfb7e45e092b511fae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataprocBatch",
    "DataprocBatchConfig",
    "DataprocBatchEnvironmentConfig",
    "DataprocBatchEnvironmentConfigExecutionConfig",
    "DataprocBatchEnvironmentConfigExecutionConfigOutputReference",
    "DataprocBatchEnvironmentConfigOutputReference",
    "DataprocBatchEnvironmentConfigPeripheralsConfig",
    "DataprocBatchEnvironmentConfigPeripheralsConfigOutputReference",
    "DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig",
    "DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfigOutputReference",
    "DataprocBatchPysparkBatch",
    "DataprocBatchPysparkBatchOutputReference",
    "DataprocBatchRuntimeConfig",
    "DataprocBatchRuntimeConfigAutotuningConfig",
    "DataprocBatchRuntimeConfigAutotuningConfigOutputReference",
    "DataprocBatchRuntimeConfigOutputReference",
    "DataprocBatchRuntimeInfo",
    "DataprocBatchRuntimeInfoApproximateUsage",
    "DataprocBatchRuntimeInfoApproximateUsageList",
    "DataprocBatchRuntimeInfoApproximateUsageOutputReference",
    "DataprocBatchRuntimeInfoCurrentUsage",
    "DataprocBatchRuntimeInfoCurrentUsageList",
    "DataprocBatchRuntimeInfoCurrentUsageOutputReference",
    "DataprocBatchRuntimeInfoList",
    "DataprocBatchRuntimeInfoOutputReference",
    "DataprocBatchSparkBatch",
    "DataprocBatchSparkBatchOutputReference",
    "DataprocBatchSparkRBatch",
    "DataprocBatchSparkRBatchOutputReference",
    "DataprocBatchSparkSqlBatch",
    "DataprocBatchSparkSqlBatchOutputReference",
    "DataprocBatchStateHistory",
    "DataprocBatchStateHistoryList",
    "DataprocBatchStateHistoryOutputReference",
    "DataprocBatchTimeouts",
    "DataprocBatchTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__725de29c9d11fb44f4a1619714f1600b8c458787b6f9c2d0f3f6fe5ffa0f1a53(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    batch_id: typing.Optional[builtins.str] = None,
    environment_config: typing.Optional[typing.Union[DataprocBatchEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    pyspark_batch: typing.Optional[typing.Union[DataprocBatchPysparkBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_config: typing.Optional[typing.Union[DataprocBatchRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_batch: typing.Optional[typing.Union[DataprocBatchSparkBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_batch: typing.Optional[typing.Union[DataprocBatchSparkRBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_batch: typing.Optional[typing.Union[DataprocBatchSparkSqlBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocBatchTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3b7bd6d43b30304b989f63b127ba7701a4f0c24f647970aba16240f9daa47194(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d5c16b40f34fd44abcf260e6722c5effcbdd1cb078599addc019532561fffc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3394fa37ab41d0a7268e3c15fd26c977ebf9d272254fcf7bc898f59fe10aebe4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f0c7d79431162397e945d056cf933c54db9f103a9397303bc878eecb0839b7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061764b113e3791281f17a998a03f879ffbde169b2b5a5e6f2a56a38399f59ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a75de19a58913f5a991165962d498a7a58096f4e589fae8803dfe28cf2e659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c68b64a05a87b3d483b326087e63b434e760d95f3c32bbad5fc06f4687d33a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    batch_id: typing.Optional[builtins.str] = None,
    environment_config: typing.Optional[typing.Union[DataprocBatchEnvironmentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    pyspark_batch: typing.Optional[typing.Union[DataprocBatchPysparkBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_config: typing.Optional[typing.Union[DataprocBatchRuntimeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_batch: typing.Optional[typing.Union[DataprocBatchSparkBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_batch: typing.Optional[typing.Union[DataprocBatchSparkRBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_batch: typing.Optional[typing.Union[DataprocBatchSparkSqlBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocBatchTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0555ea3eeb600c2ce28a1c2068d82bc9264e9bc79daf86e2ee45c0f43e8c8c2(
    *,
    execution_config: typing.Optional[typing.Union[DataprocBatchEnvironmentConfigExecutionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    peripherals_config: typing.Optional[typing.Union[DataprocBatchEnvironmentConfigPeripheralsConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8a8fae405e7ec873f2e8dc4c8f521894610c2a4f4341df7d5e7ec99d99124e(
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

def _typecheckingstub__096ae0ad3687307130ab575b382601d9bf6a07b29bf23696db0120f9124547c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8027e0b1785d4e1bee0150a75c924b8d2024860d77f0801235133a8d8b1d97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc7eee489dcf75a57b7587c882e921bb63feab3a12dd977a91a2cc01a2a1a6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625934dd0a201f71b7ab241cfaf921c7ef5f89294588894bcbc491f3bae26c8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0117f0027147607595d38327948a0ca44ede813cc98335a1a8fdf91081dc45b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a154ab2278c9ee784e1f818554e1f186c4b5f2ab8f54d4daf63a12a6ec95669c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c478c5c37ffa6456b1d9f18ad227fc94f51b3ed7ecad084db90d684b86d275eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b2ce51089ffa12e964774d79921bbc46517ff54f47953c5b6cdf728e54ff10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f1a2b551c645278221cc8c2e3d1465c355753c0052822f95a3a2cb9ce207e31(
    value: typing.Optional[DataprocBatchEnvironmentConfigExecutionConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7dc7f47bcc5beaf69ac51690cc251e51817dcb8438f19419dc8b6f6d295e7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da2000b2dcfefd653cd9a9dfd21c6b70e2622119041169abfb03c1fea78ff441(
    value: typing.Optional[DataprocBatchEnvironmentConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100edde5643f533d359805642a869dffdf7b691597044f505b06daef5dd6ad8b(
    *,
    metastore_service: typing.Optional[builtins.str] = None,
    spark_history_server_config: typing.Optional[typing.Union[DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6cbc058a147ccd95824ba39eecfd9721b947aef7971c9c735d09a005b75bd3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37130bfbf9fde3e8da658a9cfa338f5eda6777862d7f71b3042cf65f6e2ff6bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a07f5ed80e17ed619cb0c540038d89ff06c69c614f40f62e86250e434115d0(
    value: typing.Optional[DataprocBatchEnvironmentConfigPeripheralsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1d8793206a74b9ef918ed7e5a1df6179e82fdcf728151f6420d43aff780d65(
    *,
    dataproc_cluster: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d19ecaa6bc66da62497bbb9ca5714d1ff7960cba3e6320622d2ecdb4382dd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060e324e0ac12c97571e1d297fb6f17e1b356d1a32cc86be735ceac784b4b607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7fb544f5b71c88cd8fcd5131708d70dd215b87ef9e8cc0e9cf5bfdee2cc67e(
    value: typing.Optional[DataprocBatchEnvironmentConfigPeripheralsConfigSparkHistoryServerConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef14e04ce4a4b6819a6df6bb32aa091b128c1035e787f732bb6fd33c267c2262(
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

def _typecheckingstub__ca7d212e66860c68d29b84d511f95887ce7e1fab274efa3a2812a1392a7d855e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58831538b28532d4b17e0faaef761f3cacc66e10c100782fbc93f55cc67286f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eacc394ea0d0af4070bec61b53ef87be4260dfa0b0a146cf0c91936d06579307(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee82a085d4104ec07fcb0ddd712363212d3712a41f3f5993491ba79b4c986e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88df5b5a45da80abce093274bbf9e86b280699caf23080b6038d3d298c40000b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024e6fec372ff08a288bb169ce3ce4e56b1cd8fd5ace86b9693c97d6e32c728a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1687301891c1319089d0ca07023a60d5ecdbb5fba054f3259fd64d3878f12d27(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c7d23ee265075636ccf91f9c79de8b92f9faa041425ea28942f48fec883f33(
    value: typing.Optional[DataprocBatchPysparkBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8830ab03df5b23036e5793fc94b7e0aea522d284cd8ce0ba68f71638c3f0ec8d(
    *,
    autotuning_config: typing.Optional[typing.Union[DataprocBatchRuntimeConfigAutotuningConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    cohort: typing.Optional[builtins.str] = None,
    container_image: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7e9a949bbddd324dcf55886f4b92a66bed3062c1e69fa3b3bc353ce6f7b97fa(
    *,
    scenarios: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de42d528d97f699bea56fef1132958143942584bf449962885a9300b560b6686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b9405faf77885e734d872f8e7cf25d56771d0197f62ca8c92493e585c0c030(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d33dbde1a9b4f115a63633a021d77afe1e2fe60e17660725af4801bfda536f(
    value: typing.Optional[DataprocBatchRuntimeConfigAutotuningConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7f06d8af8162e2723198d81f039b90ebfabe31a6e383c7d39bc1d609c22d98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3ec67d6e3ee73c56c370ffa34d0a276908c90a17a3e83bee2fb6c24c3520ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab582d51ebf3d8a4fbffd45f83ce35fe6ff3fc479f2e524c828d03e17dc94c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17508f2492806092ed4a4ab2a56be4839bafe1d4b88537f66790f519d158ace(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78049b951d863a980d065860a1f0b86e5eb66cb7c2307fe08cb30ca05e4ecf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18d3c35645db693690fa4d5aad35ba46681dd8b0df62f1db4554da99ed2e076(
    value: typing.Optional[DataprocBatchRuntimeConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9db00b7b80d154bd3ce5af49ea149119fc4e5923582d095d195c2cfa8efade(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad34a49dd7bee48352f49065961670e0a10938cb1691253dcaa3e1b462e1a510(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e3ea5d687e70a0144293a124a90e78d027f537838d4412f530634653e1d782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b8c8197e1f359a35c1a4742f8e5b57939a415f7622e032789c8f30f394233e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dd2d3949348c22a79ba38a5582cbc4b8fcf50111160fd448a527327f57ba6a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ba9d99af54999bba2abfe51a0827b2fe6cdc7c265f54e36964c1122b032adc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af63554dda03094b706890db8770f0b57e57082123d0de5d1ed7f4554a158739(
    value: typing.Optional[DataprocBatchRuntimeInfoApproximateUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f351e5a5ef8590db6015586da0103c5f275bfdfd859724b31a1f8968f8706af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72335fc0c506b45822a94b87f73ee8dafb0b0a0e1394624f602b2ec05c43434d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ca81054cb761f749b8287c32e267daeb5f0faf40c9e018c0fa644033fb3500(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc112a00151a461f8093e6d852af85a231f309172cd88f7634f889285e8449e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b78ed824f5a11dafe89c407cdc8dd964599d24c18bd8d227b55fbe9da67ac3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac999defa40588d7b7e09ba2d982da9855e7f28801f534324b78795ead6831ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325332593b53ecb85e0db007d03ca96183b442e1cd6f0bfbd21e67eec0638bc3(
    value: typing.Optional[DataprocBatchRuntimeInfoCurrentUsage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2066222debb039bb185f410a3ce96276ff47c69bc04c70012e780af55f7e0ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c1b05080f03d26af12d078cb3d7237537d497eabe1d2159da7cd547ab9a333(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7863bc076c1c8583b43957f3bd9762a22d44e9a3fba558b9b38d67bb2927e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0d54f40e3b1c474e69e490b97230887157e28b04e173ac21a4b2080b0d33ba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596e05198393cb797502b6d81c82585b4cd4f9baafbefa5efe82e2c40a58fe3b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894846021dd6547a28df0c94ddb63e5137049bf45deca360306aa863e8f1d363(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93f3d9064d70400ef7e1bff5b06070a9bcbe776cd8308a3da785fe7f3af673c(
    value: typing.Optional[DataprocBatchRuntimeInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c67d4e5ab4f9f13b02560b7dd676d4c03b33883aa4b6590e23b729f6a9126c5(
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

def _typecheckingstub__0b2912fd5aa75adf3ac97c1f693f95953d40f7498e7408db8b165987c312bf87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c1acb74e0cc046561a41fb4c8af45a8fce090a31473fc6349dd74f6b8c22d6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4979c2edb4da9ebfbadea574088f05c4fa260223ac10c5993b178bbc935c32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0227096103963757744d3893a38a6071018a70bebc90d9277c980324ef55b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1c6ced6f90c874761fa142b036f34579baf657c5e53024be9add3aabedbc20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9a668189b63ca4c1b7d6a2328156c663e9b432ec36f296b0b08c9b148334bd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b0caa5cb738194c7ea1edaba1c3d809df16aace7768e64120565c62a2fdd683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d29e163755d4ce94770ce03cbfef030a87e00f54a5e72e14f7f42bff284a2b(
    value: typing.Optional[DataprocBatchSparkBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a694fb2499ad62836030e5edf27855d85d91cf6d7b40e8d4a355ae29b791f292(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    main_r_file_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5ff78053370135ae72118bf80bddaa16ac746cb295b55eafb4830cfa3e686b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86abe8a57661236447ab8b5e041271b1564ca9ae995471db3767c4932fc16618(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca21c729edc4beca44eeed7c09c5a8b2ea6852ed8c4ca85d706687dae7f23fd7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8890067bad6a191053c29d6609c0d34a068892b1edc3efbcea50d4c7ac278b01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a744734202c6519a4dbcd926518d738ce1f020f0f1c9c1fdffdfec7bdcecc14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2612c3b9b9d5b9ea7126f0e64ee1d4e9fe53c3a9f242c1e95487a82462daa727(
    value: typing.Optional[DataprocBatchSparkRBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73aa713a8568a0fd4a751546142a33cb0bc0ae5a7526724d9b4afdf33482e11e(
    *,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7553ab11c243d006d6437c2fa2a060f570645dc7307c415189911706405e9064(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdad41669111c647709b7b160457b14e6b617c0b2865d4f25f651f3597f55bd6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2467a54768082890a59e183b36d3fff7a334ce059802c321a1070ab0f1be76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcead1ad5fda55279c82e5609f3e0a5bc874f7c0aa8ccc7f082bd529310ed67b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b399835af1e9cbdeb20b34b1befd9cf3c5cc51199980b2bd37a3dfaabda26392(
    value: typing.Optional[DataprocBatchSparkSqlBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57c40a6dbc3cfac32076d21f7881fafe299ae3847e76b72c6df1b23648572e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14dca1c18e793dad9f8c56938e774db5f2a6515dfd423c4329765a376cbd3d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d8114c95318053d30317c2f9c839cc4836539eec7273c0e43fc1d58216ec53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb74fa9282756230302c28a82b66e8d207ca67a724b9ad43751ee7ba8baa7c5e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbf2accec1dc8bed4148b3246ddb36d19888fd3d6286e4ae972f64579d6e5ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f9d5131dacfb43eb781084d4dba1e1f08f3ea59af34dd4008fb4eeee7e5bc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d11b882721b6df679b54de32d0c1c2183093029157b7a76f4ca941e178f0591(
    value: typing.Optional[DataprocBatchStateHistory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7b3137fafaebc0896b6ead65f2284bf10f2072270a20be657b53177b557065(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e9f9010836dece130ffd1f61423b3f85104d3b32380ea2fdbba5a6bba0268b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3629f37cd19f7bffe05a3a845be07548894d806dbe0201c739266740868948e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a701c2d3a209289664f43a0d353bd2d8ee953f52df2d461514b8715cba9b292b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e10edcc03275cb8a1391a5dbc4224454f41d2740c59046fc26e49f028616f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de389ab73225efa987e7996d5ebef3ca5f4a083cec1abfb7e45e092b511fae2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocBatchTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

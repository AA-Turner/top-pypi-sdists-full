r'''
# `google_dataproc_gdc_spark_application`

Refer to the Terraform Registry for docs: [`google_dataproc_gdc_spark_application`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application).
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


class DataprocGdcSparkApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application google_dataproc_gdc_spark_application}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        serviceinstance: builtins.str,
        spark_application_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        application_environment: typing.Optional[builtins.str] = None,
        dependency_images: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        pyspark_application_config: typing.Optional[typing.Union["DataprocGdcSparkApplicationPysparkApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_application_config: typing.Optional[typing.Union["DataprocGdcSparkApplicationSparkApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_application_config: typing.Optional[typing.Union["DataprocGdcSparkApplicationSparkRApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_application_config: typing.Optional[typing.Union["DataprocGdcSparkApplicationSparkSqlApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocGdcSparkApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application google_dataproc_gdc_spark_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the spark application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#location DataprocGdcSparkApplication#location}
        :param serviceinstance: The id of the service instance to which this spark application belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#serviceinstance DataprocGdcSparkApplication#serviceinstance}
        :param spark_application_id: The id of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_application_id DataprocGdcSparkApplication#spark_application_id}
        :param annotations: The annotations to associate with this application. Annotations may be used to store client information, but are not used by the server. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#annotations DataprocGdcSparkApplication#annotations}
        :param application_environment: An ApplicationEnvironment from which to inherit configuration properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#application_environment DataprocGdcSparkApplication#application_environment}
        :param dependency_images: List of container image uris for additional file dependencies. Dependent files are sequentially copied from each image. If a file with the same name exists in 2 images then the file from later image is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#dependency_images DataprocGdcSparkApplication#dependency_images}
        :param display_name: User-provided human-readable name to be used in user interfaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#display_name DataprocGdcSparkApplication#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#id DataprocGdcSparkApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this application. Labels may be used for filtering and billing tracking. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#labels DataprocGdcSparkApplication#labels}
        :param namespace: The Kubernetes namespace in which to create the application. This namespace must already exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#namespace DataprocGdcSparkApplication#namespace}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#project DataprocGdcSparkApplication#project}.
        :param properties: application-specific properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#properties DataprocGdcSparkApplication#properties}
        :param pyspark_application_config: pyspark_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#pyspark_application_config DataprocGdcSparkApplication#pyspark_application_config}
        :param spark_application_config: spark_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_application_config DataprocGdcSparkApplication#spark_application_config}
        :param spark_r_application_config: spark_r_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_r_application_config DataprocGdcSparkApplication#spark_r_application_config}
        :param spark_sql_application_config: spark_sql_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_sql_application_config DataprocGdcSparkApplication#spark_sql_application_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#timeouts DataprocGdcSparkApplication#timeouts}
        :param version: The Dataproc version of this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#version DataprocGdcSparkApplication#version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43699763398ba85e86a6ff3bd3536579784e9603c99b9dca1aa1564e26b710c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataprocGdcSparkApplicationConfig(
            location=location,
            serviceinstance=serviceinstance,
            spark_application_id=spark_application_id,
            annotations=annotations,
            application_environment=application_environment,
            dependency_images=dependency_images,
            display_name=display_name,
            id=id,
            labels=labels,
            namespace=namespace,
            project=project,
            properties=properties,
            pyspark_application_config=pyspark_application_config,
            spark_application_config=spark_application_config,
            spark_r_application_config=spark_r_application_config,
            spark_sql_application_config=spark_sql_application_config,
            timeouts=timeouts,
            version=version,
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
        '''Generates CDKTF code for importing a DataprocGdcSparkApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataprocGdcSparkApplication to import.
        :param import_from_id: The id of the existing DataprocGdcSparkApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataprocGdcSparkApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d040fe899c172714e53dfd71fd686c7ac360ad4436a661bd3de675c5b0d6acde)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPysparkApplicationConfig")
    def put_pyspark_application_config(
        self,
        *,
        main_python_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_python_file_uri: The HCFS URI of the main Python file to use as the driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_python_file_uri DataprocGdcSparkApplication#main_python_file_uri}
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        :param python_file_uris: HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#python_file_uris DataprocGdcSparkApplication#python_file_uris}
        '''
        value = DataprocGdcSparkApplicationPysparkApplicationConfig(
            main_python_file_uri=main_python_file_uri,
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            python_file_uris=python_file_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putPysparkApplicationConfig", [value]))

    @jsii.member(jsii_name="putSparkApplicationConfig")
    def put_spark_application_config(
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: '.jar', '.tar', '.tar.gz', '.tgz', and '.zip'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as application properties, such as '--conf', since a collision can occur that causes an incorrect application submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        :param main_class: The name of the driver main class. The jar file that contains the class must be in the classpath or specified in 'jar_file_uris'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_class DataprocGdcSparkApplication#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_jar_file_uri DataprocGdcSparkApplication#main_jar_file_uri}
        '''
        value = DataprocGdcSparkApplicationSparkApplicationConfig(
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            main_class=main_class,
            main_jar_file_uri=main_jar_file_uri,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkApplicationConfig", [value]))

    @jsii.member(jsii_name="putSparkRApplicationConfig")
    def put_spark_r_application_config(
        self,
        *,
        main_r_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_r_file_uri: The HCFS URI of the main R file to use as the driver. Must be a .R file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_r_file_uri DataprocGdcSparkApplication#main_r_file_uri}
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        '''
        value = DataprocGdcSparkApplicationSparkRApplicationConfig(
            main_r_file_uri=main_r_file_uri,
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkRApplicationConfig", [value]))

    @jsii.member(jsii_name="putSparkSqlApplicationConfig")
    def put_spark_sql_application_config(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#query_file_uri DataprocGdcSparkApplication#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#query_list DataprocGdcSparkApplication#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET 'name="value";'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#script_variables DataprocGdcSparkApplication#script_variables}
        '''
        value = DataprocGdcSparkApplicationSparkSqlApplicationConfig(
            jar_file_uris=jar_file_uris,
            query_file_uri=query_file_uri,
            query_list=query_list,
            script_variables=script_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkSqlApplicationConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#create DataprocGdcSparkApplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#delete DataprocGdcSparkApplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#update DataprocGdcSparkApplication#update}.
        '''
        value = DataprocGdcSparkApplicationTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetApplicationEnvironment")
    def reset_application_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationEnvironment", []))

    @jsii.member(jsii_name="resetDependencyImages")
    def reset_dependency_images(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependencyImages", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetPysparkApplicationConfig")
    def reset_pyspark_application_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPysparkApplicationConfig", []))

    @jsii.member(jsii_name="resetSparkApplicationConfig")
    def reset_spark_application_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkApplicationConfig", []))

    @jsii.member(jsii_name="resetSparkRApplicationConfig")
    def reset_spark_r_application_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkRApplicationConfig", []))

    @jsii.member(jsii_name="resetSparkSqlApplicationConfig")
    def reset_spark_sql_application_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkSqlApplicationConfig", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="monitoringEndpoint")
    def monitoring_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitoringEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="outputUri")
    def output_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputUri"))

    @builtins.property
    @jsii.member(jsii_name="pysparkApplicationConfig")
    def pyspark_application_config(
        self,
    ) -> "DataprocGdcSparkApplicationPysparkApplicationConfigOutputReference":
        return typing.cast("DataprocGdcSparkApplicationPysparkApplicationConfigOutputReference", jsii.get(self, "pysparkApplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="sparkApplicationConfig")
    def spark_application_config(
        self,
    ) -> "DataprocGdcSparkApplicationSparkApplicationConfigOutputReference":
        return typing.cast("DataprocGdcSparkApplicationSparkApplicationConfigOutputReference", jsii.get(self, "sparkApplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparkRApplicationConfig")
    def spark_r_application_config(
        self,
    ) -> "DataprocGdcSparkApplicationSparkRApplicationConfigOutputReference":
        return typing.cast("DataprocGdcSparkApplicationSparkRApplicationConfigOutputReference", jsii.get(self, "sparkRApplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlApplicationConfig")
    def spark_sql_application_config(
        self,
    ) -> "DataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference":
        return typing.cast("DataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference", jsii.get(self, "sparkSqlApplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateMessage")
    def state_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateMessage"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataprocGdcSparkApplicationTimeoutsOutputReference":
        return typing.cast("DataprocGdcSparkApplicationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationEnvironmentInput")
    def application_environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationEnvironmentInput"))

    @builtins.property
    @jsii.member(jsii_name="dependencyImagesInput")
    def dependency_images_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependencyImagesInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

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
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="pysparkApplicationConfigInput")
    def pyspark_application_config_input(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationPysparkApplicationConfig"]:
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationPysparkApplicationConfig"], jsii.get(self, "pysparkApplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceinstanceInput")
    def serviceinstance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceinstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkApplicationConfigInput")
    def spark_application_config_input(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationSparkApplicationConfig"]:
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationSparkApplicationConfig"], jsii.get(self, "sparkApplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkApplicationIdInput")
    def spark_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkRApplicationConfigInput")
    def spark_r_application_config_input(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationSparkRApplicationConfig"]:
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationSparkRApplicationConfig"], jsii.get(self, "sparkRApplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlApplicationConfigInput")
    def spark_sql_application_config_input(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationSparkSqlApplicationConfig"]:
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationSparkSqlApplicationConfig"], jsii.get(self, "sparkSqlApplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocGdcSparkApplicationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocGdcSparkApplicationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3968f05c46270c9cdc2118cfbf4e500b356a74700084375c95112c6380ba3ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationEnvironment")
    def application_environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationEnvironment"))

    @application_environment.setter
    def application_environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292af0f00eabdd2fd821740ed03c044daccf6837947064cd073f812037bb36ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependencyImages")
    def dependency_images(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependencyImages"))

    @dependency_images.setter
    def dependency_images(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9126e358bee339826b6c53ae1f49580bcc11ca81d224dfb923c7ec1c7aeb39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencyImages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2473e2f7f50fe120002b1c3e5bd253466e8821f00c15bf2a79b60ad4818464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864ba9ec69de153ffb028ca7d6562b2823f0e89564db7a072cab5c60a375de22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb9ae1130ce8834b0f379934f4727329a3984b860c7a4a499825e74b73cd83e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190b6c52cec3fd536e74099cd1167b68133549167bc37805bcf657b2b21d8f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6d0a106a8c40f548bbbe918ecb9a3d05194d7261651e64ab0624d5bec20083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd1b296c71ed5f8bed1cfbdb3c8f80045d77a37432480273dd88bbc47442ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267223919eef39f8c783ac61e846da1b8859f39e686fffcade5027059c0dced9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceinstance")
    def serviceinstance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceinstance"))

    @serviceinstance.setter
    def serviceinstance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ff33fad869778bf9d5e250d3239262e88c93e29bb8ae28c79a6933c62fad9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceinstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkApplicationId")
    def spark_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkApplicationId"))

    @spark_application_id.setter
    def spark_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6071f9703c4000c474a34681196a01adcaa6cdfb735422d5c50085e2af87819f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b1b63a14c157b8bddfcb4745d32a729fbacee57571f227f17992f852cb2bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "serviceinstance": "serviceinstance",
        "spark_application_id": "sparkApplicationId",
        "annotations": "annotations",
        "application_environment": "applicationEnvironment",
        "dependency_images": "dependencyImages",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "namespace": "namespace",
        "project": "project",
        "properties": "properties",
        "pyspark_application_config": "pysparkApplicationConfig",
        "spark_application_config": "sparkApplicationConfig",
        "spark_r_application_config": "sparkRApplicationConfig",
        "spark_sql_application_config": "sparkSqlApplicationConfig",
        "timeouts": "timeouts",
        "version": "version",
    },
)
class DataprocGdcSparkApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        serviceinstance: builtins.str,
        spark_application_id: builtins.str,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        application_environment: typing.Optional[builtins.str] = None,
        dependency_images: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        pyspark_application_config: typing.Optional[typing.Union["DataprocGdcSparkApplicationPysparkApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_application_config: typing.Optional[typing.Union["DataprocGdcSparkApplicationSparkApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_application_config: typing.Optional[typing.Union["DataprocGdcSparkApplicationSparkRApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_application_config: typing.Optional[typing.Union["DataprocGdcSparkApplicationSparkSqlApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocGdcSparkApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the spark application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#location DataprocGdcSparkApplication#location}
        :param serviceinstance: The id of the service instance to which this spark application belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#serviceinstance DataprocGdcSparkApplication#serviceinstance}
        :param spark_application_id: The id of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_application_id DataprocGdcSparkApplication#spark_application_id}
        :param annotations: The annotations to associate with this application. Annotations may be used to store client information, but are not used by the server. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#annotations DataprocGdcSparkApplication#annotations}
        :param application_environment: An ApplicationEnvironment from which to inherit configuration properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#application_environment DataprocGdcSparkApplication#application_environment}
        :param dependency_images: List of container image uris for additional file dependencies. Dependent files are sequentially copied from each image. If a file with the same name exists in 2 images then the file from later image is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#dependency_images DataprocGdcSparkApplication#dependency_images}
        :param display_name: User-provided human-readable name to be used in user interfaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#display_name DataprocGdcSparkApplication#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#id DataprocGdcSparkApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this application. Labels may be used for filtering and billing tracking. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#labels DataprocGdcSparkApplication#labels}
        :param namespace: The Kubernetes namespace in which to create the application. This namespace must already exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#namespace DataprocGdcSparkApplication#namespace}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#project DataprocGdcSparkApplication#project}.
        :param properties: application-specific properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#properties DataprocGdcSparkApplication#properties}
        :param pyspark_application_config: pyspark_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#pyspark_application_config DataprocGdcSparkApplication#pyspark_application_config}
        :param spark_application_config: spark_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_application_config DataprocGdcSparkApplication#spark_application_config}
        :param spark_r_application_config: spark_r_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_r_application_config DataprocGdcSparkApplication#spark_r_application_config}
        :param spark_sql_application_config: spark_sql_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_sql_application_config DataprocGdcSparkApplication#spark_sql_application_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#timeouts DataprocGdcSparkApplication#timeouts}
        :param version: The Dataproc version of this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#version DataprocGdcSparkApplication#version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(pyspark_application_config, dict):
            pyspark_application_config = DataprocGdcSparkApplicationPysparkApplicationConfig(**pyspark_application_config)
        if isinstance(spark_application_config, dict):
            spark_application_config = DataprocGdcSparkApplicationSparkApplicationConfig(**spark_application_config)
        if isinstance(spark_r_application_config, dict):
            spark_r_application_config = DataprocGdcSparkApplicationSparkRApplicationConfig(**spark_r_application_config)
        if isinstance(spark_sql_application_config, dict):
            spark_sql_application_config = DataprocGdcSparkApplicationSparkSqlApplicationConfig(**spark_sql_application_config)
        if isinstance(timeouts, dict):
            timeouts = DataprocGdcSparkApplicationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc4ef0cd4b03124b001221405f8614656bf06b59b4e3e171297cf3422a98d875)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument serviceinstance", value=serviceinstance, expected_type=type_hints["serviceinstance"])
            check_type(argname="argument spark_application_id", value=spark_application_id, expected_type=type_hints["spark_application_id"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument application_environment", value=application_environment, expected_type=type_hints["application_environment"])
            check_type(argname="argument dependency_images", value=dependency_images, expected_type=type_hints["dependency_images"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument pyspark_application_config", value=pyspark_application_config, expected_type=type_hints["pyspark_application_config"])
            check_type(argname="argument spark_application_config", value=spark_application_config, expected_type=type_hints["spark_application_config"])
            check_type(argname="argument spark_r_application_config", value=spark_r_application_config, expected_type=type_hints["spark_r_application_config"])
            check_type(argname="argument spark_sql_application_config", value=spark_sql_application_config, expected_type=type_hints["spark_sql_application_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "serviceinstance": serviceinstance,
            "spark_application_id": spark_application_id,
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
        if annotations is not None:
            self._values["annotations"] = annotations
        if application_environment is not None:
            self._values["application_environment"] = application_environment
        if dependency_images is not None:
            self._values["dependency_images"] = dependency_images
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if namespace is not None:
            self._values["namespace"] = namespace
        if project is not None:
            self._values["project"] = project
        if properties is not None:
            self._values["properties"] = properties
        if pyspark_application_config is not None:
            self._values["pyspark_application_config"] = pyspark_application_config
        if spark_application_config is not None:
            self._values["spark_application_config"] = spark_application_config
        if spark_r_application_config is not None:
            self._values["spark_r_application_config"] = spark_r_application_config
        if spark_sql_application_config is not None:
            self._values["spark_sql_application_config"] = spark_sql_application_config
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version is not None:
            self._values["version"] = version

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
    def location(self) -> builtins.str:
        '''The location of the spark application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#location DataprocGdcSparkApplication#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def serviceinstance(self) -> builtins.str:
        '''The id of the service instance to which this spark application belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#serviceinstance DataprocGdcSparkApplication#serviceinstance}
        '''
        result = self._values.get("serviceinstance")
        assert result is not None, "Required property 'serviceinstance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spark_application_id(self) -> builtins.str:
        '''The id of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_application_id DataprocGdcSparkApplication#spark_application_id}
        '''
        result = self._values.get("spark_application_id")
        assert result is not None, "Required property 'spark_application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The annotations to associate with this application.

        Annotations may be used to store client information, but are not used by the server.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#annotations DataprocGdcSparkApplication#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def application_environment(self) -> typing.Optional[builtins.str]:
        '''An ApplicationEnvironment from which to inherit configuration properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#application_environment DataprocGdcSparkApplication#application_environment}
        '''
        result = self._values.get("application_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependency_images(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of container image uris for additional file dependencies.

        Dependent files are sequentially copied from each image. If a file with the same name exists in 2 images then the file from later image is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#dependency_images DataprocGdcSparkApplication#dependency_images}
        '''
        result = self._values.get("dependency_images")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-provided human-readable name to be used in user interfaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#display_name DataprocGdcSparkApplication#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#id DataprocGdcSparkApplication#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels to associate with this application. Labels may be used for filtering and billing tracking.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#labels DataprocGdcSparkApplication#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace in which to create the application. This namespace must already exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#namespace DataprocGdcSparkApplication#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#project DataprocGdcSparkApplication#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''application-specific properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#properties DataprocGdcSparkApplication#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def pyspark_application_config(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationPysparkApplicationConfig"]:
        '''pyspark_application_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#pyspark_application_config DataprocGdcSparkApplication#pyspark_application_config}
        '''
        result = self._values.get("pyspark_application_config")
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationPysparkApplicationConfig"], result)

    @builtins.property
    def spark_application_config(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationSparkApplicationConfig"]:
        '''spark_application_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_application_config DataprocGdcSparkApplication#spark_application_config}
        '''
        result = self._values.get("spark_application_config")
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationSparkApplicationConfig"], result)

    @builtins.property
    def spark_r_application_config(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationSparkRApplicationConfig"]:
        '''spark_r_application_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_r_application_config DataprocGdcSparkApplication#spark_r_application_config}
        '''
        result = self._values.get("spark_r_application_config")
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationSparkRApplicationConfig"], result)

    @builtins.property
    def spark_sql_application_config(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationSparkSqlApplicationConfig"]:
        '''spark_sql_application_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#spark_sql_application_config DataprocGdcSparkApplication#spark_sql_application_config}
        '''
        result = self._values.get("spark_sql_application_config")
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationSparkSqlApplicationConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataprocGdcSparkApplicationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#timeouts DataprocGdcSparkApplication#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Dataproc version of this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#version DataprocGdcSparkApplication#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocGdcSparkApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationPysparkApplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "main_python_file_uri": "mainPythonFileUri",
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "python_file_uris": "pythonFileUris",
    },
)
class DataprocGdcSparkApplicationPysparkApplicationConfig:
    def __init__(
        self,
        *,
        main_python_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_python_file_uri: The HCFS URI of the main Python file to use as the driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_python_file_uri DataprocGdcSparkApplication#main_python_file_uri}
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        :param python_file_uris: HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#python_file_uris DataprocGdcSparkApplication#python_file_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3611e17a97d8fc560994f7197f13292c9c2fc8242a402e5fdfe9aa837f6ab24)
            check_type(argname="argument main_python_file_uri", value=main_python_file_uri, expected_type=type_hints["main_python_file_uri"])
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument python_file_uris", value=python_file_uris, expected_type=type_hints["python_file_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "main_python_file_uri": main_python_file_uri,
        }
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if python_file_uris is not None:
            self._values["python_file_uris"] = python_file_uris

    @builtins.property
    def main_python_file_uri(self) -> builtins.str:
        '''The HCFS URI of the main Python file to use as the driver. Must be a .py file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_python_file_uri DataprocGdcSparkApplication#main_python_file_uri}
        '''
        result = self._values.get("main_python_file_uri")
        assert result is not None, "Required property 'main_python_file_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def python_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#python_file_uris DataprocGdcSparkApplication#python_file_uris}
        '''
        result = self._values.get("python_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocGdcSparkApplicationPysparkApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocGdcSparkApplicationPysparkApplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationPysparkApplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9efe63a7bb2629402ef800b3905dac98519c243a4f6494ac5415d7d5f1a5b8a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d60c14562e9163f90d134d9714f82d7108e7853d34fd859bb4628cfb081d139d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c3032fcbd66e7bfefc1488095bcfd278dac8e2609b5e28e8ecb1e827c723bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d443ba09187f48323721adf4c16f5e055bbfabf883b5980e123e74950a73fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed69065506831538e37e8b5adca298262382054a3ea74e65b1769c374c55c407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUri")
    def main_python_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainPythonFileUri"))

    @main_python_file_uri.setter
    def main_python_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2034a60728804094d3f7a3f3d5587fd0619b8984962f80f9aa4d0daa868b376f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainPythonFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonFileUris")
    def python_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonFileUris"))

    @python_file_uris.setter
    def python_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d343d1d13bae55995dc0360df3bfd90d106242c4d003d37e226ca95bbe63c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocGdcSparkApplicationPysparkApplicationConfig]:
        return typing.cast(typing.Optional[DataprocGdcSparkApplicationPysparkApplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocGdcSparkApplicationPysparkApplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0c8897e8e0d4c29c969bedcb9fc4b3377b2583e4a0e782cf9ea9b798b4bda8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationSparkApplicationConfig",
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
class DataprocGdcSparkApplicationSparkApplicationConfig:
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: '.jar', '.tar', '.tar.gz', '.tgz', and '.zip'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as application properties, such as '--conf', since a collision can occur that causes an incorrect application submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        :param main_class: The name of the driver main class. The jar file that contains the class must be in the classpath or specified in 'jar_file_uris'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_class DataprocGdcSparkApplication#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_jar_file_uri DataprocGdcSparkApplication#main_jar_file_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaaaad758126a9ff1447f5641582b3337b4f1f7c26029d83a01065ea37b8544b)
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

        Supported file types: '.jar', '.tar', '.tar.gz', '.tgz', and '.zip'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments that can be set as application properties, such as '--conf', since a collision can occur that causes an incorrect application submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the classpath of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The name of the driver main class.

        The jar file that contains the class must be in the classpath or specified in 'jar_file_uris'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_class DataprocGdcSparkApplication#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the jar file that contains the main class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_jar_file_uri DataprocGdcSparkApplication#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocGdcSparkApplicationSparkApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocGdcSparkApplicationSparkApplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationSparkApplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcfd614f04dd837285cc62d675a003f70caf0cb3b1137817af71210a832e16f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72babcbe77c0cab093121c1b89f572822ada3548b9ae1a126e74d385007f5ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7384ad90c7abb32b557bb0849b2cedbd3ff416e17525b13017f4f23e7c898c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b03b7df793e8d71721707d80cfb72392ea4bb436f5b559db36b40354e24395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770849eed78510fda1e5c22e72b1e816c9b3cf6633679731fe9bcc29dd9426a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f82363c1257c426bc596b987bdef62165c95d9118d2b4f76d22b4c9ef5d6b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f996c3269766bf669fdab54d9d9f10a7f3948d21220d02f6df4330ef5bc97c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocGdcSparkApplicationSparkApplicationConfig]:
        return typing.cast(typing.Optional[DataprocGdcSparkApplicationSparkApplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocGdcSparkApplicationSparkApplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc4853133e7d8b8c43bd375b9f0a010b25851b5e22bc7f54b220e4da19d65d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationSparkRApplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "main_r_file_uri": "mainRFileUri",
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
    },
)
class DataprocGdcSparkApplicationSparkRApplicationConfig:
    def __init__(
        self,
        *,
        main_r_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_r_file_uri: The HCFS URI of the main R file to use as the driver. Must be a .R file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_r_file_uri DataprocGdcSparkApplication#main_r_file_uri}
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ded1236cd932e235bc544fa38017944a7c38695fb7f6826a259421c8b5dddf)
            check_type(argname="argument main_r_file_uri", value=main_r_file_uri, expected_type=type_hints["main_r_file_uri"])
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "main_r_file_uri": main_r_file_uri,
        }
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris

    @builtins.property
    def main_r_file_uri(self) -> builtins.str:
        '''The HCFS URI of the main R file to use as the driver. Must be a .R file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#main_r_file_uri DataprocGdcSparkApplication#main_r_file_uri}
        '''
        result = self._values.get("main_r_file_uri")
        assert result is not None, "Required property 'main_r_file_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#archive_uris DataprocGdcSparkApplication#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#args DataprocGdcSparkApplication#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#file_uris DataprocGdcSparkApplication#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocGdcSparkApplicationSparkRApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocGdcSparkApplicationSparkRApplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationSparkRApplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0c22d4ad4e56fb8afa19151e4029165c2ff0f6b3912f129e884ee5e4220f277)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6053c7c8175ead41a7f02caf635691917d5bb5dc85046161fb02fe7b91b602b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332d574f929f0a4b023d9397326de40f5874d3475074453f192db83537abacce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b60cfea37a132cfcbc181d5413d239553bbc40e6e466aa73599d3a5d1f238154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainRFileUri")
    def main_r_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainRFileUri"))

    @main_r_file_uri.setter
    def main_r_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90860f19b4a6435f5264ceff294d9a8e929eb3f4b2786d0b1119d9bdd20eab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainRFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocGdcSparkApplicationSparkRApplicationConfig]:
        return typing.cast(typing.Optional[DataprocGdcSparkApplicationSparkRApplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocGdcSparkApplicationSparkRApplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71d6b0a1985fd41bd433498daacb92ec16c26ec18d88a44c2098e66e7fc0209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationSparkSqlApplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "jar_file_uris": "jarFileUris",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
        "script_variables": "scriptVariables",
    },
)
class DataprocGdcSparkApplicationSparkSqlApplicationConfig:
    def __init__(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#query_file_uri DataprocGdcSparkApplication#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#query_list DataprocGdcSparkApplication#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET 'name="value";'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#script_variables DataprocGdcSparkApplication#script_variables}
        '''
        if isinstance(query_list, dict):
            query_list = DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct(**query_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c070f9eaefa21647004f5c41dc8787c7e6a8f64cfd9fdeca86e968730ef1926c)
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
            check_type(argname="argument script_variables", value=script_variables, expected_type=type_hints["script_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list
        if script_variables is not None:
            self._values["script_variables"] = script_variables

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to be added to the Spark CLASSPATH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#jar_file_uris DataprocGdcSparkApplication#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains SQL queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#query_file_uri DataprocGdcSparkApplication#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct"]:
        '''query_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#query_list DataprocGdcSparkApplication#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct"], result)

    @builtins.property
    def script_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping of query variable names to values (equivalent to the Spark SQL command: SET 'name="value";').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#script_variables DataprocGdcSparkApplication#script_variables}
        '''
        result = self._values.get("script_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocGdcSparkApplicationSparkSqlApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e81b9047e7156abc79a614c2e84c4d01b70dafdbf8fc9332337cd77db8fe3ee5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putQueryList")
    def put_query_list(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: The queries to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#queries DataprocGdcSparkApplication#queries}
        '''
        value = DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct(
            queries=queries
        )

        return typing.cast(None, jsii.invoke(self, "putQueryList", [value]))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetQueryFileUri")
    def reset_query_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryFileUri", []))

    @jsii.member(jsii_name="resetQueryList")
    def reset_query_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryList", []))

    @jsii.member(jsii_name="resetScriptVariables")
    def reset_script_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScriptVariables", []))

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(
        self,
    ) -> "DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference":
        return typing.cast("DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference", jsii.get(self, "queryList"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(
        self,
    ) -> typing.Optional["DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct"]:
        return typing.cast(typing.Optional["DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct"], jsii.get(self, "queryListInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptVariablesInput")
    def script_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "scriptVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d77644d9c757e0fff1906e9045afcefcc8dfd463bf68eb4b860d1c3a2be763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfef53ee7e51b33c0067008023d62fcc174ab29d18c9dd8e471d1cf3de2d90c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scriptVariables")
    def script_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "scriptVariables"))

    @script_variables.setter
    def script_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76e69d3d265681fd3ed3488f0dc1bf0027855b59e4ec6d68ddae0f3e949ba10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocGdcSparkApplicationSparkSqlApplicationConfig]:
        return typing.cast(typing.Optional[DataprocGdcSparkApplicationSparkSqlApplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocGdcSparkApplicationSparkSqlApplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700ca844299472454c2236b32eeeadef6e18d5b01cb20d643af1e39f4f5e56f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct",
    jsii_struct_bases=[],
    name_mapping={"queries": "queries"},
)
class DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct:
    def __init__(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: The queries to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#queries DataprocGdcSparkApplication#queries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faeb3e76f53d8232e34ac049e5ed8ecdb79cca0cc04c1487ef5ac0d3985c840b)
            check_type(argname="argument queries", value=queries, expected_type=type_hints["queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queries": queries,
        }

    @builtins.property
    def queries(self) -> typing.List[builtins.str]:
        '''The queries to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#queries DataprocGdcSparkApplication#queries}
        '''
        result = self._values.get("queries")
        assert result is not None, "Required property 'queries' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__523dc12686e6851450edebdc9867d885906cbfc35563e94657035bedc0ed6155)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="queriesInput")
    def queries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queriesInput"))

    @builtins.property
    @jsii.member(jsii_name="queries")
    def queries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queries"))

    @queries.setter
    def queries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb395923e8ead8f866cab4be775a3745da505211a1bdbfd424a98e4e31ad8851)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct]:
        return typing.cast(typing.Optional[DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9059a3800f561f98a9f9e32f71a8624cf83a219ae4c9aa6f77f9d760fb5fc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataprocGdcSparkApplicationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#create DataprocGdcSparkApplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#delete DataprocGdcSparkApplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#update DataprocGdcSparkApplication#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7c565cef7bca2763ba769407b9722d7a68af7613c0602a8c2678bbab7f8e18)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#create DataprocGdcSparkApplication#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#delete DataprocGdcSparkApplication#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_gdc_spark_application#update DataprocGdcSparkApplication#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocGdcSparkApplicationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocGdcSparkApplicationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocGdcSparkApplication.DataprocGdcSparkApplicationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cee2f5d0a66c07a18477183d0abfd2d4f3cee5e29332c4032503411e6d68303)
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
            type_hints = typing.get_type_hints(_typecheckingstub__979b1c26a8780bbfdaf946b782ed46b0cf77f8e32a15bfa1e3f5a69a6519b8cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812bdd00f5763b20503e7b346674d0d79c8349fe93b4da03b548917f1514c041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b596eef0176f6f647d839a42978a3f83b07ea889d815c178cbfe25664d2390)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocGdcSparkApplicationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocGdcSparkApplicationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocGdcSparkApplicationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0489769f00427c4e1cd0745a17f22eda2d7c14a312116b15551e189bd53706c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataprocGdcSparkApplication",
    "DataprocGdcSparkApplicationConfig",
    "DataprocGdcSparkApplicationPysparkApplicationConfig",
    "DataprocGdcSparkApplicationPysparkApplicationConfigOutputReference",
    "DataprocGdcSparkApplicationSparkApplicationConfig",
    "DataprocGdcSparkApplicationSparkApplicationConfigOutputReference",
    "DataprocGdcSparkApplicationSparkRApplicationConfig",
    "DataprocGdcSparkApplicationSparkRApplicationConfigOutputReference",
    "DataprocGdcSparkApplicationSparkSqlApplicationConfig",
    "DataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference",
    "DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct",
    "DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference",
    "DataprocGdcSparkApplicationTimeouts",
    "DataprocGdcSparkApplicationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__43699763398ba85e86a6ff3bd3536579784e9603c99b9dca1aa1564e26b710c6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    serviceinstance: builtins.str,
    spark_application_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    application_environment: typing.Optional[builtins.str] = None,
    dependency_images: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    pyspark_application_config: typing.Optional[typing.Union[DataprocGdcSparkApplicationPysparkApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_application_config: typing.Optional[typing.Union[DataprocGdcSparkApplicationSparkApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_application_config: typing.Optional[typing.Union[DataprocGdcSparkApplicationSparkRApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_application_config: typing.Optional[typing.Union[DataprocGdcSparkApplicationSparkSqlApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocGdcSparkApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d040fe899c172714e53dfd71fd686c7ac360ad4436a661bd3de675c5b0d6acde(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3968f05c46270c9cdc2118cfbf4e500b356a74700084375c95112c6380ba3ef(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292af0f00eabdd2fd821740ed03c044daccf6837947064cd073f812037bb36ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9126e358bee339826b6c53ae1f49580bcc11ca81d224dfb923c7ec1c7aeb39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2473e2f7f50fe120002b1c3e5bd253466e8821f00c15bf2a79b60ad4818464(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864ba9ec69de153ffb028ca7d6562b2823f0e89564db7a072cab5c60a375de22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb9ae1130ce8834b0f379934f4727329a3984b860c7a4a499825e74b73cd83e6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190b6c52cec3fd536e74099cd1167b68133549167bc37805bcf657b2b21d8f50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6d0a106a8c40f548bbbe918ecb9a3d05194d7261651e64ab0624d5bec20083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd1b296c71ed5f8bed1cfbdb3c8f80045d77a37432480273dd88bbc47442ae7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267223919eef39f8c783ac61e846da1b8859f39e686fffcade5027059c0dced9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ff33fad869778bf9d5e250d3239262e88c93e29bb8ae28c79a6933c62fad9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6071f9703c4000c474a34681196a01adcaa6cdfb735422d5c50085e2af87819f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b1b63a14c157b8bddfcb4745d32a729fbacee57571f227f17992f852cb2bb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc4ef0cd4b03124b001221405f8614656bf06b59b4e3e171297cf3422a98d875(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    serviceinstance: builtins.str,
    spark_application_id: builtins.str,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    application_environment: typing.Optional[builtins.str] = None,
    dependency_images: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    pyspark_application_config: typing.Optional[typing.Union[DataprocGdcSparkApplicationPysparkApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_application_config: typing.Optional[typing.Union[DataprocGdcSparkApplicationSparkApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_application_config: typing.Optional[typing.Union[DataprocGdcSparkApplicationSparkRApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_application_config: typing.Optional[typing.Union[DataprocGdcSparkApplicationSparkSqlApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocGdcSparkApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3611e17a97d8fc560994f7197f13292c9c2fc8242a402e5fdfe9aa837f6ab24(
    *,
    main_python_file_uri: builtins.str,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9efe63a7bb2629402ef800b3905dac98519c243a4f6494ac5415d7d5f1a5b8a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d60c14562e9163f90d134d9714f82d7108e7853d34fd859bb4628cfb081d139d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c3032fcbd66e7bfefc1488095bcfd278dac8e2609b5e28e8ecb1e827c723bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d443ba09187f48323721adf4c16f5e055bbfabf883b5980e123e74950a73fe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed69065506831538e37e8b5adca298262382054a3ea74e65b1769c374c55c407(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2034a60728804094d3f7a3f3d5587fd0619b8984962f80f9aa4d0daa868b376f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d343d1d13bae55995dc0360df3bfd90d106242c4d003d37e226ca95bbe63c0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0c8897e8e0d4c29c969bedcb9fc4b3377b2583e4a0e782cf9ea9b798b4bda8(
    value: typing.Optional[DataprocGdcSparkApplicationPysparkApplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaaaad758126a9ff1447f5641582b3337b4f1f7c26029d83a01065ea37b8544b(
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

def _typecheckingstub__dcfd614f04dd837285cc62d675a003f70caf0cb3b1137817af71210a832e16f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72babcbe77c0cab093121c1b89f572822ada3548b9ae1a126e74d385007f5ac0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7384ad90c7abb32b557bb0849b2cedbd3ff416e17525b13017f4f23e7c898c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b03b7df793e8d71721707d80cfb72392ea4bb436f5b559db36b40354e24395(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770849eed78510fda1e5c22e72b1e816c9b3cf6633679731fe9bcc29dd9426a1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f82363c1257c426bc596b987bdef62165c95d9118d2b4f76d22b4c9ef5d6b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f996c3269766bf669fdab54d9d9f10a7f3948d21220d02f6df4330ef5bc97c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc4853133e7d8b8c43bd375b9f0a010b25851b5e22bc7f54b220e4da19d65d4(
    value: typing.Optional[DataprocGdcSparkApplicationSparkApplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ded1236cd932e235bc544fa38017944a7c38695fb7f6826a259421c8b5dddf(
    *,
    main_r_file_uri: builtins.str,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c22d4ad4e56fb8afa19151e4029165c2ff0f6b3912f129e884ee5e4220f277(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6053c7c8175ead41a7f02caf635691917d5bb5dc85046161fb02fe7b91b602b0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332d574f929f0a4b023d9397326de40f5874d3475074453f192db83537abacce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60cfea37a132cfcbc181d5413d239553bbc40e6e466aa73599d3a5d1f238154(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90860f19b4a6435f5264ceff294d9a8e929eb3f4b2786d0b1119d9bdd20eab9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71d6b0a1985fd41bd433498daacb92ec16c26ec18d88a44c2098e66e7fc0209(
    value: typing.Optional[DataprocGdcSparkApplicationSparkRApplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c070f9eaefa21647004f5c41dc8787c7e6a8f64cfd9fdeca86e968730ef1926c(
    *,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Union[DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e81b9047e7156abc79a614c2e84c4d01b70dafdbf8fc9332337cd77db8fe3ee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d77644d9c757e0fff1906e9045afcefcc8dfd463bf68eb4b860d1c3a2be763(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfef53ee7e51b33c0067008023d62fcc174ab29d18c9dd8e471d1cf3de2d90c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76e69d3d265681fd3ed3488f0dc1bf0027855b59e4ec6d68ddae0f3e949ba10(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700ca844299472454c2236b32eeeadef6e18d5b01cb20d643af1e39f4f5e56f4(
    value: typing.Optional[DataprocGdcSparkApplicationSparkSqlApplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faeb3e76f53d8232e34ac049e5ed8ecdb79cca0cc04c1487ef5ac0d3985c840b(
    *,
    queries: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523dc12686e6851450edebdc9867d885906cbfc35563e94657035bedc0ed6155(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb395923e8ead8f866cab4be775a3745da505211a1bdbfd424a98e4e31ad8851(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9059a3800f561f98a9f9e32f71a8624cf83a219ae4c9aa6f77f9d760fb5fc9(
    value: typing.Optional[DataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7c565cef7bca2763ba769407b9722d7a68af7613c0602a8c2678bbab7f8e18(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cee2f5d0a66c07a18477183d0abfd2d4f3cee5e29332c4032503411e6d68303(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979b1c26a8780bbfdaf946b782ed46b0cf77f8e32a15bfa1e3f5a69a6519b8cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812bdd00f5763b20503e7b346674d0d79c8349fe93b4da03b548917f1514c041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b596eef0176f6f647d839a42978a3f83b07ea889d815c178cbfe25664d2390(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0489769f00427c4e1cd0745a17f22eda2d7c14a312116b15551e189bd53706c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocGdcSparkApplicationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

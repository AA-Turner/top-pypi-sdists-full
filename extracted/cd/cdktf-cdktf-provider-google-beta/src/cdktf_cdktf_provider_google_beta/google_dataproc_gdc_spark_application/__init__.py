r'''
# `google_dataproc_gdc_spark_application`

Refer to the Terraform Registry for docs: [`google_dataproc_gdc_spark_application`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application).
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


class GoogleDataprocGdcSparkApplication(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplication",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application google_dataproc_gdc_spark_application}.'''

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
        pyspark_application_config: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationPysparkApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_application_config: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationSparkApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_application_config: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationSparkRApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_application_config: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application google_dataproc_gdc_spark_application} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the spark application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#location GoogleDataprocGdcSparkApplication#location}
        :param serviceinstance: The id of the service instance to which this spark application belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#serviceinstance GoogleDataprocGdcSparkApplication#serviceinstance}
        :param spark_application_id: The id of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_application_id GoogleDataprocGdcSparkApplication#spark_application_id}
        :param annotations: The annotations to associate with this application. Annotations may be used to store client information, but are not used by the server. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#annotations GoogleDataprocGdcSparkApplication#annotations}
        :param application_environment: An ApplicationEnvironment from which to inherit configuration properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#application_environment GoogleDataprocGdcSparkApplication#application_environment}
        :param dependency_images: List of container image uris for additional file dependencies. Dependent files are sequentially copied from each image. If a file with the same name exists in 2 images then the file from later image is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#dependency_images GoogleDataprocGdcSparkApplication#dependency_images}
        :param display_name: User-provided human-readable name to be used in user interfaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#display_name GoogleDataprocGdcSparkApplication#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#id GoogleDataprocGdcSparkApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this application. Labels may be used for filtering and billing tracking. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#labels GoogleDataprocGdcSparkApplication#labels}
        :param namespace: The Kubernetes namespace in which to create the application. This namespace must already exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#namespace GoogleDataprocGdcSparkApplication#namespace}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#project GoogleDataprocGdcSparkApplication#project}.
        :param properties: application-specific properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#properties GoogleDataprocGdcSparkApplication#properties}
        :param pyspark_application_config: pyspark_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#pyspark_application_config GoogleDataprocGdcSparkApplication#pyspark_application_config}
        :param spark_application_config: spark_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_application_config GoogleDataprocGdcSparkApplication#spark_application_config}
        :param spark_r_application_config: spark_r_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_r_application_config GoogleDataprocGdcSparkApplication#spark_r_application_config}
        :param spark_sql_application_config: spark_sql_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_sql_application_config GoogleDataprocGdcSparkApplication#spark_sql_application_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#timeouts GoogleDataprocGdcSparkApplication#timeouts}
        :param version: The Dataproc version of this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#version GoogleDataprocGdcSparkApplication#version}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b42dd7b27ac785932025906e10637673f6c65f78beb38358e38558cf9597fb58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataprocGdcSparkApplicationConfig(
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
        '''Generates CDKTF code for importing a GoogleDataprocGdcSparkApplication resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataprocGdcSparkApplication to import.
        :param import_from_id: The id of the existing GoogleDataprocGdcSparkApplication that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataprocGdcSparkApplication to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e6073723ed20b968cf18b19e9d7a8ca25f488bd5afc663fd9f5f5386a67d6c)
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
        :param main_python_file_uri: The HCFS URI of the main Python file to use as the driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_python_file_uri GoogleDataprocGdcSparkApplication#main_python_file_uri}
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        :param python_file_uris: HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#python_file_uris GoogleDataprocGdcSparkApplication#python_file_uris}
        '''
        value = GoogleDataprocGdcSparkApplicationPysparkApplicationConfig(
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: '.jar', '.tar', '.tar.gz', '.tgz', and '.zip'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as application properties, such as '--conf', since a collision can occur that causes an incorrect application submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        :param main_class: The name of the driver main class. The jar file that contains the class must be in the classpath or specified in 'jar_file_uris'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_class GoogleDataprocGdcSparkApplication#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_jar_file_uri GoogleDataprocGdcSparkApplication#main_jar_file_uri}
        '''
        value = GoogleDataprocGdcSparkApplicationSparkApplicationConfig(
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
        :param main_r_file_uri: The HCFS URI of the main R file to use as the driver. Must be a .R file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_r_file_uri GoogleDataprocGdcSparkApplication#main_r_file_uri}
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        '''
        value = GoogleDataprocGdcSparkApplicationSparkRApplicationConfig(
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
        query_list: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#query_file_uri GoogleDataprocGdcSparkApplication#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#query_list GoogleDataprocGdcSparkApplication#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET 'name="value";'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#script_variables GoogleDataprocGdcSparkApplication#script_variables}
        '''
        value = GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#create GoogleDataprocGdcSparkApplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#delete GoogleDataprocGdcSparkApplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#update GoogleDataprocGdcSparkApplication#update}.
        '''
        value = GoogleDataprocGdcSparkApplicationTimeouts(
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
    ) -> "GoogleDataprocGdcSparkApplicationPysparkApplicationConfigOutputReference":
        return typing.cast("GoogleDataprocGdcSparkApplicationPysparkApplicationConfigOutputReference", jsii.get(self, "pysparkApplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="sparkApplicationConfig")
    def spark_application_config(
        self,
    ) -> "GoogleDataprocGdcSparkApplicationSparkApplicationConfigOutputReference":
        return typing.cast("GoogleDataprocGdcSparkApplicationSparkApplicationConfigOutputReference", jsii.get(self, "sparkApplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparkRApplicationConfig")
    def spark_r_application_config(
        self,
    ) -> "GoogleDataprocGdcSparkApplicationSparkRApplicationConfigOutputReference":
        return typing.cast("GoogleDataprocGdcSparkApplicationSparkRApplicationConfigOutputReference", jsii.get(self, "sparkRApplicationConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlApplicationConfig")
    def spark_sql_application_config(
        self,
    ) -> "GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference":
        return typing.cast("GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference", jsii.get(self, "sparkSqlApplicationConfig"))

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
    def timeouts(self) -> "GoogleDataprocGdcSparkApplicationTimeoutsOutputReference":
        return typing.cast("GoogleDataprocGdcSparkApplicationTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationPysparkApplicationConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationPysparkApplicationConfig"], jsii.get(self, "pysparkApplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceinstanceInput")
    def serviceinstance_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceinstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkApplicationConfigInput")
    def spark_application_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationSparkApplicationConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationSparkApplicationConfig"], jsii.get(self, "sparkApplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkApplicationIdInput")
    def spark_application_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkRApplicationConfigInput")
    def spark_r_application_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationSparkRApplicationConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationSparkRApplicationConfig"], jsii.get(self, "sparkRApplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkSqlApplicationConfigInput")
    def spark_sql_application_config_input(
        self,
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig"]:
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig"], jsii.get(self, "sparkSqlApplicationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocGdcSparkApplicationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataprocGdcSparkApplicationTimeouts"]], jsii.get(self, "timeoutsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d62d24d8cb75a2a060f5739f3687ce24ff76c1e0c3f9be8d52f7c7882e158479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationEnvironment")
    def application_environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationEnvironment"))

    @application_environment.setter
    def application_environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c940be755bc60b4b2ea602c1d685f5c310bfe701f00e5e0118130848bacfdbc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependencyImages")
    def dependency_images(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependencyImages"))

    @dependency_images.setter
    def dependency_images(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8460441bd20e64bdcd82413f280ed53437440ebc95dd723de6bfb7e3c425153a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependencyImages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c5e23d4cbeb5a8d72f165f65c024207e2b2a5328da90390801cb2b1a67aa37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2cbf3601e3fa452adc53c542b31d39a1bce4bba23c0bef716a95854c9def72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf27962bf8bb6564fc210bd74bfd371b5acc9624f70e441ba7650e9e4625adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4021c307bcd4eddcf48e156eb5e737b4bf8e49e07f7097569b9a318ae2946604)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d42d8dc9f9966ca48affd8936d6527a13206e045ccaf61794927fd7396093802)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c82068eff13c68aa1f0036786beaec50d14e03f88cbfd66df3f77863e51029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064ef819948dc97cef75b2dbd2de5a3a50115e368dd2af3a2c796a61b24722ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceinstance")
    def serviceinstance(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceinstance"))

    @serviceinstance.setter
    def serviceinstance(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a4503f20574dedf61c3a471454e2cf578c9f20325ee188c11ec8bbcbb7d4ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceinstance", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sparkApplicationId")
    def spark_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sparkApplicationId"))

    @spark_application_id.setter
    def spark_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcd29a42ef6009815e93340fd17f31d4b41d186bc32e06077f5cb20e5eb5dd42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f832d29003045d8ee35f50234dc8aa9869f8dabbfac1f282e1ba480547e0189f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationConfig",
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
class GoogleDataprocGdcSparkApplicationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        pyspark_application_config: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationPysparkApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_application_config: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationSparkApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_r_application_config: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationSparkRApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_sql_application_config: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param location: The location of the spark application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#location GoogleDataprocGdcSparkApplication#location}
        :param serviceinstance: The id of the service instance to which this spark application belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#serviceinstance GoogleDataprocGdcSparkApplication#serviceinstance}
        :param spark_application_id: The id of the application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_application_id GoogleDataprocGdcSparkApplication#spark_application_id}
        :param annotations: The annotations to associate with this application. Annotations may be used to store client information, but are not used by the server. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#annotations GoogleDataprocGdcSparkApplication#annotations}
        :param application_environment: An ApplicationEnvironment from which to inherit configuration properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#application_environment GoogleDataprocGdcSparkApplication#application_environment}
        :param dependency_images: List of container image uris for additional file dependencies. Dependent files are sequentially copied from each image. If a file with the same name exists in 2 images then the file from later image is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#dependency_images GoogleDataprocGdcSparkApplication#dependency_images}
        :param display_name: User-provided human-readable name to be used in user interfaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#display_name GoogleDataprocGdcSparkApplication#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#id GoogleDataprocGdcSparkApplication#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels to associate with this application. Labels may be used for filtering and billing tracking. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#labels GoogleDataprocGdcSparkApplication#labels}
        :param namespace: The Kubernetes namespace in which to create the application. This namespace must already exist on the cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#namespace GoogleDataprocGdcSparkApplication#namespace}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#project GoogleDataprocGdcSparkApplication#project}.
        :param properties: application-specific properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#properties GoogleDataprocGdcSparkApplication#properties}
        :param pyspark_application_config: pyspark_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#pyspark_application_config GoogleDataprocGdcSparkApplication#pyspark_application_config}
        :param spark_application_config: spark_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_application_config GoogleDataprocGdcSparkApplication#spark_application_config}
        :param spark_r_application_config: spark_r_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_r_application_config GoogleDataprocGdcSparkApplication#spark_r_application_config}
        :param spark_sql_application_config: spark_sql_application_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_sql_application_config GoogleDataprocGdcSparkApplication#spark_sql_application_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#timeouts GoogleDataprocGdcSparkApplication#timeouts}
        :param version: The Dataproc version of this application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#version GoogleDataprocGdcSparkApplication#version}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(pyspark_application_config, dict):
            pyspark_application_config = GoogleDataprocGdcSparkApplicationPysparkApplicationConfig(**pyspark_application_config)
        if isinstance(spark_application_config, dict):
            spark_application_config = GoogleDataprocGdcSparkApplicationSparkApplicationConfig(**spark_application_config)
        if isinstance(spark_r_application_config, dict):
            spark_r_application_config = GoogleDataprocGdcSparkApplicationSparkRApplicationConfig(**spark_r_application_config)
        if isinstance(spark_sql_application_config, dict):
            spark_sql_application_config = GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig(**spark_sql_application_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataprocGdcSparkApplicationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd267e84a14a58a7ee7bf6e6b2a12f7f54d5889fbc0caeff36393ad33f3b9ce0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#location GoogleDataprocGdcSparkApplication#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def serviceinstance(self) -> builtins.str:
        '''The id of the service instance to which this spark application belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#serviceinstance GoogleDataprocGdcSparkApplication#serviceinstance}
        '''
        result = self._values.get("serviceinstance")
        assert result is not None, "Required property 'serviceinstance' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spark_application_id(self) -> builtins.str:
        '''The id of the application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_application_id GoogleDataprocGdcSparkApplication#spark_application_id}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#annotations GoogleDataprocGdcSparkApplication#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def application_environment(self) -> typing.Optional[builtins.str]:
        '''An ApplicationEnvironment from which to inherit configuration properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#application_environment GoogleDataprocGdcSparkApplication#application_environment}
        '''
        result = self._values.get("application_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dependency_images(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of container image uris for additional file dependencies.

        Dependent files are sequentially copied from each image. If a file with the same name exists in 2 images then the file from later image is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#dependency_images GoogleDataprocGdcSparkApplication#dependency_images}
        '''
        result = self._values.get("dependency_images")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User-provided human-readable name to be used in user interfaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#display_name GoogleDataprocGdcSparkApplication#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#id GoogleDataprocGdcSparkApplication#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#labels GoogleDataprocGdcSparkApplication#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace in which to create the application. This namespace must already exist on the cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#namespace GoogleDataprocGdcSparkApplication#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#project GoogleDataprocGdcSparkApplication#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''application-specific properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#properties GoogleDataprocGdcSparkApplication#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def pyspark_application_config(
        self,
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationPysparkApplicationConfig"]:
        '''pyspark_application_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#pyspark_application_config GoogleDataprocGdcSparkApplication#pyspark_application_config}
        '''
        result = self._values.get("pyspark_application_config")
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationPysparkApplicationConfig"], result)

    @builtins.property
    def spark_application_config(
        self,
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationSparkApplicationConfig"]:
        '''spark_application_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_application_config GoogleDataprocGdcSparkApplication#spark_application_config}
        '''
        result = self._values.get("spark_application_config")
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationSparkApplicationConfig"], result)

    @builtins.property
    def spark_r_application_config(
        self,
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationSparkRApplicationConfig"]:
        '''spark_r_application_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_r_application_config GoogleDataprocGdcSparkApplication#spark_r_application_config}
        '''
        result = self._values.get("spark_r_application_config")
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationSparkRApplicationConfig"], result)

    @builtins.property
    def spark_sql_application_config(
        self,
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig"]:
        '''spark_sql_application_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#spark_sql_application_config GoogleDataprocGdcSparkApplication#spark_sql_application_config}
        '''
        result = self._values.get("spark_sql_application_config")
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataprocGdcSparkApplicationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#timeouts GoogleDataprocGdcSparkApplication#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationTimeouts"], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Dataproc version of this application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#version GoogleDataprocGdcSparkApplication#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocGdcSparkApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationPysparkApplicationConfig",
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
class GoogleDataprocGdcSparkApplicationPysparkApplicationConfig:
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
        :param main_python_file_uri: The HCFS URI of the main Python file to use as the driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_python_file_uri GoogleDataprocGdcSparkApplication#main_python_file_uri}
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        :param python_file_uris: HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#python_file_uris GoogleDataprocGdcSparkApplication#python_file_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126f6d2f990600d69968404debbb1885bd7fb450c81f2f6c2be2ce9f8fd568f7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_python_file_uri GoogleDataprocGdcSparkApplication#main_python_file_uri}
        '''
        result = self._values.get("main_python_file_uri")
        assert result is not None, "Required property 'main_python_file_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def python_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#python_file_uris GoogleDataprocGdcSparkApplication#python_file_uris}
        '''
        result = self._values.get("python_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocGdcSparkApplicationPysparkApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocGdcSparkApplicationPysparkApplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationPysparkApplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3d1657c936d0f4d7b22828249d23fd410dacfc734f88fabcb7dbf5c849979cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77b0073a829c65c85140595119d7a63bf13b0eb1f3375f178c94640502772b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1410e409d4abeeef34ba291875913f6c01a0f310f07e09d51af201df9ac0d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb108086e9f8c2b14b3e225f4895c19e30162c03202591674518bf9782de0337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc1e2f1ad97abefd1fd763d9451119f899cd937f22254f9f619e482555d48585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUri")
    def main_python_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainPythonFileUri"))

    @main_python_file_uri.setter
    def main_python_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc9a085727e61cae19d8202fa74f024f31e72553b5bae6a511ac4e80605a445)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainPythonFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonFileUris")
    def python_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonFileUris"))

    @python_file_uris.setter
    def python_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c64c175fa4933854e4528495308d08e61c78e790c7b36856b8f8f354d894fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocGdcSparkApplicationPysparkApplicationConfig]:
        return typing.cast(typing.Optional[GoogleDataprocGdcSparkApplicationPysparkApplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocGdcSparkApplicationPysparkApplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d4e52e63c55c76d18d57bc62a7008427342f90f1b56d09a78e4ccc9fd56056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationSparkApplicationConfig",
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
class GoogleDataprocGdcSparkApplicationSparkApplicationConfig:
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
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: '.jar', '.tar', '.tar.gz', '.tgz', and '.zip'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments that can be set as application properties, such as '--conf', since a collision can occur that causes an incorrect application submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the classpath of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        :param main_class: The name of the driver main class. The jar file that contains the class must be in the classpath or specified in 'jar_file_uris'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_class GoogleDataprocGdcSparkApplication#main_class}
        :param main_jar_file_uri: The HCFS URI of the jar file that contains the main class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_jar_file_uri GoogleDataprocGdcSparkApplication#main_jar_file_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19404586a6846dd0d4d528df14ae6659f9d85ad2d4651d32d6e056c8a07f9b2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments that can be set as application properties, such as '--conf', since a collision can occur that causes an incorrect application submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the classpath of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The name of the driver main class.

        The jar file that contains the class must be in the classpath or specified in 'jar_file_uris'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_class GoogleDataprocGdcSparkApplication#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the jar file that contains the main class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_jar_file_uri GoogleDataprocGdcSparkApplication#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocGdcSparkApplicationSparkApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocGdcSparkApplicationSparkApplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationSparkApplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df1b6135bb79a2a38093f7e916e28eab5f06503962ae221a619bb1254aafb914)
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
            type_hints = typing.get_type_hints(_typecheckingstub__859f1dcaf3bc86bdc868caff8924c7f984933a1fd3eba0b2c43f79c70163ef69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0279364d9d4e512fd5665c88aba751be6fc552c414b9e0f3e879da20857fb94d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2af90a9dbd69a533e05c8e67d3e13678c18319fdcf0f421e02824d09a8635202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ef8998ec38a306edb869114a3e783b2e40f3671d6af0071bc20091466e827e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9a459e29520c43f1100c2a120f35090a24047708dcbaf112bd7e614fab0a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__940b46749afd3422e7c3dad090e57380af777ba3de22e3a8f2ecd7febeac7526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocGdcSparkApplicationSparkApplicationConfig]:
        return typing.cast(typing.Optional[GoogleDataprocGdcSparkApplicationSparkApplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocGdcSparkApplicationSparkApplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4979fddb16710a1f15f4016c7badee988456d66f3a5cc42838f9c81d94c2c31d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationSparkRApplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "main_r_file_uri": "mainRFileUri",
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
    },
)
class GoogleDataprocGdcSparkApplicationSparkRApplicationConfig:
    def __init__(
        self,
        *,
        main_r_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_r_file_uri: The HCFS URI of the main R file to use as the driver. Must be a .R file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_r_file_uri GoogleDataprocGdcSparkApplication#main_r_file_uri}
        :param archive_uris: HCFS URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        :param args: The arguments to pass to the driver. Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        :param file_uris: HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3558e88fdd8e6980863c163a3749e400c0253e8eb36c6dbd7aa6f67115760ab8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#main_r_file_uri GoogleDataprocGdcSparkApplication#main_r_file_uri}
        '''
        result = self._values.get("main_r_file_uri")
        assert result is not None, "Required property 'main_r_file_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#archive_uris GoogleDataprocGdcSparkApplication#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Do not include arguments, such as '--conf', that can be set as job properties, since a collision may occur that causes an incorrect job submission.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#args GoogleDataprocGdcSparkApplication#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be placed in the working directory of each executor. Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#file_uris GoogleDataprocGdcSparkApplication#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocGdcSparkApplicationSparkRApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocGdcSparkApplicationSparkRApplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationSparkRApplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__709462a21cd24e60f886654ceb5464f5b03fc482e6099aa965668777cb824888)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c153b34c98e8d7fe3f7a9986fc35b08b786a34f3e4ed489eed77d22c5803041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce0b8e464b02ea76d3b53b282ffe469e0b264523dc123bc09ce4d1126a7357d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32d3d899d9a48cbefd78734eea62b2a5a1dbc67c7e77f2d1ec35cf6c53f642df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainRFileUri")
    def main_r_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainRFileUri"))

    @main_r_file_uri.setter
    def main_r_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a4d34401bcfd7c6e38d072a31ee1f6a95144dbb686f2efa9b229a95e60a7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainRFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocGdcSparkApplicationSparkRApplicationConfig]:
        return typing.cast(typing.Optional[GoogleDataprocGdcSparkApplicationSparkRApplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocGdcSparkApplicationSparkRApplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a621930daa0b2155fb6de405f3bf4b694c8494928f0ef1c13d9ded53db3f01f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "jar_file_uris": "jarFileUris",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
        "script_variables": "scriptVariables",
    },
)
class GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig:
    def __init__(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Union["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct", typing.Dict[builtins.str, typing.Any]]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#query_file_uri GoogleDataprocGdcSparkApplication#query_file_uri}
        :param query_list: query_list block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#query_list GoogleDataprocGdcSparkApplication#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET 'name="value";'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#script_variables GoogleDataprocGdcSparkApplication#script_variables}
        '''
        if isinstance(query_list, dict):
            query_list = GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct(**query_list)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12495f118bfac0cb1fa7e566813aee95c50aa54ad49b9d9e75bc4905945872aa)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#jar_file_uris GoogleDataprocGdcSparkApplication#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains SQL queries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#query_file_uri GoogleDataprocGdcSparkApplication#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(
        self,
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct"]:
        '''query_list block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#query_list GoogleDataprocGdcSparkApplication#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct"], result)

    @builtins.property
    def script_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping of query variable names to values (equivalent to the Spark SQL command: SET 'name="value";').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#script_variables GoogleDataprocGdcSparkApplication#script_variables}
        '''
        result = self._values.get("script_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ceeb7483351296e7e95e89ed017ae43853dfb0f14463709d17095558c7dcee6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putQueryList")
    def put_query_list(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: The queries to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#queries GoogleDataprocGdcSparkApplication#queries}
        '''
        value = GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct(
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
    ) -> "GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference":
        return typing.cast("GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference", jsii.get(self, "queryList"))

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
    ) -> typing.Optional["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct"]:
        return typing.cast(typing.Optional["GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct"], jsii.get(self, "queryListInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__05e0e9d1c4610b6bd2209b2cdda9ac9acc5bf762c60df8f1d2e7b6fc3c94bef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ed6c94e7b4c783bd949d03ecc13a5d1d886c4c1536bd2e32b7f4b83552440ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b2913040e5ebd6f535c787ff976451037fc1573cd4e70a9fd90ce487d7c1cc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig]:
        return typing.cast(typing.Optional[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a002d3126612fa4e64f15a88e4611f481dca0cb5ab697576263882d0df092b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct",
    jsii_struct_bases=[],
    name_mapping={"queries": "queries"},
)
class GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct:
    def __init__(self, *, queries: typing.Sequence[builtins.str]) -> None:
        '''
        :param queries: The queries to run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#queries GoogleDataprocGdcSparkApplication#queries}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922c30c1fed28d7d28d12f8fea73363789b9f7979a42e7b3a890f794f6a9488e)
            check_type(argname="argument queries", value=queries, expected_type=type_hints["queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "queries": queries,
        }

    @builtins.property
    def queries(self) -> typing.List[builtins.str]:
        '''The queries to run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#queries GoogleDataprocGdcSparkApplication#queries}
        '''
        result = self._values.get("queries")
        assert result is not None, "Required property 'queries' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cf4c6fcc78a5427f84888d2915c506e157dc57e09e9c61e80c87d63af49605d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25f0d44899e2d7d717d660d6e8215c3e62fd6a232becb66069521f279e522689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct]:
        return typing.cast(typing.Optional[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b416f42f22087f7284151f0f7fea678fc4b7002a4cf3bf13c2efc9aa792f8f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataprocGdcSparkApplicationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#create GoogleDataprocGdcSparkApplication#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#delete GoogleDataprocGdcSparkApplication#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#update GoogleDataprocGdcSparkApplication#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e13b1bffa6300fbd9787f71f1e3aaf6b34bd0eac98b9560989f552a013dc0db)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#create GoogleDataprocGdcSparkApplication#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#delete GoogleDataprocGdcSparkApplication#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataproc_gdc_spark_application#update GoogleDataprocGdcSparkApplication#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataprocGdcSparkApplicationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataprocGdcSparkApplicationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataprocGdcSparkApplication.GoogleDataprocGdcSparkApplicationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81657dc282d55b9ccce654bccbbdbdc4626bc4b2c4018d4c8751e07a122479eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a266bbc00c1ef0f6aaa9004dde2aa76d4cc0fdccc0b0f109fd1282ac8a2b3332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0859477a9e3de4cb90b1592e41833de85443fc04527dac961424a17d9fe7e8c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3865f4bff9595ff8604f8acb6e6f64f757f15681d426b8126a41d2d584d9fb37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocGdcSparkApplicationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocGdcSparkApplicationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocGdcSparkApplicationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa265aae39e4ad83cb85e7b7cf0e23b5b4b3b81d34867a5f452e674f42119387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataprocGdcSparkApplication",
    "GoogleDataprocGdcSparkApplicationConfig",
    "GoogleDataprocGdcSparkApplicationPysparkApplicationConfig",
    "GoogleDataprocGdcSparkApplicationPysparkApplicationConfigOutputReference",
    "GoogleDataprocGdcSparkApplicationSparkApplicationConfig",
    "GoogleDataprocGdcSparkApplicationSparkApplicationConfigOutputReference",
    "GoogleDataprocGdcSparkApplicationSparkRApplicationConfig",
    "GoogleDataprocGdcSparkApplicationSparkRApplicationConfigOutputReference",
    "GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig",
    "GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigOutputReference",
    "GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct",
    "GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStructOutputReference",
    "GoogleDataprocGdcSparkApplicationTimeouts",
    "GoogleDataprocGdcSparkApplicationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b42dd7b27ac785932025906e10637673f6c65f78beb38358e38558cf9597fb58(
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
    pyspark_application_config: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationPysparkApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_application_config: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationSparkApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_application_config: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationSparkRApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_application_config: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__12e6073723ed20b968cf18b19e9d7a8ca25f488bd5afc663fd9f5f5386a67d6c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62d24d8cb75a2a060f5739f3687ce24ff76c1e0c3f9be8d52f7c7882e158479(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c940be755bc60b4b2ea602c1d685f5c310bfe701f00e5e0118130848bacfdbc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8460441bd20e64bdcd82413f280ed53437440ebc95dd723de6bfb7e3c425153a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c5e23d4cbeb5a8d72f165f65c024207e2b2a5328da90390801cb2b1a67aa37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2cbf3601e3fa452adc53c542b31d39a1bce4bba23c0bef716a95854c9def72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf27962bf8bb6564fc210bd74bfd371b5acc9624f70e441ba7650e9e4625adb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4021c307bcd4eddcf48e156eb5e737b4bf8e49e07f7097569b9a318ae2946604(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d42d8dc9f9966ca48affd8936d6527a13206e045ccaf61794927fd7396093802(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c82068eff13c68aa1f0036786beaec50d14e03f88cbfd66df3f77863e51029(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064ef819948dc97cef75b2dbd2de5a3a50115e368dd2af3a2c796a61b24722ac(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a4503f20574dedf61c3a471454e2cf578c9f20325ee188c11ec8bbcbb7d4ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd29a42ef6009815e93340fd17f31d4b41d186bc32e06077f5cb20e5eb5dd42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f832d29003045d8ee35f50234dc8aa9869f8dabbfac1f282e1ba480547e0189f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd267e84a14a58a7ee7bf6e6b2a12f7f54d5889fbc0caeff36393ad33f3b9ce0(
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
    pyspark_application_config: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationPysparkApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_application_config: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationSparkApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_r_application_config: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationSparkRApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_sql_application_config: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126f6d2f990600d69968404debbb1885bd7fb450c81f2f6c2be2ce9f8fd568f7(
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

def _typecheckingstub__d3d1657c936d0f4d7b22828249d23fd410dacfc734f88fabcb7dbf5c849979cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b0073a829c65c85140595119d7a63bf13b0eb1f3375f178c94640502772b54(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1410e409d4abeeef34ba291875913f6c01a0f310f07e09d51af201df9ac0d6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb108086e9f8c2b14b3e225f4895c19e30162c03202591674518bf9782de0337(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc1e2f1ad97abefd1fd763d9451119f899cd937f22254f9f619e482555d48585(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc9a085727e61cae19d8202fa74f024f31e72553b5bae6a511ac4e80605a445(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c64c175fa4933854e4528495308d08e61c78e790c7b36856b8f8f354d894fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d4e52e63c55c76d18d57bc62a7008427342f90f1b56d09a78e4ccc9fd56056(
    value: typing.Optional[GoogleDataprocGdcSparkApplicationPysparkApplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19404586a6846dd0d4d528df14ae6659f9d85ad2d4651d32d6e056c8a07f9b2(
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

def _typecheckingstub__df1b6135bb79a2a38093f7e916e28eab5f06503962ae221a619bb1254aafb914(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859f1dcaf3bc86bdc868caff8924c7f984933a1fd3eba0b2c43f79c70163ef69(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0279364d9d4e512fd5665c88aba751be6fc552c414b9e0f3e879da20857fb94d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af90a9dbd69a533e05c8e67d3e13678c18319fdcf0f421e02824d09a8635202(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ef8998ec38a306edb869114a3e783b2e40f3671d6af0071bc20091466e827e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9a459e29520c43f1100c2a120f35090a24047708dcbaf112bd7e614fab0a58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__940b46749afd3422e7c3dad090e57380af777ba3de22e3a8f2ecd7febeac7526(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4979fddb16710a1f15f4016c7badee988456d66f3a5cc42838f9c81d94c2c31d(
    value: typing.Optional[GoogleDataprocGdcSparkApplicationSparkApplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3558e88fdd8e6980863c163a3749e400c0253e8eb36c6dbd7aa6f67115760ab8(
    *,
    main_r_file_uri: builtins.str,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709462a21cd24e60f886654ceb5464f5b03fc482e6099aa965668777cb824888(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c153b34c98e8d7fe3f7a9986fc35b08b786a34f3e4ed489eed77d22c5803041(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce0b8e464b02ea76d3b53b282ffe469e0b264523dc123bc09ce4d1126a7357d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32d3d899d9a48cbefd78734eea62b2a5a1dbc67c7e77f2d1ec35cf6c53f642df(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a4d34401bcfd7c6e38d072a31ee1f6a95144dbb686f2efa9b229a95e60a7f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a621930daa0b2155fb6de405f3bf4b694c8494928f0ef1c13d9ded53db3f01f7(
    value: typing.Optional[GoogleDataprocGdcSparkApplicationSparkRApplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12495f118bfac0cb1fa7e566813aee95c50aa54ad49b9d9e75bc4905945872aa(
    *,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Union[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct, typing.Dict[builtins.str, typing.Any]]] = None,
    script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ceeb7483351296e7e95e89ed017ae43853dfb0f14463709d17095558c7dcee6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e0e9d1c4610b6bd2209b2cdda9ac9acc5bf762c60df8f1d2e7b6fc3c94bef8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed6c94e7b4c783bd949d03ecc13a5d1d886c4c1536bd2e32b7f4b83552440ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2913040e5ebd6f535c787ff976451037fc1573cd4e70a9fd90ce487d7c1cc0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a002d3126612fa4e64f15a88e4611f481dca0cb5ab697576263882d0df092b88(
    value: typing.Optional[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922c30c1fed28d7d28d12f8fea73363789b9f7979a42e7b3a890f794f6a9488e(
    *,
    queries: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf4c6fcc78a5427f84888d2915c506e157dc57e09e9c61e80c87d63af49605d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f0d44899e2d7d717d660d6e8215c3e62fd6a232becb66069521f279e522689(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b416f42f22087f7284151f0f7fea678fc4b7002a4cf3bf13c2efc9aa792f8f5(
    value: typing.Optional[GoogleDataprocGdcSparkApplicationSparkSqlApplicationConfigQueryListStruct],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e13b1bffa6300fbd9787f71f1e3aaf6b34bd0eac98b9560989f552a013dc0db(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81657dc282d55b9ccce654bccbbdbdc4626bc4b2c4018d4c8751e07a122479eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a266bbc00c1ef0f6aaa9004dde2aa76d4cc0fdccc0b0f109fd1282ac8a2b3332(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0859477a9e3de4cb90b1592e41833de85443fc04527dac961424a17d9fe7e8c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3865f4bff9595ff8604f8acb6e6f64f757f15681d426b8126a41d2d584d9fb37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa265aae39e4ad83cb85e7b7cf0e23b5b4b3b81d34867a5f452e674f42119387(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataprocGdcSparkApplicationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

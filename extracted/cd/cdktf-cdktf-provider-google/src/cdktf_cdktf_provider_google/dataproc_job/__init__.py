r'''
# `google_dataproc_job`

Refer to the Terraform Registry for docs: [`google_dataproc_job`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job).
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


class DataprocJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJob",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job google_dataproc_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        placement: typing.Union["DataprocJobPlacement", typing.Dict[builtins.str, typing.Any]],
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hadoop_config: typing.Optional[typing.Union["DataprocJobHadoopConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_config: typing.Optional[typing.Union["DataprocJobHiveConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        pig_config: typing.Optional[typing.Union["DataprocJobPigConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        presto_config: typing.Optional[typing.Union["DataprocJobPrestoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        pyspark_config: typing.Optional[typing.Union["DataprocJobPysparkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        reference: typing.Optional[typing.Union["DataprocJobReference", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        scheduling: typing.Optional[typing.Union["DataprocJobScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_config: typing.Optional[typing.Union["DataprocJobSparkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sparksql_config: typing.Optional[typing.Union["DataprocJobSparksqlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job google_dataproc_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#placement DataprocJob#placement}
        :param force_delete: By default, you can only delete inactive jobs within Dataproc. Setting this to true, and calling destroy, will ensure that the job is first cancelled before issuing the delete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#force_delete DataprocJob#force_delete}
        :param hadoop_config: hadoop_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#hadoop_config DataprocJob#hadoop_config}
        :param hive_config: hive_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#hive_config DataprocJob#hive_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#id DataprocJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. The labels to associate with this job. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#labels DataprocJob#labels}
        :param pig_config: pig_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#pig_config DataprocJob#pig_config}
        :param presto_config: presto_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#presto_config DataprocJob#presto_config}
        :param project: The project in which the cluster can be found and jobs subsequently run against. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#project DataprocJob#project}
        :param pyspark_config: pyspark_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#pyspark_config DataprocJob#pyspark_config}
        :param reference: reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#reference DataprocJob#reference}
        :param region: The Cloud Dataproc region. This essentially determines which clusters are available for this job to be submitted to. If not specified, defaults to global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#region DataprocJob#region}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#scheduling DataprocJob#scheduling}
        :param spark_config: spark_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#spark_config DataprocJob#spark_config}
        :param sparksql_config: sparksql_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#sparksql_config DataprocJob#sparksql_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#timeouts DataprocJob#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d359f5e467197af5eb08fd9c707e56d1d2cfc77714b7dac2551c01517f1e0f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataprocJobConfig(
            placement=placement,
            force_delete=force_delete,
            hadoop_config=hadoop_config,
            hive_config=hive_config,
            id=id,
            labels=labels,
            pig_config=pig_config,
            presto_config=presto_config,
            project=project,
            pyspark_config=pyspark_config,
            reference=reference,
            region=region,
            scheduling=scheduling,
            spark_config=spark_config,
            sparksql_config=sparksql_config,
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
        '''Generates CDKTF code for importing a DataprocJob resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataprocJob to import.
        :param import_from_id: The id of the existing DataprocJob that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataprocJob to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e035dc6bb712520ac3867eb904948a6a31e52a0245cf44e00d9251a7f4e0cae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putHadoopConfig")
    def put_hadoop_config(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobHadoopConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        :param args: The arguments to pass to the driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        :param file_uris: HCFS URIs of files to be copied to the working directory of Spark drivers and distributed tasks. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param main_class: The class containing the main method of the driver. Must be in a provided jar or jar that is already on the classpath. Conflicts with main_jar_file_uri Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_class DataprocJob#main_class}
        :param main_jar_file_uri: The HCFS URI of jar file containing the driver jar. Conflicts with main_class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_jar_file_uri DataprocJob#main_jar_file_uri}
        :param properties: A mapping of property names to values, used to configure Spark. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        value = DataprocJobHadoopConfig(
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            main_class=main_class,
            main_jar_file_uri=main_jar_file_uri,
            properties=properties,
        )

        return typing.cast(None, jsii.invoke(self, "putHadoopConfig", [value]))

    @jsii.member(jsii_name="putHiveConfig")
    def put_hive_config(
        self,
        *,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param continue_on_failure: Whether to continue executing queries if a query fails. The default value is false. Setting to true can be useful when executing independent parallel queries. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATH of the Hive server and Hadoop MapReduce (MR) tasks. Can contain Hive SerDes and UDFs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param properties: A mapping of property names and values, used to configure Hive. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/hive/conf/hive-site.xml, and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param query_file_uri: HCFS URI of file containing Hive script to execute as the job. Conflicts with query_list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        :param query_list: The list of Hive queries or statements to execute as part of the job. Conflicts with query_file_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Hive command: SET name="value";). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        value = DataprocJobHiveConfig(
            continue_on_failure=continue_on_failure,
            jar_file_uris=jar_file_uris,
            properties=properties,
            query_file_uri=query_file_uri,
            query_list=query_list,
            script_variables=script_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putHiveConfig", [value]))

    @jsii.member(jsii_name="putPigConfig")
    def put_pig_config(
        self,
        *,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobPigConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param continue_on_failure: Whether to continue executing queries if a query fails. The default value is false. Setting to true can be useful when executing independent parallel queries. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATH of the Pig Client and Hadoop MapReduce (MR) tasks. Can contain Pig UDFs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param properties: A mapping of property names to values, used to configure Pig. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/pig/conf/pig.properties, and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param query_file_uri: HCFS URI of file containing Hive script to execute as the job. Conflicts with query_list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        :param query_list: The list of Hive queries or statements to execute as part of the job. Conflicts with query_file_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Pig command: name=[value]). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        value = DataprocJobPigConfig(
            continue_on_failure=continue_on_failure,
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            properties=properties,
            query_file_uri=query_file_uri,
            query_list=query_list,
            script_variables=script_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putPigConfig", [value]))

    @jsii.member(jsii_name="putPlacement")
    def put_placement(self, *, cluster_name: builtins.str) -> None:
        '''
        :param cluster_name: The name of the cluster where the job will be submitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#cluster_name DataprocJob#cluster_name}
        '''
        value = DataprocJobPlacement(cluster_name=cluster_name)

        return typing.cast(None, jsii.invoke(self, "putPlacement", [value]))

    @jsii.member(jsii_name="putPrestoConfig")
    def put_presto_config(
        self,
        *,
        client_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobPrestoConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        output_format: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_tags: Presto client tags to attach to this query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#client_tags DataprocJob#client_tags}
        :param continue_on_failure: Whether to continue executing queries if a query fails. Setting to true can be useful when executing independent parallel queries. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param output_format: The format in which query output will be displayed. See the Presto documentation for supported output formats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#output_format DataprocJob#output_format}
        :param properties: A mapping of property names to values. Used to set Presto session properties Equivalent to using the --session flag in the Presto CLI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Conflicts with query_list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        :param query_list: The list of SQL queries or statements to execute as part of the job. Conflicts with query_file_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        '''
        value = DataprocJobPrestoConfig(
            client_tags=client_tags,
            continue_on_failure=continue_on_failure,
            logging_config=logging_config,
            output_format=output_format,
            properties=properties,
            query_file_uri=query_file_uri,
            query_list=query_list,
        )

        return typing.cast(None, jsii.invoke(self, "putPrestoConfig", [value]))

    @jsii.member(jsii_name="putPysparkConfig")
    def put_pyspark_config(
        self,
        *,
        main_python_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobPysparkConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_python_file_uri: Required. The HCFS URI of the main Python file to use as the driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_python_file_uri DataprocJob#main_python_file_uri}
        :param archive_uris: Optional. HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as --conf, that can be set as job properties, since a collision may occur that causes an incorrect job submission Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        :param file_uris: Optional. HCFS URIs of files to be copied to the working directory of Python drivers and distributed tasks. Useful for naively parallel tasks Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure PySpark. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param python_file_uris: Optional. HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#python_file_uris DataprocJob#python_file_uris}
        '''
        value = DataprocJobPysparkConfig(
            main_python_file_uri=main_python_file_uri,
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            properties=properties,
            python_file_uris=python_file_uris,
        )

        return typing.cast(None, jsii.invoke(self, "putPysparkConfig", [value]))

    @jsii.member(jsii_name="putReference")
    def put_reference(self, *, job_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param job_id: The job ID, which must be unique within the project. The job ID is generated by the server upon job submission or provided by the user as a means to perform retries without creating duplicate jobs Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#job_id DataprocJob#job_id}
        '''
        value = DataprocJobReference(job_id=job_id)

        return typing.cast(None, jsii.invoke(self, "putReference", [value]))

    @jsii.member(jsii_name="putScheduling")
    def put_scheduling(
        self,
        *,
        max_failures_per_hour: jsii.Number,
        max_failures_total: jsii.Number,
    ) -> None:
        '''
        :param max_failures_per_hour: Maximum number of times per hour a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#max_failures_per_hour DataprocJob#max_failures_per_hour}
        :param max_failures_total: Maximum number of times in total a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#max_failures_total DataprocJob#max_failures_total}
        '''
        value = DataprocJobScheduling(
            max_failures_per_hour=max_failures_per_hour,
            max_failures_total=max_failures_total,
        )

        return typing.cast(None, jsii.invoke(self, "putScheduling", [value]))

    @jsii.member(jsii_name="putSparkConfig")
    def put_spark_config(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobSparkConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        :param args: The arguments to pass to the driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        :param file_uris: HCFS URIs of files to be copied to the working directory of Spark drivers and distributed tasks. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param main_class: The class containing the main method of the driver. Must be in a provided jar or jar that is already on the classpath. Conflicts with main_jar_file_uri Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_class DataprocJob#main_class}
        :param main_jar_file_uri: The HCFS URI of jar file containing the driver jar. Conflicts with main_class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_jar_file_uri DataprocJob#main_jar_file_uri}
        :param properties: A mapping of property names to values, used to configure Spark. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        value = DataprocJobSparkConfig(
            archive_uris=archive_uris,
            args=args,
            file_uris=file_uris,
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            main_class=main_class,
            main_jar_file_uri=main_jar_file_uri,
            properties=properties,
        )

        return typing.cast(None, jsii.invoke(self, "putSparkConfig", [value]))

    @jsii.member(jsii_name="putSparksqlConfig")
    def put_sparksql_config(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobSparksqlConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param properties: A mapping of property names to values, used to configure Spark SQL's SparkConf. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Conflicts with query_list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        :param query_list: The list of SQL queries or statements to execute as part of the job. Conflicts with query_file_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        value = DataprocJobSparksqlConfig(
            jar_file_uris=jar_file_uris,
            logging_config=logging_config,
            properties=properties,
            query_file_uri=query_file_uri,
            query_list=query_list,
            script_variables=script_variables,
        )

        return typing.cast(None, jsii.invoke(self, "putSparksqlConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#create DataprocJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#delete DataprocJob#delete}.
        '''
        value = DataprocJobTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetForceDelete")
    def reset_force_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForceDelete", []))

    @jsii.member(jsii_name="resetHadoopConfig")
    def reset_hadoop_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHadoopConfig", []))

    @jsii.member(jsii_name="resetHiveConfig")
    def reset_hive_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHiveConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetPigConfig")
    def reset_pig_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPigConfig", []))

    @jsii.member(jsii_name="resetPrestoConfig")
    def reset_presto_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrestoConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetPysparkConfig")
    def reset_pyspark_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPysparkConfig", []))

    @jsii.member(jsii_name="resetReference")
    def reset_reference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReference", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetScheduling")
    def reset_scheduling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduling", []))

    @jsii.member(jsii_name="resetSparkConfig")
    def reset_spark_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparkConfig", []))

    @jsii.member(jsii_name="resetSparksqlConfig")
    def reset_sparksql_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSparksqlConfig", []))

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
    @jsii.member(jsii_name="driverControlsFilesUri")
    def driver_controls_files_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverControlsFilesUri"))

    @builtins.property
    @jsii.member(jsii_name="driverOutputResourceUri")
    def driver_output_resource_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "driverOutputResourceUri"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="hadoopConfig")
    def hadoop_config(self) -> "DataprocJobHadoopConfigOutputReference":
        return typing.cast("DataprocJobHadoopConfigOutputReference", jsii.get(self, "hadoopConfig"))

    @builtins.property
    @jsii.member(jsii_name="hiveConfig")
    def hive_config(self) -> "DataprocJobHiveConfigOutputReference":
        return typing.cast("DataprocJobHiveConfigOutputReference", jsii.get(self, "hiveConfig"))

    @builtins.property
    @jsii.member(jsii_name="pigConfig")
    def pig_config(self) -> "DataprocJobPigConfigOutputReference":
        return typing.cast("DataprocJobPigConfigOutputReference", jsii.get(self, "pigConfig"))

    @builtins.property
    @jsii.member(jsii_name="placement")
    def placement(self) -> "DataprocJobPlacementOutputReference":
        return typing.cast("DataprocJobPlacementOutputReference", jsii.get(self, "placement"))

    @builtins.property
    @jsii.member(jsii_name="prestoConfig")
    def presto_config(self) -> "DataprocJobPrestoConfigOutputReference":
        return typing.cast("DataprocJobPrestoConfigOutputReference", jsii.get(self, "prestoConfig"))

    @builtins.property
    @jsii.member(jsii_name="pysparkConfig")
    def pyspark_config(self) -> "DataprocJobPysparkConfigOutputReference":
        return typing.cast("DataprocJobPysparkConfigOutputReference", jsii.get(self, "pysparkConfig"))

    @builtins.property
    @jsii.member(jsii_name="reference")
    def reference(self) -> "DataprocJobReferenceOutputReference":
        return typing.cast("DataprocJobReferenceOutputReference", jsii.get(self, "reference"))

    @builtins.property
    @jsii.member(jsii_name="scheduling")
    def scheduling(self) -> "DataprocJobSchedulingOutputReference":
        return typing.cast("DataprocJobSchedulingOutputReference", jsii.get(self, "scheduling"))

    @builtins.property
    @jsii.member(jsii_name="sparkConfig")
    def spark_config(self) -> "DataprocJobSparkConfigOutputReference":
        return typing.cast("DataprocJobSparkConfigOutputReference", jsii.get(self, "sparkConfig"))

    @builtins.property
    @jsii.member(jsii_name="sparksqlConfig")
    def sparksql_config(self) -> "DataprocJobSparksqlConfigOutputReference":
        return typing.cast("DataprocJobSparksqlConfigOutputReference", jsii.get(self, "sparksqlConfig"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "DataprocJobStatusList":
        return typing.cast("DataprocJobStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataprocJobTimeoutsOutputReference":
        return typing.cast("DataprocJobTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="forceDeleteInput")
    def force_delete_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "forceDeleteInput"))

    @builtins.property
    @jsii.member(jsii_name="hadoopConfigInput")
    def hadoop_config_input(self) -> typing.Optional["DataprocJobHadoopConfig"]:
        return typing.cast(typing.Optional["DataprocJobHadoopConfig"], jsii.get(self, "hadoopConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="hiveConfigInput")
    def hive_config_input(self) -> typing.Optional["DataprocJobHiveConfig"]:
        return typing.cast(typing.Optional["DataprocJobHiveConfig"], jsii.get(self, "hiveConfigInput"))

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
    @jsii.member(jsii_name="pigConfigInput")
    def pig_config_input(self) -> typing.Optional["DataprocJobPigConfig"]:
        return typing.cast(typing.Optional["DataprocJobPigConfig"], jsii.get(self, "pigConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="placementInput")
    def placement_input(self) -> typing.Optional["DataprocJobPlacement"]:
        return typing.cast(typing.Optional["DataprocJobPlacement"], jsii.get(self, "placementInput"))

    @builtins.property
    @jsii.member(jsii_name="prestoConfigInput")
    def presto_config_input(self) -> typing.Optional["DataprocJobPrestoConfig"]:
        return typing.cast(typing.Optional["DataprocJobPrestoConfig"], jsii.get(self, "prestoConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="pysparkConfigInput")
    def pyspark_config_input(self) -> typing.Optional["DataprocJobPysparkConfig"]:
        return typing.cast(typing.Optional["DataprocJobPysparkConfig"], jsii.get(self, "pysparkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceInput")
    def reference_input(self) -> typing.Optional["DataprocJobReference"]:
        return typing.cast(typing.Optional["DataprocJobReference"], jsii.get(self, "referenceInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulingInput")
    def scheduling_input(self) -> typing.Optional["DataprocJobScheduling"]:
        return typing.cast(typing.Optional["DataprocJobScheduling"], jsii.get(self, "schedulingInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkConfigInput")
    def spark_config_input(self) -> typing.Optional["DataprocJobSparkConfig"]:
        return typing.cast(typing.Optional["DataprocJobSparkConfig"], jsii.get(self, "sparkConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sparksqlConfigInput")
    def sparksql_config_input(self) -> typing.Optional["DataprocJobSparksqlConfig"]:
        return typing.cast(typing.Optional["DataprocJobSparksqlConfig"], jsii.get(self, "sparksqlConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocJobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataprocJobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="forceDelete")
    def force_delete(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "forceDelete"))

    @force_delete.setter
    def force_delete(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea356f34e4434378fdd1352620965feaf770e9190f54fe49ec71650b906a5ecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forceDelete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c90ecf842186c821de90ec65f564591377c212d4f268c5d40c641ef6bcf6b562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5fd53089eee46c1e9295231b3afcb173d91c0753539e1e137974147e30dd2d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c86ca0274edb24688ca5062b59c7bf80f8db521fc391c20b9a71953a212665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77ff4f1cbd21d2be5c3b84d845c001c5268b170b34b42da4282e11df0d3e4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "placement": "placement",
        "force_delete": "forceDelete",
        "hadoop_config": "hadoopConfig",
        "hive_config": "hiveConfig",
        "id": "id",
        "labels": "labels",
        "pig_config": "pigConfig",
        "presto_config": "prestoConfig",
        "project": "project",
        "pyspark_config": "pysparkConfig",
        "reference": "reference",
        "region": "region",
        "scheduling": "scheduling",
        "spark_config": "sparkConfig",
        "sparksql_config": "sparksqlConfig",
        "timeouts": "timeouts",
    },
)
class DataprocJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        placement: typing.Union["DataprocJobPlacement", typing.Dict[builtins.str, typing.Any]],
        force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hadoop_config: typing.Optional[typing.Union["DataprocJobHadoopConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        hive_config: typing.Optional[typing.Union["DataprocJobHiveConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        pig_config: typing.Optional[typing.Union["DataprocJobPigConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        presto_config: typing.Optional[typing.Union["DataprocJobPrestoConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        pyspark_config: typing.Optional[typing.Union["DataprocJobPysparkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        reference: typing.Optional[typing.Union["DataprocJobReference", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
        scheduling: typing.Optional[typing.Union["DataprocJobScheduling", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_config: typing.Optional[typing.Union["DataprocJobSparkConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sparksql_config: typing.Optional[typing.Union["DataprocJobSparksqlConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DataprocJobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param placement: placement block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#placement DataprocJob#placement}
        :param force_delete: By default, you can only delete inactive jobs within Dataproc. Setting this to true, and calling destroy, will ensure that the job is first cancelled before issuing the delete. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#force_delete DataprocJob#force_delete}
        :param hadoop_config: hadoop_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#hadoop_config DataprocJob#hadoop_config}
        :param hive_config: hive_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#hive_config DataprocJob#hive_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#id DataprocJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. The labels to associate with this job. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#labels DataprocJob#labels}
        :param pig_config: pig_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#pig_config DataprocJob#pig_config}
        :param presto_config: presto_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#presto_config DataprocJob#presto_config}
        :param project: The project in which the cluster can be found and jobs subsequently run against. If it is not provided, the provider project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#project DataprocJob#project}
        :param pyspark_config: pyspark_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#pyspark_config DataprocJob#pyspark_config}
        :param reference: reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#reference DataprocJob#reference}
        :param region: The Cloud Dataproc region. This essentially determines which clusters are available for this job to be submitted to. If not specified, defaults to global. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#region DataprocJob#region}
        :param scheduling: scheduling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#scheduling DataprocJob#scheduling}
        :param spark_config: spark_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#spark_config DataprocJob#spark_config}
        :param sparksql_config: sparksql_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#sparksql_config DataprocJob#sparksql_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#timeouts DataprocJob#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(placement, dict):
            placement = DataprocJobPlacement(**placement)
        if isinstance(hadoop_config, dict):
            hadoop_config = DataprocJobHadoopConfig(**hadoop_config)
        if isinstance(hive_config, dict):
            hive_config = DataprocJobHiveConfig(**hive_config)
        if isinstance(pig_config, dict):
            pig_config = DataprocJobPigConfig(**pig_config)
        if isinstance(presto_config, dict):
            presto_config = DataprocJobPrestoConfig(**presto_config)
        if isinstance(pyspark_config, dict):
            pyspark_config = DataprocJobPysparkConfig(**pyspark_config)
        if isinstance(reference, dict):
            reference = DataprocJobReference(**reference)
        if isinstance(scheduling, dict):
            scheduling = DataprocJobScheduling(**scheduling)
        if isinstance(spark_config, dict):
            spark_config = DataprocJobSparkConfig(**spark_config)
        if isinstance(sparksql_config, dict):
            sparksql_config = DataprocJobSparksqlConfig(**sparksql_config)
        if isinstance(timeouts, dict):
            timeouts = DataprocJobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0578fea2b9fbad8b752ce63c843454f0cfbe081370de05b6c386c48f5d85d7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument placement", value=placement, expected_type=type_hints["placement"])
            check_type(argname="argument force_delete", value=force_delete, expected_type=type_hints["force_delete"])
            check_type(argname="argument hadoop_config", value=hadoop_config, expected_type=type_hints["hadoop_config"])
            check_type(argname="argument hive_config", value=hive_config, expected_type=type_hints["hive_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument pig_config", value=pig_config, expected_type=type_hints["pig_config"])
            check_type(argname="argument presto_config", value=presto_config, expected_type=type_hints["presto_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument pyspark_config", value=pyspark_config, expected_type=type_hints["pyspark_config"])
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument scheduling", value=scheduling, expected_type=type_hints["scheduling"])
            check_type(argname="argument spark_config", value=spark_config, expected_type=type_hints["spark_config"])
            check_type(argname="argument sparksql_config", value=sparksql_config, expected_type=type_hints["sparksql_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "placement": placement,
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
        if force_delete is not None:
            self._values["force_delete"] = force_delete
        if hadoop_config is not None:
            self._values["hadoop_config"] = hadoop_config
        if hive_config is not None:
            self._values["hive_config"] = hive_config
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if pig_config is not None:
            self._values["pig_config"] = pig_config
        if presto_config is not None:
            self._values["presto_config"] = presto_config
        if project is not None:
            self._values["project"] = project
        if pyspark_config is not None:
            self._values["pyspark_config"] = pyspark_config
        if reference is not None:
            self._values["reference"] = reference
        if region is not None:
            self._values["region"] = region
        if scheduling is not None:
            self._values["scheduling"] = scheduling
        if spark_config is not None:
            self._values["spark_config"] = spark_config
        if sparksql_config is not None:
            self._values["sparksql_config"] = sparksql_config
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
    def placement(self) -> "DataprocJobPlacement":
        '''placement block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#placement DataprocJob#placement}
        '''
        result = self._values.get("placement")
        assert result is not None, "Required property 'placement' is missing"
        return typing.cast("DataprocJobPlacement", result)

    @builtins.property
    def force_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''By default, you can only delete inactive jobs within Dataproc.

        Setting this to true, and calling destroy, will ensure that the job is first cancelled before issuing the delete.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#force_delete DataprocJob#force_delete}
        '''
        result = self._values.get("force_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hadoop_config(self) -> typing.Optional["DataprocJobHadoopConfig"]:
        '''hadoop_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#hadoop_config DataprocJob#hadoop_config}
        '''
        result = self._values.get("hadoop_config")
        return typing.cast(typing.Optional["DataprocJobHadoopConfig"], result)

    @builtins.property
    def hive_config(self) -> typing.Optional["DataprocJobHiveConfig"]:
        '''hive_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#hive_config DataprocJob#hive_config}
        '''
        result = self._values.get("hive_config")
        return typing.cast(typing.Optional["DataprocJobHiveConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#id DataprocJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. The labels to associate with this job.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#labels DataprocJob#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def pig_config(self) -> typing.Optional["DataprocJobPigConfig"]:
        '''pig_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#pig_config DataprocJob#pig_config}
        '''
        result = self._values.get("pig_config")
        return typing.cast(typing.Optional["DataprocJobPigConfig"], result)

    @builtins.property
    def presto_config(self) -> typing.Optional["DataprocJobPrestoConfig"]:
        '''presto_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#presto_config DataprocJob#presto_config}
        '''
        result = self._values.get("presto_config")
        return typing.cast(typing.Optional["DataprocJobPrestoConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project in which the cluster can be found and jobs subsequently run against.

        If it is not provided, the provider project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#project DataprocJob#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pyspark_config(self) -> typing.Optional["DataprocJobPysparkConfig"]:
        '''pyspark_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#pyspark_config DataprocJob#pyspark_config}
        '''
        result = self._values.get("pyspark_config")
        return typing.cast(typing.Optional["DataprocJobPysparkConfig"], result)

    @builtins.property
    def reference(self) -> typing.Optional["DataprocJobReference"]:
        '''reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#reference DataprocJob#reference}
        '''
        result = self._values.get("reference")
        return typing.cast(typing.Optional["DataprocJobReference"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The Cloud Dataproc region.

        This essentially determines which clusters are available for this job to be submitted to. If not specified, defaults to global.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#region DataprocJob#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduling(self) -> typing.Optional["DataprocJobScheduling"]:
        '''scheduling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#scheduling DataprocJob#scheduling}
        '''
        result = self._values.get("scheduling")
        return typing.cast(typing.Optional["DataprocJobScheduling"], result)

    @builtins.property
    def spark_config(self) -> typing.Optional["DataprocJobSparkConfig"]:
        '''spark_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#spark_config DataprocJob#spark_config}
        '''
        result = self._values.get("spark_config")
        return typing.cast(typing.Optional["DataprocJobSparkConfig"], result)

    @builtins.property
    def sparksql_config(self) -> typing.Optional["DataprocJobSparksqlConfig"]:
        '''sparksql_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#sparksql_config DataprocJob#sparksql_config}
        '''
        result = self._values.get("sparksql_config")
        return typing.cast(typing.Optional["DataprocJobSparksqlConfig"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataprocJobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#timeouts DataprocJob#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataprocJobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobHadoopConfig",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "main_class": "mainClass",
        "main_jar_file_uri": "mainJarFileUri",
        "properties": "properties",
    },
)
class DataprocJobHadoopConfig:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobHadoopConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        :param args: The arguments to pass to the driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        :param file_uris: HCFS URIs of files to be copied to the working directory of Spark drivers and distributed tasks. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param main_class: The class containing the main method of the driver. Must be in a provided jar or jar that is already on the classpath. Conflicts with main_jar_file_uri Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_class DataprocJob#main_class}
        :param main_jar_file_uri: The HCFS URI of jar file containing the driver jar. Conflicts with main_class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_jar_file_uri DataprocJob#main_jar_file_uri}
        :param properties: A mapping of property names to values, used to configure Spark. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocJobHadoopConfigLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de0216a673887532a18b5d83977f967cd5d11f3144ff56d79dd37d5580c36a8)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
            check_type(argname="argument main_jar_file_uri", value=main_jar_file_uri, expected_type=type_hints["main_jar_file_uri"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if main_class is not None:
            self._values["main_class"] = main_class
        if main_jar_file_uri is not None:
            self._values["main_jar_file_uri"] = main_jar_file_uri
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be copied to the working directory of Spark drivers and distributed tasks.

        Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["DataprocJobHadoopConfigLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocJobHadoopConfigLoggingConfig"], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The class containing the main method of the driver.

        Must be in a provided jar or jar that is already on the classpath. Conflicts with main_jar_file_uri

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_class DataprocJob#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of jar file containing the driver jar. Conflicts with main_class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_jar_file_uri DataprocJob#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values, used to configure Spark.

        Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobHadoopConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobHadoopConfigLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocJobHadoopConfigLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0840482f38d08cf13dfdf64569e6c8dd696e9a3ecfcc9fd28b38631c8546d929)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver_log_levels": driver_log_levels,
        }

    @builtins.property
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Optional.

        The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        assert result is not None, "Required property 'driver_log_levels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobHadoopConfigLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobHadoopConfigLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobHadoopConfigLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5cb1043e5c58121b41e4d95bbca5db5661659208970d119e08f4974482f75191)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5863e2221e4c9728b1655e2de33b891ff529e13fe1f5cbae75c2011a5121e1fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobHadoopConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobHadoopConfigLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocJobHadoopConfigLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c71916f1e778448b08fd51e2457a30337ddc9381101f8b719976212ce24d1830)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocJobHadoopConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobHadoopConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__893cc1916365a69c96c98c53d824d30826d827c43638f3a2f459f88697d6ed7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        value = DataprocJobHadoopConfigLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

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

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetMainClass")
    def reset_main_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainClass", []))

    @jsii.member(jsii_name="resetMainJarFileUri")
    def reset_main_jar_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainJarFileUri", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> DataprocJobHadoopConfigLoggingConfigOutputReference:
        return typing.cast(DataprocJobHadoopConfigLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

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
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocJobHadoopConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobHadoopConfigLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mainClassInput")
    def main_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainClassInput"))

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUriInput")
    def main_jar_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainJarFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcad4308dad4d9ab45bc148b86896a3816961275d805e1f58ad30e46802cce50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8ff95d538ddaf868541b66a5f629bc3baafee03cc6cf58aa262a30024f7ca5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566ac81283174bc60284512f0e9935679d72b4af53f5bc373318ac31d78c1827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fb57c0d58163c48f889285ef5900b024a83935b403bb7db6abcd572fa7ba1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3739b51f2ab2308e807ec53a28e733d444735c95ef966fa9e70007a551bcfa18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffa2299af0e9d7ddc3be13d862478a3d61a852e7c78ab5b4d960d8b0922b0fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e5f802e5f73f4cc4917b1ec7defe6b18736ff5d900168d8fa6fe64a3411b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobHadoopConfig]:
        return typing.cast(typing.Optional[DataprocJobHadoopConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobHadoopConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be94e0841a2ed1ad9b7679af4a66ed1782f126437ca816341e7dab199d535dd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobHiveConfig",
    jsii_struct_bases=[],
    name_mapping={
        "continue_on_failure": "continueOnFailure",
        "jar_file_uris": "jarFileUris",
        "properties": "properties",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
        "script_variables": "scriptVariables",
    },
)
class DataprocJobHiveConfig:
    def __init__(
        self,
        *,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param continue_on_failure: Whether to continue executing queries if a query fails. The default value is false. Setting to true can be useful when executing independent parallel queries. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATH of the Hive server and Hadoop MapReduce (MR) tasks. Can contain Hive SerDes and UDFs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param properties: A mapping of property names and values, used to configure Hive. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/hive/conf/hive-site.xml, and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param query_file_uri: HCFS URI of file containing Hive script to execute as the job. Conflicts with query_list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        :param query_list: The list of Hive queries or statements to execute as part of the job. Conflicts with query_file_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Hive command: SET name="value";). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9583b29393f33d93ca3c796cdcb7f63ef782fde34624a171b396a72afee7e6af)
            check_type(argname="argument continue_on_failure", value=continue_on_failure, expected_type=type_hints["continue_on_failure"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
            check_type(argname="argument script_variables", value=script_variables, expected_type=type_hints["script_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continue_on_failure is not None:
            self._values["continue_on_failure"] = continue_on_failure
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if properties is not None:
            self._values["properties"] = properties
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list
        if script_variables is not None:
            self._values["script_variables"] = script_variables

    @builtins.property
    def continue_on_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to continue executing queries if a query fails.

        The default value is false. Setting to true can be useful when executing independent parallel queries. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        '''
        result = self._values.get("continue_on_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the CLASSPATH of the Hive server and Hadoop MapReduce (MR) tasks.

        Can contain Hive SerDes and UDFs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names and values, used to configure Hive.

        Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/hive/conf/hive-site.xml, and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''HCFS URI of file containing Hive script to execute as the job. Conflicts with query_list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Hive queries or statements to execute as part of the job. Conflicts with query_file_uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def script_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping of query variable names to values (equivalent to the Hive command: SET name="value";).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        result = self._values.get("script_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobHiveConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobHiveConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobHiveConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eff34b7de837afff1fd45ce77925e7464849db91f330f89f18bd8d7a89d703a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContinueOnFailure")
    def reset_continue_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinueOnFailure", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

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
    @jsii.member(jsii_name="continueOnFailureInput")
    def continue_on_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continueOnFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryListInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptVariablesInput")
    def script_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "scriptVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailure")
    def continue_on_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continueOnFailure"))

    @continue_on_failure.setter
    def continue_on_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8a597e691cc6b5cd5187246806008dce035badd7b847c2f2179d4fd07d1c11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continueOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5322add1f924cc8348a682ca760e5f2a6228e56f4c8004ab94201fefcc5800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a16662e14f06228055cfa8733c7331d95d4db3e2064f7556af0888cf7f33b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf5f98a1c104fc52ef50ec204438cb84da859c61c1280e61e6191f9a801f5a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryList"))

    @query_list.setter
    def query_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f76047419042870fbd8a10a020d460b95969b7d2a199e2f9c7ce96074821144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryList", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__4e34fbd623d66acfd9f10e58f4a60690bb6591a1615b3e1585d22051ce41fa42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobHiveConfig]:
        return typing.cast(typing.Optional[DataprocJobHiveConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobHiveConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce00193da41ad1bbabb61e2010c51ced80fa48752875ed6a8f936940f917eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPigConfig",
    jsii_struct_bases=[],
    name_mapping={
        "continue_on_failure": "continueOnFailure",
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "properties": "properties",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
        "script_variables": "scriptVariables",
    },
)
class DataprocJobPigConfig:
    def __init__(
        self,
        *,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobPigConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param continue_on_failure: Whether to continue executing queries if a query fails. The default value is false. Setting to true can be useful when executing independent parallel queries. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATH of the Pig Client and Hadoop MapReduce (MR) tasks. Can contain Pig UDFs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param properties: A mapping of property names to values, used to configure Pig. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/pig/conf/pig.properties, and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param query_file_uri: HCFS URI of file containing Hive script to execute as the job. Conflicts with query_list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        :param query_list: The list of Hive queries or statements to execute as part of the job. Conflicts with query_file_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Pig command: name=[value]). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocJobPigConfigLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f165b861158dfacabcd85ea3d94e6250990126d3470af1a8c296c58941c4721b)
            check_type(argname="argument continue_on_failure", value=continue_on_failure, expected_type=type_hints["continue_on_failure"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
            check_type(argname="argument script_variables", value=script_variables, expected_type=type_hints["script_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if continue_on_failure is not None:
            self._values["continue_on_failure"] = continue_on_failure
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if properties is not None:
            self._values["properties"] = properties
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list
        if script_variables is not None:
            self._values["script_variables"] = script_variables

    @builtins.property
    def continue_on_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to continue executing queries if a query fails.

        The default value is false. Setting to true can be useful when executing independent parallel queries. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        '''
        result = self._values.get("continue_on_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the CLASSPATH of the Pig Client and Hadoop MapReduce (MR) tasks.

        Can contain Pig UDFs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["DataprocJobPigConfigLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocJobPigConfigLoggingConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values, used to configure Pig.

        Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/hadoop/conf/*-site.xml, /etc/pig/conf/pig.properties, and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''HCFS URI of file containing Hive script to execute as the job. Conflicts with query_list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Hive queries or statements to execute as part of the job. Conflicts with query_file_uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def script_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping of query variable names to values (equivalent to the Pig command: name=[value]).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        result = self._values.get("script_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobPigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPigConfigLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocJobPigConfigLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d24fcf8edf801cbe7c41d2daebea67dd5d87e6d7f0f80a91f8b9ff1142025a)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver_log_levels": driver_log_levels,
        }

    @builtins.property
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Optional.

        The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        assert result is not None, "Required property 'driver_log_levels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobPigConfigLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobPigConfigLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPigConfigLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41b0a12f95380d7da3e062281c22af040abaec13aacc1a130e6ef87dc133eaf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8678c52d87db01610e9278dc6a915284ca82d8a90eb896fbee192769e624f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobPigConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobPigConfigLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocJobPigConfigLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0881d88c35eb0f8bb91cb4ab3e6b85597abb1859f7284e9d6c856c3a854debf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocJobPigConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPigConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4613a5480c3a1f9cd98465c2964909eca957d7ff7fe2ba5f15c81f855568b036)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        value = DataprocJobPigConfigLoggingConfig(driver_log_levels=driver_log_levels)

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetContinueOnFailure")
    def reset_continue_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinueOnFailure", []))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

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
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> DataprocJobPigConfigLoggingConfigOutputReference:
        return typing.cast(DataprocJobPigConfigLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailureInput")
    def continue_on_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continueOnFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocJobPigConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobPigConfigLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryListInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptVariablesInput")
    def script_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "scriptVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailure")
    def continue_on_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continueOnFailure"))

    @continue_on_failure.setter
    def continue_on_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c312008768c81fb57c29330ed50cb75ddd00fa73368c73bada5af6f46b17b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continueOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85264aed103779d4c4d2b5d7c7f0d48a257bae72753e5a99014a00a8d0469d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b1123cafbe57f9d53f7161d97b38aafc270ec49278b70fa3481fe31a3fc036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25887437c7456849edf3f1c58b53f332d75042886ae0f45eaf7cf3ff04788f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryList"))

    @query_list.setter
    def query_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4d98e74ac17b32e4d9093127ed65878655cfe5f9628ccef012bb1d539af34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryList", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__2a8e54efe153b4366f0aa95a16d10a8483f97c7355f1bf6efee7bcaed7322930)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobPigConfig]:
        return typing.cast(typing.Optional[DataprocJobPigConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobPigConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24563c85f92c58e7336e09ee93f48eec9bb8b8fd80f8966d77bfc32941ceff7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPlacement",
    jsii_struct_bases=[],
    name_mapping={"cluster_name": "clusterName"},
)
class DataprocJobPlacement:
    def __init__(self, *, cluster_name: builtins.str) -> None:
        '''
        :param cluster_name: The name of the cluster where the job will be submitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#cluster_name DataprocJob#cluster_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57b84890ad7e85ea2367705b3754cc940d187c27e14b59de0e9de06927a624d)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
        }

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''The name of the cluster where the job will be submitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#cluster_name DataprocJob#cluster_name}
        '''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobPlacement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobPlacementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPlacementOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc481c8b59c4374cf3649a6e0c2402b11ea5073b89c0e5631d8f81deeaa1c7c7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clusterUuid")
    def cluster_uuid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterUuid"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7991527eba01196e73b9d2b25905987b56907b6bcfcd1a4c032e27d37ccca31e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobPlacement]:
        return typing.cast(typing.Optional[DataprocJobPlacement], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobPlacement]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1833d47949728e5e9f34fc2f5794fe72efcb1a55a6ecfd0a7d8d686830756b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPrestoConfig",
    jsii_struct_bases=[],
    name_mapping={
        "client_tags": "clientTags",
        "continue_on_failure": "continueOnFailure",
        "logging_config": "loggingConfig",
        "output_format": "outputFormat",
        "properties": "properties",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
    },
)
class DataprocJobPrestoConfig:
    def __init__(
        self,
        *,
        client_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobPrestoConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        output_format: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_tags: Presto client tags to attach to this query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#client_tags DataprocJob#client_tags}
        :param continue_on_failure: Whether to continue executing queries if a query fails. Setting to true can be useful when executing independent parallel queries. Defaults to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param output_format: The format in which query output will be displayed. See the Presto documentation for supported output formats. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#output_format DataprocJob#output_format}
        :param properties: A mapping of property names to values. Used to set Presto session properties Equivalent to using the --session flag in the Presto CLI. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Conflicts with query_list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        :param query_list: The list of SQL queries or statements to execute as part of the job. Conflicts with query_file_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocJobPrestoConfigLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796aa3e3955d77bbb143c96d77c07f08583f4b6e67a25c402790e16307a3aaba)
            check_type(argname="argument client_tags", value=client_tags, expected_type=type_hints["client_tags"])
            check_type(argname="argument continue_on_failure", value=continue_on_failure, expected_type=type_hints["continue_on_failure"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_tags is not None:
            self._values["client_tags"] = client_tags
        if continue_on_failure is not None:
            self._values["continue_on_failure"] = continue_on_failure
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if output_format is not None:
            self._values["output_format"] = output_format
        if properties is not None:
            self._values["properties"] = properties
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list

    @builtins.property
    def client_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Presto client tags to attach to this query.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#client_tags DataprocJob#client_tags}
        '''
        result = self._values.get("client_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def continue_on_failure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to continue executing queries if a query fails.

        Setting to true can be useful when executing independent parallel queries. Defaults to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#continue_on_failure DataprocJob#continue_on_failure}
        '''
        result = self._values.get("continue_on_failure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["DataprocJobPrestoConfigLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocJobPrestoConfigLoggingConfig"], result)

    @builtins.property
    def output_format(self) -> typing.Optional[builtins.str]:
        '''The format in which query output will be displayed. See the Presto documentation for supported output formats.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#output_format DataprocJob#output_format}
        '''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values.

        Used to set Presto session properties Equivalent to using the --session flag in the Presto CLI.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains SQL queries. Conflicts with query_list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of SQL queries or statements to execute as part of the job. Conflicts with query_file_uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobPrestoConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPrestoConfigLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocJobPrestoConfigLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4515d1cbd724916b4414fb5786290467bde477dd689255342f48526f6d870e)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver_log_levels": driver_log_levels,
        }

    @builtins.property
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Optional.

        The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        assert result is not None, "Required property 'driver_log_levels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobPrestoConfigLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobPrestoConfigLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPrestoConfigLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70a6b1e03a086b7428bba4645ff09cd542aa6f96c67b8d6888c69ce96940c6cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc1101e696feda87ea1a28c2e20ec6acf8778f99574ada0ef05df912af0b05d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobPrestoConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobPrestoConfigLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocJobPrestoConfigLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea643c7363e3dd0636f099b2976be83e78697fedd621d87bff7d3c4184b89042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocJobPrestoConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPrestoConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a374eb5d4f0fff0662bc5b8858393858e2a03279c403c478f1b673887742b9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        value = DataprocJobPrestoConfigLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetClientTags")
    def reset_client_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientTags", []))

    @jsii.member(jsii_name="resetContinueOnFailure")
    def reset_continue_on_failure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinueOnFailure", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetOutputFormat")
    def reset_output_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputFormat", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetQueryFileUri")
    def reset_query_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryFileUri", []))

    @jsii.member(jsii_name="resetQueryList")
    def reset_query_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryList", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> DataprocJobPrestoConfigLoggingConfigOutputReference:
        return typing.cast(DataprocJobPrestoConfigLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="clientTagsInput")
    def client_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clientTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="continueOnFailureInput")
    def continue_on_failure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continueOnFailureInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocJobPrestoConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobPrestoConfigLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFormatInput")
    def output_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryListInput"))

    @builtins.property
    @jsii.member(jsii_name="clientTags")
    def client_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "clientTags"))

    @client_tags.setter
    def client_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec073948dcb157a45f193d36a01da81004e9d5329b231704213cbf12e635cf67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="continueOnFailure")
    def continue_on_failure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continueOnFailure"))

    @continue_on_failure.setter
    def continue_on_failure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eba8761b36d42ec252f9d17e4dadbe6bd6204e1b07fa9f85574b93f81ba7ae77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continueOnFailure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFormat"))

    @output_format.setter
    def output_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81fe987c3fda81683a096b4994e1c71ac1fbbc87ee2cfc81e59bc38e785eb95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFormat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4648dd8ac416f488fc421d52f291cdcd94ff612cef69c3c29c37174437d6fd59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3559c83d3c411a5308c6357be73a4835a4a65c880567afa5c72f67b031fc32e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryList"))

    @query_list.setter
    def query_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe4dd16996b06d4a9c21eebb1ba6ec43baf5b4c47d14efc82b0731201e31f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobPrestoConfig]:
        return typing.cast(typing.Optional[DataprocJobPrestoConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobPrestoConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4411c048bafe3232346e7ea793b6f1f258570e01046e642a1f410bff25c1dfec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPysparkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "main_python_file_uri": "mainPythonFileUri",
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "properties": "properties",
        "python_file_uris": "pythonFileUris",
    },
)
class DataprocJobPysparkConfig:
    def __init__(
        self,
        *,
        main_python_file_uri: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobPysparkConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param main_python_file_uri: Required. The HCFS URI of the main Python file to use as the driver. Must be a .py file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_python_file_uri DataprocJob#main_python_file_uri}
        :param archive_uris: Optional. HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        :param args: Optional. The arguments to pass to the driver. Do not include arguments, such as --conf, that can be set as job properties, since a collision may occur that causes an incorrect job submission Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        :param file_uris: Optional. HCFS URIs of files to be copied to the working directory of Python drivers and distributed tasks. Useful for naively parallel tasks Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        :param jar_file_uris: Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param properties: Optional. A mapping of property names to values, used to configure PySpark. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param python_file_uris: Optional. HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#python_file_uris DataprocJob#python_file_uris}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocJobPysparkConfigLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de350134d0342f811823e4a102abf189d81b62d5f0d19fe92e1fb21fe48a9da)
            check_type(argname="argument main_python_file_uri", value=main_python_file_uri, expected_type=type_hints["main_python_file_uri"])
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
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
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if properties is not None:
            self._values["properties"] = properties
        if python_file_uris is not None:
            self._values["python_file_uris"] = python_file_uris

    @builtins.property
    def main_python_file_uri(self) -> builtins.str:
        '''Required. The HCFS URI of the main Python file to use as the driver. Must be a .py file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_python_file_uri DataprocJob#main_python_file_uri}
        '''
        result = self._values.get("main_python_file_uri")
        assert result is not None, "Required property 'main_python_file_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        The arguments to pass to the driver. Do not include arguments, such as --conf, that can be set as job properties, since a collision may occur that causes an incorrect job submission

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS URIs of files to be copied to the working directory of Python drivers and distributed tasks. Useful for naively parallel tasks

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. HCFS URIs of jar files to add to the CLASSPATHs of the Python driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocJobPysparkConfigLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocJobPysparkConfigLoggingConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional.

        A mapping of property names to values, used to configure PySpark. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def python_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional.

        HCFS file URIs of Python files to pass to the PySpark framework. Supported file types: .py, .egg, and .zip

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#python_file_uris DataprocJob#python_file_uris}
        '''
        result = self._values.get("python_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobPysparkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPysparkConfigLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocJobPysparkConfigLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b01824ca4afc06953850248bceb26e5fb833102a749ab849131eb15b9013de1)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver_log_levels": driver_log_levels,
        }

    @builtins.property
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Optional.

        The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        assert result is not None, "Required property 'driver_log_levels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobPysparkConfigLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobPysparkConfigLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPysparkConfigLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd1c068dc9a1c4398cf23a4a596132505f060e9fe46115cafee38ce704ec72ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275c1f680ddb19cedcb3aea3a08885c12cb1547f7671d2375fa9223e342ab185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobPysparkConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobPysparkConfigLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocJobPysparkConfigLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f893eccd590f370f3f9e8db030ac26b41d631d9da141ef7acb3c158cf91e97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocJobPysparkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobPysparkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d863ebdde2320bde37eb422581b599839a270dee7eab875fa680534f5ce40c19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        value = DataprocJobPysparkConfigLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

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

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetPythonFileUris")
    def reset_python_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonFileUris", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> DataprocJobPysparkConfigLoggingConfigOutputReference:
        return typing.cast(DataprocJobPysparkConfigLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

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
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocJobPysparkConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobPysparkConfigLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUriInput")
    def main_python_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainPythonFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fd527b64d981352076255e010d6865261b1e4173c9e45d7e43351ddacf259fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42290320b09bfcf4f909a428e708a4a586a4941a28a1dc8cc16d3472ceab8fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf3c4da1d36c821ac64d8bdc50bdeea24cfe91bd7fa592e61ccd21fe031eaba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26bc96ce78dd080e0633296d10f7b702df5f3152e94522ee152716fa860fff32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainPythonFileUri")
    def main_python_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainPythonFileUri"))

    @main_python_file_uri.setter
    def main_python_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd49ddde70a8943a5fe89ec6553d98228e0fe6dbeb114cdcb94f5cd30db6399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainPythonFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d0a0934d481813cf3accf0304a6d2158fdcb6db7d33be89804418b373f907a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonFileUris")
    def python_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonFileUris"))

    @python_file_uris.setter
    def python_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d352cda352f14ad9b67e41329cdc6c001fc5c57c193ccd5312df207bc5fe43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobPysparkConfig]:
        return typing.cast(typing.Optional[DataprocJobPysparkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobPysparkConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa21961b62d07d00527ef251de930f5576034ae82a50d5d4602a318ef06410aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobReference",
    jsii_struct_bases=[],
    name_mapping={"job_id": "jobId"},
)
class DataprocJobReference:
    def __init__(self, *, job_id: typing.Optional[builtins.str] = None) -> None:
        '''
        :param job_id: The job ID, which must be unique within the project. The job ID is generated by the server upon job submission or provided by the user as a means to perform retries without creating duplicate jobs Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#job_id DataprocJob#job_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76814f527f2ad40a848682d00358b7a88501033404b2db1923a36b39ace2bf0d)
            check_type(argname="argument job_id", value=job_id, expected_type=type_hints["job_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_id is not None:
            self._values["job_id"] = job_id

    @builtins.property
    def job_id(self) -> typing.Optional[builtins.str]:
        '''The job ID, which must be unique within the project.

        The job ID is generated by the server upon job submission or provided by the user as a means to perform retries without creating duplicate jobs

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#job_id DataprocJob#job_id}
        '''
        result = self._values.get("job_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__615a638ac2bffb3edb4352651fae7b1aedc0471f2b60ade3ba062cc1931fdb2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetJobId")
    def reset_job_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJobId", []))

    @builtins.property
    @jsii.member(jsii_name="jobIdInput")
    def job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="jobId")
    def job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jobId"))

    @job_id.setter
    def job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8d1998d4d7ea08a4b48a9c1f9554cbc0924fb377880dbe8ade264024d3594c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobReference]:
        return typing.cast(typing.Optional[DataprocJobReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobReference]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b90fa64f43c2141773b7b8e26d4a1b9cab19d1eb52a0a36b54e48ea18e6eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobScheduling",
    jsii_struct_bases=[],
    name_mapping={
        "max_failures_per_hour": "maxFailuresPerHour",
        "max_failures_total": "maxFailuresTotal",
    },
)
class DataprocJobScheduling:
    def __init__(
        self,
        *,
        max_failures_per_hour: jsii.Number,
        max_failures_total: jsii.Number,
    ) -> None:
        '''
        :param max_failures_per_hour: Maximum number of times per hour a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#max_failures_per_hour DataprocJob#max_failures_per_hour}
        :param max_failures_total: Maximum number of times in total a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#max_failures_total DataprocJob#max_failures_total}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38597e6ec2c7244a2d4abd9cf7e8852dd60c8cbef291fef2e598a29fbe0bba01)
            check_type(argname="argument max_failures_per_hour", value=max_failures_per_hour, expected_type=type_hints["max_failures_per_hour"])
            check_type(argname="argument max_failures_total", value=max_failures_total, expected_type=type_hints["max_failures_total"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_failures_per_hour": max_failures_per_hour,
            "max_failures_total": max_failures_total,
        }

    @builtins.property
    def max_failures_per_hour(self) -> jsii.Number:
        '''Maximum number of times per hour a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#max_failures_per_hour DataprocJob#max_failures_per_hour}
        '''
        result = self._values.get("max_failures_per_hour")
        assert result is not None, "Required property 'max_failures_per_hour' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_failures_total(self) -> jsii.Number:
        '''Maximum number of times in total a driver may be restarted as a result of driver exiting with non-zero code before job is reported failed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#max_failures_total DataprocJob#max_failures_total}
        '''
        result = self._values.get("max_failures_total")
        assert result is not None, "Required property 'max_failures_total' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobScheduling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobSchedulingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSchedulingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10ab9c739a7d50bc6a0b5f2c313807685f602612b337cb7686ff5324102bc545)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="maxFailuresPerHourInput")
    def max_failures_per_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFailuresPerHourInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFailuresTotalInput")
    def max_failures_total_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxFailuresTotalInput"))

    @builtins.property
    @jsii.member(jsii_name="maxFailuresPerHour")
    def max_failures_per_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFailuresPerHour"))

    @max_failures_per_hour.setter
    def max_failures_per_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64ce4ca62c7e500210159f49bd79c24575584ace26a27f33c0b666132c74ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFailuresPerHour", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxFailuresTotal")
    def max_failures_total(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxFailuresTotal"))

    @max_failures_total.setter
    def max_failures_total(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20966de2930bfa40b6cbd2f5174bc61bebe8331e1baea62932b27716c70168cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxFailuresTotal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobScheduling]:
        return typing.cast(typing.Optional[DataprocJobScheduling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobScheduling]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd61d59d3499ad904745eb6082145289a1f7e4e3ad972dcc741404ef19fb1921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSparkConfig",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "args": "args",
        "file_uris": "fileUris",
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "main_class": "mainClass",
        "main_jar_file_uri": "mainJarFileUri",
        "properties": "properties",
    },
)
class DataprocJobSparkConfig:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobSparkConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param archive_uris: HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        :param args: The arguments to pass to the driver. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        :param file_uris: HCFS URIs of files to be copied to the working directory of Spark drivers and distributed tasks. Useful for naively parallel tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        :param jar_file_uris: HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param main_class: The class containing the main method of the driver. Must be in a provided jar or jar that is already on the classpath. Conflicts with main_jar_file_uri Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_class DataprocJob#main_class}
        :param main_jar_file_uri: The HCFS URI of jar file containing the driver jar. Conflicts with main_class. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_jar_file_uri DataprocJob#main_jar_file_uri}
        :param properties: A mapping of property names to values, used to configure Spark. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocJobSparkConfigLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecaeac2e477cd31d665bf45669c7a28676f9147807e5617e4eeb0af5f2fce8df)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
            check_type(argname="argument main_jar_file_uri", value=main_jar_file_uri, expected_type=type_hints["main_jar_file_uri"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if args is not None:
            self._values["args"] = args
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if main_class is not None:
            self._values["main_class"] = main_class
        if main_jar_file_uri is not None:
            self._values["main_jar_file_uri"] = main_jar_file_uri
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of archives to be extracted in the working directory of .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#archive_uris DataprocJob#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The arguments to pass to the driver.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#args DataprocJob#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of files to be copied to the working directory of Spark drivers and distributed tasks.

        Useful for naively parallel tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#file_uris DataprocJob#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to add to the CLASSPATHs of the Spark driver and tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(self) -> typing.Optional["DataprocJobSparkConfigLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocJobSparkConfigLoggingConfig"], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The class containing the main method of the driver.

        Must be in a provided jar or jar that is already on the classpath. Conflicts with main_jar_file_uri

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_class DataprocJob#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of jar file containing the driver jar. Conflicts with main_class.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#main_jar_file_uri DataprocJob#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values, used to configure Spark.

        Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Can include properties set in /etc/spark/conf/spark-defaults.conf and classes in user code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobSparkConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSparkConfigLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocJobSparkConfigLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63868bfc2a14eed75d930850d55585fc2776c2c0f8bca946443abf63a183f89)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver_log_levels": driver_log_levels,
        }

    @builtins.property
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Optional.

        The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        assert result is not None, "Required property 'driver_log_levels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobSparkConfigLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobSparkConfigLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSparkConfigLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81c94fcd3099405897a572c2638be99ba58d8cdeb61835c2589adf0f8214cdd9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75ff5cf1b287d7ba347ad007d8e9c465d3140cd66b1eeeae819740d5c3082f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobSparkConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobSparkConfigLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocJobSparkConfigLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6eda3fd79e95dbf444f638a03e5e6563af49b1bb270a4c1b072631adfe3543e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocJobSparkConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSparkConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c18a9f4cb719a8ecc50775ab7de72b66ce0ea184b9dd148bdfe8d983628d0ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        value = DataprocJobSparkConfigLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

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

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetMainClass")
    def reset_main_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainClass", []))

    @jsii.member(jsii_name="resetMainJarFileUri")
    def reset_main_jar_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainJarFileUri", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> DataprocJobSparkConfigLoggingConfigOutputReference:
        return typing.cast(DataprocJobSparkConfigLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

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
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocJobSparkConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobSparkConfigLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="mainClassInput")
    def main_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainClassInput"))

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUriInput")
    def main_jar_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainJarFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e093b6f740d529f7f53e23c38c5f371b6faaf9da3b4732e6088394ae10e6d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c86792f68d51dec11bcc0b3c50c6ebde7595b1bb267ca3b1afcc9e4a56fb18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11c2678b47a8dc0a305002d95bd72337dc912ab53bd1033ae8997e329648a322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jarFileUris")
    def jar_file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jarFileUris"))

    @jar_file_uris.setter
    def jar_file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49eb89431482ec4ef3e92aaf54b85b24e1a5ab63efda3d9840224520fbf4ed90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba4d868d722b4133d430ea096f07421311dc9b145d808c1c395a39530919c91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f272c2723974344a5cad7848b84f6350e6cef25efe40a4d1fac6f0f9abc951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e252d977be1e1101d9fdad5034494368390fbfdf219eba3024ea33592ebb469d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobSparkConfig]:
        return typing.cast(typing.Optional[DataprocJobSparkConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobSparkConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dd4ab0e6b0bba42b4583d5788b3915e4ba1ef24031608cb1c1a0d0149a17fa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSparksqlConfig",
    jsii_struct_bases=[],
    name_mapping={
        "jar_file_uris": "jarFileUris",
        "logging_config": "loggingConfig",
        "properties": "properties",
        "query_file_uri": "queryFileUri",
        "query_list": "queryList",
        "script_variables": "scriptVariables",
    },
)
class DataprocJobSparksqlConfig:
    def __init__(
        self,
        *,
        jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_config: typing.Optional[typing.Union["DataprocJobSparksqlConfigLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        query_file_uri: typing.Optional[builtins.str] = None,
        query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param jar_file_uris: HCFS URIs of jar files to be added to the Spark CLASSPATH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        :param logging_config: logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        :param properties: A mapping of property names to values, used to configure Spark SQL's SparkConf. Properties that conflict with values set by the Cloud Dataproc API may be overwritten. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        :param query_file_uri: The HCFS URI of the script that contains SQL queries. Conflicts with query_list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        :param query_list: The list of SQL queries or statements to execute as part of the job. Conflicts with query_file_uri. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        :param script_variables: Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        if isinstance(logging_config, dict):
            logging_config = DataprocJobSparksqlConfigLoggingConfig(**logging_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2891a8180a93ba673a8c51130f3773884473ebeff7777f1b742debdb44fef39c)
            check_type(argname="argument jar_file_uris", value=jar_file_uris, expected_type=type_hints["jar_file_uris"])
            check_type(argname="argument logging_config", value=logging_config, expected_type=type_hints["logging_config"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument query_file_uri", value=query_file_uri, expected_type=type_hints["query_file_uri"])
            check_type(argname="argument query_list", value=query_list, expected_type=type_hints["query_list"])
            check_type(argname="argument script_variables", value=script_variables, expected_type=type_hints["script_variables"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jar_file_uris is not None:
            self._values["jar_file_uris"] = jar_file_uris
        if logging_config is not None:
            self._values["logging_config"] = logging_config
        if properties is not None:
            self._values["properties"] = properties
        if query_file_uri is not None:
            self._values["query_file_uri"] = query_file_uri
        if query_list is not None:
            self._values["query_list"] = query_list
        if script_variables is not None:
            self._values["script_variables"] = script_variables

    @builtins.property
    def jar_file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''HCFS URIs of jar files to be added to the Spark CLASSPATH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#jar_file_uris DataprocJob#jar_file_uris}
        '''
        result = self._values.get("jar_file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_config(
        self,
    ) -> typing.Optional["DataprocJobSparksqlConfigLoggingConfig"]:
        '''logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#logging_config DataprocJob#logging_config}
        '''
        result = self._values.get("logging_config")
        return typing.cast(typing.Optional["DataprocJobSparksqlConfigLoggingConfig"], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A mapping of property names to values, used to configure Spark SQL's SparkConf.

        Properties that conflict with values set by the Cloud Dataproc API may be overwritten.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#properties DataprocJob#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def query_file_uri(self) -> typing.Optional[builtins.str]:
        '''The HCFS URI of the script that contains SQL queries. Conflicts with query_list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_file_uri DataprocJob#query_file_uri}
        '''
        result = self._values.get("query_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of SQL queries or statements to execute as part of the job. Conflicts with query_file_uri.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#query_list DataprocJob#query_list}
        '''
        result = self._values.get("query_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def script_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping of query variable names to values (equivalent to the Spark SQL command: SET name="value";).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#script_variables DataprocJob#script_variables}
        '''
        result = self._values.get("script_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobSparksqlConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSparksqlConfigLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={"driver_log_levels": "driverLogLevels"},
)
class DataprocJobSparksqlConfigLoggingConfig:
    def __init__(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b8fa0e7d2fd831bf31df1f767f5fd5c8399af8655f4e02c759f6ab1659a736)
            check_type(argname="argument driver_log_levels", value=driver_log_levels, expected_type=type_hints["driver_log_levels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "driver_log_levels": driver_log_levels,
        }

    @builtins.property
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Optional.

        The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        result = self._values.get("driver_log_levels")
        assert result is not None, "Required property 'driver_log_levels' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobSparksqlConfigLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobSparksqlConfigLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSparksqlConfigLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7ba6e615844b0379270ef2cf63e2ee5b70e58a26966bea693755212a4cf7c65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="driverLogLevelsInput")
    def driver_log_levels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "driverLogLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="driverLogLevels")
    def driver_log_levels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "driverLogLevels"))

    @driver_log_levels.setter
    def driver_log_levels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__210b2b0e6d6f9c1476ee4b0b229765566b1ee7920a80c7663914d65ac528baee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "driverLogLevels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobSparksqlConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobSparksqlConfigLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataprocJobSparksqlConfigLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253fae1cb50b07b43214fabe2ad24c0938bd59fdd0029e84fabf021fbedabc37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataprocJobSparksqlConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobSparksqlConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6fd5635031cf66199debe22441c033c9bc2ab83f39afab81318da25b435ac3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLoggingConfig")
    def put_logging_config(
        self,
        *,
        driver_log_levels: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param driver_log_levels: Optional. The per-package log levels for the driver. This may include 'root' package name to configure rootLogger. Examples: 'com.google = FATAL', 'root = INFO', 'org.apache = DEBUG'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#driver_log_levels DataprocJob#driver_log_levels}
        '''
        value = DataprocJobSparksqlConfigLoggingConfig(
            driver_log_levels=driver_log_levels
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingConfig", [value]))

    @jsii.member(jsii_name="resetJarFileUris")
    def reset_jar_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJarFileUris", []))

    @jsii.member(jsii_name="resetLoggingConfig")
    def reset_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingConfig", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

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
    @jsii.member(jsii_name="loggingConfig")
    def logging_config(self) -> DataprocJobSparksqlConfigLoggingConfigOutputReference:
        return typing.cast(DataprocJobSparksqlConfigLoggingConfigOutputReference, jsii.get(self, "loggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="jarFileUrisInput")
    def jar_file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jarFileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigInput")
    def logging_config_input(
        self,
    ) -> typing.Optional[DataprocJobSparksqlConfigLoggingConfig]:
        return typing.cast(typing.Optional[DataprocJobSparksqlConfigLoggingConfig], jsii.get(self, "loggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="queryFileUriInput")
    def query_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="queryListInput")
    def query_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "queryListInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__78a18288654a2478a3cdfa628ce083cc15c6bb7b40f6906da4c6bbe5f59be5a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jarFileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__605819ac3bccaef7c5b0380b3a97aabc2c2c18ce9110f7d622dfd720af9c8291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryFileUri")
    def query_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryFileUri"))

    @query_file_uri.setter
    def query_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71015542a396e106b8935caa280ed8d97b7c5bf3ee88e89ceef102338e75d788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryList")
    def query_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "queryList"))

    @query_list.setter
    def query_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a10e096771af2063b1648fb618bb5f46a1455366723b616efc57b5caad137e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryList", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__312c6a9f91a1918159b03efda5f209ac02af2fe0376ad791dd657fe28a3bb3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobSparksqlConfig]:
        return typing.cast(typing.Optional[DataprocJobSparksqlConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobSparksqlConfig]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02b37a78d5d205de646dfff1d00769020cb342506a14b894c95cb710c994adc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataprocJobStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a62107d61ca4c9ab233d8e5fec9becac2aed4df1248705d4b66646191c827793)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataprocJobStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a71e14ed17f6f0137107eb8716b756722b21838699a89dc5879de34bd00ebbea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataprocJobStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c106f88b3a6915bfebd69d235e2ebf86a0a08182353e2eab69c200646fad6fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7abe926fa2d4955a74e194c3e5d194d796f7be503afb5e68f9236346b739cc7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21eb3d2a4a514a7378dee5d0998748cade9680a18ede09d7ca11f0ab7dd1cb2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataprocJobStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__609b3107514398844c02b5e91d10557e7cf43a461d8f72ee11829b690865538d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="stateStartTime")
    def state_start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateStartTime"))

    @builtins.property
    @jsii.member(jsii_name="substate")
    def substate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "substate"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataprocJobStatus]:
        return typing.cast(typing.Optional[DataprocJobStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataprocJobStatus]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3bfd66c7adbacb984ed56bee637c7475b49d9ec8f19961cf3b4de3ec456fe8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class DataprocJobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#create DataprocJob#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#delete DataprocJob#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeb1837ad48d05e8f2c21732551874f2e607233fdf6c6f2ab0d6619ada9dd349)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#create DataprocJob#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataproc_job#delete DataprocJob#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataprocJobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataprocJobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataprocJob.DataprocJobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__038ff7fec69319e05853a97a7f9f9b44a4a729bc92895279a98eb13c0bb0ddbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83106728b64feeacc799f440e00c46ae4f6943fa4b1487cb6d9a3f753193a9d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51050d612666c2559cf70bd8483324c7669117d755c69b3a168f2be6e71d4afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocJobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocJobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocJobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b6b3034bdd5582293bbad7c30f4ff14175b8723b098b539f704869781b6db91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataprocJob",
    "DataprocJobConfig",
    "DataprocJobHadoopConfig",
    "DataprocJobHadoopConfigLoggingConfig",
    "DataprocJobHadoopConfigLoggingConfigOutputReference",
    "DataprocJobHadoopConfigOutputReference",
    "DataprocJobHiveConfig",
    "DataprocJobHiveConfigOutputReference",
    "DataprocJobPigConfig",
    "DataprocJobPigConfigLoggingConfig",
    "DataprocJobPigConfigLoggingConfigOutputReference",
    "DataprocJobPigConfigOutputReference",
    "DataprocJobPlacement",
    "DataprocJobPlacementOutputReference",
    "DataprocJobPrestoConfig",
    "DataprocJobPrestoConfigLoggingConfig",
    "DataprocJobPrestoConfigLoggingConfigOutputReference",
    "DataprocJobPrestoConfigOutputReference",
    "DataprocJobPysparkConfig",
    "DataprocJobPysparkConfigLoggingConfig",
    "DataprocJobPysparkConfigLoggingConfigOutputReference",
    "DataprocJobPysparkConfigOutputReference",
    "DataprocJobReference",
    "DataprocJobReferenceOutputReference",
    "DataprocJobScheduling",
    "DataprocJobSchedulingOutputReference",
    "DataprocJobSparkConfig",
    "DataprocJobSparkConfigLoggingConfig",
    "DataprocJobSparkConfigLoggingConfigOutputReference",
    "DataprocJobSparkConfigOutputReference",
    "DataprocJobSparksqlConfig",
    "DataprocJobSparksqlConfigLoggingConfig",
    "DataprocJobSparksqlConfigLoggingConfigOutputReference",
    "DataprocJobSparksqlConfigOutputReference",
    "DataprocJobStatus",
    "DataprocJobStatusList",
    "DataprocJobStatusOutputReference",
    "DataprocJobTimeouts",
    "DataprocJobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0d359f5e467197af5eb08fd9c707e56d1d2cfc77714b7dac2551c01517f1e0f0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    placement: typing.Union[DataprocJobPlacement, typing.Dict[builtins.str, typing.Any]],
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hadoop_config: typing.Optional[typing.Union[DataprocJobHadoopConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_config: typing.Optional[typing.Union[DataprocJobHiveConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    pig_config: typing.Optional[typing.Union[DataprocJobPigConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    presto_config: typing.Optional[typing.Union[DataprocJobPrestoConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    pyspark_config: typing.Optional[typing.Union[DataprocJobPysparkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    reference: typing.Optional[typing.Union[DataprocJobReference, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    scheduling: typing.Optional[typing.Union[DataprocJobScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_config: typing.Optional[typing.Union[DataprocJobSparkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sparksql_config: typing.Optional[typing.Union[DataprocJobSparksqlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6e035dc6bb712520ac3867eb904948a6a31e52a0245cf44e00d9251a7f4e0cae(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea356f34e4434378fdd1352620965feaf770e9190f54fe49ec71650b906a5ecc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c90ecf842186c821de90ec65f564591377c212d4f268c5d40c641ef6bcf6b562(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5fd53089eee46c1e9295231b3afcb173d91c0753539e1e137974147e30dd2d5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c86ca0274edb24688ca5062b59c7bf80f8db521fc391c20b9a71953a212665(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77ff4f1cbd21d2be5c3b84d845c001c5268b170b34b42da4282e11df0d3e4bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0578fea2b9fbad8b752ce63c843454f0cfbe081370de05b6c386c48f5d85d7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    placement: typing.Union[DataprocJobPlacement, typing.Dict[builtins.str, typing.Any]],
    force_delete: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hadoop_config: typing.Optional[typing.Union[DataprocJobHadoopConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    hive_config: typing.Optional[typing.Union[DataprocJobHiveConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    pig_config: typing.Optional[typing.Union[DataprocJobPigConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    presto_config: typing.Optional[typing.Union[DataprocJobPrestoConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    pyspark_config: typing.Optional[typing.Union[DataprocJobPysparkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    reference: typing.Optional[typing.Union[DataprocJobReference, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
    scheduling: typing.Optional[typing.Union[DataprocJobScheduling, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_config: typing.Optional[typing.Union[DataprocJobSparkConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sparksql_config: typing.Optional[typing.Union[DataprocJobSparksqlConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DataprocJobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de0216a673887532a18b5d83977f967cd5d11f3144ff56d79dd37d5580c36a8(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocJobHadoopConfigLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    main_class: typing.Optional[builtins.str] = None,
    main_jar_file_uri: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0840482f38d08cf13dfdf64569e6c8dd696e9a3ecfcc9fd28b38631c8546d929(
    *,
    driver_log_levels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb1043e5c58121b41e4d95bbca5db5661659208970d119e08f4974482f75191(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5863e2221e4c9728b1655e2de33b891ff529e13fe1f5cbae75c2011a5121e1fd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c71916f1e778448b08fd51e2457a30337ddc9381101f8b719976212ce24d1830(
    value: typing.Optional[DataprocJobHadoopConfigLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__893cc1916365a69c96c98c53d824d30826d827c43638f3a2f459f88697d6ed7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcad4308dad4d9ab45bc148b86896a3816961275d805e1f58ad30e46802cce50(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8ff95d538ddaf868541b66a5f629bc3baafee03cc6cf58aa262a30024f7ca5e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566ac81283174bc60284512f0e9935679d72b4af53f5bc373318ac31d78c1827(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fb57c0d58163c48f889285ef5900b024a83935b403bb7db6abcd572fa7ba1b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3739b51f2ab2308e807ec53a28e733d444735c95ef966fa9e70007a551bcfa18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fffa2299af0e9d7ddc3be13d862478a3d61a852e7c78ab5b4d960d8b0922b0fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e5f802e5f73f4cc4917b1ec7defe6b18736ff5d900168d8fa6fe64a3411b93(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be94e0841a2ed1ad9b7679af4a66ed1782f126437ca816341e7dab199d535dd4(
    value: typing.Optional[DataprocJobHadoopConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9583b29393f33d93ca3c796cdcb7f63ef782fde34624a171b396a72afee7e6af(
    *,
    continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff34b7de837afff1fd45ce77925e7464849db91f330f89f18bd8d7a89d703a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8a597e691cc6b5cd5187246806008dce035badd7b847c2f2179d4fd07d1c11(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5322add1f924cc8348a682ca760e5f2a6228e56f4c8004ab94201fefcc5800(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a16662e14f06228055cfa8733c7331d95d4db3e2064f7556af0888cf7f33b6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf5f98a1c104fc52ef50ec204438cb84da859c61c1280e61e6191f9a801f5a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f76047419042870fbd8a10a020d460b95969b7d2a199e2f9c7ce96074821144(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e34fbd623d66acfd9f10e58f4a60690bb6591a1615b3e1585d22051ce41fa42(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce00193da41ad1bbabb61e2010c51ced80fa48752875ed6a8f936940f917eb5(
    value: typing.Optional[DataprocJobHiveConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f165b861158dfacabcd85ea3d94e6250990126d3470af1a8c296c58941c4721b(
    *,
    continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocJobPigConfigLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d24fcf8edf801cbe7c41d2daebea67dd5d87e6d7f0f80a91f8b9ff1142025a(
    *,
    driver_log_levels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b0a12f95380d7da3e062281c22af040abaec13aacc1a130e6ef87dc133eaf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8678c52d87db01610e9278dc6a915284ca82d8a90eb896fbee192769e624f14(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0881d88c35eb0f8bb91cb4ab3e6b85597abb1859f7284e9d6c856c3a854debf0(
    value: typing.Optional[DataprocJobPigConfigLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4613a5480c3a1f9cd98465c2964909eca957d7ff7fe2ba5f15c81f855568b036(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c312008768c81fb57c29330ed50cb75ddd00fa73368c73bada5af6f46b17b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85264aed103779d4c4d2b5d7c7f0d48a257bae72753e5a99014a00a8d0469d51(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b1123cafbe57f9d53f7161d97b38aafc270ec49278b70fa3481fe31a3fc036(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25887437c7456849edf3f1c58b53f332d75042886ae0f45eaf7cf3ff04788f24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4d98e74ac17b32e4d9093127ed65878655cfe5f9628ccef012bb1d539af34e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8e54efe153b4366f0aa95a16d10a8483f97c7355f1bf6efee7bcaed7322930(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24563c85f92c58e7336e09ee93f48eec9bb8b8fd80f8966d77bfc32941ceff7f(
    value: typing.Optional[DataprocJobPigConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57b84890ad7e85ea2367705b3754cc940d187c27e14b59de0e9de06927a624d(
    *,
    cluster_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc481c8b59c4374cf3649a6e0c2402b11ea5073b89c0e5631d8f81deeaa1c7c7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7991527eba01196e73b9d2b25905987b56907b6bcfcd1a4c032e27d37ccca31e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1833d47949728e5e9f34fc2f5794fe72efcb1a55a6ecfd0a7d8d686830756b3(
    value: typing.Optional[DataprocJobPlacement],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796aa3e3955d77bbb143c96d77c07f08583f4b6e67a25c402790e16307a3aaba(
    *,
    client_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    continue_on_failure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    logging_config: typing.Optional[typing.Union[DataprocJobPrestoConfigLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    output_format: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4515d1cbd724916b4414fb5786290467bde477dd689255342f48526f6d870e(
    *,
    driver_log_levels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a6b1e03a086b7428bba4645ff09cd542aa6f96c67b8d6888c69ce96940c6cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc1101e696feda87ea1a28c2e20ec6acf8778f99574ada0ef05df912af0b05d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea643c7363e3dd0636f099b2976be83e78697fedd621d87bff7d3c4184b89042(
    value: typing.Optional[DataprocJobPrestoConfigLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a374eb5d4f0fff0662bc5b8858393858e2a03279c403c478f1b673887742b9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec073948dcb157a45f193d36a01da81004e9d5329b231704213cbf12e635cf67(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba8761b36d42ec252f9d17e4dadbe6bd6204e1b07fa9f85574b93f81ba7ae77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81fe987c3fda81683a096b4994e1c71ac1fbbc87ee2cfc81e59bc38e785eb95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4648dd8ac416f488fc421d52f291cdcd94ff612cef69c3c29c37174437d6fd59(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3559c83d3c411a5308c6357be73a4835a4a65c880567afa5c72f67b031fc32e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe4dd16996b06d4a9c21eebb1ba6ec43baf5b4c47d14efc82b0731201e31f53(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4411c048bafe3232346e7ea793b6f1f258570e01046e642a1f410bff25c1dfec(
    value: typing.Optional[DataprocJobPrestoConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de350134d0342f811823e4a102abf189d81b62d5f0d19fe92e1fb21fe48a9da(
    *,
    main_python_file_uri: builtins.str,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocJobPysparkConfigLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    python_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b01824ca4afc06953850248bceb26e5fb833102a749ab849131eb15b9013de1(
    *,
    driver_log_levels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1c068dc9a1c4398cf23a4a596132505f060e9fe46115cafee38ce704ec72ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275c1f680ddb19cedcb3aea3a08885c12cb1547f7671d2375fa9223e342ab185(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f893eccd590f370f3f9e8db030ac26b41d631d9da141ef7acb3c158cf91e97(
    value: typing.Optional[DataprocJobPysparkConfigLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d863ebdde2320bde37eb422581b599839a270dee7eab875fa680534f5ce40c19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd527b64d981352076255e010d6865261b1e4173c9e45d7e43351ddacf259fd0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42290320b09bfcf4f909a428e708a4a586a4941a28a1dc8cc16d3472ceab8fc4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf3c4da1d36c821ac64d8bdc50bdeea24cfe91bd7fa592e61ccd21fe031eaba(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26bc96ce78dd080e0633296d10f7b702df5f3152e94522ee152716fa860fff32(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd49ddde70a8943a5fe89ec6553d98228e0fe6dbeb114cdcb94f5cd30db6399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d0a0934d481813cf3accf0304a6d2158fdcb6db7d33be89804418b373f907a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d352cda352f14ad9b67e41329cdc6c001fc5c57c193ccd5312df207bc5fe43(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa21961b62d07d00527ef251de930f5576034ae82a50d5d4602a318ef06410aa(
    value: typing.Optional[DataprocJobPysparkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76814f527f2ad40a848682d00358b7a88501033404b2db1923a36b39ace2bf0d(
    *,
    job_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__615a638ac2bffb3edb4352651fae7b1aedc0471f2b60ade3ba062cc1931fdb2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8d1998d4d7ea08a4b48a9c1f9554cbc0924fb377880dbe8ade264024d3594c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b90fa64f43c2141773b7b8e26d4a1b9cab19d1eb52a0a36b54e48ea18e6eb5(
    value: typing.Optional[DataprocJobReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38597e6ec2c7244a2d4abd9cf7e8852dd60c8cbef291fef2e598a29fbe0bba01(
    *,
    max_failures_per_hour: jsii.Number,
    max_failures_total: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ab9c739a7d50bc6a0b5f2c313807685f602612b337cb7686ff5324102bc545(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64ce4ca62c7e500210159f49bd79c24575584ace26a27f33c0b666132c74ed4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20966de2930bfa40b6cbd2f5174bc61bebe8331e1baea62932b27716c70168cf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd61d59d3499ad904745eb6082145289a1f7e4e3ad972dcc741404ef19fb1921(
    value: typing.Optional[DataprocJobScheduling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecaeac2e477cd31d665bf45669c7a28676f9147807e5617e4eeb0af5f2fce8df(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocJobSparkConfigLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    main_class: typing.Optional[builtins.str] = None,
    main_jar_file_uri: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63868bfc2a14eed75d930850d55585fc2776c2c0f8bca946443abf63a183f89(
    *,
    driver_log_levels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c94fcd3099405897a572c2638be99ba58d8cdeb61835c2589adf0f8214cdd9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75ff5cf1b287d7ba347ad007d8e9c465d3140cd66b1eeeae819740d5c3082f9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6eda3fd79e95dbf444f638a03e5e6563af49b1bb270a4c1b072631adfe3543e(
    value: typing.Optional[DataprocJobSparkConfigLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c18a9f4cb719a8ecc50775ab7de72b66ce0ea184b9dd148bdfe8d983628d0ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e093b6f740d529f7f53e23c38c5f371b6faaf9da3b4732e6088394ae10e6d3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c86792f68d51dec11bcc0b3c50c6ebde7595b1bb267ca3b1afcc9e4a56fb18(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c2678b47a8dc0a305002d95bd72337dc912ab53bd1033ae8997e329648a322(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49eb89431482ec4ef3e92aaf54b85b24e1a5ab63efda3d9840224520fbf4ed90(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba4d868d722b4133d430ea096f07421311dc9b145d808c1c395a39530919c91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f272c2723974344a5cad7848b84f6350e6cef25efe40a4d1fac6f0f9abc951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e252d977be1e1101d9fdad5034494368390fbfdf219eba3024ea33592ebb469d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dd4ab0e6b0bba42b4583d5788b3915e4ba1ef24031608cb1c1a0d0149a17fa1(
    value: typing.Optional[DataprocJobSparkConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2891a8180a93ba673a8c51130f3773884473ebeff7777f1b742debdb44fef39c(
    *,
    jar_file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_config: typing.Optional[typing.Union[DataprocJobSparksqlConfigLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    query_file_uri: typing.Optional[builtins.str] = None,
    query_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    script_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b8fa0e7d2fd831bf31df1f767f5fd5c8399af8655f4e02c759f6ab1659a736(
    *,
    driver_log_levels: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ba6e615844b0379270ef2cf63e2ee5b70e58a26966bea693755212a4cf7c65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210b2b0e6d6f9c1476ee4b0b229765566b1ee7920a80c7663914d65ac528baee(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253fae1cb50b07b43214fabe2ad24c0938bd59fdd0029e84fabf021fbedabc37(
    value: typing.Optional[DataprocJobSparksqlConfigLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fd5635031cf66199debe22441c033c9bc2ab83f39afab81318da25b435ac3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a18288654a2478a3cdfa628ce083cc15c6bb7b40f6906da4c6bbe5f59be5a9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605819ac3bccaef7c5b0380b3a97aabc2c2c18ce9110f7d622dfd720af9c8291(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71015542a396e106b8935caa280ed8d97b7c5bf3ee88e89ceef102338e75d788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a10e096771af2063b1648fb618bb5f46a1455366723b616efc57b5caad137e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__312c6a9f91a1918159b03efda5f209ac02af2fe0376ad791dd657fe28a3bb3fc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02b37a78d5d205de646dfff1d00769020cb342506a14b894c95cb710c994adc8(
    value: typing.Optional[DataprocJobSparksqlConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a62107d61ca4c9ab233d8e5fec9becac2aed4df1248705d4b66646191c827793(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a71e14ed17f6f0137107eb8716b756722b21838699a89dc5879de34bd00ebbea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c106f88b3a6915bfebd69d235e2ebf86a0a08182353e2eab69c200646fad6fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abe926fa2d4955a74e194c3e5d194d796f7be503afb5e68f9236346b739cc7b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21eb3d2a4a514a7378dee5d0998748cade9680a18ede09d7ca11f0ab7dd1cb2a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609b3107514398844c02b5e91d10557e7cf43a461d8f72ee11829b690865538d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bfd66c7adbacb984ed56bee637c7475b49d9ec8f19961cf3b4de3ec456fe8b(
    value: typing.Optional[DataprocJobStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb1837ad48d05e8f2c21732551874f2e607233fdf6c6f2ab0d6619ada9dd349(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__038ff7fec69319e05853a97a7f9f9b44a4a729bc92895279a98eb13c0bb0ddbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83106728b64feeacc799f440e00c46ae4f6943fa4b1487cb6d9a3f753193a9d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51050d612666c2559cf70bd8483324c7669117d755c69b3a168f2be6e71d4afe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b6b3034bdd5582293bbad7c30f4ff14175b8723b098b539f704869781b6db91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataprocJobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

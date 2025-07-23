r'''
# `google_dataplex_task`

Refer to the Terraform Registry for docs: [`google_dataplex_task`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task).
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


class DataplexTask(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTask",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task google_dataplex_task}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        execution_spec: typing.Union["DataplexTaskExecutionSpec", typing.Dict[builtins.str, typing.Any]],
        trigger_spec: typing.Union["DataplexTaskTriggerSpec", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lake: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notebook: typing.Optional[typing.Union["DataplexTaskNotebook", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        spark: typing.Optional[typing.Union["DataplexTaskSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        task_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexTaskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task google_dataplex_task} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param execution_spec: execution_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#execution_spec DataplexTask#execution_spec}
        :param trigger_spec: trigger_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#trigger_spec DataplexTask#trigger_spec}
        :param description: User-provided description of the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#description DataplexTask#description}
        :param display_name: User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#display_name DataplexTask#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#id DataplexTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the task. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#labels DataplexTask#labels}
        :param lake: The lake in which the task will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#lake DataplexTask#lake}
        :param location: The location in which the task will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#location DataplexTask#location}
        :param notebook: notebook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#notebook DataplexTask#notebook}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#project DataplexTask#project}.
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#spark DataplexTask#spark}
        :param task_id: The task Id of the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#task_id DataplexTask#task_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#timeouts DataplexTask#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c532711edf94d7290439d75a50ee9ef1ea94feeec8d5de1d203b4a4a4d2bc73a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataplexTaskConfig(
            execution_spec=execution_spec,
            trigger_spec=trigger_spec,
            description=description,
            display_name=display_name,
            id=id,
            labels=labels,
            lake=lake,
            location=location,
            notebook=notebook,
            project=project,
            spark=spark,
            task_id=task_id,
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
        '''Generates CDKTF code for importing a DataplexTask resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataplexTask to import.
        :param import_from_id: The id of the existing DataplexTask that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataplexTask to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40aac603017e1dfbbd3b06433851128239057b99e7873de1c736a4d21809d2d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExecutionSpec")
    def put_execution_spec(
        self,
        *,
        service_account: builtins.str,
        args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        max_job_execution_lifetime: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account: Service account to use to execute a task. If not provided, the default Compute service account for the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#service_account DataplexTask#service_account}
        :param args: The arguments to pass to the task. The args can use placeholders of the format ${placeholder} as part of key/value string. These will be interpolated before passing the args to the driver. Currently supported placeholders: - ${taskId} - ${job_time} To pass positional args, set the key as TASK_ARGS. The value should be a comma-separated string of all the positional arguments. To use a delimiter other than comma, refer to https://cloud.google.com/sdk/gcloud/reference/topic/escaping. In case of other keys being present in the args, then TASK_ARGS will be passed as the last argument. An object containing a list of 'key': value pairs. Example: { 'name': 'wrench', 'mass': '1.3kg', 'count': '3' }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#args DataplexTask#args}
        :param kms_key: The Cloud KMS key to use for encryption, of the form: projects/{project_number}/locations/{locationId}/keyRings/{key-ring-name}/cryptoKeys/{key-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#kms_key DataplexTask#kms_key}
        :param max_job_execution_lifetime: The maximum duration after which the job execution is expired. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_job_execution_lifetime DataplexTask#max_job_execution_lifetime}
        :param project: The project in which jobs are run. By default, the project containing the Lake is used. If a project is provided, the ExecutionSpec.service_account must belong to this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#project DataplexTask#project}
        '''
        value = DataplexTaskExecutionSpec(
            service_account=service_account,
            args=args,
            kms_key=kms_key,
            max_job_execution_lifetime=max_job_execution_lifetime,
            project=project,
        )

        return typing.cast(None, jsii.invoke(self, "putExecutionSpec", [value]))

    @jsii.member(jsii_name="putNotebook")
    def put_notebook(
        self,
        *,
        notebook: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        infrastructure_spec: typing.Optional[typing.Union["DataplexTaskNotebookInfrastructureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param notebook: Path to input notebook. This can be the Cloud Storage URI of the notebook file or the path to a Notebook Content. The execution args are accessible as environment variables (TASK_key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#notebook DataplexTask#notebook}
        :param archive_uris: Cloud Storage URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#archive_uris DataplexTask#archive_uris}
        :param file_uris: Cloud Storage URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#file_uris DataplexTask#file_uris}
        :param infrastructure_spec: infrastructure_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#infrastructure_spec DataplexTask#infrastructure_spec}
        '''
        value = DataplexTaskNotebook(
            notebook=notebook,
            archive_uris=archive_uris,
            file_uris=file_uris,
            infrastructure_spec=infrastructure_spec,
        )

        return typing.cast(None, jsii.invoke(self, "putNotebook", [value]))

    @jsii.member(jsii_name="putSpark")
    def put_spark(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        infrastructure_spec: typing.Optional[typing.Union["DataplexTaskSparkInfrastructureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        python_script_file: typing.Optional[builtins.str] = None,
        sql_script: typing.Optional[builtins.str] = None,
        sql_script_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: Cloud Storage URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#archive_uris DataplexTask#archive_uris}
        :param file_uris: Cloud Storage URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#file_uris DataplexTask#file_uris}
        :param infrastructure_spec: infrastructure_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#infrastructure_spec DataplexTask#infrastructure_spec}
        :param main_class: The name of the driver's main class. The jar file that contains the class must be in the default CLASSPATH or specified in jar_file_uris. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#main_class DataplexTask#main_class}
        :param main_jar_file_uri: The Cloud Storage URI of the jar file that contains the main class. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#main_jar_file_uri DataplexTask#main_jar_file_uri}
        :param python_script_file: The Gcloud Storage URI of the main Python file to use as the driver. Must be a .py file. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_script_file DataplexTask#python_script_file}
        :param sql_script: The query text. The execution args are used to declare a set of script variables (set key='value';). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sql_script DataplexTask#sql_script}
        :param sql_script_file: A reference to a query file. This can be the Cloud Storage URI of the query file or it can the path to a SqlScript Content. The execution args are used to declare a set of script variables (set key='value';). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sql_script_file DataplexTask#sql_script_file}
        '''
        value = DataplexTaskSpark(
            archive_uris=archive_uris,
            file_uris=file_uris,
            infrastructure_spec=infrastructure_spec,
            main_class=main_class,
            main_jar_file_uri=main_jar_file_uri,
            python_script_file=python_script_file,
            sql_script=sql_script,
            sql_script_file=sql_script_file,
        )

        return typing.cast(None, jsii.invoke(self, "putSpark", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#create DataplexTask#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#delete DataplexTask#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#update DataplexTask#update}.
        '''
        value = DataplexTaskTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTriggerSpec")
    def put_trigger_spec(
        self,
        *,
        type: builtins.str,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        schedule: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Trigger type of the user-specified Task Possible values: ["ON_DEMAND", "RECURRING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#type DataplexTask#type}
        :param disabled: Prevent the task from executing. This does not cancel already running tasks. It is intended to temporarily disable RECURRING tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#disabled DataplexTask#disabled}
        :param max_retries: Number of retry attempts before aborting. Set to zero to never attempt to retry a failed task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_retries DataplexTask#max_retries}
        :param schedule: Cron schedule (https://en.wikipedia.org/wiki/Cron) for running tasks periodically. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: 'CRON_TZ=${IANA_TIME_ZONE}' or 'TZ=${IANA_TIME_ZONE}'. The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, CRON_TZ=America/New_York 1 * * * *, or TZ=America/New_York 1 * * * *. This field is required for RECURRING tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#schedule DataplexTask#schedule}
        :param start_time: The first run of the task will be after this time. If not specified, the task will run shortly after being submitted if ON_DEMAND and based on the schedule if RECURRING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#start_time DataplexTask#start_time}
        '''
        value = DataplexTaskTriggerSpec(
            type=type,
            disabled=disabled,
            max_retries=max_retries,
            schedule=schedule,
            start_time=start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putTriggerSpec", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLake")
    def reset_lake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLake", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetNotebook")
    def reset_notebook(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebook", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetSpark")
    def reset_spark(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpark", []))

    @jsii.member(jsii_name="resetTaskId")
    def reset_task_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskId", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="executionSpec")
    def execution_spec(self) -> "DataplexTaskExecutionSpecOutputReference":
        return typing.cast("DataplexTaskExecutionSpecOutputReference", jsii.get(self, "executionSpec"))

    @builtins.property
    @jsii.member(jsii_name="executionStatus")
    def execution_status(self) -> "DataplexTaskExecutionStatusList":
        return typing.cast("DataplexTaskExecutionStatusList", jsii.get(self, "executionStatus"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="notebook")
    def notebook(self) -> "DataplexTaskNotebookOutputReference":
        return typing.cast("DataplexTaskNotebookOutputReference", jsii.get(self, "notebook"))

    @builtins.property
    @jsii.member(jsii_name="spark")
    def spark(self) -> "DataplexTaskSparkOutputReference":
        return typing.cast("DataplexTaskSparkOutputReference", jsii.get(self, "spark"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataplexTaskTimeoutsOutputReference":
        return typing.cast("DataplexTaskTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="triggerSpec")
    def trigger_spec(self) -> "DataplexTaskTriggerSpecOutputReference":
        return typing.cast("DataplexTaskTriggerSpecOutputReference", jsii.get(self, "triggerSpec"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="executionSpecInput")
    def execution_spec_input(self) -> typing.Optional["DataplexTaskExecutionSpec"]:
        return typing.cast(typing.Optional["DataplexTaskExecutionSpec"], jsii.get(self, "executionSpecInput"))

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
    @jsii.member(jsii_name="lakeInput")
    def lake_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lakeInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="notebookInput")
    def notebook_input(self) -> typing.Optional["DataplexTaskNotebook"]:
        return typing.cast(typing.Optional["DataplexTaskNotebook"], jsii.get(self, "notebookInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkInput")
    def spark_input(self) -> typing.Optional["DataplexTaskSpark"]:
        return typing.cast(typing.Optional["DataplexTaskSpark"], jsii.get(self, "sparkInput"))

    @builtins.property
    @jsii.member(jsii_name="taskIdInput")
    def task_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexTaskTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DataplexTaskTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerSpecInput")
    def trigger_spec_input(self) -> typing.Optional["DataplexTaskTriggerSpec"]:
        return typing.cast(typing.Optional["DataplexTaskTriggerSpec"], jsii.get(self, "triggerSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f29a20c13cf74f2eb7e10d668176b6c6e4f52cf6904375aae76bada1cde99a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8bba46f88c98739f1a17cbddbfd2ad33a0c36b063cfaefc5ad30353a729e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0698d6f08f960a2bd0bac5da2d50f99dd30b9c881d0e8a68c52d225aa861ad86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aab7b41a0157adb0ae102bbf4c4cffb5664c22ad33736d45991a728431f5f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lake")
    def lake(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lake"))

    @lake.setter
    def lake(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f5f0ff50255230857c48e92b87fbb4581007d711a8c8bd1b35f2c1811ed138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lake", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38556b42ae5438c0281839052ee55aafcbf00e03cedde19cdbf5da1fd1c97c24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76394337c5f5a9f75fba639a4e3de771bf09f41e17a625529807b37956d8c2f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskId")
    def task_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskId"))

    @task_id.setter
    def task_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f549423364419434ee2bb75c178a482e799807f5013c22ea41d6ed7416c75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "execution_spec": "executionSpec",
        "trigger_spec": "triggerSpec",
        "description": "description",
        "display_name": "displayName",
        "id": "id",
        "labels": "labels",
        "lake": "lake",
        "location": "location",
        "notebook": "notebook",
        "project": "project",
        "spark": "spark",
        "task_id": "taskId",
        "timeouts": "timeouts",
    },
)
class DataplexTaskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        execution_spec: typing.Union["DataplexTaskExecutionSpec", typing.Dict[builtins.str, typing.Any]],
        trigger_spec: typing.Union["DataplexTaskTriggerSpec", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lake: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notebook: typing.Optional[typing.Union["DataplexTaskNotebook", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        spark: typing.Optional[typing.Union["DataplexTaskSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        task_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataplexTaskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param execution_spec: execution_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#execution_spec DataplexTask#execution_spec}
        :param trigger_spec: trigger_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#trigger_spec DataplexTask#trigger_spec}
        :param description: User-provided description of the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#description DataplexTask#description}
        :param display_name: User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#display_name DataplexTask#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#id DataplexTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the task. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#labels DataplexTask#labels}
        :param lake: The lake in which the task will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#lake DataplexTask#lake}
        :param location: The location in which the task will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#location DataplexTask#location}
        :param notebook: notebook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#notebook DataplexTask#notebook}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#project DataplexTask#project}.
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#spark DataplexTask#spark}
        :param task_id: The task Id of the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#task_id DataplexTask#task_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#timeouts DataplexTask#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(execution_spec, dict):
            execution_spec = DataplexTaskExecutionSpec(**execution_spec)
        if isinstance(trigger_spec, dict):
            trigger_spec = DataplexTaskTriggerSpec(**trigger_spec)
        if isinstance(notebook, dict):
            notebook = DataplexTaskNotebook(**notebook)
        if isinstance(spark, dict):
            spark = DataplexTaskSpark(**spark)
        if isinstance(timeouts, dict):
            timeouts = DataplexTaskTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88bd4c457e15ac7951ff223f6c7625700f77ca31cdf951e28737e9ad858bca4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument execution_spec", value=execution_spec, expected_type=type_hints["execution_spec"])
            check_type(argname="argument trigger_spec", value=trigger_spec, expected_type=type_hints["trigger_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument lake", value=lake, expected_type=type_hints["lake"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument notebook", value=notebook, expected_type=type_hints["notebook"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument spark", value=spark, expected_type=type_hints["spark"])
            check_type(argname="argument task_id", value=task_id, expected_type=type_hints["task_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_spec": execution_spec,
            "trigger_spec": trigger_spec,
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
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if lake is not None:
            self._values["lake"] = lake
        if location is not None:
            self._values["location"] = location
        if notebook is not None:
            self._values["notebook"] = notebook
        if project is not None:
            self._values["project"] = project
        if spark is not None:
            self._values["spark"] = spark
        if task_id is not None:
            self._values["task_id"] = task_id
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
    def execution_spec(self) -> "DataplexTaskExecutionSpec":
        '''execution_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#execution_spec DataplexTask#execution_spec}
        '''
        result = self._values.get("execution_spec")
        assert result is not None, "Required property 'execution_spec' is missing"
        return typing.cast("DataplexTaskExecutionSpec", result)

    @builtins.property
    def trigger_spec(self) -> "DataplexTaskTriggerSpec":
        '''trigger_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#trigger_spec DataplexTask#trigger_spec}
        '''
        result = self._values.get("trigger_spec")
        assert result is not None, "Required property 'trigger_spec' is missing"
        return typing.cast("DataplexTaskTriggerSpec", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description of the task.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#description DataplexTask#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User friendly display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#display_name DataplexTask#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#id DataplexTask#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-defined labels for the task.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#labels DataplexTask#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lake(self) -> typing.Optional[builtins.str]:
        '''The lake in which the task will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#lake DataplexTask#lake}
        '''
        result = self._values.get("lake")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location in which the task will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#location DataplexTask#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notebook(self) -> typing.Optional["DataplexTaskNotebook"]:
        '''notebook block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#notebook DataplexTask#notebook}
        '''
        result = self._values.get("notebook")
        return typing.cast(typing.Optional["DataplexTaskNotebook"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#project DataplexTask#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark(self) -> typing.Optional["DataplexTaskSpark"]:
        '''spark block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#spark DataplexTask#spark}
        '''
        result = self._values.get("spark")
        return typing.cast(typing.Optional["DataplexTaskSpark"], result)

    @builtins.property
    def task_id(self) -> typing.Optional[builtins.str]:
        '''The task Id of the task.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#task_id DataplexTask#task_id}
        '''
        result = self._values.get("task_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataplexTaskTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#timeouts DataplexTask#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataplexTaskTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskExecutionSpec",
    jsii_struct_bases=[],
    name_mapping={
        "service_account": "serviceAccount",
        "args": "args",
        "kms_key": "kmsKey",
        "max_job_execution_lifetime": "maxJobExecutionLifetime",
        "project": "project",
    },
)
class DataplexTaskExecutionSpec:
    def __init__(
        self,
        *,
        service_account: builtins.str,
        args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        max_job_execution_lifetime: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account: Service account to use to execute a task. If not provided, the default Compute service account for the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#service_account DataplexTask#service_account}
        :param args: The arguments to pass to the task. The args can use placeholders of the format ${placeholder} as part of key/value string. These will be interpolated before passing the args to the driver. Currently supported placeholders: - ${taskId} - ${job_time} To pass positional args, set the key as TASK_ARGS. The value should be a comma-separated string of all the positional arguments. To use a delimiter other than comma, refer to https://cloud.google.com/sdk/gcloud/reference/topic/escaping. In case of other keys being present in the args, then TASK_ARGS will be passed as the last argument. An object containing a list of 'key': value pairs. Example: { 'name': 'wrench', 'mass': '1.3kg', 'count': '3' }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#args DataplexTask#args}
        :param kms_key: The Cloud KMS key to use for encryption, of the form: projects/{project_number}/locations/{locationId}/keyRings/{key-ring-name}/cryptoKeys/{key-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#kms_key DataplexTask#kms_key}
        :param max_job_execution_lifetime: The maximum duration after which the job execution is expired. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_job_execution_lifetime DataplexTask#max_job_execution_lifetime}
        :param project: The project in which jobs are run. By default, the project containing the Lake is used. If a project is provided, the ExecutionSpec.service_account must belong to this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#project DataplexTask#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072e5ee9d2283471bfcff111a561766da94dd297d16c28cf8fffb1a281a531a0)
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument max_job_execution_lifetime", value=max_job_execution_lifetime, expected_type=type_hints["max_job_execution_lifetime"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_account": service_account,
        }
        if args is not None:
            self._values["args"] = args
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if max_job_execution_lifetime is not None:
            self._values["max_job_execution_lifetime"] = max_job_execution_lifetime
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def service_account(self) -> builtins.str:
        '''Service account to use to execute a task.

        If not provided, the default Compute service account for the project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#service_account DataplexTask#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The arguments to pass to the task.

        The args can use placeholders of the format ${placeholder} as part of key/value string. These will be interpolated before passing the args to the driver. Currently supported placeholders: - ${taskId} - ${job_time} To pass positional args, set the key as TASK_ARGS. The value should be a comma-separated string of all the positional arguments. To use a delimiter other than comma, refer to https://cloud.google.com/sdk/gcloud/reference/topic/escaping. In case of other keys being present in the args, then TASK_ARGS will be passed as the last argument. An object containing a list of 'key': value pairs. Example: { 'name': 'wrench', 'mass': '1.3kg', 'count': '3' }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#args DataplexTask#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS key to use for encryption, of the form: projects/{project_number}/locations/{locationId}/keyRings/{key-ring-name}/cryptoKeys/{key-name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#kms_key DataplexTask#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_job_execution_lifetime(self) -> typing.Optional[builtins.str]:
        '''The maximum duration after which the job execution is expired.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_job_execution_lifetime DataplexTask#max_job_execution_lifetime}
        '''
        result = self._values.get("max_job_execution_lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project in which jobs are run.

        By default, the project containing the Lake is used. If a project is provided, the ExecutionSpec.service_account must belong to this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#project DataplexTask#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskExecutionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskExecutionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskExecutionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7855fd9957ee882d80a776e7ff0751955751dfd2a82e65349bb0fb5dc54d6336)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetKmsKey")
    def reset_kms_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKey", []))

    @jsii.member(jsii_name="resetMaxJobExecutionLifetime")
    def reset_max_job_execution_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxJobExecutionLifetime", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyInput")
    def kms_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="maxJobExecutionLifetimeInput")
    def max_job_execution_lifetime_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxJobExecutionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3808b18bbfb0e0663ca3e7c2df5444d9683577970354abb54f5dd06cd907558a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571adedba2e45a5c0ef71ab9953bf3326b812b411e838773b7e4f6d843a951e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxJobExecutionLifetime")
    def max_job_execution_lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxJobExecutionLifetime"))

    @max_job_execution_lifetime.setter
    def max_job_execution_lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76787775b886adb241793e9adc910b7d05f39099edff7281871cc7b00188a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxJobExecutionLifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be4a038e49de6605dc59867eb4b3860c91919ef643728e59d6abf226add33f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7be0aec0fd667fe2d89937a16657ed4ababe626d7b47a40b98ed9ea00da039e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexTaskExecutionSpec]:
        return typing.cast(typing.Optional[DataplexTaskExecutionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexTaskExecutionSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b7521f1458d7eac57d509338d3122eaa50060e04a217977bdd1c06cf9d15724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskExecutionStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexTaskExecutionStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskExecutionStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskExecutionStatusLatestJob",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataplexTaskExecutionStatusLatestJob:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskExecutionStatusLatestJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskExecutionStatusLatestJobList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskExecutionStatusLatestJobList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7180072b55f689c4437e2d26af52b6790e64c7ec404242a03354834ccb4af6df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataplexTaskExecutionStatusLatestJobOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc68110fb95d24c86345ed8d2303eb734d99a18aee292e0256a6f46b17ab2cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexTaskExecutionStatusLatestJobOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b303e8683a8beb673a9bbee4ed71a2211551657defc145596f9b192c5a6c2d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__981074338a294d3cc6435e493bb1ed99825101bc64424cd71b9dbdca94c517fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abee913e94bb78c3f7487fa66caba59fd69e04763d97ab652671c120c71a0df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataplexTaskExecutionStatusLatestJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskExecutionStatusLatestJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79e92fcaaa74396434ada188a9416eec6173763698cb3e2023c3fa0eb468f381)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="retryCount")
    def retry_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retryCount"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="serviceJob")
    def service_job(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceJob"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexTaskExecutionStatusLatestJob]:
        return typing.cast(typing.Optional[DataplexTaskExecutionStatusLatestJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskExecutionStatusLatestJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6b5d1ca6e9fc530d11c59e7dacd30fc3a922df4998cc9f7e73588892fe52b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexTaskExecutionStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskExecutionStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ab26d1226ec63c814bca0b97f0eec92623187652480ceb14cbe3427d8ade9ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataplexTaskExecutionStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7586fdd7eee120b86d44d3be350fb45e1282433e7b4b14ff7c687e4fb738ff54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataplexTaskExecutionStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbe87607afbc21cbe3d18aa05d2395df3953c982a94b06a4398e7d699a7ffdb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__102bf2e1b49923de717d8842766de361ae7d30c1bc3597e3450eb0b0c860f631)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b47c6ebaa6095c651a8e4b2a144a1655f3b171340b13c277e647c0a394f039c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataplexTaskExecutionStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskExecutionStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a746e0b0a024a50301fbf6d4d36fb0627ebe085cbfb56e912ef2b2b063d45b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="latestJob")
    def latest_job(self) -> DataplexTaskExecutionStatusLatestJobList:
        return typing.cast(DataplexTaskExecutionStatusLatestJobList, jsii.get(self, "latestJob"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexTaskExecutionStatus]:
        return typing.cast(typing.Optional[DataplexTaskExecutionStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskExecutionStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3519de2758e1321ae430de1146c70ff0bdc9186f553ffe813a92c077711be4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebook",
    jsii_struct_bases=[],
    name_mapping={
        "notebook": "notebook",
        "archive_uris": "archiveUris",
        "file_uris": "fileUris",
        "infrastructure_spec": "infrastructureSpec",
    },
)
class DataplexTaskNotebook:
    def __init__(
        self,
        *,
        notebook: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        infrastructure_spec: typing.Optional[typing.Union["DataplexTaskNotebookInfrastructureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param notebook: Path to input notebook. This can be the Cloud Storage URI of the notebook file or the path to a Notebook Content. The execution args are accessible as environment variables (TASK_key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#notebook DataplexTask#notebook}
        :param archive_uris: Cloud Storage URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#archive_uris DataplexTask#archive_uris}
        :param file_uris: Cloud Storage URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#file_uris DataplexTask#file_uris}
        :param infrastructure_spec: infrastructure_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#infrastructure_spec DataplexTask#infrastructure_spec}
        '''
        if isinstance(infrastructure_spec, dict):
            infrastructure_spec = DataplexTaskNotebookInfrastructureSpec(**infrastructure_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021238a5cc76a058e53bb187a2debd40905a27f35ef165e438170fcd6b3a9061)
            check_type(argname="argument notebook", value=notebook, expected_type=type_hints["notebook"])
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument infrastructure_spec", value=infrastructure_spec, expected_type=type_hints["infrastructure_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notebook": notebook,
        }
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if infrastructure_spec is not None:
            self._values["infrastructure_spec"] = infrastructure_spec

    @builtins.property
    def notebook(self) -> builtins.str:
        '''Path to input notebook.

        This can be the Cloud Storage URI of the notebook file or the path to a Notebook Content. The execution args are accessible as environment variables (TASK_key=value).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#notebook DataplexTask#notebook}
        '''
        result = self._values.get("notebook")
        assert result is not None, "Required property 'notebook' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#archive_uris DataplexTask#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#file_uris DataplexTask#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def infrastructure_spec(
        self,
    ) -> typing.Optional["DataplexTaskNotebookInfrastructureSpec"]:
        '''infrastructure_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#infrastructure_spec DataplexTask#infrastructure_spec}
        '''
        result = self._values.get("infrastructure_spec")
        return typing.cast(typing.Optional["DataplexTaskNotebookInfrastructureSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskNotebook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookInfrastructureSpec",
    jsii_struct_bases=[],
    name_mapping={
        "batch": "batch",
        "container_image": "containerImage",
        "vpc_network": "vpcNetwork",
    },
)
class DataplexTaskNotebookInfrastructureSpec:
    def __init__(
        self,
        *,
        batch: typing.Optional[typing.Union["DataplexTaskNotebookInfrastructureSpecBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union["DataplexTaskNotebookInfrastructureSpecContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network: typing.Optional[typing.Union["DataplexTaskNotebookInfrastructureSpecVpcNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch: batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#batch DataplexTask#batch}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#container_image DataplexTask#container_image}
        :param vpc_network: vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#vpc_network DataplexTask#vpc_network}
        '''
        if isinstance(batch, dict):
            batch = DataplexTaskNotebookInfrastructureSpecBatch(**batch)
        if isinstance(container_image, dict):
            container_image = DataplexTaskNotebookInfrastructureSpecContainerImage(**container_image)
        if isinstance(vpc_network, dict):
            vpc_network = DataplexTaskNotebookInfrastructureSpecVpcNetwork(**vpc_network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a983c216c5819dbf14556d958e97ff3df63f1911f8f30a8de453755b44a02c)
            check_type(argname="argument batch", value=batch, expected_type=type_hints["batch"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument vpc_network", value=vpc_network, expected_type=type_hints["vpc_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch is not None:
            self._values["batch"] = batch
        if container_image is not None:
            self._values["container_image"] = container_image
        if vpc_network is not None:
            self._values["vpc_network"] = vpc_network

    @builtins.property
    def batch(self) -> typing.Optional["DataplexTaskNotebookInfrastructureSpecBatch"]:
        '''batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#batch DataplexTask#batch}
        '''
        result = self._values.get("batch")
        return typing.cast(typing.Optional["DataplexTaskNotebookInfrastructureSpecBatch"], result)

    @builtins.property
    def container_image(
        self,
    ) -> typing.Optional["DataplexTaskNotebookInfrastructureSpecContainerImage"]:
        '''container_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#container_image DataplexTask#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional["DataplexTaskNotebookInfrastructureSpecContainerImage"], result)

    @builtins.property
    def vpc_network(
        self,
    ) -> typing.Optional["DataplexTaskNotebookInfrastructureSpecVpcNetwork"]:
        '''vpc_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#vpc_network DataplexTask#vpc_network}
        '''
        result = self._values.get("vpc_network")
        return typing.cast(typing.Optional["DataplexTaskNotebookInfrastructureSpecVpcNetwork"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskNotebookInfrastructureSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookInfrastructureSpecBatch",
    jsii_struct_bases=[],
    name_mapping={
        "executors_count": "executorsCount",
        "max_executors_count": "maxExecutorsCount",
    },
)
class DataplexTaskNotebookInfrastructureSpecBatch:
    def __init__(
        self,
        *,
        executors_count: typing.Optional[jsii.Number] = None,
        max_executors_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param executors_count: Total number of job executors. Executor Count should be between 2 and 100. [Default=2]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#executors_count DataplexTask#executors_count}
        :param max_executors_count: Max configurable executors. If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_executors_count DataplexTask#max_executors_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6134fbcdc2ef10c7510c11edd48a048d95a947db7d2594af43066cdea80159e)
            check_type(argname="argument executors_count", value=executors_count, expected_type=type_hints["executors_count"])
            check_type(argname="argument max_executors_count", value=max_executors_count, expected_type=type_hints["max_executors_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if executors_count is not None:
            self._values["executors_count"] = executors_count
        if max_executors_count is not None:
            self._values["max_executors_count"] = max_executors_count

    @builtins.property
    def executors_count(self) -> typing.Optional[jsii.Number]:
        '''Total number of job executors. Executor Count should be between 2 and 100. [Default=2].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#executors_count DataplexTask#executors_count}
        '''
        result = self._values.get("executors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_executors_count(self) -> typing.Optional[jsii.Number]:
        '''Max configurable executors.

        If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_executors_count DataplexTask#max_executors_count}
        '''
        result = self._values.get("max_executors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskNotebookInfrastructureSpecBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskNotebookInfrastructureSpecBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookInfrastructureSpecBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26800b75d60f8b97bfa7e98fda51d5e9426d86b25e142dc7c7464d5801e8a8ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecutorsCount")
    def reset_executors_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutorsCount", []))

    @jsii.member(jsii_name="resetMaxExecutorsCount")
    def reset_max_executors_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxExecutorsCount", []))

    @builtins.property
    @jsii.member(jsii_name="executorsCountInput")
    def executors_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxExecutorsCountInput")
    def max_executors_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxExecutorsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="executorsCount")
    def executors_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executorsCount"))

    @executors_count.setter
    def executors_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d37dff5a19774caf8f4743e40b67a22fadeef1082f74e698db3c7e441b8db97c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxExecutorsCount")
    def max_executors_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxExecutorsCount"))

    @max_executors_count.setter
    def max_executors_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aedcb68336405641786830b3f7c2f617a45bab7fb2b8d8ef94df8c85fefa3cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxExecutorsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexTaskNotebookInfrastructureSpecBatch]:
        return typing.cast(typing.Optional[DataplexTaskNotebookInfrastructureSpecBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskNotebookInfrastructureSpecBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72afac978f06b3919d7f2a9c3155d157c4d0b2d7bfb41cb5aeda26e07a936dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookInfrastructureSpecContainerImage",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "java_jars": "javaJars",
        "properties": "properties",
        "python_packages": "pythonPackages",
    },
)
class DataplexTaskNotebookInfrastructureSpecContainerImage:
    def __init__(
        self,
        *,
        image: typing.Optional[builtins.str] = None,
        java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param image: Container image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#image DataplexTask#image}
        :param java_jars: A list of Java JARS to add to the classpath. Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#java_jars DataplexTask#java_jars}
        :param properties: Override to common configuration of open source components installed on the Dataproc cluster. The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#properties DataplexTask#properties}
        :param python_packages: A list of python packages to be installed. Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_packages DataplexTask#python_packages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b558456921b12618929a35e630ad17eee7cbd9d77b7a4358352ad03902200c35)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument java_jars", value=java_jars, expected_type=type_hints["java_jars"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument python_packages", value=python_packages, expected_type=type_hints["python_packages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image is not None:
            self._values["image"] = image
        if java_jars is not None:
            self._values["java_jars"] = java_jars
        if properties is not None:
            self._values["properties"] = properties
        if python_packages is not None:
            self._values["python_packages"] = python_packages

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Container image to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#image DataplexTask#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def java_jars(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Java JARS to add to the classpath.

        Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#java_jars DataplexTask#java_jars}
        '''
        result = self._values.get("java_jars")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Override to common configuration of open source components installed on the Dataproc cluster.

        The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#properties DataplexTask#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def python_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of python packages to be installed.

        Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_packages DataplexTask#python_packages}
        '''
        result = self._values.get("python_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskNotebookInfrastructureSpecContainerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskNotebookInfrastructureSpecContainerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookInfrastructureSpecContainerImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a661bef24e01565e7a200451a0dc52004d00f1a56f84446057cb03b405af8ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetJavaJars")
    def reset_java_jars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJavaJars", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetPythonPackages")
    def reset_python_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonPackages", []))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="javaJarsInput")
    def java_jars_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "javaJarsInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonPackagesInput")
    def python_packages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pythonPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b68c83c8f0136c3af5f879d107b0ab9f5b4eef4f1c10c1b84221cc0927a264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="javaJars")
    def java_jars(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "javaJars"))

    @java_jars.setter
    def java_jars(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413126f4455d7029077556576e70177ef9ce16946df620aa216d365c928e2ad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javaJars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b693c454e65591aed40eff85b794d21b31fe1849d443746531bde11b90268b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonPackages")
    def python_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonPackages"))

    @python_packages.setter
    def python_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__444a1066d5c6038e45f8f360cb92b8d8aa65dc34b14004aad93e3bdab01a58a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonPackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexTaskNotebookInfrastructureSpecContainerImage]:
        return typing.cast(typing.Optional[DataplexTaskNotebookInfrastructureSpecContainerImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskNotebookInfrastructureSpecContainerImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8dd6d86ce08350884955936987958d0f1509ebda9ea32de309099883498efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexTaskNotebookInfrastructureSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookInfrastructureSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4eca2140776fedf00d922a869ebf62848a2fed8705dbc9e7a85c2d42cb28f6dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBatch")
    def put_batch(
        self,
        *,
        executors_count: typing.Optional[jsii.Number] = None,
        max_executors_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param executors_count: Total number of job executors. Executor Count should be between 2 and 100. [Default=2]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#executors_count DataplexTask#executors_count}
        :param max_executors_count: Max configurable executors. If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_executors_count DataplexTask#max_executors_count}
        '''
        value = DataplexTaskNotebookInfrastructureSpecBatch(
            executors_count=executors_count, max_executors_count=max_executors_count
        )

        return typing.cast(None, jsii.invoke(self, "putBatch", [value]))

    @jsii.member(jsii_name="putContainerImage")
    def put_container_image(
        self,
        *,
        image: typing.Optional[builtins.str] = None,
        java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param image: Container image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#image DataplexTask#image}
        :param java_jars: A list of Java JARS to add to the classpath. Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#java_jars DataplexTask#java_jars}
        :param properties: Override to common configuration of open source components installed on the Dataproc cluster. The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#properties DataplexTask#properties}
        :param python_packages: A list of python packages to be installed. Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_packages DataplexTask#python_packages}
        '''
        value = DataplexTaskNotebookInfrastructureSpecContainerImage(
            image=image,
            java_jars=java_jars,
            properties=properties,
            python_packages=python_packages,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerImage", [value]))

    @jsii.member(jsii_name="putVpcNetwork")
    def put_vpc_network(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        sub_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network: The Cloud VPC network in which the job is run. By default, the Cloud VPC network named Default within the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network DataplexTask#network}
        :param network_tags: List of network tags to apply to the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network_tags DataplexTask#network_tags}
        :param sub_network: The Cloud VPC sub-network in which the job is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sub_network DataplexTask#sub_network}
        '''
        value = DataplexTaskNotebookInfrastructureSpecVpcNetwork(
            network=network, network_tags=network_tags, sub_network=sub_network
        )

        return typing.cast(None, jsii.invoke(self, "putVpcNetwork", [value]))

    @jsii.member(jsii_name="resetBatch")
    def reset_batch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatch", []))

    @jsii.member(jsii_name="resetContainerImage")
    def reset_container_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImage", []))

    @jsii.member(jsii_name="resetVpcNetwork")
    def reset_vpc_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="batch")
    def batch(self) -> DataplexTaskNotebookInfrastructureSpecBatchOutputReference:
        return typing.cast(DataplexTaskNotebookInfrastructureSpecBatchOutputReference, jsii.get(self, "batch"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(
        self,
    ) -> DataplexTaskNotebookInfrastructureSpecContainerImageOutputReference:
        return typing.cast(DataplexTaskNotebookInfrastructureSpecContainerImageOutputReference, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetwork")
    def vpc_network(
        self,
    ) -> "DataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference":
        return typing.cast("DataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference", jsii.get(self, "vpcNetwork"))

    @builtins.property
    @jsii.member(jsii_name="batchInput")
    def batch_input(
        self,
    ) -> typing.Optional[DataplexTaskNotebookInfrastructureSpecBatch]:
        return typing.cast(typing.Optional[DataplexTaskNotebookInfrastructureSpecBatch], jsii.get(self, "batchInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(
        self,
    ) -> typing.Optional[DataplexTaskNotebookInfrastructureSpecContainerImage]:
        return typing.cast(typing.Optional[DataplexTaskNotebookInfrastructureSpecContainerImage], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkInput")
    def vpc_network_input(
        self,
    ) -> typing.Optional["DataplexTaskNotebookInfrastructureSpecVpcNetwork"]:
        return typing.cast(typing.Optional["DataplexTaskNotebookInfrastructureSpecVpcNetwork"], jsii.get(self, "vpcNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexTaskNotebookInfrastructureSpec]:
        return typing.cast(typing.Optional[DataplexTaskNotebookInfrastructureSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskNotebookInfrastructureSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24aa7ed6bf49a5aa59b3fc401cd2ac13564b38bf92e6300dcb2ff7bd3e185ca2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookInfrastructureSpecVpcNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "network": "network",
        "network_tags": "networkTags",
        "sub_network": "subNetwork",
    },
)
class DataplexTaskNotebookInfrastructureSpecVpcNetwork:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        sub_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network: The Cloud VPC network in which the job is run. By default, the Cloud VPC network named Default within the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network DataplexTask#network}
        :param network_tags: List of network tags to apply to the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network_tags DataplexTask#network_tags}
        :param sub_network: The Cloud VPC sub-network in which the job is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sub_network DataplexTask#sub_network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__362f079490d66b0974028b3843a844458f32ad38c5c90ac975122e0ab9bcde79)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_tags", value=network_tags, expected_type=type_hints["network_tags"])
            check_type(argname="argument sub_network", value=sub_network, expected_type=type_hints["sub_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network
        if network_tags is not None:
            self._values["network_tags"] = network_tags
        if sub_network is not None:
            self._values["sub_network"] = sub_network

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The Cloud VPC network in which the job is run.

        By default, the Cloud VPC network named Default within the project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network DataplexTask#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of network tags to apply to the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network_tags DataplexTask#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sub_network(self) -> typing.Optional[builtins.str]:
        '''The Cloud VPC sub-network in which the job is run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sub_network DataplexTask#sub_network}
        '''
        result = self._values.get("sub_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskNotebookInfrastructureSpecVpcNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__033f679003447b8fbfd55d67489270c841daca809bf9e606fce74b3c9fd158ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkTags")
    def reset_network_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkTags", []))

    @jsii.member(jsii_name="resetSubNetwork")
    def reset_sub_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTagsInput")
    def network_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="subNetworkInput")
    def sub_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38456b9a6bb8a2bf44dd929b8b32f4d2143879055e1aa2e107dbd3c0dd918a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4bbca56b46f20d5cc14815853ee85d74e74c09eb59818c9566765331f460f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subNetwork")
    def sub_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subNetwork"))

    @sub_network.setter
    def sub_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90b6092ec74b88dc58c6ea801ff956f284dd124a1efef67353c0964132d5358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexTaskNotebookInfrastructureSpecVpcNetwork]:
        return typing.cast(typing.Optional[DataplexTaskNotebookInfrastructureSpecVpcNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskNotebookInfrastructureSpecVpcNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475da08c25daa8e92b5e4ef17c8f2473ee213ca9137be02aeb273a94d17874d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexTaskNotebookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskNotebookOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__588ab522036016d1004c8ca7f5852bd34cd534d677d58016c0e4893c0ab79325)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfrastructureSpec")
    def put_infrastructure_spec(
        self,
        *,
        batch: typing.Optional[typing.Union[DataplexTaskNotebookInfrastructureSpecBatch, typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union[DataplexTaskNotebookInfrastructureSpecContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network: typing.Optional[typing.Union[DataplexTaskNotebookInfrastructureSpecVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch: batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#batch DataplexTask#batch}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#container_image DataplexTask#container_image}
        :param vpc_network: vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#vpc_network DataplexTask#vpc_network}
        '''
        value = DataplexTaskNotebookInfrastructureSpec(
            batch=batch, container_image=container_image, vpc_network=vpc_network
        )

        return typing.cast(None, jsii.invoke(self, "putInfrastructureSpec", [value]))

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetInfrastructureSpec")
    def reset_infrastructure_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureSpec", []))

    @builtins.property
    @jsii.member(jsii_name="infrastructureSpec")
    def infrastructure_spec(
        self,
    ) -> DataplexTaskNotebookInfrastructureSpecOutputReference:
        return typing.cast(DataplexTaskNotebookInfrastructureSpecOutputReference, jsii.get(self, "infrastructureSpec"))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureSpecInput")
    def infrastructure_spec_input(
        self,
    ) -> typing.Optional[DataplexTaskNotebookInfrastructureSpec]:
        return typing.cast(typing.Optional[DataplexTaskNotebookInfrastructureSpec], jsii.get(self, "infrastructureSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="notebookInput")
    def notebook_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebookInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0d24b6f4e561ca48ff00ec92eef43cc3db1bc343e238c17da42f7cdd99a478b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c07b4b16a3a2fcf841714ba58e6d075d56dbf6fc03307e8b6e0f1564fb0ae24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebook")
    def notebook(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebook"))

    @notebook.setter
    def notebook(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3012d11ad9bf5fdfcd51ac9dc7da6467cec8fa5f6095697149fe34ba0ae9b784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexTaskNotebook]:
        return typing.cast(typing.Optional[DataplexTaskNotebook], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexTaskNotebook]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0815c4d01df785e253a97e145f0576cd857c0e12945edf6470251db103bfc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSpark",
    jsii_struct_bases=[],
    name_mapping={
        "archive_uris": "archiveUris",
        "file_uris": "fileUris",
        "infrastructure_spec": "infrastructureSpec",
        "main_class": "mainClass",
        "main_jar_file_uri": "mainJarFileUri",
        "python_script_file": "pythonScriptFile",
        "sql_script": "sqlScript",
        "sql_script_file": "sqlScriptFile",
    },
)
class DataplexTaskSpark:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        infrastructure_spec: typing.Optional[typing.Union["DataplexTaskSparkInfrastructureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        python_script_file: typing.Optional[builtins.str] = None,
        sql_script: typing.Optional[builtins.str] = None,
        sql_script_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: Cloud Storage URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#archive_uris DataplexTask#archive_uris}
        :param file_uris: Cloud Storage URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#file_uris DataplexTask#file_uris}
        :param infrastructure_spec: infrastructure_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#infrastructure_spec DataplexTask#infrastructure_spec}
        :param main_class: The name of the driver's main class. The jar file that contains the class must be in the default CLASSPATH or specified in jar_file_uris. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#main_class DataplexTask#main_class}
        :param main_jar_file_uri: The Cloud Storage URI of the jar file that contains the main class. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#main_jar_file_uri DataplexTask#main_jar_file_uri}
        :param python_script_file: The Gcloud Storage URI of the main Python file to use as the driver. Must be a .py file. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_script_file DataplexTask#python_script_file}
        :param sql_script: The query text. The execution args are used to declare a set of script variables (set key='value';). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sql_script DataplexTask#sql_script}
        :param sql_script_file: A reference to a query file. This can be the Cloud Storage URI of the query file or it can the path to a SqlScript Content. The execution args are used to declare a set of script variables (set key='value';). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sql_script_file DataplexTask#sql_script_file}
        '''
        if isinstance(infrastructure_spec, dict):
            infrastructure_spec = DataplexTaskSparkInfrastructureSpec(**infrastructure_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15278a948bd7ff153d1e52a4a978b8b513ad940341ac7d8135bc5395205613b)
            check_type(argname="argument archive_uris", value=archive_uris, expected_type=type_hints["archive_uris"])
            check_type(argname="argument file_uris", value=file_uris, expected_type=type_hints["file_uris"])
            check_type(argname="argument infrastructure_spec", value=infrastructure_spec, expected_type=type_hints["infrastructure_spec"])
            check_type(argname="argument main_class", value=main_class, expected_type=type_hints["main_class"])
            check_type(argname="argument main_jar_file_uri", value=main_jar_file_uri, expected_type=type_hints["main_jar_file_uri"])
            check_type(argname="argument python_script_file", value=python_script_file, expected_type=type_hints["python_script_file"])
            check_type(argname="argument sql_script", value=sql_script, expected_type=type_hints["sql_script"])
            check_type(argname="argument sql_script_file", value=sql_script_file, expected_type=type_hints["sql_script_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_uris is not None:
            self._values["archive_uris"] = archive_uris
        if file_uris is not None:
            self._values["file_uris"] = file_uris
        if infrastructure_spec is not None:
            self._values["infrastructure_spec"] = infrastructure_spec
        if main_class is not None:
            self._values["main_class"] = main_class
        if main_jar_file_uri is not None:
            self._values["main_jar_file_uri"] = main_jar_file_uri
        if python_script_file is not None:
            self._values["python_script_file"] = python_script_file
        if sql_script is not None:
            self._values["sql_script"] = sql_script
        if sql_script_file is not None:
            self._values["sql_script_file"] = sql_script_file

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#archive_uris DataplexTask#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#file_uris DataplexTask#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def infrastructure_spec(
        self,
    ) -> typing.Optional["DataplexTaskSparkInfrastructureSpec"]:
        '''infrastructure_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#infrastructure_spec DataplexTask#infrastructure_spec}
        '''
        result = self._values.get("infrastructure_spec")
        return typing.cast(typing.Optional["DataplexTaskSparkInfrastructureSpec"], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The name of the driver's main class.

        The jar file that contains the class must be in the default CLASSPATH or specified in jar_file_uris. The execution args are passed in as a sequence of named process arguments (--key=value).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#main_class DataplexTask#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of the jar file that contains the main class.

        The execution args are passed in as a sequence of named process arguments (--key=value).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#main_jar_file_uri DataplexTask#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_script_file(self) -> typing.Optional[builtins.str]:
        '''The Gcloud Storage URI of the main Python file to use as the driver.

        Must be a .py file. The execution args are passed in as a sequence of named process arguments (--key=value).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_script_file DataplexTask#python_script_file}
        '''
        result = self._values.get("python_script_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_script(self) -> typing.Optional[builtins.str]:
        '''The query text. The execution args are used to declare a set of script variables (set key='value';).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sql_script DataplexTask#sql_script}
        '''
        result = self._values.get("sql_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_script_file(self) -> typing.Optional[builtins.str]:
        '''A reference to a query file.

        This can be the Cloud Storage URI of the query file or it can the path to a SqlScript Content. The execution args are used to declare a set of script variables (set key='value';).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sql_script_file DataplexTask#sql_script_file}
        '''
        result = self._values.get("sql_script_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskSpark(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkInfrastructureSpec",
    jsii_struct_bases=[],
    name_mapping={
        "batch": "batch",
        "container_image": "containerImage",
        "vpc_network": "vpcNetwork",
    },
)
class DataplexTaskSparkInfrastructureSpec:
    def __init__(
        self,
        *,
        batch: typing.Optional[typing.Union["DataplexTaskSparkInfrastructureSpecBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union["DataplexTaskSparkInfrastructureSpecContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network: typing.Optional[typing.Union["DataplexTaskSparkInfrastructureSpecVpcNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch: batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#batch DataplexTask#batch}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#container_image DataplexTask#container_image}
        :param vpc_network: vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#vpc_network DataplexTask#vpc_network}
        '''
        if isinstance(batch, dict):
            batch = DataplexTaskSparkInfrastructureSpecBatch(**batch)
        if isinstance(container_image, dict):
            container_image = DataplexTaskSparkInfrastructureSpecContainerImage(**container_image)
        if isinstance(vpc_network, dict):
            vpc_network = DataplexTaskSparkInfrastructureSpecVpcNetwork(**vpc_network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721908c8415b261c5f2f6e152bfe9f02965865fc3d7641e6314ebf5444ebc153)
            check_type(argname="argument batch", value=batch, expected_type=type_hints["batch"])
            check_type(argname="argument container_image", value=container_image, expected_type=type_hints["container_image"])
            check_type(argname="argument vpc_network", value=vpc_network, expected_type=type_hints["vpc_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch is not None:
            self._values["batch"] = batch
        if container_image is not None:
            self._values["container_image"] = container_image
        if vpc_network is not None:
            self._values["vpc_network"] = vpc_network

    @builtins.property
    def batch(self) -> typing.Optional["DataplexTaskSparkInfrastructureSpecBatch"]:
        '''batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#batch DataplexTask#batch}
        '''
        result = self._values.get("batch")
        return typing.cast(typing.Optional["DataplexTaskSparkInfrastructureSpecBatch"], result)

    @builtins.property
    def container_image(
        self,
    ) -> typing.Optional["DataplexTaskSparkInfrastructureSpecContainerImage"]:
        '''container_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#container_image DataplexTask#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional["DataplexTaskSparkInfrastructureSpecContainerImage"], result)

    @builtins.property
    def vpc_network(
        self,
    ) -> typing.Optional["DataplexTaskSparkInfrastructureSpecVpcNetwork"]:
        '''vpc_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#vpc_network DataplexTask#vpc_network}
        '''
        result = self._values.get("vpc_network")
        return typing.cast(typing.Optional["DataplexTaskSparkInfrastructureSpecVpcNetwork"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskSparkInfrastructureSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkInfrastructureSpecBatch",
    jsii_struct_bases=[],
    name_mapping={
        "executors_count": "executorsCount",
        "max_executors_count": "maxExecutorsCount",
    },
)
class DataplexTaskSparkInfrastructureSpecBatch:
    def __init__(
        self,
        *,
        executors_count: typing.Optional[jsii.Number] = None,
        max_executors_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param executors_count: Total number of job executors. Executor Count should be between 2 and 100. [Default=2]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#executors_count DataplexTask#executors_count}
        :param max_executors_count: Max configurable executors. If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_executors_count DataplexTask#max_executors_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48f9139f91239561cb18212a077f0090fe05ab8cd431d2c970c7e53910bd487)
            check_type(argname="argument executors_count", value=executors_count, expected_type=type_hints["executors_count"])
            check_type(argname="argument max_executors_count", value=max_executors_count, expected_type=type_hints["max_executors_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if executors_count is not None:
            self._values["executors_count"] = executors_count
        if max_executors_count is not None:
            self._values["max_executors_count"] = max_executors_count

    @builtins.property
    def executors_count(self) -> typing.Optional[jsii.Number]:
        '''Total number of job executors. Executor Count should be between 2 and 100. [Default=2].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#executors_count DataplexTask#executors_count}
        '''
        result = self._values.get("executors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_executors_count(self) -> typing.Optional[jsii.Number]:
        '''Max configurable executors.

        If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_executors_count DataplexTask#max_executors_count}
        '''
        result = self._values.get("max_executors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskSparkInfrastructureSpecBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskSparkInfrastructureSpecBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkInfrastructureSpecBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e12c740366e9ca4d1d237a1ac2336169492a594ad8687bf432e62dcb946768a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecutorsCount")
    def reset_executors_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutorsCount", []))

    @jsii.member(jsii_name="resetMaxExecutorsCount")
    def reset_max_executors_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxExecutorsCount", []))

    @builtins.property
    @jsii.member(jsii_name="executorsCountInput")
    def executors_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "executorsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxExecutorsCountInput")
    def max_executors_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxExecutorsCountInput"))

    @builtins.property
    @jsii.member(jsii_name="executorsCount")
    def executors_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executorsCount"))

    @executors_count.setter
    def executors_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b809c656b96d0917eb2f2a759ae8de6fc698a34a10e11403eb12faa5203504c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxExecutorsCount")
    def max_executors_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxExecutorsCount"))

    @max_executors_count.setter
    def max_executors_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99e068c97ee25d120bd9e7ce8c5c529e3afc22fca920b6d08e333b6a6bce8b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxExecutorsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexTaskSparkInfrastructureSpecBatch]:
        return typing.cast(typing.Optional[DataplexTaskSparkInfrastructureSpecBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskSparkInfrastructureSpecBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a11ec10a75b24dc76d8a3d6fac69eddd85c55c3f94c71c3b302bada8df2dda4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkInfrastructureSpecContainerImage",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "java_jars": "javaJars",
        "properties": "properties",
        "python_packages": "pythonPackages",
    },
)
class DataplexTaskSparkInfrastructureSpecContainerImage:
    def __init__(
        self,
        *,
        image: typing.Optional[builtins.str] = None,
        java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param image: Container image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#image DataplexTask#image}
        :param java_jars: A list of Java JARS to add to the classpath. Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#java_jars DataplexTask#java_jars}
        :param properties: Override to common configuration of open source components installed on the Dataproc cluster. The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#properties DataplexTask#properties}
        :param python_packages: A list of python packages to be installed. Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_packages DataplexTask#python_packages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fedeb09bc118cb100005b8444c2ba6e726ca98bd9a33d29a4e9b7f28b044184)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument java_jars", value=java_jars, expected_type=type_hints["java_jars"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument python_packages", value=python_packages, expected_type=type_hints["python_packages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image is not None:
            self._values["image"] = image
        if java_jars is not None:
            self._values["java_jars"] = java_jars
        if properties is not None:
            self._values["properties"] = properties
        if python_packages is not None:
            self._values["python_packages"] = python_packages

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''Container image to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#image DataplexTask#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def java_jars(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Java JARS to add to the classpath.

        Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#java_jars DataplexTask#java_jars}
        '''
        result = self._values.get("java_jars")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Override to common configuration of open source components installed on the Dataproc cluster.

        The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#properties DataplexTask#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def python_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of python packages to be installed.

        Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_packages DataplexTask#python_packages}
        '''
        result = self._values.get("python_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskSparkInfrastructureSpecContainerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskSparkInfrastructureSpecContainerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkInfrastructureSpecContainerImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7229e4bfebdbf008cdef618d4f66f82d989d6060a365932a44968091f79b3b44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetImage")
    def reset_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImage", []))

    @jsii.member(jsii_name="resetJavaJars")
    def reset_java_jars(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJavaJars", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetPythonPackages")
    def reset_python_packages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonPackages", []))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="javaJarsInput")
    def java_jars_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "javaJarsInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonPackagesInput")
    def python_packages_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "pythonPackagesInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b8d51089c55ae1f02fcb08c11a60bc834c16584a811fdb98385a5b623fa070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="javaJars")
    def java_jars(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "javaJars"))

    @java_jars.setter
    def java_jars(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113ee21bac4fea0f8d1452f6fe7c8e57f9a91e5c3ad753c5fd322d58f74176d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javaJars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db2efabe28804897f2951a158e4a41bc17613323e505a0b8baaed70b7238ac5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonPackages")
    def python_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonPackages"))

    @python_packages.setter
    def python_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e9b85d09da41067079f7c975a7babac7577d05820ffe85a8e482af7c1f0f87e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonPackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexTaskSparkInfrastructureSpecContainerImage]:
        return typing.cast(typing.Optional[DataplexTaskSparkInfrastructureSpecContainerImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskSparkInfrastructureSpecContainerImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b5f09c5c8ab664ba6758b0cf2459fccf8ae07a367d643b1495164c3a334d88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexTaskSparkInfrastructureSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkInfrastructureSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cd5036ab5c64df09c703929d0aecec0fdaf746b331085dc25838b3fd6bfaf89)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBatch")
    def put_batch(
        self,
        *,
        executors_count: typing.Optional[jsii.Number] = None,
        max_executors_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param executors_count: Total number of job executors. Executor Count should be between 2 and 100. [Default=2]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#executors_count DataplexTask#executors_count}
        :param max_executors_count: Max configurable executors. If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_executors_count DataplexTask#max_executors_count}
        '''
        value = DataplexTaskSparkInfrastructureSpecBatch(
            executors_count=executors_count, max_executors_count=max_executors_count
        )

        return typing.cast(None, jsii.invoke(self, "putBatch", [value]))

    @jsii.member(jsii_name="putContainerImage")
    def put_container_image(
        self,
        *,
        image: typing.Optional[builtins.str] = None,
        java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param image: Container image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#image DataplexTask#image}
        :param java_jars: A list of Java JARS to add to the classpath. Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#java_jars DataplexTask#java_jars}
        :param properties: Override to common configuration of open source components installed on the Dataproc cluster. The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#properties DataplexTask#properties}
        :param python_packages: A list of python packages to be installed. Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#python_packages DataplexTask#python_packages}
        '''
        value = DataplexTaskSparkInfrastructureSpecContainerImage(
            image=image,
            java_jars=java_jars,
            properties=properties,
            python_packages=python_packages,
        )

        return typing.cast(None, jsii.invoke(self, "putContainerImage", [value]))

    @jsii.member(jsii_name="putVpcNetwork")
    def put_vpc_network(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        sub_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network: The Cloud VPC network in which the job is run. By default, the Cloud VPC network named Default within the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network DataplexTask#network}
        :param network_tags: List of network tags to apply to the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network_tags DataplexTask#network_tags}
        :param sub_network: The Cloud VPC sub-network in which the job is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sub_network DataplexTask#sub_network}
        '''
        value = DataplexTaskSparkInfrastructureSpecVpcNetwork(
            network=network, network_tags=network_tags, sub_network=sub_network
        )

        return typing.cast(None, jsii.invoke(self, "putVpcNetwork", [value]))

    @jsii.member(jsii_name="resetBatch")
    def reset_batch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBatch", []))

    @jsii.member(jsii_name="resetContainerImage")
    def reset_container_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerImage", []))

    @jsii.member(jsii_name="resetVpcNetwork")
    def reset_vpc_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="batch")
    def batch(self) -> DataplexTaskSparkInfrastructureSpecBatchOutputReference:
        return typing.cast(DataplexTaskSparkInfrastructureSpecBatchOutputReference, jsii.get(self, "batch"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(
        self,
    ) -> DataplexTaskSparkInfrastructureSpecContainerImageOutputReference:
        return typing.cast(DataplexTaskSparkInfrastructureSpecContainerImageOutputReference, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetwork")
    def vpc_network(
        self,
    ) -> "DataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference":
        return typing.cast("DataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference", jsii.get(self, "vpcNetwork"))

    @builtins.property
    @jsii.member(jsii_name="batchInput")
    def batch_input(self) -> typing.Optional[DataplexTaskSparkInfrastructureSpecBatch]:
        return typing.cast(typing.Optional[DataplexTaskSparkInfrastructureSpecBatch], jsii.get(self, "batchInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(
        self,
    ) -> typing.Optional[DataplexTaskSparkInfrastructureSpecContainerImage]:
        return typing.cast(typing.Optional[DataplexTaskSparkInfrastructureSpecContainerImage], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkInput")
    def vpc_network_input(
        self,
    ) -> typing.Optional["DataplexTaskSparkInfrastructureSpecVpcNetwork"]:
        return typing.cast(typing.Optional["DataplexTaskSparkInfrastructureSpecVpcNetwork"], jsii.get(self, "vpcNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexTaskSparkInfrastructureSpec]:
        return typing.cast(typing.Optional[DataplexTaskSparkInfrastructureSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskSparkInfrastructureSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__594e7ede2414136b78a10ddc8fe11f65e592c5cb515e028ab55ce74d85afaaef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkInfrastructureSpecVpcNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "network": "network",
        "network_tags": "networkTags",
        "sub_network": "subNetwork",
    },
)
class DataplexTaskSparkInfrastructureSpecVpcNetwork:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        sub_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network: The Cloud VPC network in which the job is run. By default, the Cloud VPC network named Default within the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network DataplexTask#network}
        :param network_tags: List of network tags to apply to the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network_tags DataplexTask#network_tags}
        :param sub_network: The Cloud VPC sub-network in which the job is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sub_network DataplexTask#sub_network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980ce1848c1e08c0dfec30372660dace82c10d8482f5b5884107e9f779fac2d2)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument network_tags", value=network_tags, expected_type=type_hints["network_tags"])
            check_type(argname="argument sub_network", value=sub_network, expected_type=type_hints["sub_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network
        if network_tags is not None:
            self._values["network_tags"] = network_tags
        if sub_network is not None:
            self._values["sub_network"] = sub_network

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The Cloud VPC network in which the job is run.

        By default, the Cloud VPC network named Default within the project is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network DataplexTask#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of network tags to apply to the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#network_tags DataplexTask#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sub_network(self) -> typing.Optional[builtins.str]:
        '''The Cloud VPC sub-network in which the job is run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#sub_network DataplexTask#sub_network}
        '''
        result = self._values.get("sub_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskSparkInfrastructureSpecVpcNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e45696fc7f2ca95fe5b151d551d88ec651fdfd430da386b533a0016bfb419fa7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetNetworkTags")
    def reset_network_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkTags", []))

    @jsii.member(jsii_name="resetSubNetwork")
    def reset_sub_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubNetwork", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="networkTagsInput")
    def network_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="subNetworkInput")
    def sub_network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf53e0c966bfed0a12f37e2d6840fc0d9e46ad652f759f1b56bec00502f7a2d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed645c4d641eb9af87e4df4526775b9660d6b387b04c6010ee12b2035a47b1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subNetwork")
    def sub_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subNetwork"))

    @sub_network.setter
    def sub_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ac065aa108e92951c15a5f7c23409e79ba88d647bf41b92516db7b3b9bfc7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataplexTaskSparkInfrastructureSpecVpcNetwork]:
        return typing.cast(typing.Optional[DataplexTaskSparkInfrastructureSpecVpcNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataplexTaskSparkInfrastructureSpecVpcNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c233c046ed36d12ad7f51ec84279885953e08b2698adbfc989e672e5b049225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataplexTaskSparkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskSparkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a610144ea420864b6f10039c5126041c77bbb4109daf58571189f18324d61f9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfrastructureSpec")
    def put_infrastructure_spec(
        self,
        *,
        batch: typing.Optional[typing.Union[DataplexTaskSparkInfrastructureSpecBatch, typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union[DataplexTaskSparkInfrastructureSpecContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network: typing.Optional[typing.Union[DataplexTaskSparkInfrastructureSpecVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch: batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#batch DataplexTask#batch}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#container_image DataplexTask#container_image}
        :param vpc_network: vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#vpc_network DataplexTask#vpc_network}
        '''
        value = DataplexTaskSparkInfrastructureSpec(
            batch=batch, container_image=container_image, vpc_network=vpc_network
        )

        return typing.cast(None, jsii.invoke(self, "putInfrastructureSpec", [value]))

    @jsii.member(jsii_name="resetArchiveUris")
    def reset_archive_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchiveUris", []))

    @jsii.member(jsii_name="resetFileUris")
    def reset_file_uris(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileUris", []))

    @jsii.member(jsii_name="resetInfrastructureSpec")
    def reset_infrastructure_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureSpec", []))

    @jsii.member(jsii_name="resetMainClass")
    def reset_main_class(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainClass", []))

    @jsii.member(jsii_name="resetMainJarFileUri")
    def reset_main_jar_file_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMainJarFileUri", []))

    @jsii.member(jsii_name="resetPythonScriptFile")
    def reset_python_script_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonScriptFile", []))

    @jsii.member(jsii_name="resetSqlScript")
    def reset_sql_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlScript", []))

    @jsii.member(jsii_name="resetSqlScriptFile")
    def reset_sql_script_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSqlScriptFile", []))

    @builtins.property
    @jsii.member(jsii_name="infrastructureSpec")
    def infrastructure_spec(self) -> DataplexTaskSparkInfrastructureSpecOutputReference:
        return typing.cast(DataplexTaskSparkInfrastructureSpecOutputReference, jsii.get(self, "infrastructureSpec"))

    @builtins.property
    @jsii.member(jsii_name="archiveUrisInput")
    def archive_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "archiveUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="fileUrisInput")
    def file_uris_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fileUrisInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureSpecInput")
    def infrastructure_spec_input(
        self,
    ) -> typing.Optional[DataplexTaskSparkInfrastructureSpec]:
        return typing.cast(typing.Optional[DataplexTaskSparkInfrastructureSpec], jsii.get(self, "infrastructureSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="mainClassInput")
    def main_class_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainClassInput"))

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUriInput")
    def main_jar_file_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mainJarFileUriInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonScriptFileInput")
    def python_script_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pythonScriptFileInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlScriptFileInput")
    def sql_script_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlScriptFileInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlScriptInput")
    def sql_script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlScriptInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveUris")
    def archive_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "archiveUris"))

    @archive_uris.setter
    def archive_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b6b7ea34b7a00bcc043f33f4e2dd5b141001be2eddd8418e3db553edab0df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d128400f48ad62b15441ec6223967a89fd46e4c6451fe7467de4178d28b54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a19bc23efcf34e1d1d202ab411cb88658b6e3872d4269fed20d0167d314609a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af5d7fabd12048826864da6d4b1eb8b576458d2de25c52c0a25b5f56af2d6ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonScriptFile")
    def python_script_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonScriptFile"))

    @python_script_file.setter
    def python_script_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5faceec35b410599b912a49fab4c6281570622ddfbcf5938b43024bfd3b6bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonScriptFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlScript")
    def sql_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlScript"))

    @sql_script.setter
    def sql_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a33a0cf41c33edbf1131ccdb54d3f8db061f2c0682ec9a079d704109559927f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlScriptFile")
    def sql_script_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlScriptFile"))

    @sql_script_file.setter
    def sql_script_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96cded50ad1716550573ecf31db6313e652397aca6044ce46da0abb9c7803009)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlScriptFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexTaskSpark]:
        return typing.cast(typing.Optional[DataplexTaskSpark], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexTaskSpark]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d813d33ec280caeb0e43606d49c4da99b0bd47d1f2ff650f9dc7df776cd9cdb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DataplexTaskTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#create DataplexTask#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#delete DataplexTask#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#update DataplexTask#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506d00659bcea6a54bd56b2c15882e57b48e8038df2ecf34927fc94993896dd7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#create DataplexTask#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#delete DataplexTask#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#update DataplexTask#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66618b7de564a95a9fdb432e2c7b114bc50afbd008e1e876df2d1ff323907680)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2200813787c1bf8fbd2811f2950b62db8e266b8f002f3944c303023e5a0ab87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfb8551d2a114a9a402e7d67ecda99ce478efb9d86a1c65ac1f081301b2f532)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e71fb8ea96397e02ddfad217d9cbf3c26cfa89105957556e998bf874413d78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexTaskTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexTaskTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexTaskTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f718558ea3051dab97999bd597416fff7d1c215c5b6ffc60af4d067d78dd8c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskTriggerSpec",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "disabled": "disabled",
        "max_retries": "maxRetries",
        "schedule": "schedule",
        "start_time": "startTime",
    },
)
class DataplexTaskTriggerSpec:
    def __init__(
        self,
        *,
        type: builtins.str,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        schedule: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Trigger type of the user-specified Task Possible values: ["ON_DEMAND", "RECURRING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#type DataplexTask#type}
        :param disabled: Prevent the task from executing. This does not cancel already running tasks. It is intended to temporarily disable RECURRING tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#disabled DataplexTask#disabled}
        :param max_retries: Number of retry attempts before aborting. Set to zero to never attempt to retry a failed task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_retries DataplexTask#max_retries}
        :param schedule: Cron schedule (https://en.wikipedia.org/wiki/Cron) for running tasks periodically. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: 'CRON_TZ=${IANA_TIME_ZONE}' or 'TZ=${IANA_TIME_ZONE}'. The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, CRON_TZ=America/New_York 1 * * * *, or TZ=America/New_York 1 * * * *. This field is required for RECURRING tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#schedule DataplexTask#schedule}
        :param start_time: The first run of the task will be after this time. If not specified, the task will run shortly after being submitted if ON_DEMAND and based on the schedule if RECURRING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#start_time DataplexTask#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb15fd395531d1d4da3373c7c4ecb2f02f3e800454ada35072e333fdf3176c70)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if disabled is not None:
            self._values["disabled"] = disabled
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if schedule is not None:
            self._values["schedule"] = schedule
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def type(self) -> builtins.str:
        '''Trigger type of the user-specified Task Possible values: ["ON_DEMAND", "RECURRING"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#type DataplexTask#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Prevent the task from executing.

        This does not cancel already running tasks. It is intended to temporarily disable RECURRING tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#disabled DataplexTask#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''Number of retry attempts before aborting. Set to zero to never attempt to retry a failed task.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#max_retries DataplexTask#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Cron schedule (https://en.wikipedia.org/wiki/Cron) for running tasks periodically. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: 'CRON_TZ=${IANA_TIME_ZONE}' or 'TZ=${IANA_TIME_ZONE}'. The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, CRON_TZ=America/New_York 1 * * * *, or TZ=America/New_York 1 * * * *. This field is required for RECURRING tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#schedule DataplexTask#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The first run of the task will be after this time.

        If not specified, the task will run shortly after being submitted if ON_DEMAND and based on the schedule if RECURRING.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dataplex_task#start_time DataplexTask#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataplexTaskTriggerSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataplexTaskTriggerSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dataplexTask.DataplexTaskTriggerSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c78e4443a484da191e48aa92535749bf62461a0193af505e89dc5a5e6b484088)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a3f4fed33b331667dd7a3da7847d0b102536fa5fa54e316a38c763680c5165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923d70550f653f31311f4287919aa2d21ecdb1da99575f791dbf9f1f9483ab9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72083a0572f877741fb0cf1696bd978bdc60613851c9cc8c37c55138f8cfac1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c273dfb0936e32ca73a2ce5f278ea74e414d1a8181f21978f2b69e76fc87f278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054b78195bbeb015b1f2836394ac4de8eff43c5df9c06b980e6a48c5d3776962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataplexTaskTriggerSpec]:
        return typing.cast(typing.Optional[DataplexTaskTriggerSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataplexTaskTriggerSpec]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25580da19ebbb7148d6532a1acadceef7edef2c058cd677dec05bd747a3230eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataplexTask",
    "DataplexTaskConfig",
    "DataplexTaskExecutionSpec",
    "DataplexTaskExecutionSpecOutputReference",
    "DataplexTaskExecutionStatus",
    "DataplexTaskExecutionStatusLatestJob",
    "DataplexTaskExecutionStatusLatestJobList",
    "DataplexTaskExecutionStatusLatestJobOutputReference",
    "DataplexTaskExecutionStatusList",
    "DataplexTaskExecutionStatusOutputReference",
    "DataplexTaskNotebook",
    "DataplexTaskNotebookInfrastructureSpec",
    "DataplexTaskNotebookInfrastructureSpecBatch",
    "DataplexTaskNotebookInfrastructureSpecBatchOutputReference",
    "DataplexTaskNotebookInfrastructureSpecContainerImage",
    "DataplexTaskNotebookInfrastructureSpecContainerImageOutputReference",
    "DataplexTaskNotebookInfrastructureSpecOutputReference",
    "DataplexTaskNotebookInfrastructureSpecVpcNetwork",
    "DataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference",
    "DataplexTaskNotebookOutputReference",
    "DataplexTaskSpark",
    "DataplexTaskSparkInfrastructureSpec",
    "DataplexTaskSparkInfrastructureSpecBatch",
    "DataplexTaskSparkInfrastructureSpecBatchOutputReference",
    "DataplexTaskSparkInfrastructureSpecContainerImage",
    "DataplexTaskSparkInfrastructureSpecContainerImageOutputReference",
    "DataplexTaskSparkInfrastructureSpecOutputReference",
    "DataplexTaskSparkInfrastructureSpecVpcNetwork",
    "DataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference",
    "DataplexTaskSparkOutputReference",
    "DataplexTaskTimeouts",
    "DataplexTaskTimeoutsOutputReference",
    "DataplexTaskTriggerSpec",
    "DataplexTaskTriggerSpecOutputReference",
]

publication.publish()

def _typecheckingstub__c532711edf94d7290439d75a50ee9ef1ea94feeec8d5de1d203b4a4a4d2bc73a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    execution_spec: typing.Union[DataplexTaskExecutionSpec, typing.Dict[builtins.str, typing.Any]],
    trigger_spec: typing.Union[DataplexTaskTriggerSpec, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lake: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    notebook: typing.Optional[typing.Union[DataplexTaskNotebook, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    spark: typing.Optional[typing.Union[DataplexTaskSpark, typing.Dict[builtins.str, typing.Any]]] = None,
    task_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexTaskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__40aac603017e1dfbbd3b06433851128239057b99e7873de1c736a4d21809d2d5(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f29a20c13cf74f2eb7e10d668176b6c6e4f52cf6904375aae76bada1cde99a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8bba46f88c98739f1a17cbddbfd2ad33a0c36b063cfaefc5ad30353a729e96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0698d6f08f960a2bd0bac5da2d50f99dd30b9c881d0e8a68c52d225aa861ad86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aab7b41a0157adb0ae102bbf4c4cffb5664c22ad33736d45991a728431f5f42(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f5f0ff50255230857c48e92b87fbb4581007d711a8c8bd1b35f2c1811ed138(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38556b42ae5438c0281839052ee55aafcbf00e03cedde19cdbf5da1fd1c97c24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76394337c5f5a9f75fba639a4e3de771bf09f41e17a625529807b37956d8c2f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f549423364419434ee2bb75c178a482e799807f5013c22ea41d6ed7416c75b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88bd4c457e15ac7951ff223f6c7625700f77ca31cdf951e28737e9ad858bca4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    execution_spec: typing.Union[DataplexTaskExecutionSpec, typing.Dict[builtins.str, typing.Any]],
    trigger_spec: typing.Union[DataplexTaskTriggerSpec, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lake: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    notebook: typing.Optional[typing.Union[DataplexTaskNotebook, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    spark: typing.Optional[typing.Union[DataplexTaskSpark, typing.Dict[builtins.str, typing.Any]]] = None,
    task_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataplexTaskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072e5ee9d2283471bfcff111a561766da94dd297d16c28cf8fffb1a281a531a0(
    *,
    service_account: builtins.str,
    args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    max_job_execution_lifetime: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7855fd9957ee882d80a776e7ff0751955751dfd2a82e65349bb0fb5dc54d6336(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3808b18bbfb0e0663ca3e7c2df5444d9683577970354abb54f5dd06cd907558a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571adedba2e45a5c0ef71ab9953bf3326b812b411e838773b7e4f6d843a951e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76787775b886adb241793e9adc910b7d05f39099edff7281871cc7b00188a9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4a038e49de6605dc59867eb4b3860c91919ef643728e59d6abf226add33f93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7be0aec0fd667fe2d89937a16657ed4ababe626d7b47a40b98ed9ea00da039e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7521f1458d7eac57d509338d3122eaa50060e04a217977bdd1c06cf9d15724(
    value: typing.Optional[DataplexTaskExecutionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7180072b55f689c4437e2d26af52b6790e64c7ec404242a03354834ccb4af6df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc68110fb95d24c86345ed8d2303eb734d99a18aee292e0256a6f46b17ab2cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b303e8683a8beb673a9bbee4ed71a2211551657defc145596f9b192c5a6c2d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__981074338a294d3cc6435e493bb1ed99825101bc64424cd71b9dbdca94c517fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abee913e94bb78c3f7487fa66caba59fd69e04763d97ab652671c120c71a0df2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e92fcaaa74396434ada188a9416eec6173763698cb3e2023c3fa0eb468f381(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6b5d1ca6e9fc530d11c59e7dacd30fc3a922df4998cc9f7e73588892fe52b7(
    value: typing.Optional[DataplexTaskExecutionStatusLatestJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ab26d1226ec63c814bca0b97f0eec92623187652480ceb14cbe3427d8ade9ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7586fdd7eee120b86d44d3be350fb45e1282433e7b4b14ff7c687e4fb738ff54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbe87607afbc21cbe3d18aa05d2395df3953c982a94b06a4398e7d699a7ffdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102bf2e1b49923de717d8842766de361ae7d30c1bc3597e3450eb0b0c860f631(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47c6ebaa6095c651a8e4b2a144a1655f3b171340b13c277e647c0a394f039c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a746e0b0a024a50301fbf6d4d36fb0627ebe085cbfb56e912ef2b2b063d45b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3519de2758e1321ae430de1146c70ff0bdc9186f553ffe813a92c077711be4(
    value: typing.Optional[DataplexTaskExecutionStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021238a5cc76a058e53bb187a2debd40905a27f35ef165e438170fcd6b3a9061(
    *,
    notebook: builtins.str,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrastructure_spec: typing.Optional[typing.Union[DataplexTaskNotebookInfrastructureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a983c216c5819dbf14556d958e97ff3df63f1911f8f30a8de453755b44a02c(
    *,
    batch: typing.Optional[typing.Union[DataplexTaskNotebookInfrastructureSpecBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    container_image: typing.Optional[typing.Union[DataplexTaskNotebookInfrastructureSpecContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_network: typing.Optional[typing.Union[DataplexTaskNotebookInfrastructureSpecVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6134fbcdc2ef10c7510c11edd48a048d95a947db7d2594af43066cdea80159e(
    *,
    executors_count: typing.Optional[jsii.Number] = None,
    max_executors_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26800b75d60f8b97bfa7e98fda51d5e9426d86b25e142dc7c7464d5801e8a8ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37dff5a19774caf8f4743e40b67a22fadeef1082f74e698db3c7e441b8db97c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aedcb68336405641786830b3f7c2f617a45bab7fb2b8d8ef94df8c85fefa3cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72afac978f06b3919d7f2a9c3155d157c4d0b2d7bfb41cb5aeda26e07a936dfa(
    value: typing.Optional[DataplexTaskNotebookInfrastructureSpecBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b558456921b12618929a35e630ad17eee7cbd9d77b7a4358352ad03902200c35(
    *,
    image: typing.Optional[builtins.str] = None,
    java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a661bef24e01565e7a200451a0dc52004d00f1a56f84446057cb03b405af8ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b68c83c8f0136c3af5f879d107b0ab9f5b4eef4f1c10c1b84221cc0927a264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413126f4455d7029077556576e70177ef9ce16946df620aa216d365c928e2ad0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b693c454e65591aed40eff85b794d21b31fe1849d443746531bde11b90268b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444a1066d5c6038e45f8f360cb92b8d8aa65dc34b14004aad93e3bdab01a58a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8dd6d86ce08350884955936987958d0f1509ebda9ea32de309099883498efc(
    value: typing.Optional[DataplexTaskNotebookInfrastructureSpecContainerImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eca2140776fedf00d922a869ebf62848a2fed8705dbc9e7a85c2d42cb28f6dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24aa7ed6bf49a5aa59b3fc401cd2ac13564b38bf92e6300dcb2ff7bd3e185ca2(
    value: typing.Optional[DataplexTaskNotebookInfrastructureSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362f079490d66b0974028b3843a844458f32ad38c5c90ac975122e0ab9bcde79(
    *,
    network: typing.Optional[builtins.str] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    sub_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__033f679003447b8fbfd55d67489270c841daca809bf9e606fce74b3c9fd158ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38456b9a6bb8a2bf44dd929b8b32f4d2143879055e1aa2e107dbd3c0dd918a68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4bbca56b46f20d5cc14815853ee85d74e74c09eb59818c9566765331f460f56(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90b6092ec74b88dc58c6ea801ff956f284dd124a1efef67353c0964132d5358(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475da08c25daa8e92b5e4ef17c8f2473ee213ca9137be02aeb273a94d17874d6(
    value: typing.Optional[DataplexTaskNotebookInfrastructureSpecVpcNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588ab522036016d1004c8ca7f5852bd34cd534d677d58016c0e4893c0ab79325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d24b6f4e561ca48ff00ec92eef43cc3db1bc343e238c17da42f7cdd99a478b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c07b4b16a3a2fcf841714ba58e6d075d56dbf6fc03307e8b6e0f1564fb0ae24(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3012d11ad9bf5fdfcd51ac9dc7da6467cec8fa5f6095697149fe34ba0ae9b784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0815c4d01df785e253a97e145f0576cd857c0e12945edf6470251db103bfc8(
    value: typing.Optional[DataplexTaskNotebook],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15278a948bd7ff153d1e52a4a978b8b513ad940341ac7d8135bc5395205613b(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrastructure_spec: typing.Optional[typing.Union[DataplexTaskSparkInfrastructureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    main_class: typing.Optional[builtins.str] = None,
    main_jar_file_uri: typing.Optional[builtins.str] = None,
    python_script_file: typing.Optional[builtins.str] = None,
    sql_script: typing.Optional[builtins.str] = None,
    sql_script_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721908c8415b261c5f2f6e152bfe9f02965865fc3d7641e6314ebf5444ebc153(
    *,
    batch: typing.Optional[typing.Union[DataplexTaskSparkInfrastructureSpecBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    container_image: typing.Optional[typing.Union[DataplexTaskSparkInfrastructureSpecContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_network: typing.Optional[typing.Union[DataplexTaskSparkInfrastructureSpecVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48f9139f91239561cb18212a077f0090fe05ab8cd431d2c970c7e53910bd487(
    *,
    executors_count: typing.Optional[jsii.Number] = None,
    max_executors_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12c740366e9ca4d1d237a1ac2336169492a594ad8687bf432e62dcb946768a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b809c656b96d0917eb2f2a759ae8de6fc698a34a10e11403eb12faa5203504c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99e068c97ee25d120bd9e7ce8c5c529e3afc22fca920b6d08e333b6a6bce8b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a11ec10a75b24dc76d8a3d6fac69eddd85c55c3f94c71c3b302bada8df2dda4(
    value: typing.Optional[DataplexTaskSparkInfrastructureSpecBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fedeb09bc118cb100005b8444c2ba6e726ca98bd9a33d29a4e9b7f28b044184(
    *,
    image: typing.Optional[builtins.str] = None,
    java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7229e4bfebdbf008cdef618d4f66f82d989d6060a365932a44968091f79b3b44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b8d51089c55ae1f02fcb08c11a60bc834c16584a811fdb98385a5b623fa070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113ee21bac4fea0f8d1452f6fe7c8e57f9a91e5c3ad753c5fd322d58f74176d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db2efabe28804897f2951a158e4a41bc17613323e505a0b8baaed70b7238ac5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e9b85d09da41067079f7c975a7babac7577d05820ffe85a8e482af7c1f0f87e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b5f09c5c8ab664ba6758b0cf2459fccf8ae07a367d643b1495164c3a334d88(
    value: typing.Optional[DataplexTaskSparkInfrastructureSpecContainerImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd5036ab5c64df09c703929d0aecec0fdaf746b331085dc25838b3fd6bfaf89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__594e7ede2414136b78a10ddc8fe11f65e592c5cb515e028ab55ce74d85afaaef(
    value: typing.Optional[DataplexTaskSparkInfrastructureSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980ce1848c1e08c0dfec30372660dace82c10d8482f5b5884107e9f779fac2d2(
    *,
    network: typing.Optional[builtins.str] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    sub_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45696fc7f2ca95fe5b151d551d88ec651fdfd430da386b533a0016bfb419fa7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf53e0c966bfed0a12f37e2d6840fc0d9e46ad652f759f1b56bec00502f7a2d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed645c4d641eb9af87e4df4526775b9660d6b387b04c6010ee12b2035a47b1ff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ac065aa108e92951c15a5f7c23409e79ba88d647bf41b92516db7b3b9bfc7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c233c046ed36d12ad7f51ec84279885953e08b2698adbfc989e672e5b049225(
    value: typing.Optional[DataplexTaskSparkInfrastructureSpecVpcNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a610144ea420864b6f10039c5126041c77bbb4109daf58571189f18324d61f9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b6b7ea34b7a00bcc043f33f4e2dd5b141001be2eddd8418e3db553edab0df2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d128400f48ad62b15441ec6223967a89fd46e4c6451fe7467de4178d28b54b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a19bc23efcf34e1d1d202ab411cb88658b6e3872d4269fed20d0167d314609a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af5d7fabd12048826864da6d4b1eb8b576458d2de25c52c0a25b5f56af2d6ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5faceec35b410599b912a49fab4c6281570622ddfbcf5938b43024bfd3b6bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a33a0cf41c33edbf1131ccdb54d3f8db061f2c0682ec9a079d704109559927f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96cded50ad1716550573ecf31db6313e652397aca6044ce46da0abb9c7803009(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d813d33ec280caeb0e43606d49c4da99b0bd47d1f2ff650f9dc7df776cd9cdb7(
    value: typing.Optional[DataplexTaskSpark],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506d00659bcea6a54bd56b2c15882e57b48e8038df2ecf34927fc94993896dd7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66618b7de564a95a9fdb432e2c7b114bc50afbd008e1e876df2d1ff323907680(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2200813787c1bf8fbd2811f2950b62db8e266b8f002f3944c303023e5a0ab87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfb8551d2a114a9a402e7d67ecda99ce478efb9d86a1c65ac1f081301b2f532(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e71fb8ea96397e02ddfad217d9cbf3c26cfa89105957556e998bf874413d78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f718558ea3051dab97999bd597416fff7d1c215c5b6ffc60af4d067d78dd8c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DataplexTaskTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb15fd395531d1d4da3373c7c4ecb2f02f3e800454ada35072e333fdf3176c70(
    *,
    type: builtins.str,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    schedule: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78e4443a484da191e48aa92535749bf62461a0193af505e89dc5a5e6b484088(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a3f4fed33b331667dd7a3da7847d0b102536fa5fa54e316a38c763680c5165(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923d70550f653f31311f4287919aa2d21ecdb1da99575f791dbf9f1f9483ab9a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72083a0572f877741fb0cf1696bd978bdc60613851c9cc8c37c55138f8cfac1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c273dfb0936e32ca73a2ce5f278ea74e414d1a8181f21978f2b69e76fc87f278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054b78195bbeb015b1f2836394ac4de8eff43c5df9c06b980e6a48c5d3776962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25580da19ebbb7148d6532a1acadceef7edef2c058cd677dec05bd747a3230eb(
    value: typing.Optional[DataplexTaskTriggerSpec],
) -> None:
    """Type checking stubs"""
    pass

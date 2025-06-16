r'''
# `google_dataplex_task`

Refer to the Terraform Registry for docs: [`google_dataplex_task`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task).
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


class GoogleDataplexTask(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTask",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task google_dataplex_task}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        execution_spec: typing.Union["GoogleDataplexTaskExecutionSpec", typing.Dict[builtins.str, typing.Any]],
        trigger_spec: typing.Union["GoogleDataplexTaskTriggerSpec", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lake: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notebook: typing.Optional[typing.Union["GoogleDataplexTaskNotebook", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        spark: typing.Optional[typing.Union["GoogleDataplexTaskSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        task_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataplexTaskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task google_dataplex_task} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param execution_spec: execution_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#execution_spec GoogleDataplexTask#execution_spec}
        :param trigger_spec: trigger_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#trigger_spec GoogleDataplexTask#trigger_spec}
        :param description: User-provided description of the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#description GoogleDataplexTask#description}
        :param display_name: User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#display_name GoogleDataplexTask#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#id GoogleDataplexTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the task. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#labels GoogleDataplexTask#labels}
        :param lake: The lake in which the task will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#lake GoogleDataplexTask#lake}
        :param location: The location in which the task will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#location GoogleDataplexTask#location}
        :param notebook: notebook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#notebook GoogleDataplexTask#notebook}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#project GoogleDataplexTask#project}.
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#spark GoogleDataplexTask#spark}
        :param task_id: The task Id of the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#task_id GoogleDataplexTask#task_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#timeouts GoogleDataplexTask#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a273fb9f44daefdb3bd53f1b3faffb0e8a65bfb2af31ca7b784f77b0b44610)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleDataplexTaskConfig(
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
        '''Generates CDKTF code for importing a GoogleDataplexTask resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleDataplexTask to import.
        :param import_from_id: The id of the existing GoogleDataplexTask that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleDataplexTask to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0bb8115ddf92681504bc40d195bc75dc26a3b470d9e3d498f6e58adf48c3d52)
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
        :param service_account: Service account to use to execute a task. If not provided, the default Compute service account for the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#service_account GoogleDataplexTask#service_account}
        :param args: The arguments to pass to the task. The args can use placeholders of the format ${placeholder} as part of key/value string. These will be interpolated before passing the args to the driver. Currently supported placeholders: - ${taskId} - ${job_time} To pass positional args, set the key as TASK_ARGS. The value should be a comma-separated string of all the positional arguments. To use a delimiter other than comma, refer to https://cloud.google.com/sdk/gcloud/reference/topic/escaping. In case of other keys being present in the args, then TASK_ARGS will be passed as the last argument. An object containing a list of 'key': value pairs. Example: { 'name': 'wrench', 'mass': '1.3kg', 'count': '3' }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#args GoogleDataplexTask#args}
        :param kms_key: The Cloud KMS key to use for encryption, of the form: projects/{project_number}/locations/{locationId}/keyRings/{key-ring-name}/cryptoKeys/{key-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#kms_key GoogleDataplexTask#kms_key}
        :param max_job_execution_lifetime: The maximum duration after which the job execution is expired. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_job_execution_lifetime GoogleDataplexTask#max_job_execution_lifetime}
        :param project: The project in which jobs are run. By default, the project containing the Lake is used. If a project is provided, the ExecutionSpec.service_account must belong to this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#project GoogleDataplexTask#project}
        '''
        value = GoogleDataplexTaskExecutionSpec(
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
        infrastructure_spec: typing.Optional[typing.Union["GoogleDataplexTaskNotebookInfrastructureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param notebook: Path to input notebook. This can be the Cloud Storage URI of the notebook file or the path to a Notebook Content. The execution args are accessible as environment variables (TASK_key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#notebook GoogleDataplexTask#notebook}
        :param archive_uris: Cloud Storage URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#archive_uris GoogleDataplexTask#archive_uris}
        :param file_uris: Cloud Storage URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#file_uris GoogleDataplexTask#file_uris}
        :param infrastructure_spec: infrastructure_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#infrastructure_spec GoogleDataplexTask#infrastructure_spec}
        '''
        value = GoogleDataplexTaskNotebook(
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
        infrastructure_spec: typing.Optional[typing.Union["GoogleDataplexTaskSparkInfrastructureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        python_script_file: typing.Optional[builtins.str] = None,
        sql_script: typing.Optional[builtins.str] = None,
        sql_script_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: Cloud Storage URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#archive_uris GoogleDataplexTask#archive_uris}
        :param file_uris: Cloud Storage URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#file_uris GoogleDataplexTask#file_uris}
        :param infrastructure_spec: infrastructure_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#infrastructure_spec GoogleDataplexTask#infrastructure_spec}
        :param main_class: The name of the driver's main class. The jar file that contains the class must be in the default CLASSPATH or specified in jar_file_uris. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#main_class GoogleDataplexTask#main_class}
        :param main_jar_file_uri: The Cloud Storage URI of the jar file that contains the main class. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#main_jar_file_uri GoogleDataplexTask#main_jar_file_uri}
        :param python_script_file: The Gcloud Storage URI of the main Python file to use as the driver. Must be a .py file. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_script_file GoogleDataplexTask#python_script_file}
        :param sql_script: The query text. The execution args are used to declare a set of script variables (set key='value';). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sql_script GoogleDataplexTask#sql_script}
        :param sql_script_file: A reference to a query file. This can be the Cloud Storage URI of the query file or it can the path to a SqlScript Content. The execution args are used to declare a set of script variables (set key='value';). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sql_script_file GoogleDataplexTask#sql_script_file}
        '''
        value = GoogleDataplexTaskSpark(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#create GoogleDataplexTask#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#delete GoogleDataplexTask#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#update GoogleDataplexTask#update}.
        '''
        value = GoogleDataplexTaskTimeouts(create=create, delete=delete, update=update)

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
        :param type: Trigger type of the user-specified Task Possible values: ["ON_DEMAND", "RECURRING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#type GoogleDataplexTask#type}
        :param disabled: Prevent the task from executing. This does not cancel already running tasks. It is intended to temporarily disable RECURRING tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#disabled GoogleDataplexTask#disabled}
        :param max_retries: Number of retry attempts before aborting. Set to zero to never attempt to retry a failed task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_retries GoogleDataplexTask#max_retries}
        :param schedule: Cron schedule (https://en.wikipedia.org/wiki/Cron) for running tasks periodically. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: 'CRON_TZ=${IANA_TIME_ZONE}' or 'TZ=${IANA_TIME_ZONE}'. The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, CRON_TZ=America/New_York 1 * * * *, or TZ=America/New_York 1 * * * *. This field is required for RECURRING tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#schedule GoogleDataplexTask#schedule}
        :param start_time: The first run of the task will be after this time. If not specified, the task will run shortly after being submitted if ON_DEMAND and based on the schedule if RECURRING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#start_time GoogleDataplexTask#start_time}
        '''
        value = GoogleDataplexTaskTriggerSpec(
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
    def execution_spec(self) -> "GoogleDataplexTaskExecutionSpecOutputReference":
        return typing.cast("GoogleDataplexTaskExecutionSpecOutputReference", jsii.get(self, "executionSpec"))

    @builtins.property
    @jsii.member(jsii_name="executionStatus")
    def execution_status(self) -> "GoogleDataplexTaskExecutionStatusList":
        return typing.cast("GoogleDataplexTaskExecutionStatusList", jsii.get(self, "executionStatus"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="notebook")
    def notebook(self) -> "GoogleDataplexTaskNotebookOutputReference":
        return typing.cast("GoogleDataplexTaskNotebookOutputReference", jsii.get(self, "notebook"))

    @builtins.property
    @jsii.member(jsii_name="spark")
    def spark(self) -> "GoogleDataplexTaskSparkOutputReference":
        return typing.cast("GoogleDataplexTaskSparkOutputReference", jsii.get(self, "spark"))

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
    def timeouts(self) -> "GoogleDataplexTaskTimeoutsOutputReference":
        return typing.cast("GoogleDataplexTaskTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="triggerSpec")
    def trigger_spec(self) -> "GoogleDataplexTaskTriggerSpecOutputReference":
        return typing.cast("GoogleDataplexTaskTriggerSpecOutputReference", jsii.get(self, "triggerSpec"))

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
    def execution_spec_input(
        self,
    ) -> typing.Optional["GoogleDataplexTaskExecutionSpec"]:
        return typing.cast(typing.Optional["GoogleDataplexTaskExecutionSpec"], jsii.get(self, "executionSpecInput"))

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
    def notebook_input(self) -> typing.Optional["GoogleDataplexTaskNotebook"]:
        return typing.cast(typing.Optional["GoogleDataplexTaskNotebook"], jsii.get(self, "notebookInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="sparkInput")
    def spark_input(self) -> typing.Optional["GoogleDataplexTaskSpark"]:
        return typing.cast(typing.Optional["GoogleDataplexTaskSpark"], jsii.get(self, "sparkInput"))

    @builtins.property
    @jsii.member(jsii_name="taskIdInput")
    def task_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "taskIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataplexTaskTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleDataplexTaskTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerSpecInput")
    def trigger_spec_input(self) -> typing.Optional["GoogleDataplexTaskTriggerSpec"]:
        return typing.cast(typing.Optional["GoogleDataplexTaskTriggerSpec"], jsii.get(self, "triggerSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699b2162700fe89aae17d20c21b1797ff25a5f409a1c02991a18bd0968d64d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f06509a6ff963e29bb481248ee63462e1f6511bf9a2b27b4181d0f76857f66a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240319c78eea3c4de7dfa7747b4e4c353f89cb4aa2aa35835fef7969e33315d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0db3c2d52325e6cd2814561d05ae32ebc5584ee6c4747d9546edeb78e8aaca75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="lake")
    def lake(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lake"))

    @lake.setter
    def lake(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433f8b8a3d5e3346b9c37681755d443dc595a98e2906f34cd2337bebc27ffd0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lake", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a96a1876d2e9e4e95f8b80021e15b6ca09d5ad3c5a541990b28e7163d2764f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb409c2bb9da1f483c23e0829019e4f98e2372b6e45857657c3eee097e43bf60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskId")
    def task_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskId"))

    @task_id.setter
    def task_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539e127946b5b0a13e17a16694f4df10be6f1275cd4f0abcea13b4726a025669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskConfig",
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
class GoogleDataplexTaskConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        execution_spec: typing.Union["GoogleDataplexTaskExecutionSpec", typing.Dict[builtins.str, typing.Any]],
        trigger_spec: typing.Union["GoogleDataplexTaskTriggerSpec", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        lake: typing.Optional[builtins.str] = None,
        location: typing.Optional[builtins.str] = None,
        notebook: typing.Optional[typing.Union["GoogleDataplexTaskNotebook", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        spark: typing.Optional[typing.Union["GoogleDataplexTaskSpark", typing.Dict[builtins.str, typing.Any]]] = None,
        task_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleDataplexTaskTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param execution_spec: execution_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#execution_spec GoogleDataplexTask#execution_spec}
        :param trigger_spec: trigger_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#trigger_spec GoogleDataplexTask#trigger_spec}
        :param description: User-provided description of the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#description GoogleDataplexTask#description}
        :param display_name: User friendly display name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#display_name GoogleDataplexTask#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#id GoogleDataplexTask#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: User-defined labels for the task. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#labels GoogleDataplexTask#labels}
        :param lake: The lake in which the task will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#lake GoogleDataplexTask#lake}
        :param location: The location in which the task will be created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#location GoogleDataplexTask#location}
        :param notebook: notebook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#notebook GoogleDataplexTask#notebook}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#project GoogleDataplexTask#project}.
        :param spark: spark block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#spark GoogleDataplexTask#spark}
        :param task_id: The task Id of the task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#task_id GoogleDataplexTask#task_id}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#timeouts GoogleDataplexTask#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(execution_spec, dict):
            execution_spec = GoogleDataplexTaskExecutionSpec(**execution_spec)
        if isinstance(trigger_spec, dict):
            trigger_spec = GoogleDataplexTaskTriggerSpec(**trigger_spec)
        if isinstance(notebook, dict):
            notebook = GoogleDataplexTaskNotebook(**notebook)
        if isinstance(spark, dict):
            spark = GoogleDataplexTaskSpark(**spark)
        if isinstance(timeouts, dict):
            timeouts = GoogleDataplexTaskTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7b5ffc5a9bf606a5074cdc5dea868b2fd5238fabdb6abf490d721b75b0e7e8)
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
    def execution_spec(self) -> "GoogleDataplexTaskExecutionSpec":
        '''execution_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#execution_spec GoogleDataplexTask#execution_spec}
        '''
        result = self._values.get("execution_spec")
        assert result is not None, "Required property 'execution_spec' is missing"
        return typing.cast("GoogleDataplexTaskExecutionSpec", result)

    @builtins.property
    def trigger_spec(self) -> "GoogleDataplexTaskTriggerSpec":
        '''trigger_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#trigger_spec GoogleDataplexTask#trigger_spec}
        '''
        result = self._values.get("trigger_spec")
        assert result is not None, "Required property 'trigger_spec' is missing"
        return typing.cast("GoogleDataplexTaskTriggerSpec", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description of the task.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#description GoogleDataplexTask#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''User friendly display name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#display_name GoogleDataplexTask#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#id GoogleDataplexTask#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#labels GoogleDataplexTask#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def lake(self) -> typing.Optional[builtins.str]:
        '''The lake in which the task will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#lake GoogleDataplexTask#lake}
        '''
        result = self._values.get("lake")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location in which the task will be created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#location GoogleDataplexTask#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notebook(self) -> typing.Optional["GoogleDataplexTaskNotebook"]:
        '''notebook block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#notebook GoogleDataplexTask#notebook}
        '''
        result = self._values.get("notebook")
        return typing.cast(typing.Optional["GoogleDataplexTaskNotebook"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#project GoogleDataplexTask#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark(self) -> typing.Optional["GoogleDataplexTaskSpark"]:
        '''spark block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#spark GoogleDataplexTask#spark}
        '''
        result = self._values.get("spark")
        return typing.cast(typing.Optional["GoogleDataplexTaskSpark"], result)

    @builtins.property
    def task_id(self) -> typing.Optional[builtins.str]:
        '''The task Id of the task.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#task_id GoogleDataplexTask#task_id}
        '''
        result = self._values.get("task_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleDataplexTaskTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#timeouts GoogleDataplexTask#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleDataplexTaskTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskExecutionSpec",
    jsii_struct_bases=[],
    name_mapping={
        "service_account": "serviceAccount",
        "args": "args",
        "kms_key": "kmsKey",
        "max_job_execution_lifetime": "maxJobExecutionLifetime",
        "project": "project",
    },
)
class GoogleDataplexTaskExecutionSpec:
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
        :param service_account: Service account to use to execute a task. If not provided, the default Compute service account for the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#service_account GoogleDataplexTask#service_account}
        :param args: The arguments to pass to the task. The args can use placeholders of the format ${placeholder} as part of key/value string. These will be interpolated before passing the args to the driver. Currently supported placeholders: - ${taskId} - ${job_time} To pass positional args, set the key as TASK_ARGS. The value should be a comma-separated string of all the positional arguments. To use a delimiter other than comma, refer to https://cloud.google.com/sdk/gcloud/reference/topic/escaping. In case of other keys being present in the args, then TASK_ARGS will be passed as the last argument. An object containing a list of 'key': value pairs. Example: { 'name': 'wrench', 'mass': '1.3kg', 'count': '3' }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#args GoogleDataplexTask#args}
        :param kms_key: The Cloud KMS key to use for encryption, of the form: projects/{project_number}/locations/{locationId}/keyRings/{key-ring-name}/cryptoKeys/{key-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#kms_key GoogleDataplexTask#kms_key}
        :param max_job_execution_lifetime: The maximum duration after which the job execution is expired. A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_job_execution_lifetime GoogleDataplexTask#max_job_execution_lifetime}
        :param project: The project in which jobs are run. By default, the project containing the Lake is used. If a project is provided, the ExecutionSpec.service_account must belong to this project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#project GoogleDataplexTask#project}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84181f3291584320601dea4f71e61ccd7fbd9d27c16a5fab04b6df635bd2841)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#service_account GoogleDataplexTask#service_account}
        '''
        result = self._values.get("service_account")
        assert result is not None, "Required property 'service_account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The arguments to pass to the task.

        The args can use placeholders of the format ${placeholder} as part of key/value string. These will be interpolated before passing the args to the driver. Currently supported placeholders: - ${taskId} - ${job_time} To pass positional args, set the key as TASK_ARGS. The value should be a comma-separated string of all the positional arguments. To use a delimiter other than comma, refer to https://cloud.google.com/sdk/gcloud/reference/topic/escaping. In case of other keys being present in the args, then TASK_ARGS will be passed as the last argument. An object containing a list of 'key': value pairs. Example: { 'name': 'wrench', 'mass': '1.3kg', 'count': '3' }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#args GoogleDataplexTask#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The Cloud KMS key to use for encryption, of the form: projects/{project_number}/locations/{locationId}/keyRings/{key-ring-name}/cryptoKeys/{key-name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#kms_key GoogleDataplexTask#kms_key}
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_job_execution_lifetime(self) -> typing.Optional[builtins.str]:
        '''The maximum duration after which the job execution is expired.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: '3.5s'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_job_execution_lifetime GoogleDataplexTask#max_job_execution_lifetime}
        '''
        result = self._values.get("max_job_execution_lifetime")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''The project in which jobs are run.

        By default, the project containing the Lake is used. If a project is provided, the ExecutionSpec.service_account must belong to this project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#project GoogleDataplexTask#project}
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskExecutionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskExecutionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskExecutionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8bbb3aedb3b3813de300f059f3ddec972aae18a782a3230e16a219d7d529741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ce1e9c6c1ecf4ec2c1b8fe09e4f4f5e53dbf62339054fd9701a6a41e737a7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="kmsKey")
    def kms_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKey"))

    @kms_key.setter
    def kms_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff19bc4e2ac62f2197bc13bcef6ee365db4ef4322ae539ca2d77e6e2ac70553c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxJobExecutionLifetime")
    def max_job_execution_lifetime(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxJobExecutionLifetime"))

    @max_job_execution_lifetime.setter
    def max_job_execution_lifetime(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462708e5355952ebd0e93d4c06bc8c54b4480f1a38fef9ab759a48ae2af66922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxJobExecutionLifetime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b339fcf8d58917115d8237f136bcd69bbf03e33446c672e0d23545ea7ca35a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5914a8a6f8e16a9ed884a75c3e55a4e4a00ae0148976f791b79036b3d4b61eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataplexTaskExecutionSpec]:
        return typing.cast(typing.Optional[GoogleDataplexTaskExecutionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskExecutionSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25d1b464008fcb6f16a050cd185afdebef1a454d53d147b12481c52d76af3f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskExecutionStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataplexTaskExecutionStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskExecutionStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskExecutionStatusLatestJob",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleDataplexTaskExecutionStatusLatestJob:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskExecutionStatusLatestJob(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskExecutionStatusLatestJobList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskExecutionStatusLatestJobList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71033b0226cd192f2b054742cebf3a141884e30957636b0b8d6a36373b71bbfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataplexTaskExecutionStatusLatestJobOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48562e1922487973ca3ce54ac6a1381ae5e8a2d802c649a1a76d1e73da00fe0d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataplexTaskExecutionStatusLatestJobOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7374a8b20fd69dbca692267548b7ea048ea015c1f5aca8d1fbca21d6cfb157)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f4f75a847ffe7f854d46a6d1e18855e075a381da7aa226a50d2cbffd4ecdd11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fabc7a90f57a7667757dd11df577bfce69cc1539aaf8af78518a55c70bca5479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexTaskExecutionStatusLatestJobOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskExecutionStatusLatestJobOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__860f72ec91a63e59d085d5380463da3fc796511f59e8f33cb558b6b5add1090b)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskExecutionStatusLatestJob]:
        return typing.cast(typing.Optional[GoogleDataplexTaskExecutionStatusLatestJob], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskExecutionStatusLatestJob],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb684e3b2e3b1d63f8fb7a180a32d8969f4cab6eacdc2183a0c5a3cf72dc172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexTaskExecutionStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskExecutionStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcfa62a84503308e3a9783e4180760100aecb935fa0ba720fcb11254e5b617de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleDataplexTaskExecutionStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a67c90cfadfa8ea3fb498f18b1d51a61139028c072efe2d232fc3ee03f85f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleDataplexTaskExecutionStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__004284e349d7ffc2850a5c73c2855765ebae9a0786a4093227e306c3b52af06b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1f09ce27896c411006e27609745622a1c5c134baeb83fbca6cd4eaa8328ba35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2281ea65a45698f61ad5921db7617a1ebcb174012da7ef31b9973efd3b8b1477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexTaskExecutionStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskExecutionStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bd60f68b5a8f5abdcb2bf9748ec5102c6495d8183021768fc3aa5e45b1db915)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="latestJob")
    def latest_job(self) -> GoogleDataplexTaskExecutionStatusLatestJobList:
        return typing.cast(GoogleDataplexTaskExecutionStatusLatestJobList, jsii.get(self, "latestJob"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataplexTaskExecutionStatus]:
        return typing.cast(typing.Optional[GoogleDataplexTaskExecutionStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskExecutionStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23819704a7cabd3a1160e787556649575c4dcd8d72717e3bc0e80626b6568986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebook",
    jsii_struct_bases=[],
    name_mapping={
        "notebook": "notebook",
        "archive_uris": "archiveUris",
        "file_uris": "fileUris",
        "infrastructure_spec": "infrastructureSpec",
    },
)
class GoogleDataplexTaskNotebook:
    def __init__(
        self,
        *,
        notebook: builtins.str,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        infrastructure_spec: typing.Optional[typing.Union["GoogleDataplexTaskNotebookInfrastructureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param notebook: Path to input notebook. This can be the Cloud Storage URI of the notebook file or the path to a Notebook Content. The execution args are accessible as environment variables (TASK_key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#notebook GoogleDataplexTask#notebook}
        :param archive_uris: Cloud Storage URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#archive_uris GoogleDataplexTask#archive_uris}
        :param file_uris: Cloud Storage URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#file_uris GoogleDataplexTask#file_uris}
        :param infrastructure_spec: infrastructure_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#infrastructure_spec GoogleDataplexTask#infrastructure_spec}
        '''
        if isinstance(infrastructure_spec, dict):
            infrastructure_spec = GoogleDataplexTaskNotebookInfrastructureSpec(**infrastructure_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984b17a2a79435d78652b7a08b63871ea2e9fc76d7011aaf4561e5bc8ad90bd4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#notebook GoogleDataplexTask#notebook}
        '''
        result = self._values.get("notebook")
        assert result is not None, "Required property 'notebook' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage URIs of archives to be extracted into the working directory of each executor.

        Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#archive_uris GoogleDataplexTask#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#file_uris GoogleDataplexTask#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def infrastructure_spec(
        self,
    ) -> typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpec"]:
        '''infrastructure_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#infrastructure_spec GoogleDataplexTask#infrastructure_spec}
        '''
        result = self._values.get("infrastructure_spec")
        return typing.cast(typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskNotebook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookInfrastructureSpec",
    jsii_struct_bases=[],
    name_mapping={
        "batch": "batch",
        "container_image": "containerImage",
        "vpc_network": "vpcNetwork",
    },
)
class GoogleDataplexTaskNotebookInfrastructureSpec:
    def __init__(
        self,
        *,
        batch: typing.Optional[typing.Union["GoogleDataplexTaskNotebookInfrastructureSpecBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union["GoogleDataplexTaskNotebookInfrastructureSpecContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network: typing.Optional[typing.Union["GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch: batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#batch GoogleDataplexTask#batch}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#container_image GoogleDataplexTask#container_image}
        :param vpc_network: vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#vpc_network GoogleDataplexTask#vpc_network}
        '''
        if isinstance(batch, dict):
            batch = GoogleDataplexTaskNotebookInfrastructureSpecBatch(**batch)
        if isinstance(container_image, dict):
            container_image = GoogleDataplexTaskNotebookInfrastructureSpecContainerImage(**container_image)
        if isinstance(vpc_network, dict):
            vpc_network = GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork(**vpc_network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0d6f176adc804d692e2574b1561c33416c37db9b1fe6266071312cf8aa8e6c)
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
    def batch(
        self,
    ) -> typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpecBatch"]:
        '''batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#batch GoogleDataplexTask#batch}
        '''
        result = self._values.get("batch")
        return typing.cast(typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpecBatch"], result)

    @builtins.property
    def container_image(
        self,
    ) -> typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpecContainerImage"]:
        '''container_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#container_image GoogleDataplexTask#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpecContainerImage"], result)

    @builtins.property
    def vpc_network(
        self,
    ) -> typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork"]:
        '''vpc_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#vpc_network GoogleDataplexTask#vpc_network}
        '''
        result = self._values.get("vpc_network")
        return typing.cast(typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskNotebookInfrastructureSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookInfrastructureSpecBatch",
    jsii_struct_bases=[],
    name_mapping={
        "executors_count": "executorsCount",
        "max_executors_count": "maxExecutorsCount",
    },
)
class GoogleDataplexTaskNotebookInfrastructureSpecBatch:
    def __init__(
        self,
        *,
        executors_count: typing.Optional[jsii.Number] = None,
        max_executors_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param executors_count: Total number of job executors. Executor Count should be between 2 and 100. [Default=2]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#executors_count GoogleDataplexTask#executors_count}
        :param max_executors_count: Max configurable executors. If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_executors_count GoogleDataplexTask#max_executors_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc298ccffe5e451f8a11db211e497d30917277289365681280aadaea345df66)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#executors_count GoogleDataplexTask#executors_count}
        '''
        result = self._values.get("executors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_executors_count(self) -> typing.Optional[jsii.Number]:
        '''Max configurable executors.

        If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_executors_count GoogleDataplexTask#max_executors_count}
        '''
        result = self._values.get("max_executors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskNotebookInfrastructureSpecBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskNotebookInfrastructureSpecBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookInfrastructureSpecBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7a6f7b9fdba7f41d22b5401811cee8e4781d9108c774a914c81ab7487aa73de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f93b3f0c560d8b2b2af22ce7f220727b17b6dfa735d8e9b0c24b7e969f6f475a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxExecutorsCount")
    def max_executors_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxExecutorsCount"))

    @max_executors_count.setter
    def max_executors_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68da989b0b769a94eb73fac04223badf756a7cc5a4aed4c490351996cd892584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxExecutorsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecBatch]:
        return typing.cast(typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81b6fab959be0fd72ab8c27aee242fdd26ca701feae4841103f34d62d397d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookInfrastructureSpecContainerImage",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "java_jars": "javaJars",
        "properties": "properties",
        "python_packages": "pythonPackages",
    },
)
class GoogleDataplexTaskNotebookInfrastructureSpecContainerImage:
    def __init__(
        self,
        *,
        image: typing.Optional[builtins.str] = None,
        java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param image: Container image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#image GoogleDataplexTask#image}
        :param java_jars: A list of Java JARS to add to the classpath. Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#java_jars GoogleDataplexTask#java_jars}
        :param properties: Override to common configuration of open source components installed on the Dataproc cluster. The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#properties GoogleDataplexTask#properties}
        :param python_packages: A list of python packages to be installed. Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_packages GoogleDataplexTask#python_packages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac5e37afd5a11e39586747dac0a71d021e93c01f4406f7feb1dca4ec5e9fd4a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#image GoogleDataplexTask#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def java_jars(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Java JARS to add to the classpath.

        Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#java_jars GoogleDataplexTask#java_jars}
        '''
        result = self._values.get("java_jars")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Override to common configuration of open source components installed on the Dataproc cluster.

        The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#properties GoogleDataplexTask#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def python_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of python packages to be installed.

        Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_packages GoogleDataplexTask#python_packages}
        '''
        result = self._values.get("python_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskNotebookInfrastructureSpecContainerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskNotebookInfrastructureSpecContainerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookInfrastructureSpecContainerImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8d58e2b1bcde1e89d92f01117f536038d6a85ffd75176de8f8a661c576b187b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b4ff8425cbd44d40a90061e523c5895c06a23073b450aebead2bb5bb9284c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="javaJars")
    def java_jars(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "javaJars"))

    @java_jars.setter
    def java_jars(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79bc1667b3b69cc27320e481af56118c525ddab9a43bd93a2f3f4e17978eb94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javaJars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f4b776b8dd15dc5a53ab04a84f70f60551939cf508797169c8e88aec87a337b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonPackages")
    def python_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonPackages"))

    @python_packages.setter
    def python_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff55797a94566e25fa965b877ba2ccdb8fad0053aaa4221471399d780e0ce93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonPackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecContainerImage]:
        return typing.cast(typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecContainerImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecContainerImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe9aa4b2ccd9b52a672e81eea4c4e816b0a785c4606897ec45a9e41dc49b2dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexTaskNotebookInfrastructureSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookInfrastructureSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7820aa9848515e4c41ab6eb7c84aa7bc7615e44d81547ecb250f8499db20ce66)
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
        :param executors_count: Total number of job executors. Executor Count should be between 2 and 100. [Default=2]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#executors_count GoogleDataplexTask#executors_count}
        :param max_executors_count: Max configurable executors. If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_executors_count GoogleDataplexTask#max_executors_count}
        '''
        value = GoogleDataplexTaskNotebookInfrastructureSpecBatch(
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
        :param image: Container image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#image GoogleDataplexTask#image}
        :param java_jars: A list of Java JARS to add to the classpath. Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#java_jars GoogleDataplexTask#java_jars}
        :param properties: Override to common configuration of open source components installed on the Dataproc cluster. The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#properties GoogleDataplexTask#properties}
        :param python_packages: A list of python packages to be installed. Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_packages GoogleDataplexTask#python_packages}
        '''
        value = GoogleDataplexTaskNotebookInfrastructureSpecContainerImage(
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
        :param network: The Cloud VPC network in which the job is run. By default, the Cloud VPC network named Default within the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network GoogleDataplexTask#network}
        :param network_tags: List of network tags to apply to the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network_tags GoogleDataplexTask#network_tags}
        :param sub_network: The Cloud VPC sub-network in which the job is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sub_network GoogleDataplexTask#sub_network}
        '''
        value = GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork(
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
    def batch(self) -> GoogleDataplexTaskNotebookInfrastructureSpecBatchOutputReference:
        return typing.cast(GoogleDataplexTaskNotebookInfrastructureSpecBatchOutputReference, jsii.get(self, "batch"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(
        self,
    ) -> GoogleDataplexTaskNotebookInfrastructureSpecContainerImageOutputReference:
        return typing.cast(GoogleDataplexTaskNotebookInfrastructureSpecContainerImageOutputReference, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetwork")
    def vpc_network(
        self,
    ) -> "GoogleDataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference":
        return typing.cast("GoogleDataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference", jsii.get(self, "vpcNetwork"))

    @builtins.property
    @jsii.member(jsii_name="batchInput")
    def batch_input(
        self,
    ) -> typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecBatch]:
        return typing.cast(typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecBatch], jsii.get(self, "batchInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(
        self,
    ) -> typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecContainerImage]:
        return typing.cast(typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecContainerImage], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkInput")
    def vpc_network_input(
        self,
    ) -> typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork"]:
        return typing.cast(typing.Optional["GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork"], jsii.get(self, "vpcNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpec]:
        return typing.cast(typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f55ca26f3ef0f4095bc851cdc5b8825ecfb7d748794ed7523863b691d7a6f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "network": "network",
        "network_tags": "networkTags",
        "sub_network": "subNetwork",
    },
)
class GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        sub_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network: The Cloud VPC network in which the job is run. By default, the Cloud VPC network named Default within the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network GoogleDataplexTask#network}
        :param network_tags: List of network tags to apply to the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network_tags GoogleDataplexTask#network_tags}
        :param sub_network: The Cloud VPC sub-network in which the job is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sub_network GoogleDataplexTask#sub_network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f67aed6cc6d5c4c47d18f7b5c0d95669c19c0984e5a9e96665c57bcae62baf4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network GoogleDataplexTask#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of network tags to apply to the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network_tags GoogleDataplexTask#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sub_network(self) -> typing.Optional[builtins.str]:
        '''The Cloud VPC sub-network in which the job is run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sub_network GoogleDataplexTask#sub_network}
        '''
        result = self._values.get("sub_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__186fed0c4d8838413ffbbf60579d9152f4f8e0f92e23a06d22eee2a86f108615)
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
            type_hints = typing.get_type_hints(_typecheckingstub__934199c4ae641875f0ea5c26241c2300a45112c12767bf756bec5b9bd842a8eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a8497f4a9ba12260c1589ed19c16546a4a42be284d8249c5cc9c0afe2e3759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subNetwork")
    def sub_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subNetwork"))

    @sub_network.setter
    def sub_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bff8f0e0ef11217ad1a3f452c261817b6116bab306763e01bf6861945ecdbb88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork]:
        return typing.cast(typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971ad9f8ab3c136168507b4a4957297174c72173045fc4f72b9c23e9ab77f279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexTaskNotebookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskNotebookOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__035db14a4476d09716d141c4233e7f4d75cc3dcedc5de39abb4565e1a5de9f8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfrastructureSpec")
    def put_infrastructure_spec(
        self,
        *,
        batch: typing.Optional[typing.Union[GoogleDataplexTaskNotebookInfrastructureSpecBatch, typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union[GoogleDataplexTaskNotebookInfrastructureSpecContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network: typing.Optional[typing.Union[GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch: batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#batch GoogleDataplexTask#batch}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#container_image GoogleDataplexTask#container_image}
        :param vpc_network: vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#vpc_network GoogleDataplexTask#vpc_network}
        '''
        value = GoogleDataplexTaskNotebookInfrastructureSpec(
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
    ) -> GoogleDataplexTaskNotebookInfrastructureSpecOutputReference:
        return typing.cast(GoogleDataplexTaskNotebookInfrastructureSpecOutputReference, jsii.get(self, "infrastructureSpec"))

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
    ) -> typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpec]:
        return typing.cast(typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpec], jsii.get(self, "infrastructureSpecInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__49d3eb7a531814d2833dd4b3e067dfbf12798951dd147f481e14c6711214771e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ad9c02027f84f9bac78287882af05a50ef83424426333a4ab24bd66114e824)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notebook")
    def notebook(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebook"))

    @notebook.setter
    def notebook(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72b5371fea37cec75ac230be108006a96f3760d9e69ede1c958587a3325faa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataplexTaskNotebook]:
        return typing.cast(typing.Optional[GoogleDataplexTaskNotebook], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskNotebook],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010c3cd45dd829526600e9d3b84bc9a8d6663292b56825e0e246f1915d450306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSpark",
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
class GoogleDataplexTaskSpark:
    def __init__(
        self,
        *,
        archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
        infrastructure_spec: typing.Optional[typing.Union["GoogleDataplexTaskSparkInfrastructureSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        main_class: typing.Optional[builtins.str] = None,
        main_jar_file_uri: typing.Optional[builtins.str] = None,
        python_script_file: typing.Optional[builtins.str] = None,
        sql_script: typing.Optional[builtins.str] = None,
        sql_script_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_uris: Cloud Storage URIs of archives to be extracted into the working directory of each executor. Supported file types: .jar, .tar, .tar.gz, .tgz, and .zip. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#archive_uris GoogleDataplexTask#archive_uris}
        :param file_uris: Cloud Storage URIs of files to be placed in the working directory of each executor. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#file_uris GoogleDataplexTask#file_uris}
        :param infrastructure_spec: infrastructure_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#infrastructure_spec GoogleDataplexTask#infrastructure_spec}
        :param main_class: The name of the driver's main class. The jar file that contains the class must be in the default CLASSPATH or specified in jar_file_uris. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#main_class GoogleDataplexTask#main_class}
        :param main_jar_file_uri: The Cloud Storage URI of the jar file that contains the main class. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#main_jar_file_uri GoogleDataplexTask#main_jar_file_uri}
        :param python_script_file: The Gcloud Storage URI of the main Python file to use as the driver. Must be a .py file. The execution args are passed in as a sequence of named process arguments (--key=value). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_script_file GoogleDataplexTask#python_script_file}
        :param sql_script: The query text. The execution args are used to declare a set of script variables (set key='value';). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sql_script GoogleDataplexTask#sql_script}
        :param sql_script_file: A reference to a query file. This can be the Cloud Storage URI of the query file or it can the path to a SqlScript Content. The execution args are used to declare a set of script variables (set key='value';). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sql_script_file GoogleDataplexTask#sql_script_file}
        '''
        if isinstance(infrastructure_spec, dict):
            infrastructure_spec = GoogleDataplexTaskSparkInfrastructureSpec(**infrastructure_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee09ec2e416f0665c0a6b2c11d530bb718b01065449092a3540a479bce85fa96)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#archive_uris GoogleDataplexTask#archive_uris}
        '''
        result = self._values.get("archive_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_uris(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cloud Storage URIs of files to be placed in the working directory of each executor.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#file_uris GoogleDataplexTask#file_uris}
        '''
        result = self._values.get("file_uris")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def infrastructure_spec(
        self,
    ) -> typing.Optional["GoogleDataplexTaskSparkInfrastructureSpec"]:
        '''infrastructure_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#infrastructure_spec GoogleDataplexTask#infrastructure_spec}
        '''
        result = self._values.get("infrastructure_spec")
        return typing.cast(typing.Optional["GoogleDataplexTaskSparkInfrastructureSpec"], result)

    @builtins.property
    def main_class(self) -> typing.Optional[builtins.str]:
        '''The name of the driver's main class.

        The jar file that contains the class must be in the default CLASSPATH or specified in jar_file_uris. The execution args are passed in as a sequence of named process arguments (--key=value).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#main_class GoogleDataplexTask#main_class}
        '''
        result = self._values.get("main_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main_jar_file_uri(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage URI of the jar file that contains the main class.

        The execution args are passed in as a sequence of named process arguments (--key=value).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#main_jar_file_uri GoogleDataplexTask#main_jar_file_uri}
        '''
        result = self._values.get("main_jar_file_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_script_file(self) -> typing.Optional[builtins.str]:
        '''The Gcloud Storage URI of the main Python file to use as the driver.

        Must be a .py file. The execution args are passed in as a sequence of named process arguments (--key=value).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_script_file GoogleDataplexTask#python_script_file}
        '''
        result = self._values.get("python_script_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_script(self) -> typing.Optional[builtins.str]:
        '''The query text. The execution args are used to declare a set of script variables (set key='value';).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sql_script GoogleDataplexTask#sql_script}
        '''
        result = self._values.get("sql_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sql_script_file(self) -> typing.Optional[builtins.str]:
        '''A reference to a query file.

        This can be the Cloud Storage URI of the query file or it can the path to a SqlScript Content. The execution args are used to declare a set of script variables (set key='value';).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sql_script_file GoogleDataplexTask#sql_script_file}
        '''
        result = self._values.get("sql_script_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskSpark(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkInfrastructureSpec",
    jsii_struct_bases=[],
    name_mapping={
        "batch": "batch",
        "container_image": "containerImage",
        "vpc_network": "vpcNetwork",
    },
)
class GoogleDataplexTaskSparkInfrastructureSpec:
    def __init__(
        self,
        *,
        batch: typing.Optional[typing.Union["GoogleDataplexTaskSparkInfrastructureSpecBatch", typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union["GoogleDataplexTaskSparkInfrastructureSpecContainerImage", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network: typing.Optional[typing.Union["GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch: batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#batch GoogleDataplexTask#batch}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#container_image GoogleDataplexTask#container_image}
        :param vpc_network: vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#vpc_network GoogleDataplexTask#vpc_network}
        '''
        if isinstance(batch, dict):
            batch = GoogleDataplexTaskSparkInfrastructureSpecBatch(**batch)
        if isinstance(container_image, dict):
            container_image = GoogleDataplexTaskSparkInfrastructureSpecContainerImage(**container_image)
        if isinstance(vpc_network, dict):
            vpc_network = GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork(**vpc_network)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f842af7aa6b33021b22bc8e0e495b6d460c90ac7f57afdb01d4c01a59c186f2)
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
    def batch(
        self,
    ) -> typing.Optional["GoogleDataplexTaskSparkInfrastructureSpecBatch"]:
        '''batch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#batch GoogleDataplexTask#batch}
        '''
        result = self._values.get("batch")
        return typing.cast(typing.Optional["GoogleDataplexTaskSparkInfrastructureSpecBatch"], result)

    @builtins.property
    def container_image(
        self,
    ) -> typing.Optional["GoogleDataplexTaskSparkInfrastructureSpecContainerImage"]:
        '''container_image block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#container_image GoogleDataplexTask#container_image}
        '''
        result = self._values.get("container_image")
        return typing.cast(typing.Optional["GoogleDataplexTaskSparkInfrastructureSpecContainerImage"], result)

    @builtins.property
    def vpc_network(
        self,
    ) -> typing.Optional["GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork"]:
        '''vpc_network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#vpc_network GoogleDataplexTask#vpc_network}
        '''
        result = self._values.get("vpc_network")
        return typing.cast(typing.Optional["GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskSparkInfrastructureSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkInfrastructureSpecBatch",
    jsii_struct_bases=[],
    name_mapping={
        "executors_count": "executorsCount",
        "max_executors_count": "maxExecutorsCount",
    },
)
class GoogleDataplexTaskSparkInfrastructureSpecBatch:
    def __init__(
        self,
        *,
        executors_count: typing.Optional[jsii.Number] = None,
        max_executors_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param executors_count: Total number of job executors. Executor Count should be between 2 and 100. [Default=2]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#executors_count GoogleDataplexTask#executors_count}
        :param max_executors_count: Max configurable executors. If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_executors_count GoogleDataplexTask#max_executors_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042f32018dd3ac6ad43288af98a25af963544dc2c5f642c36cfbb63fb0e24047)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#executors_count GoogleDataplexTask#executors_count}
        '''
        result = self._values.get("executors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_executors_count(self) -> typing.Optional[jsii.Number]:
        '''Max configurable executors.

        If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_executors_count GoogleDataplexTask#max_executors_count}
        '''
        result = self._values.get("max_executors_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskSparkInfrastructureSpecBatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskSparkInfrastructureSpecBatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkInfrastructureSpecBatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__673a65adfca49086d5825808e6058b1bd8cfe3d36bf72201c96257c75b26a618)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fce499e2a63fc83506920da6d2604939b47bfbe990499918d8a8a9867fbca94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executorsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxExecutorsCount")
    def max_executors_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxExecutorsCount"))

    @max_executors_count.setter
    def max_executors_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44cff3c7cc8f380fe99862b93f0975ce753409b86ac39afc9f98e9e0001d816a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxExecutorsCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecBatch]:
        return typing.cast(typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecBatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecBatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd7f6b230247e8498b847365bb830c2d2aa9e1d1249b8d8fb75856029e39ddb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkInfrastructureSpecContainerImage",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "java_jars": "javaJars",
        "properties": "properties",
        "python_packages": "pythonPackages",
    },
)
class GoogleDataplexTaskSparkInfrastructureSpecContainerImage:
    def __init__(
        self,
        *,
        image: typing.Optional[builtins.str] = None,
        java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param image: Container image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#image GoogleDataplexTask#image}
        :param java_jars: A list of Java JARS to add to the classpath. Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#java_jars GoogleDataplexTask#java_jars}
        :param properties: Override to common configuration of open source components installed on the Dataproc cluster. The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#properties GoogleDataplexTask#properties}
        :param python_packages: A list of python packages to be installed. Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_packages GoogleDataplexTask#python_packages}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6750325070ef05efd4fbb6e46a7a29a2e01a6ac57e9fadb67348a18995d6ba7d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#image GoogleDataplexTask#image}
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def java_jars(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Java JARS to add to the classpath.

        Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#java_jars GoogleDataplexTask#java_jars}
        '''
        result = self._values.get("java_jars")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Override to common configuration of open source components installed on the Dataproc cluster.

        The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#properties GoogleDataplexTask#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def python_packages(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of python packages to be installed.

        Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_packages GoogleDataplexTask#python_packages}
        '''
        result = self._values.get("python_packages")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskSparkInfrastructureSpecContainerImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskSparkInfrastructureSpecContainerImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkInfrastructureSpecContainerImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda7de58e008bde6784d9377db63457a85cdd5fae10b42c645c0a8627c6d37e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c5bebe2f1479e8200ba4fd167f5a27e1d6cbb734dfea2fd30705643930a4f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="javaJars")
    def java_jars(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "javaJars"))

    @java_jars.setter
    def java_jars(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8126ea296a40473f422cdcdaaf9e6900b1336761a1baaedd1e0d204b5c9a250b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javaJars", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b40b8a128118c6b3b5c5de977af206bd53b934e610b2820f2064037f967a5575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonPackages")
    def python_packages(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pythonPackages"))

    @python_packages.setter
    def python_packages(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329bff94dc1957b68bd6fb9c1a820b4bce7bf4c644b4e9e7acdb675bdf86f840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonPackages", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecContainerImage]:
        return typing.cast(typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecContainerImage], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecContainerImage],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__716172edc69a91561af26f037453dc347fa8bb1a20fafc50e6f1176a6538b931)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexTaskSparkInfrastructureSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkInfrastructureSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4e78bbdf2c3446951364d89a226a6f6005cc6e81f13f27f8b72c6769d93b87a)
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
        :param executors_count: Total number of job executors. Executor Count should be between 2 and 100. [Default=2]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#executors_count GoogleDataplexTask#executors_count}
        :param max_executors_count: Max configurable executors. If maxExecutorsCount > executorsCount, then auto-scaling is enabled. Max Executor Count should be between 2 and 1000. [Default=1000] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_executors_count GoogleDataplexTask#max_executors_count}
        '''
        value = GoogleDataplexTaskSparkInfrastructureSpecBatch(
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
        :param image: Container image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#image GoogleDataplexTask#image}
        :param java_jars: A list of Java JARS to add to the classpath. Valid input includes Cloud Storage URIs to Jar binaries. For example, gs://bucket-name/my/path/to/file.jar Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#java_jars GoogleDataplexTask#java_jars}
        :param properties: Override to common configuration of open source components installed on the Dataproc cluster. The properties to set on daemon config files. Property keys are specified in prefix:property format, for example core:hadoop.tmp.dir. For more information, see Cluster properties. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#properties GoogleDataplexTask#properties}
        :param python_packages: A list of python packages to be installed. Valid formats include Cloud Storage URI to a PIP installable library. For example, gs://bucket-name/my/path/to/lib.tar.gz Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#python_packages GoogleDataplexTask#python_packages}
        '''
        value = GoogleDataplexTaskSparkInfrastructureSpecContainerImage(
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
        :param network: The Cloud VPC network in which the job is run. By default, the Cloud VPC network named Default within the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network GoogleDataplexTask#network}
        :param network_tags: List of network tags to apply to the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network_tags GoogleDataplexTask#network_tags}
        :param sub_network: The Cloud VPC sub-network in which the job is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sub_network GoogleDataplexTask#sub_network}
        '''
        value = GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork(
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
    def batch(self) -> GoogleDataplexTaskSparkInfrastructureSpecBatchOutputReference:
        return typing.cast(GoogleDataplexTaskSparkInfrastructureSpecBatchOutputReference, jsii.get(self, "batch"))

    @builtins.property
    @jsii.member(jsii_name="containerImage")
    def container_image(
        self,
    ) -> GoogleDataplexTaskSparkInfrastructureSpecContainerImageOutputReference:
        return typing.cast(GoogleDataplexTaskSparkInfrastructureSpecContainerImageOutputReference, jsii.get(self, "containerImage"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetwork")
    def vpc_network(
        self,
    ) -> "GoogleDataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference":
        return typing.cast("GoogleDataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference", jsii.get(self, "vpcNetwork"))

    @builtins.property
    @jsii.member(jsii_name="batchInput")
    def batch_input(
        self,
    ) -> typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecBatch]:
        return typing.cast(typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecBatch], jsii.get(self, "batchInput"))

    @builtins.property
    @jsii.member(jsii_name="containerImageInput")
    def container_image_input(
        self,
    ) -> typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecContainerImage]:
        return typing.cast(typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecContainerImage], jsii.get(self, "containerImageInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcNetworkInput")
    def vpc_network_input(
        self,
    ) -> typing.Optional["GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork"]:
        return typing.cast(typing.Optional["GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork"], jsii.get(self, "vpcNetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskSparkInfrastructureSpec]:
        return typing.cast(typing.Optional[GoogleDataplexTaskSparkInfrastructureSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskSparkInfrastructureSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7004a793c6df9d011ccadcbb33761f4b01eb40e8cdc3c991fd87c68fb0903df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "network": "network",
        "network_tags": "networkTags",
        "sub_network": "subNetwork",
    },
)
class GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        sub_network: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param network: The Cloud VPC network in which the job is run. By default, the Cloud VPC network named Default within the project is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network GoogleDataplexTask#network}
        :param network_tags: List of network tags to apply to the job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network_tags GoogleDataplexTask#network_tags}
        :param sub_network: The Cloud VPC sub-network in which the job is run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sub_network GoogleDataplexTask#sub_network}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce08a775d757965b12c2e089bb68ac4986557a4f00d9e2a2bf26dccb4d58a1ed)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network GoogleDataplexTask#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of network tags to apply to the job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#network_tags GoogleDataplexTask#network_tags}
        '''
        result = self._values.get("network_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sub_network(self) -> typing.Optional[builtins.str]:
        '''The Cloud VPC sub-network in which the job is run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#sub_network GoogleDataplexTask#sub_network}
        '''
        result = self._values.get("sub_network")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0402d518d5de9642c84355d045ad434bec513800d1abcb5e1374be759bfd3a9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77e681dcff2e6fa379b36b03a7b521178d08991f06a1d2b659af4d44b8181e09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkTags")
    def network_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkTags"))

    @network_tags.setter
    def network_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93774d18f5916da52c43efb88d23911555aac3bc6adc2833ca62bf2d2d0fcac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subNetwork")
    def sub_network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subNetwork"))

    @sub_network.setter
    def sub_network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0c0d079a17da30cfbbfb79d9d5c4352f9ec07028096c0fa048f6da37d176c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subNetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork]:
        return typing.cast(typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08470a6f41e5eed7cc592d14a2af5b4096c0b54abf95256293cc1a9d9f714899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleDataplexTaskSparkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskSparkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84f7549a2670aba9e6d3707fb8850011bc56409557cf5d573a0a4031079f57a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInfrastructureSpec")
    def put_infrastructure_spec(
        self,
        *,
        batch: typing.Optional[typing.Union[GoogleDataplexTaskSparkInfrastructureSpecBatch, typing.Dict[builtins.str, typing.Any]]] = None,
        container_image: typing.Optional[typing.Union[GoogleDataplexTaskSparkInfrastructureSpecContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_network: typing.Optional[typing.Union[GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param batch: batch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#batch GoogleDataplexTask#batch}
        :param container_image: container_image block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#container_image GoogleDataplexTask#container_image}
        :param vpc_network: vpc_network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#vpc_network GoogleDataplexTask#vpc_network}
        '''
        value = GoogleDataplexTaskSparkInfrastructureSpec(
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
    def infrastructure_spec(
        self,
    ) -> GoogleDataplexTaskSparkInfrastructureSpecOutputReference:
        return typing.cast(GoogleDataplexTaskSparkInfrastructureSpecOutputReference, jsii.get(self, "infrastructureSpec"))

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
    ) -> typing.Optional[GoogleDataplexTaskSparkInfrastructureSpec]:
        return typing.cast(typing.Optional[GoogleDataplexTaskSparkInfrastructureSpec], jsii.get(self, "infrastructureSpecInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9a3ec53f085f458fb5ec58f2b1ffbec6fb65ed1e68834be23530250316a8bd48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fileUris")
    def file_uris(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fileUris"))

    @file_uris.setter
    def file_uris(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c96b0773a508ebe60696b47dd3a129271dd755960554497a9a9b55013bc18e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileUris", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainClass")
    def main_class(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainClass"))

    @main_class.setter
    def main_class(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cef3085d235f0c80385d0a0e58e5f398240f617d99a4fbe39dcf5480cfe919f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainClass", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mainJarFileUri")
    def main_jar_file_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mainJarFileUri"))

    @main_jar_file_uri.setter
    def main_jar_file_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74dc31cfba5de2b56e04a2ac1c1a9d2b5c509fda38951257aff17f88b5b2d810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainJarFileUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonScriptFile")
    def python_script_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonScriptFile"))

    @python_script_file.setter
    def python_script_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33102d8230894ae86dc3d6f3c406d6d66602871d407107114ea3a815b9ddde52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonScriptFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlScript")
    def sql_script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlScript"))

    @sql_script.setter
    def sql_script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a1780254a16d177cec1a9783062989136fb49994e38d7e78e5b1d2849ff8cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlScript", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlScriptFile")
    def sql_script_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlScriptFile"))

    @sql_script_file.setter
    def sql_script_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91e4165c4be929a17465ee029e0d7f2917a422e236a019206b08c1ca809a3a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlScriptFile", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataplexTaskSpark]:
        return typing.cast(typing.Optional[GoogleDataplexTaskSpark], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GoogleDataplexTaskSpark]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3740cbd7ed0ca6f30d51121b6678c39224c60a347bf5f7eff735ddd81bd424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleDataplexTaskTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#create GoogleDataplexTask#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#delete GoogleDataplexTask#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#update GoogleDataplexTask#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d35376d87b8b51885f08d6675b67d8b4e66f6b7d6682ae4d29e93780b14d0b0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#create GoogleDataplexTask#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#delete GoogleDataplexTask#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#update GoogleDataplexTask#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e91d82cac5a9a75133b21837eab0393ff206b5826bb8412e35602f9fa338ebae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98a1a6dadb7336ae7bf8d855f95055b216aca8a79c6eda788e53674630e614d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2178c063207ad661fb9c9dba6c9b919f00722212b4e5be6441075a49bd4b317a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e83516a98d0bcdef68d4980a37564f1305802c516c62f5f250668417c27f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexTaskTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexTaskTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexTaskTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18eba98e6ab742c2ab0c16819fd7cd0ef70fc5c673bc4bfc58e5e26deea0ae5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskTriggerSpec",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "disabled": "disabled",
        "max_retries": "maxRetries",
        "schedule": "schedule",
        "start_time": "startTime",
    },
)
class GoogleDataplexTaskTriggerSpec:
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
        :param type: Trigger type of the user-specified Task Possible values: ["ON_DEMAND", "RECURRING"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#type GoogleDataplexTask#type}
        :param disabled: Prevent the task from executing. This does not cancel already running tasks. It is intended to temporarily disable RECURRING tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#disabled GoogleDataplexTask#disabled}
        :param max_retries: Number of retry attempts before aborting. Set to zero to never attempt to retry a failed task. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_retries GoogleDataplexTask#max_retries}
        :param schedule: Cron schedule (https://en.wikipedia.org/wiki/Cron) for running tasks periodically. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: 'CRON_TZ=${IANA_TIME_ZONE}' or 'TZ=${IANA_TIME_ZONE}'. The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, CRON_TZ=America/New_York 1 * * * *, or TZ=America/New_York 1 * * * *. This field is required for RECURRING tasks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#schedule GoogleDataplexTask#schedule}
        :param start_time: The first run of the task will be after this time. If not specified, the task will run shortly after being submitted if ON_DEMAND and based on the schedule if RECURRING. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#start_time GoogleDataplexTask#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f5ecc3416306cf1965d7b066fc59b83fb85fc11b74130dd91329af448c824b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#type GoogleDataplexTask#type}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#disabled GoogleDataplexTask#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''Number of retry attempts before aborting. Set to zero to never attempt to retry a failed task.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#max_retries GoogleDataplexTask#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Cron schedule (https://en.wikipedia.org/wiki/Cron) for running tasks periodically. To explicitly set a timezone to the cron tab, apply a prefix in the cron tab: 'CRON_TZ=${IANA_TIME_ZONE}' or 'TZ=${IANA_TIME_ZONE}'. The ${IANA_TIME_ZONE} may only be a valid string from IANA time zone database. For example, CRON_TZ=America/New_York 1 * * * *, or TZ=America/New_York 1 * * * *. This field is required for RECURRING tasks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#schedule GoogleDataplexTask#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The first run of the task will be after this time.

        If not specified, the task will run shortly after being submitted if ON_DEMAND and based on the schedule if RECURRING.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_dataplex_task#start_time GoogleDataplexTask#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleDataplexTaskTriggerSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleDataplexTaskTriggerSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleDataplexTask.GoogleDataplexTaskTriggerSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b567f1e7edbec4f3c8384c731332588702529d0633493509380ec163c7bf557)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f0416969b41078dca5ec40266513c0f451b997fbc5b1cb86898da980e13e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efb1f8a63cd806b6073267ad2a2be18547cd8bf0c59ab6be2ac0412fc0e07462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21107b167226a92f8d4f4ed9f28fed8094c73e96b7c5365866de94f80f9800a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00055fa3e24a6eeadf7e7dfcceb15b2a1cb95a3b47b7294b9c534ef83442610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325882ebd9c45b6c5da2233148bc965ff2ea6c7ad7e013df7ba919daa2bd906b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleDataplexTaskTriggerSpec]:
        return typing.cast(typing.Optional[GoogleDataplexTaskTriggerSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleDataplexTaskTriggerSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec1d937fa19b4be632a56c92780310a88c4549439d7102acd1fd971b538260ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleDataplexTask",
    "GoogleDataplexTaskConfig",
    "GoogleDataplexTaskExecutionSpec",
    "GoogleDataplexTaskExecutionSpecOutputReference",
    "GoogleDataplexTaskExecutionStatus",
    "GoogleDataplexTaskExecutionStatusLatestJob",
    "GoogleDataplexTaskExecutionStatusLatestJobList",
    "GoogleDataplexTaskExecutionStatusLatestJobOutputReference",
    "GoogleDataplexTaskExecutionStatusList",
    "GoogleDataplexTaskExecutionStatusOutputReference",
    "GoogleDataplexTaskNotebook",
    "GoogleDataplexTaskNotebookInfrastructureSpec",
    "GoogleDataplexTaskNotebookInfrastructureSpecBatch",
    "GoogleDataplexTaskNotebookInfrastructureSpecBatchOutputReference",
    "GoogleDataplexTaskNotebookInfrastructureSpecContainerImage",
    "GoogleDataplexTaskNotebookInfrastructureSpecContainerImageOutputReference",
    "GoogleDataplexTaskNotebookInfrastructureSpecOutputReference",
    "GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork",
    "GoogleDataplexTaskNotebookInfrastructureSpecVpcNetworkOutputReference",
    "GoogleDataplexTaskNotebookOutputReference",
    "GoogleDataplexTaskSpark",
    "GoogleDataplexTaskSparkInfrastructureSpec",
    "GoogleDataplexTaskSparkInfrastructureSpecBatch",
    "GoogleDataplexTaskSparkInfrastructureSpecBatchOutputReference",
    "GoogleDataplexTaskSparkInfrastructureSpecContainerImage",
    "GoogleDataplexTaskSparkInfrastructureSpecContainerImageOutputReference",
    "GoogleDataplexTaskSparkInfrastructureSpecOutputReference",
    "GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork",
    "GoogleDataplexTaskSparkInfrastructureSpecVpcNetworkOutputReference",
    "GoogleDataplexTaskSparkOutputReference",
    "GoogleDataplexTaskTimeouts",
    "GoogleDataplexTaskTimeoutsOutputReference",
    "GoogleDataplexTaskTriggerSpec",
    "GoogleDataplexTaskTriggerSpecOutputReference",
]

publication.publish()

def _typecheckingstub__77a273fb9f44daefdb3bd53f1b3faffb0e8a65bfb2af31ca7b784f77b0b44610(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    execution_spec: typing.Union[GoogleDataplexTaskExecutionSpec, typing.Dict[builtins.str, typing.Any]],
    trigger_spec: typing.Union[GoogleDataplexTaskTriggerSpec, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lake: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    notebook: typing.Optional[typing.Union[GoogleDataplexTaskNotebook, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    spark: typing.Optional[typing.Union[GoogleDataplexTaskSpark, typing.Dict[builtins.str, typing.Any]]] = None,
    task_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataplexTaskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a0bb8115ddf92681504bc40d195bc75dc26a3b470d9e3d498f6e58adf48c3d52(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699b2162700fe89aae17d20c21b1797ff25a5f409a1c02991a18bd0968d64d04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f06509a6ff963e29bb481248ee63462e1f6511bf9a2b27b4181d0f76857f66a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240319c78eea3c4de7dfa7747b4e4c353f89cb4aa2aa35835fef7969e33315d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0db3c2d52325e6cd2814561d05ae32ebc5584ee6c4747d9546edeb78e8aaca75(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433f8b8a3d5e3346b9c37681755d443dc595a98e2906f34cd2337bebc27ffd0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a96a1876d2e9e4e95f8b80021e15b6ca09d5ad3c5a541990b28e7163d2764f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb409c2bb9da1f483c23e0829019e4f98e2372b6e45857657c3eee097e43bf60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539e127946b5b0a13e17a16694f4df10be6f1275cd4f0abcea13b4726a025669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7b5ffc5a9bf606a5074cdc5dea868b2fd5238fabdb6abf490d721b75b0e7e8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    execution_spec: typing.Union[GoogleDataplexTaskExecutionSpec, typing.Dict[builtins.str, typing.Any]],
    trigger_spec: typing.Union[GoogleDataplexTaskTriggerSpec, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    lake: typing.Optional[builtins.str] = None,
    location: typing.Optional[builtins.str] = None,
    notebook: typing.Optional[typing.Union[GoogleDataplexTaskNotebook, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    spark: typing.Optional[typing.Union[GoogleDataplexTaskSpark, typing.Dict[builtins.str, typing.Any]]] = None,
    task_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleDataplexTaskTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84181f3291584320601dea4f71e61ccd7fbd9d27c16a5fab04b6df635bd2841(
    *,
    service_account: builtins.str,
    args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    max_job_execution_lifetime: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8bbb3aedb3b3813de300f059f3ddec972aae18a782a3230e16a219d7d529741(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce1e9c6c1ecf4ec2c1b8fe09e4f4f5e53dbf62339054fd9701a6a41e737a7eb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff19bc4e2ac62f2197bc13bcef6ee365db4ef4322ae539ca2d77e6e2ac70553c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462708e5355952ebd0e93d4c06bc8c54b4480f1a38fef9ab759a48ae2af66922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b339fcf8d58917115d8237f136bcd69bbf03e33446c672e0d23545ea7ca35a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5914a8a6f8e16a9ed884a75c3e55a4e4a00ae0148976f791b79036b3d4b61eb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25d1b464008fcb6f16a050cd185afdebef1a454d53d147b12481c52d76af3f4(
    value: typing.Optional[GoogleDataplexTaskExecutionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71033b0226cd192f2b054742cebf3a141884e30957636b0b8d6a36373b71bbfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48562e1922487973ca3ce54ac6a1381ae5e8a2d802c649a1a76d1e73da00fe0d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7374a8b20fd69dbca692267548b7ea048ea015c1f5aca8d1fbca21d6cfb157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f4f75a847ffe7f854d46a6d1e18855e075a381da7aa226a50d2cbffd4ecdd11(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabc7a90f57a7667757dd11df577bfce69cc1539aaf8af78518a55c70bca5479(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860f72ec91a63e59d085d5380463da3fc796511f59e8f33cb558b6b5add1090b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb684e3b2e3b1d63f8fb7a180a32d8969f4cab6eacdc2183a0c5a3cf72dc172(
    value: typing.Optional[GoogleDataplexTaskExecutionStatusLatestJob],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfa62a84503308e3a9783e4180760100aecb935fa0ba720fcb11254e5b617de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a67c90cfadfa8ea3fb498f18b1d51a61139028c072efe2d232fc3ee03f85f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004284e349d7ffc2850a5c73c2855765ebae9a0786a4093227e306c3b52af06b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1f09ce27896c411006e27609745622a1c5c134baeb83fbca6cd4eaa8328ba35(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2281ea65a45698f61ad5921db7617a1ebcb174012da7ef31b9973efd3b8b1477(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd60f68b5a8f5abdcb2bf9748ec5102c6495d8183021768fc3aa5e45b1db915(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23819704a7cabd3a1160e787556649575c4dcd8d72717e3bc0e80626b6568986(
    value: typing.Optional[GoogleDataplexTaskExecutionStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984b17a2a79435d78652b7a08b63871ea2e9fc76d7011aaf4561e5bc8ad90bd4(
    *,
    notebook: builtins.str,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrastructure_spec: typing.Optional[typing.Union[GoogleDataplexTaskNotebookInfrastructureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0d6f176adc804d692e2574b1561c33416c37db9b1fe6266071312cf8aa8e6c(
    *,
    batch: typing.Optional[typing.Union[GoogleDataplexTaskNotebookInfrastructureSpecBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    container_image: typing.Optional[typing.Union[GoogleDataplexTaskNotebookInfrastructureSpecContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_network: typing.Optional[typing.Union[GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc298ccffe5e451f8a11db211e497d30917277289365681280aadaea345df66(
    *,
    executors_count: typing.Optional[jsii.Number] = None,
    max_executors_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a6f7b9fdba7f41d22b5401811cee8e4781d9108c774a914c81ab7487aa73de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93b3f0c560d8b2b2af22ce7f220727b17b6dfa735d8e9b0c24b7e969f6f475a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68da989b0b769a94eb73fac04223badf756a7cc5a4aed4c490351996cd892584(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81b6fab959be0fd72ab8c27aee242fdd26ca701feae4841103f34d62d397d12(
    value: typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac5e37afd5a11e39586747dac0a71d021e93c01f4406f7feb1dca4ec5e9fd4a(
    *,
    image: typing.Optional[builtins.str] = None,
    java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d58e2b1bcde1e89d92f01117f536038d6a85ffd75176de8f8a661c576b187b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b4ff8425cbd44d40a90061e523c5895c06a23073b450aebead2bb5bb9284c08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bc1667b3b69cc27320e481af56118c525ddab9a43bd93a2f3f4e17978eb94a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f4b776b8dd15dc5a53ab04a84f70f60551939cf508797169c8e88aec87a337b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff55797a94566e25fa965b877ba2ccdb8fad0053aaa4221471399d780e0ce93c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe9aa4b2ccd9b52a672e81eea4c4e816b0a785c4606897ec45a9e41dc49b2dd(
    value: typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecContainerImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7820aa9848515e4c41ab6eb7c84aa7bc7615e44d81547ecb250f8499db20ce66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f55ca26f3ef0f4095bc851cdc5b8825ecfb7d748794ed7523863b691d7a6f12(
    value: typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f67aed6cc6d5c4c47d18f7b5c0d95669c19c0984e5a9e96665c57bcae62baf4(
    *,
    network: typing.Optional[builtins.str] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    sub_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186fed0c4d8838413ffbbf60579d9152f4f8e0f92e23a06d22eee2a86f108615(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934199c4ae641875f0ea5c26241c2300a45112c12767bf756bec5b9bd842a8eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a8497f4a9ba12260c1589ed19c16546a4a42be284d8249c5cc9c0afe2e3759(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bff8f0e0ef11217ad1a3f452c261817b6116bab306763e01bf6861945ecdbb88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971ad9f8ab3c136168507b4a4957297174c72173045fc4f72b9c23e9ab77f279(
    value: typing.Optional[GoogleDataplexTaskNotebookInfrastructureSpecVpcNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035db14a4476d09716d141c4233e7f4d75cc3dcedc5de39abb4565e1a5de9f8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d3eb7a531814d2833dd4b3e067dfbf12798951dd147f481e14c6711214771e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ad9c02027f84f9bac78287882af05a50ef83424426333a4ab24bd66114e824(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72b5371fea37cec75ac230be108006a96f3760d9e69ede1c958587a3325faa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010c3cd45dd829526600e9d3b84bc9a8d6663292b56825e0e246f1915d450306(
    value: typing.Optional[GoogleDataplexTaskNotebook],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee09ec2e416f0665c0a6b2c11d530bb718b01065449092a3540a479bce85fa96(
    *,
    archive_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_uris: typing.Optional[typing.Sequence[builtins.str]] = None,
    infrastructure_spec: typing.Optional[typing.Union[GoogleDataplexTaskSparkInfrastructureSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    main_class: typing.Optional[builtins.str] = None,
    main_jar_file_uri: typing.Optional[builtins.str] = None,
    python_script_file: typing.Optional[builtins.str] = None,
    sql_script: typing.Optional[builtins.str] = None,
    sql_script_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f842af7aa6b33021b22bc8e0e495b6d460c90ac7f57afdb01d4c01a59c186f2(
    *,
    batch: typing.Optional[typing.Union[GoogleDataplexTaskSparkInfrastructureSpecBatch, typing.Dict[builtins.str, typing.Any]]] = None,
    container_image: typing.Optional[typing.Union[GoogleDataplexTaskSparkInfrastructureSpecContainerImage, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_network: typing.Optional[typing.Union[GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042f32018dd3ac6ad43288af98a25af963544dc2c5f642c36cfbb63fb0e24047(
    *,
    executors_count: typing.Optional[jsii.Number] = None,
    max_executors_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673a65adfca49086d5825808e6058b1bd8cfe3d36bf72201c96257c75b26a618(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fce499e2a63fc83506920da6d2604939b47bfbe990499918d8a8a9867fbca94(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cff3c7cc8f380fe99862b93f0975ce753409b86ac39afc9f98e9e0001d816a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd7f6b230247e8498b847365bb830c2d2aa9e1d1249b8d8fb75856029e39ddb(
    value: typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecBatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6750325070ef05efd4fbb6e46a7a29a2e01a6ac57e9fadb67348a18995d6ba7d(
    *,
    image: typing.Optional[builtins.str] = None,
    java_jars: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    python_packages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda7de58e008bde6784d9377db63457a85cdd5fae10b42c645c0a8627c6d37e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5bebe2f1479e8200ba4fd167f5a27e1d6cbb734dfea2fd30705643930a4f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8126ea296a40473f422cdcdaaf9e6900b1336761a1baaedd1e0d204b5c9a250b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40b8a128118c6b3b5c5de977af206bd53b934e610b2820f2064037f967a5575(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329bff94dc1957b68bd6fb9c1a820b4bce7bf4c644b4e9e7acdb675bdf86f840(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__716172edc69a91561af26f037453dc347fa8bb1a20fafc50e6f1176a6538b931(
    value: typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecContainerImage],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e78bbdf2c3446951364d89a226a6f6005cc6e81f13f27f8b72c6769d93b87a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7004a793c6df9d011ccadcbb33761f4b01eb40e8cdc3c991fd87c68fb0903df0(
    value: typing.Optional[GoogleDataplexTaskSparkInfrastructureSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce08a775d757965b12c2e089bb68ac4986557a4f00d9e2a2bf26dccb4d58a1ed(
    *,
    network: typing.Optional[builtins.str] = None,
    network_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    sub_network: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0402d518d5de9642c84355d045ad434bec513800d1abcb5e1374be759bfd3a9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e681dcff2e6fa379b36b03a7b521178d08991f06a1d2b659af4d44b8181e09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93774d18f5916da52c43efb88d23911555aac3bc6adc2833ca62bf2d2d0fcac3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0c0d079a17da30cfbbfb79d9d5c4352f9ec07028096c0fa048f6da37d176c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08470a6f41e5eed7cc592d14a2af5b4096c0b54abf95256293cc1a9d9f714899(
    value: typing.Optional[GoogleDataplexTaskSparkInfrastructureSpecVpcNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f7549a2670aba9e6d3707fb8850011bc56409557cf5d573a0a4031079f57a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3ec53f085f458fb5ec58f2b1ffbec6fb65ed1e68834be23530250316a8bd48(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c96b0773a508ebe60696b47dd3a129271dd755960554497a9a9b55013bc18e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef3085d235f0c80385d0a0e58e5f398240f617d99a4fbe39dcf5480cfe919f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74dc31cfba5de2b56e04a2ac1c1a9d2b5c509fda38951257aff17f88b5b2d810(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33102d8230894ae86dc3d6f3c406d6d66602871d407107114ea3a815b9ddde52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1780254a16d177cec1a9783062989136fb49994e38d7e78e5b1d2849ff8cd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91e4165c4be929a17465ee029e0d7f2917a422e236a019206b08c1ca809a3a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3740cbd7ed0ca6f30d51121b6678c39224c60a347bf5f7eff735ddd81bd424(
    value: typing.Optional[GoogleDataplexTaskSpark],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d35376d87b8b51885f08d6675b67d8b4e66f6b7d6682ae4d29e93780b14d0b0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91d82cac5a9a75133b21837eab0393ff206b5826bb8412e35602f9fa338ebae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a1a6dadb7336ae7bf8d855f95055b216aca8a79c6eda788e53674630e614d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2178c063207ad661fb9c9dba6c9b919f00722212b4e5be6441075a49bd4b317a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e83516a98d0bcdef68d4980a37564f1305802c516c62f5f250668417c27f08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18eba98e6ab742c2ab0c16819fd7cd0ef70fc5c673bc4bfc58e5e26deea0ae5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleDataplexTaskTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f5ecc3416306cf1965d7b066fc59b83fb85fc11b74130dd91329af448c824b(
    *,
    type: builtins.str,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    schedule: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b567f1e7edbec4f3c8384c731332588702529d0633493509380ec163c7bf557(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f0416969b41078dca5ec40266513c0f451b997fbc5b1cb86898da980e13e50(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efb1f8a63cd806b6073267ad2a2be18547cd8bf0c59ab6be2ac0412fc0e07462(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21107b167226a92f8d4f4ed9f28fed8094c73e96b7c5365866de94f80f9800a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00055fa3e24a6eeadf7e7dfcceb15b2a1cb95a3b47b7294b9c534ef83442610(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325882ebd9c45b6c5da2233148bc965ff2ea6c7ad7e013df7ba919daa2bd906b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec1d937fa19b4be632a56c92780310a88c4549439d7102acd1fd971b538260ff(
    value: typing.Optional[GoogleDataplexTaskTriggerSpec],
) -> None:
    """Type checking stubs"""
    pass

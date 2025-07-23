r'''
# `google_cloud_run_v2_job`

Refer to the Terraform Registry for docs: [`google_cloud_run_v2_job`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job).
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


class CloudRunV2Job(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2Job",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job google_cloud_run_v2_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        template: typing.Union["CloudRunV2JobTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union["CloudRunV2JobBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        client_version: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_stage: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudRunV2JobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job google_cloud_run_v2_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the cloud run job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#location CloudRunV2Job#location}
        :param name: Name of the Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#template CloudRunV2Job#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected on new resources. All system annotations in v1 now have a corresponding field in v2 Job. This field follows Kubernetes annotations' namespacing, limits, and rules. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#annotations CloudRunV2Job#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#binary_authorization CloudRunV2Job#binary_authorization}
        :param client: Arbitrary identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#client CloudRunV2Job#client}
        :param client_version: Arbitrary version identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#client_version CloudRunV2Job#client_version}
        :param deletion_protection: Whether Terraform will be prevented from destroying the job. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the job, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the job will fail. When the field is set to false, deleting the job is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#deletion_protection CloudRunV2Job#deletion_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#id CloudRunV2Job#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 Job. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#labels CloudRunV2Job#labels}
        :param launch_stage: The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features. For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#launch_stage CloudRunV2Job#launch_stage}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#project CloudRunV2Job#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeouts CloudRunV2Job#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07681793f9e8d8de4337a42ae6bfae6f39cd0ee924647af81415362b94aa61a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudRunV2JobConfig(
            location=location,
            name=name,
            template=template,
            annotations=annotations,
            binary_authorization=binary_authorization,
            client=client,
            client_version=client_version,
            deletion_protection=deletion_protection,
            id=id,
            labels=labels,
            launch_stage=launch_stage,
            project=project,
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
        '''Generates CDKTF code for importing a CloudRunV2Job resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudRunV2Job to import.
        :param import_from_id: The id of the existing CloudRunV2Job that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudRunV2Job to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3911cb5c2c76c1582ee3343e30ebcdabee98783c4fac57fffc18b280f82774ad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBinaryAuthorization")
    def put_binary_authorization(
        self,
        *,
        breakglass_justification: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param breakglass_justification: If present, indicates to use Breakglass using this justification. If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#breakglass_justification CloudRunV2Job#breakglass_justification}
        :param policy: The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#policy CloudRunV2Job#policy}
        :param use_default: If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#use_default CloudRunV2Job#use_default}
        '''
        value = CloudRunV2JobBinaryAuthorization(
            breakglass_justification=breakglass_justification,
            policy=policy,
            use_default=use_default,
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        template: typing.Union["CloudRunV2JobTemplateTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#template CloudRunV2Job#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system annotations in v1 now have a corresponding field in v2 ExecutionTemplate. This field follows Kubernetes annotations' namespacing, limits, and rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#annotations CloudRunV2Job#annotations}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 ExecutionTemplate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#labels CloudRunV2Job#labels}
        :param parallelism: Specifies the maximum desired number of tasks the execution should run at given time. Must be <= taskCount. When the job is run, if this field is 0 or unset, the maximum possible value will be used for that execution. The actual number of tasks running in steady state will be less than this number when there are fewer tasks waiting to be completed remaining, i.e. when the work left to do is less than max parallelism. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#parallelism CloudRunV2Job#parallelism}
        :param task_count: Specifies the desired number of tasks the execution should run. Setting to 1 means that parallelism is limited to 1 and the success of that task signals the success of the execution. More info: https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#task_count CloudRunV2Job#task_count}
        '''
        value = CloudRunV2JobTemplate(
            template=template,
            annotations=annotations,
            labels=labels,
            parallelism=parallelism,
            task_count=task_count,
        )

        return typing.cast(None, jsii.invoke(self, "putTemplate", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#create CloudRunV2Job#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#delete CloudRunV2Job#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#update CloudRunV2Job#update}.
        '''
        value = CloudRunV2JobTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBinaryAuthorization")
    def reset_binary_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorization", []))

    @jsii.member(jsii_name="resetClient")
    def reset_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClient", []))

    @jsii.member(jsii_name="resetClientVersion")
    def reset_client_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientVersion", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLaunchStage")
    def reset_launch_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchStage", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="binaryAuthorization")
    def binary_authorization(self) -> "CloudRunV2JobBinaryAuthorizationOutputReference":
        return typing.cast("CloudRunV2JobBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "CloudRunV2JobConditionsList":
        return typing.cast("CloudRunV2JobConditionsList", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="creator")
    def creator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creator"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="executionCount")
    def execution_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "executionCount"))

    @builtins.property
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="lastModifier")
    def last_modifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifier"))

    @builtins.property
    @jsii.member(jsii_name="latestCreatedExecution")
    def latest_created_execution(self) -> "CloudRunV2JobLatestCreatedExecutionList":
        return typing.cast("CloudRunV2JobLatestCreatedExecutionList", jsii.get(self, "latestCreatedExecution"))

    @builtins.property
    @jsii.member(jsii_name="observedGeneration")
    def observed_generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "observedGeneration"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "CloudRunV2JobTemplateOutputReference":
        return typing.cast("CloudRunV2JobTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="terminalCondition")
    def terminal_condition(self) -> "CloudRunV2JobTerminalConditionList":
        return typing.cast("CloudRunV2JobTerminalConditionList", jsii.get(self, "terminalCondition"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudRunV2JobTimeoutsOutputReference":
        return typing.cast("CloudRunV2JobTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="binaryAuthorizationInput")
    def binary_authorization_input(
        self,
    ) -> typing.Optional["CloudRunV2JobBinaryAuthorization"]:
        return typing.cast(typing.Optional["CloudRunV2JobBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientInput")
    def client_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientInput"))

    @builtins.property
    @jsii.member(jsii_name="clientVersionInput")
    def client_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

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
    @jsii.member(jsii_name="launchStageInput")
    def launch_stage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "launchStageInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["CloudRunV2JobTemplate"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudRunV2JobTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudRunV2JobTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69be8e25e0fffbe830209e88bf65e9b764144fcabdae2f7aaffb735384578eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="client")
    def client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "client"))

    @client.setter
    def client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f174589e82aea9d58560a23745ee0f90ab435e50048673816be7c728d63c279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "client", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientVersion")
    def client_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientVersion"))

    @client_version.setter
    def client_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3032cbf7fe284bfd8979ac9aed71a54a44cee34e75b92cfc4deddd46a3e6ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3492ffdbbfbfc07aab24dc225c08b5aa02835f4ab2e1bdc29a5de5af6a13bf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5489848e74075b947a68dd1809bb0586b2cbd4ae642d8c953d69952676e01b7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ddeea4f44a85221db965b5a8ee56ca273f93571907bcc7ca11c39affe80b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchStage")
    def launch_stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchStage"))

    @launch_stage.setter
    def launch_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffad024fca4ebc7335bfc3c9688411fe708353b4463b713289dad7d64552345)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37645e50e6c12d6d4fed18b03be9196ef57eb8c779c275abd084920e3bc60153)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21add8c8b194867cd7fd56e27e348e5e3ab370845416b790642c3fef0262eca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005fa1a81f317f712a598377a6d14ae05e9b5969ae6d1f54fedbc21818913d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={
        "breakglass_justification": "breakglassJustification",
        "policy": "policy",
        "use_default": "useDefault",
    },
)
class CloudRunV2JobBinaryAuthorization:
    def __init__(
        self,
        *,
        breakglass_justification: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param breakglass_justification: If present, indicates to use Breakglass using this justification. If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#breakglass_justification CloudRunV2Job#breakglass_justification}
        :param policy: The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#policy CloudRunV2Job#policy}
        :param use_default: If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#use_default CloudRunV2Job#use_default}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba391bf182ebfe028ed7b08be2d884aec42484adc436539313494138a65c3e16)
            check_type(argname="argument breakglass_justification", value=breakglass_justification, expected_type=type_hints["breakglass_justification"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument use_default", value=use_default, expected_type=type_hints["use_default"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if breakglass_justification is not None:
            self._values["breakglass_justification"] = breakglass_justification
        if policy is not None:
            self._values["policy"] = policy
        if use_default is not None:
            self._values["use_default"] = use_default

    @builtins.property
    def breakglass_justification(self) -> typing.Optional[builtins.str]:
        '''If present, indicates to use Breakglass using this justification.

        If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#breakglass_justification CloudRunV2Job#breakglass_justification}
        '''
        result = self._values.get("breakglass_justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#policy CloudRunV2Job#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#use_default CloudRunV2Job#use_default}
        '''
        result = self._values.get("use_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ded0e475ace79d08a6ab84a68d70b3c51dad0f7362a49125fe686c79a9026190)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBreakglassJustification")
    def reset_breakglass_justification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBreakglassJustification", []))

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @jsii.member(jsii_name="resetUseDefault")
    def reset_use_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseDefault", []))

    @builtins.property
    @jsii.member(jsii_name="breakglassJustificationInput")
    def breakglass_justification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "breakglassJustificationInput"))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="useDefaultInput")
    def use_default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="breakglassJustification")
    def breakglass_justification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "breakglassJustification"))

    @breakglass_justification.setter
    def breakglass_justification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffab614a2dd0b825a36faf9fb13ff86b532de7d795a057f604446851762d485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "breakglassJustification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1239116a26c803f6cc3037c307c4e0b68a4e217727be1fcd92c575d10137620b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDefault")
    def use_default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useDefault"))

    @use_default.setter
    def use_default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89448547e632da742fec2d243d83b950beb7d4496d784ab1cf2779c883aa2ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2JobBinaryAuthorization]:
        return typing.cast(typing.Optional[CloudRunV2JobBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45402e6e6434bd7a205ecfada75876b9ea6b4c9363877059796af269cd355e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2JobConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42fde2e3b810cfb39ab3506131f6b8d10d88ad8ea5b289210727a4ac6c493d1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudRunV2JobConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4a56664e70c4dae55809b492a2a4775bcbf49a923f1c4f43ed6a511c425b4d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c224664ab824c06c88aa169cd91b44b97ab1cca4ebf17f699f297c9d85f465)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5acbc4394a8159a66efb684bbd87d965323d311928aa37055bc3b440eb8c2136)
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
            type_hints = typing.get_type_hints(_typecheckingstub__360de86a5873e4e62676aefa8c6b9e05bb15d060133635bb20a9180f9265062f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9aece4806a8b42fae4e587e4cc2b9d78e6c24eb321fd01c06a14bdf4a0d704be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="executionReason")
    def execution_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionReason"))

    @builtins.property
    @jsii.member(jsii_name="lastTransitionTime")
    def last_transition_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransitionTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="revisionReason")
    def revision_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionReason"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2JobConditions]:
        return typing.cast(typing.Optional[CloudRunV2JobConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudRunV2JobConditions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac21bce80efd068eeac872d644c1c490774287aa8cb29ea7b5ebb334c71b183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobConfig",
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
        "name": "name",
        "template": "template",
        "annotations": "annotations",
        "binary_authorization": "binaryAuthorization",
        "client": "client",
        "client_version": "clientVersion",
        "deletion_protection": "deletionProtection",
        "id": "id",
        "labels": "labels",
        "launch_stage": "launchStage",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class CloudRunV2JobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        template: typing.Union["CloudRunV2JobTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union[CloudRunV2JobBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        client_version: typing.Optional[builtins.str] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_stage: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CloudRunV2JobTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the cloud run job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#location CloudRunV2Job#location}
        :param name: Name of the Job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#template CloudRunV2Job#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected on new resources. All system annotations in v1 now have a corresponding field in v2 Job. This field follows Kubernetes annotations' namespacing, limits, and rules. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#annotations CloudRunV2Job#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#binary_authorization CloudRunV2Job#binary_authorization}
        :param client: Arbitrary identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#client CloudRunV2Job#client}
        :param client_version: Arbitrary version identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#client_version CloudRunV2Job#client_version}
        :param deletion_protection: Whether Terraform will be prevented from destroying the job. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the job, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the job will fail. When the field is set to false, deleting the job is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#deletion_protection CloudRunV2Job#deletion_protection}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#id CloudRunV2Job#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 Job. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#labels CloudRunV2Job#labels}
        :param launch_stage: The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features. For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#launch_stage CloudRunV2Job#launch_stage}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#project CloudRunV2Job#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeouts CloudRunV2Job#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(template, dict):
            template = CloudRunV2JobTemplate(**template)
        if isinstance(binary_authorization, dict):
            binary_authorization = CloudRunV2JobBinaryAuthorization(**binary_authorization)
        if isinstance(timeouts, dict):
            timeouts = CloudRunV2JobTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f8bf68c0796fb3d93a12b7b29a955b2dd06fc5989f084db5b2d50e226ad57c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument binary_authorization", value=binary_authorization, expected_type=type_hints["binary_authorization"])
            check_type(argname="argument client", value=client, expected_type=type_hints["client"])
            check_type(argname="argument client_version", value=client_version, expected_type=type_hints["client_version"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument launch_stage", value=launch_stage, expected_type=type_hints["launch_stage"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "template": template,
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
        if binary_authorization is not None:
            self._values["binary_authorization"] = binary_authorization
        if client is not None:
            self._values["client"] = client
        if client_version is not None:
            self._values["client_version"] = client_version
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if launch_stage is not None:
            self._values["launch_stage"] = launch_stage
        if project is not None:
            self._values["project"] = project
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
    def location(self) -> builtins.str:
        '''The location of the cloud run job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#location CloudRunV2Job#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> "CloudRunV2JobTemplate":
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#template CloudRunV2Job#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("CloudRunV2JobTemplate", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that may be set by external tools to store and arbitrary metadata.

        They are not queryable and should be preserved when modifying objects.

        Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected on new resources.
        All system annotations in v1 now have a corresponding field in v2 Job.

        This field follows Kubernetes annotations' namespacing, limits, and rules.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#annotations CloudRunV2Job#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def binary_authorization(self) -> typing.Optional[CloudRunV2JobBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#binary_authorization CloudRunV2Job#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[CloudRunV2JobBinaryAuthorization], result)

    @builtins.property
    def client(self) -> typing.Optional[builtins.str]:
        '''Arbitrary identifier for the API client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#client CloudRunV2Job#client}
        '''
        result = self._values.get("client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_version(self) -> typing.Optional[builtins.str]:
        '''Arbitrary version identifier for the API client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#client_version CloudRunV2Job#client_version}
        '''
        result = self._values.get("client_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the job.

        Defaults to true.
        When a'terraform destroy' or 'terraform apply' would delete the job,
        the command will fail if this field is not set to false in Terraform state.
        When the field is set to true or unset in Terraform state, a 'terraform apply'
        or 'terraform destroy' that would delete the job will fail.
        When the field is set to false, deleting the job is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#deletion_protection CloudRunV2Job#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#id CloudRunV2Job#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that can be used to organize and categorize objects.

        User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component,
        environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels.

        Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system labels in v1 now have a corresponding field in v2 Job.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#labels CloudRunV2Job#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def launch_stage(self) -> typing.Optional[builtins.str]:
        '''The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features.

        For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#launch_stage CloudRunV2Job#launch_stage}
        '''
        result = self._values.get("launch_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#project CloudRunV2Job#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudRunV2JobTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeouts CloudRunV2Job#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudRunV2JobTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobLatestCreatedExecution",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2JobLatestCreatedExecution:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobLatestCreatedExecution(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobLatestCreatedExecutionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobLatestCreatedExecutionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ec635d02fd4bc972e524ada5c9a02898b70c41377b9312f37cb56082ad90fd1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobLatestCreatedExecutionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abc8d40f6ed8d90ead12827ecf28009ee8fcbfa7659bd6c1632a5afee21012d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobLatestCreatedExecutionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36a1e6c3e415150c141c36664b697ebb4ed23184740d9e7a3ea2e5851cf7ab71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d6934d9f54f488a101683250aa4d83c309495f8fcc129ad87a6329227d62bf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e98553783f8999b9d64eb2740b7dc6d688949cd61e7b4735b4663ab65556cd3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobLatestCreatedExecutionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobLatestCreatedExecutionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e26b25692eeacec30992a3c80a99bc44e1345d33676532fbe964602808e5fcd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="completionTime")
    def completion_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "completionTime"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2JobLatestCreatedExecution]:
        return typing.cast(typing.Optional[CloudRunV2JobLatestCreatedExecution], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobLatestCreatedExecution],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69d8936e200034ec1b65525d15d974d7eaf2c8dd03f21901d4417e520b90fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "template": "template",
        "annotations": "annotations",
        "labels": "labels",
        "parallelism": "parallelism",
        "task_count": "taskCount",
    },
)
class CloudRunV2JobTemplate:
    def __init__(
        self,
        *,
        template: typing.Union["CloudRunV2JobTemplateTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        task_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#template CloudRunV2Job#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system annotations in v1 now have a corresponding field in v2 ExecutionTemplate. This field follows Kubernetes annotations' namespacing, limits, and rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#annotations CloudRunV2Job#annotations}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 ExecutionTemplate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#labels CloudRunV2Job#labels}
        :param parallelism: Specifies the maximum desired number of tasks the execution should run at given time. Must be <= taskCount. When the job is run, if this field is 0 or unset, the maximum possible value will be used for that execution. The actual number of tasks running in steady state will be less than this number when there are fewer tasks waiting to be completed remaining, i.e. when the work left to do is less than max parallelism. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#parallelism CloudRunV2Job#parallelism}
        :param task_count: Specifies the desired number of tasks the execution should run. Setting to 1 means that parallelism is limited to 1 and the success of that task signals the success of the execution. More info: https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/ Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#task_count CloudRunV2Job#task_count}
        '''
        if isinstance(template, dict):
            template = CloudRunV2JobTemplateTemplate(**template)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0818b6915563663838f531f7d254e53513db3f5dab8ca1da962fe6277eef8d1)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument parallelism", value=parallelism, expected_type=type_hints["parallelism"])
            check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template": template,
        }
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if task_count is not None:
            self._values["task_count"] = task_count

    @builtins.property
    def template(self) -> "CloudRunV2JobTemplateTemplate":
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#template CloudRunV2Job#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("CloudRunV2JobTemplateTemplate", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that may be set by external tools to store and arbitrary metadata.

        They are not queryable and should be preserved when modifying objects.

        Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system annotations in v1 now have a corresponding field in v2 ExecutionTemplate.

        This field follows Kubernetes annotations' namespacing, limits, and rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#annotations CloudRunV2Job#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that can be used to organize and categorize objects.

        User-provided labels are shared with Google's billing system, so they can be used to filter,
        or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or
        https://cloud.google.com/run/docs/configuring/labels.

        Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system labels in v1 now have a corresponding field in v2 ExecutionTemplate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#labels CloudRunV2Job#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        '''Specifies the maximum desired number of tasks the execution should run at given time.

        Must be <= taskCount. When the job is run, if this field is 0 or unset, the maximum possible value will be used for that execution. The actual number of tasks running in steady state will be less than this number when there are fewer tasks waiting to be completed remaining, i.e. when the work left to do is less than max parallelism.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#parallelism CloudRunV2Job#parallelism}
        '''
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        '''Specifies the desired number of tasks the execution should run.

        Setting to 1 means that parallelism is limited to 1 and the success of that task signals the success of the execution. More info: https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#task_count CloudRunV2Job#task_count}
        '''
        result = self._values.get("task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac249cb401b1f24c3266e1465c872c8cb5990d66b63a54b3fbf8705d4be5c3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        execution_environment: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        node_selector: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateNodeSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_access: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#containers CloudRunV2Job#containers}
        :param encryption_key: A reference to a customer managed encryption key (CMEK) to use to encrypt this container image. For more information, go to https://cloud.google.com/run/docs/securing/using-cmek Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#encryption_key CloudRunV2Job#encryption_key}
        :param execution_environment: The execution environment being used to host this Task. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#execution_environment CloudRunV2Job#execution_environment}
        :param max_retries: Number of retries allowed per Task, before marking this Task failed. Defaults to 3. Minimum value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#max_retries CloudRunV2Job#max_retries}
        :param node_selector: node_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#node_selector CloudRunV2Job#node_selector}
        :param service_account: Email address of the IAM service account associated with the Task of a Job. The service account represents the identity of the running task, and determines what permissions the task has. If not provided, the task will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#service_account CloudRunV2Job#service_account}
        :param timeout: Max allowed time duration the Task may be active before the system will actively try to mark it failed and kill associated containers. This applies per attempt of a task, meaning each retry can run for the full timeout. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeout CloudRunV2Job#timeout}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#volumes CloudRunV2Job#volumes}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#vpc_access CloudRunV2Job#vpc_access}
        '''
        value = CloudRunV2JobTemplateTemplate(
            containers=containers,
            encryption_key=encryption_key,
            execution_environment=execution_environment,
            max_retries=max_retries,
            node_selector=node_selector,
            service_account=service_account,
            timeout=timeout,
            volumes=volumes,
            vpc_access=vpc_access,
        )

        return typing.cast(None, jsii.invoke(self, "putTemplate", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetParallelism")
    def reset_parallelism(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParallelism", []))

    @jsii.member(jsii_name="resetTaskCount")
    def reset_task_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaskCount", []))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "CloudRunV2JobTemplateTemplateOutputReference":
        return typing.cast("CloudRunV2JobTemplateTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="parallelismInput")
    def parallelism_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "parallelismInput"))

    @builtins.property
    @jsii.member(jsii_name="taskCountInput")
    def task_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "taskCountInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["CloudRunV2JobTemplateTemplate"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a42038d353a47fc830b0a6cf7c66ea1b6c40a3f076abf7624145f2cb0895a4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91821f36b7ef9ad1ed6d730f1b5e54f2633bc2e886e51958a2202b4955020e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parallelism")
    def parallelism(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "parallelism"))

    @parallelism.setter
    def parallelism(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9a1a5c13c235584cf787e72aa94af4d35508ba85e3d8d5757e65f9064562f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parallelism", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="taskCount")
    def task_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "taskCount"))

    @task_count.setter
    def task_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c21f9ce68812af6224e9f3619e3f132ea1e8a837d932c0a02966750e74c095)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "taskCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2JobTemplate]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CloudRunV2JobTemplate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b684a19af1cdbee6d9443e97976149fa09a0d778219c8b7989df5cbdf801baaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "containers": "containers",
        "encryption_key": "encryptionKey",
        "execution_environment": "executionEnvironment",
        "max_retries": "maxRetries",
        "node_selector": "nodeSelector",
        "service_account": "serviceAccount",
        "timeout": "timeout",
        "volumes": "volumes",
        "vpc_access": "vpcAccess",
    },
)
class CloudRunV2JobTemplateTemplate:
    def __init__(
        self,
        *,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        execution_environment: typing.Optional[builtins.str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        node_selector: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateNodeSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_access: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#containers CloudRunV2Job#containers}
        :param encryption_key: A reference to a customer managed encryption key (CMEK) to use to encrypt this container image. For more information, go to https://cloud.google.com/run/docs/securing/using-cmek Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#encryption_key CloudRunV2Job#encryption_key}
        :param execution_environment: The execution environment being used to host this Task. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#execution_environment CloudRunV2Job#execution_environment}
        :param max_retries: Number of retries allowed per Task, before marking this Task failed. Defaults to 3. Minimum value is 0. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#max_retries CloudRunV2Job#max_retries}
        :param node_selector: node_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#node_selector CloudRunV2Job#node_selector}
        :param service_account: Email address of the IAM service account associated with the Task of a Job. The service account represents the identity of the running task, and determines what permissions the task has. If not provided, the task will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#service_account CloudRunV2Job#service_account}
        :param timeout: Max allowed time duration the Task may be active before the system will actively try to mark it failed and kill associated containers. This applies per attempt of a task, meaning each retry can run for the full timeout. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeout CloudRunV2Job#timeout}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#volumes CloudRunV2Job#volumes}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#vpc_access CloudRunV2Job#vpc_access}
        '''
        if isinstance(node_selector, dict):
            node_selector = CloudRunV2JobTemplateTemplateNodeSelector(**node_selector)
        if isinstance(vpc_access, dict):
            vpc_access = CloudRunV2JobTemplateTemplateVpcAccess(**vpc_access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2779fd9a2ac837ebc8d3873d9ae10154a55dd22672673169e3db2400926b98)
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument execution_environment", value=execution_environment, expected_type=type_hints["execution_environment"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument node_selector", value=node_selector, expected_type=type_hints["node_selector"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument vpc_access", value=vpc_access, expected_type=type_hints["vpc_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if containers is not None:
            self._values["containers"] = containers
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if execution_environment is not None:
            self._values["execution_environment"] = execution_environment
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if node_selector is not None:
            self._values["node_selector"] = node_selector
        if service_account is not None:
            self._values["service_account"] = service_account
        if timeout is not None:
            self._values["timeout"] = timeout
        if volumes is not None:
            self._values["volumes"] = volumes
        if vpc_access is not None:
            self._values["vpc_access"] = vpc_access

    @builtins.property
    def containers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainers"]]]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#containers CloudRunV2Job#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainers"]]], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''A reference to a customer managed encryption key (CMEK) to use to encrypt this container image.

        For more information, go to https://cloud.google.com/run/docs/securing/using-cmek

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#encryption_key CloudRunV2Job#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_environment(self) -> typing.Optional[builtins.str]:
        '''The execution environment being used to host this Task. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#execution_environment CloudRunV2Job#execution_environment}
        '''
        result = self._values.get("execution_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''Number of retries allowed per Task, before marking this Task failed. Defaults to 3. Minimum value is 0.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#max_retries CloudRunV2Job#max_retries}
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_selector(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateNodeSelector"]:
        '''node_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#node_selector CloudRunV2Job#node_selector}
        '''
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateNodeSelector"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Email address of the IAM service account associated with the Task of a Job.

        The service account represents the identity of the running task, and determines what permissions the task has. If not provided, the task will use the project's default service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#service_account CloudRunV2Job#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Max allowed time duration the Task may be active before the system will actively try to mark it failed and kill associated containers.

        This applies per attempt of a task, meaning each retry can run for the full timeout.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeout CloudRunV2Job#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#volumes CloudRunV2Job#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateVolumes"]]], result)

    @builtins.property
    def vpc_access(self) -> typing.Optional["CloudRunV2JobTemplateTemplateVpcAccess"]:
        '''vpc_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#vpc_access CloudRunV2Job#vpc_access}
        '''
        result = self._values.get("vpc_access")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateVpcAccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainers",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "command": "command",
        "depends_on": "dependsOn",
        "env": "env",
        "name": "name",
        "ports": "ports",
        "resources": "resources",
        "startup_probe": "startupProbe",
        "volume_mounts": "volumeMounts",
        "working_dir": "workingDir",
    },
)
class CloudRunV2JobTemplateTemplateContainers:
    def __init__(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateContainersEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateContainersPorts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resources: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersResources", typing.Dict[builtins.str, typing.Any]]] = None,
        startup_probe: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersStartupProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: URL of the Container image in Google Container Registry or Google Artifact Registry. More info: https://kubernetes.io/docs/concepts/containers/images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#image CloudRunV2Job#image}
        :param args: Arguments to the entrypoint. The docker image's CMD is used if this is not provided. Variable references are not supported in Cloud Run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#args CloudRunV2Job#args}
        :param command: Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#command CloudRunV2Job#command}
        :param depends_on: Names of the containers that must start before this container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#depends_on CloudRunV2Job#depends_on}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#env CloudRunV2Job#env}
        :param name: Name of the container specified as a DNS_LABEL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#ports CloudRunV2Job#ports}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#resources CloudRunV2Job#resources}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#startup_probe CloudRunV2Job#startup_probe}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#volume_mounts CloudRunV2Job#volume_mounts}
        :param working_dir: Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#working_dir CloudRunV2Job#working_dir}
        '''
        if isinstance(resources, dict):
            resources = CloudRunV2JobTemplateTemplateContainersResources(**resources)
        if isinstance(startup_probe, dict):
            startup_probe = CloudRunV2JobTemplateTemplateContainersStartupProbe(**startup_probe)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51113b1e358b9d5401a891c8f50df4ef92fa51086ea2f9f46a18089fa21510a1)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument startup_probe", value=startup_probe, expected_type=type_hints["startup_probe"])
            check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
            check_type(argname="argument working_dir", value=working_dir, expected_type=type_hints["working_dir"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if env is not None:
            self._values["env"] = env
        if name is not None:
            self._values["name"] = name
        if ports is not None:
            self._values["ports"] = ports
        if resources is not None:
            self._values["resources"] = resources
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def image(self) -> builtins.str:
        '''URL of the Container image in Google Container Registry or Google Artifact Registry. More info: https://kubernetes.io/docs/concepts/containers/images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#image CloudRunV2Job#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to the entrypoint.

        The docker image's CMD is used if this is not provided. Variable references are not supported in Cloud Run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#args CloudRunV2Job#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Entrypoint array.

        Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#command CloudRunV2Job#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of the containers that must start before this container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#depends_on CloudRunV2Job#depends_on}
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#env CloudRunV2Job#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersEnv"]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the container specified as a DNS_LABEL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersPorts"]]]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#ports CloudRunV2Job#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersPorts"]]], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#resources CloudRunV2Job#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersResources"], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbe"]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#startup_probe CloudRunV2Job#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbe"], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#volume_mounts CloudRunV2Job#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersVolumeMounts"]]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''Container's working directory.

        If not specified, the container runtime's default will be used, which might be configured in the container image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#working_dir CloudRunV2Job#working_dir}
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "value_source": "valueSource"},
)
class CloudRunV2JobTemplateTemplateContainersEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
        value_source: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersEnvValueSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Must be a C_IDENTIFIER, and mnay not exceed 32768 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        :param value: Literal value of the environment variable. Defaults to "" and the maximum allowed length is 32768 characters. Variable references are not supported in Cloud Run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#value CloudRunV2Job#value}
        :param value_source: value_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#value_source CloudRunV2Job#value_source}
        '''
        if isinstance(value_source, dict):
            value_source = CloudRunV2JobTemplateTemplateContainersEnvValueSource(**value_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0adbf791027f9f38fde86406e34c5b69a08a114987dc89e7a3847da1865510b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument value_source", value=value_source, expected_type=type_hints["value_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value
        if value_source is not None:
            self._values["value_source"] = value_source

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the environment variable. Must be a C_IDENTIFIER, and mnay not exceed 32768 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Literal value of the environment variable.

        Defaults to "" and the maximum allowed length is 32768 characters. Variable references are not supported in Cloud Run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#value CloudRunV2Job#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_source(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersEnvValueSource"]:
        '''value_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#value_source CloudRunV2Job#value_source}
        '''
        result = self._values.get("value_source")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersEnvValueSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53abdfc36772332d7a6c4ff794bfb6793d3fcb7785fdae61a169d126c166d3d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTemplateTemplateContainersEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10b1c32d5ce827a8bae45afa84712ad781ccad33c3509a4fa5f1c3c0b7d7e2c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTemplateTemplateContainersEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed964016dc6a304878e9cc3aaaa58a0e5dd6457e7dead7f478de7f0c703bbe18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca4df7e6f049bc48546dfe3d296addc1752fbb77c2438a18076abbbea9514845)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5aeaef55731865a322c47de6f8fc25c12751350d46df2c6e9b67b36be2670b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e33ed9eb36d2ecb670c941268b26189e1dc41dbdae435031666a761d32590a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateContainersEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42cf77875d784d4135cbcc92446846de93c2b5394a6901c539a832c03d5ecb6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueSource")
    def put_value_source(
        self,
        *,
        secret_key_ref: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret_key_ref CloudRunV2Job#secret_key_ref}
        '''
        value = CloudRunV2JobTemplateTemplateContainersEnvValueSource(
            secret_key_ref=secret_key_ref
        )

        return typing.cast(None, jsii.invoke(self, "putValueSource", [value]))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @jsii.member(jsii_name="resetValueSource")
    def reset_value_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueSource", []))

    @builtins.property
    @jsii.member(jsii_name="valueSource")
    def value_source(
        self,
    ) -> "CloudRunV2JobTemplateTemplateContainersEnvValueSourceOutputReference":
        return typing.cast("CloudRunV2JobTemplateTemplateContainersEnvValueSourceOutputReference", jsii.get(self, "valueSource"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="valueSourceInput")
    def value_source_input(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersEnvValueSource"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersEnvValueSource"], jsii.get(self, "valueSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75565f47816ed87efdd1ffc5d1d916bd8d4ce11913a7391bf43056903b2142c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__315fd177349143b4e28bf10b143571871f46acd68318d68ed1195086bba6763e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e833b808cbaab0121e7dd377fdf4d34e7112b9adfd52a39a34d65d4e3650d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersEnvValueSource",
    jsii_struct_bases=[],
    name_mapping={"secret_key_ref": "secretKeyRef"},
)
class CloudRunV2JobTemplateTemplateContainersEnvValueSource:
    def __init__(
        self,
        *,
        secret_key_ref: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret_key_ref CloudRunV2Job#secret_key_ref}
        '''
        if isinstance(secret_key_ref, dict):
            secret_key_ref = CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef(**secret_key_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4a11cef8f0b5f4087b382b1cfdaf109a41d54e9202c107ee423c3eedaf3c95)
            check_type(argname="argument secret_key_ref", value=secret_key_ref, expected_type=type_hints["secret_key_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_key_ref is not None:
            self._values["secret_key_ref"] = secret_key_ref

    @builtins.property
    def secret_key_ref(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef"]:
        '''secret_key_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret_key_ref CloudRunV2Job#secret_key_ref}
        '''
        result = self._values.get("secret_key_ref")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersEnvValueSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersEnvValueSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersEnvValueSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b524cbcaf75f6d25ec86da188b0bfc781b96c7c16b807ad016caebfb03757f7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretKeyRef")
    def put_secret_key_ref(
        self,
        *,
        secret: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret CloudRunV2Job#secret}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#version CloudRunV2Job#version}
        '''
        value = CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef(
            secret=secret, version=version
        )

        return typing.cast(None, jsii.invoke(self, "putSecretKeyRef", [value]))

    @jsii.member(jsii_name="resetSecretKeyRef")
    def reset_secret_key_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecretKeyRef", []))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRef")
    def secret_key_ref(
        self,
    ) -> "CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRefOutputReference":
        return typing.cast("CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRefOutputReference", jsii.get(self, "secretKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRefInput")
    def secret_key_ref_input(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef"], jsii.get(self, "secretKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersEnvValueSource]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersEnvValueSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateContainersEnvValueSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6aeea1fb54e86bc647f81451db6a1154a0a7f31941ab222ccdec0d7e7c75229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "version": "version"},
)
class CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef:
    def __init__(self, *, secret: builtins.str, version: builtins.str) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret CloudRunV2Job#secret}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#version CloudRunV2Job#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5084de4f0073ddbc77e1d0ee0810b35a23b09ca01ca2fdb255c2388321ec74bb)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
            "version": version,
        }

    @builtins.property
    def secret(self) -> builtins.str:
        '''The name of the secret in Cloud Secret Manager.

        Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret CloudRunV2Job#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Cloud Secret Manager secret version.

        Can be 'latest' for the latest value or an integer for a specific version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#version CloudRunV2Job#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__100f5b6b026228fa31832349e461b104ef5ab0130f7c38c503fb54577ce2b353)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2736f5929d4ddf250e24aa3aa0aa2536ccedf670de3ae103d2407e0cfbe79681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96cd8dadad902873b3608fe9a587379ede51219749bcc5d3db0c89a382b5c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4889c771699bcea2f20299eaa83301792df691496493f42d4a44ef332c27f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f148dc004fea11892a81abf94cc7871aee642b7e26fc9064103cb6ef6393205)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTemplateTemplateContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a25ada2d3713da0156abe27adafee12d0ac2d20557c455e5821aeaf28bff38)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTemplateTemplateContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16aefb2e71bf1f6f33ef7dead6c7b4bf4d970da9ea3b5b17c73d190b185b740)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcf5d5a8855af64a4f162715323e93d5573091183436a26c6b37ef95a9932311)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bae3ad9d37549bfcd4fc3a91a10433f94bd37cbb8a748b2011f1fd3e7887d777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58e69f9eaee75016931477e6b3f0bff56eb47723a7b1f7093220882cb78736d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2cf314fc1149c7a7e4f81e5d91394040d7fe3f66f9ef48ecd2bc48ced1cbc37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eadeb12b0b65e0ebdf4cad5021798c560700b462026965db2cb6a5c25482cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putPorts")
    def put_ports(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateContainersPorts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0a7ebec73a4590c352139cd1ecf7374654949cf5e7e36627ef1ef545269c29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        *,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param limits: Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#limits CloudRunV2Job#limits}
        '''
        value = CloudRunV2JobTemplateTemplateContainersResources(limits=limits)

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#failure_threshold CloudRunV2Job#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#grpc CloudRunV2Job#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#http_get CloudRunV2Job#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#initial_delay_seconds CloudRunV2Job#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#period_seconds CloudRunV2Job#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#tcp_socket CloudRunV2Job#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeout_seconds CloudRunV2Job#timeout_seconds}
        '''
        value = CloudRunV2JobTemplateTemplateContainersStartupProbe(
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            tcp_socket=tcp_socket,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putStartupProbe", [value]))

    @jsii.member(jsii_name="putVolumeMounts")
    def put_volume_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea7214917463382309b760dd78760840a277fa3d05d105a26c337efed41393f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeMounts", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetDependsOn")
    def reset_depends_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependsOn", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetStartupProbe")
    def reset_startup_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupProbe", []))

    @jsii.member(jsii_name="resetVolumeMounts")
    def reset_volume_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMounts", []))

    @jsii.member(jsii_name="resetWorkingDir")
    def reset_working_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDir", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> CloudRunV2JobTemplateTemplateContainersEnvList:
        return typing.cast(CloudRunV2JobTemplateTemplateContainersEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> "CloudRunV2JobTemplateTemplateContainersPortsList":
        return typing.cast("CloudRunV2JobTemplateTemplateContainersPortsList", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "CloudRunV2JobTemplateTemplateContainersResourcesOutputReference":
        return typing.cast("CloudRunV2JobTemplateTemplateContainersResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(
        self,
    ) -> "CloudRunV2JobTemplateTemplateContainersStartupProbeOutputReference":
        return typing.cast("CloudRunV2JobTemplateTemplateContainersStartupProbeOutputReference", jsii.get(self, "startupProbe"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(
        self,
    ) -> "CloudRunV2JobTemplateTemplateContainersVolumeMountsList":
        return typing.cast("CloudRunV2JobTemplateTemplateContainersVolumeMountsList", jsii.get(self, "volumeMounts"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="commandInput")
    def command_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "commandInput"))

    @builtins.property
    @jsii.member(jsii_name="dependsOnInput")
    def depends_on_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependsOnInput"))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersPorts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersPorts"]]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersResources"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="startupProbeInput")
    def startup_probe_input(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbe"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbe"], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

    @builtins.property
    @jsii.member(jsii_name="workingDirInput")
    def working_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ac9d7c983cb4f45c158c4593b5c2480673067736e1717039ecde793e53c871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0a6476eebd27a35e93b548071b29656d1594b7e5529aa3bbff93fbfd9255be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93dc6858c4369e937dfe46b75fcf876259c549099a27070e81bec12c5101eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3cf3c9c775b8beb8756b17ad2555dae9c40dc02fba60a17183fc75bd28ae9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4c2c79a61d05ff2613e1c94eb0db1ec509143eeb3668d4a6344b50a1246dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5340b1110cb96708f8ca520b61cb98b51392bfbde09709561f90f3e890260bcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31d54cd1e213ac8c2b50bb97a16cb12780bc5d31456da4e4776e85cdd2bb4a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersPorts",
    jsii_struct_bases=[],
    name_mapping={"container_port": "containerPort", "name": "name"},
)
class CloudRunV2JobTemplateTemplateContainersPorts:
    def __init__(
        self,
        *,
        container_port: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_port: Port number the container listens on. This must be a valid TCP port number, 0 < containerPort < 65536. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#container_port CloudRunV2Job#container_port}
        :param name: If specified, used to specify which protocol to use. Allowed values are "http1" and "h2c". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08bb73d3381bd120a9d5c81be1516738a0cd5376201f984b5ff0b0f54c9b7cc5)
            check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_port is not None:
            self._values["container_port"] = container_port
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        '''Port number the container listens on. This must be a valid TCP port number, 0 < containerPort < 65536.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#container_port CloudRunV2Job#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''If specified, used to specify which protocol to use. Allowed values are "http1" and "h2c".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersPortsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersPortsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aeb1c0fa8ea4645642736bdfcecd1206135fb79102ad92ee9f50ccbeaa951d8b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTemplateTemplateContainersPortsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f56e64ff610ec71230f3eea6c8807559988631c894d01281ab02f317e7818a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTemplateTemplateContainersPortsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757503a5ea5409a8b615c9151d011b6c20c6488406da1c9e0a9feb81304795d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3264ab737b24b0c6e56d70132f0c252e66c75828296b178030352330366de6d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c249149754746bbc684578e64e0f0cba7cf74096ca74012d872871d76e84d074)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersPorts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersPorts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersPorts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ca76183292a4c5e75a9352db91962effb9a2f855e74384aa106dcb33136b41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateContainersPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff4151ed166f9728fe0b985db51d0e18a73aa5d9b43d4b4f086a5283f131229)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContainerPort")
    def reset_container_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerPort", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="containerPortInput")
    def container_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "containerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerPort"))

    @container_port.setter
    def container_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301924481b0880f265a79b07d6c3d5b762b03ef3b325eff4b6f7e64a5f60289b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54a2f222d3317acee428cd46668381b1c06ff28aabe41ea0e69b270f3d7b65d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersPorts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersPorts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersPorts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d390090891688d9d609bc8f1025f1664834cd61b9910b85470bb83fec8805ca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits"},
)
class CloudRunV2JobTemplateTemplateContainersResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param limits: Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#limits CloudRunV2Job#limits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3642cbe6aabdad011daa9c0711bd672f0404a966de18bb6014ee7f5b2ca53b4)
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limits is not None:
            self._values["limits"] = limits

    @builtins.property
    def limits(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#limits CloudRunV2Job#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a594219de7fb563a855529735df99a4adbc0bf4fcc8dec49d136366d17abf71b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "limits"))

    @limits.setter
    def limits(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42480f3677cf933329dda247ef12c88bd2051c3051036a6b76fb1951a5441e68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersResources]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateContainersResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676a5d58485494d64ef72970170813d504093a2ff46e217c8681e1acecd92fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbe",
    jsii_struct_bases=[],
    name_mapping={
        "failure_threshold": "failureThreshold",
        "grpc": "grpc",
        "http_get": "httpGet",
        "initial_delay_seconds": "initialDelaySeconds",
        "period_seconds": "periodSeconds",
        "tcp_socket": "tcpSocket",
        "timeout_seconds": "timeoutSeconds",
    },
)
class CloudRunV2JobTemplateTemplateContainersStartupProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#failure_threshold CloudRunV2Job#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#grpc CloudRunV2Job#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#http_get CloudRunV2Job#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#initial_delay_seconds CloudRunV2Job#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#period_seconds CloudRunV2Job#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#tcp_socket CloudRunV2Job#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeout_seconds CloudRunV2Job#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1192aea2ac00145a2eedde8be1c207800749427dbfb10203a4663f5bb14e63)
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument grpc", value=grpc, expected_type=type_hints["grpc"])
            check_type(argname="argument http_get", value=http_get, expected_type=type_hints["http_get"])
            check_type(argname="argument initial_delay_seconds", value=initial_delay_seconds, expected_type=type_hints["initial_delay_seconds"])
            check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
            check_type(argname="argument tcp_socket", value=tcp_socket, expected_type=type_hints["tcp_socket"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if grpc is not None:
            self._values["grpc"] = grpc
        if http_get is not None:
            self._values["http_get"] = http_get
        if initial_delay_seconds is not None:
            self._values["initial_delay_seconds"] = initial_delay_seconds
        if period_seconds is not None:
            self._values["period_seconds"] = period_seconds
        if tcp_socket is not None:
            self._values["tcp_socket"] = tcp_socket
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#failure_threshold CloudRunV2Job#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#grpc CloudRunV2Job#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#http_get CloudRunV2Job#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value is 240.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#initial_delay_seconds CloudRunV2Job#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value is 240.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#period_seconds CloudRunV2Job#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#tcp_socket CloudRunV2Job#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600.
        Must be smaller than periodSeconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#timeout_seconds CloudRunV2Job#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#service CloudRunV2Job#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afae6975ae039cbbcc64f04a0a696dd8d5db62c3fe023b485361cfff73e4138)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#service CloudRunV2Job#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersStartupProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93e4935389b6728e8f45149f6b00b16fd2106ae7131b7ca759fef621931a1331)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc6c02b010319033ffb48e8371a953fcd29dd936900dec1f42f436a3505c684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3afefa9b2310f5ee3a6a8d50d145c62c92e52f418442369deadd8d18108d61b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f07dc3d60bbe4d17289943825f6bf9ad545fa7cd3af742127bf7dd623f76493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#http_headers CloudRunV2Job#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#path CloudRunV2Job#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648d2e2699f499f14a4816a067195b5c80fb1fcbdcff30ec051aa4a2dbf3e1e2)
            check_type(argname="argument http_headers", value=http_headers, expected_type=type_hints["http_headers"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_headers is not None:
            self._values["http_headers"] = http_headers
        if path is not None:
            self._values["path"] = path
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def http_headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#http_headers CloudRunV2Job#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. If set, it should not be empty string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#path CloudRunV2Job#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#value CloudRunV2Job#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e008acfc5bf6b83d78100c84fe48794226a5bb93e677b3a8e4cafd2b27717c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def name(self) -> builtins.str:
        '''The header field name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#value CloudRunV2Job#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f29e4af90d00f09bb364c74d815ff73119a69a4cce9ce6dda5756e5d4f34704b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35332ef6301b6f8589852d38fb90ce0e44cf4dbcc9d7b4c605306f95123ec24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96dc57fb29fe0ca592fc856a35f203130e130d7ff02bd9c77d373e60156acb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__457a97251358721c323e8420dab941ede1240197331a20eb55cdbd7a4485ae5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16198255a9df18315d520352e90dcafa6bce09c35c1ae3d26b63b78bc4e161fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd3a1f918f45d47be7a7ce414cfb1cfc0581a92d9219799048998f4d9b34e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e91ffc046236a93fa7684607d8b3e46ac8edd24d0b5470504f2240aad0877c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc802291b397cfeac9222d5abc245217ad18b6fab9ea0451c7e15a670dba9afc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00736a76baef53ec0c693e54b8a7a032455cdcad0a0bce244069817bd02c2279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3698ad57bfad1fbbb20d354929b7ea5e52657b36330954403fd6addc33e0deb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3251c835b88a0753cbd4a51eee46477dcf2acf4b89a48ce64a51d01c8cc3c444)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a43df340d16d1bac577202024191337f84e2f55f3dd19bc873405c468c305d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHttpHeaders", [value]))

    @jsii.member(jsii_name="resetHttpHeaders")
    def reset_http_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHeaders", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="httpHeaders")
    def http_headers(
        self,
    ) -> CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersList:
        return typing.cast(CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8df33ad7eb4a94e55ecae41cd75b93d64ae34f7404f0cada71dd3abda69302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3a8964fbd8fed096bb53ebf162454fbdf5d90775b560d260bd047d79a59424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e077058ed8557628f40289a0968daf86d55687153447551b407330557d6aadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateContainersStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04423d527afc9391a104f47d239269fbf367d79c29f7bf22083a677fe1414636)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGrpc")
    def put_grpc(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#service CloudRunV2Job#service}
        '''
        value = CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#http_headers CloudRunV2Job#http_headers}
        :param path: Path to access on the HTTP server. If set, it should not be empty string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#path CloudRunV2Job#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        '''
        value = CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet(
            http_headers=http_headers, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        '''
        value = CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket(port=port)

        return typing.cast(None, jsii.invoke(self, "putTcpSocket", [value]))

    @jsii.member(jsii_name="resetFailureThreshold")
    def reset_failure_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailureThreshold", []))

    @jsii.member(jsii_name="resetGrpc")
    def reset_grpc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGrpc", []))

    @jsii.member(jsii_name="resetHttpGet")
    def reset_http_get(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpGet", []))

    @jsii.member(jsii_name="resetInitialDelaySeconds")
    def reset_initial_delay_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInitialDelaySeconds", []))

    @jsii.member(jsii_name="resetPeriodSeconds")
    def reset_period_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeriodSeconds", []))

    @jsii.member(jsii_name="resetTcpSocket")
    def reset_tcp_socket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpSocket", []))

    @jsii.member(jsii_name="resetTimeoutSeconds")
    def reset_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="grpc")
    def grpc(
        self,
    ) -> CloudRunV2JobTemplateTemplateContainersStartupProbeGrpcOutputReference:
        return typing.cast(CloudRunV2JobTemplateTemplateContainersStartupProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetOutputReference:
        return typing.cast(CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocketOutputReference":
        return typing.cast("CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet], jsii.get(self, "httpGetInput"))

    @builtins.property
    @jsii.member(jsii_name="initialDelaySecondsInput")
    def initial_delay_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "initialDelaySecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="periodSecondsInput")
    def period_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "periodSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocketInput")
    def tcp_socket_input(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutSecondsInput")
    def timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="failureThreshold")
    def failure_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failureThreshold"))

    @failure_threshold.setter
    def failure_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9a754b1bca5b0d2eba0c3e72d60c837962751cab43e5276b5aac767e57eff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fd9c11384173a943635b1aa45676e47504de9cb7c4e38515a9399666d1bf62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c284b74c7993ab998e43a3ba3725108c39b585b2e429e2ffac510e9beb58b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31aabc8c1a87045516352d551f139595a3cfd8389c1119401693758e7f16c51f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbe]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530c4d14c3493071d00a5a546af06fa6347a123b34e9a6cc47ffd0e0fa01458a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"port": "port"},
)
class CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket:
    def __init__(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__549568f1cc4d7e0519d04283b2c8d52ff913df023ba08cf0f598f439f718ee59)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#port CloudRunV2Job#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e5e8fa5936618f80d98178f08146648cb1abcee5cfbb758d10c422ac7690168)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c712f94bfc8649f14a71f336bccb9a79a342a7d9106f3be21817d40d1bcca2f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28fa174e2ea71a7dd2a354b629a89091d6a9802e1d32c1b254d345cdfcc0000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"mount_path": "mountPath", "name": "name"},
)
class CloudRunV2JobTemplateTemplateContainersVolumeMounts:
    def __init__(self, *, mount_path: builtins.str, name: builtins.str) -> None:
        '''
        :param mount_path: Path within the container at which the volume should be mounted. Must not contain ':'. For Cloud SQL volumes, it can be left empty, or must otherwise be /cloudsql. All instances defined in the Volume will be available as /cloudsql/[instance]. For more information on Cloud SQL volumes, visit https://cloud.google.com/sql/docs/mysql/connect-run Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#mount_path CloudRunV2Job#mount_path}
        :param name: This must match the Name of a Volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443c0155fad35f0b43f55ae6f3b55661989c820846fdc4d8c461677d433f38cb)
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mount_path": mount_path,
            "name": name,
        }

    @builtins.property
    def mount_path(self) -> builtins.str:
        '''Path within the container at which the volume should be mounted.

        Must not contain ':'. For Cloud SQL volumes, it can be left empty, or must otherwise be /cloudsql. All instances defined in the Volume will be available as /cloudsql/[instance]. For more information on Cloud SQL volumes, visit https://cloud.google.com/sql/docs/mysql/connect-run

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#mount_path CloudRunV2Job#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''This must match the Name of a Volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateContainersVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateContainersVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15b623fef922ddceeede59379e378ffe17b56e620cf4422d01e785ad12d2fb88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTemplateTemplateContainersVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4633bf3fd8e485df31f2d34d3190f39a710ccb0ad792603039c02a51664f7c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTemplateTemplateContainersVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee44ec8a2092bc718a32c33092b7b63e7234a14cd8229ccac1c713235da78113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ba3c8071457b9e72c6fe84c077c01ed4d642e2364f9a7d4b7e3ea1eec5daa8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39e720d874f94afd3c41c3ae925ad788e5346a2dfedd3cb8a16c0f5a5b0c2a64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__527e927a96b1d064df69abef020dfbe8275ad51f68b8ab5e8c03d379527c3714)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateContainersVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateContainersVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b80a77f4ceaf9ccb4f21148c89ee6033e0d85a7089fa70b1356d22a0c6ee3d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c32eeaf8f4a4f64e194acd8eeb7ccf380d79dac4f902545c115f4683b11125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0075dc7f9c4823a0c51df0810cbbf5aeb3de880cf07bb60b8c5efd48f1d0518e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e809eff03c28a50a357e8259b0984ba2160492e57b4e6e6c7ef668f7b280b3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateNodeSelector",
    jsii_struct_bases=[],
    name_mapping={"accelerator": "accelerator"},
)
class CloudRunV2JobTemplateTemplateNodeSelector:
    def __init__(self, *, accelerator: builtins.str) -> None:
        '''
        :param accelerator: The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/jobs/gpu for configuring GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#accelerator CloudRunV2Job#accelerator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e5497472e372f7ab5d97d0b3b61aef7ce4ee0cce0ec23a1e30466efd41de59)
            check_type(argname="argument accelerator", value=accelerator, expected_type=type_hints["accelerator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator": accelerator,
        }

    @builtins.property
    def accelerator(self) -> builtins.str:
        '''The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/jobs/gpu for configuring GPU.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#accelerator CloudRunV2Job#accelerator}
        '''
        result = self._values.get("accelerator")
        assert result is not None, "Required property 'accelerator' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateNodeSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateNodeSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateNodeSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__937bf4d7ae460a83489a09dada9f4860e4ac0d46bee49165e80f55b8e25ea5e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="acceleratorInput")
    def accelerator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorInput"))

    @builtins.property
    @jsii.member(jsii_name="accelerator")
    def accelerator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accelerator"))

    @accelerator.setter
    def accelerator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77b53fce00a95deda04d49208becda4c547559eb056cbb3bec65eae9b0f0948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accelerator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateNodeSelector]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateNodeSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateNodeSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01df8dbe4d6c726a43c006f23b980cdb5f5f9041d9fe80f61d21b01e6bc2d2fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcc2c9b2aa2dc6823c150e5c41a804c67fd8db5961490e2704cb0efb6c3c5793)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e881a5c6c703d07af5e4c2ae7aed091742858de96a505177a930b01cc0123e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainers", [value]))

    @jsii.member(jsii_name="putNodeSelector")
    def put_node_selector(self, *, accelerator: builtins.str) -> None:
        '''
        :param accelerator: The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/jobs/gpu for configuring GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#accelerator CloudRunV2Job#accelerator}
        '''
        value = CloudRunV2JobTemplateTemplateNodeSelector(accelerator=accelerator)

        return typing.cast(None, jsii.invoke(self, "putNodeSelector", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bd43104b5650c65f76e1688faf81ace3c37b42bb7807f7c8a20462b2242395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="putVpcAccess")
    def put_vpc_access(
        self,
        *,
        connector: typing.Optional[builtins.str] = None,
        egress: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connector: VPC Access connector name. Format: projects/{project}/locations/{location}/connectors/{connector}, where {project} can be project id or number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#connector CloudRunV2Job#connector}
        :param egress: Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#egress CloudRunV2Job#egress}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#network_interfaces CloudRunV2Job#network_interfaces}
        '''
        value = CloudRunV2JobTemplateTemplateVpcAccess(
            connector=connector, egress=egress, network_interfaces=network_interfaces
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccess", [value]))

    @jsii.member(jsii_name="resetContainers")
    def reset_containers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainers", []))

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetExecutionEnvironment")
    def reset_execution_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionEnvironment", []))

    @jsii.member(jsii_name="resetMaxRetries")
    def reset_max_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxRetries", []))

    @jsii.member(jsii_name="resetNodeSelector")
    def reset_node_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeSelector", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetVpcAccess")
    def reset_vpc_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccess", []))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(self) -> CloudRunV2JobTemplateTemplateContainersList:
        return typing.cast(CloudRunV2JobTemplateTemplateContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelector")
    def node_selector(self) -> CloudRunV2JobTemplateTemplateNodeSelectorOutputReference:
        return typing.cast(CloudRunV2JobTemplateTemplateNodeSelectorOutputReference, jsii.get(self, "nodeSelector"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "CloudRunV2JobTemplateTemplateVolumesList":
        return typing.cast("CloudRunV2JobTemplateTemplateVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccess")
    def vpc_access(self) -> "CloudRunV2JobTemplateTemplateVpcAccessOutputReference":
        return typing.cast("CloudRunV2JobTemplateTemplateVpcAccessOutputReference", jsii.get(self, "vpcAccess"))

    @builtins.property
    @jsii.member(jsii_name="containersInput")
    def containers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainers]]], jsii.get(self, "containersInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="executionEnvironmentInput")
    def execution_environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionEnvironmentInput"))

    @builtins.property
    @jsii.member(jsii_name="maxRetriesInput")
    def max_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelectorInput")
    def node_selector_input(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateNodeSelector]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateNodeSelector], jsii.get(self, "nodeSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessInput")
    def vpc_access_input(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateVpcAccess"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateVpcAccess"], jsii.get(self, "vpcAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__347b666bffd90a2ce4c4dd3a05a616042927095ed98dcbecb03472fbc254aa08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionEnvironment")
    def execution_environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionEnvironment"))

    @execution_environment.setter
    def execution_environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377ccd8ec5b9eb7b84ee930857bce5b053d53961ee123b3400363b231f78cf05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionEnvironment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxRetries"))

    @max_retries.setter
    def max_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2da0e112210f09f7449ff80c8b19ec95bca2797299655a040a0233905977f02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f9283b98bd0ea3b5d9a96ba2f2329ff9e758081da99e5d7e42066773765611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de418f276715744464dd408ac8c1b2437e7096842ec08a26ac89403db8de6419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2JobTemplateTemplate]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91483e98fac22bfa8f4acd24c8e7769ea86bd527ae671fff3c66679762a9d32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumes",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "cloud_sql_instance": "cloudSqlInstance",
        "empty_dir": "emptyDir",
        "gcs": "gcs",
        "nfs": "nfs",
        "secret": "secret",
    },
)
class CloudRunV2JobTemplateTemplateVolumes:
    def __init__(
        self,
        *,
        name: builtins.str,
        cloud_sql_instance: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        empty_dir: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateVolumesEmptyDir", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateVolumesGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        nfs: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateVolumesNfs", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["CloudRunV2JobTemplateTemplateVolumesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Volume's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        :param cloud_sql_instance: cloud_sql_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#cloud_sql_instance CloudRunV2Job#cloud_sql_instance}
        :param empty_dir: empty_dir block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#empty_dir CloudRunV2Job#empty_dir}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#gcs CloudRunV2Job#gcs}
        :param nfs: nfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#nfs CloudRunV2Job#nfs}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret CloudRunV2Job#secret}
        '''
        if isinstance(cloud_sql_instance, dict):
            cloud_sql_instance = CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance(**cloud_sql_instance)
        if isinstance(empty_dir, dict):
            empty_dir = CloudRunV2JobTemplateTemplateVolumesEmptyDir(**empty_dir)
        if isinstance(gcs, dict):
            gcs = CloudRunV2JobTemplateTemplateVolumesGcs(**gcs)
        if isinstance(nfs, dict):
            nfs = CloudRunV2JobTemplateTemplateVolumesNfs(**nfs)
        if isinstance(secret, dict):
            secret = CloudRunV2JobTemplateTemplateVolumesSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2efda8447a649b91f9c7e7ef6e6e32c111cd2cdfbb31a9b8fda10d219a512784)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument cloud_sql_instance", value=cloud_sql_instance, expected_type=type_hints["cloud_sql_instance"])
            check_type(argname="argument empty_dir", value=empty_dir, expected_type=type_hints["empty_dir"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument nfs", value=nfs, expected_type=type_hints["nfs"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if cloud_sql_instance is not None:
            self._values["cloud_sql_instance"] = cloud_sql_instance
        if empty_dir is not None:
            self._values["empty_dir"] = empty_dir
        if gcs is not None:
            self._values["gcs"] = gcs
        if nfs is not None:
            self._values["nfs"] = nfs
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def name(self) -> builtins.str:
        '''Volume's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#name CloudRunV2Job#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_sql_instance(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance"]:
        '''cloud_sql_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#cloud_sql_instance CloudRunV2Job#cloud_sql_instance}
        '''
        result = self._values.get("cloud_sql_instance")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance"], result)

    @builtins.property
    def empty_dir(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateVolumesEmptyDir"]:
        '''empty_dir block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#empty_dir CloudRunV2Job#empty_dir}
        '''
        result = self._values.get("empty_dir")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateVolumesEmptyDir"], result)

    @builtins.property
    def gcs(self) -> typing.Optional["CloudRunV2JobTemplateTemplateVolumesGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#gcs CloudRunV2Job#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateVolumesGcs"], result)

    @builtins.property
    def nfs(self) -> typing.Optional["CloudRunV2JobTemplateTemplateVolumesNfs"]:
        '''nfs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#nfs CloudRunV2Job#nfs}
        '''
        result = self._values.get("nfs")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateVolumesNfs"], result)

    @builtins.property
    def secret(self) -> typing.Optional["CloudRunV2JobTemplateTemplateVolumesSecret"]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret CloudRunV2Job#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateVolumesSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance:
    def __init__(
        self,
        *,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#instances CloudRunV2Job#instances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad511c231ea44cd56ef4e7cf2e4444bc40f314be4f8a84e7cd353b72dc68d6aa)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instances is not None:
            self._values["instances"] = instances

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#instances CloudRunV2Job#instances}
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateVolumesCloudSqlInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesCloudSqlInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44cdf22bd5198e665e0276e26352e798b7705ff853b195e713668907ab8925e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstances")
    def reset_instances(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstances", []))

    @builtins.property
    @jsii.member(jsii_name="instancesInput")
    def instances_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instancesInput"))

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91cd546f6caf53b096e315e52e4af0473f78bacaa0f433b7bafcae5de772f06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b98c218cab5096821dfc2c685b47576a5efcbe50c99e67eddbc98d22b3c58b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesEmptyDir",
    jsii_struct_bases=[],
    name_mapping={"medium": "medium", "size_limit": "sizeLimit"},
)
class CloudRunV2JobTemplateTemplateVolumesEmptyDir:
    def __init__(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#medium CloudRunV2Job#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#size_limit CloudRunV2Job#size_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34721777cadf19e2581620ed3dd7908e3d787e5c2728ed8f5eda4d2183f426ad)
            check_type(argname="argument medium", value=medium, expected_type=type_hints["medium"])
            check_type(argname="argument size_limit", value=size_limit, expected_type=type_hints["size_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if medium is not None:
            self._values["medium"] = medium
        if size_limit is not None:
            self._values["size_limit"] = size_limit

    @builtins.property
    def medium(self) -> typing.Optional[builtins.str]:
        '''The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#medium CloudRunV2Job#medium}
        '''
        result = self._values.get("medium")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_limit(self) -> typing.Optional[builtins.str]:
        '''Limit on the storage usable by this EmptyDir volume.

        The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#size_limit CloudRunV2Job#size_limit}
        '''
        result = self._values.get("size_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVolumesEmptyDir(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateVolumesEmptyDirOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesEmptyDirOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8643e7935e912c87f4822c809828c36edbe05b311a2724f39747c3de3422f5d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMedium")
    def reset_medium(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMedium", []))

    @jsii.member(jsii_name="resetSizeLimit")
    def reset_size_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSizeLimit", []))

    @builtins.property
    @jsii.member(jsii_name="mediumInput")
    def medium_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediumInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeLimitInput")
    def size_limit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="medium")
    def medium(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "medium"))

    @medium.setter
    def medium(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bca9315459084863e896c22339bc9343b6d546cb2958e972ee1671b801bee4cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "medium", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeLimit")
    def size_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeLimit"))

    @size_limit.setter
    def size_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d471906e36219df62dc7f8c71380ba01fbebb3a6af54507c4a10e715e88a2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesEmptyDir]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesEmptyDir], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesEmptyDir],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3f1dd2bd63005c53086059d34b6a2bfec5899f1077792bbee5df5473233233c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "read_only": "readOnly"},
)
class CloudRunV2JobTemplateTemplateVolumesGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket: Name of the cloud storage bucket to back the volume. The resource service account must have permission to access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#bucket CloudRunV2Job#bucket}
        :param read_only: If true, mount this volume as read-only in all mounts. If false, mount this volume as read-write. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#read_only CloudRunV2Job#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe360cf2b0afba3e4c0e05837218bacc01a3103050366ca2e13386c066a8e2e9)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Name of the cloud storage bucket to back the volume.

        The resource service account must have permission to access the bucket.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#bucket CloudRunV2Job#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount this volume as read-only in all mounts. If false, mount this volume as read-write.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#read_only CloudRunV2Job#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVolumesGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateVolumesGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0094c8ef05fc3a2d4af25484d4180515722c7975ca3cefd92f8e698aefafc8a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa73b401a40bb231f8093c9a10181d6381aa3be01689e456ac87a3c42ef01617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013c5fe68997f9fe11bff40a6748513c97f6295ec87b5cba8d7a3b7f5fddd1d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesGcs]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d9ba8122ebd13cfde4076f88ffc6ff2c15a6111e435ab3dfeba1a5911515c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b420af9d237d1cf7718c884934b1349c18199d1c7d43a44cd2c9b896949f494)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTemplateTemplateVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fea507ceeeade2688aab8e86a707b3d50809eb60321d4fc17008a098aaf4f5d8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTemplateTemplateVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f732a040e3ac19917a0336bbf9df6ea58470ebe8d7e33173538ddc5d91233d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09e27249fada4a271c7c8e43d541e940a0f17361a1b49a701906b7ba7da0b4f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac3143ff419bdd8bc6700023e0bd203b14df084315fb575fac690b7dec30c0f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb87ff97b7825577d0e5c4f10ac2423cd90fe2c1c11a3596b669e522518118ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesNfs",
    jsii_struct_bases=[],
    name_mapping={"server": "server", "path": "path", "read_only": "readOnly"},
)
class CloudRunV2JobTemplateTemplateVolumesNfs:
    def __init__(
        self,
        *,
        server: builtins.str,
        path: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param server: Hostname or IP address of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#server CloudRunV2Job#server}
        :param path: Path that is exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#path CloudRunV2Job#path}
        :param read_only: If true, mount this volume as read-only in all mounts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#read_only CloudRunV2Job#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aab6b8cb71c7e1058c33c4503be13c6a227a8eceedb36f0100c9f826acccb2c)
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server": server,
        }
        if path is not None:
            self._values["path"] = path
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def server(self) -> builtins.str:
        '''Hostname or IP address of the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#server CloudRunV2Job#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path that is exported by the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#path CloudRunV2Job#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount this volume as read-only in all mounts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#read_only CloudRunV2Job#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVolumesNfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateVolumesNfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesNfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc83ab9f8c0d52614c71151df684c8f3e8399a6096eef08a2495b42308fa01be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlyInput")
    def read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "readOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06803649e4b9b3a9eff699293368bde5e58191e06c5bd1bbd0f83c757f18094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readOnly")
    def read_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "readOnly"))

    @read_only.setter
    def read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b285d1de48e6ac2a04c13e0024583fc18892fa87d0b020cc92e0d509002c214)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034afb548fff8485f7bd56082442c49f208f81270fe8afbd12e53cdf5a99c2fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesNfs]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesNfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesNfs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ec846829c6705622c7d1bae6696326cc6490db0cc9b1f2713291946423448ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e2e23ad83b2bc418c85c4cfe9d946c08486d90623d8d933f63f28286f199ed1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCloudSqlInstance")
    def put_cloud_sql_instance(
        self,
        *,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#instances CloudRunV2Job#instances}
        '''
        value = CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance(
            instances=instances
        )

        return typing.cast(None, jsii.invoke(self, "putCloudSqlInstance", [value]))

    @jsii.member(jsii_name="putEmptyDir")
    def put_empty_dir(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#medium CloudRunV2Job#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#size_limit CloudRunV2Job#size_limit}
        '''
        value = CloudRunV2JobTemplateTemplateVolumesEmptyDir(
            medium=medium, size_limit=size_limit
        )

        return typing.cast(None, jsii.invoke(self, "putEmptyDir", [value]))

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket: Name of the cloud storage bucket to back the volume. The resource service account must have permission to access the bucket. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#bucket CloudRunV2Job#bucket}
        :param read_only: If true, mount this volume as read-only in all mounts. If false, mount this volume as read-write. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#read_only CloudRunV2Job#read_only}
        '''
        value = CloudRunV2JobTemplateTemplateVolumesGcs(
            bucket=bucket, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putNfs")
    def put_nfs(
        self,
        *,
        server: builtins.str,
        path: typing.Optional[builtins.str] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param server: Hostname or IP address of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#server CloudRunV2Job#server}
        :param path: Path that is exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#path CloudRunV2Job#path}
        :param read_only: If true, mount this volume as read-only in all mounts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#read_only CloudRunV2Job#read_only}
        '''
        value = CloudRunV2JobTemplateTemplateVolumesNfs(
            server=server, path=path, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putNfs", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        *,
        secret: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret CloudRunV2Job#secret}
        :param default_mode: Integer representation of mode bits to use on created files by default. Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#default_mode CloudRunV2Job#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#items CloudRunV2Job#items}
        '''
        value = CloudRunV2JobTemplateTemplateVolumesSecret(
            secret=secret, default_mode=default_mode, items=items
        )

        return typing.cast(None, jsii.invoke(self, "putSecret", [value]))

    @jsii.member(jsii_name="resetCloudSqlInstance")
    def reset_cloud_sql_instance(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudSqlInstance", []))

    @jsii.member(jsii_name="resetEmptyDir")
    def reset_empty_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmptyDir", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetNfs")
    def reset_nfs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNfs", []))

    @jsii.member(jsii_name="resetSecret")
    def reset_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecret", []))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstance")
    def cloud_sql_instance(
        self,
    ) -> CloudRunV2JobTemplateTemplateVolumesCloudSqlInstanceOutputReference:
        return typing.cast(CloudRunV2JobTemplateTemplateVolumesCloudSqlInstanceOutputReference, jsii.get(self, "cloudSqlInstance"))

    @builtins.property
    @jsii.member(jsii_name="emptyDir")
    def empty_dir(self) -> CloudRunV2JobTemplateTemplateVolumesEmptyDirOutputReference:
        return typing.cast(CloudRunV2JobTemplateTemplateVolumesEmptyDirOutputReference, jsii.get(self, "emptyDir"))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(self) -> CloudRunV2JobTemplateTemplateVolumesGcsOutputReference:
        return typing.cast(CloudRunV2JobTemplateTemplateVolumesGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="nfs")
    def nfs(self) -> CloudRunV2JobTemplateTemplateVolumesNfsOutputReference:
        return typing.cast(CloudRunV2JobTemplateTemplateVolumesNfsOutputReference, jsii.get(self, "nfs"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "CloudRunV2JobTemplateTemplateVolumesSecretOutputReference":
        return typing.cast("CloudRunV2JobTemplateTemplateVolumesSecretOutputReference", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstanceInput")
    def cloud_sql_instance_input(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance], jsii.get(self, "cloudSqlInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyDirInput")
    def empty_dir_input(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesEmptyDir]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesEmptyDir], jsii.get(self, "emptyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(self) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesGcs]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsInput")
    def nfs_input(self) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesNfs]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesNfs], jsii.get(self, "nfsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional["CloudRunV2JobTemplateTemplateVolumesSecret"]:
        return typing.cast(typing.Optional["CloudRunV2JobTemplateTemplateVolumesSecret"], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e165a3e0c8a54f6d1e576997b3c00c239e85fcd6f6bd515198337e6e04f0004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74469918576ad44b5a27b9c07ef921107afbdc236782fd08b19ec979b3aebbcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesSecret",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "default_mode": "defaultMode", "items": "items"},
)
class CloudRunV2JobTemplateTemplateVolumesSecret:
    def __init__(
        self,
        *,
        secret: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret CloudRunV2Job#secret}
        :param default_mode: Integer representation of mode bits to use on created files by default. Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#default_mode CloudRunV2Job#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#items CloudRunV2Job#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c2ce9892d0eea91e5fe6561e6f5fbe901a79314fa43071d7cc1b0080b30b9f)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument default_mode", value=default_mode, expected_type=type_hints["default_mode"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }
        if default_mode is not None:
            self._values["default_mode"] = default_mode
        if items is not None:
            self._values["items"] = items

    @builtins.property
    def secret(self) -> builtins.str:
        '''The name of the secret in Cloud Secret Manager.

        Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#secret CloudRunV2Job#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_mode(self) -> typing.Optional[jsii.Number]:
        '''Integer representation of mode bits to use on created files by default.

        Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#default_mode CloudRunV2Job#default_mode}
        '''
        result = self._values.get("default_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateVolumesSecretItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#items CloudRunV2Job#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateVolumesSecretItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVolumesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesSecretItems",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "version": "version", "mode": "mode"},
)
class CloudRunV2JobTemplateTemplateVolumesSecretItems:
    def __init__(
        self,
        *,
        path: builtins.str,
        version: builtins.str,
        mode: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param path: The relative path of the secret in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#path CloudRunV2Job#path}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#version CloudRunV2Job#version}
        :param mode: Integer octal mode bits to use on this file, must be a value between 01 and 0777 (octal). If 0 or not set, the Volume's default mode will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#mode CloudRunV2Job#mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa214c26301909c0ca01af0b4b5e874d1e1834e941b7f0e090739804d22c2f9)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "version": version,
        }
        if mode is not None:
            self._values["mode"] = mode

    @builtins.property
    def path(self) -> builtins.str:
        '''The relative path of the secret in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#path CloudRunV2Job#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''The Cloud Secret Manager secret version.

        Can be 'latest' for the latest value or an integer for a specific version

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#version CloudRunV2Job#version}
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        '''Integer octal mode bits to use on this file, must be a value between 01 and 0777 (octal).

        If 0 or not set, the Volume's default mode will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#mode CloudRunV2Job#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVolumesSecretItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateVolumesSecretItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesSecretItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1117cc13bc00d4bc8ecdd1658d0d037685b39064ffd15ee6a97ef91e04b11ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTemplateTemplateVolumesSecretItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c21de4dc0bc1bef20eccb0a1b170657ddf0dfb713e85360e45c3c7c42eb7b5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTemplateTemplateVolumesSecretItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__812988ece82c5d238c19dfb8c0ee4dd2f5df579a66613e996358655671451529)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ec341bbd7e68d59e3cf67f700ba4e55a67742fcacba75850c672ec58ba455db)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9cb07556910ea2121e84e4767be39344bb309242240ae793678370d49e261ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumesSecretItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumesSecretItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9531b834b3a4691f13f6d2d03aab5df4e71f6e177f29b7570d8a4c7fb42bc332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateVolumesSecretItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesSecretItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eef7d4a9eeebf3d3a632b4a38dc48ac805c5e289674e8120db1a279a9509a9c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44de3bf7fe5511da6f06d8c66fa561063bce6ad196fd5150ac141125b947866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e52236d61a41a4095e5728b29299e8c30fdbbada1c62968d52396714728d6bbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__311ec37039b9e24021b0ce54e43cc33ccb6752ef3d33ab4725bd0b4a7770d7f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVolumesSecretItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVolumesSecretItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVolumesSecretItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f875eb9aa562a304257fd61fb03d849256a55bded5523234b854aa01f123f7ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateVolumesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVolumesSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b11d39fba825746c4f8443186850325c95db1a9ed4c2b3d5569284cd0ff24f00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0f25d4099d9ff9c3ead14dc345db7f13c9acc3f2460cbbb4661e72b85111ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItems", [value]))

    @jsii.member(jsii_name="resetDefaultMode")
    def reset_default_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultMode", []))

    @jsii.member(jsii_name="resetItems")
    def reset_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItems", []))

    @builtins.property
    @jsii.member(jsii_name="items")
    def items(self) -> CloudRunV2JobTemplateTemplateVolumesSecretItemsList:
        return typing.cast(CloudRunV2JobTemplateTemplateVolumesSecretItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="defaultModeInput")
    def default_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultModeInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumesSecretItems]]], jsii.get(self, "itemsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultMode")
    def default_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultMode"))

    @default_mode.setter
    def default_mode(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3693e0fcf80a43c3535d9c4c502e30305e1daf333bf0cf4d264378a148f5dae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3325452d9a6e4c39be5900aea55e023fdd03dad0faca5b4c90a56111da20605b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2JobTemplateTemplateVolumesSecret]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVolumesSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6767072da9e286072052752fc82be7c6255f2a6c7981dcf0d21b12dba7914341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVpcAccess",
    jsii_struct_bases=[],
    name_mapping={
        "connector": "connector",
        "egress": "egress",
        "network_interfaces": "networkInterfaces",
    },
)
class CloudRunV2JobTemplateTemplateVpcAccess:
    def __init__(
        self,
        *,
        connector: typing.Optional[builtins.str] = None,
        egress: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connector: VPC Access connector name. Format: projects/{project}/locations/{location}/connectors/{connector}, where {project} can be project id or number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#connector CloudRunV2Job#connector}
        :param egress: Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#egress CloudRunV2Job#egress}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#network_interfaces CloudRunV2Job#network_interfaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c17a52ee17ee34bdfe8cec8a1ba1cb87a767632018d3cf50aa1cbbf3888820f)
            check_type(argname="argument connector", value=connector, expected_type=type_hints["connector"])
            check_type(argname="argument egress", value=egress, expected_type=type_hints["egress"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connector is not None:
            self._values["connector"] = connector
        if egress is not None:
            self._values["egress"] = egress
        if network_interfaces is not None:
            self._values["network_interfaces"] = network_interfaces

    @builtins.property
    def connector(self) -> typing.Optional[builtins.str]:
        '''VPC Access connector name. Format: projects/{project}/locations/{location}/connectors/{connector}, where {project} can be project id or number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#connector CloudRunV2Job#connector}
        '''
        result = self._values.get("connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def egress(self) -> typing.Optional[builtins.str]:
        '''Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#egress CloudRunV2Job#egress}
        '''
        result = self._values.get("egress")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces"]]]:
        '''network_interfaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#network_interfaces CloudRunV2Job#network_interfaces}
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVpcAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "subnetwork": "subnetwork", "tags": "tags"},
)
class CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: The VPC network that the Cloud Run resource will be able to send traffic to. At least one of network or subnetwork must be specified. If both network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If network is not specified, it will be looked up from the subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#network CloudRunV2Job#network}
        :param subnetwork: The VPC subnetwork that the Cloud Run resource will get IPs from. At least one of network or subnetwork must be specified. If both network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If subnetwork is not specified, the subnetwork with the same name with the network will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#subnetwork CloudRunV2Job#subnetwork}
        :param tags: Network tags applied to this Cloud Run job. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#tags CloudRunV2Job#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff1bc70e8a62096794ee68bb2d08c55e006cdaae43f01d8e6c486315f9ea362)
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument subnetwork", value=subnetwork, expected_type=type_hints["subnetwork"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network is not None:
            self._values["network"] = network
        if subnetwork is not None:
            self._values["subnetwork"] = subnetwork
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The VPC network that the Cloud Run resource will be able to send traffic to.

        At least one of network or subnetwork must be specified. If both
        network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If network is not specified, it will be
        looked up from the subnetwork.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#network CloudRunV2Job#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The VPC subnetwork that the Cloud Run resource will get IPs from.

        At least one of network or subnetwork must be specified. If both
        network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If subnetwork is not specified, the
        subnetwork with the same name with the network will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#subnetwork CloudRunV2Job#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Network tags applied to this Cloud Run job.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#tags CloudRunV2Job#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3c51a8f29831279f8e6f0c51cbc1f7ed9d04f1c31a99405f1572d88745cd21e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575a2f3a3a70852bb9126c480417e0b4c33e0d8c09490b97ff13e2b5c80753ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c6150639eb24702cc3d612ab2041d9f6d143e098d58b3e57191027f639a17c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8c9ffb18c8b1a6f19a0b189ec8c447b51928f4907d0706df9d4b5f3ac59081c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99b2019c8b3b45f5724eb1d6315985ff3a79d4138adf738dc566e494e687ffa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d475c98b1aa240407219801118730b068f3f903ca7bd00d273af9d1c2e06f3a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__905a5b41ea19095b6e4d696f599790208234cd077ce3bccd5d89c6f6d4d271f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetSubnetwork")
    def reset_subnetwork(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetwork", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetworkInput")
    def subnetwork_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetworkInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83419621559b9bf03ecc3e6b1a8e896660d4da82cb509ba9f89dce840cec8faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd6283046bd52f5c263a985646d7d58442a13e8c343abebd8588b8e59a6b794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ab30b6b0979d0d51fd6af22c918c151020f514e65ae575ebfc795663e0bd578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0967761f28b86ed60c0c1c1c7ed5b48e40353c67730d82b20554a95fbb489ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTemplateTemplateVpcAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTemplateTemplateVpcAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ffb1df4d1f80c55a7f82056036461ca0eb42beb5fab1f4bc84022fa580a7f86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkInterfaces")
    def put_network_interfaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c24f3e00cd4a83f7d539a6f327b02988333287710ffe21e505cb8c89532a1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterfaces", [value]))

    @jsii.member(jsii_name="resetConnector")
    def reset_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnector", []))

    @jsii.member(jsii_name="resetEgress")
    def reset_egress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEgress", []))

    @jsii.member(jsii_name="resetNetworkInterfaces")
    def reset_network_interfaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterfaces", []))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(
        self,
    ) -> CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesList:
        return typing.cast(CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesList, jsii.get(self, "networkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="connectorInput")
    def connector_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectorInput"))

    @builtins.property
    @jsii.member(jsii_name="egressInput")
    def egress_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "egressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfacesInput")
    def network_interfaces_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]]], jsii.get(self, "networkInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="connector")
    def connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connector"))

    @connector.setter
    def connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db8bff6a2b8439623cff62f26e997f4a62607ec7bf3288afd99841aa5a1e2fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="egress")
    def egress(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egress"))

    @egress.setter
    def egress(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40c9406cc02ff6a3c3f08d8d20855706782dfdc18b25e97e7efb417010d94f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2JobTemplateTemplateVpcAccess]:
        return typing.cast(typing.Optional[CloudRunV2JobTemplateTemplateVpcAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTemplateTemplateVpcAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddbedea60d7912e953ef7593d750b7d9a905a51d8d8c3a793940e25b0d933bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTerminalCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2JobTerminalCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTerminalCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTerminalConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTerminalConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcb8bf67498bd655273d156eebf17c7f44382115eb96cee67f81837ada23724a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2JobTerminalConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ccac3328cdceed9d4d331fead294f8521af05f5ad6ce5b894783e883bbfcc0f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2JobTerminalConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08fed643890bb180a678e549ad058057e188674e349f3630cacdaf9d6d8e898)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12f1fbe4c91c2ac876d214034672d7128236d507fc51e37a22adaa5398f24cb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__96f58e923d6dc919fce0dc48e65d4501b7b46f073483fca036cfea0b8e0234e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2JobTerminalConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTerminalConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__226b56ec0252138484bbd07dd3fbcdae71b1e48e6f2e14829386815df6ad3e6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="executionReason")
    def execution_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionReason"))

    @builtins.property
    @jsii.member(jsii_name="lastTransitionTime")
    def last_transition_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastTransitionTime"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "reason"))

    @builtins.property
    @jsii.member(jsii_name="revisionReason")
    def revision_reason(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionReason"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2JobTerminalCondition]:
        return typing.cast(typing.Optional[CloudRunV2JobTerminalCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2JobTerminalCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef231eab14d9079d7d036d806cd62db558fd4abe65fd75f455f2965fc993d67c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudRunV2JobTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#create CloudRunV2Job#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#delete CloudRunV2Job#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#update CloudRunV2Job#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b161e8bb2506db1821833fd23735cc942b73ffc04cb8be807f7a42b1e501aa69)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#create CloudRunV2Job#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#delete CloudRunV2Job#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_job#update CloudRunV2Job#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2JobTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2JobTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2Job.CloudRunV2JobTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80a625f0ab652e98f819d7ee710f3dc408906ad36a5f1ab01693add3c63e94c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b87585097b82b6e72ad7bc48d182b1287735e3d3c44d161302bb357e0c3cfd46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c470e38b08dcc59ec77e294055f289d17c8efdc72a7939b8e427d94ecead8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ce35add381bfa843edf6d3120f6e28048b015ab060d568929172f40760f865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d371260728b55ca6fade212777088b2675f288f3f4e843a4f417a3de9be092a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudRunV2Job",
    "CloudRunV2JobBinaryAuthorization",
    "CloudRunV2JobBinaryAuthorizationOutputReference",
    "CloudRunV2JobConditions",
    "CloudRunV2JobConditionsList",
    "CloudRunV2JobConditionsOutputReference",
    "CloudRunV2JobConfig",
    "CloudRunV2JobLatestCreatedExecution",
    "CloudRunV2JobLatestCreatedExecutionList",
    "CloudRunV2JobLatestCreatedExecutionOutputReference",
    "CloudRunV2JobTemplate",
    "CloudRunV2JobTemplateOutputReference",
    "CloudRunV2JobTemplateTemplate",
    "CloudRunV2JobTemplateTemplateContainers",
    "CloudRunV2JobTemplateTemplateContainersEnv",
    "CloudRunV2JobTemplateTemplateContainersEnvList",
    "CloudRunV2JobTemplateTemplateContainersEnvOutputReference",
    "CloudRunV2JobTemplateTemplateContainersEnvValueSource",
    "CloudRunV2JobTemplateTemplateContainersEnvValueSourceOutputReference",
    "CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef",
    "CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRefOutputReference",
    "CloudRunV2JobTemplateTemplateContainersList",
    "CloudRunV2JobTemplateTemplateContainersOutputReference",
    "CloudRunV2JobTemplateTemplateContainersPorts",
    "CloudRunV2JobTemplateTemplateContainersPortsList",
    "CloudRunV2JobTemplateTemplateContainersPortsOutputReference",
    "CloudRunV2JobTemplateTemplateContainersResources",
    "CloudRunV2JobTemplateTemplateContainersResourcesOutputReference",
    "CloudRunV2JobTemplateTemplateContainersStartupProbe",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeGrpcOutputReference",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersList",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetOutputReference",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeOutputReference",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket",
    "CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocketOutputReference",
    "CloudRunV2JobTemplateTemplateContainersVolumeMounts",
    "CloudRunV2JobTemplateTemplateContainersVolumeMountsList",
    "CloudRunV2JobTemplateTemplateContainersVolumeMountsOutputReference",
    "CloudRunV2JobTemplateTemplateNodeSelector",
    "CloudRunV2JobTemplateTemplateNodeSelectorOutputReference",
    "CloudRunV2JobTemplateTemplateOutputReference",
    "CloudRunV2JobTemplateTemplateVolumes",
    "CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance",
    "CloudRunV2JobTemplateTemplateVolumesCloudSqlInstanceOutputReference",
    "CloudRunV2JobTemplateTemplateVolumesEmptyDir",
    "CloudRunV2JobTemplateTemplateVolumesEmptyDirOutputReference",
    "CloudRunV2JobTemplateTemplateVolumesGcs",
    "CloudRunV2JobTemplateTemplateVolumesGcsOutputReference",
    "CloudRunV2JobTemplateTemplateVolumesList",
    "CloudRunV2JobTemplateTemplateVolumesNfs",
    "CloudRunV2JobTemplateTemplateVolumesNfsOutputReference",
    "CloudRunV2JobTemplateTemplateVolumesOutputReference",
    "CloudRunV2JobTemplateTemplateVolumesSecret",
    "CloudRunV2JobTemplateTemplateVolumesSecretItems",
    "CloudRunV2JobTemplateTemplateVolumesSecretItemsList",
    "CloudRunV2JobTemplateTemplateVolumesSecretItemsOutputReference",
    "CloudRunV2JobTemplateTemplateVolumesSecretOutputReference",
    "CloudRunV2JobTemplateTemplateVpcAccess",
    "CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces",
    "CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesList",
    "CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfacesOutputReference",
    "CloudRunV2JobTemplateTemplateVpcAccessOutputReference",
    "CloudRunV2JobTerminalCondition",
    "CloudRunV2JobTerminalConditionList",
    "CloudRunV2JobTerminalConditionOutputReference",
    "CloudRunV2JobTimeouts",
    "CloudRunV2JobTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__a07681793f9e8d8de4337a42ae6bfae6f39cd0ee924647af81415362b94aa61a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    template: typing.Union[CloudRunV2JobTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[CloudRunV2JobBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    client_version: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_stage: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudRunV2JobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3911cb5c2c76c1582ee3343e30ebcdabee98783c4fac57fffc18b280f82774ad(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69be8e25e0fffbe830209e88bf65e9b764144fcabdae2f7aaffb735384578eeb(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f174589e82aea9d58560a23745ee0f90ab435e50048673816be7c728d63c279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3032cbf7fe284bfd8979ac9aed71a54a44cee34e75b92cfc4deddd46a3e6ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3492ffdbbfbfc07aab24dc225c08b5aa02835f4ab2e1bdc29a5de5af6a13bf5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5489848e74075b947a68dd1809bb0586b2cbd4ae642d8c953d69952676e01b7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ddeea4f44a85221db965b5a8ee56ca273f93571907bcc7ca11c39affe80b46(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffad024fca4ebc7335bfc3c9688411fe708353b4463b713289dad7d64552345(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37645e50e6c12d6d4fed18b03be9196ef57eb8c779c275abd084920e3bc60153(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21add8c8b194867cd7fd56e27e348e5e3ab370845416b790642c3fef0262eca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005fa1a81f317f712a598377a6d14ae05e9b5969ae6d1f54fedbc21818913d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba391bf182ebfe028ed7b08be2d884aec42484adc436539313494138a65c3e16(
    *,
    breakglass_justification: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ded0e475ace79d08a6ab84a68d70b3c51dad0f7362a49125fe686c79a9026190(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffab614a2dd0b825a36faf9fb13ff86b532de7d795a057f604446851762d485(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1239116a26c803f6cc3037c307c4e0b68a4e217727be1fcd92c575d10137620b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89448547e632da742fec2d243d83b950beb7d4496d784ab1cf2779c883aa2ee6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45402e6e6434bd7a205ecfada75876b9ea6b4c9363877059796af269cd355e29(
    value: typing.Optional[CloudRunV2JobBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fde2e3b810cfb39ab3506131f6b8d10d88ad8ea5b289210727a4ac6c493d1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4a56664e70c4dae55809b492a2a4775bcbf49a923f1c4f43ed6a511c425b4d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c224664ab824c06c88aa169cd91b44b97ab1cca4ebf17f699f297c9d85f465(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5acbc4394a8159a66efb684bbd87d965323d311928aa37055bc3b440eb8c2136(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360de86a5873e4e62676aefa8c6b9e05bb15d060133635bb20a9180f9265062f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aece4806a8b42fae4e587e4cc2b9d78e6c24eb321fd01c06a14bdf4a0d704be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac21bce80efd068eeac872d644c1c490774287aa8cb29ea7b5ebb334c71b183(
    value: typing.Optional[CloudRunV2JobConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f8bf68c0796fb3d93a12b7b29a955b2dd06fc5989f084db5b2d50e226ad57c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    template: typing.Union[CloudRunV2JobTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[CloudRunV2JobBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    client_version: typing.Optional[builtins.str] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_stage: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CloudRunV2JobTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec635d02fd4bc972e524ada5c9a02898b70c41377b9312f37cb56082ad90fd1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abc8d40f6ed8d90ead12827ecf28009ee8fcbfa7659bd6c1632a5afee21012d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a1e6c3e415150c141c36664b697ebb4ed23184740d9e7a3ea2e5851cf7ab71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6934d9f54f488a101683250aa4d83c309495f8fcc129ad87a6329227d62bf0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98553783f8999b9d64eb2740b7dc6d688949cd61e7b4735b4663ab65556cd3b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e26b25692eeacec30992a3c80a99bc44e1345d33676532fbe964602808e5fcd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69d8936e200034ec1b65525d15d974d7eaf2c8dd03f21901d4417e520b90fa2(
    value: typing.Optional[CloudRunV2JobLatestCreatedExecution],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0818b6915563663838f531f7d254e53513db3f5dab8ca1da962fe6277eef8d1(
    *,
    template: typing.Union[CloudRunV2JobTemplateTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    parallelism: typing.Optional[jsii.Number] = None,
    task_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac249cb401b1f24c3266e1465c872c8cb5990d66b63a54b3fbf8705d4be5c3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a42038d353a47fc830b0a6cf7c66ea1b6c40a3f076abf7624145f2cb0895a4c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91821f36b7ef9ad1ed6d730f1b5e54f2633bc2e886e51958a2202b4955020e62(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9a1a5c13c235584cf787e72aa94af4d35508ba85e3d8d5757e65f9064562f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c21f9ce68812af6224e9f3619e3f132ea1e8a837d932c0a02966750e74c095(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b684a19af1cdbee6d9443e97976149fa09a0d778219c8b7989df5cbdf801baaf(
    value: typing.Optional[CloudRunV2JobTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2779fd9a2ac837ebc8d3873d9ae10154a55dd22672673169e3db2400926b98(
    *,
    containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    execution_environment: typing.Optional[builtins.str] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    node_selector: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateNodeSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vpc_access: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateVpcAccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51113b1e358b9d5401a891c8f50df4ef92fa51086ea2f9f46a18089fa21510a1(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersPorts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resources: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateContainersResources, typing.Dict[builtins.str, typing.Any]]] = None,
    startup_probe: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateContainersStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0adbf791027f9f38fde86406e34c5b69a08a114987dc89e7a3847da1865510b(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
    value_source: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateContainersEnvValueSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53abdfc36772332d7a6c4ff794bfb6793d3fcb7785fdae61a169d126c166d3d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10b1c32d5ce827a8bae45afa84712ad781ccad33c3509a4fa5f1c3c0b7d7e2c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed964016dc6a304878e9cc3aaaa58a0e5dd6457e7dead7f478de7f0c703bbe18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4df7e6f049bc48546dfe3d296addc1752fbb77c2438a18076abbbea9514845(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aeaef55731865a322c47de6f8fc25c12751350d46df2c6e9b67b36be2670b0f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e33ed9eb36d2ecb670c941268b26189e1dc41dbdae435031666a761d32590a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cf77875d784d4135cbcc92446846de93c2b5394a6901c539a832c03d5ecb6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75565f47816ed87efdd1ffc5d1d916bd8d4ce11913a7391bf43056903b2142c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__315fd177349143b4e28bf10b143571871f46acd68318d68ed1195086bba6763e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e833b808cbaab0121e7dd377fdf4d34e7112b9adfd52a39a34d65d4e3650d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4a11cef8f0b5f4087b382b1cfdaf109a41d54e9202c107ee423c3eedaf3c95(
    *,
    secret_key_ref: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b524cbcaf75f6d25ec86da188b0bfc781b96c7c16b807ad016caebfb03757f7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6aeea1fb54e86bc647f81451db6a1154a0a7f31941ab222ccdec0d7e7c75229(
    value: typing.Optional[CloudRunV2JobTemplateTemplateContainersEnvValueSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5084de4f0073ddbc77e1d0ee0810b35a23b09ca01ca2fdb255c2388321ec74bb(
    *,
    secret: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100f5b6b026228fa31832349e461b104ef5ab0130f7c38c503fb54577ce2b353(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2736f5929d4ddf250e24aa3aa0aa2536ccedf670de3ae103d2407e0cfbe79681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96cd8dadad902873b3608fe9a587379ede51219749bcc5d3db0c89a382b5c5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4889c771699bcea2f20299eaa83301792df691496493f42d4a44ef332c27f39(
    value: typing.Optional[CloudRunV2JobTemplateTemplateContainersEnvValueSourceSecretKeyRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f148dc004fea11892a81abf94cc7871aee642b7e26fc9064103cb6ef6393205(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a25ada2d3713da0156abe27adafee12d0ac2d20557c455e5821aeaf28bff38(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16aefb2e71bf1f6f33ef7dead6c7b4bf4d970da9ea3b5b17c73d190b185b740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf5d5a8855af64a4f162715323e93d5573091183436a26c6b37ef95a9932311(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae3ad9d37549bfcd4fc3a91a10433f94bd37cbb8a748b2011f1fd3e7887d777(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58e69f9eaee75016931477e6b3f0bff56eb47723a7b1f7093220882cb78736d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2cf314fc1149c7a7e4f81e5d91394040d7fe3f66f9ef48ecd2bc48ced1cbc37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eadeb12b0b65e0ebdf4cad5021798c560700b462026965db2cb6a5c25482cc7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0a7ebec73a4590c352139cd1ecf7374654949cf5e7e36627ef1ef545269c29(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersPorts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea7214917463382309b760dd78760840a277fa3d05d105a26c337efed41393f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ac9d7c983cb4f45c158c4593b5c2480673067736e1717039ecde793e53c871(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0a6476eebd27a35e93b548071b29656d1594b7e5529aa3bbff93fbfd9255be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93dc6858c4369e937dfe46b75fcf876259c549099a27070e81bec12c5101eb9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3cf3c9c775b8beb8756b17ad2555dae9c40dc02fba60a17183fc75bd28ae9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4c2c79a61d05ff2613e1c94eb0db1ec509143eeb3668d4a6344b50a1246dbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5340b1110cb96708f8ca520b61cb98b51392bfbde09709561f90f3e890260bcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31d54cd1e213ac8c2b50bb97a16cb12780bc5d31456da4e4776e85cdd2bb4a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08bb73d3381bd120a9d5c81be1516738a0cd5376201f984b5ff0b0f54c9b7cc5(
    *,
    container_port: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb1c0fa8ea4645642736bdfcecd1206135fb79102ad92ee9f50ccbeaa951d8b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f56e64ff610ec71230f3eea6c8807559988631c894d01281ab02f317e7818a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757503a5ea5409a8b615c9151d011b6c20c6488406da1c9e0a9feb81304795d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3264ab737b24b0c6e56d70132f0c252e66c75828296b178030352330366de6d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c249149754746bbc684578e64e0f0cba7cf74096ca74012d872871d76e84d074(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ca76183292a4c5e75a9352db91962effb9a2f855e74384aa106dcb33136b41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersPorts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff4151ed166f9728fe0b985db51d0e18a73aa5d9b43d4b4f086a5283f131229(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301924481b0880f265a79b07d6c3d5b762b03ef3b325eff4b6f7e64a5f60289b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54a2f222d3317acee428cd46668381b1c06ff28aabe41ea0e69b270f3d7b65d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d390090891688d9d609bc8f1025f1664834cd61b9910b85470bb83fec8805ca1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersPorts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3642cbe6aabdad011daa9c0711bd672f0404a966de18bb6014ee7f5b2ca53b4(
    *,
    limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a594219de7fb563a855529735df99a4adbc0bf4fcc8dec49d136366d17abf71b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42480f3677cf933329dda247ef12c88bd2051c3051036a6b76fb1951a5441e68(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676a5d58485494d64ef72970170813d504093a2ff46e217c8681e1acecd92fdc(
    value: typing.Optional[CloudRunV2JobTemplateTemplateContainersResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1192aea2ac00145a2eedde8be1c207800749427dbfb10203a4663f5bb14e63(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afae6975ae039cbbcc64f04a0a696dd8d5db62c3fe023b485361cfff73e4138(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93e4935389b6728e8f45149f6b00b16fd2106ae7131b7ca759fef621931a1331(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc6c02b010319033ffb48e8371a953fcd29dd936900dec1f42f436a3505c684(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3afefa9b2310f5ee3a6a8d50d145c62c92e52f418442369deadd8d18108d61b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f07dc3d60bbe4d17289943825f6bf9ad545fa7cd3af742127bf7dd623f76493(
    value: typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648d2e2699f499f14a4816a067195b5c80fb1fcbdcff30ec051aa4a2dbf3e1e2(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e008acfc5bf6b83d78100c84fe48794226a5bb93e677b3a8e4cafd2b27717c(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29e4af90d00f09bb364c74d815ff73119a69a4cce9ce6dda5756e5d4f34704b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35332ef6301b6f8589852d38fb90ce0e44cf4dbcc9d7b4c605306f95123ec24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96dc57fb29fe0ca592fc856a35f203130e130d7ff02bd9c77d373e60156acb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457a97251358721c323e8420dab941ede1240197331a20eb55cdbd7a4485ae5a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16198255a9df18315d520352e90dcafa6bce09c35c1ae3d26b63b78bc4e161fb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd3a1f918f45d47be7a7ce414cfb1cfc0581a92d9219799048998f4d9b34e4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e91ffc046236a93fa7684607d8b3e46ac8edd24d0b5470504f2240aad0877c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc802291b397cfeac9222d5abc245217ad18b6fab9ea0451c7e15a670dba9afc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00736a76baef53ec0c693e54b8a7a032455cdcad0a0bce244069817bd02c2279(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3698ad57bfad1fbbb20d354929b7ea5e52657b36330954403fd6addc33e0deb8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3251c835b88a0753cbd4a51eee46477dcf2acf4b89a48ce64a51d01c8cc3c444(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a43df340d16d1bac577202024191337f84e2f55f3dd19bc873405c468c305d1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8df33ad7eb4a94e55ecae41cd75b93d64ae34f7404f0cada71dd3abda69302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3a8964fbd8fed096bb53ebf162454fbdf5d90775b560d260bd047d79a59424(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e077058ed8557628f40289a0968daf86d55687153447551b407330557d6aadb(
    value: typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04423d527afc9391a104f47d239269fbf367d79c29f7bf22083a677fe1414636(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9a754b1bca5b0d2eba0c3e72d60c837962751cab43e5276b5aac767e57eff1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fd9c11384173a943635b1aa45676e47504de9cb7c4e38515a9399666d1bf62(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c284b74c7993ab998e43a3ba3725108c39b585b2e429e2ffac510e9beb58b3a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31aabc8c1a87045516352d551f139595a3cfd8389c1119401693758e7f16c51f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530c4d14c3493071d00a5a546af06fa6347a123b34e9a6cc47ffd0e0fa01458a(
    value: typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__549568f1cc4d7e0519d04283b2c8d52ff913df023ba08cf0f598f439f718ee59(
    *,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5e8fa5936618f80d98178f08146648cb1abcee5cfbb758d10c422ac7690168(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c712f94bfc8649f14a71f336bccb9a79a342a7d9106f3be21817d40d1bcca2f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28fa174e2ea71a7dd2a354b629a89091d6a9802e1d32c1b254d345cdfcc0000(
    value: typing.Optional[CloudRunV2JobTemplateTemplateContainersStartupProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443c0155fad35f0b43f55ae6f3b55661989c820846fdc4d8c461677d433f38cb(
    *,
    mount_path: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b623fef922ddceeede59379e378ffe17b56e620cf4422d01e785ad12d2fb88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4633bf3fd8e485df31f2d34d3190f39a710ccb0ad792603039c02a51664f7c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee44ec8a2092bc718a32c33092b7b63e7234a14cd8229ccac1c713235da78113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba3c8071457b9e72c6fe84c077c01ed4d642e2364f9a7d4b7e3ea1eec5daa8f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39e720d874f94afd3c41c3ae925ad788e5346a2dfedd3cb8a16c0f5a5b0c2a64(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527e927a96b1d064df69abef020dfbe8275ad51f68b8ab5e8c03d379527c3714(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateContainersVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b80a77f4ceaf9ccb4f21148c89ee6033e0d85a7089fa70b1356d22a0c6ee3d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c32eeaf8f4a4f64e194acd8eeb7ccf380d79dac4f902545c115f4683b11125(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0075dc7f9c4823a0c51df0810cbbf5aeb3de880cf07bb60b8c5efd48f1d0518e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e809eff03c28a50a357e8259b0984ba2160492e57b4e6e6c7ef668f7b280b3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateContainersVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e5497472e372f7ab5d97d0b3b61aef7ce4ee0cce0ec23a1e30466efd41de59(
    *,
    accelerator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937bf4d7ae460a83489a09dada9f4860e4ac0d46bee49165e80f55b8e25ea5e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77b53fce00a95deda04d49208becda4c547559eb056cbb3bec65eae9b0f0948(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01df8dbe4d6c726a43c006f23b980cdb5f5f9041d9fe80f61d21b01e6bc2d2fa(
    value: typing.Optional[CloudRunV2JobTemplateTemplateNodeSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc2c9b2aa2dc6823c150e5c41a804c67fd8db5961490e2704cb0efb6c3c5793(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e881a5c6c703d07af5e4c2ae7aed091742858de96a505177a930b01cc0123e8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateContainers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bd43104b5650c65f76e1688faf81ace3c37b42bb7807f7c8a20462b2242395(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347b666bffd90a2ce4c4dd3a05a616042927095ed98dcbecb03472fbc254aa08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377ccd8ec5b9eb7b84ee930857bce5b053d53961ee123b3400363b231f78cf05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2da0e112210f09f7449ff80c8b19ec95bca2797299655a040a0233905977f02(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f9283b98bd0ea3b5d9a96ba2f2329ff9e758081da99e5d7e42066773765611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de418f276715744464dd408ac8c1b2437e7096842ec08a26ac89403db8de6419(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91483e98fac22bfa8f4acd24c8e7769ea86bd527ae671fff3c66679762a9d32(
    value: typing.Optional[CloudRunV2JobTemplateTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2efda8447a649b91f9c7e7ef6e6e32c111cd2cdfbb31a9b8fda10d219a512784(
    *,
    name: builtins.str,
    cloud_sql_instance: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    empty_dir: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateVolumesEmptyDir, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateVolumesGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    nfs: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateVolumesNfs, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[CloudRunV2JobTemplateTemplateVolumesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad511c231ea44cd56ef4e7cf2e4444bc40f314be4f8a84e7cd353b72dc68d6aa(
    *,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cdf22bd5198e665e0276e26352e798b7705ff853b195e713668907ab8925e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91cd546f6caf53b096e315e52e4af0473f78bacaa0f433b7bafcae5de772f06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b98c218cab5096821dfc2c685b47576a5efcbe50c99e67eddbc98d22b3c58b9(
    value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesCloudSqlInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34721777cadf19e2581620ed3dd7908e3d787e5c2728ed8f5eda4d2183f426ad(
    *,
    medium: typing.Optional[builtins.str] = None,
    size_limit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8643e7935e912c87f4822c809828c36edbe05b311a2724f39747c3de3422f5d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca9315459084863e896c22339bc9343b6d546cb2958e972ee1671b801bee4cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d471906e36219df62dc7f8c71380ba01fbebb3a6af54507c4a10e715e88a2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f1dd2bd63005c53086059d34b6a2bfec5899f1077792bbee5df5473233233c(
    value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesEmptyDir],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe360cf2b0afba3e4c0e05837218bacc01a3103050366ca2e13386c066a8e2e9(
    *,
    bucket: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0094c8ef05fc3a2d4af25484d4180515722c7975ca3cefd92f8e698aefafc8a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa73b401a40bb231f8093c9a10181d6381aa3be01689e456ac87a3c42ef01617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013c5fe68997f9fe11bff40a6748513c97f6295ec87b5cba8d7a3b7f5fddd1d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d9ba8122ebd13cfde4076f88ffc6ff2c15a6111e435ab3dfeba1a5911515c0(
    value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b420af9d237d1cf7718c884934b1349c18199d1c7d43a44cd2c9b896949f494(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea507ceeeade2688aab8e86a707b3d50809eb60321d4fc17008a098aaf4f5d8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f732a040e3ac19917a0336bbf9df6ea58470ebe8d7e33173538ddc5d91233d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e27249fada4a271c7c8e43d541e940a0f17361a1b49a701906b7ba7da0b4f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3143ff419bdd8bc6700023e0bd203b14df084315fb575fac690b7dec30c0f6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb87ff97b7825577d0e5c4f10ac2423cd90fe2c1c11a3596b669e522518118ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aab6b8cb71c7e1058c33c4503be13c6a227a8eceedb36f0100c9f826acccb2c(
    *,
    server: builtins.str,
    path: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc83ab9f8c0d52614c71151df684c8f3e8399a6096eef08a2495b42308fa01be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06803649e4b9b3a9eff699293368bde5e58191e06c5bd1bbd0f83c757f18094(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b285d1de48e6ac2a04c13e0024583fc18892fa87d0b020cc92e0d509002c214(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034afb548fff8485f7bd56082442c49f208f81270fe8afbd12e53cdf5a99c2fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ec846829c6705622c7d1bae6696326cc6490db0cc9b1f2713291946423448ab(
    value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesNfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2e23ad83b2bc418c85c4cfe9d946c08486d90623d8d933f63f28286f199ed1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e165a3e0c8a54f6d1e576997b3c00c239e85fcd6f6bd515198337e6e04f0004(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74469918576ad44b5a27b9c07ef921107afbdc236782fd08b19ec979b3aebbcf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c2ce9892d0eea91e5fe6561e6f5fbe901a79314fa43071d7cc1b0080b30b9f(
    *,
    secret: builtins.str,
    default_mode: typing.Optional[jsii.Number] = None,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa214c26301909c0ca01af0b4b5e874d1e1834e941b7f0e090739804d22c2f9(
    *,
    path: builtins.str,
    version: builtins.str,
    mode: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1117cc13bc00d4bc8ecdd1658d0d037685b39064ffd15ee6a97ef91e04b11ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c21de4dc0bc1bef20eccb0a1b170657ddf0dfb713e85360e45c3c7c42eb7b5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812988ece82c5d238c19dfb8c0ee4dd2f5df579a66613e996358655671451529(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec341bbd7e68d59e3cf67f700ba4e55a67742fcacba75850c672ec58ba455db(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cb07556910ea2121e84e4767be39344bb309242240ae793678370d49e261ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9531b834b3a4691f13f6d2d03aab5df4e71f6e177f29b7570d8a4c7fb42bc332(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVolumesSecretItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef7d4a9eeebf3d3a632b4a38dc48ac805c5e289674e8120db1a279a9509a9c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44de3bf7fe5511da6f06d8c66fa561063bce6ad196fd5150ac141125b947866(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52236d61a41a4095e5728b29299e8c30fdbbada1c62968d52396714728d6bbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311ec37039b9e24021b0ce54e43cc33ccb6752ef3d33ab4725bd0b4a7770d7f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f875eb9aa562a304257fd61fb03d849256a55bded5523234b854aa01f123f7ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVolumesSecretItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b11d39fba825746c4f8443186850325c95db1a9ed4c2b3d5569284cd0ff24f00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0f25d4099d9ff9c3ead14dc345db7f13c9acc3f2460cbbb4661e72b85111ea4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3693e0fcf80a43c3535d9c4c502e30305e1daf333bf0cf4d264378a148f5dae2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3325452d9a6e4c39be5900aea55e023fdd03dad0faca5b4c90a56111da20605b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6767072da9e286072052752fc82be7c6255f2a6c7981dcf0d21b12dba7914341(
    value: typing.Optional[CloudRunV2JobTemplateTemplateVolumesSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c17a52ee17ee34bdfe8cec8a1ba1cb87a767632018d3cf50aa1cbbf3888820f(
    *,
    connector: typing.Optional[builtins.str] = None,
    egress: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff1bc70e8a62096794ee68bb2d08c55e006cdaae43f01d8e6c486315f9ea362(
    *,
    network: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c51a8f29831279f8e6f0c51cbc1f7ed9d04f1c31a99405f1572d88745cd21e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575a2f3a3a70852bb9126c480417e0b4c33e0d8c09490b97ff13e2b5c80753ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c6150639eb24702cc3d612ab2041d9f6d143e098d58b3e57191027f639a17c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c9ffb18c8b1a6f19a0b189ec8c447b51928f4907d0706df9d4b5f3ac59081c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b2019c8b3b45f5724eb1d6315985ff3a79d4138adf738dc566e494e687ffa8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d475c98b1aa240407219801118730b068f3f903ca7bd00d273af9d1c2e06f3a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__905a5b41ea19095b6e4d696f599790208234cd077ce3bccd5d89c6f6d4d271f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83419621559b9bf03ecc3e6b1a8e896660d4da82cb509ba9f89dce840cec8faa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd6283046bd52f5c263a985646d7d58442a13e8c343abebd8588b8e59a6b794(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ab30b6b0979d0d51fd6af22c918c151020f514e65ae575ebfc795663e0bd578(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0967761f28b86ed60c0c1c1c7ed5b48e40353c67730d82b20554a95fbb489ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffb1df4d1f80c55a7f82056036461ca0eb42beb5fab1f4bc84022fa580a7f86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c24f3e00cd4a83f7d539a6f327b02988333287710ffe21e505cb8c89532a1d0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2JobTemplateTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db8bff6a2b8439623cff62f26e997f4a62607ec7bf3288afd99841aa5a1e2fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40c9406cc02ff6a3c3f08d8d20855706782dfdc18b25e97e7efb417010d94f8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddbedea60d7912e953ef7593d750b7d9a905a51d8d8c3a793940e25b0d933bff(
    value: typing.Optional[CloudRunV2JobTemplateTemplateVpcAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb8bf67498bd655273d156eebf17c7f44382115eb96cee67f81837ada23724a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccac3328cdceed9d4d331fead294f8521af05f5ad6ce5b894783e883bbfcc0f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08fed643890bb180a678e549ad058057e188674e349f3630cacdaf9d6d8e898(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f1fbe4c91c2ac876d214034672d7128236d507fc51e37a22adaa5398f24cb0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96f58e923d6dc919fce0dc48e65d4501b7b46f073483fca036cfea0b8e0234e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226b56ec0252138484bbd07dd3fbcdae71b1e48e6f2e14829386815df6ad3e6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef231eab14d9079d7d036d806cd62db558fd4abe65fd75f455f2965fc993d67c(
    value: typing.Optional[CloudRunV2JobTerminalCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b161e8bb2506db1821833fd23735cc942b73ffc04cb8be807f7a42b1e501aa69(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80a625f0ab652e98f819d7ee710f3dc408906ad36a5f1ab01693add3c63e94c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87585097b82b6e72ad7bc48d182b1287735e3d3c44d161302bb357e0c3cfd46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c470e38b08dcc59ec77e294055f289d17c8efdc72a7939b8e427d94ecead8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ce35add381bfa843edf6d3120f6e28048b015ab060d568929172f40760f865(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d371260728b55ca6fade212777088b2675f288f3f4e843a4f417a3de9be092a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2JobTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

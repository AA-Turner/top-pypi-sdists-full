r'''
# `google_cloud_run_v2_worker_pool`

Refer to the Terraform Registry for docs: [`google_cloud_run_v2_worker_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool).
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


class CloudRunV2WorkerPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool google_cloud_run_v2_worker_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        template: typing.Union["CloudRunV2WorkerPoolTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union["CloudRunV2WorkerPoolBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        client_version: typing.Optional[builtins.str] = None,
        custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_splits: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolInstanceSplits", typing.Dict[builtins.str, typing.Any]]]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_stage: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["CloudRunV2WorkerPoolScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudRunV2WorkerPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool google_cloud_run_v2_worker_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the cloud run worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#location CloudRunV2WorkerPool#location}
        :param name: Name of the WorkerPool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#template CloudRunV2WorkerPool#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources. All system annotations in v1 now have a corresponding field in v2 WorkerPool. This field follows Kubernetes annotations' namespacing, limits, and rules. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#annotations CloudRunV2WorkerPool#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#binary_authorization CloudRunV2WorkerPool#binary_authorization}
        :param client: Arbitrary identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#client CloudRunV2WorkerPool#client}
        :param client_version: Arbitrary version identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#client_version CloudRunV2WorkerPool#client_version}
        :param custom_audiences: One or more custom audiences that you want this worker pool to support. Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests. For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#custom_audiences CloudRunV2WorkerPool#custom_audiences}
        :param deletion_protection: Whether Terraform will be prevented from destroying the service. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the service, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the WorkerPool will fail. When the field is set to false, deleting the WorkerPool is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#deletion_protection CloudRunV2WorkerPool#deletion_protection}
        :param description: User-provided description of the WorkerPool. This field currently has a 512-character limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#description CloudRunV2WorkerPool#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#id CloudRunV2WorkerPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_splits: instance_splits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#instance_splits CloudRunV2WorkerPool#instance_splits}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 WorkerPool. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#labels CloudRunV2WorkerPool#labels}
        :param launch_stage: The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features. For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#launch_stage CloudRunV2WorkerPool#launch_stage}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#project CloudRunV2WorkerPool#project}.
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#scaling CloudRunV2WorkerPool#scaling}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#timeouts CloudRunV2WorkerPool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd21e3cb2f2c93dce353d82aa3c65b21b5812dc7a961fdcec7a7da3cf2c13e01)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudRunV2WorkerPoolConfig(
            location=location,
            name=name,
            template=template,
            annotations=annotations,
            binary_authorization=binary_authorization,
            client=client,
            client_version=client_version,
            custom_audiences=custom_audiences,
            deletion_protection=deletion_protection,
            description=description,
            id=id,
            instance_splits=instance_splits,
            labels=labels,
            launch_stage=launch_stage,
            project=project,
            scaling=scaling,
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
        '''Generates CDKTF code for importing a CloudRunV2WorkerPool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CloudRunV2WorkerPool to import.
        :param import_from_id: The id of the existing CloudRunV2WorkerPool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CloudRunV2WorkerPool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc1c6617d69b5275bdce15c08280681dc94e3dade280866767a760492f651b6)
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
        :param breakglass_justification: If present, indicates to use Breakglass using this justification. If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#breakglass_justification CloudRunV2WorkerPool#breakglass_justification}
        :param policy: The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#policy CloudRunV2WorkerPool#policy}
        :param use_default: If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#use_default CloudRunV2WorkerPool#use_default}
        '''
        value = CloudRunV2WorkerPoolBinaryAuthorization(
            breakglass_justification=breakglass_justification,
            policy=policy,
            use_default=use_default,
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putInstanceSplits")
    def put_instance_splits(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolInstanceSplits", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e6a5d0d7db37174841f049a367eae9178621e9cacfb164481df5da20d05e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInstanceSplits", [value]))

    @jsii.member(jsii_name="putScaling")
    def put_scaling(
        self,
        *,
        manual_instance_count: typing.Optional[jsii.Number] = None,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manual_instance_count: The total number of instances in manual scaling mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#manual_instance_count CloudRunV2WorkerPool#manual_instance_count}
        :param max_instance_count: The maximum count of instances distributed among revisions based on the specified instance split percentages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#max_instance_count CloudRunV2WorkerPool#max_instance_count}
        :param min_instance_count: The minimum count of instances distributed among revisions based on the specified instance split percentages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#min_instance_count CloudRunV2WorkerPool#min_instance_count}
        :param scaling_mode: The scaling mode for the worker pool. It defaults to MANUAL. Possible values: ["AUTOMATIC", "MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#scaling_mode CloudRunV2WorkerPool#scaling_mode}
        '''
        value = CloudRunV2WorkerPoolScaling(
            manual_instance_count=manual_instance_count,
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
            scaling_mode=scaling_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putScaling", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        encryption_key_revocation_action: typing.Optional[builtins.str] = None,
        encryption_key_shutdown_duration: typing.Optional[builtins.str] = None,
        gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_selector: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateNodeSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        revision: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_access: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system annotations in v1 now have a corresponding field in v2 WorkerPoolRevisionTemplate. This field follows Kubernetes annotations' namespacing, limits, and rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#annotations CloudRunV2WorkerPool#annotations}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#containers CloudRunV2WorkerPool#containers}
        :param encryption_key: A reference to a customer managed encryption key (CMEK) to use to encrypt this container image. For more information, go to https://cloud.google.com/run/docs/securing/using-cmek Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key CloudRunV2WorkerPool#encryption_key}
        :param encryption_key_revocation_action: The action to take if the encryption key is revoked. Possible values: ["PREVENT_NEW", "SHUTDOWN"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key_revocation_action CloudRunV2WorkerPool#encryption_key_revocation_action}
        :param encryption_key_shutdown_duration: If encryptionKeyRevocationAction is SHUTDOWN, the duration before shutting down all instances. The minimum increment is 1 hour. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key_shutdown_duration CloudRunV2WorkerPool#encryption_key_shutdown_duration}
        :param gpu_zonal_redundancy_disabled: True if GPU zonal redundancy is disabled on this revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#gpu_zonal_redundancy_disabled CloudRunV2WorkerPool#gpu_zonal_redundancy_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 WorkerPoolRevisionTemplate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#labels CloudRunV2WorkerPool#labels}
        :param node_selector: node_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#node_selector CloudRunV2WorkerPool#node_selector}
        :param revision: The unique name for the revision. If this field is omitted, it will be automatically generated based on the WorkerPool name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#revision CloudRunV2WorkerPool#revision}
        :param service_account: Email address of the IAM service account associated with the revision of the WorkerPool. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#service_account CloudRunV2WorkerPool#service_account}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#volumes CloudRunV2WorkerPool#volumes}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#vpc_access CloudRunV2WorkerPool#vpc_access}
        '''
        value = CloudRunV2WorkerPoolTemplate(
            annotations=annotations,
            containers=containers,
            encryption_key=encryption_key,
            encryption_key_revocation_action=encryption_key_revocation_action,
            encryption_key_shutdown_duration=encryption_key_shutdown_duration,
            gpu_zonal_redundancy_disabled=gpu_zonal_redundancy_disabled,
            labels=labels,
            node_selector=node_selector,
            revision=revision,
            service_account=service_account,
            volumes=volumes,
            vpc_access=vpc_access,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#create CloudRunV2WorkerPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#delete CloudRunV2WorkerPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#update CloudRunV2WorkerPool#update}.
        '''
        value = CloudRunV2WorkerPoolTimeouts(
            create=create, delete=delete, update=update
        )

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

    @jsii.member(jsii_name="resetCustomAudiences")
    def reset_custom_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAudiences", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceSplits")
    def reset_instance_splits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceSplits", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLaunchStage")
    def reset_launch_stage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLaunchStage", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetScaling")
    def reset_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaling", []))

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
    def binary_authorization(
        self,
    ) -> "CloudRunV2WorkerPoolBinaryAuthorizationOutputReference":
        return typing.cast("CloudRunV2WorkerPoolBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "CloudRunV2WorkerPoolConditionsList":
        return typing.cast("CloudRunV2WorkerPoolConditionsList", jsii.get(self, "conditions"))

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
    @jsii.member(jsii_name="expireTime")
    def expire_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expireTime"))

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @builtins.property
    @jsii.member(jsii_name="instanceSplits")
    def instance_splits(self) -> "CloudRunV2WorkerPoolInstanceSplitsList":
        return typing.cast("CloudRunV2WorkerPoolInstanceSplitsList", jsii.get(self, "instanceSplits"))

    @builtins.property
    @jsii.member(jsii_name="instanceSplitStatuses")
    def instance_split_statuses(
        self,
    ) -> "CloudRunV2WorkerPoolInstanceSplitStatusesList":
        return typing.cast("CloudRunV2WorkerPoolInstanceSplitStatusesList", jsii.get(self, "instanceSplitStatuses"))

    @builtins.property
    @jsii.member(jsii_name="lastModifier")
    def last_modifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastModifier"))

    @builtins.property
    @jsii.member(jsii_name="latestCreatedRevision")
    def latest_created_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestCreatedRevision"))

    @builtins.property
    @jsii.member(jsii_name="latestReadyRevision")
    def latest_ready_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "latestReadyRevision"))

    @builtins.property
    @jsii.member(jsii_name="observedGeneration")
    def observed_generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "observedGeneration"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="scaling")
    def scaling(self) -> "CloudRunV2WorkerPoolScalingOutputReference":
        return typing.cast("CloudRunV2WorkerPoolScalingOutputReference", jsii.get(self, "scaling"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "CloudRunV2WorkerPoolTemplateOutputReference":
        return typing.cast("CloudRunV2WorkerPoolTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="terminalCondition")
    def terminal_condition(self) -> "CloudRunV2WorkerPoolTerminalConditionList":
        return typing.cast("CloudRunV2WorkerPoolTerminalConditionList", jsii.get(self, "terminalCondition"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudRunV2WorkerPoolTimeoutsOutputReference":
        return typing.cast("CloudRunV2WorkerPoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["CloudRunV2WorkerPoolBinaryAuthorization"]:
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="clientInput")
    def client_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientInput"))

    @builtins.property
    @jsii.member(jsii_name="clientVersionInput")
    def client_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="customAudiencesInput")
    def custom_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSplitsInput")
    def instance_splits_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolInstanceSplits"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolInstanceSplits"]]], jsii.get(self, "instanceSplitsInput"))

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
    @jsii.member(jsii_name="scalingInput")
    def scaling_input(self) -> typing.Optional["CloudRunV2WorkerPoolScaling"]:
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolScaling"], jsii.get(self, "scalingInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["CloudRunV2WorkerPoolTemplate"]:
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudRunV2WorkerPoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CloudRunV2WorkerPoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d5f1775d6042f9f62b168a9e1081498f96d49f25e29a7e6543600238a1373a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="client")
    def client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "client"))

    @client.setter
    def client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15232a63b3aea8d73a549b0074496b83209323aace6fed4fd77ac037552a27d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "client", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientVersion")
    def client_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientVersion"))

    @client_version.setter
    def client_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c3e025ea5e4a7f63e50f2ad1293ad8e037a045f89c76690dd700bf2901152dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customAudiences")
    def custom_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customAudiences"))

    @custom_audiences.setter
    def custom_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99cfbe10d4001a9a152f32409d9af0a59db39818cd73d52807081c799e6a2213)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAudiences", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__cb45a604cf2468d5363e85a8e5d84d4c2e8863012bafbed7122e2ede55daf66d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfb57833f1caeaa23f5dc911458eda3c16c0b8fef9b18640b45a4d647a98369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507f794d4b6acf5096602281fe154bcad1a943e29fb49be74c3dc6a0cbc80706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea6fbdaa00e46622decc5d4773ddb611608c8fc7fd3f21386948e61adede6f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchStage")
    def launch_stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchStage"))

    @launch_stage.setter
    def launch_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d17225356c6e3e75bf6edcb5d4f1c81896da0de0bbc7c4ff88a52f05c0cc854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5c9c213b785cb0a1ff9592db0857a0b1a9844011d5f083b6dc59b9c8ad6f206)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77c7d133b5eb24d7694d6b53548f73a1143f74d12f37d0f97a68e51203c1c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65b729ca257c5e8f79e8fdb6657d375d5d23c9da9e00f6b9a096fe97baf3f22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={
        "breakglass_justification": "breakglassJustification",
        "policy": "policy",
        "use_default": "useDefault",
    },
)
class CloudRunV2WorkerPoolBinaryAuthorization:
    def __init__(
        self,
        *,
        breakglass_justification: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param breakglass_justification: If present, indicates to use Breakglass using this justification. If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#breakglass_justification CloudRunV2WorkerPool#breakglass_justification}
        :param policy: The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#policy CloudRunV2WorkerPool#policy}
        :param use_default: If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#use_default CloudRunV2WorkerPool#use_default}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc8f3e8502c474a0ae5443b04bbde4b62145dbb2ff7f0332a6713d4c0207f02a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#breakglass_justification CloudRunV2WorkerPool#breakglass_justification}
        '''
        result = self._values.get("breakglass_justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#policy CloudRunV2WorkerPool#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#use_default CloudRunV2WorkerPool#use_default}
        '''
        result = self._values.get("use_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21138ec96d1d85e6518418a86215e4de9828aa8109c099b1ad73dd55d76e18ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61d5b57c29a6bb4f5d424fa3f8e371daec102746483c232ddf994d5f4172ddc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "breakglassJustification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d61ed671a282dcedf4dea1d2bb2cab8feaaa82a50ac98da6dd839dd1ee5aaa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47117fd64527a702a46bc333665f8e5e1a59b37d0da45560dc3da236376bf7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolBinaryAuthorization]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a92caeb1b029231cb29a74fcadbe8b8a752183daf7b86c3a78afa7e6666e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2WorkerPoolConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ba0f593bffc76d306761a4e1955adcd9fae7684763c1dc06e1a161276021288)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1563ce4ea8e0bd9dab4e15f5aa4038adaf8ac9157c84c07d02a84d84814595)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d831117986c1729769983d4df9ddc489d0bed9aa4500329042e8c59358eb0d38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0618601dea149028f0b7027786067d31430719676838d4235fb0ae5070b8bb5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cd0788fb0104f605cfe373a8d8366963d169174360bf3c55372a78795a8f2bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__413923ea7ca9f2ece275c19f61a6b6b381fe820c0c4bbcd6b2589942570f9afc)
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
    def internal_value(self) -> typing.Optional[CloudRunV2WorkerPoolConditions]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7b74031323221798bd56eef072a8de6f76d75bed5d51f429b91979340fb93a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolConfig",
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
        "custom_audiences": "customAudiences",
        "deletion_protection": "deletionProtection",
        "description": "description",
        "id": "id",
        "instance_splits": "instanceSplits",
        "labels": "labels",
        "launch_stage": "launchStage",
        "project": "project",
        "scaling": "scaling",
        "timeouts": "timeouts",
    },
)
class CloudRunV2WorkerPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        template: typing.Union["CloudRunV2WorkerPoolTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union[CloudRunV2WorkerPoolBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        client_version: typing.Optional[builtins.str] = None,
        custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_splits: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolInstanceSplits", typing.Dict[builtins.str, typing.Any]]]]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_stage: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["CloudRunV2WorkerPoolScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["CloudRunV2WorkerPoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the cloud run worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#location CloudRunV2WorkerPool#location}
        :param name: Name of the WorkerPool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#template CloudRunV2WorkerPool#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources. All system annotations in v1 now have a corresponding field in v2 WorkerPool. This field follows Kubernetes annotations' namespacing, limits, and rules. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#annotations CloudRunV2WorkerPool#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#binary_authorization CloudRunV2WorkerPool#binary_authorization}
        :param client: Arbitrary identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#client CloudRunV2WorkerPool#client}
        :param client_version: Arbitrary version identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#client_version CloudRunV2WorkerPool#client_version}
        :param custom_audiences: One or more custom audiences that you want this worker pool to support. Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests. For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#custom_audiences CloudRunV2WorkerPool#custom_audiences}
        :param deletion_protection: Whether Terraform will be prevented from destroying the service. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the service, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the WorkerPool will fail. When the field is set to false, deleting the WorkerPool is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#deletion_protection CloudRunV2WorkerPool#deletion_protection}
        :param description: User-provided description of the WorkerPool. This field currently has a 512-character limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#description CloudRunV2WorkerPool#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#id CloudRunV2WorkerPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_splits: instance_splits block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#instance_splits CloudRunV2WorkerPool#instance_splits}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 WorkerPool. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#labels CloudRunV2WorkerPool#labels}
        :param launch_stage: The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features. For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#launch_stage CloudRunV2WorkerPool#launch_stage}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#project CloudRunV2WorkerPool#project}.
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#scaling CloudRunV2WorkerPool#scaling}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#timeouts CloudRunV2WorkerPool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(template, dict):
            template = CloudRunV2WorkerPoolTemplate(**template)
        if isinstance(binary_authorization, dict):
            binary_authorization = CloudRunV2WorkerPoolBinaryAuthorization(**binary_authorization)
        if isinstance(scaling, dict):
            scaling = CloudRunV2WorkerPoolScaling(**scaling)
        if isinstance(timeouts, dict):
            timeouts = CloudRunV2WorkerPoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a4dd2d9e45f4f53503385f351cf10249201c7c60d0694bf83aa7f8cdc2c46a)
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
            check_type(argname="argument custom_audiences", value=custom_audiences, expected_type=type_hints["custom_audiences"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_splits", value=instance_splits, expected_type=type_hints["instance_splits"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument launch_stage", value=launch_stage, expected_type=type_hints["launch_stage"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
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
        if custom_audiences is not None:
            self._values["custom_audiences"] = custom_audiences
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if instance_splits is not None:
            self._values["instance_splits"] = instance_splits
        if labels is not None:
            self._values["labels"] = labels
        if launch_stage is not None:
            self._values["launch_stage"] = launch_stage
        if project is not None:
            self._values["project"] = project
        if scaling is not None:
            self._values["scaling"] = scaling
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
        '''The location of the cloud run worker pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#location CloudRunV2WorkerPool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the WorkerPool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> "CloudRunV2WorkerPoolTemplate":
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#template CloudRunV2WorkerPool#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("CloudRunV2WorkerPoolTemplate", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that may be set by external tools to store and arbitrary metadata.

        They are not queryable and should be preserved when modifying objects.

        Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources.
        All system annotations in v1 now have a corresponding field in v2 WorkerPool.

        This field follows Kubernetes annotations' namespacing, limits, and rules.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#annotations CloudRunV2WorkerPool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#binary_authorization CloudRunV2WorkerPool#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolBinaryAuthorization], result)

    @builtins.property
    def client(self) -> typing.Optional[builtins.str]:
        '''Arbitrary identifier for the API client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#client CloudRunV2WorkerPool#client}
        '''
        result = self._values.get("client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_version(self) -> typing.Optional[builtins.str]:
        '''Arbitrary version identifier for the API client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#client_version CloudRunV2WorkerPool#client_version}
        '''
        result = self._values.get("client_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more custom audiences that you want this worker pool to support.

        Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests.
        For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#custom_audiences CloudRunV2WorkerPool#custom_audiences}
        '''
        result = self._values.get("custom_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the service.

        Defaults to true.
        When a'terraform destroy' or 'terraform apply' would delete the service,
        the command will fail if this field is not set to false in Terraform state.
        When the field is set to true or unset in Terraform state, a 'terraform apply'
        or 'terraform destroy' that would delete the WorkerPool will fail.
        When the field is set to false, deleting the WorkerPool is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#deletion_protection CloudRunV2WorkerPool#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description of the WorkerPool. This field currently has a 512-character limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#description CloudRunV2WorkerPool#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#id CloudRunV2WorkerPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_splits(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolInstanceSplits"]]]:
        '''instance_splits block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#instance_splits CloudRunV2WorkerPool#instance_splits}
        '''
        result = self._values.get("instance_splits")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolInstanceSplits"]]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that can be used to organize and categorize objects.

        User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component,
        environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels.

        Cloud Run API v2 does not support labels with  'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system labels in v1 now have a corresponding field in v2 WorkerPool.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#labels CloudRunV2WorkerPool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def launch_stage(self) -> typing.Optional[builtins.str]:
        '''The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features.

        For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#launch_stage CloudRunV2WorkerPool#launch_stage}
        '''
        result = self._values.get("launch_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#project CloudRunV2WorkerPool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling(self) -> typing.Optional["CloudRunV2WorkerPoolScaling"]:
        '''scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#scaling CloudRunV2WorkerPool#scaling}
        '''
        result = self._values.get("scaling")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolScaling"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudRunV2WorkerPoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#timeouts CloudRunV2WorkerPool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolInstanceSplitStatuses",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2WorkerPoolInstanceSplitStatuses:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolInstanceSplitStatuses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolInstanceSplitStatusesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolInstanceSplitStatusesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb1666d668c501adf9c11c69776f3f9c318265bad2752ee4ae68950006929bca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolInstanceSplitStatusesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78acd06c350f117a538519bee75a318c0da60393ee4eeba011c9a365f7f4025f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolInstanceSplitStatusesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22aab820860bf51b98e0954d28f9ebb71dc77652a26e2aa8d450fe7027030302)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d91fb889b6fa780f01ca49a215d5efef24bcdaa302bd6a638ce2dd0dbdec8511)
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
            type_hints = typing.get_type_hints(_typecheckingstub__648b198fc8d76c3dd4845329083346bc4178cf72904409a369e2a0ee9dd63b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolInstanceSplitStatusesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolInstanceSplitStatusesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2972cde6dc6035c74a3f0d7c1c12a6a0b92c3e82cda5cbb3a1d7fe27d2beb0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolInstanceSplitStatuses]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolInstanceSplitStatuses], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolInstanceSplitStatuses],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab37d2d4823bf1b6c7d48e15db5920f44a5874697b5c92656fcedcc968b645a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolInstanceSplits",
    jsii_struct_bases=[],
    name_mapping={"percent": "percent", "revision": "revision", "type": "type"},
)
class CloudRunV2WorkerPoolInstanceSplits:
    def __init__(
        self,
        *,
        percent: typing.Optional[jsii.Number] = None,
        revision: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param percent: Specifies percent of the instance split to this Revision. This defaults to zero if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#percent CloudRunV2WorkerPool#percent}
        :param revision: Revision to which to assign this portion of instances, if split allocation is by revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#revision CloudRunV2WorkerPool#revision}
        :param type: The allocation type for this instance split. Possible values: ["INSTANCE_SPLIT_ALLOCATION_TYPE_LATEST", "INSTANCE_SPLIT_ALLOCATION_TYPE_REVISION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#type CloudRunV2WorkerPool#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b6875951bfa046e0c0e3e2a6ef291bd9bc92cdff2bc2d651d2ed0407b0ce59)
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if percent is not None:
            self._values["percent"] = percent
        if revision is not None:
            self._values["revision"] = revision
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies percent of the instance split to this Revision. This defaults to zero if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#percent CloudRunV2WorkerPool#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        '''Revision to which to assign this portion of instances, if split allocation is by revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#revision CloudRunV2WorkerPool#revision}
        '''
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The allocation type for this instance split. Possible values: ["INSTANCE_SPLIT_ALLOCATION_TYPE_LATEST", "INSTANCE_SPLIT_ALLOCATION_TYPE_REVISION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#type CloudRunV2WorkerPool#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolInstanceSplits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolInstanceSplitsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolInstanceSplitsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__756fb178bce926137c235f4b54fd4062d84f042cb5f1164b45189eb9a8977ce0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolInstanceSplitsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f1220a7d559736044cc203ae14317455b80abcd53a0e0af990deb1b4b43fbf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolInstanceSplitsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469f5db3393dbc40d62a715544810336c44ea79636169151a294e315309bda31)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa0efe4a688c2f2ca45ced91a3a9cf651fe6a238dab5ded4240108824c473160)
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
            type_hints = typing.get_type_hints(_typecheckingstub__21dc550d713bdfe04a3380e229b26f2f333090509cb623398f6c29a38aa143a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolInstanceSplits]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolInstanceSplits]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolInstanceSplits]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18547c20d426dde05d1f8d5fe533847c8325d0c6e460aa1a97b5922de1b985de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolInstanceSplitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolInstanceSplitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0d556cef40f7ddad2c4a35e50a62f8decf4a266353e7c5f40b8e61987198040)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPercent")
    def reset_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercent", []))

    @jsii.member(jsii_name="resetRevision")
    def reset_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevision", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7688e71d04fee4d37afd9d2ca25d194cfff04dc664c2299b6b0d07b24f8e8239)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2269684427ce93d4d98e516e5b3c470841541b64e6ad2db21047792f5b5e5491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbbe83df8191a2d3dd70c6fb0882643b968c65c8d247386a052452348617de56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolInstanceSplits]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolInstanceSplits]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolInstanceSplits]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5184e33f42fff992e738aa7b23d29d6dc05d816f5ab69bda4542c5273dafb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolScaling",
    jsii_struct_bases=[],
    name_mapping={
        "manual_instance_count": "manualInstanceCount",
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
        "scaling_mode": "scalingMode",
    },
)
class CloudRunV2WorkerPoolScaling:
    def __init__(
        self,
        *,
        manual_instance_count: typing.Optional[jsii.Number] = None,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manual_instance_count: The total number of instances in manual scaling mode. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#manual_instance_count CloudRunV2WorkerPool#manual_instance_count}
        :param max_instance_count: The maximum count of instances distributed among revisions based on the specified instance split percentages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#max_instance_count CloudRunV2WorkerPool#max_instance_count}
        :param min_instance_count: The minimum count of instances distributed among revisions based on the specified instance split percentages. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#min_instance_count CloudRunV2WorkerPool#min_instance_count}
        :param scaling_mode: The scaling mode for the worker pool. It defaults to MANUAL. Possible values: ["AUTOMATIC", "MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#scaling_mode CloudRunV2WorkerPool#scaling_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3ad3ae8d86daf2705443d05fde68c1c852d2e355b56920f37ab46482a13de9)
            check_type(argname="argument manual_instance_count", value=manual_instance_count, expected_type=type_hints["manual_instance_count"])
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            check_type(argname="argument scaling_mode", value=scaling_mode, expected_type=type_hints["scaling_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manual_instance_count is not None:
            self._values["manual_instance_count"] = manual_instance_count
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count
        if scaling_mode is not None:
            self._values["scaling_mode"] = scaling_mode

    @builtins.property
    def manual_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The total number of instances in manual scaling mode.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#manual_instance_count CloudRunV2WorkerPool#manual_instance_count}
        '''
        result = self._values.get("manual_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum count of instances distributed among revisions based on the specified instance split percentages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#max_instance_count CloudRunV2WorkerPool#max_instance_count}
        '''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum count of instances distributed among revisions based on the specified instance split percentages.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#min_instance_count CloudRunV2WorkerPool#min_instance_count}
        '''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scaling_mode(self) -> typing.Optional[builtins.str]:
        '''The scaling mode for the worker pool. It defaults to MANUAL. Possible values: ["AUTOMATIC", "MANUAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#scaling_mode CloudRunV2WorkerPool#scaling_mode}
        '''
        result = self._values.get("scaling_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__babbaf0252b73eb578e7bc30fb313e7ad0d60ef83add0ea947321e4c25ebd357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetManualInstanceCount")
    def reset_manual_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualInstanceCount", []))

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @jsii.member(jsii_name="resetScalingMode")
    def reset_scaling_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingMode", []))

    @builtins.property
    @jsii.member(jsii_name="manualInstanceCountInput")
    def manual_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "manualInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingModeInput")
    def scaling_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="manualInstanceCount")
    def manual_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "manualInstanceCount"))

    @manual_instance_count.setter
    def manual_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd176821aacde356e7a32473dd51196c30db1639b39a55400f2e7b7d6b4f3ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b36174ca60bac4fe01e55794ca5996394a4c98f4ce45bd1868c21fcabd36b6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0961211fe0752ea6ebc38d922393e54f37771d3095491b79f6564b7939466a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingMode")
    def scaling_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingMode"))

    @scaling_mode.setter
    def scaling_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01fc48400031add2b616aaf8a6ed5fb6e3c294ed5697f3ad87a9ead71775202e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2WorkerPoolScaling]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba0b22410b7fecaf18f2efec4c9acab6841966f7849933d39b0b0ce08485e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "containers": "containers",
        "encryption_key": "encryptionKey",
        "encryption_key_revocation_action": "encryptionKeyRevocationAction",
        "encryption_key_shutdown_duration": "encryptionKeyShutdownDuration",
        "gpu_zonal_redundancy_disabled": "gpuZonalRedundancyDisabled",
        "labels": "labels",
        "node_selector": "nodeSelector",
        "revision": "revision",
        "service_account": "serviceAccount",
        "volumes": "volumes",
        "vpc_access": "vpcAccess",
    },
)
class CloudRunV2WorkerPoolTemplate:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        encryption_key_revocation_action: typing.Optional[builtins.str] = None,
        encryption_key_shutdown_duration: typing.Optional[builtins.str] = None,
        gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_selector: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateNodeSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        revision: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_access: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system annotations in v1 now have a corresponding field in v2 WorkerPoolRevisionTemplate. This field follows Kubernetes annotations' namespacing, limits, and rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#annotations CloudRunV2WorkerPool#annotations}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#containers CloudRunV2WorkerPool#containers}
        :param encryption_key: A reference to a customer managed encryption key (CMEK) to use to encrypt this container image. For more information, go to https://cloud.google.com/run/docs/securing/using-cmek Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key CloudRunV2WorkerPool#encryption_key}
        :param encryption_key_revocation_action: The action to take if the encryption key is revoked. Possible values: ["PREVENT_NEW", "SHUTDOWN"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key_revocation_action CloudRunV2WorkerPool#encryption_key_revocation_action}
        :param encryption_key_shutdown_duration: If encryptionKeyRevocationAction is SHUTDOWN, the duration before shutting down all instances. The minimum increment is 1 hour. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key_shutdown_duration CloudRunV2WorkerPool#encryption_key_shutdown_duration}
        :param gpu_zonal_redundancy_disabled: True if GPU zonal redundancy is disabled on this revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#gpu_zonal_redundancy_disabled CloudRunV2WorkerPool#gpu_zonal_redundancy_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 WorkerPoolRevisionTemplate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#labels CloudRunV2WorkerPool#labels}
        :param node_selector: node_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#node_selector CloudRunV2WorkerPool#node_selector}
        :param revision: The unique name for the revision. If this field is omitted, it will be automatically generated based on the WorkerPool name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#revision CloudRunV2WorkerPool#revision}
        :param service_account: Email address of the IAM service account associated with the revision of the WorkerPool. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#service_account CloudRunV2WorkerPool#service_account}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#volumes CloudRunV2WorkerPool#volumes}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#vpc_access CloudRunV2WorkerPool#vpc_access}
        '''
        if isinstance(node_selector, dict):
            node_selector = CloudRunV2WorkerPoolTemplateNodeSelector(**node_selector)
        if isinstance(vpc_access, dict):
            vpc_access = CloudRunV2WorkerPoolTemplateVpcAccess(**vpc_access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f0210d87d8040e86c3d2051f85ee4709b1fc395037f66ff0485d4be2c6925d)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument encryption_key_revocation_action", value=encryption_key_revocation_action, expected_type=type_hints["encryption_key_revocation_action"])
            check_type(argname="argument encryption_key_shutdown_duration", value=encryption_key_shutdown_duration, expected_type=type_hints["encryption_key_shutdown_duration"])
            check_type(argname="argument gpu_zonal_redundancy_disabled", value=gpu_zonal_redundancy_disabled, expected_type=type_hints["gpu_zonal_redundancy_disabled"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument node_selector", value=node_selector, expected_type=type_hints["node_selector"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument vpc_access", value=vpc_access, expected_type=type_hints["vpc_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if containers is not None:
            self._values["containers"] = containers
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if encryption_key_revocation_action is not None:
            self._values["encryption_key_revocation_action"] = encryption_key_revocation_action
        if encryption_key_shutdown_duration is not None:
            self._values["encryption_key_shutdown_duration"] = encryption_key_shutdown_duration
        if gpu_zonal_redundancy_disabled is not None:
            self._values["gpu_zonal_redundancy_disabled"] = gpu_zonal_redundancy_disabled
        if labels is not None:
            self._values["labels"] = labels
        if node_selector is not None:
            self._values["node_selector"] = node_selector
        if revision is not None:
            self._values["revision"] = revision
        if service_account is not None:
            self._values["service_account"] = service_account
        if volumes is not None:
            self._values["volumes"] = volumes
        if vpc_access is not None:
            self._values["vpc_access"] = vpc_access

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that may be set by external tools to store and arbitrary metadata.

        They are not queryable and should be preserved when modifying objects.

        Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system annotations in v1 now have a corresponding field in v2 WorkerPoolRevisionTemplate.

        This field follows Kubernetes annotations' namespacing, limits, and rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#annotations CloudRunV2WorkerPool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def containers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateContainers"]]]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#containers CloudRunV2WorkerPool#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateContainers"]]], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''A reference to a customer managed encryption key (CMEK) to use to encrypt this container image.

        For more information, go to https://cloud.google.com/run/docs/securing/using-cmek

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key CloudRunV2WorkerPool#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key_revocation_action(self) -> typing.Optional[builtins.str]:
        '''The action to take if the encryption key is revoked. Possible values: ["PREVENT_NEW", "SHUTDOWN"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key_revocation_action CloudRunV2WorkerPool#encryption_key_revocation_action}
        '''
        result = self._values.get("encryption_key_revocation_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key_shutdown_duration(self) -> typing.Optional[builtins.str]:
        '''If encryptionKeyRevocationAction is SHUTDOWN, the duration before shutting down all instances. The minimum increment is 1 hour.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#encryption_key_shutdown_duration CloudRunV2WorkerPool#encryption_key_shutdown_duration}
        '''
        result = self._values.get("encryption_key_shutdown_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpu_zonal_redundancy_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if GPU zonal redundancy is disabled on this revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#gpu_zonal_redundancy_disabled CloudRunV2WorkerPool#gpu_zonal_redundancy_disabled}
        '''
        result = self._values.get("gpu_zonal_redundancy_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that can be used to organize and categorize objects.

        User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc.
        For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels.

        Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system labels in v1 now have a corresponding field in v2 WorkerPoolRevisionTemplate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#labels CloudRunV2WorkerPool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_selector(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateNodeSelector"]:
        '''node_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#node_selector CloudRunV2WorkerPool#node_selector}
        '''
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateNodeSelector"], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        '''The unique name for the revision.

        If this field is omitted, it will be automatically generated based on the WorkerPool name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#revision CloudRunV2WorkerPool#revision}
        '''
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Email address of the IAM service account associated with the revision of the WorkerPool.

        The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#service_account CloudRunV2WorkerPool#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#volumes CloudRunV2WorkerPool#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateVolumes"]]], result)

    @builtins.property
    def vpc_access(self) -> typing.Optional["CloudRunV2WorkerPoolTemplateVpcAccess"]:
        '''vpc_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#vpc_access CloudRunV2WorkerPool#vpc_access}
        '''
        result = self._values.get("vpc_access")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateVpcAccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainers",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "command": "command",
        "depends_on": "dependsOn",
        "env": "env",
        "name": "name",
        "resources": "resources",
        "volume_mounts": "volumeMounts",
        "working_dir": "workingDir",
    },
)
class CloudRunV2WorkerPoolTemplateContainers:
    def __init__(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateContainersEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateContainersResources", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: URL of the Container image in Google Container Registry or Google Artifact Registry. More info: https://kubernetes.io/docs/concepts/containers/images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#image CloudRunV2WorkerPool#image}
        :param args: Arguments to the entrypoint. The docker image's CMD is used if this is not provided. Variable references are not supported in Cloud Run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#args CloudRunV2WorkerPool#args}
        :param command: Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#command CloudRunV2WorkerPool#command}
        :param depends_on: Containers which should be started before this container. If specified the container will wait to start until all containers with the listed names are healthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#depends_on CloudRunV2WorkerPool#depends_on}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#env CloudRunV2WorkerPool#env}
        :param name: Name of the container specified as a DNS_LABEL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#resources CloudRunV2WorkerPool#resources}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#volume_mounts CloudRunV2WorkerPool#volume_mounts}
        :param working_dir: Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#working_dir CloudRunV2WorkerPool#working_dir}
        '''
        if isinstance(resources, dict):
            resources = CloudRunV2WorkerPoolTemplateContainersResources(**resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58b71ddcceeca73442e3150f2162d4717b371d1cb4283df4c7f91f5a54e0b41)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
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
        if resources is not None:
            self._values["resources"] = resources
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def image(self) -> builtins.str:
        '''URL of the Container image in Google Container Registry or Google Artifact Registry. More info: https://kubernetes.io/docs/concepts/containers/images.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#image CloudRunV2WorkerPool#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to the entrypoint.

        The docker image's CMD is used if this is not provided. Variable references are not supported in Cloud Run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#args CloudRunV2WorkerPool#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Entrypoint array.

        Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#command CloudRunV2WorkerPool#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Containers which should be started before this container.

        If specified the container will wait to start until all containers with the listed names are healthy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#depends_on CloudRunV2WorkerPool#depends_on}
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateContainersEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#env CloudRunV2WorkerPool#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateContainersEnv"]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the container specified as a DNS_LABEL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateContainersResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#resources CloudRunV2WorkerPool#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateContainersResources"], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateContainersVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#volume_mounts CloudRunV2WorkerPool#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateContainersVolumeMounts"]]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''Container's working directory.

        If not specified, the container runtime's default will be used, which might be configured in the container image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#working_dir CloudRunV2WorkerPool#working_dir}
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "value_source": "valueSource"},
)
class CloudRunV2WorkerPoolTemplateContainersEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
        value_source: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateContainersEnvValueSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Must be a C_IDENTIFIER, and may not exceed 32768 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        :param value: Literal value of the environment variable. Defaults to "" and the maximum allowed length is 32768 characters. Variable references are not supported in Cloud Run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#value CloudRunV2WorkerPool#value}
        :param value_source: value_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#value_source CloudRunV2WorkerPool#value_source}
        '''
        if isinstance(value_source, dict):
            value_source = CloudRunV2WorkerPoolTemplateContainersEnvValueSource(**value_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c3b878b91800befdc5a7792c1e01ac0b50b9e4aef2f0ac2f554440d7f203cd)
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
        '''Name of the environment variable. Must be a C_IDENTIFIER, and may not exceed 32768 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Literal value of the environment variable.

        Defaults to "" and the maximum allowed length is 32768 characters. Variable references are not supported in Cloud Run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#value CloudRunV2WorkerPool#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_source(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateContainersEnvValueSource"]:
        '''value_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#value_source CloudRunV2WorkerPool#value_source}
        '''
        result = self._values.get("value_source")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateContainersEnvValueSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateContainersEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateContainersEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6cc57177c0e04df33a82103075522c4636c6b5536b1771354191a79e12bd217)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolTemplateContainersEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7daaceecc5bd40c2f6b4757d0e929a0990e33c64f27d1672ab3f5b3d9e4a98a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolTemplateContainersEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bdebc481f6e79b7a32dd654249f567c13f3164577efaa990ab565997f14f1c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd952a0740e3e2f7aece6b27a6a8c6492e0ecf8bdc97ba4c20c34eaf58d28d60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__207b9db6b6330ef477034ee2c1a34cbed887d5fdeabe9cd1e34159d128a132d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a51bced51d6d3861cb59369968610c76d79343950fad217f2acf17886fb09ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateContainersEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cae500e0b7d0293bc79555a5958573239700fa32cff3d283fda6f52e632902e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueSource")
    def put_value_source(
        self,
        *,
        secret_key_ref: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret_key_ref CloudRunV2WorkerPool#secret_key_ref}
        '''
        value = CloudRunV2WorkerPoolTemplateContainersEnvValueSource(
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
    ) -> "CloudRunV2WorkerPoolTemplateContainersEnvValueSourceOutputReference":
        return typing.cast("CloudRunV2WorkerPoolTemplateContainersEnvValueSourceOutputReference", jsii.get(self, "valueSource"))

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
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateContainersEnvValueSource"]:
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateContainersEnvValueSource"], jsii.get(self, "valueSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351205b33f34735d85225dbb8cb1571daed9058a4d611ca430bca1ff68854a5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c04877ce4d5198d6181fcd5a38016afeba50f9d190878a78101b36e6be78869a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainersEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainersEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainersEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ac9dfa91145330a13284a294a9b5c0fd3fdf2f4016b87944266ac87cf22b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersEnvValueSource",
    jsii_struct_bases=[],
    name_mapping={"secret_key_ref": "secretKeyRef"},
)
class CloudRunV2WorkerPoolTemplateContainersEnvValueSource:
    def __init__(
        self,
        *,
        secret_key_ref: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret_key_ref CloudRunV2WorkerPool#secret_key_ref}
        '''
        if isinstance(secret_key_ref, dict):
            secret_key_ref = CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef(**secret_key_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c64e26bcecf9ae1f10781dade2fdd5512ed7023119d3265f52affc0b779bf3d)
            check_type(argname="argument secret_key_ref", value=secret_key_ref, expected_type=type_hints["secret_key_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_key_ref is not None:
            self._values["secret_key_ref"] = secret_key_ref

    @builtins.property
    def secret_key_ref(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef"]:
        '''secret_key_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret_key_ref CloudRunV2WorkerPool#secret_key_ref}
        '''
        result = self._values.get("secret_key_ref")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateContainersEnvValueSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateContainersEnvValueSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersEnvValueSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8eb487b8dfc8e6e8ff20c3b638119f845e1fa5e6f371fbcdb20f2094349f587e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSecretKeyRef")
    def put_secret_key_ref(
        self,
        *,
        secret: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret CloudRunV2WorkerPool#secret}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#version CloudRunV2WorkerPool#version}
        '''
        value = CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef(
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
    ) -> "CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRefOutputReference":
        return typing.cast("CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRefOutputReference", jsii.get(self, "secretKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRefInput")
    def secret_key_ref_input(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef"]:
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef"], jsii.get(self, "secretKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateContainersEnvValueSource]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateContainersEnvValueSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateContainersEnvValueSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ee284c0dd8987045474f402ed6f799d44bd33da0c1242545037508c5cc1a038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "version": "version"},
)
class CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef:
    def __init__(
        self,
        *,
        secret: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret CloudRunV2WorkerPool#secret}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#version CloudRunV2WorkerPool#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab719dbffc8e82b65afd88673b0a10b1dffacc66f5d43f9fcfe1d49c975537df)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "secret": secret,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def secret(self) -> builtins.str:
        '''The name of the secret in Cloud Secret Manager.

        Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret CloudRunV2WorkerPool#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Cloud Secret Manager secret version.

        Can be 'latest' for the latest value or an integer for a specific version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#version CloudRunV2WorkerPool#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b2d886b23c1dabf436fea1d0488d4b4c0003ec0e963604e595cf1016095e439)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__04c322bb6d27a9f8802f3c460f0cf391fcd8d7b5da57795ca543255aa46951d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6177ee2d9114e4970365588bdc1e2a5057f7d338293bd3d70a75669aafdfa28b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86752061dfc3086f08c98db8c46c0706ed092d5cbbdd0fdc57cd90b9b499ca60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fbca2e68ee4ce69161d1c771b4eec3919c0d0978dabd9716bc43a3792e357a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolTemplateContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fae0f84a9df18cebf64f46d42e0fc6182019facce0edbc43113a64b5f7e43b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolTemplateContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1df5faddb4743fad136321a5d73a43d1c5b780e54af8da6c5a2bbef15c54d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b008b3d6621f0f2976d596920a6cb045f7a528ecdc97fa5cda30f442adbcb0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba854db103663c2fda1045f0a6dd8d2a247ee6dcac27f03fde05a208470489d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86163a90432a8544f6524468f2251bc7a6de977707485f286c12c1f7ae312393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__465f8d0ddba5d277159924da2a23fd5d58088499d1b5626fef412b9190cbb144)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029fc24d9d0857ab157f8d405941aed1bca066664aefaca7f9ba1c8a90cbbc30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        *,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param limits: Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#limits CloudRunV2WorkerPool#limits}
        '''
        value = CloudRunV2WorkerPoolTemplateContainersResources(limits=limits)

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putVolumeMounts")
    def put_volume_mounts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdaa49b242d5bf7c36d1340595304e545252f84b656d98b5df5c2b88a30eee7)
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

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @jsii.member(jsii_name="resetVolumeMounts")
    def reset_volume_mounts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumeMounts", []))

    @jsii.member(jsii_name="resetWorkingDir")
    def reset_working_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDir", []))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> CloudRunV2WorkerPoolTemplateContainersEnvList:
        return typing.cast(CloudRunV2WorkerPoolTemplateContainersEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "CloudRunV2WorkerPoolTemplateContainersResourcesOutputReference":
        return typing.cast("CloudRunV2WorkerPoolTemplateContainersResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(self) -> "CloudRunV2WorkerPoolTemplateContainersVolumeMountsList":
        return typing.cast("CloudRunV2WorkerPoolTemplateContainersVolumeMountsList", jsii.get(self, "volumeMounts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateContainersResources"]:
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateContainersResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateContainersVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateContainersVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d2349f4148bf91a2f89049192a712c91bb3a23f60113ce8b68d39834631fcfdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d29b7c4ce86a728865c20cbad5fc6ebb07d0c156dee5965618ca84d4b3f6ee9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1fc7ebe80f92efa0ca3c489f14252395d4be0a88fdb6ef1fdc99fd47e1949c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04392e220ef0c1253c7124b58fc548639d8b4b7485f398b65e489ca69155a883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb9a03d6c0c5ec1aac694655f49233f06483741440395c67ed9337e8c88cad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504fb92295791bb6074ca790e53e249fc473345ad5667631615e9a4c7464d47e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262606cb07908937332dd98ca8c0072f88f86da25027cb986e372d54ea2f4418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersResources",
    jsii_struct_bases=[],
    name_mapping={"limits": "limits"},
)
class CloudRunV2WorkerPoolTemplateContainersResources:
    def __init__(
        self,
        *,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param limits: Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#limits CloudRunV2WorkerPool#limits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b300111fd521033b3e00677e054fb617caa78c703d0486e63f2e20f83e7340d)
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if limits is not None:
            self._values["limits"] = limits

    @builtins.property
    def limits(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#limits CloudRunV2WorkerPool#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateContainersResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateContainersResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12df50ca501028fbda921a71cb1d943296e022ad77fb6d5f4f7eebd47e23583c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4614d12147ba56fd1e6c4446f6fc64bbafd5ec323ee6a9b0fd11b84721b277e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateContainersResources]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateContainersResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateContainersResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e991907c620f58fa6a4bb659a77a43774e55727377058c1bf49482247820a358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"mount_path": "mountPath", "name": "name"},
)
class CloudRunV2WorkerPoolTemplateContainersVolumeMounts:
    def __init__(self, *, mount_path: builtins.str, name: builtins.str) -> None:
        '''
        :param mount_path: Path within the container at which the volume should be mounted. Must not contain ':'. For Cloud SQL volumes, it can be left empty, or must otherwise be /cloudsql. All instances defined in the Volume will be available as /cloudsql/[instance]. For more information on Cloud SQL volumes, visit https://cloud.google.com/sql/docs/mysql/connect-run Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#mount_path CloudRunV2WorkerPool#mount_path}
        :param name: This must match the Name of a Volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c9f6f8e85856bdd810a09813d7ebf9b64a44d9bbce3e0bfdf32fd566adb82d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#mount_path CloudRunV2WorkerPool#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''This must match the Name of a Volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateContainersVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateContainersVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e42739c89219af89d17ddac6093fa527d439a306e9156fbc2c4dd5eda67b0cfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolTemplateContainersVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0eb6bcb1a54b83480895d52bcd637dcc10426920c0fae28c87c11eb7b0c3efc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolTemplateContainersVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4dd089a1c96bf24cfb06495fc31f9fc9bf0b9c7cc69e614c8237f1d0818802)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30683208e920f5f06a1d59d232f092dcc1ffbbe129ebcdbf0e90de905537e48a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bde4bc927f4b31dc5b198aeb8d20014e61ef6ff40d7a3e2fbbcba8bdad333e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22233f303a258ae7f5f7063e1af7a93665722992ccbb19f1471197a6c59b9cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateContainersVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateContainersVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d16629e1cd62f89f08240579131bea34d907c1c4977bcb03fca4c1ecacd6b741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc6b9c20dcb7a12119a103e8e071ba33c0e5a44c13739887b115fef65b02cc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__977646ff69cfa45cfbad563f6b64c6db4064e8b90a6b74ee0e2eb98744312594)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainersVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainersVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainersVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218b50099f251b08071b8d6bab510fccea25d95ddc8fae8432573b6c39ef85aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateNodeSelector",
    jsii_struct_bases=[],
    name_mapping={"accelerator": "accelerator"},
)
class CloudRunV2WorkerPoolTemplateNodeSelector:
    def __init__(self, *, accelerator: builtins.str) -> None:
        '''
        :param accelerator: The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#accelerator CloudRunV2WorkerPool#accelerator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c2d3bd16403215bcf5334882dc5e5bc449a79f855c04d679473c1b43609606)
            check_type(argname="argument accelerator", value=accelerator, expected_type=type_hints["accelerator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator": accelerator,
        }

    @builtins.property
    def accelerator(self) -> builtins.str:
        '''The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#accelerator CloudRunV2WorkerPool#accelerator}
        '''
        result = self._values.get("accelerator")
        assert result is not None, "Required property 'accelerator' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateNodeSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateNodeSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateNodeSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ff1d3a5bd3504299931402ed783b5f80f007adc1d6a0afc858ebef51a07904b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f4e91420a3259d6ad73ce18230c89842673d3550f7b996b2e4a1f4520b0669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accelerator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateNodeSelector]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateNodeSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateNodeSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08dac623d3a325d443723b16ff67f4af549c50696cc9567406ca56950be6454f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6c25dca39a76da84eebe36fd45d2c01e2591e2021a0b69bd0b6ddb9e61fec5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateContainers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d205c0ae2bddee826e8c0419c8592ad163bf19e55f5972787f02559a01c9eb18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainers", [value]))

    @jsii.member(jsii_name="putNodeSelector")
    def put_node_selector(self, *, accelerator: builtins.str) -> None:
        '''
        :param accelerator: The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#accelerator CloudRunV2WorkerPool#accelerator}
        '''
        value = CloudRunV2WorkerPoolTemplateNodeSelector(accelerator=accelerator)

        return typing.cast(None, jsii.invoke(self, "putNodeSelector", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1312c77a8f077281f6ebcde278921b53dcd183a0ec7a61cde3f70deedc396a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="putVpcAccess")
    def put_vpc_access(
        self,
        *,
        egress: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param egress: Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#egress CloudRunV2WorkerPool#egress}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#network_interfaces CloudRunV2WorkerPool#network_interfaces}
        '''
        value = CloudRunV2WorkerPoolTemplateVpcAccess(
            egress=egress, network_interfaces=network_interfaces
        )

        return typing.cast(None, jsii.invoke(self, "putVpcAccess", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetContainers")
    def reset_containers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainers", []))

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetEncryptionKeyRevocationAction")
    def reset_encryption_key_revocation_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyRevocationAction", []))

    @jsii.member(jsii_name="resetEncryptionKeyShutdownDuration")
    def reset_encryption_key_shutdown_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeyShutdownDuration", []))

    @jsii.member(jsii_name="resetGpuZonalRedundancyDisabled")
    def reset_gpu_zonal_redundancy_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuZonalRedundancyDisabled", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNodeSelector")
    def reset_node_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeSelector", []))

    @jsii.member(jsii_name="resetRevision")
    def reset_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevision", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetVolumes")
    def reset_volumes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolumes", []))

    @jsii.member(jsii_name="resetVpcAccess")
    def reset_vpc_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcAccess", []))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(self) -> CloudRunV2WorkerPoolTemplateContainersList:
        return typing.cast(CloudRunV2WorkerPoolTemplateContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelector")
    def node_selector(self) -> CloudRunV2WorkerPoolTemplateNodeSelectorOutputReference:
        return typing.cast(CloudRunV2WorkerPoolTemplateNodeSelectorOutputReference, jsii.get(self, "nodeSelector"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "CloudRunV2WorkerPoolTemplateVolumesList":
        return typing.cast("CloudRunV2WorkerPoolTemplateVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccess")
    def vpc_access(self) -> "CloudRunV2WorkerPoolTemplateVpcAccessOutputReference":
        return typing.cast("CloudRunV2WorkerPoolTemplateVpcAccessOutputReference", jsii.get(self, "vpcAccess"))

    @builtins.property
    @jsii.member(jsii_name="annotationsInput")
    def annotations_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "annotationsInput"))

    @builtins.property
    @jsii.member(jsii_name="containersInput")
    def containers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainers]]], jsii.get(self, "containersInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyRevocationActionInput")
    def encryption_key_revocation_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyRevocationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyShutdownDurationInput")
    def encryption_key_shutdown_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyShutdownDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="gpuZonalRedundancyDisabledInput")
    def gpu_zonal_redundancy_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gpuZonalRedundancyDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelectorInput")
    def node_selector_input(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateNodeSelector]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateNodeSelector], jsii.get(self, "nodeSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessInput")
    def vpc_access_input(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateVpcAccess"]:
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateVpcAccess"], jsii.get(self, "vpcAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f9141fb410db568bd048f9cf734eb2edd0a9878932409043b0792a43531ead6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16517eb5a45f332a7ee1489d6f579a084e07059d6fa256cc2e40d4789421033e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyRevocationAction")
    def encryption_key_revocation_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyRevocationAction"))

    @encryption_key_revocation_action.setter
    def encryption_key_revocation_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09836793df054267a36694d811299d9ea6b86a56e3738e3a3fc2fb0ac09b0784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyRevocationAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyShutdownDuration")
    def encryption_key_shutdown_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeyShutdownDuration"))

    @encryption_key_shutdown_duration.setter
    def encryption_key_shutdown_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f884778e53a89a204c24bfd7e50706ad0b25b6d1044c3eadcbfa39901f00d715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeyShutdownDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpuZonalRedundancyDisabled")
    def gpu_zonal_redundancy_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "gpuZonalRedundancyDisabled"))

    @gpu_zonal_redundancy_disabled.setter
    def gpu_zonal_redundancy_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9925ae95f308c47d905c8db170c91d6f1d85e101d885001578b8bd5e6c2c9633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuZonalRedundancyDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__397f442b11cb43a3f73b95e01b3c92d8a4db9bd445eb9048514dc96e405fbfe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc31ea8e870a41b26b232ab38f1da346a0fcfe31470ba589d94845fcc2c3c4ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4666f65acac9ba5323626ebcef1499f189cf68f409b83c7fe51166bdbd0a766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2WorkerPoolTemplate]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b90a4929360b08c62460ee8f56f91a88e27368ab8969fb9705a1a85a263c05d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumes",
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
class CloudRunV2WorkerPoolTemplateVolumes:
    def __init__(
        self,
        *,
        name: builtins.str,
        cloud_sql_instance: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        empty_dir: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateVolumesEmptyDir", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateVolumesGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        nfs: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateVolumesNfs", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["CloudRunV2WorkerPoolTemplateVolumesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Volume's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        :param cloud_sql_instance: cloud_sql_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#cloud_sql_instance CloudRunV2WorkerPool#cloud_sql_instance}
        :param empty_dir: empty_dir block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#empty_dir CloudRunV2WorkerPool#empty_dir}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#gcs CloudRunV2WorkerPool#gcs}
        :param nfs: nfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#nfs CloudRunV2WorkerPool#nfs}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret CloudRunV2WorkerPool#secret}
        '''
        if isinstance(cloud_sql_instance, dict):
            cloud_sql_instance = CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance(**cloud_sql_instance)
        if isinstance(empty_dir, dict):
            empty_dir = CloudRunV2WorkerPoolTemplateVolumesEmptyDir(**empty_dir)
        if isinstance(gcs, dict):
            gcs = CloudRunV2WorkerPoolTemplateVolumesGcs(**gcs)
        if isinstance(nfs, dict):
            nfs = CloudRunV2WorkerPoolTemplateVolumesNfs(**nfs)
        if isinstance(secret, dict):
            secret = CloudRunV2WorkerPoolTemplateVolumesSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287856f82aba7150d099697e59eb67729f305ccea07121b1672c1b757497fa7b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#name CloudRunV2WorkerPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_sql_instance(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance"]:
        '''cloud_sql_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#cloud_sql_instance CloudRunV2WorkerPool#cloud_sql_instance}
        '''
        result = self._values.get("cloud_sql_instance")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance"], result)

    @builtins.property
    def empty_dir(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateVolumesEmptyDir"]:
        '''empty_dir block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#empty_dir CloudRunV2WorkerPool#empty_dir}
        '''
        result = self._values.get("empty_dir")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateVolumesEmptyDir"], result)

    @builtins.property
    def gcs(self) -> typing.Optional["CloudRunV2WorkerPoolTemplateVolumesGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#gcs CloudRunV2WorkerPool#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateVolumesGcs"], result)

    @builtins.property
    def nfs(self) -> typing.Optional["CloudRunV2WorkerPoolTemplateVolumesNfs"]:
        '''nfs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#nfs CloudRunV2WorkerPool#nfs}
        '''
        result = self._values.get("nfs")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateVolumesNfs"], result)

    @builtins.property
    def secret(self) -> typing.Optional["CloudRunV2WorkerPoolTemplateVolumesSecret"]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret CloudRunV2WorkerPool#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateVolumesSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance:
    def __init__(
        self,
        *,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#instances CloudRunV2WorkerPool#instances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad90091ad544b7c5acf17a93e28a76d76a0db4e52bd6c7b820edc7b1fcbae4d)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instances is not None:
            self._values["instances"] = instances

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#instances CloudRunV2WorkerPool#instances}
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8172edd53404421a3d9b2fbbef446549b62a74111d43fe6e57e13efb884a1bc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db409a018d9252f72a3bbac117fe6c0e728dfb678f1c26a278238c8cd0b6481e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9678faa46293ac2deb7f9e6c2050b9844316eb8032b97484e5d71ce853d35a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesEmptyDir",
    jsii_struct_bases=[],
    name_mapping={"medium": "medium", "size_limit": "sizeLimit"},
)
class CloudRunV2WorkerPoolTemplateVolumesEmptyDir:
    def __init__(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#medium CloudRunV2WorkerPool#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#size_limit CloudRunV2WorkerPool#size_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a458cc15f4195d8c576919feabbd630c41d76e3575701cbe594d63a9bf52dfb)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#medium CloudRunV2WorkerPool#medium}
        '''
        result = self._values.get("medium")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_limit(self) -> typing.Optional[builtins.str]:
        '''Limit on the storage usable by this EmptyDir volume.

        The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#size_limit CloudRunV2WorkerPool#size_limit}
        '''
        result = self._values.get("size_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVolumesEmptyDir(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateVolumesEmptyDirOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesEmptyDirOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f80901613abb8909566d7c95d2b0e8b90c33e569105058ac065467a528404548)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2c6267a4f0f8427c02b90aefb2d01fd569c31b1935a07dd38b479ffd0cda216)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "medium", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeLimit")
    def size_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeLimit"))

    @size_limit.setter
    def size_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ab6eb4a7925e3ef17c4dcbe3922c41baf0b9b7ce51fb48aa8f8b53458be37c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesEmptyDir]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesEmptyDir], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesEmptyDir],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7934baf8c023e2103fbdd2f059caabd5c71fc3b0181e4c997001c9b72968b9a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "read_only": "readOnly"},
)
class CloudRunV2WorkerPoolTemplateVolumesGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket: GCS Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#bucket CloudRunV2WorkerPool#bucket}
        :param read_only: If true, mount the GCS bucket as read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#read_only CloudRunV2WorkerPool#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510998696bc83f19fc3053a13744ac9a4aabde1c43669978c7a1baa71af5d4ad)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def bucket(self) -> builtins.str:
        '''GCS Bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#bucket CloudRunV2WorkerPool#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount the GCS bucket as read-only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#read_only CloudRunV2WorkerPool#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVolumesGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateVolumesGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46c5bd8d79960715b4917027fbd62153a326a7dc4d501961d573437b13717ae5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32e254f7187d99081b7e9d98e0d120959d8a4927cdddeec15e2e7dda71ad6fe2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55c5c2bf56d4e0b38646ac30645fcfb145c263544a1389f2141a297ab6e06f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesGcs]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d8c331f6507b2277c3a5ee8a0714a07ec6af41ad5d294cdf6e4bb673f2ba4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b833aee85960d3403eb59bd47609b4ed5cec04bbb4a956f8d22492cfdb773365)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolTemplateVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9590b889a7f1a49517ce204b38e11262bb994b8f1f3444cb722f09f0e858d9e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolTemplateVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b08ec607f1c083c5f7f9c9934239cd397861153afa771f80c8c6fe84dfa06950)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b26175de4f4ae2eb3469cec1bd3fe6f7cbb78e1f1314832f5322c8f179170c18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03b482340f606838ff202e2353934450759b0681644816ef536b74802df798dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83f04814b99c8d0007a0482b0762c11ef8df4c584f592aa6ab3e5d29ecb9a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesNfs",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "server": "server", "read_only": "readOnly"},
)
class CloudRunV2WorkerPoolTemplateVolumesNfs:
    def __init__(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path that is exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#path CloudRunV2WorkerPool#path}
        :param server: Hostname or IP address of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#server CloudRunV2WorkerPool#server}
        :param read_only: If true, mount the NFS volume as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#read_only CloudRunV2WorkerPool#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47b35483992062648093fe938a0982539e286e7379ab77d012ddf7e927fe0725)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "server": server,
        }
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def path(self) -> builtins.str:
        '''Path that is exported by the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#path CloudRunV2WorkerPool#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Hostname or IP address of the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#server CloudRunV2WorkerPool#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount the NFS volume as read only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#read_only CloudRunV2WorkerPool#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVolumesNfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateVolumesNfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesNfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e854227e0a95c6bae805ca4ca1feadc9544034b2416c932a5b7091bf42047fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__55e9146f7d7b673343b9d4d6d5895e9ad34588a4218743f6ae5f2f6b740fe125)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16d9aded43bbb6983ed525fe2a0d6b084ecd09a7f7d50ca852423a583a393b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b804e5b219506dbc404af76572755726511595f1a624daa1f095c908656eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesNfs]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesNfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesNfs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59a727f4e71a5c7fb888ae5d2a99fd9c172b62be87d8d1b765d2dcc6cbb4f49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb32702fd2b1b32259c4169c54e4b6bb97edfd3157567eeef4d8258e9793ebd8)
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
        :param instances: The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#instances CloudRunV2WorkerPool#instances}
        '''
        value = CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance(
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
        :param medium: The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#medium CloudRunV2WorkerPool#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#size_limit CloudRunV2WorkerPool#size_limit}
        '''
        value = CloudRunV2WorkerPoolTemplateVolumesEmptyDir(
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
        :param bucket: GCS Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#bucket CloudRunV2WorkerPool#bucket}
        :param read_only: If true, mount the GCS bucket as read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#read_only CloudRunV2WorkerPool#read_only}
        '''
        value = CloudRunV2WorkerPoolTemplateVolumesGcs(
            bucket=bucket, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putNfs")
    def put_nfs(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path that is exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#path CloudRunV2WorkerPool#path}
        :param server: Hostname or IP address of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#server CloudRunV2WorkerPool#server}
        :param read_only: If true, mount the NFS volume as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#read_only CloudRunV2WorkerPool#read_only}
        '''
        value = CloudRunV2WorkerPoolTemplateVolumesNfs(
            path=path, server=server, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putNfs", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        *,
        secret: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret CloudRunV2WorkerPool#secret}
        :param default_mode: Integer representation of mode bits to use on created files by default. Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#default_mode CloudRunV2WorkerPool#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#items CloudRunV2WorkerPool#items}
        '''
        value = CloudRunV2WorkerPoolTemplateVolumesSecret(
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
    ) -> CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstanceOutputReference:
        return typing.cast(CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstanceOutputReference, jsii.get(self, "cloudSqlInstance"))

    @builtins.property
    @jsii.member(jsii_name="emptyDir")
    def empty_dir(self) -> CloudRunV2WorkerPoolTemplateVolumesEmptyDirOutputReference:
        return typing.cast(CloudRunV2WorkerPoolTemplateVolumesEmptyDirOutputReference, jsii.get(self, "emptyDir"))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(self) -> CloudRunV2WorkerPoolTemplateVolumesGcsOutputReference:
        return typing.cast(CloudRunV2WorkerPoolTemplateVolumesGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="nfs")
    def nfs(self) -> CloudRunV2WorkerPoolTemplateVolumesNfsOutputReference:
        return typing.cast(CloudRunV2WorkerPoolTemplateVolumesNfsOutputReference, jsii.get(self, "nfs"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "CloudRunV2WorkerPoolTemplateVolumesSecretOutputReference":
        return typing.cast("CloudRunV2WorkerPoolTemplateVolumesSecretOutputReference", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstanceInput")
    def cloud_sql_instance_input(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance], jsii.get(self, "cloudSqlInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyDirInput")
    def empty_dir_input(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesEmptyDir]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesEmptyDir], jsii.get(self, "emptyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(self) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesGcs]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsInput")
    def nfs_input(self) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesNfs]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesNfs], jsii.get(self, "nfsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional["CloudRunV2WorkerPoolTemplateVolumesSecret"]:
        return typing.cast(typing.Optional["CloudRunV2WorkerPoolTemplateVolumesSecret"], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb7618b832d90514417f2544c860a5399e024c78f4c953b87c9a59ba46b78cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8785a724149442e1e0b3cfb3b610b49df92481a0fcafa7f61be789354adb09b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesSecret",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "default_mode": "defaultMode", "items": "items"},
)
class CloudRunV2WorkerPoolTemplateVolumesSecret:
    def __init__(
        self,
        *,
        secret: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret CloudRunV2WorkerPool#secret}
        :param default_mode: Integer representation of mode bits to use on created files by default. Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#default_mode CloudRunV2WorkerPool#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#items CloudRunV2WorkerPool#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66a6046ef6acacc7553ff0dc0da1e71bddabd0c929276f19b546cced2df13d5)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#secret CloudRunV2WorkerPool#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_mode(self) -> typing.Optional[jsii.Number]:
        '''Integer representation of mode bits to use on created files by default.

        Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#default_mode CloudRunV2WorkerPool#default_mode}
        '''
        result = self._values.get("default_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateVolumesSecretItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#items CloudRunV2WorkerPool#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateVolumesSecretItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVolumesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesSecretItems",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "mode": "mode", "version": "version"},
)
class CloudRunV2WorkerPoolTemplateVolumesSecretItems:
    def __init__(
        self,
        *,
        path: builtins.str,
        mode: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The relative path of the secret in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#path CloudRunV2WorkerPool#path}
        :param mode: Integer octal mode bits to use on this file, must be a value between 01 and 0777 (octal). If 0 or not set, the Volume's default mode will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#mode CloudRunV2WorkerPool#mode}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#version CloudRunV2WorkerPool#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3472879057808705df274165c175faf113c74d399e988811487187f530a6aa8)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
        }
        if mode is not None:
            self._values["mode"] = mode
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def path(self) -> builtins.str:
        '''The relative path of the secret in the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#path CloudRunV2WorkerPool#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        '''Integer octal mode bits to use on this file, must be a value between 01 and 0777 (octal).

        If 0 or not set, the Volume's default mode will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#mode CloudRunV2WorkerPool#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Cloud Secret Manager secret version.

        Can be 'latest' for the latest value or an integer for a specific version

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#version CloudRunV2WorkerPool#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVolumesSecretItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateVolumesSecretItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesSecretItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79fdfb89f69045ac1f0aefa42c94f2a3458b25cb0d509c685c08b47d4db53d12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolTemplateVolumesSecretItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e07f3f93302bb030a044811159f1fc5a7ec53d079b8aff46253c7ab047e38778)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolTemplateVolumesSecretItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18853d18da5bc921e38ee747e6ca75bea7fd10313f587bd5530d0449f197e2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f80e198cae9d4481858aca613dc31ae3981a80ada5949f4801d3d12d39fc04e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75d74b77d05e7b1d50e2d769b58a22644b8dc2c344c79c01b95b7f804536bd1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumesSecretItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumesSecretItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6d4863cff9dce8e2ba7ae8f8b85a0085f804ed190d72acd5e6a8a01d2ca3a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateVolumesSecretItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesSecretItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc911587b767851428521780f89c1b0c80f673bcc152d706844fbedd886fb03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMode")
    def reset_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMode", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1e09a3313fb034530d43ac087204d3755b50b4dc911de82c01e89858bbe278e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d6aa042e054a0e1ed4e7f398dde666a9e6cf5bf0b2ee0b8f6ac582c0046cd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ef47e45d32004491fd343b13757f78e6e3da5ced398ce2b9ef4ada186a922b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVolumesSecretItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVolumesSecretItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVolumesSecretItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61627023d5b58424370a060e11804c990d3689d0386d7c59beeaaa098dcef85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateVolumesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVolumesSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ad58812dbd01e37a060c525a1e583cc3176851dc2fa7097b2239e9b69e415c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719c486513bf6b682412500d57323f74f2896329a1702ea82de17c393baa3784)
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
    def items(self) -> CloudRunV2WorkerPoolTemplateVolumesSecretItemsList:
        return typing.cast(CloudRunV2WorkerPoolTemplateVolumesSecretItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="defaultModeInput")
    def default_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultModeInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumesSecretItems]]], jsii.get(self, "itemsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__20473a891bd4c3fd0f13cc3f948f5a054ff59d4ba901f6d6fb86f063c76ef145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9608d52724b231560e87e4dd6180d39e89b57a61952742b2f54c1aa1558632f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudRunV2WorkerPoolTemplateVolumesSecret]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVolumesSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a94bfcbdf1c42b6fed01b4ea64183906a4e3416589120a7cc79b47be778123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVpcAccess",
    jsii_struct_bases=[],
    name_mapping={"egress": "egress", "network_interfaces": "networkInterfaces"},
)
class CloudRunV2WorkerPoolTemplateVpcAccess:
    def __init__(
        self,
        *,
        egress: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param egress: Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#egress CloudRunV2WorkerPool#egress}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#network_interfaces CloudRunV2WorkerPool#network_interfaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538ee960996a3a9a8f23bc068c29ee9d9517a4ad2b3c87d89c84b01c611c7205)
            check_type(argname="argument egress", value=egress, expected_type=type_hints["egress"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if egress is not None:
            self._values["egress"] = egress
        if network_interfaces is not None:
            self._values["network_interfaces"] = network_interfaces

    @builtins.property
    def egress(self) -> typing.Optional[builtins.str]:
        '''Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#egress CloudRunV2WorkerPool#egress}
        '''
        result = self._values.get("egress")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces"]]]:
        '''network_interfaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#network_interfaces CloudRunV2WorkerPool#network_interfaces}
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVpcAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "subnetwork": "subnetwork", "tags": "tags"},
)
class CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: The VPC network that the Cloud Run resource will be able to send traffic to. At least one of network or subnetwork must be specified. If both network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If network is not specified, it will be looked up from the subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#network CloudRunV2WorkerPool#network}
        :param subnetwork: The VPC subnetwork that the Cloud Run resource will get IPs from. At least one of network or subnetwork must be specified. If both network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If subnetwork is not specified, the subnetwork with the same name with the network will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#subnetwork CloudRunV2WorkerPool#subnetwork}
        :param tags: Network tags applied to this Cloud Run WorkerPool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#tags CloudRunV2WorkerPool#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41e60df6fba390b6052b2f266bc843ca1b8f7ae1529a51c8b42948b232cd2d1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#network CloudRunV2WorkerPool#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The VPC subnetwork that the Cloud Run resource will get IPs from.

        At least one of network or subnetwork must be specified. If both
        network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If subnetwork is not specified, the
        subnetwork with the same name with the network will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#subnetwork CloudRunV2WorkerPool#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Network tags applied to this Cloud Run WorkerPool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#tags CloudRunV2WorkerPool#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac849733debf0cd1aa487cf2e6f71f722410101e9fb0a06001e40a8284fbe17b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d364c216d76d6e58d8d1bf0788d3e759f1227c1725b6b738e75fc05a4caea4f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7cd7f67d064b71bc163973e6474372e59634263a34937c43163ae1dc345807)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4dfa3f4cb7c452904204af2eb4ef03e65e0e5d4687ca682aed1e313d7473a4dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e48d93b0b75de4d74c39c186fb8987fe1fe560eaedcc8e06178ab3858c2e0a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaaa8143b49f49b9314e3ed92aa57c51b8e3c14043314ccc361224b060078322)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67798c4b74e09cbc62f3ab725954eb238d08b70598e4ea26cf5a07c9c1444734)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f530cc0b81add8ada39b5d26de840c76bc5659ab69a74b9020578179e673762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cc94b0b991b0579d4fcbe941301f4ce5eea7f12b6448194b17e2a2ec9fffd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5bc1ad170d18cbf29ddc26dac4c0c080d0ca2212c446cec37033d65472d6d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b251388527359c1063498188cf657aa0e984202eabf1105c3fa8834e9ac89fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTemplateVpcAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTemplateVpcAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e04984e79a6f173af7eec54188bb3b51611cb8cce192cb525713daad771e2cff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkInterfaces")
    def put_network_interfaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf8140578a684a5b751afd4f1c067c8bac2f6a83c820abbc264e9a04e41c562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterfaces", [value]))

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
    ) -> CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesList:
        return typing.cast(CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesList, jsii.get(self, "networkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="egressInput")
    def egress_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "egressInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfacesInput")
    def network_interfaces_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]]], jsii.get(self, "networkInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="egress")
    def egress(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egress"))

    @egress.setter
    def egress(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15fc3c33e38fb5b86ab38cd0618b445119d91236af47864938e0b469be4b783a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudRunV2WorkerPoolTemplateVpcAccess]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTemplateVpcAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTemplateVpcAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3214f97d0dc31eb70ad521c4a4ab10a25b4fdfecfdd470a0389925181881554b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTerminalCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudRunV2WorkerPoolTerminalCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTerminalCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTerminalConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTerminalConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2734503fcd55d6af60c6e96591b03b3f209e5e6aceb02912faa2112bbab0efe7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudRunV2WorkerPoolTerminalConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78f33ece278feb38a265b8f6d00c25a0abcbf468e270b13af4223b84ccb2960)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudRunV2WorkerPoolTerminalConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__313a7bf688f5850c8d60f60ced968ca15f80b80cb39222525dc9fd4865c8eedb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6881778b050247578eec4adb6021c95ad9615c4190a22a2e8910d6ac334d930)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f841b3234e349bef0f1980b650b64e750a7d8f90f8228a333136f2f90f1bd20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CloudRunV2WorkerPoolTerminalConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTerminalConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c92e6fc16d898ca5e1d0d5656829b2fff8cb31d1394aee63464e10b1a62c251)
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
    def internal_value(self) -> typing.Optional[CloudRunV2WorkerPoolTerminalCondition]:
        return typing.cast(typing.Optional[CloudRunV2WorkerPoolTerminalCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudRunV2WorkerPoolTerminalCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5b692a988bad6d6f10eebf1a4cce2591a6c9d90bf9415e9bd000ae1dd1b1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudRunV2WorkerPoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#create CloudRunV2WorkerPool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#delete CloudRunV2WorkerPool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#update CloudRunV2WorkerPool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7569bbe15ed477f241952ee6b3e22ffeb574f769355ae570b61038e43299291d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#create CloudRunV2WorkerPool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#delete CloudRunV2WorkerPool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/cloud_run_v2_worker_pool#update CloudRunV2WorkerPool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudRunV2WorkerPoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudRunV2WorkerPoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudRunV2WorkerPool.CloudRunV2WorkerPoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4753fd9b582a5bd44ef76d1467977152ccdef31fd4ae070203999a23bf6838b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4934810c30509fe49b770c75a1f77211f348de8debed6b5580f645d62cf423f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d533aee63e1792acc0d807aa7038927f25f16ecd2129636b79904248d1e8ceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a706e0d981225f5d6bc9a9aec8f60ec4584f3df08ddea322600667e1e0ad75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ececc392aa56721af4cc9566efb208dac996fff1b4ec4cf62f095a42b80b30d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CloudRunV2WorkerPool",
    "CloudRunV2WorkerPoolBinaryAuthorization",
    "CloudRunV2WorkerPoolBinaryAuthorizationOutputReference",
    "CloudRunV2WorkerPoolConditions",
    "CloudRunV2WorkerPoolConditionsList",
    "CloudRunV2WorkerPoolConditionsOutputReference",
    "CloudRunV2WorkerPoolConfig",
    "CloudRunV2WorkerPoolInstanceSplitStatuses",
    "CloudRunV2WorkerPoolInstanceSplitStatusesList",
    "CloudRunV2WorkerPoolInstanceSplitStatusesOutputReference",
    "CloudRunV2WorkerPoolInstanceSplits",
    "CloudRunV2WorkerPoolInstanceSplitsList",
    "CloudRunV2WorkerPoolInstanceSplitsOutputReference",
    "CloudRunV2WorkerPoolScaling",
    "CloudRunV2WorkerPoolScalingOutputReference",
    "CloudRunV2WorkerPoolTemplate",
    "CloudRunV2WorkerPoolTemplateContainers",
    "CloudRunV2WorkerPoolTemplateContainersEnv",
    "CloudRunV2WorkerPoolTemplateContainersEnvList",
    "CloudRunV2WorkerPoolTemplateContainersEnvOutputReference",
    "CloudRunV2WorkerPoolTemplateContainersEnvValueSource",
    "CloudRunV2WorkerPoolTemplateContainersEnvValueSourceOutputReference",
    "CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef",
    "CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRefOutputReference",
    "CloudRunV2WorkerPoolTemplateContainersList",
    "CloudRunV2WorkerPoolTemplateContainersOutputReference",
    "CloudRunV2WorkerPoolTemplateContainersResources",
    "CloudRunV2WorkerPoolTemplateContainersResourcesOutputReference",
    "CloudRunV2WorkerPoolTemplateContainersVolumeMounts",
    "CloudRunV2WorkerPoolTemplateContainersVolumeMountsList",
    "CloudRunV2WorkerPoolTemplateContainersVolumeMountsOutputReference",
    "CloudRunV2WorkerPoolTemplateNodeSelector",
    "CloudRunV2WorkerPoolTemplateNodeSelectorOutputReference",
    "CloudRunV2WorkerPoolTemplateOutputReference",
    "CloudRunV2WorkerPoolTemplateVolumes",
    "CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance",
    "CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstanceOutputReference",
    "CloudRunV2WorkerPoolTemplateVolumesEmptyDir",
    "CloudRunV2WorkerPoolTemplateVolumesEmptyDirOutputReference",
    "CloudRunV2WorkerPoolTemplateVolumesGcs",
    "CloudRunV2WorkerPoolTemplateVolumesGcsOutputReference",
    "CloudRunV2WorkerPoolTemplateVolumesList",
    "CloudRunV2WorkerPoolTemplateVolumesNfs",
    "CloudRunV2WorkerPoolTemplateVolumesNfsOutputReference",
    "CloudRunV2WorkerPoolTemplateVolumesOutputReference",
    "CloudRunV2WorkerPoolTemplateVolumesSecret",
    "CloudRunV2WorkerPoolTemplateVolumesSecretItems",
    "CloudRunV2WorkerPoolTemplateVolumesSecretItemsList",
    "CloudRunV2WorkerPoolTemplateVolumesSecretItemsOutputReference",
    "CloudRunV2WorkerPoolTemplateVolumesSecretOutputReference",
    "CloudRunV2WorkerPoolTemplateVpcAccess",
    "CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces",
    "CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesList",
    "CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfacesOutputReference",
    "CloudRunV2WorkerPoolTemplateVpcAccessOutputReference",
    "CloudRunV2WorkerPoolTerminalCondition",
    "CloudRunV2WorkerPoolTerminalConditionList",
    "CloudRunV2WorkerPoolTerminalConditionOutputReference",
    "CloudRunV2WorkerPoolTimeouts",
    "CloudRunV2WorkerPoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__dd21e3cb2f2c93dce353d82aa3c65b21b5812dc7a961fdcec7a7da3cf2c13e01(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    template: typing.Union[CloudRunV2WorkerPoolTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[CloudRunV2WorkerPoolBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    client_version: typing.Optional[builtins.str] = None,
    custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_splits: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolInstanceSplits, typing.Dict[builtins.str, typing.Any]]]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_stage: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[CloudRunV2WorkerPoolScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudRunV2WorkerPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6cc1c6617d69b5275bdce15c08280681dc94e3dade280866767a760492f651b6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e6a5d0d7db37174841f049a367eae9178621e9cacfb164481df5da20d05e67(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolInstanceSplits, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d5f1775d6042f9f62b168a9e1081498f96d49f25e29a7e6543600238a1373a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15232a63b3aea8d73a549b0074496b83209323aace6fed4fd77ac037552a27d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c3e025ea5e4a7f63e50f2ad1293ad8e037a045f89c76690dd700bf2901152dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99cfbe10d4001a9a152f32409d9af0a59db39818cd73d52807081c799e6a2213(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb45a604cf2468d5363e85a8e5d84d4c2e8863012bafbed7122e2ede55daf66d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acfb57833f1caeaa23f5dc911458eda3c16c0b8fef9b18640b45a4d647a98369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507f794d4b6acf5096602281fe154bcad1a943e29fb49be74c3dc6a0cbc80706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea6fbdaa00e46622decc5d4773ddb611608c8fc7fd3f21386948e61adede6f4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d17225356c6e3e75bf6edcb5d4f1c81896da0de0bbc7c4ff88a52f05c0cc854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5c9c213b785cb0a1ff9592db0857a0b1a9844011d5f083b6dc59b9c8ad6f206(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77c7d133b5eb24d7694d6b53548f73a1143f74d12f37d0f97a68e51203c1c73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65b729ca257c5e8f79e8fdb6657d375d5d23c9da9e00f6b9a096fe97baf3f22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc8f3e8502c474a0ae5443b04bbde4b62145dbb2ff7f0332a6713d4c0207f02a(
    *,
    breakglass_justification: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21138ec96d1d85e6518418a86215e4de9828aa8109c099b1ad73dd55d76e18ed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d5b57c29a6bb4f5d424fa3f8e371daec102746483c232ddf994d5f4172ddc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d61ed671a282dcedf4dea1d2bb2cab8feaaa82a50ac98da6dd839dd1ee5aaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47117fd64527a702a46bc333665f8e5e1a59b37d0da45560dc3da236376bf7f8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a92caeb1b029231cb29a74fcadbe8b8a752183daf7b86c3a78afa7e6666e6f(
    value: typing.Optional[CloudRunV2WorkerPoolBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba0f593bffc76d306761a4e1955adcd9fae7684763c1dc06e1a161276021288(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1563ce4ea8e0bd9dab4e15f5aa4038adaf8ac9157c84c07d02a84d84814595(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d831117986c1729769983d4df9ddc489d0bed9aa4500329042e8c59358eb0d38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0618601dea149028f0b7027786067d31430719676838d4235fb0ae5070b8bb5c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd0788fb0104f605cfe373a8d8366963d169174360bf3c55372a78795a8f2bd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413923ea7ca9f2ece275c19f61a6b6b381fe820c0c4bbcd6b2589942570f9afc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7b74031323221798bd56eef072a8de6f76d75bed5d51f429b91979340fb93a(
    value: typing.Optional[CloudRunV2WorkerPoolConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a4dd2d9e45f4f53503385f351cf10249201c7c60d0694bf83aa7f8cdc2c46a(
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
    template: typing.Union[CloudRunV2WorkerPoolTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[CloudRunV2WorkerPoolBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    client_version: typing.Optional[builtins.str] = None,
    custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_splits: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolInstanceSplits, typing.Dict[builtins.str, typing.Any]]]]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_stage: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[CloudRunV2WorkerPoolScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[CloudRunV2WorkerPoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1666d668c501adf9c11c69776f3f9c318265bad2752ee4ae68950006929bca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78acd06c350f117a538519bee75a318c0da60393ee4eeba011c9a365f7f4025f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22aab820860bf51b98e0954d28f9ebb71dc77652a26e2aa8d450fe7027030302(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d91fb889b6fa780f01ca49a215d5efef24bcdaa302bd6a638ce2dd0dbdec8511(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648b198fc8d76c3dd4845329083346bc4178cf72904409a369e2a0ee9dd63b4c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2972cde6dc6035c74a3f0d7c1c12a6a0b92c3e82cda5cbb3a1d7fe27d2beb0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab37d2d4823bf1b6c7d48e15db5920f44a5874697b5c92656fcedcc968b645a2(
    value: typing.Optional[CloudRunV2WorkerPoolInstanceSplitStatuses],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b6875951bfa046e0c0e3e2a6ef291bd9bc92cdff2bc2d651d2ed0407b0ce59(
    *,
    percent: typing.Optional[jsii.Number] = None,
    revision: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756fb178bce926137c235f4b54fd4062d84f042cb5f1164b45189eb9a8977ce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f1220a7d559736044cc203ae14317455b80abcd53a0e0af990deb1b4b43fbf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469f5db3393dbc40d62a715544810336c44ea79636169151a294e315309bda31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa0efe4a688c2f2ca45ced91a3a9cf651fe6a238dab5ded4240108824c473160(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21dc550d713bdfe04a3380e229b26f2f333090509cb623398f6c29a38aa143a4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18547c20d426dde05d1f8d5fe533847c8325d0c6e460aa1a97b5922de1b985de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolInstanceSplits]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d556cef40f7ddad2c4a35e50a62f8decf4a266353e7c5f40b8e61987198040(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7688e71d04fee4d37afd9d2ca25d194cfff04dc664c2299b6b0d07b24f8e8239(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2269684427ce93d4d98e516e5b3c470841541b64e6ad2db21047792f5b5e5491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbbe83df8191a2d3dd70c6fb0882643b968c65c8d247386a052452348617de56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5184e33f42fff992e738aa7b23d29d6dc05d816f5ab69bda4542c5273dafb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolInstanceSplits]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3ad3ae8d86daf2705443d05fde68c1c852d2e355b56920f37ab46482a13de9(
    *,
    manual_instance_count: typing.Optional[jsii.Number] = None,
    max_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
    scaling_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__babbaf0252b73eb578e7bc30fb313e7ad0d60ef83add0ea947321e4c25ebd357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd176821aacde356e7a32473dd51196c30db1639b39a55400f2e7b7d6b4f3ee6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b36174ca60bac4fe01e55794ca5996394a4c98f4ce45bd1868c21fcabd36b6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0961211fe0752ea6ebc38d922393e54f37771d3095491b79f6564b7939466a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01fc48400031add2b616aaf8a6ed5fb6e3c294ed5697f3ad87a9ead71775202e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba0b22410b7fecaf18f2efec4c9acab6841966f7849933d39b0b0ce08485e46(
    value: typing.Optional[CloudRunV2WorkerPoolScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f0210d87d8040e86c3d2051f85ee4709b1fc395037f66ff0485d4be2c6925d(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateContainers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    encryption_key_revocation_action: typing.Optional[builtins.str] = None,
    encryption_key_shutdown_duration: typing.Optional[builtins.str] = None,
    gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_selector: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateNodeSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    revision: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vpc_access: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateVpcAccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58b71ddcceeca73442e3150f2162d4717b371d1cb4283df4c7f91f5a54e0b41(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateContainersResources, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c3b878b91800befdc5a7792c1e01ac0b50b9e4aef2f0ac2f554440d7f203cd(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
    value_source: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateContainersEnvValueSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6cc57177c0e04df33a82103075522c4636c6b5536b1771354191a79e12bd217(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7daaceecc5bd40c2f6b4757d0e929a0990e33c64f27d1672ab3f5b3d9e4a98a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bdebc481f6e79b7a32dd654249f567c13f3164577efaa990ab565997f14f1c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd952a0740e3e2f7aece6b27a6a8c6492e0ecf8bdc97ba4c20c34eaf58d28d60(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207b9db6b6330ef477034ee2c1a34cbed887d5fdeabe9cd1e34159d128a132d4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51bced51d6d3861cb59369968610c76d79343950fad217f2acf17886fb09ebe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cae500e0b7d0293bc79555a5958573239700fa32cff3d283fda6f52e632902e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351205b33f34735d85225dbb8cb1571daed9058a4d611ca430bca1ff68854a5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c04877ce4d5198d6181fcd5a38016afeba50f9d190878a78101b36e6be78869a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ac9dfa91145330a13284a294a9b5c0fd3fdf2f4016b87944266ac87cf22b08(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainersEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c64e26bcecf9ae1f10781dade2fdd5512ed7023119d3265f52affc0b779bf3d(
    *,
    secret_key_ref: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb487b8dfc8e6e8ff20c3b638119f845e1fa5e6f371fbcdb20f2094349f587e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee284c0dd8987045474f402ed6f799d44bd33da0c1242545037508c5cc1a038(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateContainersEnvValueSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab719dbffc8e82b65afd88673b0a10b1dffacc66f5d43f9fcfe1d49c975537df(
    *,
    secret: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2d886b23c1dabf436fea1d0488d4b4c0003ec0e963604e595cf1016095e439(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c322bb6d27a9f8802f3c460f0cf391fcd8d7b5da57795ca543255aa46951d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6177ee2d9114e4970365588bdc1e2a5057f7d338293bd3d70a75669aafdfa28b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86752061dfc3086f08c98db8c46c0706ed092d5cbbdd0fdc57cd90b9b499ca60(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateContainersEnvValueSourceSecretKeyRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbca2e68ee4ce69161d1c771b4eec3919c0d0978dabd9716bc43a3792e357a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fae0f84a9df18cebf64f46d42e0fc6182019facce0edbc43113a64b5f7e43b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1df5faddb4743fad136321a5d73a43d1c5b780e54af8da6c5a2bbef15c54d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b008b3d6621f0f2976d596920a6cb045f7a528ecdc97fa5cda30f442adbcb0d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba854db103663c2fda1045f0a6dd8d2a247ee6dcac27f03fde05a208470489d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86163a90432a8544f6524468f2251bc7a6de977707485f286c12c1f7ae312393(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465f8d0ddba5d277159924da2a23fd5d58088499d1b5626fef412b9190cbb144(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029fc24d9d0857ab157f8d405941aed1bca066664aefaca7f9ba1c8a90cbbc30(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdaa49b242d5bf7c36d1340595304e545252f84b656d98b5df5c2b88a30eee7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2349f4148bf91a2f89049192a712c91bb3a23f60113ce8b68d39834631fcfdf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d29b7c4ce86a728865c20cbad5fc6ebb07d0c156dee5965618ca84d4b3f6ee9b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fc7ebe80f92efa0ca3c489f14252395d4be0a88fdb6ef1fdc99fd47e1949c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04392e220ef0c1253c7124b58fc548639d8b4b7485f398b65e489ca69155a883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb9a03d6c0c5ec1aac694655f49233f06483741440395c67ed9337e8c88cad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504fb92295791bb6074ca790e53e249fc473345ad5667631615e9a4c7464d47e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262606cb07908937332dd98ca8c0072f88f86da25027cb986e372d54ea2f4418(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b300111fd521033b3e00677e054fb617caa78c703d0486e63f2e20f83e7340d(
    *,
    limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12df50ca501028fbda921a71cb1d943296e022ad77fb6d5f4f7eebd47e23583c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4614d12147ba56fd1e6c4446f6fc64bbafd5ec323ee6a9b0fd11b84721b277e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e991907c620f58fa6a4bb659a77a43774e55727377058c1bf49482247820a358(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateContainersResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c9f6f8e85856bdd810a09813d7ebf9b64a44d9bbce3e0bfdf32fd566adb82d(
    *,
    mount_path: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e42739c89219af89d17ddac6093fa527d439a306e9156fbc2c4dd5eda67b0cfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0eb6bcb1a54b83480895d52bcd637dcc10426920c0fae28c87c11eb7b0c3efc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4dd089a1c96bf24cfb06495fc31f9fc9bf0b9c7cc69e614c8237f1d0818802(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30683208e920f5f06a1d59d232f092dcc1ffbbe129ebcdbf0e90de905537e48a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bde4bc927f4b31dc5b198aeb8d20014e61ef6ff40d7a3e2fbbcba8bdad333e9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22233f303a258ae7f5f7063e1af7a93665722992ccbb19f1471197a6c59b9cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateContainersVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16629e1cd62f89f08240579131bea34d907c1c4977bcb03fca4c1ecacd6b741(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6b9c20dcb7a12119a103e8e071ba33c0e5a44c13739887b115fef65b02cc82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__977646ff69cfa45cfbad563f6b64c6db4064e8b90a6b74ee0e2eb98744312594(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218b50099f251b08071b8d6bab510fccea25d95ddc8fae8432573b6c39ef85aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateContainersVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c2d3bd16403215bcf5334882dc5e5bc449a79f855c04d679473c1b43609606(
    *,
    accelerator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff1d3a5bd3504299931402ed783b5f80f007adc1d6a0afc858ebef51a07904b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f4e91420a3259d6ad73ce18230c89842673d3550f7b996b2e4a1f4520b0669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08dac623d3a325d443723b16ff67f4af549c50696cc9567406ca56950be6454f(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateNodeSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c25dca39a76da84eebe36fd45d2c01e2591e2021a0b69bd0b6ddb9e61fec5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d205c0ae2bddee826e8c0419c8592ad163bf19e55f5972787f02559a01c9eb18(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateContainers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1312c77a8f077281f6ebcde278921b53dcd183a0ec7a61cde3f70deedc396a9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9141fb410db568bd048f9cf734eb2edd0a9878932409043b0792a43531ead6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16517eb5a45f332a7ee1489d6f579a084e07059d6fa256cc2e40d4789421033e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09836793df054267a36694d811299d9ea6b86a56e3738e3a3fc2fb0ac09b0784(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f884778e53a89a204c24bfd7e50706ad0b25b6d1044c3eadcbfa39901f00d715(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9925ae95f308c47d905c8db170c91d6f1d85e101d885001578b8bd5e6c2c9633(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__397f442b11cb43a3f73b95e01b3c92d8a4db9bd445eb9048514dc96e405fbfe5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc31ea8e870a41b26b232ab38f1da346a0fcfe31470ba589d94845fcc2c3c4ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4666f65acac9ba5323626ebcef1499f189cf68f409b83c7fe51166bdbd0a766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b90a4929360b08c62460ee8f56f91a88e27368ab8969fb9705a1a85a263c05d(
    value: typing.Optional[CloudRunV2WorkerPoolTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287856f82aba7150d099697e59eb67729f305ccea07121b1672c1b757497fa7b(
    *,
    name: builtins.str,
    cloud_sql_instance: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    empty_dir: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateVolumesEmptyDir, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateVolumesGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    nfs: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateVolumesNfs, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[CloudRunV2WorkerPoolTemplateVolumesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad90091ad544b7c5acf17a93e28a76d76a0db4e52bd6c7b820edc7b1fcbae4d(
    *,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8172edd53404421a3d9b2fbbef446549b62a74111d43fe6e57e13efb884a1bc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db409a018d9252f72a3bbac117fe6c0e728dfb678f1c26a278238c8cd0b6481e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9678faa46293ac2deb7f9e6c2050b9844316eb8032b97484e5d71ce853d35a1(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesCloudSqlInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a458cc15f4195d8c576919feabbd630c41d76e3575701cbe594d63a9bf52dfb(
    *,
    medium: typing.Optional[builtins.str] = None,
    size_limit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80901613abb8909566d7c95d2b0e8b90c33e569105058ac065467a528404548(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c6267a4f0f8427c02b90aefb2d01fd569c31b1935a07dd38b479ffd0cda216(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ab6eb4a7925e3ef17c4dcbe3922c41baf0b9b7ce51fb48aa8f8b53458be37c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7934baf8c023e2103fbdd2f059caabd5c71fc3b0181e4c997001c9b72968b9a0(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesEmptyDir],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510998696bc83f19fc3053a13744ac9a4aabde1c43669978c7a1baa71af5d4ad(
    *,
    bucket: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c5bd8d79960715b4917027fbd62153a326a7dc4d501961d573437b13717ae5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e254f7187d99081b7e9d98e0d120959d8a4927cdddeec15e2e7dda71ad6fe2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55c5c2bf56d4e0b38646ac30645fcfb145c263544a1389f2141a297ab6e06f14(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d8c331f6507b2277c3a5ee8a0714a07ec6af41ad5d294cdf6e4bb673f2ba4a(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b833aee85960d3403eb59bd47609b4ed5cec04bbb4a956f8d22492cfdb773365(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9590b889a7f1a49517ce204b38e11262bb994b8f1f3444cb722f09f0e858d9e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b08ec607f1c083c5f7f9c9934239cd397861153afa771f80c8c6fe84dfa06950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26175de4f4ae2eb3469cec1bd3fe6f7cbb78e1f1314832f5322c8f179170c18(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b482340f606838ff202e2353934450759b0681644816ef536b74802df798dd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83f04814b99c8d0007a0482b0762c11ef8df4c584f592aa6ab3e5d29ecb9a8d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47b35483992062648093fe938a0982539e286e7379ab77d012ddf7e927fe0725(
    *,
    path: builtins.str,
    server: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e854227e0a95c6bae805ca4ca1feadc9544034b2416c932a5b7091bf42047fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e9146f7d7b673343b9d4d6d5895e9ad34588a4218743f6ae5f2f6b740fe125(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16d9aded43bbb6983ed525fe2a0d6b084ecd09a7f7d50ca852423a583a393b0a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b804e5b219506dbc404af76572755726511595f1a624daa1f095c908656eff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59a727f4e71a5c7fb888ae5d2a99fd9c172b62be87d8d1b765d2dcc6cbb4f49(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesNfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb32702fd2b1b32259c4169c54e4b6bb97edfd3157567eeef4d8258e9793ebd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb7618b832d90514417f2544c860a5399e024c78f4c953b87c9a59ba46b78cb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8785a724149442e1e0b3cfb3b610b49df92481a0fcafa7f61be789354adb09b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66a6046ef6acacc7553ff0dc0da1e71bddabd0c929276f19b546cced2df13d5(
    *,
    secret: builtins.str,
    default_mode: typing.Optional[jsii.Number] = None,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3472879057808705df274165c175faf113c74d399e988811487187f530a6aa8(
    *,
    path: builtins.str,
    mode: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fdfb89f69045ac1f0aefa42c94f2a3458b25cb0d509c685c08b47d4db53d12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e07f3f93302bb030a044811159f1fc5a7ec53d079b8aff46253c7ab047e38778(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d18853d18da5bc921e38ee747e6ca75bea7fd10313f587bd5530d0449f197e2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f80e198cae9d4481858aca613dc31ae3981a80ada5949f4801d3d12d39fc04e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d74b77d05e7b1d50e2d769b58a22644b8dc2c344c79c01b95b7f804536bd1b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6d4863cff9dce8e2ba7ae8f8b85a0085f804ed190d72acd5e6a8a01d2ca3a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVolumesSecretItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc911587b767851428521780f89c1b0c80f673bcc152d706844fbedd886fb03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e09a3313fb034530d43ac087204d3755b50b4dc911de82c01e89858bbe278e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d6aa042e054a0e1ed4e7f398dde666a9e6cf5bf0b2ee0b8f6ac582c0046cd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ef47e45d32004491fd343b13757f78e6e3da5ced398ce2b9ef4ada186a922b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61627023d5b58424370a060e11804c990d3689d0386d7c59beeaaa098dcef85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVolumesSecretItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad58812dbd01e37a060c525a1e583cc3176851dc2fa7097b2239e9b69e415c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719c486513bf6b682412500d57323f74f2896329a1702ea82de17c393baa3784(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20473a891bd4c3fd0f13cc3f948f5a054ff59d4ba901f6d6fb86f063c76ef145(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9608d52724b231560e87e4dd6180d39e89b57a61952742b2f54c1aa1558632f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a94bfcbdf1c42b6fed01b4ea64183906a4e3416589120a7cc79b47be778123(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateVolumesSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538ee960996a3a9a8f23bc068c29ee9d9517a4ad2b3c87d89c84b01c611c7205(
    *,
    egress: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41e60df6fba390b6052b2f266bc843ca1b8f7ae1529a51c8b42948b232cd2d1(
    *,
    network: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac849733debf0cd1aa487cf2e6f71f722410101e9fb0a06001e40a8284fbe17b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d364c216d76d6e58d8d1bf0788d3e759f1227c1725b6b738e75fc05a4caea4f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7cd7f67d064b71bc163973e6474372e59634263a34937c43163ae1dc345807(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dfa3f4cb7c452904204af2eb4ef03e65e0e5d4687ca682aed1e313d7473a4dd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48d93b0b75de4d74c39c186fb8987fe1fe560eaedcc8e06178ab3858c2e0a7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaaa8143b49f49b9314e3ed92aa57c51b8e3c14043314ccc361224b060078322(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67798c4b74e09cbc62f3ab725954eb238d08b70598e4ea26cf5a07c9c1444734(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f530cc0b81add8ada39b5d26de840c76bc5659ab69a74b9020578179e673762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cc94b0b991b0579d4fcbe941301f4ce5eea7f12b6448194b17e2a2ec9fffd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5bc1ad170d18cbf29ddc26dac4c0c080d0ca2212c446cec37033d65472d6d6e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b251388527359c1063498188cf657aa0e984202eabf1105c3fa8834e9ac89fe2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04984e79a6f173af7eec54188bb3b51611cb8cce192cb525713daad771e2cff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf8140578a684a5b751afd4f1c067c8bac2f6a83c820abbc264e9a04e41c562(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudRunV2WorkerPoolTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15fc3c33e38fb5b86ab38cd0618b445119d91236af47864938e0b469be4b783a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3214f97d0dc31eb70ad521c4a4ab10a25b4fdfecfdd470a0389925181881554b(
    value: typing.Optional[CloudRunV2WorkerPoolTemplateVpcAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2734503fcd55d6af60c6e96591b03b3f209e5e6aceb02912faa2112bbab0efe7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78f33ece278feb38a265b8f6d00c25a0abcbf468e270b13af4223b84ccb2960(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__313a7bf688f5850c8d60f60ced968ca15f80b80cb39222525dc9fd4865c8eedb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6881778b050247578eec4adb6021c95ad9615c4190a22a2e8910d6ac334d930(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f841b3234e349bef0f1980b650b64e750a7d8f90f8228a333136f2f90f1bd20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c92e6fc16d898ca5e1d0d5656829b2fff8cb31d1394aee63464e10b1a62c251(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5b692a988bad6d6f10eebf1a4cce2591a6c9d90bf9415e9bd000ae1dd1b1e0(
    value: typing.Optional[CloudRunV2WorkerPoolTerminalCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7569bbe15ed477f241952ee6b3e22ffeb574f769355ae570b61038e43299291d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4753fd9b582a5bd44ef76d1467977152ccdef31fd4ae070203999a23bf6838b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4934810c30509fe49b770c75a1f77211f348de8debed6b5580f645d62cf423f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d533aee63e1792acc0d807aa7038927f25f16ecd2129636b79904248d1e8ceb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a706e0d981225f5d6bc9a9aec8f60ec4584f3df08ddea322600667e1e0ad75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ececc392aa56721af4cc9566efb208dac996fff1b4ec4cf62f095a42b80b30d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudRunV2WorkerPoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

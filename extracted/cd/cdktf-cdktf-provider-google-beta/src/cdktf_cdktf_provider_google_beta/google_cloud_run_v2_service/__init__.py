r'''
# `google_cloud_run_v2_service`

Refer to the Terraform Registry for docs: [`google_cloud_run_v2_service`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service).
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


class GoogleCloudRunV2Service(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2Service",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service google_cloud_run_v2_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        template: typing.Union["GoogleCloudRunV2ServiceTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union["GoogleCloudRunV2ServiceBinaryAuthorization", typing.Dict[builtins.str, typing.Any]]] = None,
        build_config: typing.Optional[typing.Union["GoogleCloudRunV2ServiceBuildConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        client_version: typing.Optional[builtins.str] = None,
        custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_uri_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        iap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ingress: typing.Optional[builtins.str] = None,
        invoker_iam_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_stage: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["GoogleCloudRunV2ServiceScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTraffic", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service google_cloud_run_v2_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: The location of the cloud run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#location GoogleCloudRunV2Service#location}
        :param name: Name of the Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#template GoogleCloudRunV2Service#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources. All system annotations in v1 now have a corresponding field in v2 Service. This field follows Kubernetes annotations' namespacing, limits, and rules. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#annotations GoogleCloudRunV2Service#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#binary_authorization GoogleCloudRunV2Service#binary_authorization}
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#build_config GoogleCloudRunV2Service#build_config}
        :param client: Arbitrary identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#client GoogleCloudRunV2Service#client}
        :param client_version: Arbitrary version identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#client_version GoogleCloudRunV2Service#client_version}
        :param custom_audiences: One or more custom audiences that you want this service to support. Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests. For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#custom_audiences GoogleCloudRunV2Service#custom_audiences}
        :param default_uri_disabled: Disables public resolution of the default URI of this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#default_uri_disabled GoogleCloudRunV2Service#default_uri_disabled}
        :param deletion_protection: Whether Terraform will be prevented from destroying the service. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the service, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the service will fail. When the field is set to false, deleting the service is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#deletion_protection GoogleCloudRunV2Service#deletion_protection}
        :param description: User-provided description of the Service. This field currently has a 512-character limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#description GoogleCloudRunV2Service#description}
        :param iap_enabled: Used to enable/disable IAP for the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#iap_enabled GoogleCloudRunV2Service#iap_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#id GoogleCloudRunV2Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress: Provides the ingress settings for this Service. On output, returns the currently observed ingress settings, or INGRESS_TRAFFIC_UNSPECIFIED if no revision is active. Possible values: ["INGRESS_TRAFFIC_ALL", "INGRESS_TRAFFIC_INTERNAL_ONLY", "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#ingress GoogleCloudRunV2Service#ingress}
        :param invoker_iam_disabled: Disables IAM permission check for run.routes.invoke for callers of this service. For more information, visit https://cloud.google.com/run/docs/securing/managing-access#invoker_check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#invoker_iam_disabled GoogleCloudRunV2Service#invoker_iam_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 Service. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#labels GoogleCloudRunV2Service#labels}
        :param launch_stage: The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features. For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#launch_stage GoogleCloudRunV2Service#launch_stage}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#project GoogleCloudRunV2Service#project}.
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling GoogleCloudRunV2Service#scaling}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeouts GoogleCloudRunV2Service#timeouts}
        :param traffic: traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#traffic GoogleCloudRunV2Service#traffic}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3f94b63656d4c1b629fea2a6c5c4ba6acf26b0325b584589b994fe33db59e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleCloudRunV2ServiceConfig(
            location=location,
            name=name,
            template=template,
            annotations=annotations,
            binary_authorization=binary_authorization,
            build_config=build_config,
            client=client,
            client_version=client_version,
            custom_audiences=custom_audiences,
            default_uri_disabled=default_uri_disabled,
            deletion_protection=deletion_protection,
            description=description,
            iap_enabled=iap_enabled,
            id=id,
            ingress=ingress,
            invoker_iam_disabled=invoker_iam_disabled,
            labels=labels,
            launch_stage=launch_stage,
            project=project,
            scaling=scaling,
            timeouts=timeouts,
            traffic=traffic,
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
        '''Generates CDKTF code for importing a GoogleCloudRunV2Service resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleCloudRunV2Service to import.
        :param import_from_id: The id of the existing GoogleCloudRunV2Service that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleCloudRunV2Service to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1641a1de9b4f13ebc0bb48e8f6809beed349b2352da3afcb4dd2e76c9cd790c9)
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
        :param breakglass_justification: If present, indicates to use Breakglass using this justification. If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#breakglass_justification GoogleCloudRunV2Service#breakglass_justification}
        :param policy: The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#policy GoogleCloudRunV2Service#policy}
        :param use_default: If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#use_default GoogleCloudRunV2Service#use_default}
        '''
        value = GoogleCloudRunV2ServiceBinaryAuthorization(
            breakglass_justification=breakglass_justification,
            policy=policy,
            use_default=use_default,
        )

        return typing.cast(None, jsii.invoke(self, "putBinaryAuthorization", [value]))

    @jsii.member(jsii_name="putBuildConfig")
    def put_build_config(
        self,
        *,
        base_image: typing.Optional[builtins.str] = None,
        enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        function_target: typing.Optional[builtins.str] = None,
        image_uri: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        source_location: typing.Optional[builtins.str] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param base_image: The base image used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#base_image GoogleCloudRunV2Service#base_image}
        :param enable_automatic_updates: Sets whether the function will receive automatic base image updates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#enable_automatic_updates GoogleCloudRunV2Service#enable_automatic_updates}
        :param environment_variables: User-provided build-time environment variables for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#environment_variables GoogleCloudRunV2Service#environment_variables}
        :param function_target: The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#function_target GoogleCloudRunV2Service#function_target}
        :param image_uri: Artifact Registry URI to store the built image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#image_uri GoogleCloudRunV2Service#image_uri}
        :param service_account: Service account to be used for building the container. The format of this field is 'projects/{projectId}/serviceAccounts/{serviceAccountEmail}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_account GoogleCloudRunV2Service#service_account}
        :param source_location: The Cloud Storage bucket URI where the function source code is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#source_location GoogleCloudRunV2Service#source_location}
        :param worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the Cloud Run function. The format of this field is 'projects/{project}/locations/{region}/workerPools/{workerPool}' where {project} and {region} are the project id and region respectively where the worker pool is defined and {workerPool} is the short name of the worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#worker_pool GoogleCloudRunV2Service#worker_pool}
        '''
        value = GoogleCloudRunV2ServiceBuildConfig(
            base_image=base_image,
            enable_automatic_updates=enable_automatic_updates,
            environment_variables=environment_variables,
            function_target=function_target,
            image_uri=image_uri,
            service_account=service_account,
            source_location=source_location,
            worker_pool=worker_pool,
        )

        return typing.cast(None, jsii.invoke(self, "putBuildConfig", [value]))

    @jsii.member(jsii_name="putScaling")
    def put_scaling(
        self,
        *,
        manual_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manual_instance_count: Total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#manual_instance_count GoogleCloudRunV2Service#manual_instance_count}
        :param min_instance_count: Minimum number of instances for the service, to be divided among all revisions receiving traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#min_instance_count GoogleCloudRunV2Service#min_instance_count}
        :param scaling_mode: The `scaling mode <https://cloud.google.com/run/docs/reference/rest/v2/projects.locations.services#scalingmode>`_ for the service. Possible values: ["AUTOMATIC", "MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling_mode GoogleCloudRunV2Service#scaling_mode}
        '''
        value = GoogleCloudRunV2ServiceScaling(
            manual_instance_count=manual_instance_count,
            min_instance_count=min_instance_count,
            scaling_mode=scaling_mode,
        )

        return typing.cast(None, jsii.invoke(self, "putScaling", [value]))

    @jsii.member(jsii_name="putTemplate")
    def put_template(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        execution_environment: typing.Optional[builtins.str] = None,
        gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
        node_selector: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateNodeSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        revision: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_mesh: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateServiceMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_access: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system annotations in v1 now have a corresponding field in v2 RevisionTemplate. This field follows Kubernetes annotations' namespacing, limits, and rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#annotations GoogleCloudRunV2Service#annotations}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#containers GoogleCloudRunV2Service#containers}
        :param encryption_key: A reference to a customer managed encryption key (CMEK) to use to encrypt this container image. For more information, go to https://cloud.google.com/run/docs/securing/using-cmek Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#encryption_key GoogleCloudRunV2Service#encryption_key}
        :param execution_environment: The sandbox environment to host this Revision. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#execution_environment GoogleCloudRunV2Service#execution_environment}
        :param gpu_zonal_redundancy_disabled: True if GPU zonal redundancy is disabled on this revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#gpu_zonal_redundancy_disabled GoogleCloudRunV2Service#gpu_zonal_redundancy_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 RevisionTemplate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#labels GoogleCloudRunV2Service#labels}
        :param max_instance_request_concurrency: Sets the maximum number of requests that each serving instance can receive. If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#max_instance_request_concurrency GoogleCloudRunV2Service#max_instance_request_concurrency}
        :param node_selector: node_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#node_selector GoogleCloudRunV2Service#node_selector}
        :param revision: The unique name for the revision. If this field is omitted, it will be automatically generated based on the Service name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#revision GoogleCloudRunV2Service#revision}
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling GoogleCloudRunV2Service#scaling}
        :param service_account: Email address of the IAM service account associated with the revision of the service. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_account GoogleCloudRunV2Service#service_account}
        :param service_mesh: service_mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_mesh GoogleCloudRunV2Service#service_mesh}
        :param session_affinity: Enables session affinity. For more information, go to https://cloud.google.com/run/docs/configuring/session-affinity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#session_affinity GoogleCloudRunV2Service#session_affinity}
        :param timeout: Max allowed time for an instance to respond to a request. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout GoogleCloudRunV2Service#timeout}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#volumes GoogleCloudRunV2Service#volumes}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#vpc_access GoogleCloudRunV2Service#vpc_access}
        '''
        value = GoogleCloudRunV2ServiceTemplate(
            annotations=annotations,
            containers=containers,
            encryption_key=encryption_key,
            execution_environment=execution_environment,
            gpu_zonal_redundancy_disabled=gpu_zonal_redundancy_disabled,
            labels=labels,
            max_instance_request_concurrency=max_instance_request_concurrency,
            node_selector=node_selector,
            revision=revision,
            scaling=scaling,
            service_account=service_account,
            service_mesh=service_mesh,
            session_affinity=session_affinity,
            timeout=timeout,
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#create GoogleCloudRunV2Service#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#delete GoogleCloudRunV2Service#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#update GoogleCloudRunV2Service#update}.
        '''
        value = GoogleCloudRunV2ServiceTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTraffic")
    def put_traffic(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTraffic", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df50b46406afc889a4c6965cd49c52ffb107bd2e5be3b2e05894c6e72b698e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTraffic", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetBinaryAuthorization")
    def reset_binary_authorization(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBinaryAuthorization", []))

    @jsii.member(jsii_name="resetBuildConfig")
    def reset_build_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildConfig", []))

    @jsii.member(jsii_name="resetClient")
    def reset_client(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClient", []))

    @jsii.member(jsii_name="resetClientVersion")
    def reset_client_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientVersion", []))

    @jsii.member(jsii_name="resetCustomAudiences")
    def reset_custom_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomAudiences", []))

    @jsii.member(jsii_name="resetDefaultUriDisabled")
    def reset_default_uri_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultUriDisabled", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetIapEnabled")
    def reset_iap_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIapEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIngress")
    def reset_ingress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIngress", []))

    @jsii.member(jsii_name="resetInvokerIamDisabled")
    def reset_invoker_iam_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvokerIamDisabled", []))

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

    @jsii.member(jsii_name="resetTraffic")
    def reset_traffic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTraffic", []))

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
    ) -> "GoogleCloudRunV2ServiceBinaryAuthorizationOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceBinaryAuthorizationOutputReference", jsii.get(self, "binaryAuthorization"))

    @builtins.property
    @jsii.member(jsii_name="buildConfig")
    def build_config(self) -> "GoogleCloudRunV2ServiceBuildConfigOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceBuildConfigOutputReference", jsii.get(self, "buildConfig"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "GoogleCloudRunV2ServiceConditionsList":
        return typing.cast("GoogleCloudRunV2ServiceConditionsList", jsii.get(self, "conditions"))

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
    def scaling(self) -> "GoogleCloudRunV2ServiceScalingOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceScalingOutputReference", jsii.get(self, "scaling"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> "GoogleCloudRunV2ServiceTemplateOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateOutputReference", jsii.get(self, "template"))

    @builtins.property
    @jsii.member(jsii_name="terminalCondition")
    def terminal_condition(self) -> "GoogleCloudRunV2ServiceTerminalConditionList":
        return typing.cast("GoogleCloudRunV2ServiceTerminalConditionList", jsii.get(self, "terminalCondition"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleCloudRunV2ServiceTimeoutsOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="traffic")
    def traffic(self) -> "GoogleCloudRunV2ServiceTrafficList":
        return typing.cast("GoogleCloudRunV2ServiceTrafficList", jsii.get(self, "traffic"))

    @builtins.property
    @jsii.member(jsii_name="trafficStatuses")
    def traffic_statuses(self) -> "GoogleCloudRunV2ServiceTrafficStatusesList":
        return typing.cast("GoogleCloudRunV2ServiceTrafficStatusesList", jsii.get(self, "trafficStatuses"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urls"))

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
    ) -> typing.Optional["GoogleCloudRunV2ServiceBinaryAuthorization"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceBinaryAuthorization"], jsii.get(self, "binaryAuthorizationInput"))

    @builtins.property
    @jsii.member(jsii_name="buildConfigInput")
    def build_config_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceBuildConfig"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceBuildConfig"], jsii.get(self, "buildConfigInput"))

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
    @jsii.member(jsii_name="defaultUriDisabledInput")
    def default_uri_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultUriDisabledInput"))

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
    @jsii.member(jsii_name="iapEnabledInput")
    def iap_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "iapEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ingressInput")
    def ingress_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ingressInput"))

    @builtins.property
    @jsii.member(jsii_name="invokerIamDisabledInput")
    def invoker_iam_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invokerIamDisabledInput"))

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
    def scaling_input(self) -> typing.Optional["GoogleCloudRunV2ServiceScaling"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceScaling"], jsii.get(self, "scalingInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional["GoogleCloudRunV2ServiceTemplate"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplate"], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudRunV2ServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleCloudRunV2ServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficInput")
    def traffic_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTraffic"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTraffic"]]], jsii.get(self, "trafficInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd68dfcf7915c4b4b1ecfe51bb22d3305b46f8a304aeab203212c3d99afce31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="client")
    def client(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "client"))

    @client.setter
    def client(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5a71e0072df047656fdf667d3606d1e18c5e80412e0e168a1333322b70eedb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "client", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientVersion")
    def client_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientVersion"))

    @client_version.setter
    def client_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f614ab3d5145d8f2e2e71c5e1adce367dd72fd64d82cc82c3427c06ee39f7669)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customAudiences")
    def custom_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customAudiences"))

    @custom_audiences.setter
    def custom_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d4085c8e5763017ca36e3341a4a483d91c045d2ad43a2d026a7d6a29b645e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultUriDisabled")
    def default_uri_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultUriDisabled"))

    @default_uri_disabled.setter
    def default_uri_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3051e3ea5223aded6e4324e8fa04b02d82c1fc03d2e5bae2b689b2194f1d3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultUriDisabled", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__f174c6db38a1823941800c0b7656a5aacc852c1860e7251f5ccb8e74ce8d0d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020b719a3aa31afbdf3cbd1e8e4803cb441c4f95bde5d5594f0bd5e531793c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iapEnabled")
    def iap_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "iapEnabled"))

    @iap_enabled.setter
    def iap_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae2ab9e9f4df240bcd887da88d013482184c0623a1d4d375a981db7dce5d167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iapEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c454104d79a7e2f8c5bbfbe86f12ff2d9af7e9785a315a7a5d8c7326472073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ingress")
    def ingress(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ingress"))

    @ingress.setter
    def ingress(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d899dc672b624c6bb7a9cae547cf5332bfb9e7bdb22850efdbd826fa1686cf0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invokerIamDisabled")
    def invoker_iam_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invokerIamDisabled"))

    @invoker_iam_disabled.setter
    def invoker_iam_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d498d2621ab9a16ba3b8dec4230df07a4b0f53e1aefcaa66c2105296643fb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invokerIamDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a0e1631217d5b77ccd2cf8862598fc9c3606c426a602067f22ebb053ee536d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="launchStage")
    def launch_stage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "launchStage"))

    @launch_stage.setter
    def launch_stage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60194e64e91030b0de7bc09e9b946fa7d0ca5596b269cdce7dd3119bfb4ba43d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchStage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83646107c613ffdc69d303fef4624716c1cd69f5226d809bfa3b0d66284bd3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91cdd09c7b40cab478b04fb072e2f30542a689c36ef9f95677d79c432426a69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba234e5b7954faffd73830483c055a6c67051940d7f0a789e8aa5812a8cf52a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceBinaryAuthorization",
    jsii_struct_bases=[],
    name_mapping={
        "breakglass_justification": "breakglassJustification",
        "policy": "policy",
        "use_default": "useDefault",
    },
)
class GoogleCloudRunV2ServiceBinaryAuthorization:
    def __init__(
        self,
        *,
        breakglass_justification: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param breakglass_justification: If present, indicates to use Breakglass using this justification. If useDefault is False, then it must be empty. For more information on breakglass, see https://cloud.google.com/binary-authorization/docs/using-breakglass Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#breakglass_justification GoogleCloudRunV2Service#breakglass_justification}
        :param policy: The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#policy GoogleCloudRunV2Service#policy}
        :param use_default: If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#use_default GoogleCloudRunV2Service#use_default}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9ee5eeefd2186f348b8da7e4bf265e96778ac3b4c7399bdd536fbfc5a271c04)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#breakglass_justification GoogleCloudRunV2Service#breakglass_justification}
        '''
        result = self._values.get("breakglass_justification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''The path to a binary authorization policy. Format: projects/{project}/platforms/cloudRun/{policy-name}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#policy GoogleCloudRunV2Service#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If True, indicates to use the default project's binary authorization policy. If False, binary authorization will be disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#use_default GoogleCloudRunV2Service#use_default}
        '''
        result = self._values.get("use_default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceBinaryAuthorization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceBinaryAuthorizationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceBinaryAuthorizationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10dbe204ff68209651cc722084d90169386dd379bbdad9e295fa4902e9d96daf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efbd169a61ed79ec013738cf5147d97ca8269193778a45eab1ed38ebd0e53e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "breakglassJustification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d5ddb4c6f3b0e5dbdffe95050c3842cd6e14cf54277c13fa59dd3732871a11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__efbd9f522b9349f77e093c590d7fd15ef315491d0f1d9181df92178e1c5ddeb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDefault", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceBinaryAuthorization]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceBinaryAuthorization], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceBinaryAuthorization],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dadbf393b6b6fc977e043a73298ac5caefd3f17b484a8c3176e4c675321cd4d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceBuildConfig",
    jsii_struct_bases=[],
    name_mapping={
        "base_image": "baseImage",
        "enable_automatic_updates": "enableAutomaticUpdates",
        "environment_variables": "environmentVariables",
        "function_target": "functionTarget",
        "image_uri": "imageUri",
        "service_account": "serviceAccount",
        "source_location": "sourceLocation",
        "worker_pool": "workerPool",
    },
)
class GoogleCloudRunV2ServiceBuildConfig:
    def __init__(
        self,
        *,
        base_image: typing.Optional[builtins.str] = None,
        enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        function_target: typing.Optional[builtins.str] = None,
        image_uri: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        source_location: typing.Optional[builtins.str] = None,
        worker_pool: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param base_image: The base image used to build the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#base_image GoogleCloudRunV2Service#base_image}
        :param enable_automatic_updates: Sets whether the function will receive automatic base image updates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#enable_automatic_updates GoogleCloudRunV2Service#enable_automatic_updates}
        :param environment_variables: User-provided build-time environment variables for the function. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#environment_variables GoogleCloudRunV2Service#environment_variables}
        :param function_target: The name of the function (as defined in source code) that will be executed. Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#function_target GoogleCloudRunV2Service#function_target}
        :param image_uri: Artifact Registry URI to store the built image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#image_uri GoogleCloudRunV2Service#image_uri}
        :param service_account: Service account to be used for building the container. The format of this field is 'projects/{projectId}/serviceAccounts/{serviceAccountEmail}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_account GoogleCloudRunV2Service#service_account}
        :param source_location: The Cloud Storage bucket URI where the function source code is located. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#source_location GoogleCloudRunV2Service#source_location}
        :param worker_pool: Name of the Cloud Build Custom Worker Pool that should be used to build the Cloud Run function. The format of this field is 'projects/{project}/locations/{region}/workerPools/{workerPool}' where {project} and {region} are the project id and region respectively where the worker pool is defined and {workerPool} is the short name of the worker pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#worker_pool GoogleCloudRunV2Service#worker_pool}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38755c466d623b4a096822fb9a1eb9a0f6ed56c5a21468a9477683ec238f6eb8)
            check_type(argname="argument base_image", value=base_image, expected_type=type_hints["base_image"])
            check_type(argname="argument enable_automatic_updates", value=enable_automatic_updates, expected_type=type_hints["enable_automatic_updates"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument function_target", value=function_target, expected_type=type_hints["function_target"])
            check_type(argname="argument image_uri", value=image_uri, expected_type=type_hints["image_uri"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument source_location", value=source_location, expected_type=type_hints["source_location"])
            check_type(argname="argument worker_pool", value=worker_pool, expected_type=type_hints["worker_pool"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if base_image is not None:
            self._values["base_image"] = base_image
        if enable_automatic_updates is not None:
            self._values["enable_automatic_updates"] = enable_automatic_updates
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if function_target is not None:
            self._values["function_target"] = function_target
        if image_uri is not None:
            self._values["image_uri"] = image_uri
        if service_account is not None:
            self._values["service_account"] = service_account
        if source_location is not None:
            self._values["source_location"] = source_location
        if worker_pool is not None:
            self._values["worker_pool"] = worker_pool

    @builtins.property
    def base_image(self) -> typing.Optional[builtins.str]:
        '''The base image used to build the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#base_image GoogleCloudRunV2Service#base_image}
        '''
        result = self._values.get("base_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_automatic_updates(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Sets whether the function will receive automatic base image updates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#enable_automatic_updates GoogleCloudRunV2Service#enable_automatic_updates}
        '''
        result = self._values.get("enable_automatic_updates")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''User-provided build-time environment variables for the function.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#environment_variables GoogleCloudRunV2Service#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def function_target(self) -> typing.Optional[builtins.str]:
        '''The name of the function (as defined in source code) that will be executed.

        Defaults to the resource name suffix, if not specified. For backward compatibility, if function with given name is not found, then the system will try to use function named "function".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#function_target GoogleCloudRunV2Service#function_target}
        '''
        result = self._values.get("function_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_uri(self) -> typing.Optional[builtins.str]:
        '''Artifact Registry URI to store the built image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#image_uri GoogleCloudRunV2Service#image_uri}
        '''
        result = self._values.get("image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Service account to be used for building the container. The format of this field is 'projects/{projectId}/serviceAccounts/{serviceAccountEmail}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_account GoogleCloudRunV2Service#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_location(self) -> typing.Optional[builtins.str]:
        '''The Cloud Storage bucket URI where the function source code is located.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#source_location GoogleCloudRunV2Service#source_location}
        '''
        result = self._values.get("source_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def worker_pool(self) -> typing.Optional[builtins.str]:
        '''Name of the Cloud Build Custom Worker Pool that should be used to build the Cloud Run function.

        The format of this field is 'projects/{project}/locations/{region}/workerPools/{workerPool}' where {project} and {region} are the project id and region respectively where the worker pool is defined and {workerPool} is the short name of the worker pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#worker_pool GoogleCloudRunV2Service#worker_pool}
        '''
        result = self._values.get("worker_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceBuildConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceBuildConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceBuildConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0586a1f6e51da94ff218d55dc3cf4eaa0644d473684e3e59cafe970687ffcc8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBaseImage")
    def reset_base_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseImage", []))

    @jsii.member(jsii_name="resetEnableAutomaticUpdates")
    def reset_enable_automatic_updates(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAutomaticUpdates", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetFunctionTarget")
    def reset_function_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionTarget", []))

    @jsii.member(jsii_name="resetImageUri")
    def reset_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageUri", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetSourceLocation")
    def reset_source_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceLocation", []))

    @jsii.member(jsii_name="resetWorkerPool")
    def reset_worker_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerPool", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="baseImageInput")
    def base_image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseImageInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticUpdatesInput")
    def enable_automatic_updates_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAutomaticUpdatesInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariablesInput")
    def environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="functionTargetInput")
    def function_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="imageUriInput")
    def image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageUriInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceLocationInput")
    def source_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="workerPoolInput")
    def worker_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workerPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="baseImage")
    def base_image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseImage"))

    @base_image.setter
    def base_image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74a9961d0c122ff5abe2181616581476ea20b2541fea9852d6ecc13aa63945e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseImage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAutomaticUpdates")
    def enable_automatic_updates(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAutomaticUpdates"))

    @enable_automatic_updates.setter
    def enable_automatic_updates(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85ab1978267c1011dc601b7db27f14c257022cac7844f9bc801d62be105d8e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutomaticUpdates", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c1b83a64e38332163f2edc8c76cc2094f4e95982d60560c26864f71a3edf2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionTarget")
    def function_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionTarget"))

    @function_target.setter
    def function_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c295ed5924b0291ccdb678068b0ae5419683544578bfe5ea651abef7e7676b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionTarget", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16957a9b191d72002a55a8910ad73a49b91492ca42bdfe6d6a7d6f89b52998cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead10a242ecd667f4fda1330d33fef307468b5b76dbc3cfb0810f115bdb263e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceLocation")
    def source_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceLocation"))

    @source_location.setter
    def source_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644c62210d82a9105a946d1ea0d76567dbd2fcb67fa98d952e97ee5bbd8a9309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerPool")
    def worker_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workerPool"))

    @worker_pool.setter
    def worker_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4c18b8241937db7f80497225ed8a2f8d1ccda50464ce6a8fa40e7ec97f86b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerPool", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunV2ServiceBuildConfig]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceBuildConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceBuildConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa6629b69aa165b43204dec7a7a9206a9a3129bb01946167c589e05b76b0a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudRunV2ServiceConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e3ef785fba42b4000fce1388db0d17f005a94a55101b4af0f08648f63a00977)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea541c7ce54c296dd60072af08b0737558a24a312d2a4c2a40623b4d31de9b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b504cfd9ded8696b97b39a219b1146587c904291d864fa1b74cf91a90c41e19e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6fd7ce7e86301b0ad7ec0a4d2d174313b1af4409091f38f9144794b343273cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c309859202d0f152fda825d0f22dc633ab418599677aa9bc3eb99efcea60cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a2b87b51e563b692d36945af4877314b659a4324629f562ffbbe9055e208905)
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
    def internal_value(self) -> typing.Optional[GoogleCloudRunV2ServiceConditions]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b497e9961d0d735dffd2e070dbc4dccba637f0187b2524beb76d979b7957ffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceConfig",
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
        "build_config": "buildConfig",
        "client": "client",
        "client_version": "clientVersion",
        "custom_audiences": "customAudiences",
        "default_uri_disabled": "defaultUriDisabled",
        "deletion_protection": "deletionProtection",
        "description": "description",
        "iap_enabled": "iapEnabled",
        "id": "id",
        "ingress": "ingress",
        "invoker_iam_disabled": "invokerIamDisabled",
        "labels": "labels",
        "launch_stage": "launchStage",
        "project": "project",
        "scaling": "scaling",
        "timeouts": "timeouts",
        "traffic": "traffic",
    },
)
class GoogleCloudRunV2ServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        template: typing.Union["GoogleCloudRunV2ServiceTemplate", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        binary_authorization: typing.Optional[typing.Union[GoogleCloudRunV2ServiceBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
        build_config: typing.Optional[typing.Union[GoogleCloudRunV2ServiceBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        client: typing.Optional[builtins.str] = None,
        client_version: typing.Optional[builtins.str] = None,
        custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_uri_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        iap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        ingress: typing.Optional[builtins.str] = None,
        invoker_iam_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        launch_stage: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["GoogleCloudRunV2ServiceScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTraffic", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: The location of the cloud run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#location GoogleCloudRunV2Service#location}
        :param name: Name of the Service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        :param template: template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#template GoogleCloudRunV2Service#template}
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources. All system annotations in v1 now have a corresponding field in v2 Service. This field follows Kubernetes annotations' namespacing, limits, and rules. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#annotations GoogleCloudRunV2Service#annotations}
        :param binary_authorization: binary_authorization block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#binary_authorization GoogleCloudRunV2Service#binary_authorization}
        :param build_config: build_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#build_config GoogleCloudRunV2Service#build_config}
        :param client: Arbitrary identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#client GoogleCloudRunV2Service#client}
        :param client_version: Arbitrary version identifier for the API client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#client_version GoogleCloudRunV2Service#client_version}
        :param custom_audiences: One or more custom audiences that you want this service to support. Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests. For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#custom_audiences GoogleCloudRunV2Service#custom_audiences}
        :param default_uri_disabled: Disables public resolution of the default URI of this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#default_uri_disabled GoogleCloudRunV2Service#default_uri_disabled}
        :param deletion_protection: Whether Terraform will be prevented from destroying the service. Defaults to true. When a'terraform destroy' or 'terraform apply' would delete the service, the command will fail if this field is not set to false in Terraform state. When the field is set to true or unset in Terraform state, a 'terraform apply' or 'terraform destroy' that would delete the service will fail. When the field is set to false, deleting the service is allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#deletion_protection GoogleCloudRunV2Service#deletion_protection}
        :param description: User-provided description of the Service. This field currently has a 512-character limit. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#description GoogleCloudRunV2Service#description}
        :param iap_enabled: Used to enable/disable IAP for the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#iap_enabled GoogleCloudRunV2Service#iap_enabled}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#id GoogleCloudRunV2Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ingress: Provides the ingress settings for this Service. On output, returns the currently observed ingress settings, or INGRESS_TRAFFIC_UNSPECIFIED if no revision is active. Possible values: ["INGRESS_TRAFFIC_ALL", "INGRESS_TRAFFIC_INTERNAL_ONLY", "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#ingress GoogleCloudRunV2Service#ingress}
        :param invoker_iam_disabled: Disables IAM permission check for run.routes.invoke for callers of this service. For more information, visit https://cloud.google.com/run/docs/securing/managing-access#invoker_check. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#invoker_iam_disabled GoogleCloudRunV2Service#invoker_iam_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 Service. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#labels GoogleCloudRunV2Service#labels}
        :param launch_stage: The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features. For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#launch_stage GoogleCloudRunV2Service#launch_stage}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#project GoogleCloudRunV2Service#project}.
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling GoogleCloudRunV2Service#scaling}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeouts GoogleCloudRunV2Service#timeouts}
        :param traffic: traffic block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#traffic GoogleCloudRunV2Service#traffic}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(template, dict):
            template = GoogleCloudRunV2ServiceTemplate(**template)
        if isinstance(binary_authorization, dict):
            binary_authorization = GoogleCloudRunV2ServiceBinaryAuthorization(**binary_authorization)
        if isinstance(build_config, dict):
            build_config = GoogleCloudRunV2ServiceBuildConfig(**build_config)
        if isinstance(scaling, dict):
            scaling = GoogleCloudRunV2ServiceScaling(**scaling)
        if isinstance(timeouts, dict):
            timeouts = GoogleCloudRunV2ServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec22f99db982f16e6413ec5ff0ae621810b21b17f2a8220d37334b4f16c1bf78)
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
            check_type(argname="argument build_config", value=build_config, expected_type=type_hints["build_config"])
            check_type(argname="argument client", value=client, expected_type=type_hints["client"])
            check_type(argname="argument client_version", value=client_version, expected_type=type_hints["client_version"])
            check_type(argname="argument custom_audiences", value=custom_audiences, expected_type=type_hints["custom_audiences"])
            check_type(argname="argument default_uri_disabled", value=default_uri_disabled, expected_type=type_hints["default_uri_disabled"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument iap_enabled", value=iap_enabled, expected_type=type_hints["iap_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ingress", value=ingress, expected_type=type_hints["ingress"])
            check_type(argname="argument invoker_iam_disabled", value=invoker_iam_disabled, expected_type=type_hints["invoker_iam_disabled"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument launch_stage", value=launch_stage, expected_type=type_hints["launch_stage"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument traffic", value=traffic, expected_type=type_hints["traffic"])
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
        if build_config is not None:
            self._values["build_config"] = build_config
        if client is not None:
            self._values["client"] = client
        if client_version is not None:
            self._values["client_version"] = client_version
        if custom_audiences is not None:
            self._values["custom_audiences"] = custom_audiences
        if default_uri_disabled is not None:
            self._values["default_uri_disabled"] = default_uri_disabled
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if iap_enabled is not None:
            self._values["iap_enabled"] = iap_enabled
        if id is not None:
            self._values["id"] = id
        if ingress is not None:
            self._values["ingress"] = ingress
        if invoker_iam_disabled is not None:
            self._values["invoker_iam_disabled"] = invoker_iam_disabled
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
        if traffic is not None:
            self._values["traffic"] = traffic

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
        '''The location of the cloud run service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#location GoogleCloudRunV2Service#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the Service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template(self) -> "GoogleCloudRunV2ServiceTemplate":
        '''template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#template GoogleCloudRunV2Service#template}
        '''
        result = self._values.get("template")
        assert result is not None, "Required property 'template' is missing"
        return typing.cast("GoogleCloudRunV2ServiceTemplate", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that may be set by external tools to store and arbitrary metadata.

        They are not queryable and should be preserved when modifying objects.

        Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected in new resources.
        All system annotations in v1 now have a corresponding field in v2 Service.

        This field follows Kubernetes annotations' namespacing, limits, and rules.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#annotations GoogleCloudRunV2Service#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def binary_authorization(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceBinaryAuthorization]:
        '''binary_authorization block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#binary_authorization GoogleCloudRunV2Service#binary_authorization}
        '''
        result = self._values.get("binary_authorization")
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceBinaryAuthorization], result)

    @builtins.property
    def build_config(self) -> typing.Optional[GoogleCloudRunV2ServiceBuildConfig]:
        '''build_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#build_config GoogleCloudRunV2Service#build_config}
        '''
        result = self._values.get("build_config")
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceBuildConfig], result)

    @builtins.property
    def client(self) -> typing.Optional[builtins.str]:
        '''Arbitrary identifier for the API client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#client GoogleCloudRunV2Service#client}
        '''
        result = self._values.get("client")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_version(self) -> typing.Optional[builtins.str]:
        '''Arbitrary version identifier for the API client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#client_version GoogleCloudRunV2Service#client_version}
        '''
        result = self._values.get("client_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''One or more custom audiences that you want this service to support.

        Specify each custom audience as the full URL in a string. The custom audiences are encoded in the token and used to authenticate requests.
        For more information, see https://cloud.google.com/run/docs/configuring/custom-audiences.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#custom_audiences GoogleCloudRunV2Service#custom_audiences}
        '''
        result = self._values.get("custom_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_uri_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables public resolution of the default URI of this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#default_uri_disabled GoogleCloudRunV2Service#default_uri_disabled}
        '''
        result = self._values.get("default_uri_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Terraform will be prevented from destroying the service.

        Defaults to true.
        When a'terraform destroy' or 'terraform apply' would delete the service,
        the command will fail if this field is not set to false in Terraform state.
        When the field is set to true or unset in Terraform state, a 'terraform apply'
        or 'terraform destroy' that would delete the service will fail.
        When the field is set to false, deleting the service is allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#deletion_protection GoogleCloudRunV2Service#deletion_protection}
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-provided description of the Service. This field currently has a 512-character limit.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#description GoogleCloudRunV2Service#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def iap_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Used to enable/disable IAP for the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#iap_enabled GoogleCloudRunV2Service#iap_enabled}
        '''
        result = self._values.get("iap_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#id GoogleCloudRunV2Service#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingress(self) -> typing.Optional[builtins.str]:
        '''Provides the ingress settings for this Service.

        On output, returns the currently observed ingress settings, or INGRESS_TRAFFIC_UNSPECIFIED if no revision is active. Possible values: ["INGRESS_TRAFFIC_ALL", "INGRESS_TRAFFIC_INTERNAL_ONLY", "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#ingress GoogleCloudRunV2Service#ingress}
        '''
        result = self._values.get("ingress")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invoker_iam_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables IAM permission check for run.routes.invoke for callers of this service. For more information, visit https://cloud.google.com/run/docs/securing/managing-access#invoker_check.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#invoker_iam_disabled GoogleCloudRunV2Service#invoker_iam_disabled}
        '''
        result = self._values.get("invoker_iam_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that can be used to organize and categorize objects.

        User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component,
        environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels.

        Cloud Run API v2 does not support labels with  'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system labels in v1 now have a corresponding field in v2 Service.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#labels GoogleCloudRunV2Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def launch_stage(self) -> typing.Optional[builtins.str]:
        '''The launch stage as defined by `Google Cloud Platform Launch Stages <https://cloud.google.com/products#product-launch-stages>`_. Cloud Run supports ALPHA, BETA, and GA. If no value is specified, GA is assumed. Set the launch stage to a preview stage on input to allow use of preview features in that stage. On read (or output), describes whether the resource uses preview features.

        For example, if ALPHA is provided as input, but only BETA and GA-level features are used, this field will be BETA on output. Possible values: ["UNIMPLEMENTED", "PRELAUNCH", "EARLY_ACCESS", "ALPHA", "BETA", "GA", "DEPRECATED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#launch_stage GoogleCloudRunV2Service#launch_stage}
        '''
        result = self._values.get("launch_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#project GoogleCloudRunV2Service#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling(self) -> typing.Optional["GoogleCloudRunV2ServiceScaling"]:
        '''scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling GoogleCloudRunV2Service#scaling}
        '''
        result = self._values.get("scaling")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceScaling"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleCloudRunV2ServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeouts GoogleCloudRunV2Service#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTimeouts"], result)

    @builtins.property
    def traffic(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTraffic"]]]:
        '''traffic block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#traffic GoogleCloudRunV2Service#traffic}
        '''
        result = self._values.get("traffic")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTraffic"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceScaling",
    jsii_struct_bases=[],
    name_mapping={
        "manual_instance_count": "manualInstanceCount",
        "min_instance_count": "minInstanceCount",
        "scaling_mode": "scalingMode",
    },
)
class GoogleCloudRunV2ServiceScaling:
    def __init__(
        self,
        *,
        manual_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param manual_instance_count: Total instance count for the service in manual scaling mode. This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#manual_instance_count GoogleCloudRunV2Service#manual_instance_count}
        :param min_instance_count: Minimum number of instances for the service, to be divided among all revisions receiving traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#min_instance_count GoogleCloudRunV2Service#min_instance_count}
        :param scaling_mode: The `scaling mode <https://cloud.google.com/run/docs/reference/rest/v2/projects.locations.services#scalingmode>`_ for the service. Possible values: ["AUTOMATIC", "MANUAL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling_mode GoogleCloudRunV2Service#scaling_mode}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085dfdb45f7f09b3169b6952d35bad2421a5979cf2ded6b21c6869bd4be2e79f)
            check_type(argname="argument manual_instance_count", value=manual_instance_count, expected_type=type_hints["manual_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            check_type(argname="argument scaling_mode", value=scaling_mode, expected_type=type_hints["scaling_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if manual_instance_count is not None:
            self._values["manual_instance_count"] = manual_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count
        if scaling_mode is not None:
            self._values["scaling_mode"] = scaling_mode

    @builtins.property
    def manual_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Total instance count for the service in manual scaling mode.

        This number of instances is divided among all revisions with specified traffic based on the percent of traffic they are receiving.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#manual_instance_count GoogleCloudRunV2Service#manual_instance_count}
        '''
        result = self._values.get("manual_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of instances for the service, to be divided among all revisions receiving traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#min_instance_count GoogleCloudRunV2Service#min_instance_count}
        '''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scaling_mode(self) -> typing.Optional[builtins.str]:
        '''The `scaling mode <https://cloud.google.com/run/docs/reference/rest/v2/projects.locations.services#scalingmode>`_ for the service. Possible values: ["AUTOMATIC", "MANUAL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling_mode GoogleCloudRunV2Service#scaling_mode}
        '''
        result = self._values.get("scaling_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__719fba8de1beb3f671156aa22eae591f81fed1f90d4bb27007a8221b7c76dfb3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetManualInstanceCount")
    def reset_manual_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManualInstanceCount", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b7ae5c616868732d44ffe62ccc55b64ce7919a8c531a6959828a439b9edd1620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "manualInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532adff6ee96c1994159a5f18983b0d4656941957dacda45b9660ce582cb1cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scalingMode")
    def scaling_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scalingMode"))

    @scaling_mode.setter
    def scaling_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb6e4442c3d353d244ca1e6b2deae608a3dd46a46a7062334677f38f548ea1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunV2ServiceScaling]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e676532ba80a1ea091c797d3132d45f8ebcd0637b7bfc1beae7c7645461c3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "containers": "containers",
        "encryption_key": "encryptionKey",
        "execution_environment": "executionEnvironment",
        "gpu_zonal_redundancy_disabled": "gpuZonalRedundancyDisabled",
        "labels": "labels",
        "max_instance_request_concurrency": "maxInstanceRequestConcurrency",
        "node_selector": "nodeSelector",
        "revision": "revision",
        "scaling": "scaling",
        "service_account": "serviceAccount",
        "service_mesh": "serviceMesh",
        "session_affinity": "sessionAffinity",
        "timeout": "timeout",
        "volumes": "volumes",
        "vpc_access": "vpcAccess",
    },
)
class GoogleCloudRunV2ServiceTemplate:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateContainers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        execution_environment: typing.Optional[builtins.str] = None,
        gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
        node_selector: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateNodeSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        revision: typing.Optional[builtins.str] = None,
        scaling: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        service_account: typing.Optional[builtins.str] = None,
        service_mesh: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateServiceMesh", typing.Dict[builtins.str, typing.Any]]] = None,
        session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        vpc_access: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateVpcAccess", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param annotations: Unstructured key value map that may be set by external tools to store and arbitrary metadata. They are not queryable and should be preserved when modifying objects. Cloud Run API v2 does not support annotations with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system annotations in v1 now have a corresponding field in v2 RevisionTemplate. This field follows Kubernetes annotations' namespacing, limits, and rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#annotations GoogleCloudRunV2Service#annotations}
        :param containers: containers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#containers GoogleCloudRunV2Service#containers}
        :param encryption_key: A reference to a customer managed encryption key (CMEK) to use to encrypt this container image. For more information, go to https://cloud.google.com/run/docs/securing/using-cmek Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#encryption_key GoogleCloudRunV2Service#encryption_key}
        :param execution_environment: The sandbox environment to host this Revision. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#execution_environment GoogleCloudRunV2Service#execution_environment}
        :param gpu_zonal_redundancy_disabled: True if GPU zonal redundancy is disabled on this revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#gpu_zonal_redundancy_disabled GoogleCloudRunV2Service#gpu_zonal_redundancy_disabled}
        :param labels: Unstructured key value map that can be used to organize and categorize objects. User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc. For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels. Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected. All system labels in v1 now have a corresponding field in v2 RevisionTemplate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#labels GoogleCloudRunV2Service#labels}
        :param max_instance_request_concurrency: Sets the maximum number of requests that each serving instance can receive. If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#max_instance_request_concurrency GoogleCloudRunV2Service#max_instance_request_concurrency}
        :param node_selector: node_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#node_selector GoogleCloudRunV2Service#node_selector}
        :param revision: The unique name for the revision. If this field is omitted, it will be automatically generated based on the Service name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#revision GoogleCloudRunV2Service#revision}
        :param scaling: scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling GoogleCloudRunV2Service#scaling}
        :param service_account: Email address of the IAM service account associated with the revision of the service. The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_account GoogleCloudRunV2Service#service_account}
        :param service_mesh: service_mesh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_mesh GoogleCloudRunV2Service#service_mesh}
        :param session_affinity: Enables session affinity. For more information, go to https://cloud.google.com/run/docs/configuring/session-affinity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#session_affinity GoogleCloudRunV2Service#session_affinity}
        :param timeout: Max allowed time for an instance to respond to a request. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout GoogleCloudRunV2Service#timeout}
        :param volumes: volumes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#volumes GoogleCloudRunV2Service#volumes}
        :param vpc_access: vpc_access block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#vpc_access GoogleCloudRunV2Service#vpc_access}
        '''
        if isinstance(node_selector, dict):
            node_selector = GoogleCloudRunV2ServiceTemplateNodeSelector(**node_selector)
        if isinstance(scaling, dict):
            scaling = GoogleCloudRunV2ServiceTemplateScaling(**scaling)
        if isinstance(service_mesh, dict):
            service_mesh = GoogleCloudRunV2ServiceTemplateServiceMesh(**service_mesh)
        if isinstance(vpc_access, dict):
            vpc_access = GoogleCloudRunV2ServiceTemplateVpcAccess(**vpc_access)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5633739d4db407b6ba3492871adba693e751f919329bbe3ce0af405d5da869d)
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument execution_environment", value=execution_environment, expected_type=type_hints["execution_environment"])
            check_type(argname="argument gpu_zonal_redundancy_disabled", value=gpu_zonal_redundancy_disabled, expected_type=type_hints["gpu_zonal_redundancy_disabled"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument max_instance_request_concurrency", value=max_instance_request_concurrency, expected_type=type_hints["max_instance_request_concurrency"])
            check_type(argname="argument node_selector", value=node_selector, expected_type=type_hints["node_selector"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            check_type(argname="argument scaling", value=scaling, expected_type=type_hints["scaling"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument service_mesh", value=service_mesh, expected_type=type_hints["service_mesh"])
            check_type(argname="argument session_affinity", value=session_affinity, expected_type=type_hints["session_affinity"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument vpc_access", value=vpc_access, expected_type=type_hints["vpc_access"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if containers is not None:
            self._values["containers"] = containers
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if execution_environment is not None:
            self._values["execution_environment"] = execution_environment
        if gpu_zonal_redundancy_disabled is not None:
            self._values["gpu_zonal_redundancy_disabled"] = gpu_zonal_redundancy_disabled
        if labels is not None:
            self._values["labels"] = labels
        if max_instance_request_concurrency is not None:
            self._values["max_instance_request_concurrency"] = max_instance_request_concurrency
        if node_selector is not None:
            self._values["node_selector"] = node_selector
        if revision is not None:
            self._values["revision"] = revision
        if scaling is not None:
            self._values["scaling"] = scaling
        if service_account is not None:
            self._values["service_account"] = service_account
        if service_mesh is not None:
            self._values["service_mesh"] = service_mesh
        if session_affinity is not None:
            self._values["session_affinity"] = session_affinity
        if timeout is not None:
            self._values["timeout"] = timeout
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
        All system annotations in v1 now have a corresponding field in v2 RevisionTemplate.

        This field follows Kubernetes annotations' namespacing, limits, and rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#annotations GoogleCloudRunV2Service#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def containers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainers"]]]:
        '''containers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#containers GoogleCloudRunV2Service#containers}
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainers"]]], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''A reference to a customer managed encryption key (CMEK) to use to encrypt this container image.

        For more information, go to https://cloud.google.com/run/docs/securing/using-cmek

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#encryption_key GoogleCloudRunV2Service#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_environment(self) -> typing.Optional[builtins.str]:
        '''The sandbox environment to host this Revision. Possible values: ["EXECUTION_ENVIRONMENT_GEN1", "EXECUTION_ENVIRONMENT_GEN2"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#execution_environment GoogleCloudRunV2Service#execution_environment}
        '''
        result = self._values.get("execution_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpu_zonal_redundancy_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if GPU zonal redundancy is disabled on this revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#gpu_zonal_redundancy_disabled GoogleCloudRunV2Service#gpu_zonal_redundancy_disabled}
        '''
        result = self._values.get("gpu_zonal_redundancy_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Unstructured key value map that can be used to organize and categorize objects.

        User-provided labels are shared with Google's billing system, so they can be used to filter, or break down billing charges by team, component, environment, state, etc.
        For more information, visit https://cloud.google.com/resource-manager/docs/creating-managing-labels or https://cloud.google.com/run/docs/configuring/labels.

        Cloud Run API v2 does not support labels with 'run.googleapis.com', 'cloud.googleapis.com', 'serving.knative.dev', or 'autoscaling.knative.dev' namespaces, and they will be rejected.
        All system labels in v1 now have a corresponding field in v2 RevisionTemplate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#labels GoogleCloudRunV2Service#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_instance_request_concurrency(self) -> typing.Optional[jsii.Number]:
        '''Sets the maximum number of requests that each serving instance can receive.

        If not specified or 0, defaults to 80 when requested CPU >= 1 and defaults to 1 when requested CPU < 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#max_instance_request_concurrency GoogleCloudRunV2Service#max_instance_request_concurrency}
        '''
        result = self._values.get("max_instance_request_concurrency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def node_selector(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateNodeSelector"]:
        '''node_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#node_selector GoogleCloudRunV2Service#node_selector}
        '''
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateNodeSelector"], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        '''The unique name for the revision.

        If this field is omitted, it will be automatically generated based on the Service name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#revision GoogleCloudRunV2Service#revision}
        '''
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling(self) -> typing.Optional["GoogleCloudRunV2ServiceTemplateScaling"]:
        '''scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#scaling GoogleCloudRunV2Service#scaling}
        '''
        result = self._values.get("scaling")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateScaling"], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''Email address of the IAM service account associated with the revision of the service.

        The service account represents the identity of the running revision, and determines what permissions the revision has. If not provided, the revision will use the project's default service account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_account GoogleCloudRunV2Service#service_account}
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_mesh(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateServiceMesh"]:
        '''service_mesh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service_mesh GoogleCloudRunV2Service#service_mesh}
        '''
        result = self._values.get("service_mesh")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateServiceMesh"], result)

    @builtins.property
    def session_affinity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables session affinity. For more information, go to https://cloud.google.com/run/docs/configuring/session-affinity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#session_affinity GoogleCloudRunV2Service#session_affinity}
        '''
        result = self._values.get("session_affinity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Max allowed time for an instance to respond to a request.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout GoogleCloudRunV2Service#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateVolumes"]]]:
        '''volumes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#volumes GoogleCloudRunV2Service#volumes}
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateVolumes"]]], result)

    @builtins.property
    def vpc_access(self) -> typing.Optional["GoogleCloudRunV2ServiceTemplateVpcAccess"]:
        '''vpc_access block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#vpc_access GoogleCloudRunV2Service#vpc_access}
        '''
        result = self._values.get("vpc_access")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateVpcAccess"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainers",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "base_image_uri": "baseImageUri",
        "command": "command",
        "depends_on": "dependsOn",
        "env": "env",
        "liveness_probe": "livenessProbe",
        "name": "name",
        "ports": "ports",
        "resources": "resources",
        "startup_probe": "startupProbe",
        "volume_mounts": "volumeMounts",
        "working_dir": "workingDir",
    },
)
class GoogleCloudRunV2ServiceTemplateContainers:
    def __init__(
        self,
        *,
        image: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        base_image_uri: typing.Optional[builtins.str] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateContainersEnv", typing.Dict[builtins.str, typing.Any]]]]] = None,
        liveness_probe: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersLivenessProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersPorts", typing.Dict[builtins.str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersResources", typing.Dict[builtins.str, typing.Any]]] = None,
        startup_probe: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersStartupProbe", typing.Dict[builtins.str, typing.Any]]] = None,
        volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: URL of the Container image in Google Container Registry or Google Artifact Registry. More info: https://kubernetes.io/docs/concepts/containers/images. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#image GoogleCloudRunV2Service#image}
        :param args: Arguments to the entrypoint. The docker image's CMD is used if this is not provided. Variable references are not supported in Cloud Run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#args GoogleCloudRunV2Service#args}
        :param base_image_uri: Base image for this container. If set, it indicates that the service is enrolled into automatic base image update. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#base_image_uri GoogleCloudRunV2Service#base_image_uri}
        :param command: Entrypoint array. Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#command GoogleCloudRunV2Service#command}
        :param depends_on: Containers which should be started before this container. If specified the container will wait to start until all containers with the listed names are healthy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#depends_on GoogleCloudRunV2Service#depends_on}
        :param env: env block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#env GoogleCloudRunV2Service#env}
        :param liveness_probe: liveness_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#liveness_probe GoogleCloudRunV2Service#liveness_probe}
        :param name: Name of the container specified as a DNS_LABEL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        :param ports: ports block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#ports GoogleCloudRunV2Service#ports}
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#resources GoogleCloudRunV2Service#resources}
        :param startup_probe: startup_probe block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#startup_probe GoogleCloudRunV2Service#startup_probe}
        :param volume_mounts: volume_mounts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#volume_mounts GoogleCloudRunV2Service#volume_mounts}
        :param working_dir: Container's working directory. If not specified, the container runtime's default will be used, which might be configured in the container image. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#working_dir GoogleCloudRunV2Service#working_dir}
        '''
        if isinstance(liveness_probe, dict):
            liveness_probe = GoogleCloudRunV2ServiceTemplateContainersLivenessProbe(**liveness_probe)
        if isinstance(ports, dict):
            ports = GoogleCloudRunV2ServiceTemplateContainersPorts(**ports)
        if isinstance(resources, dict):
            resources = GoogleCloudRunV2ServiceTemplateContainersResources(**resources)
        if isinstance(startup_probe, dict):
            startup_probe = GoogleCloudRunV2ServiceTemplateContainersStartupProbe(**startup_probe)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b76a72e168b6fb360869f2a2dff92a42470af5f28f60b95e50bf3ab39afca516)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument base_image_uri", value=base_image_uri, expected_type=type_hints["base_image_uri"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument liveness_probe", value=liveness_probe, expected_type=type_hints["liveness_probe"])
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
        if base_image_uri is not None:
            self._values["base_image_uri"] = base_image_uri
        if command is not None:
            self._values["command"] = command
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if env is not None:
            self._values["env"] = env
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#image GoogleCloudRunV2Service#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Arguments to the entrypoint.

        The docker image's CMD is used if this is not provided. Variable references are not supported in Cloud Run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#args GoogleCloudRunV2Service#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def base_image_uri(self) -> typing.Optional[builtins.str]:
        '''Base image for this container. If set, it indicates that the service is enrolled into automatic base image update.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#base_image_uri GoogleCloudRunV2Service#base_image_uri}
        '''
        result = self._values.get("base_image_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Entrypoint array.

        Not executed within a shell. The docker image's ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) are expanded using the container's environment. If a variable cannot be resolved, the reference in the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, regardless of whether the variable exists or not. More info: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#command GoogleCloudRunV2Service#command}
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Containers which should be started before this container.

        If specified the container will wait to start until all containers with the listed names are healthy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#depends_on GoogleCloudRunV2Service#depends_on}
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersEnv"]]]:
        '''env block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#env GoogleCloudRunV2Service#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersEnv"]]], result)

    @builtins.property
    def liveness_probe(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbe"]:
        '''liveness_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#liveness_probe GoogleCloudRunV2Service#liveness_probe}
        '''
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbe"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the container specified as a DNS_LABEL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersPorts"]:
        '''ports block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#ports GoogleCloudRunV2Service#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersPorts"], result)

    @builtins.property
    def resources(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersResources"]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#resources GoogleCloudRunV2Service#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersResources"], result)

    @builtins.property
    def startup_probe(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbe"]:
        '''startup_probe block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#startup_probe GoogleCloudRunV2Service#startup_probe}
        '''
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbe"], result)

    @builtins.property
    def volume_mounts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersVolumeMounts"]]]:
        '''volume_mounts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#volume_mounts GoogleCloudRunV2Service#volume_mounts}
        '''
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersVolumeMounts"]]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''Container's working directory.

        If not specified, the container runtime's default will be used, which might be configured in the container image.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#working_dir GoogleCloudRunV2Service#working_dir}
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersBuildInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudRunV2ServiceTemplateContainersBuildInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersBuildInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersBuildInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersBuildInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e04ef4beee98b5dda7c3e53302a6182096a7c23ca39f7cad23ed12f352efb8e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersBuildInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74a319f96ffe3c09fba7f680d528d3250fc0bac8b05c469b318040dfd7add8a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersBuildInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe33fabbe9ce44ed0b70feff7a65ff27cc19f67acfa20e4c3793f4a0c8fb477)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f58d4bc15032953b66662f39487fecf7bcbf92b1fd0f9304ba7c9283c0814d77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6247b367ee8e2a1c9685edba1bb7e48adfeb6f939e85c576d6b6f24b1313b191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersBuildInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersBuildInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f5e8efc1b32482d2306a07a318a822809a795b3144bd2f9f12ab2bebc0bcc2a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="functionTarget")
    def function_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionTarget"))

    @builtins.property
    @jsii.member(jsii_name="sourceLocation")
    def source_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceLocation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersBuildInfo]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersBuildInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersBuildInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3f838303dac58e2b91d58e9c18cdfed0e037f606723acda21097062beea17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersEnv",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "value_source": "valueSource"},
)
class GoogleCloudRunV2ServiceTemplateContainersEnv:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
        value_source: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersEnvValueSource", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Name of the environment variable. Must be a C_IDENTIFIER, and may not exceed 32768 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        :param value: Literal value of the environment variable. Defaults to "" and the maximum allowed length is 32768 characters. Variable references are not supported in Cloud Run. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#value GoogleCloudRunV2Service#value}
        :param value_source: value_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#value_source GoogleCloudRunV2Service#value_source}
        '''
        if isinstance(value_source, dict):
            value_source = GoogleCloudRunV2ServiceTemplateContainersEnvValueSource(**value_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__765037831f8c94469ce5b6176eba646fc3fb5f62c5094cdc020d3be60033240c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Literal value of the environment variable.

        Defaults to "" and the maximum allowed length is 32768 characters. Variable references are not supported in Cloud Run.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#value GoogleCloudRunV2Service#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_source(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersEnvValueSource"]:
        '''value_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#value_source GoogleCloudRunV2Service#value_source}
        '''
        result = self._values.get("value_source")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersEnvValueSource"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersEnv(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersEnvList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersEnvList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92930110d5a67b032de4a8c6ee70ab5b6f4963f859e8c0cd627daa087496cdbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersEnvOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743bc010270b72189e62e0e63b5222d9c78edaed6c84635159932c4d4c202703)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersEnvOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f878dcd07068d31579b08effc577f64678524a7115087c97ac127f30ac5137)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe0326218d09050c8fc0151c0417211653e21defec4c0824b315532ccedb9686)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d617caf40c9ab07ffcae8255522307c95d1e04ef16432532b10f36553030b371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersEnv]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersEnv]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cbdb0bfda7d512db6bbc6079d6de3ce0d5274445a4afbe81b5018efac5a1229)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersEnvOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersEnvOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a8614dbd73f260d72309dc284364edcc40c7f7849795aef05573b033597aaf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValueSource")
    def put_value_source(
        self,
        *,
        secret_key_ref: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret_key_ref GoogleCloudRunV2Service#secret_key_ref}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersEnvValueSource(
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
    ) -> "GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference", jsii.get(self, "valueSource"))

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
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersEnvValueSource"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersEnvValueSource"], jsii.get(self, "valueSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d0dac26c8e5d6484206569d49d87786aca9ecbaf7db064ba972b376a9487e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6a00ba23592da6addf905e0280182f49cdf351b056990fc758bdcc6a9b4a9ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersEnv]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersEnv]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersEnv]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730720ee8936f6dfb9f7044b5ceb499b5d220b371e7f349863a9fbb8d686a2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersEnvValueSource",
    jsii_struct_bases=[],
    name_mapping={"secret_key_ref": "secretKeyRef"},
)
class GoogleCloudRunV2ServiceTemplateContainersEnvValueSource:
    def __init__(
        self,
        *,
        secret_key_ref: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param secret_key_ref: secret_key_ref block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret_key_ref GoogleCloudRunV2Service#secret_key_ref}
        '''
        if isinstance(secret_key_ref, dict):
            secret_key_ref = GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef(**secret_key_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066e2dbfa2f343347cf085817d11f36ea386487fe58079645310c4558a0157ca)
            check_type(argname="argument secret_key_ref", value=secret_key_ref, expected_type=type_hints["secret_key_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret_key_ref is not None:
            self._values["secret_key_ref"] = secret_key_ref

    @builtins.property
    def secret_key_ref(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef"]:
        '''secret_key_ref block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret_key_ref GoogleCloudRunV2Service#secret_key_ref}
        '''
        result = self._values.get("secret_key_ref")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersEnvValueSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58a67a2b532d7841b32ea5a944975b12ff4b51c5546dd5eb70eb7ff61172245c)
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
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret GoogleCloudRunV2Service#secret}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#version GoogleCloudRunV2Service#version}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef(
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
    ) -> "GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference", jsii.get(self, "secretKeyRef"))

    @builtins.property
    @jsii.member(jsii_name="secretKeyRefInput")
    def secret_key_ref_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef"], jsii.get(self, "secretKeyRefInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersEnvValueSource]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersEnvValueSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersEnvValueSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939603c43d2f821907be56ae6c1d79ab4476560e017c560128138b22c4678c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "version": "version"},
)
class GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef:
    def __init__(
        self,
        *,
        secret: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secretName} if the secret is in the same project. projects/{project}/secrets/{secretName} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret GoogleCloudRunV2Service#secret}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#version GoogleCloudRunV2Service#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6bc0d2d1e8c59607a107d6570be76e16dc3b294c695499c0becd1c8f062711)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret GoogleCloudRunV2Service#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Cloud Secret Manager secret version.

        Can be 'latest' for the latest value or an integer for a specific version.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#version GoogleCloudRunV2Service#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c78f6d9fbe89cc3a44c754a8ffc6bda476eab9a582b86ca42e07f2646932b8d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d192dba23fa30b7f8429133185e04c125908563c94d861ef3088c15c4fe6ab5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79fca087f9a31097937d8095afc15b3925340a970ed442872ad4de5aa5d7752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cea31e0b831d58cdbe4e7148cd37dca9ce583850d2b4844adb4ad441107eb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f825a6278fc2aea3ac8226dafb54267b8b9c9606972f5aa51c94b6be1930991)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07ac81de8fec851957ea2bbacb76a76d56915fed0d0b997467d5b8089aaf20f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8e090c86956da77f94b04492bb2f4b1681deb77d50c5c1247f6b6852a529156)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd9e464b03b3f754d555f4d8798b2ca5f2bed08fc6517ab0a0b042383c759306)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54cc7a853302d999f8862992158f8704d7f02ac9dee8a420c84d34de38066030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef7eca6cee376eed0cd6157c05d31260eee68659e2dc12fd5858cbdaec63ed2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbe",
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
class GoogleCloudRunV2ServiceTemplateContainersLivenessProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#failure_threshold GoogleCloudRunV2Service#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#grpc GoogleCloudRunV2Service#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_get GoogleCloudRunV2Service#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#initial_delay_seconds GoogleCloudRunV2Service#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#period_seconds GoogleCloudRunV2Service#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tcp_socket GoogleCloudRunV2Service#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout_seconds GoogleCloudRunV2Service#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a122105687fffb31a228f477735e9131b59185fe7944c0e204acb6ef87a33b5)
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
        '''Minimum consecutive failures for the probe to be considered failed after having succeeded.

        Defaults to 3. Minimum value is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#failure_threshold GoogleCloudRunV2Service#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#grpc GoogleCloudRunV2Service#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_get GoogleCloudRunV2Service#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#initial_delay_seconds GoogleCloudRunV2Service#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#period_seconds GoogleCloudRunV2Service#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tcp_socket GoogleCloudRunV2Service#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout_seconds GoogleCloudRunV2Service#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersLivenessProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service GoogleCloudRunV2Service#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d136a6daa38a55481b05e524cddd3f094cb45a2d7b524eecd637dc125f296aad)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service GoogleCloudRunV2Service#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9c5d0696b83fc08b269341d20f698b8a2e28deb1496fd860581f2da074a574c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fb187ac96f242187f1d7fc9f8a0c378101302c659348469062968bd562ead27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934db6863d273cd4b838cd67b8331bfeb34c07d22b65db546ca9052e7d9986d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db47f2237411ff46892587e8d3eae9490e6288927ab706828d6866c1f1129ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_headers GoogleCloudRunV2Service#http_headers}
        :param path: Path to access on the HTTP server. Defaults to '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade39985521df5ad4a9976489b08c9a5be1c3d0088350c6c8d999d8d4300a0cb)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_headers GoogleCloudRunV2Service#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. Defaults to '/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Number must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#value GoogleCloudRunV2Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357f4e74f1f684136d4c93da49994927d1f12374f1285752ad8c7136b7fc43be)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#value GoogleCloudRunV2Service#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab5f7383d2a6fe8c5b003ae6f06fb0e8abc2736c07c9105282f1e638feaf8dc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c83faaffeab143b6967cf8dec1afa86044e239f693c459efc87378a37e5c798)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39da5f6fb9c0f6227a6342844000f363ef429af951ef5dd676ab162448fca3ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e2ec471aba67460e89a78b2dd217ec6902b57db914e49242b6a59c1dcd9a92f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fbd1278cafc7fae84f7a07a9eedb6100b9adcf832b9088880848da6b65e040d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de82d0dd58c1fb62b61a1d8992d547131ef2c45f3f92d1035af75f4fa196ab7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__507ee2f52e308782130fcc085199966e8c425a0b298ee4ca71dcff6e1c171a4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed44409980ec327c869b68ece42131b70800f333bb458688b0c8a2e222e99a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb81154a3230f35a85fd4cd8c7582add39556a42bdbec9bfb287f55821e027e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a3cb2aae730ec3dd57dc7992861ef618701b0f823e49f6c7d804e04638384b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8c8e7cd203628468e44acdeca6906e3c915bacbd92ede24f3e8cb45087cc6fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066ab0ebaf2df2c83f0816490a4aad21dd9433d8d703636ea225716f934cab67)
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
    ) -> GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__821af3fe71a7b3a93327e9fe5192d71dd0fa09c074fc21484d9f30fb1b31e40a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03b88aac7a40d9772a55bef5d7795f504ed74ed5bd2440d9dd6c65ec1870c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c84720e99906176f2f55ac5b7e48704c2d6944415603de27e3f790b19695598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9dcaef0f32e7f14a9ecde162f2316868c5e77c32f261232933ddf892a76910c)
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
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service GoogleCloudRunV2Service#service}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_headers GoogleCloudRunV2Service#http_headers}
        :param path: Path to access on the HTTP server. Defaults to '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet(
            http_headers=http_headers, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(self, *, port: jsii.Number) -> None:
        '''
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the exposed port of the container, which is the value of container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket(
            port=port
        )

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
    ) -> GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet], jsii.get(self, "httpGetInput"))

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
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4aa95043aa9a8e2fd8c39d47648b94adad65ea66b51b357547f2ab8803fdc9ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__805236cb7dc2ae256fe892c26c62c43457667f0b5d73e79e99f8b1179278b760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40feae15c472e26ff2da59f7c893a87f56a740ea9278f0ae02d3c46d379bf472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710ada82185dc578eab2842ab11982b5be6861989696ec2b189e0ef99e4d7014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbe]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae19a176eb45232a66e480fbc6075240bbb94cba4b2c943045040f535c20bdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"port": "port"},
)
class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket:
    def __init__(self, *, port: jsii.Number) -> None:
        '''
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the exposed port of the container, which is the value of container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b87cd830581d1ff85a5f95c4c2cbbcffa098131767805fd21c2b16ac6b002e6)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "port": port,
        }

    @builtins.property
    def port(self) -> jsii.Number:
        '''Port number to access on the container.

        Must be in the range 1 to 65535.
        If not specified, defaults to the exposed port of the container, which
        is the value of container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        result = self._values.get("port")
        assert result is not None, "Required property 'port' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b407a329332d7b8bbe85fd3c57584bb1945b5c9f1bbff632ceb50ad65274eff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__5f035ed62c0e7ca2ccdcb53a1dbafb486331458ba631182150ec49c49b2f7d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d16c38d4cfd10a72ba614df47b268559580c481df6c2d15e992b63dcde99c98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__164af89b3abd2d2cbded78a4c1827c8144c2101072668a46279a04a71c28ddf8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEnv")
    def put_env(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88470c15e9356673963755e232bed9e90b217f8d44d6815cc979fae8b23685e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnv", [value]))

    @jsii.member(jsii_name="putLivenessProbe")
    def put_liveness_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#failure_threshold GoogleCloudRunV2Service#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#grpc GoogleCloudRunV2Service#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_get GoogleCloudRunV2Service#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#initial_delay_seconds GoogleCloudRunV2Service#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#period_seconds GoogleCloudRunV2Service#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tcp_socket GoogleCloudRunV2Service#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout_seconds GoogleCloudRunV2Service#timeout_seconds}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersLivenessProbe(
            failure_threshold=failure_threshold,
            grpc=grpc,
            http_get=http_get,
            initial_delay_seconds=initial_delay_seconds,
            period_seconds=period_seconds,
            tcp_socket=tcp_socket,
            timeout_seconds=timeout_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putLivenessProbe", [value]))

    @jsii.member(jsii_name="putPorts")
    def put_ports(
        self,
        *,
        container_port: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_port: Port number the container listens on. This must be a valid TCP port number, 0 < containerPort < 65536. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#container_port GoogleCloudRunV2Service#container_port}
        :param name: If specified, used to specify which protocol to use. Allowed values are "http1" and "h2c". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersPorts(
            container_port=container_port, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putPorts", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        *,
        cpu_idle: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        startup_cpu_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cpu_idle: Determines whether CPU is only allocated during requests. True by default if the parent 'resources' field is not set. However, if 'resources' is set, this field must be explicitly set to true to preserve the default behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#cpu_idle GoogleCloudRunV2Service#cpu_idle}
        :param limits: Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#limits GoogleCloudRunV2Service#limits}
        :param startup_cpu_boost: Determines whether CPU should be boosted on startup of a new container instance above the requested CPU threshold, this can help reduce cold-start latency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#startup_cpu_boost GoogleCloudRunV2Service#startup_cpu_boost}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersResources(
            cpu_idle=cpu_idle, limits=limits, startup_cpu_boost=startup_cpu_boost
        )

        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="putStartupProbe")
    def put_startup_probe(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#failure_threshold GoogleCloudRunV2Service#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#grpc GoogleCloudRunV2Service#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_get GoogleCloudRunV2Service#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#initial_delay_seconds GoogleCloudRunV2Service#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#period_seconds GoogleCloudRunV2Service#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tcp_socket GoogleCloudRunV2Service#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout_seconds GoogleCloudRunV2Service#timeout_seconds}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersStartupProbe(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateContainersVolumeMounts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85fadf0d96458ba7dba2318dd12425011fdbb8e5f89351a343d7f39f101f2829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumeMounts", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetBaseImageUri")
    def reset_base_image_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseImageUri", []))

    @jsii.member(jsii_name="resetCommand")
    def reset_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCommand", []))

    @jsii.member(jsii_name="resetDependsOn")
    def reset_depends_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDependsOn", []))

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetLivenessProbe")
    def reset_liveness_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLivenessProbe", []))

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
    @jsii.member(jsii_name="buildInfo")
    def build_info(self) -> GoogleCloudRunV2ServiceTemplateContainersBuildInfoList:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersBuildInfoList, jsii.get(self, "buildInfo"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> GoogleCloudRunV2ServiceTemplateContainersEnvList:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersEnvList, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbe")
    def liveness_probe(
        self,
    ) -> GoogleCloudRunV2ServiceTemplateContainersLivenessProbeOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersLivenessProbeOutputReference, jsii.get(self, "livenessProbe"))

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> "GoogleCloudRunV2ServiceTemplateContainersPortsOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersPortsOutputReference", jsii.get(self, "ports"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersResourcesOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersResourcesOutputReference", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="startupProbe")
    def startup_probe(
        self,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersStartupProbeOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersStartupProbeOutputReference", jsii.get(self, "startupProbe"))

    @builtins.property
    @jsii.member(jsii_name="volumeMounts")
    def volume_mounts(
        self,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersVolumeMountsList":
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersVolumeMountsList", jsii.get(self, "volumeMounts"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="baseImageUriInput")
    def base_image_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseImageUriInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersEnv]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersEnv]]], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="livenessProbeInput")
    def liveness_probe_input(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbe]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbe], jsii.get(self, "livenessProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersPorts"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersPorts"], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersResources"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersResources"], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="startupProbeInput")
    def startup_probe_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbe"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbe"], jsii.get(self, "startupProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeMountsInput")
    def volume_mounts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersVolumeMounts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersVolumeMounts"]]], jsii.get(self, "volumeMountsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1382ff9463f208fc8e0927ce9dce7accaf88ce915f96aa498129c3ff0da823ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseImageUri")
    def base_image_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseImageUri"))

    @base_image_uri.setter
    def base_image_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4409c69e1cae58ca2e406ea82b98b3fac82792b438e1f02c284119786bb7ceb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseImageUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @command.setter
    def command(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53de62486ed0b6734deefbbf4766532414cb53d651787a539516f8a230a9f54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "command", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependsOn"))

    @depends_on.setter
    def depends_on(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d61c76e249474782c86826b2dee84a7c01c84b84ae21ffe33e1926553f00868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dependsOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d3856cf057186ce9386dffdb035b13cb009edf46a8fa484e2d5c4cebdad889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446b9abbc5878431f15c4f1a3b31162af0c88258a8f665c3b9f78bc3b974b070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b7325e69792ed5db0719868e069e8e8106b903aa0d07369229f452f0bc425d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workingDir", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413903c6827fab1e6e5fc57c066cc5887a19b1fa2fc816e229a57f10e0a34fd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersPorts",
    jsii_struct_bases=[],
    name_mapping={"container_port": "containerPort", "name": "name"},
)
class GoogleCloudRunV2ServiceTemplateContainersPorts:
    def __init__(
        self,
        *,
        container_port: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_port: Port number the container listens on. This must be a valid TCP port number, 0 < containerPort < 65536. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#container_port GoogleCloudRunV2Service#container_port}
        :param name: If specified, used to specify which protocol to use. Allowed values are "http1" and "h2c". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9709001868c215bb3b946b31fd1676bc3b050304995d8638bb112764bc668f0a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#container_port GoogleCloudRunV2Service#container_port}
        '''
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''If specified, used to specify which protocol to use. Allowed values are "http1" and "h2c".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersPorts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersPortsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersPortsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c2cae07ed12c26a40c6c2cff7883af0a85fbf80d61287798997632b6c2f5101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

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
            type_hints = typing.get_type_hints(_typecheckingstub__6c15f4ee17597826d32cc78b93550b7351242bebf438ead71282710804300250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010a3e173bdf3e583ee6456301cafc4ede9bfa1db0880972c297311e9baf16f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersPorts]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersPorts], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersPorts],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c06681ebbbb59d49d15d79c6bdf758ae3e6e4603e25a6bea7e4d06f45b561b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersResources",
    jsii_struct_bases=[],
    name_mapping={
        "cpu_idle": "cpuIdle",
        "limits": "limits",
        "startup_cpu_boost": "startupCpuBoost",
    },
)
class GoogleCloudRunV2ServiceTemplateContainersResources:
    def __init__(
        self,
        *,
        cpu_idle: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        startup_cpu_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param cpu_idle: Determines whether CPU is only allocated during requests. True by default if the parent 'resources' field is not set. However, if 'resources' is set, this field must be explicitly set to true to preserve the default behavior. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#cpu_idle GoogleCloudRunV2Service#cpu_idle}
        :param limits: Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#limits GoogleCloudRunV2Service#limits}
        :param startup_cpu_boost: Determines whether CPU should be boosted on startup of a new container instance above the requested CPU threshold, this can help reduce cold-start latency. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#startup_cpu_boost GoogleCloudRunV2Service#startup_cpu_boost}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a176bb0a0755ed5f290188d5ac6530ea8cfb9f55f0da36eb3c85d355498bb94a)
            check_type(argname="argument cpu_idle", value=cpu_idle, expected_type=type_hints["cpu_idle"])
            check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
            check_type(argname="argument startup_cpu_boost", value=startup_cpu_boost, expected_type=type_hints["startup_cpu_boost"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu_idle is not None:
            self._values["cpu_idle"] = cpu_idle
        if limits is not None:
            self._values["limits"] = limits
        if startup_cpu_boost is not None:
            self._values["startup_cpu_boost"] = startup_cpu_boost

    @builtins.property
    def cpu_idle(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether CPU is only allocated during requests.

        True by default if the parent 'resources' field is not set. However, if
        'resources' is set, this field must be explicitly set to true to preserve the default behavior.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#cpu_idle GoogleCloudRunV2Service#cpu_idle}
        '''
        result = self._values.get("cpu_idle")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def limits(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Only memory, CPU, and nvidia.com/gpu are supported. Use key 'cpu' for CPU limit, 'memory' for memory limit, 'nvidia.com/gpu' for gpu limit. Note: The only supported values for CPU are '1', '2', '4', and '8'. Setting 4 CPU requires at least 2Gi of memory. The values of the map is string form of the 'quantity' k8s type: https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apimachinery/pkg/api/resource/quantity.go.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#limits GoogleCloudRunV2Service#limits}
        '''
        result = self._values.get("limits")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def startup_cpu_boost(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Determines whether CPU should be boosted on startup of a new container instance above the requested CPU threshold, this can help reduce cold-start latency.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#startup_cpu_boost GoogleCloudRunV2Service#startup_cpu_boost}
        '''
        result = self._values.get("startup_cpu_boost")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8602ee11822ba69157cd399bb4203efb766471a14ad979c673a2ce548e75603)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCpuIdle")
    def reset_cpu_idle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuIdle", []))

    @jsii.member(jsii_name="resetLimits")
    def reset_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLimits", []))

    @jsii.member(jsii_name="resetStartupCpuBoost")
    def reset_startup_cpu_boost(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartupCpuBoost", []))

    @builtins.property
    @jsii.member(jsii_name="cpuIdleInput")
    def cpu_idle_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cpuIdleInput"))

    @builtins.property
    @jsii.member(jsii_name="limitsInput")
    def limits_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "limitsInput"))

    @builtins.property
    @jsii.member(jsii_name="startupCpuBoostInput")
    def startup_cpu_boost_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startupCpuBoostInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuIdle")
    def cpu_idle(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cpuIdle"))

    @cpu_idle.setter
    def cpu_idle(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225ddccc6484d7259f7492b6f31469302a0f8cc3ebe736c49a7929ec5dc3e87d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuIdle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="limits")
    def limits(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "limits"))

    @limits.setter
    def limits(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f14072e7768e99730b9bbd8d2371cf2c36e0f2fb92cb879c1f900c1c0a3c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startupCpuBoost")
    def startup_cpu_boost(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startupCpuBoost"))

    @startup_cpu_boost.setter
    def startup_cpu_boost(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9e1b166fefd87159a7e76416d418b6fd2b5a4d4b790aa0d42bd08bc2fb2ad0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startupCpuBoost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersResources]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beddeeecfd90ed57b36fbdd85a9585b5a08c989e0dfbaddcb0355e31c5c6ba94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbe",
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
class GoogleCloudRunV2ServiceTemplateContainersStartupProbe:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        grpc: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc", typing.Dict[builtins.str, typing.Any]]] = None,
        http_get: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet", typing.Dict[builtins.str, typing.Any]]] = None,
        initial_delay_seconds: typing.Optional[jsii.Number] = None,
        period_seconds: typing.Optional[jsii.Number] = None,
        tcp_socket: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param failure_threshold: Minimum consecutive failures for the probe to be considered failed after having succeeded. Defaults to 3. Minimum value is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#failure_threshold GoogleCloudRunV2Service#failure_threshold}
        :param grpc: grpc block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#grpc GoogleCloudRunV2Service#grpc}
        :param http_get: http_get block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_get GoogleCloudRunV2Service#http_get}
        :param initial_delay_seconds: Number of seconds after the container has started before the probe is initiated. Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#initial_delay_seconds GoogleCloudRunV2Service#initial_delay_seconds}
        :param period_seconds: How often (in seconds) to perform the probe. Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#period_seconds GoogleCloudRunV2Service#period_seconds}
        :param tcp_socket: tcp_socket block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tcp_socket GoogleCloudRunV2Service#tcp_socket}
        :param timeout_seconds: Number of seconds after which the probe times out. Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout_seconds GoogleCloudRunV2Service#timeout_seconds}
        '''
        if isinstance(grpc, dict):
            grpc = GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc(**grpc)
        if isinstance(http_get, dict):
            http_get = GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet(**http_get)
        if isinstance(tcp_socket, dict):
            tcp_socket = GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket(**tcp_socket)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1435204ced9fb5b0813a6fc3a39c8de10addea0d512b91cc7a59215c01c39bde)
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
        '''Minimum consecutive failures for the probe to be considered failed after having succeeded.

        Defaults to 3. Minimum value is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#failure_threshold GoogleCloudRunV2Service#failure_threshold}
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def grpc(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc"]:
        '''grpc block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#grpc GoogleCloudRunV2Service#grpc}
        '''
        result = self._values.get("grpc")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc"], result)

    @builtins.property
    def http_get(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet"]:
        '''http_get block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_get GoogleCloudRunV2Service#http_get}
        '''
        result = self._values.get("http_get")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet"], result)

    @builtins.property
    def initial_delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after the container has started before the probe is initiated.

        Defaults to 0 seconds. Minimum value is 0. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#initial_delay_seconds GoogleCloudRunV2Service#initial_delay_seconds}
        '''
        result = self._values.get("initial_delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def period_seconds(self) -> typing.Optional[jsii.Number]:
        '''How often (in seconds) to perform the probe.

        Default to 10 seconds. Minimum value is 1. Maximum value for liveness probe is 3600. Maximum value for startup probe is 240. Must be greater or equal than timeoutSeconds

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#period_seconds GoogleCloudRunV2Service#period_seconds}
        '''
        result = self._values.get("period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tcp_socket(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket"]:
        '''tcp_socket block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tcp_socket GoogleCloudRunV2Service#tcp_socket}
        '''
        result = self._values.get("tcp_socket")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Number of seconds after which the probe times out.

        Defaults to 1 second. Minimum value is 1. Maximum value is 3600. Must be smaller than periodSeconds. More info: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#timeout_seconds GoogleCloudRunV2Service#timeout_seconds}
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersStartupProbe(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc",
    jsii_struct_bases=[],
    name_mapping={"port": "port", "service": "service"},
)
class GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc:
    def __init__(
        self,
        *,
        port: typing.Optional[jsii.Number] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service GoogleCloudRunV2Service#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__127403790533d49a3a2402c4bb764e7f9e4a821fe473a2a8fd41bd627af7b343)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service GoogleCloudRunV2Service#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62f7b1d3339c07936414f787113fcb8a37fc82cd2b39d1fd8d5e6b12ca59d51b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aba579e5fced8f62353ece194a0957de005c5540cb4230164731a61ec055dbd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31ace03317284a2a1655657696f9ea018fb21a3676b143cbafcefe994a303f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399907a806b3ec0fa71ab601babaacea5697bd49ae2eb1401aa0594cbea720d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet",
    jsii_struct_bases=[],
    name_mapping={"http_headers": "httpHeaders", "path": "path", "port": "port"},
)
class GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet:
    def __init__(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_headers GoogleCloudRunV2Service#http_headers}
        :param path: Path to access on the HTTP server. Defaults to '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__473d22932bec0452abc27340ac4c70748cf0e82497f2b70628e11a52546461e2)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders"]]]:
        '''http_headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_headers GoogleCloudRunV2Service#http_headers}
        '''
        result = self._values.get("http_headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders"]]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path to access on the HTTP server. Defaults to '/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: The header field name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        :param value: The header field value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#value GoogleCloudRunV2Service#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8eb1e353a9264b66b02283f36065e942a44f796c8155b9675b8c435a404aa48)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The header field value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#value GoogleCloudRunV2Service#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab0b126ef124256242fae2a0de76cb010fcf0ecd2a49d0b85ca0dc0753346441)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee6bc45b5df36e631d7e9621a713650a9186c94cd45bb7f6bedee37a6a0687d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9680f7cfd6373c85f6c547e7ad4cbf50417a2e893c46115140a4c6bc7320a317)
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
            type_hints = typing.get_type_hints(_typecheckingstub__51e89f91cc8631f4e7e3132724904d8dc092efcd13b60bc45c4f7d09c72c15c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c36ca945eff150a6620f43aa284b171881c849bb8563f83e246524dacb2dc9c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccbab00c4242950851c66fccdd3f408d35ff7151f34987e2e36b6706667647f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7deb6c8caae64c5d357aa9973cc36e3089e28be01006a8f40b5c3772df3ee2af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b2f088328dd30d38a7afc79e8e3d44c7e95745c3120ee928ea11845325a9bda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4461bc80ea9e7d5087a554aff277de107052b2d660bf91ec3958e10d300bfd5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7323ca1662f481ac2e64397a7068243f5db94d6318bd8c2711867c320230b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad92ad6d7d1dc6a02e0e1b68007a9651928d0c21029f99dc21f5e02a8c3a9946)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpHeaders")
    def put_http_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629688d2472a4cd6c5d054b825b006195498eaabeb3448477f1821a4ed097519)
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
    ) -> GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList, jsii.get(self, "httpHeaders"))

    @builtins.property
    @jsii.member(jsii_name="httpHeadersInput")
    def http_headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]], jsii.get(self, "httpHeadersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__07c48f54f0b9a1087c68f51a0309debb0ed99cc5defe1f0633270e7910cdaef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9633cab1e2e744153fca340ae3bd5071eebfa98f8df57d7e512d23f4c449fbed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdda7fb9e056e43ce670c4897698e0ccbfa3170e445f4eda24c0d34a309084e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersStartupProbeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__966e7fb7448857bc39e96d03c2988e976f14ba0971261f21b21f29b5454f36c9)
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
        :param port: Port number to access on the container. Number must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        :param service: The name of the service to place in the gRPC HealthCheckRequest (see https://github.com/grpc/grpc/blob/master/doc/health-checking.md). If this is not specified, the default behavior is defined by gRPC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#service GoogleCloudRunV2Service#service}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc(
            port=port, service=service
        )

        return typing.cast(None, jsii.invoke(self, "putGrpc", [value]))

    @jsii.member(jsii_name="putHttpGet")
    def put_http_get(
        self,
        *,
        http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_headers: http_headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#http_headers GoogleCloudRunV2Service#http_headers}
        :param path: Path to access on the HTTP server. Defaults to '/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet(
            http_headers=http_headers, path=path, port=port
        )

        return typing.cast(None, jsii.invoke(self, "putHttpGet", [value]))

    @jsii.member(jsii_name="putTcpSocket")
    def put_tcp_socket(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        value = GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket(
            port=port
        )

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
    ) -> GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference, jsii.get(self, "grpc"))

    @builtins.property
    @jsii.member(jsii_name="httpGet")
    def http_get(
        self,
    ) -> GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference, jsii.get(self, "httpGet"))

    @builtins.property
    @jsii.member(jsii_name="tcpSocket")
    def tcp_socket(
        self,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference", jsii.get(self, "tcpSocket"))

    @builtins.property
    @jsii.member(jsii_name="failureThresholdInput")
    def failure_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failureThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcInput")
    def grpc_input(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc], jsii.get(self, "grpcInput"))

    @builtins.property
    @jsii.member(jsii_name="httpGetInput")
    def http_get_input(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet], jsii.get(self, "httpGetInput"))

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
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket"], jsii.get(self, "tcpSocketInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__28e651e0cfba66e3b1bff5d96dd1c9e39f506cf595e705abb08b9df35f2972d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failureThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="initialDelaySeconds")
    def initial_delay_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "initialDelaySeconds"))

    @initial_delay_seconds.setter
    def initial_delay_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b526a9abe473c7d75f44827211104b00029f4844490226e536028a542e102dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialDelaySeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="periodSeconds")
    def period_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "periodSeconds"))

    @period_seconds.setter
    def period_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e55f12b7b0f5aeee7e373455abb9c422f11d4c899b7d825a3154cefe92b0d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "periodSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutSeconds")
    def timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutSeconds"))

    @timeout_seconds.setter
    def timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ec1f3d89b1f929d6f9caf497022af11fc4eec112d1cf31b39e70d547b3576c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbe]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbe], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbe],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056fcf20a80a6f7905a13e6c3785c5bb67815c3604e650d44fbf98edbc817fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket",
    jsii_struct_bases=[],
    name_mapping={"port": "port"},
)
class GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket:
    def __init__(self, *, port: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param port: Port number to access on the container. Must be in the range 1 to 65535. If not specified, defaults to the same value as container.ports[0].containerPort. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b78293ddf915c3c892d2b98a92343daaf4f6bf30e7b6b8f364aa80b9ae4b0f4)
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number to access on the container.

        Must be in the range 1 to 65535.
        If not specified, defaults to the same value as container.ports[0].containerPort.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#port GoogleCloudRunV2Service#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a7a07f38527ed340f53d0e3ced71896cec1e378983ca527344f2f78485d9a06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea143c80a97f15afbfb670f4cb27e6e62dda339498ab271db874fe74e25ab651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41495a01fca52a513f32053407b2e3e1d5bec22923594b259e6d002e54ccca59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersVolumeMounts",
    jsii_struct_bases=[],
    name_mapping={"mount_path": "mountPath", "name": "name"},
)
class GoogleCloudRunV2ServiceTemplateContainersVolumeMounts:
    def __init__(self, *, mount_path: builtins.str, name: builtins.str) -> None:
        '''
        :param mount_path: Path within the container at which the volume should be mounted. Must not contain ':'. For Cloud SQL volumes, it can be left empty, or must otherwise be /cloudsql. All instances defined in the Volume will be available as /cloudsql/[instance]. For more information on Cloud SQL volumes, visit https://cloud.google.com/sql/docs/mysql/connect-run Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mount_path GoogleCloudRunV2Service#mount_path}
        :param name: This must match the Name of a Volume. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64cdb074c5c0d0c8582f12d8a1e040e75313bdaa925ac9bd59bf365ee8edeb8b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mount_path GoogleCloudRunV2Service#mount_path}
        '''
        result = self._values.get("mount_path")
        assert result is not None, "Required property 'mount_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''This must match the Name of a Volume.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateContainersVolumeMounts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateContainersVolumeMountsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersVolumeMountsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__212b3b736d15212730a662fe252504d261d052b565939718e623f3f01bcc6a82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateContainersVolumeMountsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ae1a84c0f44d670f3d14a8dc06274bd5d9b92758e2c13048f1078af6054f8c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateContainersVolumeMountsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3213c7caf20745851ae26312ba4bf94f639e7a9612a5dcc98b66ebaf345a476e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31b2570760086ae8989f23048b81d3cc3f3707d22f42836b4e11e0e3193ec244)
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
            type_hints = typing.get_type_hints(_typecheckingstub__244afa223c1a8143a5446a845004376b71f00a3460ecf73482c894437bdada88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersVolumeMounts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersVolumeMounts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersVolumeMounts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f87e28b82b38bef83a4fc1093a52d8166f880fa4446def19527c0c75416136d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateContainersVolumeMountsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateContainersVolumeMountsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a486f6f142637eca38432276f691b3f7a4ad0b106090e1290ad072093e38406c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b372a269de7a8ebfb7b96237460d845ed0ed409b228a570355c86d65301a24c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fccc7286a1c211e551601bee91943a022e66f2440ec9cdd49123a0e7eddb7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersVolumeMounts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersVolumeMounts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersVolumeMounts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__010e1ec998968833092e1b7475e91c70fa1f6151bf965a24d88f9301903d55d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateNodeSelector",
    jsii_struct_bases=[],
    name_mapping={"accelerator": "accelerator"},
)
class GoogleCloudRunV2ServiceTemplateNodeSelector:
    def __init__(self, *, accelerator: builtins.str) -> None:
        '''
        :param accelerator: The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#accelerator GoogleCloudRunV2Service#accelerator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac7ca347a2a676eb2e943f196c4191325acfce581e2754e7a2ab59c2e5f5eb6)
            check_type(argname="argument accelerator", value=accelerator, expected_type=type_hints["accelerator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "accelerator": accelerator,
        }

    @builtins.property
    def accelerator(self) -> builtins.str:
        '''The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#accelerator GoogleCloudRunV2Service#accelerator}
        '''
        result = self._values.get("accelerator")
        assert result is not None, "Required property 'accelerator' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateNodeSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateNodeSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateNodeSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5390ab33c9cdf381b4dec3d1451cbf319ee6fc8b21ac788ee0c1dd2d94b09891)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccee3cecd7947d516abccdbdaa0435472da36acca78bdaa7b58d7078426ec50f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accelerator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateNodeSelector]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateNodeSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateNodeSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e97148825912bd58d85c2c57b43233e385772c095d413f0bd5b51675ac39de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f2d7832816d889ed848674530f2eee413a691add66dccc81d32154e851e26f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putContainers")
    def put_containers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainers, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c7c567ad3efc3c6bda8dd749f2666e31f858eada0ea6a6a8f55d37070931e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainers", [value]))

    @jsii.member(jsii_name="putNodeSelector")
    def put_node_selector(self, *, accelerator: builtins.str) -> None:
        '''
        :param accelerator: The GPU to attach to an instance. See https://cloud.google.com/run/docs/configuring/services/gpu for configuring GPU. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#accelerator GoogleCloudRunV2Service#accelerator}
        '''
        value = GoogleCloudRunV2ServiceTemplateNodeSelector(accelerator=accelerator)

        return typing.cast(None, jsii.invoke(self, "putNodeSelector", [value]))

    @jsii.member(jsii_name="putScaling")
    def put_scaling(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instance_count: Maximum number of serving instances that this resource should have. Must not be less than minimum instance count. If absent, Cloud Run will calculate a default value based on the project's available container instances quota in the region and specified instance size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#max_instance_count GoogleCloudRunV2Service#max_instance_count}
        :param min_instance_count: Minimum number of serving instances that this resource should have. Defaults to 0. Must not be greater than maximum instance count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#min_instance_count GoogleCloudRunV2Service#min_instance_count}
        '''
        value = GoogleCloudRunV2ServiceTemplateScaling(
            max_instance_count=max_instance_count,
            min_instance_count=min_instance_count,
        )

        return typing.cast(None, jsii.invoke(self, "putScaling", [value]))

    @jsii.member(jsii_name="putServiceMesh")
    def put_service_mesh(self, *, mesh: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mesh: The Mesh resource name. For more information see https://cloud.google.com/service-mesh/docs/reference/network-services/rest/v1/projects.locations.meshes#resource:-mesh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mesh GoogleCloudRunV2Service#mesh}
        '''
        value = GoogleCloudRunV2ServiceTemplateServiceMesh(mesh=mesh)

        return typing.cast(None, jsii.invoke(self, "putServiceMesh", [value]))

    @jsii.member(jsii_name="putVolumes")
    def put_volumes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateVolumes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4baadf5a84d267eb07992ea93554fb86ee1fda972184aac9befe5125e57e9359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolumes", [value]))

    @jsii.member(jsii_name="putVpcAccess")
    def put_vpc_access(
        self,
        *,
        connector: typing.Optional[builtins.str] = None,
        egress: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connector: VPC Access connector name. Format: projects/{project}/locations/{location}/connectors/{connector}, where {project} can be project id or number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#connector GoogleCloudRunV2Service#connector}
        :param egress: Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#egress GoogleCloudRunV2Service#egress}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#network_interfaces GoogleCloudRunV2Service#network_interfaces}
        '''
        value = GoogleCloudRunV2ServiceTemplateVpcAccess(
            connector=connector, egress=egress, network_interfaces=network_interfaces
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

    @jsii.member(jsii_name="resetExecutionEnvironment")
    def reset_execution_environment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionEnvironment", []))

    @jsii.member(jsii_name="resetGpuZonalRedundancyDisabled")
    def reset_gpu_zonal_redundancy_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpuZonalRedundancyDisabled", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMaxInstanceRequestConcurrency")
    def reset_max_instance_request_concurrency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceRequestConcurrency", []))

    @jsii.member(jsii_name="resetNodeSelector")
    def reset_node_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeSelector", []))

    @jsii.member(jsii_name="resetRevision")
    def reset_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRevision", []))

    @jsii.member(jsii_name="resetScaling")
    def reset_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScaling", []))

    @jsii.member(jsii_name="resetServiceAccount")
    def reset_service_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceAccount", []))

    @jsii.member(jsii_name="resetServiceMesh")
    def reset_service_mesh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceMesh", []))

    @jsii.member(jsii_name="resetSessionAffinity")
    def reset_session_affinity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionAffinity", []))

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
    def containers(self) -> GoogleCloudRunV2ServiceTemplateContainersList:
        return typing.cast(GoogleCloudRunV2ServiceTemplateContainersList, jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelector")
    def node_selector(
        self,
    ) -> GoogleCloudRunV2ServiceTemplateNodeSelectorOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateNodeSelectorOutputReference, jsii.get(self, "nodeSelector"))

    @builtins.property
    @jsii.member(jsii_name="scaling")
    def scaling(self) -> "GoogleCloudRunV2ServiceTemplateScalingOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateScalingOutputReference", jsii.get(self, "scaling"))

    @builtins.property
    @jsii.member(jsii_name="serviceMesh")
    def service_mesh(
        self,
    ) -> "GoogleCloudRunV2ServiceTemplateServiceMeshOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateServiceMeshOutputReference", jsii.get(self, "serviceMesh"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> "GoogleCloudRunV2ServiceTemplateVolumesList":
        return typing.cast("GoogleCloudRunV2ServiceTemplateVolumesList", jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccess")
    def vpc_access(self) -> "GoogleCloudRunV2ServiceTemplateVpcAccessOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateVpcAccessOutputReference", jsii.get(self, "vpcAccess"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainers]]], jsii.get(self, "containersInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="executionEnvironmentInput")
    def execution_environment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionEnvironmentInput"))

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
    @jsii.member(jsii_name="maxInstanceRequestConcurrencyInput")
    def max_instance_request_concurrency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceRequestConcurrencyInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeSelectorInput")
    def node_selector_input(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateNodeSelector]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateNodeSelector], jsii.get(self, "nodeSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="revisionInput")
    def revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "revisionInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingInput")
    def scaling_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateScaling"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateScaling"], jsii.get(self, "scalingInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccountInput")
    def service_account_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceMeshInput")
    def service_mesh_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateServiceMesh"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateServiceMesh"], jsii.get(self, "serviceMeshInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionAffinityInput")
    def session_affinity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sessionAffinityInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="volumesInput")
    def volumes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateVolumes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateVolumes"]]], jsii.get(self, "volumesInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcAccessInput")
    def vpc_access_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateVpcAccess"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateVpcAccess"], jsii.get(self, "vpcAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9867771fccee7549992bb45b142e6a17041b3cf2ee0bf8c106cd978a88b3e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKey"))

    @encryption_key.setter
    def encryption_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4853f7dfa84750e2b923c13214a59d6fb9e13c2f6551de00f27e373e40637112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="executionEnvironment")
    def execution_environment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionEnvironment"))

    @execution_environment.setter
    def execution_environment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383e18d2d3e849af4f17998cfe416fa9660608969f57e4696c70b10dfd144193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionEnvironment", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0acd93d70611f5eaa163e3f958e9e150255e63cb91b4df94c16ead68a6bb1d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpuZonalRedundancyDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c6e84db4c84433091ffc9fb13301ebfec25df8bd8e2a8e391f4ff4017df33c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxInstanceRequestConcurrency")
    def max_instance_request_concurrency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceRequestConcurrency"))

    @max_instance_request_concurrency.setter
    def max_instance_request_concurrency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5f69efcefb4e7050d49b9a084bda1c47498b64e622c5bd26e1054c4830d2a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceRequestConcurrency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e5a9df9dcc05fe031fb6eb15accbc83c032cd631b04c286504dd0869535ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e848062a97e267c3e8854ff05d135256824edc1e96351dbc16cf8dd4f2398b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceAccount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sessionAffinity")
    def session_affinity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sessionAffinity"))

    @session_affinity.setter
    def session_affinity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20cd94552253ea4b4a7f35db1164915d461dfdceeb8d486429c249c09d23bd23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionAffinity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a882a09fadb649e59f2433178131b0859abc83295769db98c0f8aae9905365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunV2ServiceTemplate]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f530c3fb29adb552e1f7104e52c3fd3f81160c409a222d78d9a95750a9791ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateScaling",
    jsii_struct_bases=[],
    name_mapping={
        "max_instance_count": "maxInstanceCount",
        "min_instance_count": "minInstanceCount",
    },
)
class GoogleCloudRunV2ServiceTemplateScaling:
    def __init__(
        self,
        *,
        max_instance_count: typing.Optional[jsii.Number] = None,
        min_instance_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_instance_count: Maximum number of serving instances that this resource should have. Must not be less than minimum instance count. If absent, Cloud Run will calculate a default value based on the project's available container instances quota in the region and specified instance size. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#max_instance_count GoogleCloudRunV2Service#max_instance_count}
        :param min_instance_count: Minimum number of serving instances that this resource should have. Defaults to 0. Must not be greater than maximum instance count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#min_instance_count GoogleCloudRunV2Service#min_instance_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7652748c35392c2910afa2118d854e0d4aa31344e8ff898031a7610f664a6081)
            check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
            check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_instance_count is not None:
            self._values["max_instance_count"] = max_instance_count
        if min_instance_count is not None:
            self._values["min_instance_count"] = min_instance_count

    @builtins.property
    def max_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of serving instances that this resource should have.

        Must not be less than minimum instance count. If absent, Cloud Run will calculate
        a default value based on the project's available container instances quota in the region and specified instance size.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#max_instance_count GoogleCloudRunV2Service#max_instance_count}
        '''
        result = self._values.get("max_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Minimum number of serving instances that this resource should have.

        Defaults to 0. Must not be greater than maximum instance count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#min_instance_count GoogleCloudRunV2Service#min_instance_count}
        '''
        result = self._values.get("min_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe851cdbb2e7ca3bcbc452276e47babab19aff68fe7676dfcea5f8bd02a181e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxInstanceCount")
    def reset_max_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxInstanceCount", []))

    @jsii.member(jsii_name="resetMinInstanceCount")
    def reset_min_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinInstanceCount", []))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCountInput")
    def max_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minInstanceCountInput")
    def min_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxInstanceCount")
    def max_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxInstanceCount"))

    @max_instance_count.setter
    def max_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c09c936b9843ade074677f50b3855982d162930ea261a7a39023523d3ad41aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minInstanceCount")
    def min_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minInstanceCount"))

    @min_instance_count.setter
    def min_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdb503e28ed141a683341227a9ca41630b9f557e544482c9c3d04403a81fb44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunV2ServiceTemplateScaling]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef7167b7dfad451c0f182ba97b272bb80991b25418a9adabb767f38e28a5236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateServiceMesh",
    jsii_struct_bases=[],
    name_mapping={"mesh": "mesh"},
)
class GoogleCloudRunV2ServiceTemplateServiceMesh:
    def __init__(self, *, mesh: typing.Optional[builtins.str] = None) -> None:
        '''
        :param mesh: The Mesh resource name. For more information see https://cloud.google.com/service-mesh/docs/reference/network-services/rest/v1/projects.locations.meshes#resource:-mesh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mesh GoogleCloudRunV2Service#mesh}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db25562cd4aad377dbd0f769f49c4613b1cb1b0c86d28af990cc831c9f9e45dd)
            check_type(argname="argument mesh", value=mesh, expected_type=type_hints["mesh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if mesh is not None:
            self._values["mesh"] = mesh

    @builtins.property
    def mesh(self) -> typing.Optional[builtins.str]:
        '''The Mesh resource name. For more information see https://cloud.google.com/service-mesh/docs/reference/network-services/rest/v1/projects.locations.meshes#resource:-mesh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mesh GoogleCloudRunV2Service#mesh}
        '''
        result = self._values.get("mesh")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateServiceMesh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateServiceMeshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateServiceMeshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__130bf8434a19f491b4893ba92f978a890173df6adcd69507afbe7ecf22d8a324)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMesh")
    def reset_mesh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMesh", []))

    @builtins.property
    @jsii.member(jsii_name="meshInput")
    def mesh_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "meshInput"))

    @builtins.property
    @jsii.member(jsii_name="mesh")
    def mesh(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mesh"))

    @mesh.setter
    def mesh(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b4d01e5284fe3ce27e26ddc1fc80e33db4deb57d8c3512912c13088f2d6545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mesh", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateServiceMesh]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateServiceMesh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateServiceMesh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ad3f0708edfbb81d2cc10bf9afa4cc4dac815cbd45ad60f3f84e95cb69dd28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumes",
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
class GoogleCloudRunV2ServiceTemplateVolumes:
    def __init__(
        self,
        *,
        name: builtins.str,
        cloud_sql_instance: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance", typing.Dict[builtins.str, typing.Any]]] = None,
        empty_dir: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateVolumesEmptyDir", typing.Dict[builtins.str, typing.Any]]] = None,
        gcs: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateVolumesGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        nfs: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateVolumesNfs", typing.Dict[builtins.str, typing.Any]]] = None,
        secret: typing.Optional[typing.Union["GoogleCloudRunV2ServiceTemplateVolumesSecret", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Volume's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        :param cloud_sql_instance: cloud_sql_instance block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#cloud_sql_instance GoogleCloudRunV2Service#cloud_sql_instance}
        :param empty_dir: empty_dir block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#empty_dir GoogleCloudRunV2Service#empty_dir}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#gcs GoogleCloudRunV2Service#gcs}
        :param nfs: nfs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#nfs GoogleCloudRunV2Service#nfs}
        :param secret: secret block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret GoogleCloudRunV2Service#secret}
        '''
        if isinstance(cloud_sql_instance, dict):
            cloud_sql_instance = GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance(**cloud_sql_instance)
        if isinstance(empty_dir, dict):
            empty_dir = GoogleCloudRunV2ServiceTemplateVolumesEmptyDir(**empty_dir)
        if isinstance(gcs, dict):
            gcs = GoogleCloudRunV2ServiceTemplateVolumesGcs(**gcs)
        if isinstance(nfs, dict):
            nfs = GoogleCloudRunV2ServiceTemplateVolumesNfs(**nfs)
        if isinstance(secret, dict):
            secret = GoogleCloudRunV2ServiceTemplateVolumesSecret(**secret)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a37fc8cde2344446bf7b6b15a9de46a0f6d82357940ea083ea3376aa36a195)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#name GoogleCloudRunV2Service#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_sql_instance(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance"]:
        '''cloud_sql_instance block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#cloud_sql_instance GoogleCloudRunV2Service#cloud_sql_instance}
        '''
        result = self._values.get("cloud_sql_instance")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance"], result)

    @builtins.property
    def empty_dir(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesEmptyDir"]:
        '''empty_dir block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#empty_dir GoogleCloudRunV2Service#empty_dir}
        '''
        result = self._values.get("empty_dir")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesEmptyDir"], result)

    @builtins.property
    def gcs(self) -> typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#gcs GoogleCloudRunV2Service#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesGcs"], result)

    @builtins.property
    def nfs(self) -> typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesNfs"]:
        '''nfs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#nfs GoogleCloudRunV2Service#nfs}
        '''
        result = self._values.get("nfs")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesNfs"], result)

    @builtins.property
    def secret(self) -> typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesSecret"]:
        '''secret block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret GoogleCloudRunV2Service#secret}
        '''
        result = self._values.get("secret")
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesSecret"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance",
    jsii_struct_bases=[],
    name_mapping={"instances": "instances"},
)
class GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance:
    def __init__(
        self,
        *,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param instances: The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#instances GoogleCloudRunV2Service#instances}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d3c77999ae9ea213f032cf54069d9bfb15848925fb4acd1064d19472a75494)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instances is not None:
            self._values["instances"] = instances

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#instances GoogleCloudRunV2Service#instances}
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f20ee5cba4520762bbe88f31933911412fbc2a39a4822c73f6bb20f72fd53833)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67cf2f5ecafb006f4a4e1b24a51fb5a655c85994e2a02b37bed5057c8dca438b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b8d5a037886bb91892227a087a0c1cc111808e5697325709c915562106657e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesEmptyDir",
    jsii_struct_bases=[],
    name_mapping={"medium": "medium", "size_limit": "sizeLimit"},
)
class GoogleCloudRunV2ServiceTemplateVolumesEmptyDir:
    def __init__(
        self,
        *,
        medium: typing.Optional[builtins.str] = None,
        size_limit: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param medium: The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#medium GoogleCloudRunV2Service#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#size_limit GoogleCloudRunV2Service#size_limit}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e63deec4188b2112489ec70ff1a0a227c611d4fc30d9ec52b1088cc83b7f89)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#medium GoogleCloudRunV2Service#medium}
        '''
        result = self._values.get("medium")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def size_limit(self) -> typing.Optional[builtins.str]:
        '''Limit on the storage usable by this EmptyDir volume.

        The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#size_limit GoogleCloudRunV2Service#size_limit}
        '''
        result = self._values.get("size_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVolumesEmptyDir(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateVolumesEmptyDirOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesEmptyDirOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__159ff4ee399e59d6ab4e05c45927814687b5b360dd14cd0f45f7d040aec26949)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d967e7390e871593ca41f29af0a049c6ed882684f152ffb5d6b81a81958b37f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "medium", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeLimit")
    def size_limit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeLimit"))

    @size_limit.setter
    def size_limit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7b3976086fdc700a3ca5693f7a374723bca4abf0e378c4ab81590d68a2970a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesEmptyDir]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesEmptyDir], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesEmptyDir],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f415843a59c858ccce4d64957f6114cf31a5ef68b7ae63199a1407be11c9a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesGcs",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "mount_options": "mountOptions",
        "read_only": "readOnly",
    },
)
class GoogleCloudRunV2ServiceTemplateVolumesGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket: GCS Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#bucket GoogleCloudRunV2Service#bucket}
        :param mount_options: A list of flags to pass to the gcsfuse command for configuring this volume. Flags should be passed without leading dashes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mount_options GoogleCloudRunV2Service#mount_options}
        :param read_only: If true, mount the GCS bucket as read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#read_only GoogleCloudRunV2Service#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3047b64510cde95cc6010a61b8309364c6a06e621204cee2f304658b9173ba)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options
        if read_only is not None:
            self._values["read_only"] = read_only

    @builtins.property
    def bucket(self) -> builtins.str:
        '''GCS Bucket name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#bucket GoogleCloudRunV2Service#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of flags to pass to the gcsfuse command for configuring this volume.

        Flags should be passed without leading dashes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mount_options GoogleCloudRunV2Service#mount_options}
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount the GCS bucket as read-only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#read_only GoogleCloudRunV2Service#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVolumesGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateVolumesGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f7d77895488604cf7f7d49f8e58b796fe9ec3085322e38a28e6387c6b01589c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMountOptions")
    def reset_mount_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountOptions", []))

    @jsii.member(jsii_name="resetReadOnly")
    def reset_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnly", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="mountOptionsInput")
    def mount_options_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "mountOptionsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cc07109214a8ce81ca8a7e3f23cf556638b8440c79a865e951d6a2eeeb9c6ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountOptions")
    def mount_options(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mountOptions"))

    @mount_options.setter
    def mount_options(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a504a44a9650a4ee87b8e10e20ba8b464b034e4d1add06d29c89ae8855d24314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountOptions", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0141690ec1f400d4032aa0c1cd1ddc825fa8c4e03173f5b67bf1b43cdd9e65f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesGcs]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2fcd3a0727d88d0535eb7881cfd9dabeb2c77ab491564c70f041425f585434a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateVolumesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d2ac3092311887745c654f0e399796caf5fa4ccf59afd8d2fe2cdfa646fcd68)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateVolumesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b008a61b3118692bf2f2d99339b6390033b838646c46a156e35e9d3287b67e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateVolumesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ff8c9868bf0303b1be664222812a55be3495711df324dfdce12abed1c00696)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bebbf71340b40fe02bdd91c2be7ee90ae437e91a1bd1457bf2d4b4e2a9c89c1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca847b291d22d4913f8463b50029b590aea059a05b40b400f507ee2b83ace580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1748426832276794eb8c2896bbf38fabd234b1ace8bee4545767d6f32aafc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesNfs",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "server": "server", "read_only": "readOnly"},
)
class GoogleCloudRunV2ServiceTemplateVolumesNfs:
    def __init__(
        self,
        *,
        path: builtins.str,
        server: builtins.str,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param path: Path that is exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        :param server: Hostname or IP address of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#server GoogleCloudRunV2Service#server}
        :param read_only: If true, mount the NFS volume as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#read_only GoogleCloudRunV2Service#read_only}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c5846f8fb0277692947a23a93ae3a4c9d5fe979cd5a4055c49181228bbf1a6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Hostname or IP address of the NFS server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#server GoogleCloudRunV2Service#server}
        '''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, mount the NFS volume as read only.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#read_only GoogleCloudRunV2Service#read_only}
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVolumesNfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateVolumesNfsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesNfsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__605955e0f72323027f1754503789a48198d016aab9046903a99cc7eec26e1936)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16bdd5782b86a227ac96d40275e5e6552df7b266a002befa57673608243a1486)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a1631b9e36464f0a124bb8a4fdd9734ccd5110f6f3459fcbf0765ae44d3dc03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a379941ba07c7d9743a1e66d8af12f60d97ec1ce696aaa2b8391afc4c9745e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesNfs]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesNfs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesNfs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c308a7c43a6349de172eb77aa30dd3ca0f2eb8089c284b37d931223c711b5613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateVolumesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d15b3cf5047b7ee34e8f52548099effadff6a035759d9a8b5772979080d4e2e)
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
        :param instances: The Cloud SQL instance connection names, as can be found in https://console.cloud.google.com/sql/instances. Visit https://cloud.google.com/sql/docs/mysql/connect-run for more information on how to connect Cloud SQL and Cloud Run. Format: {project}:{location}:{instance}. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#instances GoogleCloudRunV2Service#instances}
        '''
        value = GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance(
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
        :param medium: The different types of medium supported for EmptyDir. Default value: "MEMORY" Possible values: ["MEMORY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#medium GoogleCloudRunV2Service#medium}
        :param size_limit: Limit on the storage usable by this EmptyDir volume. The size limit is also applicable for memory medium. The maximum usage on memory medium EmptyDir would be the minimum value between the SizeLimit specified here and the sum of memory limits of all containers in a pod. This field's values are of the 'Quantity' k8s type: https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/quantity/. The default is nil which means that the limit is undefined. More info: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#size_limit GoogleCloudRunV2Service#size_limit}
        '''
        value = GoogleCloudRunV2ServiceTemplateVolumesEmptyDir(
            medium=medium, size_limit=size_limit
        )

        return typing.cast(None, jsii.invoke(self, "putEmptyDir", [value]))

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param bucket: GCS Bucket name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#bucket GoogleCloudRunV2Service#bucket}
        :param mount_options: A list of flags to pass to the gcsfuse command for configuring this volume. Flags should be passed without leading dashes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mount_options GoogleCloudRunV2Service#mount_options}
        :param read_only: If true, mount the GCS bucket as read-only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#read_only GoogleCloudRunV2Service#read_only}
        '''
        value = GoogleCloudRunV2ServiceTemplateVolumesGcs(
            bucket=bucket, mount_options=mount_options, read_only=read_only
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
        :param path: Path that is exported by the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        :param server: Hostname or IP address of the NFS server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#server GoogleCloudRunV2Service#server}
        :param read_only: If true, mount the NFS volume as read only. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#read_only GoogleCloudRunV2Service#read_only}
        '''
        value = GoogleCloudRunV2ServiceTemplateVolumesNfs(
            path=path, server=server, read_only=read_only
        )

        return typing.cast(None, jsii.invoke(self, "putNfs", [value]))

    @jsii.member(jsii_name="putSecret")
    def put_secret(
        self,
        *,
        secret: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret GoogleCloudRunV2Service#secret}
        :param default_mode: Integer representation of mode bits to use on created files by default. Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#default_mode GoogleCloudRunV2Service#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#items GoogleCloudRunV2Service#items}
        '''
        value = GoogleCloudRunV2ServiceTemplateVolumesSecret(
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
    ) -> GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference, jsii.get(self, "cloudSqlInstance"))

    @builtins.property
    @jsii.member(jsii_name="emptyDir")
    def empty_dir(
        self,
    ) -> GoogleCloudRunV2ServiceTemplateVolumesEmptyDirOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateVolumesEmptyDirOutputReference, jsii.get(self, "emptyDir"))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(self) -> GoogleCloudRunV2ServiceTemplateVolumesGcsOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateVolumesGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="nfs")
    def nfs(self) -> GoogleCloudRunV2ServiceTemplateVolumesNfsOutputReference:
        return typing.cast(GoogleCloudRunV2ServiceTemplateVolumesNfsOutputReference, jsii.get(self, "nfs"))

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> "GoogleCloudRunV2ServiceTemplateVolumesSecretOutputReference":
        return typing.cast("GoogleCloudRunV2ServiceTemplateVolumesSecretOutputReference", jsii.get(self, "secret"))

    @builtins.property
    @jsii.member(jsii_name="cloudSqlInstanceInput")
    def cloud_sql_instance_input(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance], jsii.get(self, "cloudSqlInstanceInput"))

    @builtins.property
    @jsii.member(jsii_name="emptyDirInput")
    def empty_dir_input(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesEmptyDir]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesEmptyDir], jsii.get(self, "emptyDirInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(self) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesGcs]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsInput")
    def nfs_input(self) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesNfs]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesNfs], jsii.get(self, "nfsInput"))

    @builtins.property
    @jsii.member(jsii_name="secretInput")
    def secret_input(
        self,
    ) -> typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesSecret"]:
        return typing.cast(typing.Optional["GoogleCloudRunV2ServiceTemplateVolumesSecret"], jsii.get(self, "secretInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660d7d4e6fdda5946e6f918e530cce1bc165354190f1a63ba932cf0298c8ddf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVolumes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVolumes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVolumes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bde469ee88d1886d776d5ce0808ebf16733b12bc1e85e7bb3c2c8b6846f7aa0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesSecret",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "default_mode": "defaultMode", "items": "items"},
)
class GoogleCloudRunV2ServiceTemplateVolumesSecret:
    def __init__(
        self,
        *,
        secret: builtins.str,
        default_mode: typing.Optional[jsii.Number] = None,
        items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateVolumesSecretItems", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param secret: The name of the secret in Cloud Secret Manager. Format: {secret} if the secret is in the same project. projects/{project}/secrets/{secret} if the secret is in a different project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret GoogleCloudRunV2Service#secret}
        :param default_mode: Integer representation of mode bits to use on created files by default. Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#default_mode GoogleCloudRunV2Service#default_mode}
        :param items: items block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#items GoogleCloudRunV2Service#items}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f61bf26e62188aac61e3d39d4ed88eb87c22561423d94eb769871a5ad0132f6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#secret GoogleCloudRunV2Service#secret}
        '''
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_mode(self) -> typing.Optional[jsii.Number]:
        '''Integer representation of mode bits to use on created files by default.

        Must be a value between 0000 and 0777 (octal), defaulting to 0444. Directories within the path are not affected by this setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#default_mode GoogleCloudRunV2Service#default_mode}
        '''
        result = self._values.get("default_mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateVolumesSecretItems"]]]:
        '''items block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#items GoogleCloudRunV2Service#items}
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateVolumesSecretItems"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVolumesSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesSecretItems",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "mode": "mode", "version": "version"},
)
class GoogleCloudRunV2ServiceTemplateVolumesSecretItems:
    def __init__(
        self,
        *,
        path: builtins.str,
        mode: typing.Optional[jsii.Number] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The relative path of the secret in the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        :param mode: Integer octal mode bits to use on this file, must be a value between 01 and 0777 (octal). If 0 or not set, the Volume's default mode will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mode GoogleCloudRunV2Service#mode}
        :param version: The Cloud Secret Manager secret version. Can be 'latest' for the latest value or an integer for a specific version Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#version GoogleCloudRunV2Service#version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf71c7a55b91c82c807522a274294475db22a1dc6ed4dd317a5872d71087099a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#path GoogleCloudRunV2Service#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        '''Integer octal mode bits to use on this file, must be a value between 01 and 0777 (octal).

        If 0 or not set, the Volume's default mode will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#mode GoogleCloudRunV2Service#mode}
        '''
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Cloud Secret Manager secret version.

        Can be 'latest' for the latest value or an integer for a specific version

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#version GoogleCloudRunV2Service#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVolumesSecretItems(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateVolumesSecretItemsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesSecretItemsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0648728f6b1aba5fafb60fe37b358c1e2f71ed12057341822892239f96af3b07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateVolumesSecretItemsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e056ca3192c0690db537735df0d787212d0cfa92e68fd9fd34eab477e016df5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateVolumesSecretItemsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33fdcfda4ab7b7c6e6398b09af3ea83cdcf50419b73faa90a34e9147dbebd21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e86821068664f7b232c385acb453d6926fe0a0037e95c4e2c2f556baa75a866)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a2e52257a5b7544951f721b40ec87dc3d96b06d060ce8a5ea72934edb87a664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumesSecretItems]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumesSecretItems]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d966137dce1e8158851b6f292d9c4214651b8f35fed8436a0fcaefa97adfcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateVolumesSecretItemsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesSecretItemsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80ae21b41e5cf25bf78adad44fe2fdc95ccf0dfa1cd5153c23042eaad5c80646)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff56e5d023ecd133fb9de549898775e59ef5a0372fef739189c139693b735c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6275501b662581f067dcb68ab27dd91bb13aadce7126323babb6693c297edcc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e491504119ae62bc66171ef06ef42b93d554b19a66e915d561215fcb9d3b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVolumesSecretItems]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVolumesSecretItems]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVolumesSecretItems]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4fb98f1d588f1c647eb778f156d521222ba50843ed13ce260f2adbb8f8f9d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateVolumesSecretOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVolumesSecretOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65cbaad531eaab8e3dfb9dddbab57030a5f303b3aa7729b1e09eee3e30f80b3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putItems")
    def put_items(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9f77059316034d9f526c07f8e24c5fbaf35b13b62858670c12657cc04c0d6a)
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
    def items(self) -> GoogleCloudRunV2ServiceTemplateVolumesSecretItemsList:
        return typing.cast(GoogleCloudRunV2ServiceTemplateVolumesSecretItemsList, jsii.get(self, "items"))

    @builtins.property
    @jsii.member(jsii_name="defaultModeInput")
    def default_mode_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultModeInput"))

    @builtins.property
    @jsii.member(jsii_name="itemsInput")
    def items_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumesSecretItems]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumesSecretItems]]], jsii.get(self, "itemsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9b047a89391ea03baeb5f1fa64af643e34b1575fa15a7469a7fae504ff8ade5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secret"))

    @secret.setter
    def secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8509517a39948a3bd98401ecbeff99c257b96e5f3c37dc601793c710fd02a5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesSecret]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesSecret], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesSecret],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a177c93aea73a8871beaa6fb886b6123e1a64870437492ec6845d4476e2b8404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVpcAccess",
    jsii_struct_bases=[],
    name_mapping={
        "connector": "connector",
        "egress": "egress",
        "network_interfaces": "networkInterfaces",
    },
)
class GoogleCloudRunV2ServiceTemplateVpcAccess:
    def __init__(
        self,
        *,
        connector: typing.Optional[builtins.str] = None,
        egress: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connector: VPC Access connector name. Format: projects/{project}/locations/{location}/connectors/{connector}, where {project} can be project id or number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#connector GoogleCloudRunV2Service#connector}
        :param egress: Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#egress GoogleCloudRunV2Service#egress}
        :param network_interfaces: network_interfaces block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#network_interfaces GoogleCloudRunV2Service#network_interfaces}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88845b8aff8ce8c286e0cf2aae786f1bfa67389b40f7210ddc8eb5e6c75f0a13)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#connector GoogleCloudRunV2Service#connector}
        '''
        result = self._values.get("connector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def egress(self) -> typing.Optional[builtins.str]:
        '''Traffic VPC egress settings. Possible values: ["ALL_TRAFFIC", "PRIVATE_RANGES_ONLY"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#egress GoogleCloudRunV2Service#egress}
        '''
        result = self._values.get("egress")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces"]]]:
        '''network_interfaces block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#network_interfaces GoogleCloudRunV2Service#network_interfaces}
        '''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVpcAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={"network": "network", "subnetwork": "subnetwork", "tags": "tags"},
)
class GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces:
    def __init__(
        self,
        *,
        network: typing.Optional[builtins.str] = None,
        subnetwork: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param network: The VPC network that the Cloud Run resource will be able to send traffic to. At least one of network or subnetwork must be specified. If both network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If network is not specified, it will be looked up from the subnetwork. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#network GoogleCloudRunV2Service#network}
        :param subnetwork: The VPC subnetwork that the Cloud Run resource will get IPs from. At least one of network or subnetwork must be specified. If both network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If subnetwork is not specified, the subnetwork with the same name with the network will be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#subnetwork GoogleCloudRunV2Service#subnetwork}
        :param tags: Network tags applied to this Cloud Run service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tags GoogleCloudRunV2Service#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a3af53fc971a66530b652c6752c923b69eec67de9c43bb62535fafe3a0793f3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#network GoogleCloudRunV2Service#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnetwork(self) -> typing.Optional[builtins.str]:
        '''The VPC subnetwork that the Cloud Run resource will get IPs from.

        At least one of network or subnetwork must be specified. If both
        network and subnetwork are specified, the given VPC subnetwork must belong to the given VPC network. If subnetwork is not specified, the
        subnetwork with the same name with the network will be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#subnetwork GoogleCloudRunV2Service#subnetwork}
        '''
        result = self._values.get("subnetwork")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Network tags applied to this Cloud Run service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tags GoogleCloudRunV2Service#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00949abd09b641d15957365591b755d392881012c548af544751b49f31952f9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43d961a29d4d4ce0f4f4c54d7ceb9d3f0f12f9818b2099b4d9b8c81009e6893)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f261e8e94af27b7506a0bf29c92bb7ddf263941aab758e3b9109d9637a087f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b98bcfe99f46f0161a06f6bd1de0c4ff5e9bb7796802a91f82481c939f27f5ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cdf90f0ba1b8206e4e9b4312e782fbb787c1c30c6ca887105d64d3a1cbec1e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9dbd3a41b5f1c3a9f2a6c0d2e6988b749efb4592eb1c01d532a5f1efa42f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f566dc1c3f5d71d848bc8b818bc500df5281e279eadfbe1f36a05c894c234e82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8908a45ef057195886132225fa96fa87d692b667b8c3ac4f5d0cb453068f95fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetwork")
    def subnetwork(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetwork"))

    @subnetwork.setter
    def subnetwork(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91200eb2e6acf85b346d7ea85a8480680046ec7012e3afcd3330c2dd834e52e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetwork", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39dd7fde1415a86fa992119183087fa15d7cdc658f26ffb89d5d882ad8fab956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41660e7dd6370737ee3fcd7426863620ba51976c3b6201773508af5baf4d2868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTemplateVpcAccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTemplateVpcAccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff29fa2cadbc7cd9c2f9eade03286f864fc7edfa4bb2b7e5227f54f1b703e71e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNetworkInterfaces")
    def put_network_interfaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0b1234412eb7bd33205a31cd25e3394116618c02f9028c8767b7a40cb39dd9)
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
    ) -> GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList:
        return typing.cast(GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList, jsii.get(self, "networkInterfaces"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]], jsii.get(self, "networkInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="connector")
    def connector(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connector"))

    @connector.setter
    def connector(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e111f3e8707dfd70f219b8d162ab637b3590448f84c938e1c4f52c6b70f807e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connector", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="egress")
    def egress(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "egress"))

    @egress.setter
    def egress(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05c7eeef6da3f8da2e7ca63811bda1bbf1067c727f55d228e6163e6abef7b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "egress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTemplateVpcAccess]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTemplateVpcAccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTemplateVpcAccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf21b83b8006a08119bf12f20e7c5818f365bb9c665099d112d3ba8d4697794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTerminalCondition",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudRunV2ServiceTerminalCondition:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTerminalCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTerminalConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTerminalConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e859ddf3fcb42bc0c03bdd55195b5fd39ea4f29bc988d3c8c5e69eae6d317ce7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTerminalConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5506f6aba102d4093e3a1d30c68de7bcee1d6320a1dc765df10bc29694b2755)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTerminalConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1cdb16cb5cd5fe7058e70740ef71dab2235774a433187c7b9fadc567d8e03e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__286b345f0e7dc48ee149ff316ffe1096864205bcac4bca71071cc44f2fcb10e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a700f61ca0889496c6f249d0eea33c0863b4648cdf93fe0aa6d542e4b03a6fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTerminalConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTerminalConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__471c970638c20d8c99cc13a8b0183019a8ad8cc9b25740939e42d7f33510a864)
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
    def internal_value(
        self,
    ) -> typing.Optional[GoogleCloudRunV2ServiceTerminalCondition]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTerminalCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTerminalCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b53f3124061185ae4fd4bdec5a3031bb96a0bd1338a3c95574f8175efe72c2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleCloudRunV2ServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#create GoogleCloudRunV2Service#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#delete GoogleCloudRunV2Service#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#update GoogleCloudRunV2Service#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643087fe7320138e0cf04b2e351f4422fac75a183bb1abdbd1b100008a4bdf27)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#create GoogleCloudRunV2Service#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#delete GoogleCloudRunV2Service#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#update GoogleCloudRunV2Service#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c296edc9972feeedbfbd5cca677230c857183208d51579c1334f85c97b474f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9e58a6bf1bdf895a3b00bee159203fada28fb14be8d4088a4bdbc311a3ba943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d70212d4283b539c412ac789fe2c912467c073fc417024729e71fa7eaa875f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a31dd12a1d7aee336763f4d105d86f5fb4c677fdec30e0b0aa0eb9edad874a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b57d7f7b1a0b7451b2a0f8183d1e72cede43869afe2efead849716b27db32f90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTraffic",
    jsii_struct_bases=[],
    name_mapping={
        "percent": "percent",
        "revision": "revision",
        "tag": "tag",
        "type": "type",
    },
)
class GoogleCloudRunV2ServiceTraffic:
    def __init__(
        self,
        *,
        percent: typing.Optional[jsii.Number] = None,
        revision: typing.Optional[builtins.str] = None,
        tag: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param percent: Specifies percent of the traffic to this Revision. This defaults to zero if unspecified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#percent GoogleCloudRunV2Service#percent}
        :param revision: Revision to which to send this portion of traffic, if traffic allocation is by revision. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#revision GoogleCloudRunV2Service#revision}
        :param tag: Indicates a string to be part of the URI to exclusively reference this target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tag GoogleCloudRunV2Service#tag}
        :param type: The allocation type for this traffic target. Possible values: ["TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST", "TRAFFIC_TARGET_ALLOCATION_TYPE_REVISION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#type GoogleCloudRunV2Service#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985b988927366cda2b9672749e23a5a49d3e0888f4ca97eae5214696b65d3d30)
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
            check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if percent is not None:
            self._values["percent"] = percent
        if revision is not None:
            self._values["revision"] = revision
        if tag is not None:
            self._values["tag"] = tag
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies percent of the traffic to this Revision. This defaults to zero if unspecified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#percent GoogleCloudRunV2Service#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        '''Revision to which to send this portion of traffic, if traffic allocation is by revision.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#revision GoogleCloudRunV2Service#revision}
        '''
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''Indicates a string to be part of the URI to exclusively reference this target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#tag GoogleCloudRunV2Service#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The allocation type for this traffic target. Possible values: ["TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST", "TRAFFIC_TARGET_ALLOCATION_TYPE_REVISION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_cloud_run_v2_service#type GoogleCloudRunV2Service#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTraffic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTrafficList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTrafficList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbc8fd5b0cac799ea4d61407b09156200c860b952ec56d685e71b0fed287af1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTrafficOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96da40b3f9f6e94a81136ffbd9e9f5f0c413352d91c2c1a92e481b427c2be3a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTrafficOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e0962a55e11b301ee20b2a40a6d827ce2227ada3832a3022296e7c8557c167)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5015be70d8997c53e2f1b195436eaac6d0c3fb79acd21d7ddd354ad0c533bd5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98f9b4c4ff05fa906c0da85c30af100866d3588e69cce0fc631bade018f867f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTraffic]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTraffic]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTraffic]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf27a650605cb3734f73d633c418a7d1deb8d7321e24142ec8ad67091e1e36d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTrafficOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTrafficOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8c16b4c4650df70f069ea27592af4265b9a6403698f3e57d50e72e7f76b8a2b)
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

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

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
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__699d74e1ff8b767a6ed9f686fa8972db9db85472e2de2eb81bdb6b189091481a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="revision")
    def revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revision"))

    @revision.setter
    def revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e76472065f3a2f958995e47521d414500cfe23e13abd577d796e1662e43d5ff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "revision", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3531fb43451052f2df5d16a0d76def070b584984bbfc11f3e578a22456b148c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc686da16d497f2bcd42399e0ba68f0fafac4badc2247c9caa64b8b3285c3f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTraffic]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTraffic]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTraffic]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3aee2f761089b0fa538d135a4e1646418ee6613804335b7d8d789b25bbf7600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTrafficStatuses",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleCloudRunV2ServiceTrafficStatuses:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleCloudRunV2ServiceTrafficStatuses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleCloudRunV2ServiceTrafficStatusesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTrafficStatusesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eb9656237d74a4bf2a53e0a61dafab4cba2a4496f01d6c3a4a5401fbdab295c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleCloudRunV2ServiceTrafficStatusesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f1ed82f105370e5717b8af6248a6c585905ffa50f52669227c92c9602cd85a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleCloudRunV2ServiceTrafficStatusesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8233b7d819685727ebf71e1473a362e56c63acda8000d3ee06debfd78cf2a9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6ec566ce0c7e969a28ae800a1d99d7b4158652881a5dbcf96005c593ba09575)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df3d356496c5dcfb7196722d2e07622e9cb89abeec32864a3254feef63517d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleCloudRunV2ServiceTrafficStatusesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleCloudRunV2Service.GoogleCloudRunV2ServiceTrafficStatusesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca1eb5a9fdc01513e0a0f741aa7091d1cbc2163e57006c8d29b1bc1655ea93d3)
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
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GoogleCloudRunV2ServiceTrafficStatuses]:
        return typing.cast(typing.Optional[GoogleCloudRunV2ServiceTrafficStatuses], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleCloudRunV2ServiceTrafficStatuses],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ae2a41534cef94238ce393a633a264a9756a2860979f4de218636644729759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleCloudRunV2Service",
    "GoogleCloudRunV2ServiceBinaryAuthorization",
    "GoogleCloudRunV2ServiceBinaryAuthorizationOutputReference",
    "GoogleCloudRunV2ServiceBuildConfig",
    "GoogleCloudRunV2ServiceBuildConfigOutputReference",
    "GoogleCloudRunV2ServiceConditions",
    "GoogleCloudRunV2ServiceConditionsList",
    "GoogleCloudRunV2ServiceConditionsOutputReference",
    "GoogleCloudRunV2ServiceConfig",
    "GoogleCloudRunV2ServiceScaling",
    "GoogleCloudRunV2ServiceScalingOutputReference",
    "GoogleCloudRunV2ServiceTemplate",
    "GoogleCloudRunV2ServiceTemplateContainers",
    "GoogleCloudRunV2ServiceTemplateContainersBuildInfo",
    "GoogleCloudRunV2ServiceTemplateContainersBuildInfoList",
    "GoogleCloudRunV2ServiceTemplateContainersBuildInfoOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersEnv",
    "GoogleCloudRunV2ServiceTemplateContainersEnvList",
    "GoogleCloudRunV2ServiceTemplateContainersEnvOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersEnvValueSource",
    "GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef",
    "GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRefOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersList",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbe",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpcOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersList",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeadersOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket",
    "GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocketOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersPorts",
    "GoogleCloudRunV2ServiceTemplateContainersPortsOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersResources",
    "GoogleCloudRunV2ServiceTemplateContainersResourcesOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbe",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpcOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersList",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeadersOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket",
    "GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocketOutputReference",
    "GoogleCloudRunV2ServiceTemplateContainersVolumeMounts",
    "GoogleCloudRunV2ServiceTemplateContainersVolumeMountsList",
    "GoogleCloudRunV2ServiceTemplateContainersVolumeMountsOutputReference",
    "GoogleCloudRunV2ServiceTemplateNodeSelector",
    "GoogleCloudRunV2ServiceTemplateNodeSelectorOutputReference",
    "GoogleCloudRunV2ServiceTemplateOutputReference",
    "GoogleCloudRunV2ServiceTemplateScaling",
    "GoogleCloudRunV2ServiceTemplateScalingOutputReference",
    "GoogleCloudRunV2ServiceTemplateServiceMesh",
    "GoogleCloudRunV2ServiceTemplateServiceMeshOutputReference",
    "GoogleCloudRunV2ServiceTemplateVolumes",
    "GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance",
    "GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstanceOutputReference",
    "GoogleCloudRunV2ServiceTemplateVolumesEmptyDir",
    "GoogleCloudRunV2ServiceTemplateVolumesEmptyDirOutputReference",
    "GoogleCloudRunV2ServiceTemplateVolumesGcs",
    "GoogleCloudRunV2ServiceTemplateVolumesGcsOutputReference",
    "GoogleCloudRunV2ServiceTemplateVolumesList",
    "GoogleCloudRunV2ServiceTemplateVolumesNfs",
    "GoogleCloudRunV2ServiceTemplateVolumesNfsOutputReference",
    "GoogleCloudRunV2ServiceTemplateVolumesOutputReference",
    "GoogleCloudRunV2ServiceTemplateVolumesSecret",
    "GoogleCloudRunV2ServiceTemplateVolumesSecretItems",
    "GoogleCloudRunV2ServiceTemplateVolumesSecretItemsList",
    "GoogleCloudRunV2ServiceTemplateVolumesSecretItemsOutputReference",
    "GoogleCloudRunV2ServiceTemplateVolumesSecretOutputReference",
    "GoogleCloudRunV2ServiceTemplateVpcAccess",
    "GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces",
    "GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesList",
    "GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfacesOutputReference",
    "GoogleCloudRunV2ServiceTemplateVpcAccessOutputReference",
    "GoogleCloudRunV2ServiceTerminalCondition",
    "GoogleCloudRunV2ServiceTerminalConditionList",
    "GoogleCloudRunV2ServiceTerminalConditionOutputReference",
    "GoogleCloudRunV2ServiceTimeouts",
    "GoogleCloudRunV2ServiceTimeoutsOutputReference",
    "GoogleCloudRunV2ServiceTraffic",
    "GoogleCloudRunV2ServiceTrafficList",
    "GoogleCloudRunV2ServiceTrafficOutputReference",
    "GoogleCloudRunV2ServiceTrafficStatuses",
    "GoogleCloudRunV2ServiceTrafficStatusesList",
    "GoogleCloudRunV2ServiceTrafficStatusesOutputReference",
]

publication.publish()

def _typecheckingstub__da3f94b63656d4c1b629fea2a6c5c4ba6acf26b0325b584589b994fe33db59e4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    template: typing.Union[GoogleCloudRunV2ServiceTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[GoogleCloudRunV2ServiceBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    build_config: typing.Optional[typing.Union[GoogleCloudRunV2ServiceBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    client_version: typing.Optional[builtins.str] = None,
    custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_uri_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    iap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ingress: typing.Optional[builtins.str] = None,
    invoker_iam_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_stage: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[GoogleCloudRunV2ServiceScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTraffic, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__1641a1de9b4f13ebc0bb48e8f6809beed349b2352da3afcb4dd2e76c9cd790c9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df50b46406afc889a4c6965cd49c52ffb107bd2e5be3b2e05894c6e72b698e7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTraffic, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd68dfcf7915c4b4b1ecfe51bb22d3305b46f8a304aeab203212c3d99afce31(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5a71e0072df047656fdf667d3606d1e18c5e80412e0e168a1333322b70eedb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f614ab3d5145d8f2e2e71c5e1adce367dd72fd64d82cc82c3427c06ee39f7669(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d4085c8e5763017ca36e3341a4a483d91c045d2ad43a2d026a7d6a29b645e7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3051e3ea5223aded6e4324e8fa04b02d82c1fc03d2e5bae2b689b2194f1d3a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f174c6db38a1823941800c0b7656a5aacc852c1860e7251f5ccb8e74ce8d0d7c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020b719a3aa31afbdf3cbd1e8e4803cb441c4f95bde5d5594f0bd5e531793c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae2ab9e9f4df240bcd887da88d013482184c0623a1d4d375a981db7dce5d167(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c454104d79a7e2f8c5bbfbe86f12ff2d9af7e9785a315a7a5d8c7326472073(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d899dc672b624c6bb7a9cae547cf5332bfb9e7bdb22850efdbd826fa1686cf0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d498d2621ab9a16ba3b8dec4230df07a4b0f53e1aefcaa66c2105296643fb7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0e1631217d5b77ccd2cf8862598fc9c3606c426a602067f22ebb053ee536d1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60194e64e91030b0de7bc09e9b946fa7d0ca5596b269cdce7dd3119bfb4ba43d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83646107c613ffdc69d303fef4624716c1cd69f5226d809bfa3b0d66284bd3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91cdd09c7b40cab478b04fb072e2f30542a689c36ef9f95677d79c432426a69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba234e5b7954faffd73830483c055a6c67051940d7f0a789e8aa5812a8cf52a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9ee5eeefd2186f348b8da7e4bf265e96778ac3b4c7399bdd536fbfc5a271c04(
    *,
    breakglass_justification: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    use_default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dbe204ff68209651cc722084d90169386dd379bbdad9e295fa4902e9d96daf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbd169a61ed79ec013738cf5147d97ca8269193778a45eab1ed38ebd0e53e17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d5ddb4c6f3b0e5dbdffe95050c3842cd6e14cf54277c13fa59dd3732871a11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efbd9f522b9349f77e093c590d7fd15ef315491d0f1d9181df92178e1c5ddeb9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadbf393b6b6fc977e043a73298ac5caefd3f17b484a8c3176e4c675321cd4d1(
    value: typing.Optional[GoogleCloudRunV2ServiceBinaryAuthorization],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38755c466d623b4a096822fb9a1eb9a0f6ed56c5a21468a9477683ec238f6eb8(
    *,
    base_image: typing.Optional[builtins.str] = None,
    enable_automatic_updates: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    function_target: typing.Optional[builtins.str] = None,
    image_uri: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    source_location: typing.Optional[builtins.str] = None,
    worker_pool: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0586a1f6e51da94ff218d55dc3cf4eaa0644d473684e3e59cafe970687ffcc8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74a9961d0c122ff5abe2181616581476ea20b2541fea9852d6ecc13aa63945e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85ab1978267c1011dc601b7db27f14c257022cac7844f9bc801d62be105d8e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c1b83a64e38332163f2edc8c76cc2094f4e95982d60560c26864f71a3edf2d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c295ed5924b0291ccdb678068b0ae5419683544578bfe5ea651abef7e7676b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16957a9b191d72002a55a8910ad73a49b91492ca42bdfe6d6a7d6f89b52998cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead10a242ecd667f4fda1330d33fef307468b5b76dbc3cfb0810f115bdb263e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644c62210d82a9105a946d1ea0d76567dbd2fcb67fa98d952e97ee5bbd8a9309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4c18b8241937db7f80497225ed8a2f8d1ccda50464ce6a8fa40e7ec97f86b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa6629b69aa165b43204dec7a7a9206a9a3129bb01946167c589e05b76b0a77(
    value: typing.Optional[GoogleCloudRunV2ServiceBuildConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3ef785fba42b4000fce1388db0d17f005a94a55101b4af0f08648f63a00977(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea541c7ce54c296dd60072af08b0737558a24a312d2a4c2a40623b4d31de9b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b504cfd9ded8696b97b39a219b1146587c904291d864fa1b74cf91a90c41e19e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fd7ce7e86301b0ad7ec0a4d2d174313b1af4409091f38f9144794b343273cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c309859202d0f152fda825d0f22dc633ab418599677aa9bc3eb99efcea60cdb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2b87b51e563b692d36945af4877314b659a4324629f562ffbbe9055e208905(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b497e9961d0d735dffd2e070dbc4dccba637f0187b2524beb76d979b7957ffd(
    value: typing.Optional[GoogleCloudRunV2ServiceConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec22f99db982f16e6413ec5ff0ae621810b21b17f2a8220d37334b4f16c1bf78(
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
    template: typing.Union[GoogleCloudRunV2ServiceTemplate, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    binary_authorization: typing.Optional[typing.Union[GoogleCloudRunV2ServiceBinaryAuthorization, typing.Dict[builtins.str, typing.Any]]] = None,
    build_config: typing.Optional[typing.Union[GoogleCloudRunV2ServiceBuildConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    client: typing.Optional[builtins.str] = None,
    client_version: typing.Optional[builtins.str] = None,
    custom_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_uri_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    iap_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    ingress: typing.Optional[builtins.str] = None,
    invoker_iam_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    launch_stage: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[GoogleCloudRunV2ServiceScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTraffic, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085dfdb45f7f09b3169b6952d35bad2421a5979cf2ded6b21c6869bd4be2e79f(
    *,
    manual_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
    scaling_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719fba8de1beb3f671156aa22eae591f81fed1f90d4bb27007a8221b7c76dfb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ae5c616868732d44ffe62ccc55b64ce7919a8c531a6959828a439b9edd1620(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532adff6ee96c1994159a5f18983b0d4656941957dacda45b9660ce582cb1cb7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb6e4442c3d353d244ca1e6b2deae608a3dd46a46a7062334677f38f548ea1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e676532ba80a1ea091c797d3132d45f8ebcd0637b7bfc1beae7c7645461c3b(
    value: typing.Optional[GoogleCloudRunV2ServiceScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5633739d4db407b6ba3492871adba693e751f919329bbe3ce0af405d5da869d(
    *,
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    containers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    execution_environment: typing.Optional[builtins.str] = None,
    gpu_zonal_redundancy_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_instance_request_concurrency: typing.Optional[jsii.Number] = None,
    node_selector: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateNodeSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    revision: typing.Optional[builtins.str] = None,
    scaling: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    service_account: typing.Optional[builtins.str] = None,
    service_mesh: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateServiceMesh, typing.Dict[builtins.str, typing.Any]]] = None,
    session_affinity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateVolumes, typing.Dict[builtins.str, typing.Any]]]]] = None,
    vpc_access: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateVpcAccess, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76a72e168b6fb360869f2a2dff92a42470af5f28f60b95e50bf3ab39afca516(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    base_image_uri: typing.Optional[builtins.str] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]]] = None,
    liveness_probe: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersPorts, typing.Dict[builtins.str, typing.Any]]] = None,
    resources: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersResources, typing.Dict[builtins.str, typing.Any]]] = None,
    startup_probe: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersStartupProbe, typing.Dict[builtins.str, typing.Any]]] = None,
    volume_mounts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    working_dir: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04ef4beee98b5dda7c3e53302a6182096a7c23ca39f7cad23ed12f352efb8e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74a319f96ffe3c09fba7f680d528d3250fc0bac8b05c469b318040dfd7add8a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe33fabbe9ce44ed0b70feff7a65ff27cc19f67acfa20e4c3793f4a0c8fb477(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58d4bc15032953b66662f39487fecf7bcbf92b1fd0f9304ba7c9283c0814d77(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6247b367ee8e2a1c9685edba1bb7e48adfeb6f939e85c576d6b6f24b1313b191(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5e8efc1b32482d2306a07a318a822809a795b3144bd2f9f12ab2bebc0bcc2a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3f838303dac58e2b91d58e9c18cdfed0e037f606723acda21097062beea17d(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersBuildInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__765037831f8c94469ce5b6176eba646fc3fb5f62c5094cdc020d3be60033240c(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
    value_source: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersEnvValueSource, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92930110d5a67b032de4a8c6ee70ab5b6f4963f859e8c0cd627daa087496cdbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743bc010270b72189e62e0e63b5222d9c78edaed6c84635159932c4d4c202703(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f878dcd07068d31579b08effc577f64678524a7115087c97ac127f30ac5137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0326218d09050c8fc0151c0417211653e21defec4c0824b315532ccedb9686(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d617caf40c9ab07ffcae8255522307c95d1e04ef16432532b10f36553030b371(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbdb0bfda7d512db6bbc6079d6de3ce0d5274445a4afbe81b5018efac5a1229(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersEnv]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a8614dbd73f260d72309dc284364edcc40c7f7849795aef05573b033597aaf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d0dac26c8e5d6484206569d49d87786aca9ecbaf7db064ba972b376a9487e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a00ba23592da6addf905e0280182f49cdf351b056990fc758bdcc6a9b4a9ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730720ee8936f6dfb9f7044b5ceb499b5d220b371e7f349863a9fbb8d686a2ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersEnv]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066e2dbfa2f343347cf085817d11f36ea386487fe58079645310c4558a0157ca(
    *,
    secret_key_ref: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58a67a2b532d7841b32ea5a944975b12ff4b51c5546dd5eb70eb7ff61172245c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939603c43d2f821907be56ae6c1d79ab4476560e017c560128138b22c4678c73(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersEnvValueSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6bc0d2d1e8c59607a107d6570be76e16dc3b294c695499c0becd1c8f062711(
    *,
    secret: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c78f6d9fbe89cc3a44c754a8ffc6bda476eab9a582b86ca42e07f2646932b8d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d192dba23fa30b7f8429133185e04c125908563c94d861ef3088c15c4fe6ab5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79fca087f9a31097937d8095afc15b3925340a970ed442872ad4de5aa5d7752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cea31e0b831d58cdbe4e7148cd37dca9ce583850d2b4844adb4ad441107eb17(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersEnvValueSourceSecretKeyRef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f825a6278fc2aea3ac8226dafb54267b8b9c9606972f5aa51c94b6be1930991(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ac81de8fec851957ea2bbacb76a76d56915fed0d0b997467d5b8089aaf20f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e090c86956da77f94b04492bb2f4b1681deb77d50c5c1247f6b6852a529156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9e464b03b3f754d555f4d8798b2ca5f2bed08fc6517ab0a0b042383c759306(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cc7a853302d999f8862992158f8704d7f02ac9dee8a420c84d34de38066030(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef7eca6cee376eed0cd6157c05d31260eee68659e2dc12fd5858cbdaec63ed2f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a122105687fffb31a228f477735e9131b59185fe7944c0e204acb6ef87a33b5(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d136a6daa38a55481b05e524cddd3f094cb45a2d7b524eecd637dc125f296aad(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c5d0696b83fc08b269341d20f698b8a2e28deb1496fd860581f2da074a574c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb187ac96f242187f1d7fc9f8a0c378101302c659348469062968bd562ead27(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934db6863d273cd4b838cd67b8331bfeb34c07d22b65db546ca9052e7d9986d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db47f2237411ff46892587e8d3eae9490e6288927ab706828d6866c1f1129ec(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade39985521df5ad4a9976489b08c9a5be1c3d0088350c6c8d999d8d4300a0cb(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357f4e74f1f684136d4c93da49994927d1f12374f1285752ad8c7136b7fc43be(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5f7383d2a6fe8c5b003ae6f06fb0e8abc2736c07c9105282f1e638feaf8dc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c83faaffeab143b6967cf8dec1afa86044e239f693c459efc87378a37e5c798(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39da5f6fb9c0f6227a6342844000f363ef429af951ef5dd676ab162448fca3ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2ec471aba67460e89a78b2dd217ec6902b57db914e49242b6a59c1dcd9a92f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbd1278cafc7fae84f7a07a9eedb6100b9adcf832b9088880848da6b65e040d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de82d0dd58c1fb62b61a1d8992d547131ef2c45f3f92d1035af75f4fa196ab7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507ee2f52e308782130fcc085199966e8c425a0b298ee4ca71dcff6e1c171a4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed44409980ec327c869b68ece42131b70800f333bb458688b0c8a2e222e99a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb81154a3230f35a85fd4cd8c7582add39556a42bdbec9bfb287f55821e027e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a3cb2aae730ec3dd57dc7992861ef618701b0f823e49f6c7d804e04638384b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8c8e7cd203628468e44acdeca6906e3c915bacbd92ede24f3e8cb45087cc6fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066ab0ebaf2df2c83f0816490a4aad21dd9433d8d703636ea225716f934cab67(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821af3fe71a7b3a93327e9fe5192d71dd0fa09c074fc21484d9f30fb1b31e40a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03b88aac7a40d9772a55bef5d7795f504ed74ed5bd2440d9dd6c65ec1870c75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c84720e99906176f2f55ac5b7e48704c2d6944415603de27e3f790b19695598(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9dcaef0f32e7f14a9ecde162f2316868c5e77c32f261232933ddf892a76910c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa95043aa9a8e2fd8c39d47648b94adad65ea66b51b357547f2ab8803fdc9ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__805236cb7dc2ae256fe892c26c62c43457667f0b5d73e79e99f8b1179278b760(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40feae15c472e26ff2da59f7c893a87f56a740ea9278f0ae02d3c46d379bf472(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710ada82185dc578eab2842ab11982b5be6861989696ec2b189e0ef99e4d7014(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae19a176eb45232a66e480fbc6075240bbb94cba4b2c943045040f535c20bdf(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b87cd830581d1ff85a5f95c4c2cbbcffa098131767805fd21c2b16ac6b002e6(
    *,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b407a329332d7b8bbe85fd3c57584bb1945b5c9f1bbff632ceb50ad65274eff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f035ed62c0e7ca2ccdcb53a1dbafb486331458ba631182150ec49c49b2f7d18(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d16c38d4cfd10a72ba614df47b268559580c481df6c2d15e992b63dcde99c98(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersLivenessProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164af89b3abd2d2cbded78a4c1827c8144c2101072668a46279a04a71c28ddf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88470c15e9356673963755e232bed9e90b217f8d44d6815cc979fae8b23685e3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersEnv, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fadf0d96458ba7dba2318dd12425011fdbb8e5f89351a343d7f39f101f2829(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersVolumeMounts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1382ff9463f208fc8e0927ce9dce7accaf88ce915f96aa498129c3ff0da823ec(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4409c69e1cae58ca2e406ea82b98b3fac82792b438e1f02c284119786bb7ceb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53de62486ed0b6734deefbbf4766532414cb53d651787a539516f8a230a9f54(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d61c76e249474782c86826b2dee84a7c01c84b84ae21ffe33e1926553f00868(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d3856cf057186ce9386dffdb035b13cb009edf46a8fa484e2d5c4cebdad889(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446b9abbc5878431f15c4f1a3b31162af0c88258a8f665c3b9f78bc3b974b070(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b7325e69792ed5db0719868e069e8e8106b903aa0d07369229f452f0bc425d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413903c6827fab1e6e5fc57c066cc5887a19b1fa2fc816e229a57f10e0a34fd4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9709001868c215bb3b946b31fd1676bc3b050304995d8638bb112764bc668f0a(
    *,
    container_port: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2cae07ed12c26a40c6c2cff7883af0a85fbf80d61287798997632b6c2f5101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c15f4ee17597826d32cc78b93550b7351242bebf438ead71282710804300250(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010a3e173bdf3e583ee6456301cafc4ede9bfa1db0880972c297311e9baf16f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c06681ebbbb59d49d15d79c6bdf758ae3e6e4603e25a6bea7e4d06f45b561b1(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersPorts],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a176bb0a0755ed5f290188d5ac6530ea8cfb9f55f0da36eb3c85d355498bb94a(
    *,
    cpu_idle: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    limits: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    startup_cpu_boost: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8602ee11822ba69157cd399bb4203efb766471a14ad979c673a2ce548e75603(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225ddccc6484d7259f7492b6f31469302a0f8cc3ebe736c49a7929ec5dc3e87d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f14072e7768e99730b9bbd8d2371cf2c36e0f2fb92cb879c1f900c1c0a3c94(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9e1b166fefd87159a7e76416d418b6fd2b5a4d4b790aa0d42bd08bc2fb2ad0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beddeeecfd90ed57b36fbdd85a9585b5a08c989e0dfbaddcb0355e31c5c6ba94(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1435204ced9fb5b0813a6fc3a39c8de10addea0d512b91cc7a59215c01c39bde(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    grpc: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc, typing.Dict[builtins.str, typing.Any]]] = None,
    http_get: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet, typing.Dict[builtins.str, typing.Any]]] = None,
    initial_delay_seconds: typing.Optional[jsii.Number] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    tcp_socket: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__127403790533d49a3a2402c4bb764e7f9e4a821fe473a2a8fd41bd627af7b343(
    *,
    port: typing.Optional[jsii.Number] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f7b1d3339c07936414f787113fcb8a37fc82cd2b39d1fd8d5e6b12ca59d51b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba579e5fced8f62353ece194a0957de005c5540cb4230164731a61ec055dbd6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31ace03317284a2a1655657696f9ea018fb21a3676b143cbafcefe994a303f46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399907a806b3ec0fa71ab601babaacea5697bd49ae2eb1401aa0594cbea720d4(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeGrpc],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__473d22932bec0452abc27340ac4c70748cf0e82497f2b70628e11a52546461e2(
    *,
    http_headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8eb1e353a9264b66b02283f36065e942a44f796c8155b9675b8c435a404aa48(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0b126ef124256242fae2a0de76cb010fcf0ecd2a49d0b85ca0dc0753346441(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee6bc45b5df36e631d7e9621a713650a9186c94cd45bb7f6bedee37a6a0687d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9680f7cfd6373c85f6c547e7ad4cbf50417a2e893c46115140a4c6bc7320a317(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e89f91cc8631f4e7e3132724904d8dc092efcd13b60bc45c4f7d09c72c15c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36ca945eff150a6620f43aa284b171881c849bb8563f83e246524dacb2dc9c2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbab00c4242950851c66fccdd3f408d35ff7151f34987e2e36b6706667647f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7deb6c8caae64c5d357aa9973cc36e3089e28be01006a8f40b5c3772df3ee2af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b2f088328dd30d38a7afc79e8e3d44c7e95745c3120ee928ea11845325a9bda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4461bc80ea9e7d5087a554aff277de107052b2d660bf91ec3958e10d300bfd5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7323ca1662f481ac2e64397a7068243f5db94d6318bd8c2711867c320230b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad92ad6d7d1dc6a02e0e1b68007a9651928d0c21029f99dc21f5e02a8c3a9946(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629688d2472a4cd6c5d054b825b006195498eaabeb3448477f1821a4ed097519(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGetHttpHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c48f54f0b9a1087c68f51a0309debb0ed99cc5defe1f0633270e7910cdaef8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9633cab1e2e744153fca340ae3bd5071eebfa98f8df57d7e512d23f4c449fbed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdda7fb9e056e43ce670c4897698e0ccbfa3170e445f4eda24c0d34a309084e0(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeHttpGet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966e7fb7448857bc39e96d03c2988e976f14ba0971261f21b21f29b5454f36c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28e651e0cfba66e3b1bff5d96dd1c9e39f506cf595e705abb08b9df35f2972d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b526a9abe473c7d75f44827211104b00029f4844490226e536028a542e102dfc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e55f12b7b0f5aeee7e373455abb9c422f11d4c899b7d825a3154cefe92b0d2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ec1f3d89b1f929d6f9caf497022af11fc4eec112d1cf31b39e70d547b3576c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056fcf20a80a6f7905a13e6c3785c5bb67815c3604e650d44fbf98edbc817fdb(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbe],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b78293ddf915c3c892d2b98a92343daaf4f6bf30e7b6b8f364aa80b9ae4b0f4(
    *,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a7a07f38527ed340f53d0e3ced71896cec1e378983ca527344f2f78485d9a06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea143c80a97f15afbfb670f4cb27e6e62dda339498ab271db874fe74e25ab651(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41495a01fca52a513f32053407b2e3e1d5bec22923594b259e6d002e54ccca59(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateContainersStartupProbeTcpSocket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64cdb074c5c0d0c8582f12d8a1e040e75313bdaa925ac9bd59bf365ee8edeb8b(
    *,
    mount_path: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212b3b736d15212730a662fe252504d261d052b565939718e623f3f01bcc6a82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ae1a84c0f44d670f3d14a8dc06274bd5d9b92758e2c13048f1078af6054f8c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3213c7caf20745851ae26312ba4bf94f639e7a9612a5dcc98b66ebaf345a476e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b2570760086ae8989f23048b81d3cc3f3707d22f42836b4e11e0e3193ec244(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244afa223c1a8143a5446a845004376b71f00a3460ecf73482c894437bdada88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f87e28b82b38bef83a4fc1093a52d8166f880fa4446def19527c0c75416136d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateContainersVolumeMounts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a486f6f142637eca38432276f691b3f7a4ad0b106090e1290ad072093e38406c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b372a269de7a8ebfb7b96237460d845ed0ed409b228a570355c86d65301a24c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fccc7286a1c211e551601bee91943a022e66f2440ec9cdd49123a0e7eddb7a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010e1ec998968833092e1b7475e91c70fa1f6151bf965a24d88f9301903d55d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateContainersVolumeMounts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac7ca347a2a676eb2e943f196c4191325acfce581e2754e7a2ab59c2e5f5eb6(
    *,
    accelerator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5390ab33c9cdf381b4dec3d1451cbf319ee6fc8b21ac788ee0c1dd2d94b09891(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccee3cecd7947d516abccdbdaa0435472da36acca78bdaa7b58d7078426ec50f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e97148825912bd58d85c2c57b43233e385772c095d413f0bd5b51675ac39de(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateNodeSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2d7832816d889ed848674530f2eee413a691add66dccc81d32154e851e26f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c7c567ad3efc3c6bda8dd749f2666e31f858eada0ea6a6a8f55d37070931e2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateContainers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4baadf5a84d267eb07992ea93554fb86ee1fda972184aac9befe5125e57e9359(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateVolumes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9867771fccee7549992bb45b142e6a17041b3cf2ee0bf8c106cd978a88b3e8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4853f7dfa84750e2b923c13214a59d6fb9e13c2f6551de00f27e373e40637112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383e18d2d3e849af4f17998cfe416fa9660608969f57e4696c70b10dfd144193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acd93d70611f5eaa163e3f958e9e150255e63cb91b4df94c16ead68a6bb1d3b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6e84db4c84433091ffc9fb13301ebfec25df8bd8e2a8e391f4ff4017df33c3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5f69efcefb4e7050d49b9a084bda1c47498b64e622c5bd26e1054c4830d2a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e5a9df9dcc05fe031fb6eb15accbc83c032cd631b04c286504dd0869535ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e848062a97e267c3e8854ff05d135256824edc1e96351dbc16cf8dd4f2398b19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cd94552253ea4b4a7f35db1164915d461dfdceeb8d486429c249c09d23bd23(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a882a09fadb649e59f2433178131b0859abc83295769db98c0f8aae9905365(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f530c3fb29adb552e1f7104e52c3fd3f81160c409a222d78d9a95750a9791ba(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7652748c35392c2910afa2118d854e0d4aa31344e8ff898031a7610f664a6081(
    *,
    max_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe851cdbb2e7ca3bcbc452276e47babab19aff68fe7676dfcea5f8bd02a181e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c09c936b9843ade074677f50b3855982d162930ea261a7a39023523d3ad41aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdb503e28ed141a683341227a9ca41630b9f557e544482c9c3d04403a81fb44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef7167b7dfad451c0f182ba97b272bb80991b25418a9adabb767f38e28a5236(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db25562cd4aad377dbd0f769f49c4613b1cb1b0c86d28af990cc831c9f9e45dd(
    *,
    mesh: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130bf8434a19f491b4893ba92f978a890173df6adcd69507afbe7ecf22d8a324(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b4d01e5284fe3ce27e26ddc1fc80e33db4deb57d8c3512912c13088f2d6545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ad3f0708edfbb81d2cc10bf9afa4cc4dac815cbd45ad60f3f84e95cb69dd28(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateServiceMesh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a37fc8cde2344446bf7b6b15a9de46a0f6d82357940ea083ea3376aa36a195(
    *,
    name: builtins.str,
    cloud_sql_instance: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance, typing.Dict[builtins.str, typing.Any]]] = None,
    empty_dir: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateVolumesEmptyDir, typing.Dict[builtins.str, typing.Any]]] = None,
    gcs: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateVolumesGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    nfs: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateVolumesNfs, typing.Dict[builtins.str, typing.Any]]] = None,
    secret: typing.Optional[typing.Union[GoogleCloudRunV2ServiceTemplateVolumesSecret, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d3c77999ae9ea213f032cf54069d9bfb15848925fb4acd1064d19472a75494(
    *,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f20ee5cba4520762bbe88f31933911412fbc2a39a4822c73f6bb20f72fd53833(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67cf2f5ecafb006f4a4e1b24a51fb5a655c85994e2a02b37bed5057c8dca438b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b8d5a037886bb91892227a087a0c1cc111808e5697325709c915562106657e7(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesCloudSqlInstance],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e63deec4188b2112489ec70ff1a0a227c611d4fc30d9ec52b1088cc83b7f89(
    *,
    medium: typing.Optional[builtins.str] = None,
    size_limit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159ff4ee399e59d6ab4e05c45927814687b5b360dd14cd0f45f7d040aec26949(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d967e7390e871593ca41f29af0a049c6ed882684f152ffb5d6b81a81958b37f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7b3976086fdc700a3ca5693f7a374723bca4abf0e378c4ab81590d68a2970a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f415843a59c858ccce4d64957f6114cf31a5ef68b7ae63199a1407be11c9a5(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesEmptyDir],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3047b64510cde95cc6010a61b8309364c6a06e621204cee2f304658b9173ba(
    *,
    bucket: builtins.str,
    mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7d77895488604cf7f7d49f8e58b796fe9ec3085322e38a28e6387c6b01589c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc07109214a8ce81ca8a7e3f23cf556638b8440c79a865e951d6a2eeeb9c6ce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a504a44a9650a4ee87b8e10e20ba8b464b034e4d1add06d29c89ae8855d24314(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0141690ec1f400d4032aa0c1cd1ddc825fa8c4e03173f5b67bf1b43cdd9e65f5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fcd3a0727d88d0535eb7881cfd9dabeb2c77ab491564c70f041425f585434a(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2ac3092311887745c654f0e399796caf5fa4ccf59afd8d2fe2cdfa646fcd68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b008a61b3118692bf2f2d99339b6390033b838646c46a156e35e9d3287b67e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ff8c9868bf0303b1be664222812a55be3495711df324dfdce12abed1c00696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bebbf71340b40fe02bdd91c2be7ee90ae437e91a1bd1457bf2d4b4e2a9c89c1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca847b291d22d4913f8463b50029b590aea059a05b40b400f507ee2b83ace580(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1748426832276794eb8c2896bbf38fabd234b1ace8bee4545767d6f32aafc1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c5846f8fb0277692947a23a93ae3a4c9d5fe979cd5a4055c49181228bbf1a6(
    *,
    path: builtins.str,
    server: builtins.str,
    read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__605955e0f72323027f1754503789a48198d016aab9046903a99cc7eec26e1936(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16bdd5782b86a227ac96d40275e5e6552df7b266a002befa57673608243a1486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a1631b9e36464f0a124bb8a4fdd9734ccd5110f6f3459fcbf0765ae44d3dc03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a379941ba07c7d9743a1e66d8af12f60d97ec1ce696aaa2b8391afc4c9745e0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c308a7c43a6349de172eb77aa30dd3ca0f2eb8089c284b37d931223c711b5613(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesNfs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d15b3cf5047b7ee34e8f52548099effadff6a035759d9a8b5772979080d4e2e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660d7d4e6fdda5946e6f918e530cce1bc165354190f1a63ba932cf0298c8ddf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde469ee88d1886d776d5ce0808ebf16733b12bc1e85e7bb3c2c8b6846f7aa0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVolumes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f61bf26e62188aac61e3d39d4ed88eb87c22561423d94eb769871a5ad0132f6(
    *,
    secret: builtins.str,
    default_mode: typing.Optional[jsii.Number] = None,
    items: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf71c7a55b91c82c807522a274294475db22a1dc6ed4dd317a5872d71087099a(
    *,
    path: builtins.str,
    mode: typing.Optional[jsii.Number] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0648728f6b1aba5fafb60fe37b358c1e2f71ed12057341822892239f96af3b07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e056ca3192c0690db537735df0d787212d0cfa92e68fd9fd34eab477e016df5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33fdcfda4ab7b7c6e6398b09af3ea83cdcf50419b73faa90a34e9147dbebd21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e86821068664f7b232c385acb453d6926fe0a0037e95c4e2c2f556baa75a866(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2e52257a5b7544951f721b40ec87dc3d96b06d060ce8a5ea72934edb87a664(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d966137dce1e8158851b6f292d9c4214651b8f35fed8436a0fcaefa97adfcb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVolumesSecretItems]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ae21b41e5cf25bf78adad44fe2fdc95ccf0dfa1cd5153c23042eaad5c80646(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff56e5d023ecd133fb9de549898775e59ef5a0372fef739189c139693b735c0c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6275501b662581f067dcb68ab27dd91bb13aadce7126323babb6693c297edcc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e491504119ae62bc66171ef06ef42b93d554b19a66e915d561215fcb9d3b2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fb98f1d588f1c647eb778f156d521222ba50843ed13ce260f2adbb8f8f9d77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVolumesSecretItems]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cbaad531eaab8e3dfb9dddbab57030a5f303b3aa7729b1e09eee3e30f80b3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9f77059316034d9f526c07f8e24c5fbaf35b13b62858670c12657cc04c0d6a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateVolumesSecretItems, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b047a89391ea03baeb5f1fa64af643e34b1575fa15a7469a7fae504ff8ade5b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8509517a39948a3bd98401ecbeff99c257b96e5f3c37dc601793c710fd02a5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a177c93aea73a8871beaa6fb886b6123e1a64870437492ec6845d4476e2b8404(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateVolumesSecret],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88845b8aff8ce8c286e0cf2aae786f1bfa67389b40f7210ddc8eb5e6c75f0a13(
    *,
    connector: typing.Optional[builtins.str] = None,
    egress: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3af53fc971a66530b652c6752c923b69eec67de9c43bb62535fafe3a0793f3(
    *,
    network: typing.Optional[builtins.str] = None,
    subnetwork: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00949abd09b641d15957365591b755d392881012c548af544751b49f31952f9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43d961a29d4d4ce0f4f4c54d7ceb9d3f0f12f9818b2099b4d9b8c81009e6893(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f261e8e94af27b7506a0bf29c92bb7ddf263941aab758e3b9109d9637a087f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98bcfe99f46f0161a06f6bd1de0c4ff5e9bb7796802a91f82481c939f27f5ee(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdf90f0ba1b8206e4e9b4312e782fbb787c1c30c6ca887105d64d3a1cbec1e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9dbd3a41b5f1c3a9f2a6c0d2e6988b749efb4592eb1c01d532a5f1efa42f71(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f566dc1c3f5d71d848bc8b818bc500df5281e279eadfbe1f36a05c894c234e82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8908a45ef057195886132225fa96fa87d692b667b8c3ac4f5d0cb453068f95fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91200eb2e6acf85b346d7ea85a8480680046ec7012e3afcd3330c2dd834e52e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39dd7fde1415a86fa992119183087fa15d7cdc658f26ffb89d5d882ad8fab956(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41660e7dd6370737ee3fcd7426863620ba51976c3b6201773508af5baf4d2868(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff29fa2cadbc7cd9c2f9eade03286f864fc7edfa4bb2b7e5227f54f1b703e71e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0b1234412eb7bd33205a31cd25e3394116618c02f9028c8767b7a40cb39dd9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleCloudRunV2ServiceTemplateVpcAccessNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e111f3e8707dfd70f219b8d162ab637b3590448f84c938e1c4f52c6b70f807e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05c7eeef6da3f8da2e7ca63811bda1bbf1067c727f55d228e6163e6abef7b0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf21b83b8006a08119bf12f20e7c5818f365bb9c665099d112d3ba8d4697794(
    value: typing.Optional[GoogleCloudRunV2ServiceTemplateVpcAccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e859ddf3fcb42bc0c03bdd55195b5fd39ea4f29bc988d3c8c5e69eae6d317ce7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5506f6aba102d4093e3a1d30c68de7bcee1d6320a1dc765df10bc29694b2755(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cdb16cb5cd5fe7058e70740ef71dab2235774a433187c7b9fadc567d8e03e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286b345f0e7dc48ee149ff316ffe1096864205bcac4bca71071cc44f2fcb10e4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a700f61ca0889496c6f249d0eea33c0863b4648cdf93fe0aa6d542e4b03a6fe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471c970638c20d8c99cc13a8b0183019a8ad8cc9b25740939e42d7f33510a864(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b53f3124061185ae4fd4bdec5a3031bb96a0bd1338a3c95574f8175efe72c2d(
    value: typing.Optional[GoogleCloudRunV2ServiceTerminalCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643087fe7320138e0cf04b2e351f4422fac75a183bb1abdbd1b100008a4bdf27(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c296edc9972feeedbfbd5cca677230c857183208d51579c1334f85c97b474f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e58a6bf1bdf895a3b00bee159203fada28fb14be8d4088a4bdbc311a3ba943(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d70212d4283b539c412ac789fe2c912467c073fc417024729e71fa7eaa875f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a31dd12a1d7aee336763f4d105d86f5fb4c677fdec30e0b0aa0eb9edad874a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57d7f7b1a0b7451b2a0f8183d1e72cede43869afe2efead849716b27db32f90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985b988927366cda2b9672749e23a5a49d3e0888f4ca97eae5214696b65d3d30(
    *,
    percent: typing.Optional[jsii.Number] = None,
    revision: typing.Optional[builtins.str] = None,
    tag: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc8fd5b0cac799ea4d61407b09156200c860b952ec56d685e71b0fed287af1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96da40b3f9f6e94a81136ffbd9e9f5f0c413352d91c2c1a92e481b427c2be3a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e0962a55e11b301ee20b2a40a6d827ce2227ada3832a3022296e7c8557c167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5015be70d8997c53e2f1b195436eaac6d0c3fb79acd21d7ddd354ad0c533bd5c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f9b4c4ff05fa906c0da85c30af100866d3588e69cce0fc631bade018f867f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf27a650605cb3734f73d633c418a7d1deb8d7321e24142ec8ad67091e1e36d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleCloudRunV2ServiceTraffic]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c16b4c4650df70f069ea27592af4265b9a6403698f3e57d50e72e7f76b8a2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699d74e1ff8b767a6ed9f686fa8972db9db85472e2de2eb81bdb6b189091481a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76472065f3a2f958995e47521d414500cfe23e13abd577d796e1662e43d5ff8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3531fb43451052f2df5d16a0d76def070b584984bbfc11f3e578a22456b148c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc686da16d497f2bcd42399e0ba68f0fafac4badc2247c9caa64b8b3285c3f46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3aee2f761089b0fa538d135a4e1646418ee6613804335b7d8d789b25bbf7600(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleCloudRunV2ServiceTraffic]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb9656237d74a4bf2a53e0a61dafab4cba2a4496f01d6c3a4a5401fbdab295c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1ed82f105370e5717b8af6248a6c585905ffa50f52669227c92c9602cd85a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8233b7d819685727ebf71e1473a362e56c63acda8000d3ee06debfd78cf2a9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ec566ce0c7e969a28ae800a1d99d7b4158652881a5dbcf96005c593ba09575(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3d356496c5dcfb7196722d2e07622e9cb89abeec32864a3254feef63517d33(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1eb5a9fdc01513e0a0f741aa7091d1cbc2163e57006c8d29b1bc1655ea93d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ae2a41534cef94238ce393a633a264a9756a2860979f4de218636644729759(
    value: typing.Optional[GoogleCloudRunV2ServiceTrafficStatuses],
) -> None:
    """Type checking stubs"""
    pass

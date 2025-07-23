r'''
# `google_vertex_ai_endpoint`

Refer to the Terraform Registry for docs: [`google_vertex_ai_endpoint`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint).
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


class VertexAiEndpoint(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpoint",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint google_vertex_ai_endpoint}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        location: builtins.str,
        name: builtins.str,
        dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_spec: typing.Optional[typing.Union["VertexAiEndpointEncryptionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        predict_request_response_logging_config: typing.Optional[typing.Union["VertexAiEndpointPredictRequestResponseLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_service_connect_config: typing.Optional[typing.Union["VertexAiEndpointPrivateServiceConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiEndpointTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_split: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint google_vertex_ai_endpoint} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Required. The display name of the Endpoint. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#display_name VertexAiEndpoint#display_name}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#location VertexAiEndpoint#location}
        :param name: The resource name of the Endpoint. The name must be numeric with no leading zeros and can be at most 10 digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#name VertexAiEndpoint#name}
        :param dedicated_endpoint_enabled: If true, the endpoint will be exposed through a dedicated DNS [Endpoint.dedicated_endpoint_dns]. Your request to the dedicated DNS will be isolated from other users' traffic and will have better performance and reliability. Note: Once you enabled dedicated endpoint, you won't be able to send request to the shared DNS {region}-aiplatform.googleapis.com. The limitation will be removed soon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#dedicated_endpoint_enabled VertexAiEndpoint#dedicated_endpoint_enabled}
        :param description: The description of the Endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#description VertexAiEndpoint#description}
        :param encryption_spec: encryption_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#encryption_spec VertexAiEndpoint#encryption_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#id VertexAiEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels with user-defined metadata to organize your Endpoints. Label keys and values can be no longer than 64 characters (Unicode codepoints), can only contain lowercase letters, numeric characters, underscores and dashes. International characters are allowed. See https://goo.gl/xmQnxf for more information and examples of labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#labels VertexAiEndpoint#labels}
        :param network: The full name of the Google Compute Engine `network <https://cloud.google.com//compute/docs/networks-and-firewalls#networks>`_ to which the Endpoint should be peered. Private services access must already be configured for the network. If left unspecified, the Endpoint is not peered with any network. Only one of the fields, network or enable_private_service_connect, can be set. `Format <https://cloud.google.com/compute/docs/reference/rest/v1/networks/insert>`_: 'projects/{project}/global/networks/{network}'. Where '{project}' is a project number, as in '12345', and '{network}' is network name. Only one of the fields, 'network' or 'privateServiceConnectConfig', can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#network VertexAiEndpoint#network}
        :param predict_request_response_logging_config: predict_request_response_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#predict_request_response_logging_config VertexAiEndpoint#predict_request_response_logging_config}
        :param private_service_connect_config: private_service_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#private_service_connect_config VertexAiEndpoint#private_service_connect_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#project VertexAiEndpoint#project}.
        :param region: The region for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#region VertexAiEndpoint#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#timeouts VertexAiEndpoint#timeouts}
        :param traffic_split: A map from a DeployedModel's id to the percentage of this Endpoint's traffic that should be forwarded to that DeployedModel. If a DeployedModel's id is not listed in this map, then it receives no traffic. The traffic percentage values must add up to 100, or map must be empty if the Endpoint is to not accept any traffic at a moment. See the 'deployModel' `example <https://cloud.google.com/vertex-ai/docs/general/deployment#deploy_a_model_to_an_endpoint>`_ and `documentation <https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.endpoints/deployModel>`_ for more information. ~> **Note:** To set the map to empty, set '"{}"', apply, and then remove the field from your config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#traffic_split VertexAiEndpoint#traffic_split}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae5843bb2578a6408d1e97a23d15183f0242a04c2b2be36592e31d6479cd7b9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiEndpointConfig(
            display_name=display_name,
            location=location,
            name=name,
            dedicated_endpoint_enabled=dedicated_endpoint_enabled,
            description=description,
            encryption_spec=encryption_spec,
            id=id,
            labels=labels,
            network=network,
            predict_request_response_logging_config=predict_request_response_logging_config,
            private_service_connect_config=private_service_connect_config,
            project=project,
            region=region,
            timeouts=timeouts,
            traffic_split=traffic_split,
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
        '''Generates CDKTF code for importing a VertexAiEndpoint resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiEndpoint to import.
        :param import_from_id: The id of the existing VertexAiEndpoint that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiEndpoint to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec86b7c39a688992eb801a10e1c147db1bb4a563754a6b2f3abe0428c1934ad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionSpec")
    def put_encryption_spec(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Required. The Cloud KMS resource identifier of the customer managed encryption key used to protect a resource. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. The key needs to be in the same region as where the compute resource is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#kms_key_name VertexAiEndpoint#kms_key_name}
        '''
        value = VertexAiEndpointEncryptionSpec(kms_key_name=kms_key_name)

        return typing.cast(None, jsii.invoke(self, "putEncryptionSpec", [value]))

    @jsii.member(jsii_name="putPredictRequestResponseLoggingConfig")
    def put_predict_request_response_logging_config(
        self,
        *,
        bigquery_destination: typing.Optional[typing.Union["VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sampling_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bigquery_destination: bigquery_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#bigquery_destination VertexAiEndpoint#bigquery_destination}
        :param enabled: If logging is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enabled VertexAiEndpoint#enabled}
        :param sampling_rate: Percentage of requests to be logged, expressed as a fraction in range(0,1]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#sampling_rate VertexAiEndpoint#sampling_rate}
        '''
        value = VertexAiEndpointPredictRequestResponseLoggingConfig(
            bigquery_destination=bigquery_destination,
            enabled=enabled,
            sampling_rate=sampling_rate,
        )

        return typing.cast(None, jsii.invoke(self, "putPredictRequestResponseLoggingConfig", [value]))

    @jsii.member(jsii_name="putPrivateServiceConnectConfig")
    def put_private_service_connect_config(
        self,
        *,
        enable_private_service_connect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enable_secure_private_service_connect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_private_service_connect: Required. If true, expose the IndexEndpoint via private service connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enable_private_service_connect VertexAiEndpoint#enable_private_service_connect}
        :param enable_secure_private_service_connect: If set to true, enable secure private service connect with IAM authorization. Otherwise, private service connect will be done without authorization. Note latency will be slightly increased if authorization is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enable_secure_private_service_connect VertexAiEndpoint#enable_secure_private_service_connect}
        :param project_allowlist: A list of Projects from which the forwarding rule will target the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#project_allowlist VertexAiEndpoint#project_allowlist}
        '''
        value = VertexAiEndpointPrivateServiceConnectConfig(
            enable_private_service_connect=enable_private_service_connect,
            enable_secure_private_service_connect=enable_secure_private_service_connect,
            project_allowlist=project_allowlist,
        )

        return typing.cast(None, jsii.invoke(self, "putPrivateServiceConnectConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#create VertexAiEndpoint#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#delete VertexAiEndpoint#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#update VertexAiEndpoint#update}.
        '''
        value = VertexAiEndpointTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDedicatedEndpointEnabled")
    def reset_dedicated_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedEndpointEnabled", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryptionSpec")
    def reset_encryption_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionSpec", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetPredictRequestResponseLoggingConfig")
    def reset_predict_request_response_logging_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPredictRequestResponseLoggingConfig", []))

    @jsii.member(jsii_name="resetPrivateServiceConnectConfig")
    def reset_private_service_connect_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateServiceConnectConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrafficSplit")
    def reset_traffic_split(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficSplit", []))

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
    @jsii.member(jsii_name="dedicatedEndpointDns")
    def dedicated_endpoint_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dedicatedEndpointDns"))

    @builtins.property
    @jsii.member(jsii_name="deployedModels")
    def deployed_models(self) -> "VertexAiEndpointDeployedModelsList":
        return typing.cast("VertexAiEndpointDeployedModelsList", jsii.get(self, "deployedModels"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpec")
    def encryption_spec(self) -> "VertexAiEndpointEncryptionSpecOutputReference":
        return typing.cast("VertexAiEndpointEncryptionSpecOutputReference", jsii.get(self, "encryptionSpec"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="modelDeploymentMonitoringJob")
    def model_deployment_monitoring_job(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelDeploymentMonitoringJob"))

    @builtins.property
    @jsii.member(jsii_name="predictRequestResponseLoggingConfig")
    def predict_request_response_logging_config(
        self,
    ) -> "VertexAiEndpointPredictRequestResponseLoggingConfigOutputReference":
        return typing.cast("VertexAiEndpointPredictRequestResponseLoggingConfigOutputReference", jsii.get(self, "predictRequestResponseLoggingConfig"))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnectConfig")
    def private_service_connect_config(
        self,
    ) -> "VertexAiEndpointPrivateServiceConnectConfigOutputReference":
        return typing.cast("VertexAiEndpointPrivateServiceConnectConfigOutputReference", jsii.get(self, "privateServiceConnectConfig"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VertexAiEndpointTimeoutsOutputReference":
        return typing.cast("VertexAiEndpointTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedEndpointEnabledInput")
    def dedicated_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dedicatedEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionSpecInput")
    def encryption_spec_input(
        self,
    ) -> typing.Optional["VertexAiEndpointEncryptionSpec"]:
        return typing.cast(typing.Optional["VertexAiEndpointEncryptionSpec"], jsii.get(self, "encryptionSpecInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="predictRequestResponseLoggingConfigInput")
    def predict_request_response_logging_config_input(
        self,
    ) -> typing.Optional["VertexAiEndpointPredictRequestResponseLoggingConfig"]:
        return typing.cast(typing.Optional["VertexAiEndpointPredictRequestResponseLoggingConfig"], jsii.get(self, "predictRequestResponseLoggingConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="privateServiceConnectConfigInput")
    def private_service_connect_config_input(
        self,
    ) -> typing.Optional["VertexAiEndpointPrivateServiceConnectConfig"]:
        return typing.cast(typing.Optional["VertexAiEndpointPrivateServiceConnectConfig"], jsii.get(self, "privateServiceConnectConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiEndpointTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiEndpointTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficSplitInput")
    def traffic_split_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "trafficSplitInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedEndpointEnabled")
    def dedicated_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dedicatedEndpointEnabled"))

    @dedicated_endpoint_enabled.setter
    def dedicated_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6b3521540e92bc86aa93bd5d644d5cbde809d6a304fcd47af5e8d563031c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicatedEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d8a0e82f4137a459550bcc2f527956f3d1d5e6144444cd6b2a7d14973eee3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc9946f68c9edb40c8107b697637c21693f2a12d757198583deec797ecc5f1ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc066f2603f3bb9a57107af2a3a7a7c1ac285e71acdd86cc40d4a11f88d8bd18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250c1d8645dbb2462121e16600dea6ce470283fd5a7c715300a546f14a40642f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b20707f2f1be903944b65b8435aa9359183c04fc88ab8e457850ab2346e036)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d1b6f7bd472f78ad0a669dba6d8db152d7f0649e9fbdcf132c8fef120452d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3825d9883af41452049dda5f372b3b9cda3446c0c273cb355871bd195c6d9160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de650bb74dc9d45a3c52710ce3b74ab54a63302692e07f3bc02aa0c2551ab24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e0db9754e4bb8ef99cb4534e023b835a089b55feb4e6d878c1c08864122622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trafficSplit")
    def traffic_split(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "trafficSplit"))

    @traffic_split.setter
    def traffic_split(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5410a5e614d41f64c50ac1b1dece4c8a301897ec353e31c79d02d56a0714e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trafficSplit", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "location": "location",
        "name": "name",
        "dedicated_endpoint_enabled": "dedicatedEndpointEnabled",
        "description": "description",
        "encryption_spec": "encryptionSpec",
        "id": "id",
        "labels": "labels",
        "network": "network",
        "predict_request_response_logging_config": "predictRequestResponseLoggingConfig",
        "private_service_connect_config": "privateServiceConnectConfig",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
        "traffic_split": "trafficSplit",
    },
)
class VertexAiEndpointConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        location: builtins.str,
        name: builtins.str,
        dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_spec: typing.Optional[typing.Union["VertexAiEndpointEncryptionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        network: typing.Optional[builtins.str] = None,
        predict_request_response_logging_config: typing.Optional[typing.Union["VertexAiEndpointPredictRequestResponseLoggingConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        private_service_connect_config: typing.Optional[typing.Union["VertexAiEndpointPrivateServiceConnectConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiEndpointTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_split: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Required. The display name of the Endpoint. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#display_name VertexAiEndpoint#display_name}
        :param location: The location for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#location VertexAiEndpoint#location}
        :param name: The resource name of the Endpoint. The name must be numeric with no leading zeros and can be at most 10 digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#name VertexAiEndpoint#name}
        :param dedicated_endpoint_enabled: If true, the endpoint will be exposed through a dedicated DNS [Endpoint.dedicated_endpoint_dns]. Your request to the dedicated DNS will be isolated from other users' traffic and will have better performance and reliability. Note: Once you enabled dedicated endpoint, you won't be able to send request to the shared DNS {region}-aiplatform.googleapis.com. The limitation will be removed soon. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#dedicated_endpoint_enabled VertexAiEndpoint#dedicated_endpoint_enabled}
        :param description: The description of the Endpoint. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#description VertexAiEndpoint#description}
        :param encryption_spec: encryption_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#encryption_spec VertexAiEndpoint#encryption_spec}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#id VertexAiEndpoint#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels with user-defined metadata to organize your Endpoints. Label keys and values can be no longer than 64 characters (Unicode codepoints), can only contain lowercase letters, numeric characters, underscores and dashes. International characters are allowed. See https://goo.gl/xmQnxf for more information and examples of labels. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#labels VertexAiEndpoint#labels}
        :param network: The full name of the Google Compute Engine `network <https://cloud.google.com//compute/docs/networks-and-firewalls#networks>`_ to which the Endpoint should be peered. Private services access must already be configured for the network. If left unspecified, the Endpoint is not peered with any network. Only one of the fields, network or enable_private_service_connect, can be set. `Format <https://cloud.google.com/compute/docs/reference/rest/v1/networks/insert>`_: 'projects/{project}/global/networks/{network}'. Where '{project}' is a project number, as in '12345', and '{network}' is network name. Only one of the fields, 'network' or 'privateServiceConnectConfig', can be set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#network VertexAiEndpoint#network}
        :param predict_request_response_logging_config: predict_request_response_logging_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#predict_request_response_logging_config VertexAiEndpoint#predict_request_response_logging_config}
        :param private_service_connect_config: private_service_connect_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#private_service_connect_config VertexAiEndpoint#private_service_connect_config}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#project VertexAiEndpoint#project}.
        :param region: The region for the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#region VertexAiEndpoint#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#timeouts VertexAiEndpoint#timeouts}
        :param traffic_split: A map from a DeployedModel's id to the percentage of this Endpoint's traffic that should be forwarded to that DeployedModel. If a DeployedModel's id is not listed in this map, then it receives no traffic. The traffic percentage values must add up to 100, or map must be empty if the Endpoint is to not accept any traffic at a moment. See the 'deployModel' `example <https://cloud.google.com/vertex-ai/docs/general/deployment#deploy_a_model_to_an_endpoint>`_ and `documentation <https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.endpoints/deployModel>`_ for more information. ~> **Note:** To set the map to empty, set '"{}"', apply, and then remove the field from your config. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#traffic_split VertexAiEndpoint#traffic_split}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_spec, dict):
            encryption_spec = VertexAiEndpointEncryptionSpec(**encryption_spec)
        if isinstance(predict_request_response_logging_config, dict):
            predict_request_response_logging_config = VertexAiEndpointPredictRequestResponseLoggingConfig(**predict_request_response_logging_config)
        if isinstance(private_service_connect_config, dict):
            private_service_connect_config = VertexAiEndpointPrivateServiceConnectConfig(**private_service_connect_config)
        if isinstance(timeouts, dict):
            timeouts = VertexAiEndpointTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d721663393801d931c84712a91b1f254e4d844e028312c46feeb4ec3ed08389)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dedicated_endpoint_enabled", value=dedicated_endpoint_enabled, expected_type=type_hints["dedicated_endpoint_enabled"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_spec", value=encryption_spec, expected_type=type_hints["encryption_spec"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument predict_request_response_logging_config", value=predict_request_response_logging_config, expected_type=type_hints["predict_request_response_logging_config"])
            check_type(argname="argument private_service_connect_config", value=private_service_connect_config, expected_type=type_hints["private_service_connect_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument traffic_split", value=traffic_split, expected_type=type_hints["traffic_split"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "location": location,
            "name": name,
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
        if dedicated_endpoint_enabled is not None:
            self._values["dedicated_endpoint_enabled"] = dedicated_endpoint_enabled
        if description is not None:
            self._values["description"] = description
        if encryption_spec is not None:
            self._values["encryption_spec"] = encryption_spec
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if network is not None:
            self._values["network"] = network
        if predict_request_response_logging_config is not None:
            self._values["predict_request_response_logging_config"] = predict_request_response_logging_config
        if private_service_connect_config is not None:
            self._values["private_service_connect_config"] = private_service_connect_config
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if traffic_split is not None:
            self._values["traffic_split"] = traffic_split

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
    def display_name(self) -> builtins.str:
        '''Required.

        The display name of the Endpoint. The name can be up to 128 characters long and can consist of any UTF-8 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#display_name VertexAiEndpoint#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#location VertexAiEndpoint#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The resource name of the Endpoint.

        The name must be numeric with no leading zeros and can be at most 10 digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#name VertexAiEndpoint#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dedicated_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the endpoint will be exposed through a dedicated DNS [Endpoint.dedicated_endpoint_dns]. Your request to the dedicated DNS will be isolated from other users' traffic and will have better performance and reliability. Note: Once you enabled dedicated endpoint, you won't be able to send request to the shared DNS {region}-aiplatform.googleapis.com. The limitation will be removed soon.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#dedicated_endpoint_enabled VertexAiEndpoint#dedicated_endpoint_enabled}
        '''
        result = self._values.get("dedicated_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Endpoint.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#description VertexAiEndpoint#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_spec(self) -> typing.Optional["VertexAiEndpointEncryptionSpec"]:
        '''encryption_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#encryption_spec VertexAiEndpoint#encryption_spec}
        '''
        result = self._values.get("encryption_spec")
        return typing.cast(typing.Optional["VertexAiEndpointEncryptionSpec"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#id VertexAiEndpoint#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels with user-defined metadata to organize your Endpoints.

        Label keys and values can be no longer than 64 characters (Unicode codepoints), can only contain lowercase letters, numeric characters, underscores and dashes. International characters are allowed. See https://goo.gl/xmQnxf for more information and examples of labels.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#labels VertexAiEndpoint#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def network(self) -> typing.Optional[builtins.str]:
        '''The full name of the Google Compute Engine `network <https://cloud.google.com//compute/docs/networks-and-firewalls#networks>`_ to which the Endpoint should be peered. Private services access must already be configured for the network. If left unspecified, the Endpoint is not peered with any network. Only one of the fields, network or enable_private_service_connect, can be set. `Format <https://cloud.google.com/compute/docs/reference/rest/v1/networks/insert>`_: 'projects/{project}/global/networks/{network}'. Where '{project}' is a project number, as in '12345', and '{network}' is network name. Only one of the fields, 'network' or 'privateServiceConnectConfig', can be set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#network VertexAiEndpoint#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def predict_request_response_logging_config(
        self,
    ) -> typing.Optional["VertexAiEndpointPredictRequestResponseLoggingConfig"]:
        '''predict_request_response_logging_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#predict_request_response_logging_config VertexAiEndpoint#predict_request_response_logging_config}
        '''
        result = self._values.get("predict_request_response_logging_config")
        return typing.cast(typing.Optional["VertexAiEndpointPredictRequestResponseLoggingConfig"], result)

    @builtins.property
    def private_service_connect_config(
        self,
    ) -> typing.Optional["VertexAiEndpointPrivateServiceConnectConfig"]:
        '''private_service_connect_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#private_service_connect_config VertexAiEndpoint#private_service_connect_config}
        '''
        result = self._values.get("private_service_connect_config")
        return typing.cast(typing.Optional["VertexAiEndpointPrivateServiceConnectConfig"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#project VertexAiEndpoint#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region for the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#region VertexAiEndpoint#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VertexAiEndpointTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#timeouts VertexAiEndpoint#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiEndpointTimeouts"], result)

    @builtins.property
    def traffic_split(self) -> typing.Optional[builtins.str]:
        '''A map from a DeployedModel's id to the percentage of this Endpoint's traffic that should be forwarded to that DeployedModel.

        If a DeployedModel's id is not listed in this map, then it receives no traffic.
        The traffic percentage values must add up to 100, or map must be empty if the Endpoint is to not accept any traffic at a moment. See
        the 'deployModel' `example <https://cloud.google.com/vertex-ai/docs/general/deployment#deploy_a_model_to_an_endpoint>`_ and
        `documentation <https://cloud.google.com/vertex-ai/docs/reference/rest/v1beta1/projects.locations.endpoints/deployModel>`_ for more information.

        ~> **Note:** To set the map to empty, set '"{}"', apply, and then remove the field from your config.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#traffic_split VertexAiEndpoint#traffic_split}
        '''
        result = self._values.get("traffic_split")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModels",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiEndpointDeployedModels:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointDeployedModels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsAutomaticResources",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiEndpointDeployedModelsAutomaticResources:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointDeployedModelsAutomaticResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointDeployedModelsAutomaticResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsAutomaticResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37d8d09b2e259b4f5e9c357ee8e49501f7d7e718f7e2b2c5029b833fae8a8ab2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointDeployedModelsAutomaticResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db30cb6b593f8cb1930b2a0d4af1fcb74c37a52973521b4a6c5de70a5d844f55)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointDeployedModelsAutomaticResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85ebdac2149924738632916701cbd8cfe5dbf34ea1c846559d53530e92f74b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a3537bc6d267d877f5799a9991b7fad45f5f981d0303e1d31021f938aa0393a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1df7aeac4ba12fa0a017c9e36b6a02ab9e838e6a911882808d833f65edbf42b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointDeployedModelsAutomaticResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsAutomaticResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b83856f11073c075ac786f324283a6815901b2424841a18063dad61155c170)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxReplicaCount")
    def max_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicaCount"))

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointDeployedModelsAutomaticResources]:
        return typing.cast(typing.Optional[VertexAiEndpointDeployedModelsAutomaticResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointDeployedModelsAutomaticResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b954ef3b654a72920177e2d3245012e3420d5e6f87f4e6e64c3c9377998aa89f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResources",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiEndpointDeployedModelsDedicatedResources:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointDeployedModelsDedicatedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecs",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7995b879244923f14953cb9db182afb8909c8f1879ae7dc0e5465c1cb2687534)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff18cdecaf2282009873ee895b8b7c2fce4054dbb0bb8e8b2d3c0f531227f25)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fd1c11dfae88fe141b0a4eb959fdcddbff5f75d33cf97e799671c01aad4346)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9dcf6ee4841b3036c22c2632da18a8d06aa273733cf95c340ac60adb7dc9cd58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f45f9521cff9ad9d81ec18486ef8d437db8e624ca9c3a13875426b969243e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af5b6dbfc752eb03fbd3914cc66d492cc95dd809799977b395316286ac7090b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecs]:
        return typing.cast(typing.Optional[VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__742468a1953a1211f014f5fae52327c3460b63a9d078e454863be5fb0c631a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointDeployedModelsDedicatedResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1724121ec8d97b41ac38d2d2384ba7106a504c3c4fe0e93d04a003c473cd5b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointDeployedModelsDedicatedResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e310f901afae398c4d0142b0b24756670592adf779da48d0d30934910496e8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointDeployedModelsDedicatedResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a075fc98bfa135846e08cc70b5cea3923a64a24848d988b767e827a8e799e69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__293f96947cd45412580cc134dea4c6f8708827dfe3e3d7536a939f53b968c931)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48d73902b240a2f5e36c8fbdf20bb992b3b67240af7cb1880a5bce385457ecea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpec",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpec:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__feed58e5931d603f1b22bafd78b8c56d3c01a347ae32ec55feec66ab5324ade6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d2878bc1326465a2131a78e43e7e382590320605263bb1262067734518fd9f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d850dade41e0ff4bb910f860d1287a877df0d71183b8269e65188eb33e96b1e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7694be332e3b9606a625d65b52b248490e2f660ece14d357f553ac8b7f5bfc3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6c5f75f251a3e6ce6fe5912c60593204a21d15a187a5fbc48e3c4b1d0d9bd20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__303642129eb5178281c408ed134734aa9a1558c640db8981b8e5fb63c0477ead)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77bc59bf5626a675b4dabe679be0009150ab114bca7d5aaf0455a9be765cbe7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointDeployedModelsDedicatedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsDedicatedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b7e2b014ea53c2296dc1e8d460e4efbd31d7d73c85ad264addf44eb7c0d3af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricSpecs")
    def autoscaling_metric_specs(
        self,
    ) -> VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsList:
        return typing.cast(VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsList, jsii.get(self, "autoscalingMetricSpecs"))

    @builtins.property
    @jsii.member(jsii_name="machineSpec")
    def machine_spec(
        self,
    ) -> VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecList:
        return typing.cast(VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecList, jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicaCount")
    def max_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicaCount"))

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointDeployedModelsDedicatedResources]:
        return typing.cast(typing.Optional[VertexAiEndpointDeployedModelsDedicatedResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointDeployedModelsDedicatedResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9a41c6c28f583f20847abcf66393ad8624044bce568de8d17ee7aa3150046b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointDeployedModelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__979c020c779dfce15507d21351076d4c5a0d9012ba92159f733a4225e8a4d376)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointDeployedModelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e58203f85ce3481ff183a927029e9f95379307e701777b0fe2cb90971de3f346)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointDeployedModelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcddd6feb88daedb5742e32296e5ef10cb30336e1079aee0a9180025a56572dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be71699f6da28d903ffd41257f7b5693163a51826a595127fb608a583d46f35a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37fe1f804951357ea2024520b8c27c871ac01417c2784f02ef0581f547f10e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointDeployedModelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50c72641904a3c3eb4ad29d968b7345aca1a822a625c5f8599a6f2fc564d5a43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="automaticResources")
    def automatic_resources(
        self,
    ) -> VertexAiEndpointDeployedModelsAutomaticResourcesList:
        return typing.cast(VertexAiEndpointDeployedModelsAutomaticResourcesList, jsii.get(self, "automaticResources"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResources")
    def dedicated_resources(
        self,
    ) -> VertexAiEndpointDeployedModelsDedicatedResourcesList:
        return typing.cast(VertexAiEndpointDeployedModelsDedicatedResourcesList, jsii.get(self, "dedicatedResources"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="enableAccessLogging")
    def enable_access_logging(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableAccessLogging"))

    @builtins.property
    @jsii.member(jsii_name="enableContainerLogging")
    def enable_container_logging(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enableContainerLogging"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @builtins.property
    @jsii.member(jsii_name="modelVersionId")
    def model_version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelVersionId"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpoints")
    def private_endpoints(self) -> "VertexAiEndpointDeployedModelsPrivateEndpointsList":
        return typing.cast("VertexAiEndpointDeployedModelsPrivateEndpointsList", jsii.get(self, "privateEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="sharedResources")
    def shared_resources(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedResources"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiEndpointDeployedModels]:
        return typing.cast(typing.Optional[VertexAiEndpointDeployedModels], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointDeployedModels],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e5af3a15b33d023461facb1544b81a6c404241ec7f40fdb232469908be960d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsPrivateEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiEndpointDeployedModelsPrivateEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointDeployedModelsPrivateEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointDeployedModelsPrivateEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsPrivateEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__470cb5aabe691f6fdc0b8eb5e7164a7e9e4f80203a3b1c62f62012fa847149c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiEndpointDeployedModelsPrivateEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a2da3c723263d269270ea2ed92838e193b1781cdb7a0ff9ef10db2ae63b687)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiEndpointDeployedModelsPrivateEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448d464fa0bca0ebce4bd09549c4f65ef449b5e1d6784f3a582d21d4bbc57edf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df6377cad615a911ea494ca1b9dc1a2f88a2909da8a4e844b546cd186dbaf06e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec512184dfb9cef8f849eb5f3bcb840f9560725170ff6f519658fc4317811399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointDeployedModelsPrivateEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointDeployedModelsPrivateEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30b0e5679a9ffec71f7c165866b586a84870b752a223823d753c8b2787a76b9b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="explainHttpUri")
    def explain_http_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "explainHttpUri"))

    @builtins.property
    @jsii.member(jsii_name="healthHttpUri")
    def health_http_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthHttpUri"))

    @builtins.property
    @jsii.member(jsii_name="predictHttpUri")
    def predict_http_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "predictHttpUri"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointDeployedModelsPrivateEndpoints]:
        return typing.cast(typing.Optional[VertexAiEndpointDeployedModelsPrivateEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointDeployedModelsPrivateEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6001e7d137c950cdc16946176dd768cb3673cffcc5b513f0ddb271963ee735)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointEncryptionSpec",
    jsii_struct_bases=[],
    name_mapping={"kms_key_name": "kmsKeyName"},
)
class VertexAiEndpointEncryptionSpec:
    def __init__(self, *, kms_key_name: builtins.str) -> None:
        '''
        :param kms_key_name: Required. The Cloud KMS resource identifier of the customer managed encryption key used to protect a resource. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. The key needs to be in the same region as where the compute resource is created. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#kms_key_name VertexAiEndpoint#kms_key_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7904c6bc1d0e73b7aa75edaee52aaa0d383b97faf407241b7a45e1086835e17)
            check_type(argname="argument kms_key_name", value=kms_key_name, expected_type=type_hints["kms_key_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "kms_key_name": kms_key_name,
        }

    @builtins.property
    def kms_key_name(self) -> builtins.str:
        '''Required.

        The Cloud KMS resource identifier of the customer managed encryption key used to protect a resource. Has the form: 'projects/my-project/locations/my-region/keyRings/my-kr/cryptoKeys/my-key'. The key needs to be in the same region as where the compute resource is created.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#kms_key_name VertexAiEndpoint#kms_key_name}
        '''
        result = self._values.get("kms_key_name")
        assert result is not None, "Required property 'kms_key_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointEncryptionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointEncryptionSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointEncryptionSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18c38e5917ee0364ab817567c6e2adefcc183c67caa983cff544b5a88c02c6e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="kmsKeyNameInput")
    def kms_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyName")
    def kms_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyName"))

    @kms_key_name.setter
    def kms_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf4ebad934e5e8d288f273c31033af42db608c2143f04869404453e5108ebf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VertexAiEndpointEncryptionSpec]:
        return typing.cast(typing.Optional[VertexAiEndpointEncryptionSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointEncryptionSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0c7215d41bd02d795f129775e6c20c00d433c0735056c7a793c012d7c232b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointPredictRequestResponseLoggingConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bigquery_destination": "bigqueryDestination",
        "enabled": "enabled",
        "sampling_rate": "samplingRate",
    },
)
class VertexAiEndpointPredictRequestResponseLoggingConfig:
    def __init__(
        self,
        *,
        bigquery_destination: typing.Optional[typing.Union["VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sampling_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bigquery_destination: bigquery_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#bigquery_destination VertexAiEndpoint#bigquery_destination}
        :param enabled: If logging is enabled or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enabled VertexAiEndpoint#enabled}
        :param sampling_rate: Percentage of requests to be logged, expressed as a fraction in range(0,1]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#sampling_rate VertexAiEndpoint#sampling_rate}
        '''
        if isinstance(bigquery_destination, dict):
            bigquery_destination = VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination(**bigquery_destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ccd14c836ec093b1e2200d3b7bfbc0d6e01e409cbfbc29c5b40cf658b19d17b)
            check_type(argname="argument bigquery_destination", value=bigquery_destination, expected_type=type_hints["bigquery_destination"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument sampling_rate", value=sampling_rate, expected_type=type_hints["sampling_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bigquery_destination is not None:
            self._values["bigquery_destination"] = bigquery_destination
        if enabled is not None:
            self._values["enabled"] = enabled
        if sampling_rate is not None:
            self._values["sampling_rate"] = sampling_rate

    @builtins.property
    def bigquery_destination(
        self,
    ) -> typing.Optional["VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination"]:
        '''bigquery_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#bigquery_destination VertexAiEndpoint#bigquery_destination}
        '''
        result = self._values.get("bigquery_destination")
        return typing.cast(typing.Optional["VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If logging is enabled or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enabled VertexAiEndpoint#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sampling_rate(self) -> typing.Optional[jsii.Number]:
        '''Percentage of requests to be logged, expressed as a fraction in range(0,1].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#sampling_rate VertexAiEndpoint#sampling_rate}
        '''
        result = self._values.get("sampling_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointPredictRequestResponseLoggingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination",
    jsii_struct_bases=[],
    name_mapping={"output_uri": "outputUri"},
)
class VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination:
    def __init__(self, *, output_uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param output_uri: BigQuery URI to a project or table, up to 2000 characters long. When only the project is specified, the Dataset and Table is created. When the full table reference is specified, the Dataset must exist and table must not exist. Accepted forms: - BigQuery path. For example: 'bq://projectId' or 'bq://projectId.bqDatasetId' or 'bq://projectId.bqDatasetId.bqTableId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#output_uri VertexAiEndpoint#output_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060399abf67c905fe5691b460dc45eb213058a9d83ce09259d3506712cd2581f)
            check_type(argname="argument output_uri", value=output_uri, expected_type=type_hints["output_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if output_uri is not None:
            self._values["output_uri"] = output_uri

    @builtins.property
    def output_uri(self) -> typing.Optional[builtins.str]:
        '''BigQuery URI to a project or table, up to 2000 characters long.

        When only the project is specified, the Dataset and Table is created. When the full table reference is specified, the Dataset must exist and table must not exist. Accepted forms: - BigQuery path. For example: 'bq://projectId' or 'bq://projectId.bqDatasetId' or 'bq://projectId.bqDatasetId.bqTableId'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#output_uri VertexAiEndpoint#output_uri}
        '''
        result = self._values.get("output_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5643b52e7cdc77816cebcb2fa2cd922ebc1caa2328dc9443b567e1384c8d6beb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetOutputUri")
    def reset_output_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputUri", []))

    @builtins.property
    @jsii.member(jsii_name="outputUriInput")
    def output_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputUriInput"))

    @builtins.property
    @jsii.member(jsii_name="outputUri")
    def output_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputUri"))

    @output_uri.setter
    def output_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42aea9dc0a00eb019738ddb2fef43fe94a8a723491896dd7d3e9693a80200800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination]:
        return typing.cast(typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9320b3505678dad8c808e5343fff62a16d387bade6addbe3724b9ac472b6e7d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiEndpointPredictRequestResponseLoggingConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointPredictRequestResponseLoggingConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f07ba4f8e6351eeb1b6809f43425476a7be527a17a14bd0003d983f93e6b0dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putBigqueryDestination")
    def put_bigquery_destination(
        self,
        *,
        output_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param output_uri: BigQuery URI to a project or table, up to 2000 characters long. When only the project is specified, the Dataset and Table is created. When the full table reference is specified, the Dataset must exist and table must not exist. Accepted forms: - BigQuery path. For example: 'bq://projectId' or 'bq://projectId.bqDatasetId' or 'bq://projectId.bqDatasetId.bqTableId'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#output_uri VertexAiEndpoint#output_uri}
        '''
        value = VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination(
            output_uri=output_uri
        )

        return typing.cast(None, jsii.invoke(self, "putBigqueryDestination", [value]))

    @jsii.member(jsii_name="resetBigqueryDestination")
    def reset_bigquery_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBigqueryDestination", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetSamplingRate")
    def reset_sampling_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSamplingRate", []))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDestination")
    def bigquery_destination(
        self,
    ) -> VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestinationOutputReference:
        return typing.cast(VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestinationOutputReference, jsii.get(self, "bigqueryDestination"))

    @builtins.property
    @jsii.member(jsii_name="bigqueryDestinationInput")
    def bigquery_destination_input(
        self,
    ) -> typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination]:
        return typing.cast(typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination], jsii.get(self, "bigqueryDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingRateInput")
    def sampling_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingRateInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f28a022cf2eefd8861090087c3b3be9b2cd7794697922f073e1a16ffb9320d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="samplingRate")
    def sampling_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingRate"))

    @sampling_rate.setter
    def sampling_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d4cba4fc3cc4d8541737361571f5449c658f56c7b46d49d9714286e2b1f0c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfig]:
        return typing.cast(typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbef574862749877112310a6b0a9ce3ba3e9b4ab9498ed254f11d4ea1d6bdb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointPrivateServiceConnectConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_private_service_connect": "enablePrivateServiceConnect",
        "enable_secure_private_service_connect": "enableSecurePrivateServiceConnect",
        "project_allowlist": "projectAllowlist",
    },
)
class VertexAiEndpointPrivateServiceConnectConfig:
    def __init__(
        self,
        *,
        enable_private_service_connect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enable_secure_private_service_connect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param enable_private_service_connect: Required. If true, expose the IndexEndpoint via private service connect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enable_private_service_connect VertexAiEndpoint#enable_private_service_connect}
        :param enable_secure_private_service_connect: If set to true, enable secure private service connect with IAM authorization. Otherwise, private service connect will be done without authorization. Note latency will be slightly increased if authorization is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enable_secure_private_service_connect VertexAiEndpoint#enable_secure_private_service_connect}
        :param project_allowlist: A list of Projects from which the forwarding rule will target the service attachment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#project_allowlist VertexAiEndpoint#project_allowlist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e8a665630b427b8d4992b30c3118d074280fb78ef1440eb2e7edd24f2a09ba)
            check_type(argname="argument enable_private_service_connect", value=enable_private_service_connect, expected_type=type_hints["enable_private_service_connect"])
            check_type(argname="argument enable_secure_private_service_connect", value=enable_secure_private_service_connect, expected_type=type_hints["enable_secure_private_service_connect"])
            check_type(argname="argument project_allowlist", value=project_allowlist, expected_type=type_hints["project_allowlist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_private_service_connect": enable_private_service_connect,
        }
        if enable_secure_private_service_connect is not None:
            self._values["enable_secure_private_service_connect"] = enable_secure_private_service_connect
        if project_allowlist is not None:
            self._values["project_allowlist"] = project_allowlist

    @builtins.property
    def enable_private_service_connect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Required. If true, expose the IndexEndpoint via private service connect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enable_private_service_connect VertexAiEndpoint#enable_private_service_connect}
        '''
        result = self._values.get("enable_private_service_connect")
        assert result is not None, "Required property 'enable_private_service_connect' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def enable_secure_private_service_connect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, enable secure private service connect with IAM authorization.

        Otherwise, private service connect will be done without authorization. Note latency will be slightly increased if authorization is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#enable_secure_private_service_connect VertexAiEndpoint#enable_secure_private_service_connect}
        '''
        result = self._values.get("enable_secure_private_service_connect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_allowlist(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Projects from which the forwarding rule will target the service attachment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#project_allowlist VertexAiEndpoint#project_allowlist}
        '''
        result = self._values.get("project_allowlist")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointPrivateServiceConnectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointPrivateServiceConnectConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointPrivateServiceConnectConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecf51d7c03d710e7c8e09d5346b6c10df7c8ebe32aa6701c1fa6cb352d8e867f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableSecurePrivateServiceConnect")
    def reset_enable_secure_private_service_connect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableSecurePrivateServiceConnect", []))

    @jsii.member(jsii_name="resetProjectAllowlist")
    def reset_project_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectAllowlist", []))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateServiceConnectInput")
    def enable_private_service_connect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enablePrivateServiceConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="enableSecurePrivateServiceConnectInput")
    def enable_secure_private_service_connect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableSecurePrivateServiceConnectInput"))

    @builtins.property
    @jsii.member(jsii_name="projectAllowlistInput")
    def project_allowlist_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectAllowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="enablePrivateServiceConnect")
    def enable_private_service_connect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enablePrivateServiceConnect"))

    @enable_private_service_connect.setter
    def enable_private_service_connect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696b1bdb848ad3fdad1e3891063fda588d1c215e18ce7e9fac2457897080f788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePrivateServiceConnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableSecurePrivateServiceConnect")
    def enable_secure_private_service_connect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableSecurePrivateServiceConnect"))

    @enable_secure_private_service_connect.setter
    def enable_secure_private_service_connect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356af30744abfc3f42e2bb433b32c747c05fe78fabbd2323e5dc10c506a5a84c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableSecurePrivateServiceConnect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectAllowlist")
    def project_allowlist(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectAllowlist"))

    @project_allowlist.setter
    def project_allowlist(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4695bcf0b3d3387c1972f5dd17ff725c8102054383f0293958ab48a8f0c8e5e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectAllowlist", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiEndpointPrivateServiceConnectConfig]:
        return typing.cast(typing.Optional[VertexAiEndpointPrivateServiceConnectConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiEndpointPrivateServiceConnectConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86486284edb96602057edf04f0a5e6e9189b1167c540ebf35d467e2334c50afb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VertexAiEndpointTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#create VertexAiEndpoint#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#delete VertexAiEndpoint#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#update VertexAiEndpoint#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f892e3d1bd4ac373c407ff40ffe98d7acba1b11ac4d2d5f84cda9c2239c190a)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#create VertexAiEndpoint#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#delete VertexAiEndpoint#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_endpoint#update VertexAiEndpoint#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiEndpointTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiEndpointTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiEndpoint.VertexAiEndpointTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__726505bf6fa5a4472daf4fdbe92577a374dc2c9294bbb2146632fc9b26cf273e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__095f698ce603c0ee099dbf0c04c569960864b47660cedee48bdb6036ed65ba18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64230e1ac5af48c0329552cf6d8d7591d034a2a01fe1f5e767851d76936250c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb665d1a9b912ee0e6accb4fb6da091f7aa0c98347b60764fa9f9a08d17cfb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9473fec8633aeea63de21c34f080c4803a75beb708e7bdfcb79c77d006ce20be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VertexAiEndpoint",
    "VertexAiEndpointConfig",
    "VertexAiEndpointDeployedModels",
    "VertexAiEndpointDeployedModelsAutomaticResources",
    "VertexAiEndpointDeployedModelsAutomaticResourcesList",
    "VertexAiEndpointDeployedModelsAutomaticResourcesOutputReference",
    "VertexAiEndpointDeployedModelsDedicatedResources",
    "VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecs",
    "VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsList",
    "VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecsOutputReference",
    "VertexAiEndpointDeployedModelsDedicatedResourcesList",
    "VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpec",
    "VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecList",
    "VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpecOutputReference",
    "VertexAiEndpointDeployedModelsDedicatedResourcesOutputReference",
    "VertexAiEndpointDeployedModelsList",
    "VertexAiEndpointDeployedModelsOutputReference",
    "VertexAiEndpointDeployedModelsPrivateEndpoints",
    "VertexAiEndpointDeployedModelsPrivateEndpointsList",
    "VertexAiEndpointDeployedModelsPrivateEndpointsOutputReference",
    "VertexAiEndpointEncryptionSpec",
    "VertexAiEndpointEncryptionSpecOutputReference",
    "VertexAiEndpointPredictRequestResponseLoggingConfig",
    "VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination",
    "VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestinationOutputReference",
    "VertexAiEndpointPredictRequestResponseLoggingConfigOutputReference",
    "VertexAiEndpointPrivateServiceConnectConfig",
    "VertexAiEndpointPrivateServiceConnectConfigOutputReference",
    "VertexAiEndpointTimeouts",
    "VertexAiEndpointTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ae5843bb2578a6408d1e97a23d15183f0242a04c2b2be36592e31d6479cd7b9a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    location: builtins.str,
    name: builtins.str,
    dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_spec: typing.Optional[typing.Union[VertexAiEndpointEncryptionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    predict_request_response_logging_config: typing.Optional[typing.Union[VertexAiEndpointPredictRequestResponseLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_service_connect_config: typing.Optional[typing.Union[VertexAiEndpointPrivateServiceConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiEndpointTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_split: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__cec86b7c39a688992eb801a10e1c147db1bb4a563754a6b2f3abe0428c1934ad(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6b3521540e92bc86aa93bd5d644d5cbde809d6a304fcd47af5e8d563031c3d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d8a0e82f4137a459550bcc2f527956f3d1d5e6144444cd6b2a7d14973eee3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9946f68c9edb40c8107b697637c21693f2a12d757198583deec797ecc5f1ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc066f2603f3bb9a57107af2a3a7a7c1ac285e71acdd86cc40d4a11f88d8bd18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250c1d8645dbb2462121e16600dea6ce470283fd5a7c715300a546f14a40642f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b20707f2f1be903944b65b8435aa9359183c04fc88ab8e457850ab2346e036(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d1b6f7bd472f78ad0a669dba6d8db152d7f0649e9fbdcf132c8fef120452d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3825d9883af41452049dda5f372b3b9cda3446c0c273cb355871bd195c6d9160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de650bb74dc9d45a3c52710ce3b74ab54a63302692e07f3bc02aa0c2551ab24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e0db9754e4bb8ef99cb4534e023b835a089b55feb4e6d878c1c08864122622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5410a5e614d41f64c50ac1b1dece4c8a301897ec353e31c79d02d56a0714e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d721663393801d931c84712a91b1f254e4d844e028312c46feeb4ec3ed08389(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    location: builtins.str,
    name: builtins.str,
    dedicated_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_spec: typing.Optional[typing.Union[VertexAiEndpointEncryptionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    network: typing.Optional[builtins.str] = None,
    predict_request_response_logging_config: typing.Optional[typing.Union[VertexAiEndpointPredictRequestResponseLoggingConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    private_service_connect_config: typing.Optional[typing.Union[VertexAiEndpointPrivateServiceConnectConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiEndpointTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_split: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d8d09b2e259b4f5e9c357ee8e49501f7d7e718f7e2b2c5029b833fae8a8ab2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db30cb6b593f8cb1930b2a0d4af1fcb74c37a52973521b4a6c5de70a5d844f55(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85ebdac2149924738632916701cbd8cfe5dbf34ea1c846559d53530e92f74b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3537bc6d267d877f5799a9991b7fad45f5f981d0303e1d31021f938aa0393a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1df7aeac4ba12fa0a017c9e36b6a02ab9e838e6a911882808d833f65edbf42b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b83856f11073c075ac786f324283a6815901b2424841a18063dad61155c170(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b954ef3b654a72920177e2d3245012e3420d5e6f87f4e6e64c3c9377998aa89f(
    value: typing.Optional[VertexAiEndpointDeployedModelsAutomaticResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7995b879244923f14953cb9db182afb8909c8f1879ae7dc0e5465c1cb2687534(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff18cdecaf2282009873ee895b8b7c2fce4054dbb0bb8e8b2d3c0f531227f25(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fd1c11dfae88fe141b0a4eb959fdcddbff5f75d33cf97e799671c01aad4346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcf6ee4841b3036c22c2632da18a8d06aa273733cf95c340ac60adb7dc9cd58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f45f9521cff9ad9d81ec18486ef8d437db8e624ca9c3a13875426b969243e58(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5b6dbfc752eb03fbd3914cc66d492cc95dd809799977b395316286ac7090b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742468a1953a1211f014f5fae52327c3460b63a9d078e454863be5fb0c631a2b(
    value: typing.Optional[VertexAiEndpointDeployedModelsDedicatedResourcesAutoscalingMetricSpecs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1724121ec8d97b41ac38d2d2384ba7106a504c3c4fe0e93d04a003c473cd5b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e310f901afae398c4d0142b0b24756670592adf779da48d0d30934910496e8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a075fc98bfa135846e08cc70b5cea3923a64a24848d988b767e827a8e799e69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__293f96947cd45412580cc134dea4c6f8708827dfe3e3d7536a939f53b968c931(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d73902b240a2f5e36c8fbdf20bb992b3b67240af7cb1880a5bce385457ecea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feed58e5931d603f1b22bafd78b8c56d3c01a347ae32ec55feec66ab5324ade6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d2878bc1326465a2131a78e43e7e382590320605263bb1262067734518fd9f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d850dade41e0ff4bb910f860d1287a877df0d71183b8269e65188eb33e96b1e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7694be332e3b9606a625d65b52b248490e2f660ece14d357f553ac8b7f5bfc3f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c5f75f251a3e6ce6fe5912c60593204a21d15a187a5fbc48e3c4b1d0d9bd20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__303642129eb5178281c408ed134734aa9a1558c640db8981b8e5fb63c0477ead(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77bc59bf5626a675b4dabe679be0009150ab114bca7d5aaf0455a9be765cbe7d(
    value: typing.Optional[VertexAiEndpointDeployedModelsDedicatedResourcesMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b7e2b014ea53c2296dc1e8d460e4efbd31d7d73c85ad264addf44eb7c0d3af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a41c6c28f583f20847abcf66393ad8624044bce568de8d17ee7aa3150046b3(
    value: typing.Optional[VertexAiEndpointDeployedModelsDedicatedResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979c020c779dfce15507d21351076d4c5a0d9012ba92159f733a4225e8a4d376(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58203f85ce3481ff183a927029e9f95379307e701777b0fe2cb90971de3f346(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcddd6feb88daedb5742e32296e5ef10cb30336e1079aee0a9180025a56572dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be71699f6da28d903ffd41257f7b5693163a51826a595127fb608a583d46f35a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fe1f804951357ea2024520b8c27c871ac01417c2784f02ef0581f547f10e66(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c72641904a3c3eb4ad29d968b7345aca1a822a625c5f8599a6f2fc564d5a43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e5af3a15b33d023461facb1544b81a6c404241ec7f40fdb232469908be960d(
    value: typing.Optional[VertexAiEndpointDeployedModels],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470cb5aabe691f6fdc0b8eb5e7164a7e9e4f80203a3b1c62f62012fa847149c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a2da3c723263d269270ea2ed92838e193b1781cdb7a0ff9ef10db2ae63b687(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448d464fa0bca0ebce4bd09549c4f65ef449b5e1d6784f3a582d21d4bbc57edf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6377cad615a911ea494ca1b9dc1a2f88a2909da8a4e844b546cd186dbaf06e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec512184dfb9cef8f849eb5f3bcb840f9560725170ff6f519658fc4317811399(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b0e5679a9ffec71f7c165866b586a84870b752a223823d753c8b2787a76b9b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6001e7d137c950cdc16946176dd768cb3673cffcc5b513f0ddb271963ee735(
    value: typing.Optional[VertexAiEndpointDeployedModelsPrivateEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7904c6bc1d0e73b7aa75edaee52aaa0d383b97faf407241b7a45e1086835e17(
    *,
    kms_key_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c38e5917ee0364ab817567c6e2adefcc183c67caa983cff544b5a88c02c6e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf4ebad934e5e8d288f273c31033af42db608c2143f04869404453e5108ebf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0c7215d41bd02d795f129775e6c20c00d433c0735056c7a793c012d7c232b7(
    value: typing.Optional[VertexAiEndpointEncryptionSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ccd14c836ec093b1e2200d3b7bfbc0d6e01e409cbfbc29c5b40cf658b19d17b(
    *,
    bigquery_destination: typing.Optional[typing.Union[VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sampling_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060399abf67c905fe5691b460dc45eb213058a9d83ce09259d3506712cd2581f(
    *,
    output_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5643b52e7cdc77816cebcb2fa2cd922ebc1caa2328dc9443b567e1384c8d6beb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42aea9dc0a00eb019738ddb2fef43fe94a8a723491896dd7d3e9693a80200800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9320b3505678dad8c808e5343fff62a16d387bade6addbe3724b9ac472b6e7d3(
    value: typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfigBigqueryDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f07ba4f8e6351eeb1b6809f43425476a7be527a17a14bd0003d983f93e6b0dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f28a022cf2eefd8861090087c3b3be9b2cd7794697922f073e1a16ffb9320d5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4cba4fc3cc4d8541737361571f5449c658f56c7b46d49d9714286e2b1f0c32(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbef574862749877112310a6b0a9ce3ba3e9b4ab9498ed254f11d4ea1d6bdb4(
    value: typing.Optional[VertexAiEndpointPredictRequestResponseLoggingConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e8a665630b427b8d4992b30c3118d074280fb78ef1440eb2e7edd24f2a09ba(
    *,
    enable_private_service_connect: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    enable_secure_private_service_connect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_allowlist: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf51d7c03d710e7c8e09d5346b6c10df7c8ebe32aa6701c1fa6cb352d8e867f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696b1bdb848ad3fdad1e3891063fda588d1c215e18ce7e9fac2457897080f788(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356af30744abfc3f42e2bb433b32c747c05fe78fabbd2323e5dc10c506a5a84c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4695bcf0b3d3387c1972f5dd17ff725c8102054383f0293958ab48a8f0c8e5e1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86486284edb96602057edf04f0a5e6e9189b1167c540ebf35d467e2334c50afb(
    value: typing.Optional[VertexAiEndpointPrivateServiceConnectConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f892e3d1bd4ac373c407ff40ffe98d7acba1b11ac4d2d5f84cda9c2239c190a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726505bf6fa5a4472daf4fdbe92577a374dc2c9294bbb2146632fc9b26cf273e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095f698ce603c0ee099dbf0c04c569960864b47660cedee48bdb6036ed65ba18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64230e1ac5af48c0329552cf6d8d7591d034a2a01fe1f5e767851d76936250c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb665d1a9b912ee0e6accb4fb6da091f7aa0c98347b60764fa9f9a08d17cfb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9473fec8633aeea63de21c34f080c4803a75beb708e7bdfcb79c77d006ce20be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiEndpointTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

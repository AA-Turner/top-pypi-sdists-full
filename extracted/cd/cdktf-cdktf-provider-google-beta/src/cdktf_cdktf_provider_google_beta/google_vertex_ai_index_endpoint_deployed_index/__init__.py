r'''
# `google_vertex_ai_index_endpoint_deployed_index`

Refer to the Terraform Registry for docs: [`google_vertex_ai_index_endpoint_deployed_index`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index).
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


class GoogleVertexAiIndexEndpointDeployedIndex(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index google_vertex_ai_index_endpoint_deployed_index}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        deployed_index_id: builtins.str,
        index: builtins.str,
        index_endpoint: builtins.str,
        automatic_resources: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources", typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_resources: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        deployed_index_auth_config: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_group: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_access_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        reserved_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index google_vertex_ai_index_endpoint_deployed_index} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param deployed_index_id: The user specified ID of the DeployedIndex. The ID can be up to 128 characters long and must start with a letter and only contain letters, numbers, and underscores. The ID must be unique within the project it is created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployed_index_id GoogleVertexAiIndexEndpointDeployedIndex#deployed_index_id}
        :param index: The name of the Index this is the deployment of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#index GoogleVertexAiIndexEndpointDeployedIndex#index}
        :param index_endpoint: Identifies the index endpoint. Must be in the format 'projects/{{project}}/locations/{{region}}/indexEndpoints/{{indexEndpoint}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#index_endpoint GoogleVertexAiIndexEndpointDeployedIndex#index_endpoint}
        :param automatic_resources: automatic_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#automatic_resources GoogleVertexAiIndexEndpointDeployedIndex#automatic_resources}
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#dedicated_resources GoogleVertexAiIndexEndpointDeployedIndex#dedicated_resources}
        :param deployed_index_auth_config: deployed_index_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployed_index_auth_config GoogleVertexAiIndexEndpointDeployedIndex#deployed_index_auth_config}
        :param deployment_group: The deployment group can be no longer than 64 characters (eg: 'test', 'prod'). If not set, we will use the 'default' deployment group. Creating deployment_groups with reserved_ip_ranges is a recommended practice when the peered network has multiple peering ranges. This creates your deployments from predictable IP spaces for easier traffic administration. Also, one deployment_group (except 'default') can only be used with the same reserved_ip_ranges which means if the deployment_group has been used with reserved_ip_ranges: [a, b, c], using it with [a, b] or [d, e] is disallowed. `See the official documentation here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.indexEndpoints#DeployedIndex.FIELDS.deployment_group>`_. Note: we only support up to 5 deployment groups (not including 'default'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployment_group GoogleVertexAiIndexEndpointDeployedIndex#deployment_group}
        :param display_name: The display name of the Index. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#display_name GoogleVertexAiIndexEndpointDeployedIndex#display_name}
        :param enable_access_logging: If true, private endpoint's access logs are sent to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#enable_access_logging GoogleVertexAiIndexEndpointDeployedIndex#enable_access_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#id GoogleVertexAiIndexEndpointDeployedIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param reserved_ip_ranges: A list of reserved ip ranges under the VPC network that can be used for this DeployedIndex. If set, we will deploy the index within the provided ip ranges. Otherwise, the index might be deployed to any ip ranges under the provided VPC network. The value should be the name of the address (https://cloud.google.com/compute/docs/reference/rest/v1/addresses) Example: ['vertex-ai-ip-range']. For more information about subnets and network IP ranges, please see https://cloud.google.com/vpc/docs/subnets#manually_created_subnet_ip_ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#reserved_ip_ranges GoogleVertexAiIndexEndpointDeployedIndex#reserved_ip_ranges}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#timeouts GoogleVertexAiIndexEndpointDeployedIndex#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50aec73e18913adb7f172a292414aaa449b2af358fd2c3833b81febc9b3a6fd2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVertexAiIndexEndpointDeployedIndexConfig(
            deployed_index_id=deployed_index_id,
            index=index,
            index_endpoint=index_endpoint,
            automatic_resources=automatic_resources,
            dedicated_resources=dedicated_resources,
            deployed_index_auth_config=deployed_index_auth_config,
            deployment_group=deployment_group,
            display_name=display_name,
            enable_access_logging=enable_access_logging,
            id=id,
            reserved_ip_ranges=reserved_ip_ranges,
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
        '''Generates CDKTF code for importing a GoogleVertexAiIndexEndpointDeployedIndex resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVertexAiIndexEndpointDeployedIndex to import.
        :param import_from_id: The id of the existing GoogleVertexAiIndexEndpointDeployedIndex that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVertexAiIndexEndpointDeployedIndex to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bac9ca9fecad20f65cd4d67ada5cc29146cf4dcb1d340a126a6938b719ca84c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAutomaticResources")
    def put_automatic_resources(
        self,
        *,
        max_replica_count: typing.Optional[jsii.Number] = None,
        min_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If maxReplicaCount is not set, the default value is minReplicaCount. The max allowed replica count is 1000. The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, a no upper bound for scaling under heavy traffic will be assume, though Vertex AI may be unable to scale beyond certain replica number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#max_replica_count GoogleVertexAiIndexEndpointDeployedIndex#max_replica_count}
        :param min_replica_count: The minimum number of replicas this DeployedModel will be always deployed on. If minReplicaCount is not set, the default value is 2 (we don't provide SLA when minReplicaCount=1). If traffic against it increases, it may dynamically be deployed onto more replicas up to `maxReplicaCount <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/AutomaticResources#FIELDS.max_replica_count>`_, and as traffic decreases, some of these extra replicas may be freed. If the requested value is too large, the deployment will error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#min_replica_count GoogleVertexAiIndexEndpointDeployedIndex#min_replica_count}
        '''
        value = GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources(
            max_replica_count=max_replica_count, min_replica_count=min_replica_count
        )

        return typing.cast(None, jsii.invoke(self, "putAutomaticResources", [value]))

    @jsii.member(jsii_name="putDedicatedResources")
    def put_dedicated_resources(
        self,
        *,
        machine_spec: typing.Union["GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        max_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#machine_spec GoogleVertexAiIndexEndpointDeployedIndex#machine_spec}
        :param min_replica_count: The minimum number of machine replicas this DeployedModel will be always deployed on. This value must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#min_replica_count GoogleVertexAiIndexEndpointDeployedIndex#min_replica_count}
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If maxReplicaCount is not set, the default value is minReplicaCount Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#max_replica_count GoogleVertexAiIndexEndpointDeployedIndex#max_replica_count}
        '''
        value = GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources(
            machine_spec=machine_spec,
            min_replica_count=min_replica_count,
            max_replica_count=max_replica_count,
        )

        return typing.cast(None, jsii.invoke(self, "putDedicatedResources", [value]))

    @jsii.member(jsii_name="putDeployedIndexAuthConfig")
    def put_deployed_index_auth_config(
        self,
        *,
        auth_provider: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_provider: auth_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#auth_provider GoogleVertexAiIndexEndpointDeployedIndex#auth_provider}
        '''
        value = GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig(
            auth_provider=auth_provider
        )

        return typing.cast(None, jsii.invoke(self, "putDeployedIndexAuthConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#create GoogleVertexAiIndexEndpointDeployedIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#delete GoogleVertexAiIndexEndpointDeployedIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#update GoogleVertexAiIndexEndpointDeployedIndex#update}.
        '''
        value = GoogleVertexAiIndexEndpointDeployedIndexTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAutomaticResources")
    def reset_automatic_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticResources", []))

    @jsii.member(jsii_name="resetDedicatedResources")
    def reset_dedicated_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedResources", []))

    @jsii.member(jsii_name="resetDeployedIndexAuthConfig")
    def reset_deployed_index_auth_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeployedIndexAuthConfig", []))

    @jsii.member(jsii_name="resetDeploymentGroup")
    def reset_deployment_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeploymentGroup", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEnableAccessLogging")
    def reset_enable_access_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableAccessLogging", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetReservedIpRanges")
    def reset_reserved_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReservedIpRanges", []))

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
    @jsii.member(jsii_name="automaticResources")
    def automatic_resources(
        self,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference":
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference", jsii.get(self, "automaticResources"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResources")
    def dedicated_resources(
        self,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference":
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference", jsii.get(self, "dedicatedResources"))

    @builtins.property
    @jsii.member(jsii_name="deployedIndexAuthConfig")
    def deployed_index_auth_config(
        self,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference":
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference", jsii.get(self, "deployedIndexAuthConfig"))

    @builtins.property
    @jsii.member(jsii_name="indexSyncTime")
    def index_sync_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexSyncTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpoints")
    def private_endpoints(
        self,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsList":
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsList", jsii.get(self, "privateEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="automaticResourcesInput")
    def automatic_resources_input(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources"]:
        return typing.cast(typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources"], jsii.get(self, "automaticResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourcesInput")
    def dedicated_resources_input(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources"]:
        return typing.cast(typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources"], jsii.get(self, "dedicatedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="deployedIndexAuthConfigInput")
    def deployed_index_auth_config_input(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig"]:
        return typing.cast(typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig"], jsii.get(self, "deployedIndexAuthConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deployedIndexIdInput")
    def deployed_index_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deployedIndexIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentGroupInput")
    def deployment_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enableAccessLoggingInput")
    def enable_access_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableAccessLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexEndpointInput")
    def index_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedIpRangesInput")
    def reserved_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "reservedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiIndexEndpointDeployedIndexTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiIndexEndpointDeployedIndexTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deployedIndexId")
    def deployed_index_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployedIndexId"))

    @deployed_index_id.setter
    def deployed_index_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb02087327674ec9ce5f70f23f7de70006356e65d8aa273e1ee0f348aceac57a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployedIndexId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentGroup")
    def deployment_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroup"))

    @deployment_group.setter
    def deployment_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a90007962900e229672b0999021909d7a86ad2ee9de0c48bb19704eec754a56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4c2d4d84692cbca5431cd2afade7e5f360f40ff2bc33c7aadeb94ae395d4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableAccessLogging")
    def enable_access_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableAccessLogging"))

    @enable_access_logging.setter
    def enable_access_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67e4e5d43d7d55aa5a8399b6aa60efa5572842cdb57cf6e1887c264c8155bd80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAccessLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b30b4f7e399db3b50f2c147e06f97d4c016393c486ea9accc54827a8d7849d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84c05d18ec7b1d500bda32f7c1c7b5320dd2725eafdac2ab5b4ff25a3b395228)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexEndpoint")
    def index_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexEndpoint"))

    @index_endpoint.setter
    def index_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f170af35d8871b866c300de3b7d1e7999bae120648bf49672d10d2f452e9b4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRanges")
    def reserved_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "reservedIpRanges"))

    @reserved_ip_ranges.setter
    def reserved_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76038e41d2400673cc8c6a7a041730a60564b0c3ff58b595916cbafc666c4b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRanges", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources",
    jsii_struct_bases=[],
    name_mapping={
        "max_replica_count": "maxReplicaCount",
        "min_replica_count": "minReplicaCount",
    },
)
class GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources:
    def __init__(
        self,
        *,
        max_replica_count: typing.Optional[jsii.Number] = None,
        min_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If maxReplicaCount is not set, the default value is minReplicaCount. The max allowed replica count is 1000. The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, a no upper bound for scaling under heavy traffic will be assume, though Vertex AI may be unable to scale beyond certain replica number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#max_replica_count GoogleVertexAiIndexEndpointDeployedIndex#max_replica_count}
        :param min_replica_count: The minimum number of replicas this DeployedModel will be always deployed on. If minReplicaCount is not set, the default value is 2 (we don't provide SLA when minReplicaCount=1). If traffic against it increases, it may dynamically be deployed onto more replicas up to `maxReplicaCount <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/AutomaticResources#FIELDS.max_replica_count>`_, and as traffic decreases, some of these extra replicas may be freed. If the requested value is too large, the deployment will error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#min_replica_count GoogleVertexAiIndexEndpointDeployedIndex#min_replica_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f588c855858762bac523e08f618d0362b270bb062257afc481ba138c3656d3)
            check_type(argname="argument max_replica_count", value=max_replica_count, expected_type=type_hints["max_replica_count"])
            check_type(argname="argument min_replica_count", value=min_replica_count, expected_type=type_hints["min_replica_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_replica_count is not None:
            self._values["max_replica_count"] = max_replica_count
        if min_replica_count is not None:
            self._values["min_replica_count"] = min_replica_count

    @builtins.property
    def max_replica_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases.

        If maxReplicaCount is not set, the default value is minReplicaCount. The max allowed replica count is 1000.

        The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, a no upper bound for scaling under heavy traffic will be assume, though Vertex AI may be unable to scale beyond certain replica number.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#max_replica_count GoogleVertexAiIndexEndpointDeployedIndex#max_replica_count}
        '''
        result = self._values.get("max_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_replica_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of replicas this DeployedModel will be always deployed on.

        If minReplicaCount is not set, the default value is 2 (we don't provide SLA when minReplicaCount=1).

        If traffic against it increases, it may dynamically be deployed onto more replicas up to `maxReplicaCount <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/AutomaticResources#FIELDS.max_replica_count>`_, and as traffic decreases, some of these extra replicas may be freed. If the requested value is too large, the deployment will error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#min_replica_count GoogleVertexAiIndexEndpointDeployedIndex#min_replica_count}
        '''
        result = self._values.get("min_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe0f22b81ee59b12b0c9a351c30d75d2bd8152edd71153b3c31063b68f4742d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxReplicaCount")
    def reset_max_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxReplicaCount", []))

    @jsii.member(jsii_name="resetMinReplicaCount")
    def reset_min_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinReplicaCount", []))

    @builtins.property
    @jsii.member(jsii_name="maxReplicaCountInput")
    def max_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicaCountInput")
    def min_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicaCount")
    def max_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicaCount"))

    @max_replica_count.setter
    def max_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17ca362919578aeb1b94761df4c9253cdef517a2fca959d7a694c526f2a0055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @min_replica_count.setter
    def min_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19a401dd85039d2923396908b37bf60b1d7c3e3f53ce1a13ab3521e56174d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7175185c691a411edd1197ed1b7f8668e9dfc47069a7a17ebc2057e80add7bc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "deployed_index_id": "deployedIndexId",
        "index": "index",
        "index_endpoint": "indexEndpoint",
        "automatic_resources": "automaticResources",
        "dedicated_resources": "dedicatedResources",
        "deployed_index_auth_config": "deployedIndexAuthConfig",
        "deployment_group": "deploymentGroup",
        "display_name": "displayName",
        "enable_access_logging": "enableAccessLogging",
        "id": "id",
        "reserved_ip_ranges": "reservedIpRanges",
        "timeouts": "timeouts",
    },
)
class GoogleVertexAiIndexEndpointDeployedIndexConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        deployed_index_id: builtins.str,
        index: builtins.str,
        index_endpoint: builtins.str,
        automatic_resources: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources, typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_resources: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        deployed_index_auth_config: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_group: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_access_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        reserved_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param deployed_index_id: The user specified ID of the DeployedIndex. The ID can be up to 128 characters long and must start with a letter and only contain letters, numbers, and underscores. The ID must be unique within the project it is created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployed_index_id GoogleVertexAiIndexEndpointDeployedIndex#deployed_index_id}
        :param index: The name of the Index this is the deployment of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#index GoogleVertexAiIndexEndpointDeployedIndex#index}
        :param index_endpoint: Identifies the index endpoint. Must be in the format 'projects/{{project}}/locations/{{region}}/indexEndpoints/{{indexEndpoint}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#index_endpoint GoogleVertexAiIndexEndpointDeployedIndex#index_endpoint}
        :param automatic_resources: automatic_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#automatic_resources GoogleVertexAiIndexEndpointDeployedIndex#automatic_resources}
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#dedicated_resources GoogleVertexAiIndexEndpointDeployedIndex#dedicated_resources}
        :param deployed_index_auth_config: deployed_index_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployed_index_auth_config GoogleVertexAiIndexEndpointDeployedIndex#deployed_index_auth_config}
        :param deployment_group: The deployment group can be no longer than 64 characters (eg: 'test', 'prod'). If not set, we will use the 'default' deployment group. Creating deployment_groups with reserved_ip_ranges is a recommended practice when the peered network has multiple peering ranges. This creates your deployments from predictable IP spaces for easier traffic administration. Also, one deployment_group (except 'default') can only be used with the same reserved_ip_ranges which means if the deployment_group has been used with reserved_ip_ranges: [a, b, c], using it with [a, b] or [d, e] is disallowed. `See the official documentation here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.indexEndpoints#DeployedIndex.FIELDS.deployment_group>`_. Note: we only support up to 5 deployment groups (not including 'default'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployment_group GoogleVertexAiIndexEndpointDeployedIndex#deployment_group}
        :param display_name: The display name of the Index. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#display_name GoogleVertexAiIndexEndpointDeployedIndex#display_name}
        :param enable_access_logging: If true, private endpoint's access logs are sent to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#enable_access_logging GoogleVertexAiIndexEndpointDeployedIndex#enable_access_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#id GoogleVertexAiIndexEndpointDeployedIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param reserved_ip_ranges: A list of reserved ip ranges under the VPC network that can be used for this DeployedIndex. If set, we will deploy the index within the provided ip ranges. Otherwise, the index might be deployed to any ip ranges under the provided VPC network. The value should be the name of the address (https://cloud.google.com/compute/docs/reference/rest/v1/addresses) Example: ['vertex-ai-ip-range']. For more information about subnets and network IP ranges, please see https://cloud.google.com/vpc/docs/subnets#manually_created_subnet_ip_ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#reserved_ip_ranges GoogleVertexAiIndexEndpointDeployedIndex#reserved_ip_ranges}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#timeouts GoogleVertexAiIndexEndpointDeployedIndex#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automatic_resources, dict):
            automatic_resources = GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources(**automatic_resources)
        if isinstance(dedicated_resources, dict):
            dedicated_resources = GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources(**dedicated_resources)
        if isinstance(deployed_index_auth_config, dict):
            deployed_index_auth_config = GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig(**deployed_index_auth_config)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiIndexEndpointDeployedIndexTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267fd43d821520ce02006af5ff90cf2b7009f72c81d9508cfbf68910ed5a2dcf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument deployed_index_id", value=deployed_index_id, expected_type=type_hints["deployed_index_id"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument index_endpoint", value=index_endpoint, expected_type=type_hints["index_endpoint"])
            check_type(argname="argument automatic_resources", value=automatic_resources, expected_type=type_hints["automatic_resources"])
            check_type(argname="argument dedicated_resources", value=dedicated_resources, expected_type=type_hints["dedicated_resources"])
            check_type(argname="argument deployed_index_auth_config", value=deployed_index_auth_config, expected_type=type_hints["deployed_index_auth_config"])
            check_type(argname="argument deployment_group", value=deployment_group, expected_type=type_hints["deployment_group"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument enable_access_logging", value=enable_access_logging, expected_type=type_hints["enable_access_logging"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument reserved_ip_ranges", value=reserved_ip_ranges, expected_type=type_hints["reserved_ip_ranges"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployed_index_id": deployed_index_id,
            "index": index,
            "index_endpoint": index_endpoint,
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
        if automatic_resources is not None:
            self._values["automatic_resources"] = automatic_resources
        if dedicated_resources is not None:
            self._values["dedicated_resources"] = dedicated_resources
        if deployed_index_auth_config is not None:
            self._values["deployed_index_auth_config"] = deployed_index_auth_config
        if deployment_group is not None:
            self._values["deployment_group"] = deployment_group
        if display_name is not None:
            self._values["display_name"] = display_name
        if enable_access_logging is not None:
            self._values["enable_access_logging"] = enable_access_logging
        if id is not None:
            self._values["id"] = id
        if reserved_ip_ranges is not None:
            self._values["reserved_ip_ranges"] = reserved_ip_ranges
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
    def deployed_index_id(self) -> builtins.str:
        '''The user specified ID of the DeployedIndex.

        The ID can be up to 128 characters long and must start with a letter and only contain letters, numbers, and underscores. The ID must be unique within the project it is created in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployed_index_id GoogleVertexAiIndexEndpointDeployedIndex#deployed_index_id}
        '''
        result = self._values.get("deployed_index_id")
        assert result is not None, "Required property 'deployed_index_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''The name of the Index this is the deployment of.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#index GoogleVertexAiIndexEndpointDeployedIndex#index}
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index_endpoint(self) -> builtins.str:
        '''Identifies the index endpoint. Must be in the format 'projects/{{project}}/locations/{{region}}/indexEndpoints/{{indexEndpoint}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#index_endpoint GoogleVertexAiIndexEndpointDeployedIndex#index_endpoint}
        '''
        result = self._values.get("index_endpoint")
        assert result is not None, "Required property 'index_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automatic_resources(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources]:
        '''automatic_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#automatic_resources GoogleVertexAiIndexEndpointDeployedIndex#automatic_resources}
        '''
        result = self._values.get("automatic_resources")
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources], result)

    @builtins.property
    def dedicated_resources(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources"]:
        '''dedicated_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#dedicated_resources GoogleVertexAiIndexEndpointDeployedIndex#dedicated_resources}
        '''
        result = self._values.get("dedicated_resources")
        return typing.cast(typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources"], result)

    @builtins.property
    def deployed_index_auth_config(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig"]:
        '''deployed_index_auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployed_index_auth_config GoogleVertexAiIndexEndpointDeployedIndex#deployed_index_auth_config}
        '''
        result = self._values.get("deployed_index_auth_config")
        return typing.cast(typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig"], result)

    @builtins.property
    def deployment_group(self) -> typing.Optional[builtins.str]:
        '''The deployment group can be no longer than 64 characters (eg: 'test', 'prod').

        If not set, we will use the 'default' deployment group.
        Creating deployment_groups with reserved_ip_ranges is a recommended practice when the peered network has multiple peering ranges. This creates your deployments from predictable IP spaces for easier traffic administration. Also, one deployment_group (except 'default') can only be used with the same reserved_ip_ranges which means if the deployment_group has been used with reserved_ip_ranges: [a, b, c], using it with [a, b] or [d, e] is disallowed. `See the official documentation here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.indexEndpoints#DeployedIndex.FIELDS.deployment_group>`_.
        Note: we only support up to 5 deployment groups (not including 'default').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#deployment_group GoogleVertexAiIndexEndpointDeployedIndex#deployment_group}
        '''
        result = self._values.get("deployment_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Index.

        The name can be up to 128 characters long and can consist of any UTF-8 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#display_name GoogleVertexAiIndexEndpointDeployedIndex#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_access_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, private endpoint's access logs are sent to Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#enable_access_logging GoogleVertexAiIndexEndpointDeployedIndex#enable_access_logging}
        '''
        result = self._values.get("enable_access_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#id GoogleVertexAiIndexEndpointDeployedIndex#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of reserved ip ranges under the VPC network that can be used for this DeployedIndex.

        If set, we will deploy the index within the provided ip ranges. Otherwise, the index might be deployed to any ip ranges under the provided VPC network.

        The value should be the name of the address (https://cloud.google.com/compute/docs/reference/rest/v1/addresses) Example: ['vertex-ai-ip-range'].

        For more information about subnets and network IP ranges, please see https://cloud.google.com/vpc/docs/subnets#manually_created_subnet_ip_ranges.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#reserved_ip_ranges GoogleVertexAiIndexEndpointDeployedIndex#reserved_ip_ranges}
        '''
        result = self._values.get("reserved_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#timeouts GoogleVertexAiIndexEndpointDeployedIndex#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources",
    jsii_struct_bases=[],
    name_mapping={
        "machine_spec": "machineSpec",
        "min_replica_count": "minReplicaCount",
        "max_replica_count": "maxReplicaCount",
    },
)
class GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources:
    def __init__(
        self,
        *,
        machine_spec: typing.Union["GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        max_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#machine_spec GoogleVertexAiIndexEndpointDeployedIndex#machine_spec}
        :param min_replica_count: The minimum number of machine replicas this DeployedModel will be always deployed on. This value must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#min_replica_count GoogleVertexAiIndexEndpointDeployedIndex#min_replica_count}
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If maxReplicaCount is not set, the default value is minReplicaCount Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#max_replica_count GoogleVertexAiIndexEndpointDeployedIndex#max_replica_count}
        '''
        if isinstance(machine_spec, dict):
            machine_spec = GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec(**machine_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c354bf6657c7ee710b2753ca97b68f4e4c4302efe7af57b481863a453c187dd)
            check_type(argname="argument machine_spec", value=machine_spec, expected_type=type_hints["machine_spec"])
            check_type(argname="argument min_replica_count", value=min_replica_count, expected_type=type_hints["min_replica_count"])
            check_type(argname="argument max_replica_count", value=max_replica_count, expected_type=type_hints["max_replica_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "machine_spec": machine_spec,
            "min_replica_count": min_replica_count,
        }
        if max_replica_count is not None:
            self._values["max_replica_count"] = max_replica_count

    @builtins.property
    def machine_spec(
        self,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec":
        '''machine_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#machine_spec GoogleVertexAiIndexEndpointDeployedIndex#machine_spec}
        '''
        result = self._values.get("machine_spec")
        assert result is not None, "Required property 'machine_spec' is missing"
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec", result)

    @builtins.property
    def min_replica_count(self) -> jsii.Number:
        '''The minimum number of machine replicas this DeployedModel will be always deployed on.

        This value must be greater than or equal to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#min_replica_count GoogleVertexAiIndexEndpointDeployedIndex#min_replica_count}
        '''
        result = self._values.get("min_replica_count")
        assert result is not None, "Required property 'min_replica_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_replica_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases.

        If maxReplicaCount is not set, the default value is minReplicaCount

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#max_replica_count GoogleVertexAiIndexEndpointDeployedIndex#max_replica_count}
        '''
        result = self._values.get("max_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec",
    jsii_struct_bases=[],
    name_mapping={"machine_type": "machineType"},
)
class GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec:
    def __init__(self, *, machine_type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_ See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_. For `DeployedModel <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints#DeployedModel>`_ this field is optional, and the default value is n1-standard-2. For `BatchPredictionJob <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.batchPredictionJobs#BatchPredictionJob>`_ or as part of `WorkerPoolSpec <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#WorkerPoolSpec>`_ this field is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#machine_type GoogleVertexAiIndexEndpointDeployedIndex#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bc1557f342cdbc3368c5ae87bccadb462100641428e4036e2febcaaf0d746b)
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if machine_type is not None:
            self._values["machine_type"] = machine_type

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The type of the machine.

        See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_

        See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_.

        For `DeployedModel <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints#DeployedModel>`_ this field is optional, and the default value is n1-standard-2. For `BatchPredictionJob <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.batchPredictionJobs#BatchPredictionJob>`_ or as part of `WorkerPoolSpec <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#WorkerPoolSpec>`_ this field is required.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#machine_type GoogleVertexAiIndexEndpointDeployedIndex#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44120227bf0e87b30a38cb3d4ca293d6a5f86fa184c0a532eceba5f910eb0646)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fff575b83b953538f121e522381b4ffba85b18579868b10948d7f929f4dc44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc94f3cf7dc2febcd82d5f63657bf3d47f078c9d4e43c3ae2ae7f1ae58b0989c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5142e8a629c2ecbbd29413b37e3a709b845bf0791efebbc78eb87e01d84ea77d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMachineSpec")
    def put_machine_spec(
        self,
        *,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_ See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_. For `DeployedModel <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints#DeployedModel>`_ this field is optional, and the default value is n1-standard-2. For `BatchPredictionJob <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.batchPredictionJobs#BatchPredictionJob>`_ or as part of `WorkerPoolSpec <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#WorkerPoolSpec>`_ this field is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#machine_type GoogleVertexAiIndexEndpointDeployedIndex#machine_type}
        '''
        value = GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec(
            machine_type=machine_type
        )

        return typing.cast(None, jsii.invoke(self, "putMachineSpec", [value]))

    @jsii.member(jsii_name="resetMaxReplicaCount")
    def reset_max_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxReplicaCount", []))

    @builtins.property
    @jsii.member(jsii_name="machineSpec")
    def machine_spec(
        self,
    ) -> GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference:
        return typing.cast(GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference, jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="machineSpecInput")
    def machine_spec_input(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec], jsii.get(self, "machineSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicaCountInput")
    def max_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minReplicaCountInput")
    def min_replica_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minReplicaCountInput"))

    @builtins.property
    @jsii.member(jsii_name="maxReplicaCount")
    def max_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxReplicaCount"))

    @max_replica_count.setter
    def max_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80557ace5f35db8b493207d76358132a557fff266da40c5d146f271044ba257c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @min_replica_count.setter
    def min_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1675fbf20932200dc8880d95f2e27ccc331a820f1c4d9cc8bfb04dcc77a4a71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3ac59bf8fec3dca3460057e370edffaebbea5a16ea3d431673eeb440fb459a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig",
    jsii_struct_bases=[],
    name_mapping={"auth_provider": "authProvider"},
)
class GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig:
    def __init__(
        self,
        *,
        auth_provider: typing.Optional[typing.Union["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_provider: auth_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#auth_provider GoogleVertexAiIndexEndpointDeployedIndex#auth_provider}
        '''
        if isinstance(auth_provider, dict):
            auth_provider = GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider(**auth_provider)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4431bf476369e68c0d14b27cf01d8533327372615cf35bb5a6a0ce7f5b435583)
            check_type(argname="argument auth_provider", value=auth_provider, expected_type=type_hints["auth_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_provider is not None:
            self._values["auth_provider"] = auth_provider

    @builtins.property
    def auth_provider(
        self,
    ) -> typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider"]:
        '''auth_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#auth_provider GoogleVertexAiIndexEndpointDeployedIndex#auth_provider}
        '''
        result = self._values.get("auth_provider")
        return typing.cast(typing.Optional["GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider",
    jsii_struct_bases=[],
    name_mapping={"allowed_issuers": "allowedIssuers", "audiences": "audiences"},
)
class GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider:
    def __init__(
        self,
        *,
        allowed_issuers: typing.Optional[typing.Sequence[builtins.str]] = None,
        audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_issuers: A list of allowed JWT issuers. Each entry must be a valid Google service account, in the following format: service-account-name@project-id.iam.gserviceaccount.com Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#allowed_issuers GoogleVertexAiIndexEndpointDeployedIndex#allowed_issuers}
        :param audiences: The list of JWT audiences. that are allowed to access. A JWT containing any of these audiences will be accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#audiences GoogleVertexAiIndexEndpointDeployedIndex#audiences}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e499de1e932d3d3793bef936865aa5c6fba72aa4646fbd6de6bb398294ddcc)
            check_type(argname="argument allowed_issuers", value=allowed_issuers, expected_type=type_hints["allowed_issuers"])
            check_type(argname="argument audiences", value=audiences, expected_type=type_hints["audiences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_issuers is not None:
            self._values["allowed_issuers"] = allowed_issuers
        if audiences is not None:
            self._values["audiences"] = audiences

    @builtins.property
    def allowed_issuers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of allowed JWT issuers.

        Each entry must be a valid Google service account, in the following format: service-account-name@project-id.iam.gserviceaccount.com

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#allowed_issuers GoogleVertexAiIndexEndpointDeployedIndex#allowed_issuers}
        '''
        result = self._values.get("allowed_issuers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of JWT audiences.

        that are allowed to access. A JWT containing any of these audiences will be accepted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#audiences GoogleVertexAiIndexEndpointDeployedIndex#audiences}
        '''
        result = self._values.get("audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab00ff3a8bf1a5e4d50f5a147046e4fc6cb5139e85bee97e12423f14c51c1cb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedIssuers")
    def reset_allowed_issuers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIssuers", []))

    @jsii.member(jsii_name="resetAudiences")
    def reset_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudiences", []))

    @builtins.property
    @jsii.member(jsii_name="allowedIssuersInput")
    def allowed_issuers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIssuersInput"))

    @builtins.property
    @jsii.member(jsii_name="audiencesInput")
    def audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "audiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIssuers")
    def allowed_issuers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIssuers"))

    @allowed_issuers.setter
    def allowed_issuers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92b18df37307f05c8c6e49d0a59fa34d22dbec0ae8beca663057cd0cb2882c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIssuers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="audiences")
    def audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "audiences"))

    @audiences.setter
    def audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e35f9405934ef39030a4fe146a40e00b3af4cb8b5e7f9dc60b5949170e67b47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3f227cf9dedb9f0f6f50e68ce1ff81036874c73036376a61ba3598d561b32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1aae87b1d96e18365d20ce6d102b5250efd359c40d7fc27d9f8dade557600a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAuthProvider")
    def put_auth_provider(
        self,
        *,
        allowed_issuers: typing.Optional[typing.Sequence[builtins.str]] = None,
        audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_issuers: A list of allowed JWT issuers. Each entry must be a valid Google service account, in the following format: service-account-name@project-id.iam.gserviceaccount.com Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#allowed_issuers GoogleVertexAiIndexEndpointDeployedIndex#allowed_issuers}
        :param audiences: The list of JWT audiences. that are allowed to access. A JWT containing any of these audiences will be accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#audiences GoogleVertexAiIndexEndpointDeployedIndex#audiences}
        '''
        value = GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider(
            allowed_issuers=allowed_issuers, audiences=audiences
        )

        return typing.cast(None, jsii.invoke(self, "putAuthProvider", [value]))

    @jsii.member(jsii_name="resetAuthProvider")
    def reset_auth_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthProvider", []))

    @builtins.property
    @jsii.member(jsii_name="authProvider")
    def auth_provider(
        self,
    ) -> GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference:
        return typing.cast(GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference, jsii.get(self, "authProvider"))

    @builtins.property
    @jsii.member(jsii_name="authProviderInput")
    def auth_provider_input(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider], jsii.get(self, "authProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959fcc6805ba7aef1b2952077684eaf808585cf7046fa28e60a4c639130a0533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60205efe05b76ba7070ff29933ac29607675c5ff38e8e2f44dca8aad7553e464)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__065e70484cc26504bb8700c3ba2ff55fcc1bba7d5506626e522979f6318db711)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f062a0527bc4f1611ecc8b6954cec3c24cb83c9c3287e4c5e86186ec089221e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__437761e992a7399f26dd399dcded54a44d172befc39f9c8ccb00d8a891354de5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__08858b18f5bd18d2a9e73d5ea158194e62f07289bdbaf7d888958626e3151f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18f5df084772e3d08681eb3dd14f21452a50e6ed047c5ea562eb998199d5247d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="matchGrpcAddress")
    def match_grpc_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchGrpcAddress"))

    @builtins.property
    @jsii.member(jsii_name="pscAutomatedEndpoints")
    def psc_automated_endpoints(
        self,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList":
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList", jsii.get(self, "pscAutomatedEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpoints]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a44ccd84811e39b81104e3fc3c32b5cf087882da8d7cf043065af2034ce1ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dc2d5a17f60258f54b4394e357f667cb943b72cdc7611036843b6b5fabc9a60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b2a2f91d035af7e036b63ed09083479687bc14ec455e0638a2c6172ceace9a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7527b77298bdc276d0fa4a5da4bb3f6dfce66a4139cb8f976eb7bb96da9c549a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37c3479de27bd7904e3b03665763f4d6d3e206defd963c88fcd69f0c6d11d1fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71bb6c5dd6a61253ff4ee6532856b95056ff24bc5eba9e69f144824c233e5b26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__365e39431e27e3fdb540b260e676b5986c503cf1137ddc1b8ce058674c865f07)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="matchAddress")
    def match_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchAddress"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints]:
        return typing.cast(typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efe76a9892b8951f817f770439577d80805ba2bb98c4c89ef241a1341650f6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleVertexAiIndexEndpointDeployedIndexTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#create GoogleVertexAiIndexEndpointDeployedIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#delete GoogleVertexAiIndexEndpointDeployedIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#update GoogleVertexAiIndexEndpointDeployedIndex#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f31b0892c5e3edfae8d4db9407be59ec84512e6ff6c31a9c7e7c76ccb7ca371)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#create GoogleVertexAiIndexEndpointDeployedIndex#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#delete GoogleVertexAiIndexEndpointDeployedIndex#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_index_endpoint_deployed_index#update GoogleVertexAiIndexEndpointDeployedIndex#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiIndexEndpointDeployedIndexTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiIndexEndpointDeployedIndexTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiIndexEndpointDeployedIndex.GoogleVertexAiIndexEndpointDeployedIndexTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5cb4f3d1f9907bb4d7ce78ba9bb1aada4d4b1bae1a1d06ee8f4e53e5ff0f3a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c76c8977e51ed9bf1bb606053f1fbc5f957c136e23d4f959956c55020c5938bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04fd7c54a1b653cf7e8d252e924787612f8b788da7a774b98c46b30bb095a1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f92e61148789b9ba39b6be3ec5f7aa90ced9473e190ab0d29bbfa6a8af8252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiIndexEndpointDeployedIndexTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiIndexEndpointDeployedIndexTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiIndexEndpointDeployedIndexTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b981c762f6b5dac380da3716557d971763b91c02b741d0f482a664fc02be4227)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVertexAiIndexEndpointDeployedIndex",
    "GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources",
    "GoogleVertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference",
    "GoogleVertexAiIndexEndpointDeployedIndexConfig",
    "GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources",
    "GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec",
    "GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference",
    "GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference",
    "GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig",
    "GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider",
    "GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference",
    "GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference",
    "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpoints",
    "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsList",
    "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference",
    "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints",
    "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList",
    "GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference",
    "GoogleVertexAiIndexEndpointDeployedIndexTimeouts",
    "GoogleVertexAiIndexEndpointDeployedIndexTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__50aec73e18913adb7f172a292414aaa449b2af358fd2c3833b81febc9b3a6fd2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    deployed_index_id: builtins.str,
    index: builtins.str,
    index_endpoint: builtins.str,
    automatic_resources: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_resources: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    deployed_index_auth_config: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_group: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_access_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    reserved_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bac9ca9fecad20f65cd4d67ada5cc29146cf4dcb1d340a126a6938b719ca84c4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb02087327674ec9ce5f70f23f7de70006356e65d8aa273e1ee0f348aceac57a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a90007962900e229672b0999021909d7a86ad2ee9de0c48bb19704eec754a56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4c2d4d84692cbca5431cd2afade7e5f360f40ff2bc33c7aadeb94ae395d4ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e4e5d43d7d55aa5a8399b6aa60efa5572842cdb57cf6e1887c264c8155bd80(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b30b4f7e399db3b50f2c147e06f97d4c016393c486ea9accc54827a8d7849d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c05d18ec7b1d500bda32f7c1c7b5320dd2725eafdac2ab5b4ff25a3b395228(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f170af35d8871b866c300de3b7d1e7999bae120648bf49672d10d2f452e9b4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76038e41d2400673cc8c6a7a041730a60564b0c3ff58b595916cbafc666c4b22(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f588c855858762bac523e08f618d0362b270bb062257afc481ba138c3656d3(
    *,
    max_replica_count: typing.Optional[jsii.Number] = None,
    min_replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0f22b81ee59b12b0c9a351c30d75d2bd8152edd71153b3c31063b68f4742d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17ca362919578aeb1b94761df4c9253cdef517a2fca959d7a694c526f2a0055(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19a401dd85039d2923396908b37bf60b1d7c3e3f53ce1a13ab3521e56174d97(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7175185c691a411edd1197ed1b7f8668e9dfc47069a7a17ebc2057e80add7bc5(
    value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267fd43d821520ce02006af5ff90cf2b7009f72c81d9508cfbf68910ed5a2dcf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deployed_index_id: builtins.str,
    index: builtins.str,
    index_endpoint: builtins.str,
    automatic_resources: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexAutomaticResources, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_resources: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    deployed_index_auth_config: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_group: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_access_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    reserved_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c354bf6657c7ee710b2753ca97b68f4e4c4302efe7af57b481863a453c187dd(
    *,
    machine_spec: typing.Union[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec, typing.Dict[builtins.str, typing.Any]],
    min_replica_count: jsii.Number,
    max_replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bc1557f342cdbc3368c5ae87bccadb462100641428e4036e2febcaaf0d746b(
    *,
    machine_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44120227bf0e87b30a38cb3d4ca293d6a5f86fa184c0a532eceba5f910eb0646(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fff575b83b953538f121e522381b4ffba85b18579868b10948d7f929f4dc44d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc94f3cf7dc2febcd82d5f63657bf3d47f078c9d4e43c3ae2ae7f1ae58b0989c(
    value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5142e8a629c2ecbbd29413b37e3a709b845bf0791efebbc78eb87e01d84ea77d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80557ace5f35db8b493207d76358132a557fff266da40c5d146f271044ba257c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1675fbf20932200dc8880d95f2e27ccc331a820f1c4d9cc8bfb04dcc77a4a71e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3ac59bf8fec3dca3460057e370edffaebbea5a16ea3d431673eeb440fb459a(
    value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDedicatedResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4431bf476369e68c0d14b27cf01d8533327372615cf35bb5a6a0ce7f5b435583(
    *,
    auth_provider: typing.Optional[typing.Union[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e499de1e932d3d3793bef936865aa5c6fba72aa4646fbd6de6bb398294ddcc(
    *,
    allowed_issuers: typing.Optional[typing.Sequence[builtins.str]] = None,
    audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab00ff3a8bf1a5e4d50f5a147046e4fc6cb5139e85bee97e12423f14c51c1cb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92b18df37307f05c8c6e49d0a59fa34d22dbec0ae8beca663057cd0cb2882c3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e35f9405934ef39030a4fe146a40e00b3af4cb8b5e7f9dc60b5949170e67b47(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3f227cf9dedb9f0f6f50e68ce1ff81036874c73036376a61ba3598d561b32e(
    value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1aae87b1d96e18365d20ce6d102b5250efd359c40d7fc27d9f8dade557600a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959fcc6805ba7aef1b2952077684eaf808585cf7046fa28e60a4c639130a0533(
    value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60205efe05b76ba7070ff29933ac29607675c5ff38e8e2f44dca8aad7553e464(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__065e70484cc26504bb8700c3ba2ff55fcc1bba7d5506626e522979f6318db711(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f062a0527bc4f1611ecc8b6954cec3c24cb83c9c3287e4c5e86186ec089221e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437761e992a7399f26dd399dcded54a44d172befc39f9c8ccb00d8a891354de5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08858b18f5bd18d2a9e73d5ea158194e62f07289bdbaf7d888958626e3151f7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f5df084772e3d08681eb3dd14f21452a50e6ed047c5ea562eb998199d5247d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a44ccd84811e39b81104e3fc3c32b5cf087882da8d7cf043065af2034ce1ed8(
    value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc2d5a17f60258f54b4394e357f667cb943b72cdc7611036843b6b5fabc9a60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b2a2f91d035af7e036b63ed09083479687bc14ec455e0638a2c6172ceace9a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7527b77298bdc276d0fa4a5da4bb3f6dfce66a4139cb8f976eb7bb96da9c549a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c3479de27bd7904e3b03665763f4d6d3e206defd963c88fcd69f0c6d11d1fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71bb6c5dd6a61253ff4ee6532856b95056ff24bc5eba9e69f144824c233e5b26(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365e39431e27e3fdb540b260e676b5986c503cf1137ddc1b8ce058674c865f07(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efe76a9892b8951f817f770439577d80805ba2bb98c4c89ef241a1341650f6f(
    value: typing.Optional[GoogleVertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f31b0892c5e3edfae8d4db9407be59ec84512e6ff6c31a9c7e7c76ccb7ca371(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cb4f3d1f9907bb4d7ce78ba9bb1aada4d4b1bae1a1d06ee8f4e53e5ff0f3a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76c8977e51ed9bf1bb606053f1fbc5f957c136e23d4f959956c55020c5938bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04fd7c54a1b653cf7e8d252e924787612f8b788da7a774b98c46b30bb095a1a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f92e61148789b9ba39b6be3ec5f7aa90ced9473e190ab0d29bbfa6a8af8252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b981c762f6b5dac380da3716557d971763b91c02b741d0f482a664fc02be4227(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiIndexEndpointDeployedIndexTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

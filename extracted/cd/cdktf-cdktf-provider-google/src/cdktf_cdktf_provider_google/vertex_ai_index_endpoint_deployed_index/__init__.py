r'''
# `google_vertex_ai_index_endpoint_deployed_index`

Refer to the Terraform Registry for docs: [`google_vertex_ai_index_endpoint_deployed_index`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index).
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


class VertexAiIndexEndpointDeployedIndex(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index google_vertex_ai_index_endpoint_deployed_index}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        deployed_index_id: builtins.str,
        index: builtins.str,
        index_endpoint: builtins.str,
        automatic_resources: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexAutomaticResources", typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_resources: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        deployed_index_auth_config: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_group: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_access_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index google_vertex_ai_index_endpoint_deployed_index} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param deployed_index_id: The user specified ID of the DeployedIndex. The ID can be up to 128 characters long and must start with a letter and only contain letters, numbers, and underscores. The ID must be unique within the project it is created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployed_index_id VertexAiIndexEndpointDeployedIndex#deployed_index_id}
        :param index: The name of the Index this is the deployment of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#index VertexAiIndexEndpointDeployedIndex#index}
        :param index_endpoint: Identifies the index endpoint. Must be in the format 'projects/{{project}}/locations/{{region}}/indexEndpoints/{{indexEndpoint}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#index_endpoint VertexAiIndexEndpointDeployedIndex#index_endpoint}
        :param automatic_resources: automatic_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#automatic_resources VertexAiIndexEndpointDeployedIndex#automatic_resources}
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#dedicated_resources VertexAiIndexEndpointDeployedIndex#dedicated_resources}
        :param deployed_index_auth_config: deployed_index_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployed_index_auth_config VertexAiIndexEndpointDeployedIndex#deployed_index_auth_config}
        :param deployment_group: The deployment group can be no longer than 64 characters (eg: 'test', 'prod'). If not set, we will use the 'default' deployment group. Creating deployment_groups with reserved_ip_ranges is a recommended practice when the peered network has multiple peering ranges. This creates your deployments from predictable IP spaces for easier traffic administration. Also, one deployment_group (except 'default') can only be used with the same reserved_ip_ranges which means if the deployment_group has been used with reserved_ip_ranges: [a, b, c], using it with [a, b] or [d, e] is disallowed. `See the official documentation here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.indexEndpoints#DeployedIndex.FIELDS.deployment_group>`_. Note: we only support up to 5 deployment groups (not including 'default'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployment_group VertexAiIndexEndpointDeployedIndex#deployment_group}
        :param display_name: The display name of the Index. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#display_name VertexAiIndexEndpointDeployedIndex#display_name}
        :param enable_access_logging: If true, private endpoint's access logs are sent to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#enable_access_logging VertexAiIndexEndpointDeployedIndex#enable_access_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#id VertexAiIndexEndpointDeployedIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: The region of the index endpoint deployment. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#region VertexAiIndexEndpointDeployedIndex#region}
        :param reserved_ip_ranges: A list of reserved ip ranges under the VPC network that can be used for this DeployedIndex. If set, we will deploy the index within the provided ip ranges. Otherwise, the index might be deployed to any ip ranges under the provided VPC network. The value should be the name of the address (https://cloud.google.com/compute/docs/reference/rest/v1/addresses) Example: ['vertex-ai-ip-range']. For more information about subnets and network IP ranges, please see https://cloud.google.com/vpc/docs/subnets#manually_created_subnet_ip_ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#reserved_ip_ranges VertexAiIndexEndpointDeployedIndex#reserved_ip_ranges}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#timeouts VertexAiIndexEndpointDeployedIndex#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f782c2ba2b3c42d95dcdb81e0269f122657b16d152e3744f40001de949b062)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiIndexEndpointDeployedIndexConfig(
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
            region=region,
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
        '''Generates CDKTF code for importing a VertexAiIndexEndpointDeployedIndex resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiIndexEndpointDeployedIndex to import.
        :param import_from_id: The id of the existing VertexAiIndexEndpointDeployedIndex that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiIndexEndpointDeployedIndex to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6f65a15d36516977224573f5293f7d4c3d8d48918d24e4d6853e2b25eeec35)
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
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If maxReplicaCount is not set, the default value is minReplicaCount. The max allowed replica count is 1000. The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, a no upper bound for scaling under heavy traffic will be assume, though Vertex AI may be unable to scale beyond certain replica number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#max_replica_count VertexAiIndexEndpointDeployedIndex#max_replica_count}
        :param min_replica_count: The minimum number of replicas this DeployedModel will be always deployed on. If minReplicaCount is not set, the default value is 2 (we don't provide SLA when minReplicaCount=1). If traffic against it increases, it may dynamically be deployed onto more replicas up to `maxReplicaCount <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/AutomaticResources#FIELDS.max_replica_count>`_, and as traffic decreases, some of these extra replicas may be freed. If the requested value is too large, the deployment will error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#min_replica_count VertexAiIndexEndpointDeployedIndex#min_replica_count}
        '''
        value = VertexAiIndexEndpointDeployedIndexAutomaticResources(
            max_replica_count=max_replica_count, min_replica_count=min_replica_count
        )

        return typing.cast(None, jsii.invoke(self, "putAutomaticResources", [value]))

    @jsii.member(jsii_name="putDedicatedResources")
    def put_dedicated_resources(
        self,
        *,
        machine_spec: typing.Union["VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        max_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#machine_spec VertexAiIndexEndpointDeployedIndex#machine_spec}
        :param min_replica_count: The minimum number of machine replicas this DeployedModel will be always deployed on. This value must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#min_replica_count VertexAiIndexEndpointDeployedIndex#min_replica_count}
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If maxReplicaCount is not set, the default value is minReplicaCount Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#max_replica_count VertexAiIndexEndpointDeployedIndex#max_replica_count}
        '''
        value = VertexAiIndexEndpointDeployedIndexDedicatedResources(
            machine_spec=machine_spec,
            min_replica_count=min_replica_count,
            max_replica_count=max_replica_count,
        )

        return typing.cast(None, jsii.invoke(self, "putDedicatedResources", [value]))

    @jsii.member(jsii_name="putDeployedIndexAuthConfig")
    def put_deployed_index_auth_config(
        self,
        *,
        auth_provider: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_provider: auth_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#auth_provider VertexAiIndexEndpointDeployedIndex#auth_provider}
        '''
        value = VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#create VertexAiIndexEndpointDeployedIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#delete VertexAiIndexEndpointDeployedIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#update VertexAiIndexEndpointDeployedIndex#update}.
        '''
        value = VertexAiIndexEndpointDeployedIndexTimeouts(
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

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    ) -> "VertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference":
        return typing.cast("VertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference", jsii.get(self, "automaticResources"))

    @builtins.property
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResources")
    def dedicated_resources(
        self,
    ) -> "VertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference":
        return typing.cast("VertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference", jsii.get(self, "dedicatedResources"))

    @builtins.property
    @jsii.member(jsii_name="deployedIndexAuthConfig")
    def deployed_index_auth_config(
        self,
    ) -> "VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference":
        return typing.cast("VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference", jsii.get(self, "deployedIndexAuthConfig"))

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
    ) -> "VertexAiIndexEndpointDeployedIndexPrivateEndpointsList":
        return typing.cast("VertexAiIndexEndpointDeployedIndexPrivateEndpointsList", jsii.get(self, "privateEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VertexAiIndexEndpointDeployedIndexTimeoutsOutputReference":
        return typing.cast("VertexAiIndexEndpointDeployedIndexTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="automaticResourcesInput")
    def automatic_resources_input(
        self,
    ) -> typing.Optional["VertexAiIndexEndpointDeployedIndexAutomaticResources"]:
        return typing.cast(typing.Optional["VertexAiIndexEndpointDeployedIndexAutomaticResources"], jsii.get(self, "automaticResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourcesInput")
    def dedicated_resources_input(
        self,
    ) -> typing.Optional["VertexAiIndexEndpointDeployedIndexDedicatedResources"]:
        return typing.cast(typing.Optional["VertexAiIndexEndpointDeployedIndexDedicatedResources"], jsii.get(self, "dedicatedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="deployedIndexAuthConfigInput")
    def deployed_index_auth_config_input(
        self,
    ) -> typing.Optional["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig"]:
        return typing.cast(typing.Optional["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig"], jsii.get(self, "deployedIndexAuthConfigInput"))

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
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="reservedIpRangesInput")
    def reserved_ip_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "reservedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiIndexEndpointDeployedIndexTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiIndexEndpointDeployedIndexTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="deployedIndexId")
    def deployed_index_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deployedIndexId"))

    @deployed_index_id.setter
    def deployed_index_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d35f44917953edc697ef4e2a3918d117ec8dc73b7419194ff4569c408807f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deployedIndexId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deploymentGroup")
    def deployment_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroup"))

    @deployment_group.setter
    def deployment_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b525f391b48c24d88e96bab65cd879c89e52201f179ebd9a6fa99debaaef934e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed5424a12640bf7d04294f3a3df3015194e8c6b740cca2006f123a888096175a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f2d05c2b43d0f80780c0c6057160fbf4dda7621fa40880985ad6fbaaa5eb7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAccessLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feca74cc9d0545cda392005efba27f68dd2327efe9464704ce9ca09144041716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43223bb5a6ae024378ead4c6622c950b3333179d8854064bdcda660255bcf986)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="indexEndpoint")
    def index_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexEndpoint"))

    @index_endpoint.setter
    def index_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab7aa47b1962a8109e1afa5107a8c8e8bd0b7e446184b822ff97d213d73b6c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27185ed581ba8ac7ea6f1cc6dbab5d1906d8e2f3533a57b9c95fbd426e870eb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="reservedIpRanges")
    def reserved_ip_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "reservedIpRanges"))

    @reserved_ip_ranges.setter
    def reserved_ip_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4cd00f798689dbd6bdc768a75a149620054ec69224262132c5cc49b22c93a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reservedIpRanges", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexAutomaticResources",
    jsii_struct_bases=[],
    name_mapping={
        "max_replica_count": "maxReplicaCount",
        "min_replica_count": "minReplicaCount",
    },
)
class VertexAiIndexEndpointDeployedIndexAutomaticResources:
    def __init__(
        self,
        *,
        max_replica_count: typing.Optional[jsii.Number] = None,
        min_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If maxReplicaCount is not set, the default value is minReplicaCount. The max allowed replica count is 1000. The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, a no upper bound for scaling under heavy traffic will be assume, though Vertex AI may be unable to scale beyond certain replica number. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#max_replica_count VertexAiIndexEndpointDeployedIndex#max_replica_count}
        :param min_replica_count: The minimum number of replicas this DeployedModel will be always deployed on. If minReplicaCount is not set, the default value is 2 (we don't provide SLA when minReplicaCount=1). If traffic against it increases, it may dynamically be deployed onto more replicas up to `maxReplicaCount <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/AutomaticResources#FIELDS.max_replica_count>`_, and as traffic decreases, some of these extra replicas may be freed. If the requested value is too large, the deployment will error. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#min_replica_count VertexAiIndexEndpointDeployedIndex#min_replica_count}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f9f4458a4bb952f085556e2fd0f967cff3d460b58341e9fa223ee3f85f9d31)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#max_replica_count VertexAiIndexEndpointDeployedIndex#max_replica_count}
        '''
        result = self._values.get("max_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_replica_count(self) -> typing.Optional[jsii.Number]:
        '''The minimum number of replicas this DeployedModel will be always deployed on.

        If minReplicaCount is not set, the default value is 2 (we don't provide SLA when minReplicaCount=1).

        If traffic against it increases, it may dynamically be deployed onto more replicas up to `maxReplicaCount <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/AutomaticResources#FIELDS.max_replica_count>`_, and as traffic decreases, some of these extra replicas may be freed. If the requested value is too large, the deployment will error.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#min_replica_count VertexAiIndexEndpointDeployedIndex#min_replica_count}
        '''
        result = self._values.get("min_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexAutomaticResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98c8fcac0d4977f2b4e1b8520f0f582ba94cdf42c115ebf2ec6cfde9ad87a68f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a526dc17f58760b4f76325ae9850a0a16ad6eed843ef756f5c6ab0ec15bb4cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @min_replica_count.setter
    def min_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d4acf3c421ea6f48c9d94ef2b7580d741596341b2c273fe1d114f54566f93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexAutomaticResources]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexAutomaticResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexEndpointDeployedIndexAutomaticResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876e015868bd13e1b1ae15fcbdd571c28869b183f0480c48e73e97f52399962f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexConfig",
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
        "region": "region",
        "reserved_ip_ranges": "reservedIpRanges",
        "timeouts": "timeouts",
    },
)
class VertexAiIndexEndpointDeployedIndexConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        automatic_resources: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexAutomaticResources, typing.Dict[builtins.str, typing.Any]]] = None,
        dedicated_resources: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        deployed_index_auth_config: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_group: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        enable_access_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        reserved_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param deployed_index_id: The user specified ID of the DeployedIndex. The ID can be up to 128 characters long and must start with a letter and only contain letters, numbers, and underscores. The ID must be unique within the project it is created in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployed_index_id VertexAiIndexEndpointDeployedIndex#deployed_index_id}
        :param index: The name of the Index this is the deployment of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#index VertexAiIndexEndpointDeployedIndex#index}
        :param index_endpoint: Identifies the index endpoint. Must be in the format 'projects/{{project}}/locations/{{region}}/indexEndpoints/{{indexEndpoint}}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#index_endpoint VertexAiIndexEndpointDeployedIndex#index_endpoint}
        :param automatic_resources: automatic_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#automatic_resources VertexAiIndexEndpointDeployedIndex#automatic_resources}
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#dedicated_resources VertexAiIndexEndpointDeployedIndex#dedicated_resources}
        :param deployed_index_auth_config: deployed_index_auth_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployed_index_auth_config VertexAiIndexEndpointDeployedIndex#deployed_index_auth_config}
        :param deployment_group: The deployment group can be no longer than 64 characters (eg: 'test', 'prod'). If not set, we will use the 'default' deployment group. Creating deployment_groups with reserved_ip_ranges is a recommended practice when the peered network has multiple peering ranges. This creates your deployments from predictable IP spaces for easier traffic administration. Also, one deployment_group (except 'default') can only be used with the same reserved_ip_ranges which means if the deployment_group has been used with reserved_ip_ranges: [a, b, c], using it with [a, b] or [d, e] is disallowed. `See the official documentation here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.indexEndpoints#DeployedIndex.FIELDS.deployment_group>`_. Note: we only support up to 5 deployment groups (not including 'default'). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployment_group VertexAiIndexEndpointDeployedIndex#deployment_group}
        :param display_name: The display name of the Index. The name can be up to 128 characters long and can consist of any UTF-8 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#display_name VertexAiIndexEndpointDeployedIndex#display_name}
        :param enable_access_logging: If true, private endpoint's access logs are sent to Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#enable_access_logging VertexAiIndexEndpointDeployedIndex#enable_access_logging}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#id VertexAiIndexEndpointDeployedIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param region: The region of the index endpoint deployment. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#region VertexAiIndexEndpointDeployedIndex#region}
        :param reserved_ip_ranges: A list of reserved ip ranges under the VPC network that can be used for this DeployedIndex. If set, we will deploy the index within the provided ip ranges. Otherwise, the index might be deployed to any ip ranges under the provided VPC network. The value should be the name of the address (https://cloud.google.com/compute/docs/reference/rest/v1/addresses) Example: ['vertex-ai-ip-range']. For more information about subnets and network IP ranges, please see https://cloud.google.com/vpc/docs/subnets#manually_created_subnet_ip_ranges. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#reserved_ip_ranges VertexAiIndexEndpointDeployedIndex#reserved_ip_ranges}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#timeouts VertexAiIndexEndpointDeployedIndex#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(automatic_resources, dict):
            automatic_resources = VertexAiIndexEndpointDeployedIndexAutomaticResources(**automatic_resources)
        if isinstance(dedicated_resources, dict):
            dedicated_resources = VertexAiIndexEndpointDeployedIndexDedicatedResources(**dedicated_resources)
        if isinstance(deployed_index_auth_config, dict):
            deployed_index_auth_config = VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig(**deployed_index_auth_config)
        if isinstance(timeouts, dict):
            timeouts = VertexAiIndexEndpointDeployedIndexTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe697d0e16fe1e7886596f2df824e54d52056651ade26f279715c24eac60e99)
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
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
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
        if region is not None:
            self._values["region"] = region
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployed_index_id VertexAiIndexEndpointDeployedIndex#deployed_index_id}
        '''
        result = self._values.get("deployed_index_id")
        assert result is not None, "Required property 'deployed_index_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''The name of the Index this is the deployment of.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#index VertexAiIndexEndpointDeployedIndex#index}
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index_endpoint(self) -> builtins.str:
        '''Identifies the index endpoint. Must be in the format 'projects/{{project}}/locations/{{region}}/indexEndpoints/{{indexEndpoint}}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#index_endpoint VertexAiIndexEndpointDeployedIndex#index_endpoint}
        '''
        result = self._values.get("index_endpoint")
        assert result is not None, "Required property 'index_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def automatic_resources(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexAutomaticResources]:
        '''automatic_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#automatic_resources VertexAiIndexEndpointDeployedIndex#automatic_resources}
        '''
        result = self._values.get("automatic_resources")
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexAutomaticResources], result)

    @builtins.property
    def dedicated_resources(
        self,
    ) -> typing.Optional["VertexAiIndexEndpointDeployedIndexDedicatedResources"]:
        '''dedicated_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#dedicated_resources VertexAiIndexEndpointDeployedIndex#dedicated_resources}
        '''
        result = self._values.get("dedicated_resources")
        return typing.cast(typing.Optional["VertexAiIndexEndpointDeployedIndexDedicatedResources"], result)

    @builtins.property
    def deployed_index_auth_config(
        self,
    ) -> typing.Optional["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig"]:
        '''deployed_index_auth_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployed_index_auth_config VertexAiIndexEndpointDeployedIndex#deployed_index_auth_config}
        '''
        result = self._values.get("deployed_index_auth_config")
        return typing.cast(typing.Optional["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig"], result)

    @builtins.property
    def deployment_group(self) -> typing.Optional[builtins.str]:
        '''The deployment group can be no longer than 64 characters (eg: 'test', 'prod').

        If not set, we will use the 'default' deployment group.
        Creating deployment_groups with reserved_ip_ranges is a recommended practice when the peered network has multiple peering ranges. This creates your deployments from predictable IP spaces for easier traffic administration. Also, one deployment_group (except 'default') can only be used with the same reserved_ip_ranges which means if the deployment_group has been used with reserved_ip_ranges: [a, b, c], using it with [a, b] or [d, e] is disallowed. `See the official documentation here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.indexEndpoints#DeployedIndex.FIELDS.deployment_group>`_.
        Note: we only support up to 5 deployment groups (not including 'default').

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#deployment_group VertexAiIndexEndpointDeployedIndex#deployment_group}
        '''
        result = self._values.get("deployment_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the Index.

        The name can be up to 128 characters long and can consist of any UTF-8 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#display_name VertexAiIndexEndpointDeployedIndex#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_access_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, private endpoint's access logs are sent to Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#enable_access_logging VertexAiIndexEndpointDeployedIndex#enable_access_logging}
        '''
        result = self._values.get("enable_access_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#id VertexAiIndexEndpointDeployedIndex#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of the index endpoint deployment. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#region VertexAiIndexEndpointDeployedIndex#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reserved_ip_ranges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of reserved ip ranges under the VPC network that can be used for this DeployedIndex.

        If set, we will deploy the index within the provided ip ranges. Otherwise, the index might be deployed to any ip ranges under the provided VPC network.

        The value should be the name of the address (https://cloud.google.com/compute/docs/reference/rest/v1/addresses) Example: ['vertex-ai-ip-range'].

        For more information about subnets and network IP ranges, please see https://cloud.google.com/vpc/docs/subnets#manually_created_subnet_ip_ranges.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#reserved_ip_ranges VertexAiIndexEndpointDeployedIndex#reserved_ip_ranges}
        '''
        result = self._values.get("reserved_ip_ranges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VertexAiIndexEndpointDeployedIndexTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#timeouts VertexAiIndexEndpointDeployedIndex#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiIndexEndpointDeployedIndexTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexDedicatedResources",
    jsii_struct_bases=[],
    name_mapping={
        "machine_spec": "machineSpec",
        "min_replica_count": "minReplicaCount",
        "max_replica_count": "maxReplicaCount",
    },
)
class VertexAiIndexEndpointDeployedIndexDedicatedResources:
    def __init__(
        self,
        *,
        machine_spec: typing.Union["VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        max_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#machine_spec VertexAiIndexEndpointDeployedIndex#machine_spec}
        :param min_replica_count: The minimum number of machine replicas this DeployedModel will be always deployed on. This value must be greater than or equal to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#min_replica_count VertexAiIndexEndpointDeployedIndex#min_replica_count}
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If maxReplicaCount is not set, the default value is minReplicaCount Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#max_replica_count VertexAiIndexEndpointDeployedIndex#max_replica_count}
        '''
        if isinstance(machine_spec, dict):
            machine_spec = VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec(**machine_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfd460807c9e15a35201243c98154b545552a420c140a983a1ad1c9d442caf0)
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
    ) -> "VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec":
        '''machine_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#machine_spec VertexAiIndexEndpointDeployedIndex#machine_spec}
        '''
        result = self._values.get("machine_spec")
        assert result is not None, "Required property 'machine_spec' is missing"
        return typing.cast("VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec", result)

    @builtins.property
    def min_replica_count(self) -> jsii.Number:
        '''The minimum number of machine replicas this DeployedModel will be always deployed on.

        This value must be greater than or equal to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#min_replica_count VertexAiIndexEndpointDeployedIndex#min_replica_count}
        '''
        result = self._values.get("min_replica_count")
        assert result is not None, "Required property 'min_replica_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def max_replica_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases.

        If maxReplicaCount is not set, the default value is minReplicaCount

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#max_replica_count VertexAiIndexEndpointDeployedIndex#max_replica_count}
        '''
        result = self._values.get("max_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexDedicatedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec",
    jsii_struct_bases=[],
    name_mapping={"machine_type": "machineType"},
)
class VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec:
    def __init__(self, *, machine_type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_ See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_. For `DeployedModel <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints#DeployedModel>`_ this field is optional, and the default value is n1-standard-2. For `BatchPredictionJob <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.batchPredictionJobs#BatchPredictionJob>`_ or as part of `WorkerPoolSpec <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#WorkerPoolSpec>`_ this field is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#machine_type VertexAiIndexEndpointDeployedIndex#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56d014af2ce380357221755d242038561b9f7e269e318a0ba0c082aafeaeba1e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#machine_type VertexAiIndexEndpointDeployedIndex#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0da14450768f4d48d4c4da9d690ab1cda657accfcdc1b5b1331d65e6c14cc438)
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
            type_hints = typing.get_type_hints(_typecheckingstub__480a79aedaabf3376915a89d2f562019924c7a04a23815ce9c4c24442480e497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aed63752a64ee278391fc89776399e99c21626ccf78936f79f30236fbc3a699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5473253a0085d26a2cd3978558f0f42e69195e8ae8160f134e8fd3b8349f3827)
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
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_ See the `list of machine types supported for custom training <https://cloud.google.com/vertex-ai/docs/training/configure-compute#machine-types>`_. For `DeployedModel <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints#DeployedModel>`_ this field is optional, and the default value is n1-standard-2. For `BatchPredictionJob <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/projects.locations.batchPredictionJobs#BatchPredictionJob>`_ or as part of `WorkerPoolSpec <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#WorkerPoolSpec>`_ this field is required. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#machine_type VertexAiIndexEndpointDeployedIndex#machine_type}
        '''
        value = VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec(
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
    ) -> VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference:
        return typing.cast(VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference, jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="machineSpecInput")
    def machine_spec_input(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec], jsii.get(self, "machineSpecInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b522b86bb3313ef9c1b6e2ba4297ff74ee29f64305af9656f5dcecbca8198cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @min_replica_count.setter
    def min_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aa547e7a17be3ec33decaa9a969b174a76e0663a3438f565fa1c250c3fb70f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResources]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f17693c91fa7969724a58bf803136ec7f53a0bf8a8f66c047da315588295b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig",
    jsii_struct_bases=[],
    name_mapping={"auth_provider": "authProvider"},
)
class VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig:
    def __init__(
        self,
        *,
        auth_provider: typing.Optional[typing.Union["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param auth_provider: auth_provider block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#auth_provider VertexAiIndexEndpointDeployedIndex#auth_provider}
        '''
        if isinstance(auth_provider, dict):
            auth_provider = VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider(**auth_provider)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e65ca2bafa77f596c557b704134dc1607364f11805200e6beba5ab34edefcf2)
            check_type(argname="argument auth_provider", value=auth_provider, expected_type=type_hints["auth_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_provider is not None:
            self._values["auth_provider"] = auth_provider

    @builtins.property
    def auth_provider(
        self,
    ) -> typing.Optional["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider"]:
        '''auth_provider block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#auth_provider VertexAiIndexEndpointDeployedIndex#auth_provider}
        '''
        result = self._values.get("auth_provider")
        return typing.cast(typing.Optional["VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider",
    jsii_struct_bases=[],
    name_mapping={"allowed_issuers": "allowedIssuers", "audiences": "audiences"},
)
class VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider:
    def __init__(
        self,
        *,
        allowed_issuers: typing.Optional[typing.Sequence[builtins.str]] = None,
        audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param allowed_issuers: A list of allowed JWT issuers. Each entry must be a valid Google service account, in the following format: service-account-name@project-id.iam.gserviceaccount.com Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#allowed_issuers VertexAiIndexEndpointDeployedIndex#allowed_issuers}
        :param audiences: The list of JWT audiences. that are allowed to access. A JWT containing any of these audiences will be accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#audiences VertexAiIndexEndpointDeployedIndex#audiences}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1084e6d6f060a0e91183eb4a486314a4e9a982f35916374f6cb11c1e353c727e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#allowed_issuers VertexAiIndexEndpointDeployedIndex#allowed_issuers}
        '''
        result = self._values.get("allowed_issuers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of JWT audiences.

        that are allowed to access. A JWT containing any of these audiences will be accepted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#audiences VertexAiIndexEndpointDeployedIndex#audiences}
        '''
        result = self._values.get("audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1067919b52fca4b14d8e1dca16e79322294c0c8a9e88cd3ac953c85d0f4bef1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b4d46c03e9aeb61df5b18469f25233e8cf259efcc3ce0359257c7de6f248465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIssuers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="audiences")
    def audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "audiences"))

    @audiences.setter
    def audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4121cde77c59a3e648d509f8b92abf51b1f4d0cc8bf543793846a9c7059fdee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fcea73c84b0933900a9930aa3c00a1d537e1874e974ac91c67ab358cf6f209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6e56fbf053a0967d5b44edca4f9330c44c605f15141e897b071e3fa7480b403)
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
        :param allowed_issuers: A list of allowed JWT issuers. Each entry must be a valid Google service account, in the following format: service-account-name@project-id.iam.gserviceaccount.com Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#allowed_issuers VertexAiIndexEndpointDeployedIndex#allowed_issuers}
        :param audiences: The list of JWT audiences. that are allowed to access. A JWT containing any of these audiences will be accepted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#audiences VertexAiIndexEndpointDeployedIndex#audiences}
        '''
        value = VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider(
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
    ) -> VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference:
        return typing.cast(VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference, jsii.get(self, "authProvider"))

    @builtins.property
    @jsii.member(jsii_name="authProviderInput")
    def auth_provider_input(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider], jsii.get(self, "authProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cca55f2c156c13665aef14d43af977257c56346abf51a80957a5629929e4b15f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexPrivateEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiIndexEndpointDeployedIndexPrivateEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexPrivateEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexEndpointDeployedIndexPrivateEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexPrivateEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75aec72b4d0b931011e775384be8072a57545181162a4cf8beb58f61f358cfb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4cd4065d191cbfd87acc26541f72a03d386a3d8f51e7e95aac96358f8749170)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa3e156a7cf2046f7be907c56c748cfe7066abfae893c32575b6ce6a99eb142)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7190eb9a59b2408024ecf9ce8c9158fc6d1c974055b3de3dd299a2160af0f2de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3aa62e3fa0dae69b761f0677b1297836ef48fe85006bf83a1379090528016f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__205b9529d05dca43bc7c2f7778cc993aae0f226f48f797d875d716e1076d0b66)
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
    ) -> "VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList":
        return typing.cast("VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList", jsii.get(self, "pscAutomatedEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="serviceAttachment")
    def service_attachment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceAttachment"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexPrivateEndpoints]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexPrivateEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexEndpointDeployedIndexPrivateEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9a3ae909948f56def4428658c00cd0d4b6f3d42ce3a380069fc770b1c13430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b242d0abf999a3bc758c5b4ea970bcefb0c609c6630b55062c9c83c5ca3c9c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9422f7a8bf634e9db51f50e7e632f2388c191ca45bd4e7e824fc646d6848f408)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6982eff4dec87dc725b0571180007c53211321190626359ba2065eebdde5390b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbdd74e883e49b45a85b723788afbd58871ed283914f102cafad04e79ec41e3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__524cf7dd25197d77a6c2a59f936a6b18e624e0ad7deb06936bb9fbc895f43863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__632f2f6ee3955334eaf7db5977fa33c459a6f468d8fc0bcaa38310b6bfae4687)
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
    ) -> typing.Optional[VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints]:
        return typing.cast(typing.Optional[VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c196db45f3cfb3a006a6c5884622ac6775d14b9d91b34ef55370c2386989afdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class VertexAiIndexEndpointDeployedIndexTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#create VertexAiIndexEndpointDeployedIndex#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#delete VertexAiIndexEndpointDeployedIndex#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#update VertexAiIndexEndpointDeployedIndex#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa93b0d75cd1271e0f46ae7e9720648ae9226b505f8379b7aa756dda30d92e7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#create VertexAiIndexEndpointDeployedIndex#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#delete VertexAiIndexEndpointDeployedIndex#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_index_endpoint_deployed_index#update VertexAiIndexEndpointDeployedIndex#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiIndexEndpointDeployedIndexTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiIndexEndpointDeployedIndexTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiIndexEndpointDeployedIndex.VertexAiIndexEndpointDeployedIndexTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__121634cb0f0dc3a65f15d1cd696e59822bdb13d756623b9c05770fc2b78fa3f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53f1ec4a8a2943489db686523db3d366b09433e6bf722ddb7e175a14a0c2b431)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2edbea0d718495dbd91b1936635270a7005bf4666f7a1205446c55be04310f8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179ce93ec8a0e0fa3ed406f77ff3b84ec5aaf87027fb02e0554bcafc95e5a6ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiIndexEndpointDeployedIndexTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiIndexEndpointDeployedIndexTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiIndexEndpointDeployedIndexTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b472854e63a1a1ece29a0daaf6bf0b34e93ca3854024124cc052d5eff040be50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VertexAiIndexEndpointDeployedIndex",
    "VertexAiIndexEndpointDeployedIndexAutomaticResources",
    "VertexAiIndexEndpointDeployedIndexAutomaticResourcesOutputReference",
    "VertexAiIndexEndpointDeployedIndexConfig",
    "VertexAiIndexEndpointDeployedIndexDedicatedResources",
    "VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec",
    "VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpecOutputReference",
    "VertexAiIndexEndpointDeployedIndexDedicatedResourcesOutputReference",
    "VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig",
    "VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider",
    "VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProviderOutputReference",
    "VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigOutputReference",
    "VertexAiIndexEndpointDeployedIndexPrivateEndpoints",
    "VertexAiIndexEndpointDeployedIndexPrivateEndpointsList",
    "VertexAiIndexEndpointDeployedIndexPrivateEndpointsOutputReference",
    "VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints",
    "VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsList",
    "VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpointsOutputReference",
    "VertexAiIndexEndpointDeployedIndexTimeouts",
    "VertexAiIndexEndpointDeployedIndexTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b9f782c2ba2b3c42d95dcdb81e0269f122657b16d152e3744f40001de949b062(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    deployed_index_id: builtins.str,
    index: builtins.str,
    index_endpoint: builtins.str,
    automatic_resources: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexAutomaticResources, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_resources: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    deployed_index_auth_config: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_group: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_access_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6e6f65a15d36516977224573f5293f7d4c3d8d48918d24e4d6853e2b25eeec35(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d35f44917953edc697ef4e2a3918d117ec8dc73b7419194ff4569c408807f7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b525f391b48c24d88e96bab65cd879c89e52201f179ebd9a6fa99debaaef934e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed5424a12640bf7d04294f3a3df3015194e8c6b740cca2006f123a888096175a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f2d05c2b43d0f80780c0c6057160fbf4dda7621fa40880985ad6fbaaa5eb7f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feca74cc9d0545cda392005efba27f68dd2327efe9464704ce9ca09144041716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43223bb5a6ae024378ead4c6622c950b3333179d8854064bdcda660255bcf986(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab7aa47b1962a8109e1afa5107a8c8e8bd0b7e446184b822ff97d213d73b6c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27185ed581ba8ac7ea6f1cc6dbab5d1906d8e2f3533a57b9c95fbd426e870eb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4cd00f798689dbd6bdc768a75a149620054ec69224262132c5cc49b22c93a17(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f9f4458a4bb952f085556e2fd0f967cff3d460b58341e9fa223ee3f85f9d31(
    *,
    max_replica_count: typing.Optional[jsii.Number] = None,
    min_replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c8fcac0d4977f2b4e1b8520f0f582ba94cdf42c115ebf2ec6cfde9ad87a68f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a526dc17f58760b4f76325ae9850a0a16ad6eed843ef756f5c6ab0ec15bb4cbb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d4acf3c421ea6f48c9d94ef2b7580d741596341b2c273fe1d114f54566f93f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876e015868bd13e1b1ae15fcbdd571c28869b183f0480c48e73e97f52399962f(
    value: typing.Optional[VertexAiIndexEndpointDeployedIndexAutomaticResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe697d0e16fe1e7886596f2df824e54d52056651ade26f279715c24eac60e99(
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
    automatic_resources: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexAutomaticResources, typing.Dict[builtins.str, typing.Any]]] = None,
    dedicated_resources: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    deployed_index_auth_config: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_group: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    enable_access_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    reserved_ip_ranges: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfd460807c9e15a35201243c98154b545552a420c140a983a1ad1c9d442caf0(
    *,
    machine_spec: typing.Union[VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec, typing.Dict[builtins.str, typing.Any]],
    min_replica_count: jsii.Number,
    max_replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d014af2ce380357221755d242038561b9f7e269e318a0ba0c082aafeaeba1e(
    *,
    machine_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0da14450768f4d48d4c4da9d690ab1cda657accfcdc1b5b1331d65e6c14cc438(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480a79aedaabf3376915a89d2f562019924c7a04a23815ce9c4c24442480e497(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aed63752a64ee278391fc89776399e99c21626ccf78936f79f30236fbc3a699(
    value: typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResourcesMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5473253a0085d26a2cd3978558f0f42e69195e8ae8160f134e8fd3b8349f3827(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b522b86bb3313ef9c1b6e2ba4297ff74ee29f64305af9656f5dcecbca8198cbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa547e7a17be3ec33decaa9a969b174a76e0663a3438f565fa1c250c3fb70f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f17693c91fa7969724a58bf803136ec7f53a0bf8a8f66c047da315588295b8(
    value: typing.Optional[VertexAiIndexEndpointDeployedIndexDedicatedResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e65ca2bafa77f596c557b704134dc1607364f11805200e6beba5ab34edefcf2(
    *,
    auth_provider: typing.Optional[typing.Union[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1084e6d6f060a0e91183eb4a486314a4e9a982f35916374f6cb11c1e353c727e(
    *,
    allowed_issuers: typing.Optional[typing.Sequence[builtins.str]] = None,
    audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1067919b52fca4b14d8e1dca16e79322294c0c8a9e88cd3ac953c85d0f4bef1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4d46c03e9aeb61df5b18469f25233e8cf259efcc3ce0359257c7de6f248465(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4121cde77c59a3e648d509f8b92abf51b1f4d0cc8bf543793846a9c7059fdee4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fcea73c84b0933900a9930aa3c00a1d537e1874e974ac91c67ab358cf6f209(
    value: typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfigAuthProvider],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e56fbf053a0967d5b44edca4f9330c44c605f15141e897b071e3fa7480b403(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cca55f2c156c13665aef14d43af977257c56346abf51a80957a5629929e4b15f(
    value: typing.Optional[VertexAiIndexEndpointDeployedIndexDeployedIndexAuthConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75aec72b4d0b931011e775384be8072a57545181162a4cf8beb58f61f358cfb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cd4065d191cbfd87acc26541f72a03d386a3d8f51e7e95aac96358f8749170(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa3e156a7cf2046f7be907c56c748cfe7066abfae893c32575b6ce6a99eb142(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7190eb9a59b2408024ecf9ce8c9158fc6d1c974055b3de3dd299a2160af0f2de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3aa62e3fa0dae69b761f0677b1297836ef48fe85006bf83a1379090528016f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205b9529d05dca43bc7c2f7778cc993aae0f226f48f797d875d716e1076d0b66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9a3ae909948f56def4428658c00cd0d4b6f3d42ce3a380069fc770b1c13430(
    value: typing.Optional[VertexAiIndexEndpointDeployedIndexPrivateEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b242d0abf999a3bc758c5b4ea970bcefb0c609c6630b55062c9c83c5ca3c9c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9422f7a8bf634e9db51f50e7e632f2388c191ca45bd4e7e824fc646d6848f408(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6982eff4dec87dc725b0571180007c53211321190626359ba2065eebdde5390b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdd74e883e49b45a85b723788afbd58871ed283914f102cafad04e79ec41e3a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__524cf7dd25197d77a6c2a59f936a6b18e624e0ad7deb06936bb9fbc895f43863(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632f2f6ee3955334eaf7db5977fa33c459a6f468d8fc0bcaa38310b6bfae4687(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c196db45f3cfb3a006a6c5884622ac6775d14b9d91b34ef55370c2386989afdb(
    value: typing.Optional[VertexAiIndexEndpointDeployedIndexPrivateEndpointsPscAutomatedEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa93b0d75cd1271e0f46ae7e9720648ae9226b505f8379b7aa756dda30d92e7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121634cb0f0dc3a65f15d1cd696e59822bdb13d756623b9c05770fc2b78fa3f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f1ec4a8a2943489db686523db3d366b09433e6bf722ddb7e175a14a0c2b431(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2edbea0d718495dbd91b1936635270a7005bf4666f7a1205446c55be04310f8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179ce93ec8a0e0fa3ed406f77ff3b84ec5aaf87027fb02e0554bcafc95e5a6ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b472854e63a1a1ece29a0daaf6bf0b34e93ca3854024124cc052d5eff040be50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiIndexEndpointDeployedIndexTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

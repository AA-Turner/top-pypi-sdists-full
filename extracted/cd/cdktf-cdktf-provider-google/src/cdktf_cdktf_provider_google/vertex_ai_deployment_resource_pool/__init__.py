r'''
# `google_vertex_ai_deployment_resource_pool`

Refer to the Terraform Registry for docs: [`google_vertex_ai_deployment_resource_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool).
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


class VertexAiDeploymentResourcePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool google_vertex_ai_deployment_resource_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        dedicated_resources: typing.Optional[typing.Union["VertexAiDeploymentResourcePoolDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiDeploymentResourcePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool google_vertex_ai_deployment_resource_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of deployment resource pool. The maximum length is 63 characters, and valid characters are '/^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#name VertexAiDeploymentResourcePool#name}
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#dedicated_resources VertexAiDeploymentResourcePool#dedicated_resources}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#id VertexAiDeploymentResourcePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#project VertexAiDeploymentResourcePool#project}.
        :param region: The region of deployment resource pool. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#region VertexAiDeploymentResourcePool#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#timeouts VertexAiDeploymentResourcePool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__892c6181b08154961813a5d94e1e4ecdb96c29a2a5c497b1e6cbfe15ef236982)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VertexAiDeploymentResourcePoolConfig(
            name=name,
            dedicated_resources=dedicated_resources,
            id=id,
            project=project,
            region=region,
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
        '''Generates CDKTF code for importing a VertexAiDeploymentResourcePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VertexAiDeploymentResourcePool to import.
        :param import_from_id: The id of the existing VertexAiDeploymentResourcePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VertexAiDeploymentResourcePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18b19b97fb34041b9ca76bc2b7f24a63a6f454eac08b3cc960d5db4402b17fdf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDedicatedResources")
    def put_dedicated_resources(
        self,
        *,
        machine_spec: typing.Union["VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#machine_spec VertexAiDeploymentResourcePool#machine_spec}
        :param min_replica_count: The minimum number of machine replicas this DeployedModel will be always deployed on. This value must be greater than or equal to 1. If traffic against the DeployedModel increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#min_replica_count VertexAiDeploymentResourcePool#min_replica_count}
        :param autoscaling_metric_specs: autoscaling_metric_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#autoscaling_metric_specs VertexAiDeploymentResourcePool#autoscaling_metric_specs}
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#max_replica_count VertexAiDeploymentResourcePool#max_replica_count}
        '''
        value = VertexAiDeploymentResourcePoolDedicatedResources(
            machine_spec=machine_spec,
            min_replica_count=min_replica_count,
            autoscaling_metric_specs=autoscaling_metric_specs,
            max_replica_count=max_replica_count,
        )

        return typing.cast(None, jsii.invoke(self, "putDedicatedResources", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#create VertexAiDeploymentResourcePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#delete VertexAiDeploymentResourcePool#delete}.
        '''
        value = VertexAiDeploymentResourcePoolTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDedicatedResources")
    def reset_dedicated_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicatedResources", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

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
    @jsii.member(jsii_name="dedicatedResources")
    def dedicated_resources(
        self,
    ) -> "VertexAiDeploymentResourcePoolDedicatedResourcesOutputReference":
        return typing.cast("VertexAiDeploymentResourcePoolDedicatedResourcesOutputReference", jsii.get(self, "dedicatedResources"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VertexAiDeploymentResourcePoolTimeoutsOutputReference":
        return typing.cast("VertexAiDeploymentResourcePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourcesInput")
    def dedicated_resources_input(
        self,
    ) -> typing.Optional["VertexAiDeploymentResourcePoolDedicatedResources"]:
        return typing.cast(typing.Optional["VertexAiDeploymentResourcePoolDedicatedResources"], jsii.get(self, "dedicatedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiDeploymentResourcePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VertexAiDeploymentResourcePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec98626ca5ecfd026cd2244137c4c4dd8cfb9216519e1fe89b945532523f80da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517b287b75e2fa96dfed45d99001b8ee1bd36ff592e13b22a438bd5cd4ad827f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f628fc5330b85e9e018892f5103c23f857e196d986d8c54be6f4ae4e1a51c1f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e3ab9bdf783e932c61702b6ac041582b3073fa8dc244921346f289a3896bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "dedicated_resources": "dedicatedResources",
        "id": "id",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class VertexAiDeploymentResourcePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        dedicated_resources: typing.Optional[typing.Union["VertexAiDeploymentResourcePoolDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["VertexAiDeploymentResourcePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of deployment resource pool. The maximum length is 63 characters, and valid characters are '/^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#name VertexAiDeploymentResourcePool#name}
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#dedicated_resources VertexAiDeploymentResourcePool#dedicated_resources}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#id VertexAiDeploymentResourcePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#project VertexAiDeploymentResourcePool#project}.
        :param region: The region of deployment resource pool. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#region VertexAiDeploymentResourcePool#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#timeouts VertexAiDeploymentResourcePool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dedicated_resources, dict):
            dedicated_resources = VertexAiDeploymentResourcePoolDedicatedResources(**dedicated_resources)
        if isinstance(timeouts, dict):
            timeouts = VertexAiDeploymentResourcePoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3024004cefea8af296831c59fe8f80af6f9455b711855009461c2728cf3c464)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dedicated_resources", value=dedicated_resources, expected_type=type_hints["dedicated_resources"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if dedicated_resources is not None:
            self._values["dedicated_resources"] = dedicated_resources
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
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
    def name(self) -> builtins.str:
        '''The resource name of deployment resource pool. The maximum length is 63 characters, and valid characters are '/^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$/'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#name VertexAiDeploymentResourcePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dedicated_resources(
        self,
    ) -> typing.Optional["VertexAiDeploymentResourcePoolDedicatedResources"]:
        '''dedicated_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#dedicated_resources VertexAiDeploymentResourcePool#dedicated_resources}
        '''
        result = self._values.get("dedicated_resources")
        return typing.cast(typing.Optional["VertexAiDeploymentResourcePoolDedicatedResources"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#id VertexAiDeploymentResourcePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#project VertexAiDeploymentResourcePool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of deployment resource pool. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#region VertexAiDeploymentResourcePool#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VertexAiDeploymentResourcePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#timeouts VertexAiDeploymentResourcePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VertexAiDeploymentResourcePoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiDeploymentResourcePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolDedicatedResources",
    jsii_struct_bases=[],
    name_mapping={
        "machine_spec": "machineSpec",
        "min_replica_count": "minReplicaCount",
        "autoscaling_metric_specs": "autoscalingMetricSpecs",
        "max_replica_count": "maxReplicaCount",
    },
)
class VertexAiDeploymentResourcePoolDedicatedResources:
    def __init__(
        self,
        *,
        machine_spec: typing.Union["VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#machine_spec VertexAiDeploymentResourcePool#machine_spec}
        :param min_replica_count: The minimum number of machine replicas this DeployedModel will be always deployed on. This value must be greater than or equal to 1. If traffic against the DeployedModel increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#min_replica_count VertexAiDeploymentResourcePool#min_replica_count}
        :param autoscaling_metric_specs: autoscaling_metric_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#autoscaling_metric_specs VertexAiDeploymentResourcePool#autoscaling_metric_specs}
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#max_replica_count VertexAiDeploymentResourcePool#max_replica_count}
        '''
        if isinstance(machine_spec, dict):
            machine_spec = VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec(**machine_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64ce7621644468c4c8b49badb9b43c2f07e6130db72bf87a8935af892a886037)
            check_type(argname="argument machine_spec", value=machine_spec, expected_type=type_hints["machine_spec"])
            check_type(argname="argument min_replica_count", value=min_replica_count, expected_type=type_hints["min_replica_count"])
            check_type(argname="argument autoscaling_metric_specs", value=autoscaling_metric_specs, expected_type=type_hints["autoscaling_metric_specs"])
            check_type(argname="argument max_replica_count", value=max_replica_count, expected_type=type_hints["max_replica_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "machine_spec": machine_spec,
            "min_replica_count": min_replica_count,
        }
        if autoscaling_metric_specs is not None:
            self._values["autoscaling_metric_specs"] = autoscaling_metric_specs
        if max_replica_count is not None:
            self._values["max_replica_count"] = max_replica_count

    @builtins.property
    def machine_spec(
        self,
    ) -> "VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec":
        '''machine_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#machine_spec VertexAiDeploymentResourcePool#machine_spec}
        '''
        result = self._values.get("machine_spec")
        assert result is not None, "Required property 'machine_spec' is missing"
        return typing.cast("VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec", result)

    @builtins.property
    def min_replica_count(self) -> jsii.Number:
        '''The minimum number of machine replicas this DeployedModel will be always deployed on.

        This value must be greater than or equal to 1. If traffic against the DeployedModel increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#min_replica_count VertexAiDeploymentResourcePool#min_replica_count}
        '''
        result = self._values.get("min_replica_count")
        assert result is not None, "Required property 'min_replica_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def autoscaling_metric_specs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs"]]]:
        '''autoscaling_metric_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#autoscaling_metric_specs VertexAiDeploymentResourcePool#autoscaling_metric_specs}
        '''
        result = self._values.get("autoscaling_metric_specs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs"]]], result)

    @builtins.property
    def max_replica_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases.

        If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#max_replica_count VertexAiDeploymentResourcePool#max_replica_count}
        '''
        result = self._values.get("max_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiDeploymentResourcePoolDedicatedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs",
    jsii_struct_bases=[],
    name_mapping={"metric_name": "metricName", "target": "target"},
)
class VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        target: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metric_name: The resource metric name. Supported metrics: For Online Prediction: * 'aiplatform.googleapis.com/prediction/online/accelerator/duty_cycle' * 'aiplatform.googleapis.com/prediction/online/cpu/utilization'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#metric_name VertexAiDeploymentResourcePool#metric_name}
        :param target: The target resource utilization in percentage (1% - 100%) for the given metric; once the real usage deviates from the target by a certain percentage, the machine replicas change. The default value is 60 (representing 60%) if not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#target VertexAiDeploymentResourcePool#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8a2633f74cfb4790761f3425570af6262dadb73e2961e64d3bc44027fe7efb)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
        }
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''The resource metric name. Supported metrics: For Online Prediction: * 'aiplatform.googleapis.com/prediction/online/accelerator/duty_cycle' * 'aiplatform.googleapis.com/prediction/online/cpu/utilization'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#metric_name VertexAiDeploymentResourcePool#metric_name}
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> typing.Optional[jsii.Number]:
        '''The target resource utilization in percentage (1% - 100%) for the given metric;

        once the real usage deviates from the target by a certain percentage, the machine replicas change. The default value is 60 (representing 60%) if not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#target VertexAiDeploymentResourcePool#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__682864466cfb74d0d2c360eb8f4565237d33276db3f1dcfe1f0dbb3b6dc61d01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae9febda2396544b58fd87562d3cadcb662d16e6553c82c3404d14337f09013)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2c8782a15560c71db575dc9809e7f8800f7b3d9e1c9e98cfaf5372f5ca9380)
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
            type_hints = typing.get_type_hints(_typecheckingstub__140e2a8d26f6f0251e3d0428697c53c869fef1322a603efcb5ec243e9fd875f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__00c7245270bcfa0cdcf1a28969d4d2786025789741c52e2ee3264b9a81cb11b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__828d5c34c164fffbaddac8e0352240fd3a09805b57722c170eaa7e84af08f74c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e716c5feba2c9ef26a5fbf3ed130cd4bba8b509980b91c3d7a3d0ff3c4a28dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30a6388353ed04722212ffa362e4e8d7eebd85a1085f1179f9f036574b2d973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c0e77e687a71e9edec79d313838d61125347d698eb39c56ef1fa4e8c175942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62af483db130ffc1cee3659d1b26fb2480efc3cddf82c2d558b35f442de3fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
        "machine_type": "machineType",
    },
)
class VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators to attach to the machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#accelerator_count VertexAiDeploymentResourcePool#accelerator_count}
        :param accelerator_type: The type of accelerator(s) that may be attached to the machine as per accelerator_count. See possible values `here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/MachineSpec#AcceleratorType>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#accelerator_type VertexAiDeploymentResourcePool#accelerator_type}
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#machine_type VertexAiDeploymentResourcePool#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07a66f5a6576ebb58b7d1df09c14c731a9468e7464900d0b7af808e4200d719)
            check_type(argname="argument accelerator_count", value=accelerator_count, expected_type=type_hints["accelerator_count"])
            check_type(argname="argument accelerator_type", value=accelerator_type, expected_type=type_hints["accelerator_type"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accelerator_count is not None:
            self._values["accelerator_count"] = accelerator_count
        if accelerator_type is not None:
            self._values["accelerator_type"] = accelerator_type
        if machine_type is not None:
            self._values["machine_type"] = machine_type

    @builtins.property
    def accelerator_count(self) -> typing.Optional[jsii.Number]:
        '''The number of accelerators to attach to the machine.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#accelerator_count VertexAiDeploymentResourcePool#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''The type of accelerator(s) that may be attached to the machine as per accelerator_count. See possible values `here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/MachineSpec#AcceleratorType>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#accelerator_type VertexAiDeploymentResourcePool#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#machine_type VertexAiDeploymentResourcePool#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c8d27efd2bc804503aa16f9949a087fed3191849e015cb43bd8a08aec800b78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAcceleratorCount")
    def reset_accelerator_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorCount", []))

    @jsii.member(jsii_name="resetAcceleratorType")
    def reset_accelerator_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcceleratorType", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCountInput")
    def accelerator_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "acceleratorCountInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorTypeInput")
    def accelerator_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acceleratorTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="acceleratorCount")
    def accelerator_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "acceleratorCount"))

    @accelerator_count.setter
    def accelerator_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f885f9cc04b9596c784a96f92a2a9fa930aa253d1ab8b856366769e9b620f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb73217bc4dd5bddb0e4163b793ab45840bef9af1278dd555ad972b89e7bb0e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__894761e074cb90f597422418143283b26240610d1037e3d04ac5bcc566cc4fe8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfa852c1b78b2515dd4536621a89599fe2b807b9f0ff13e2b71214fcce5608c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VertexAiDeploymentResourcePoolDedicatedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolDedicatedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc660ab926416bce318af2d234839833d1afe2894765d809768dd6e8aa2da7e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingMetricSpecs")
    def put_autoscaling_metric_specs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5420d5d3c5f65c81c1242a5d8f538c54c95e3b77af8d06e85c2b46376d19b593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAutoscalingMetricSpecs", [value]))

    @jsii.member(jsii_name="putMachineSpec")
    def put_machine_spec(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators to attach to the machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#accelerator_count VertexAiDeploymentResourcePool#accelerator_count}
        :param accelerator_type: The type of accelerator(s) that may be attached to the machine as per accelerator_count. See possible values `here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/MachineSpec#AcceleratorType>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#accelerator_type VertexAiDeploymentResourcePool#accelerator_type}
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#machine_type VertexAiDeploymentResourcePool#machine_type}
        '''
        value = VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec(
            accelerator_count=accelerator_count,
            accelerator_type=accelerator_type,
            machine_type=machine_type,
        )

        return typing.cast(None, jsii.invoke(self, "putMachineSpec", [value]))

    @jsii.member(jsii_name="resetAutoscalingMetricSpecs")
    def reset_autoscaling_metric_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoscalingMetricSpecs", []))

    @jsii.member(jsii_name="resetMaxReplicaCount")
    def reset_max_replica_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxReplicaCount", []))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricSpecs")
    def autoscaling_metric_specs(
        self,
    ) -> VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList:
        return typing.cast(VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList, jsii.get(self, "autoscalingMetricSpecs"))

    @builtins.property
    @jsii.member(jsii_name="machineSpec")
    def machine_spec(
        self,
    ) -> VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference:
        return typing.cast(VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference, jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricSpecsInput")
    def autoscaling_metric_specs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]], jsii.get(self, "autoscalingMetricSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineSpecInput")
    def machine_spec_input(
        self,
    ) -> typing.Optional[VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec], jsii.get(self, "machineSpecInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ea1d8587b27d505625184527b1e16846e997240e774ee2c776c4bbcf25867d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @min_replica_count.setter
    def min_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e444fe429b09ce9b9e065373ac27f8c7241baccfea5e77e93307eb1390acfc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VertexAiDeploymentResourcePoolDedicatedResources]:
        return typing.cast(typing.Optional[VertexAiDeploymentResourcePoolDedicatedResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VertexAiDeploymentResourcePoolDedicatedResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da095bb19e2c6b7aa045988eda995836aede5c11f2b65b4c98819950466bc70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class VertexAiDeploymentResourcePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#create VertexAiDeploymentResourcePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#delete VertexAiDeploymentResourcePool#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0894c295cb8d944d6c2725ca463838f768c2c3385c78eeaf82839053a7c1255d)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#create VertexAiDeploymentResourcePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/vertex_ai_deployment_resource_pool#delete VertexAiDeploymentResourcePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VertexAiDeploymentResourcePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VertexAiDeploymentResourcePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.vertexAiDeploymentResourcePool.VertexAiDeploymentResourcePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__436976835a9fe8cb3d8e91c36ab439beb8ec42a842a97e14e8eef5754e8fd501)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6644ad65dfb817f24ce7c4f3d0a8ad7e4acf94e0bf9eb3f6ba6276d8df9b8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce8f91f8bb33438dc2f2cdc426b8f5a55b2bec1025067b99545c56ce9786247d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDeploymentResourcePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDeploymentResourcePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDeploymentResourcePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ead4840f14bc759e01bc971317af8854fd633d6f9d1f74ecc148ddde7968452f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VertexAiDeploymentResourcePool",
    "VertexAiDeploymentResourcePoolConfig",
    "VertexAiDeploymentResourcePoolDedicatedResources",
    "VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs",
    "VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList",
    "VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference",
    "VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec",
    "VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference",
    "VertexAiDeploymentResourcePoolDedicatedResourcesOutputReference",
    "VertexAiDeploymentResourcePoolTimeouts",
    "VertexAiDeploymentResourcePoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__892c6181b08154961813a5d94e1e4ecdb96c29a2a5c497b1e6cbfe15ef236982(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    dedicated_resources: typing.Optional[typing.Union[VertexAiDeploymentResourcePoolDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiDeploymentResourcePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__18b19b97fb34041b9ca76bc2b7f24a63a6f454eac08b3cc960d5db4402b17fdf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec98626ca5ecfd026cd2244137c4c4dd8cfb9216519e1fe89b945532523f80da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517b287b75e2fa96dfed45d99001b8ee1bd36ff592e13b22a438bd5cd4ad827f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f628fc5330b85e9e018892f5103c23f857e196d986d8c54be6f4ae4e1a51c1f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e3ab9bdf783e932c61702b6ac041582b3073fa8dc244921346f289a3896bf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3024004cefea8af296831c59fe8f80af6f9455b711855009461c2728cf3c464(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    dedicated_resources: typing.Optional[typing.Union[VertexAiDeploymentResourcePoolDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[VertexAiDeploymentResourcePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64ce7621644468c4c8b49badb9b43c2f07e6130db72bf87a8935af892a886037(
    *,
    machine_spec: typing.Union[VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec, typing.Dict[builtins.str, typing.Any]],
    min_replica_count: jsii.Number,
    autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8a2633f74cfb4790761f3425570af6262dadb73e2961e64d3bc44027fe7efb(
    *,
    metric_name: builtins.str,
    target: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682864466cfb74d0d2c360eb8f4565237d33276db3f1dcfe1f0dbb3b6dc61d01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae9febda2396544b58fd87562d3cadcb662d16e6553c82c3404d14337f09013(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2c8782a15560c71db575dc9809e7f8800f7b3d9e1c9e98cfaf5372f5ca9380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140e2a8d26f6f0251e3d0428697c53c869fef1322a603efcb5ec243e9fd875f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c7245270bcfa0cdcf1a28969d4d2786025789741c52e2ee3264b9a81cb11b3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__828d5c34c164fffbaddac8e0352240fd3a09805b57722c170eaa7e84af08f74c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e716c5feba2c9ef26a5fbf3ed130cd4bba8b509980b91c3d7a3d0ff3c4a28dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30a6388353ed04722212ffa362e4e8d7eebd85a1085f1179f9f036574b2d973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c0e77e687a71e9edec79d313838d61125347d698eb39c56ef1fa4e8c175942(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62af483db130ffc1cee3659d1b26fb2480efc3cddf82c2d558b35f442de3fe2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07a66f5a6576ebb58b7d1df09c14c731a9468e7464900d0b7af808e4200d719(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8d27efd2bc804503aa16f9949a087fed3191849e015cb43bd8a08aec800b78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f885f9cc04b9596c784a96f92a2a9fa930aa253d1ab8b856366769e9b620f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb73217bc4dd5bddb0e4163b793ab45840bef9af1278dd555ad972b89e7bb0e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894761e074cb90f597422418143283b26240610d1037e3d04ac5bcc566cc4fe8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cfa852c1b78b2515dd4536621a89599fe2b807b9f0ff13e2b71214fcce5608c(
    value: typing.Optional[VertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc660ab926416bce318af2d234839833d1afe2894765d809768dd6e8aa2da7e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5420d5d3c5f65c81c1242a5d8f538c54c95e3b77af8d06e85c2b46376d19b593(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1d8587b27d505625184527b1e16846e997240e774ee2c776c4bbcf25867d37(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e444fe429b09ce9b9e065373ac27f8c7241baccfea5e77e93307eb1390acfc8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da095bb19e2c6b7aa045988eda995836aede5c11f2b65b4c98819950466bc70(
    value: typing.Optional[VertexAiDeploymentResourcePoolDedicatedResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0894c295cb8d944d6c2725ca463838f768c2c3385c78eeaf82839053a7c1255d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__436976835a9fe8cb3d8e91c36ab439beb8ec42a842a97e14e8eef5754e8fd501(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6644ad65dfb817f24ce7c4f3d0a8ad7e4acf94e0bf9eb3f6ba6276d8df9b8f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce8f91f8bb33438dc2f2cdc426b8f5a55b2bec1025067b99545c56ce9786247d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead4840f14bc759e01bc971317af8854fd633d6f9d1f74ecc148ddde7968452f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VertexAiDeploymentResourcePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

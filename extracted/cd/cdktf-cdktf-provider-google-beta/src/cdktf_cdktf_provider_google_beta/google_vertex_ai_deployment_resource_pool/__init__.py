r'''
# `google_vertex_ai_deployment_resource_pool`

Refer to the Terraform Registry for docs: [`google_vertex_ai_deployment_resource_pool`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool).
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


class GoogleVertexAiDeploymentResourcePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool google_vertex_ai_deployment_resource_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        dedicated_resources: typing.Optional[typing.Union["GoogleVertexAiDeploymentResourcePoolDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiDeploymentResourcePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool google_vertex_ai_deployment_resource_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The resource name of deployment resource pool. The maximum length is 63 characters, and valid characters are '/^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#name GoogleVertexAiDeploymentResourcePool#name}
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#dedicated_resources GoogleVertexAiDeploymentResourcePool#dedicated_resources}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#id GoogleVertexAiDeploymentResourcePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#project GoogleVertexAiDeploymentResourcePool#project}.
        :param region: The region of deployment resource pool. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#region GoogleVertexAiDeploymentResourcePool#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#timeouts GoogleVertexAiDeploymentResourcePool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd7ac4ede8e3d0c2ef53c29491e48270129648f5faaba3e054ca3168b7c9005)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleVertexAiDeploymentResourcePoolConfig(
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
        '''Generates CDKTF code for importing a GoogleVertexAiDeploymentResourcePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleVertexAiDeploymentResourcePool to import.
        :param import_from_id: The id of the existing GoogleVertexAiDeploymentResourcePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleVertexAiDeploymentResourcePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169834efcef2269680e7c84ae5a782faa4761a454e4cce809a964de925f003e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDedicatedResources")
    def put_dedicated_resources(
        self,
        *,
        machine_spec: typing.Union["GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#machine_spec GoogleVertexAiDeploymentResourcePool#machine_spec}
        :param min_replica_count: The minimum number of machine replicas this DeployedModel will be always deployed on. This value must be greater than or equal to 1. If traffic against the DeployedModel increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#min_replica_count GoogleVertexAiDeploymentResourcePool#min_replica_count}
        :param autoscaling_metric_specs: autoscaling_metric_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#autoscaling_metric_specs GoogleVertexAiDeploymentResourcePool#autoscaling_metric_specs}
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#max_replica_count GoogleVertexAiDeploymentResourcePool#max_replica_count}
        '''
        value = GoogleVertexAiDeploymentResourcePoolDedicatedResources(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#create GoogleVertexAiDeploymentResourcePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#delete GoogleVertexAiDeploymentResourcePool#delete}.
        '''
        value = GoogleVertexAiDeploymentResourcePoolTimeouts(
            create=create, delete=delete
        )

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
    ) -> "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesOutputReference":
        return typing.cast("GoogleVertexAiDeploymentResourcePoolDedicatedResourcesOutputReference", jsii.get(self, "dedicatedResources"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GoogleVertexAiDeploymentResourcePoolTimeoutsOutputReference":
        return typing.cast("GoogleVertexAiDeploymentResourcePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dedicatedResourcesInput")
    def dedicated_resources_input(
        self,
    ) -> typing.Optional["GoogleVertexAiDeploymentResourcePoolDedicatedResources"]:
        return typing.cast(typing.Optional["GoogleVertexAiDeploymentResourcePoolDedicatedResources"], jsii.get(self, "dedicatedResourcesInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiDeploymentResourcePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleVertexAiDeploymentResourcePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b8c326e1612630f94663157b016d47f17ff65c9cfa50aeef46a2e4de8d6de8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604a6e6e8adba57abf956593c460b353375e63e56ad353ca150b95dfb894e692)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1578f1756c98c9d54be567287d38192b47e09fb3e54a7bf8bab8f8d0e047cecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191709a1017fdd335f778f79aec5c6535fd84185222aa7b39347dfeea20695ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolConfig",
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
class GoogleVertexAiDeploymentResourcePoolConfig(
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
        name: builtins.str,
        dedicated_resources: typing.Optional[typing.Union["GoogleVertexAiDeploymentResourcePoolDedicatedResources", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleVertexAiDeploymentResourcePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The resource name of deployment resource pool. The maximum length is 63 characters, and valid characters are '/^`a-z <%5Ba-z0-9-%5D%7B0,61%7D%5Ba-z0-9%5D>`_?$/'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#name GoogleVertexAiDeploymentResourcePool#name}
        :param dedicated_resources: dedicated_resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#dedicated_resources GoogleVertexAiDeploymentResourcePool#dedicated_resources}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#id GoogleVertexAiDeploymentResourcePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#project GoogleVertexAiDeploymentResourcePool#project}.
        :param region: The region of deployment resource pool. eg us-central1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#region GoogleVertexAiDeploymentResourcePool#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#timeouts GoogleVertexAiDeploymentResourcePool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(dedicated_resources, dict):
            dedicated_resources = GoogleVertexAiDeploymentResourcePoolDedicatedResources(**dedicated_resources)
        if isinstance(timeouts, dict):
            timeouts = GoogleVertexAiDeploymentResourcePoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fb80c3b3b11ed20fc4d4422e3b6b39647f671b33a7af28da5e8bd1670fbede)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#name GoogleVertexAiDeploymentResourcePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dedicated_resources(
        self,
    ) -> typing.Optional["GoogleVertexAiDeploymentResourcePoolDedicatedResources"]:
        '''dedicated_resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#dedicated_resources GoogleVertexAiDeploymentResourcePool#dedicated_resources}
        '''
        result = self._values.get("dedicated_resources")
        return typing.cast(typing.Optional["GoogleVertexAiDeploymentResourcePoolDedicatedResources"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#id GoogleVertexAiDeploymentResourcePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#project GoogleVertexAiDeploymentResourcePool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region of deployment resource pool. eg us-central1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#region GoogleVertexAiDeploymentResourcePool#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleVertexAiDeploymentResourcePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#timeouts GoogleVertexAiDeploymentResourcePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleVertexAiDeploymentResourcePoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiDeploymentResourcePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolDedicatedResources",
    jsii_struct_bases=[],
    name_mapping={
        "machine_spec": "machineSpec",
        "min_replica_count": "minReplicaCount",
        "autoscaling_metric_specs": "autoscalingMetricSpecs",
        "max_replica_count": "maxReplicaCount",
    },
)
class GoogleVertexAiDeploymentResourcePoolDedicatedResources:
    def __init__(
        self,
        *,
        machine_spec: typing.Union["GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec", typing.Dict[builtins.str, typing.Any]],
        min_replica_count: jsii.Number,
        autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        max_replica_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param machine_spec: machine_spec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#machine_spec GoogleVertexAiDeploymentResourcePool#machine_spec}
        :param min_replica_count: The minimum number of machine replicas this DeployedModel will be always deployed on. This value must be greater than or equal to 1. If traffic against the DeployedModel increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#min_replica_count GoogleVertexAiDeploymentResourcePool#min_replica_count}
        :param autoscaling_metric_specs: autoscaling_metric_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#autoscaling_metric_specs GoogleVertexAiDeploymentResourcePool#autoscaling_metric_specs}
        :param max_replica_count: The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases. If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#max_replica_count GoogleVertexAiDeploymentResourcePool#max_replica_count}
        '''
        if isinstance(machine_spec, dict):
            machine_spec = GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec(**machine_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87bac5502c939bba4c2a7d4847ff704e582bbd143a108b18f37bba69596eee0c)
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
    ) -> "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec":
        '''machine_spec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#machine_spec GoogleVertexAiDeploymentResourcePool#machine_spec}
        '''
        result = self._values.get("machine_spec")
        assert result is not None, "Required property 'machine_spec' is missing"
        return typing.cast("GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec", result)

    @builtins.property
    def min_replica_count(self) -> jsii.Number:
        '''The minimum number of machine replicas this DeployedModel will be always deployed on.

        This value must be greater than or equal to 1. If traffic against the DeployedModel increases, it may dynamically be deployed onto more replicas, and as traffic decreases, some of these extra replicas may be freed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#min_replica_count GoogleVertexAiDeploymentResourcePool#min_replica_count}
        '''
        result = self._values.get("min_replica_count")
        assert result is not None, "Required property 'min_replica_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def autoscaling_metric_specs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs"]]]:
        '''autoscaling_metric_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#autoscaling_metric_specs GoogleVertexAiDeploymentResourcePool#autoscaling_metric_specs}
        '''
        result = self._values.get("autoscaling_metric_specs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs"]]], result)

    @builtins.property
    def max_replica_count(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of replicas this DeployedModel may be deployed on when the traffic against it increases.

        If the requested value is too large, the deployment will error, but if deployment succeeds then the ability to scale the model to that many replicas is guaranteed (barring service outages). If traffic against the DeployedModel increases beyond what its replicas at maximum may handle, a portion of the traffic will be dropped. If this value is not provided, will use min_replica_count as the default value. The value of this field impacts the charge against Vertex CPU and GPU quotas. Specifically, you will be charged for max_replica_count * number of cores in the selected machine type) and (max_replica_count * number of GPUs per replica in the selected machine type).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#max_replica_count GoogleVertexAiDeploymentResourcePool#max_replica_count}
        '''
        result = self._values.get("max_replica_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiDeploymentResourcePoolDedicatedResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs",
    jsii_struct_bases=[],
    name_mapping={"metric_name": "metricName", "target": "target"},
)
class GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs:
    def __init__(
        self,
        *,
        metric_name: builtins.str,
        target: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param metric_name: The resource metric name. Supported metrics: For Online Prediction: * 'aiplatform.googleapis.com/prediction/online/accelerator/duty_cycle' * 'aiplatform.googleapis.com/prediction/online/cpu/utilization'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#metric_name GoogleVertexAiDeploymentResourcePool#metric_name}
        :param target: The target resource utilization in percentage (1% - 100%) for the given metric; once the real usage deviates from the target by a certain percentage, the machine replicas change. The default value is 60 (representing 60%) if not provided. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#target GoogleVertexAiDeploymentResourcePool#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e318f392e45ae4a6c32e60a8192ac17e887ffd69b08370cd4d1c8857253cf5f0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#metric_name GoogleVertexAiDeploymentResourcePool#metric_name}
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> typing.Optional[jsii.Number]:
        '''The target resource utilization in percentage (1% - 100%) for the given metric;

        once the real usage deviates from the target by a certain percentage, the machine replicas change. The default value is 60 (representing 60%) if not provided.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#target GoogleVertexAiDeploymentResourcePool#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bec41c361d328135ebc4427328542ade960bc85927f01a35547d0c0a826a7ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be6af8bb4771af65f8450f20aeef59f94102f0493d20380e27ceb15e7dadf47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6becae7834d088f30d06aabe74ba0f2e764777942b507faef8869d6257ede7b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__073f510aa3fc899242512e5e9ee95c1def26a2afe8ab44900f359cbe6bbcc6ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8366cbc2ac69b0c00c2a547618d01b852a005da16d1ed9631ce10a5ae6be04d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9aa6fde6986b0e09fd3fd5e09b37b07a0a88ad4d1876f21c45d1f927aca1aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9948547656898b9f14e9690bc46543c7b504c4d8d944e958479b18e3af034de8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cba9dadf2171ef103a2fa9c36179f1ad763e948c728d297041c28d5fc5f2420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "target"))

    @target.setter
    def target(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbb98ad5730ee5dbccd6ff01b79a261f0dfdb0a3b8f20a3d4d8f59a9b5b66053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4fec1f137924a7ea2700dd7f190e3b3cb2778198153c74f5117769b4ed1a0c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec",
    jsii_struct_bases=[],
    name_mapping={
        "accelerator_count": "acceleratorCount",
        "accelerator_type": "acceleratorType",
        "machine_type": "machineType",
    },
)
class GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec:
    def __init__(
        self,
        *,
        accelerator_count: typing.Optional[jsii.Number] = None,
        accelerator_type: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param accelerator_count: The number of accelerators to attach to the machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#accelerator_count GoogleVertexAiDeploymentResourcePool#accelerator_count}
        :param accelerator_type: The type of accelerator(s) that may be attached to the machine as per accelerator_count. See possible values `here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/MachineSpec#AcceleratorType>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#accelerator_type GoogleVertexAiDeploymentResourcePool#accelerator_type}
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#machine_type GoogleVertexAiDeploymentResourcePool#machine_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2342cfcbb74714151c5c0ba2468a3f6edb794a1742cabd3a85e6fbbbb35e421d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#accelerator_count GoogleVertexAiDeploymentResourcePool#accelerator_count}
        '''
        result = self._values.get("accelerator_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def accelerator_type(self) -> typing.Optional[builtins.str]:
        '''The type of accelerator(s) that may be attached to the machine as per accelerator_count. See possible values `here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/MachineSpec#AcceleratorType>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#accelerator_type GoogleVertexAiDeploymentResourcePool#accelerator_type}
        '''
        result = self._values.get("accelerator_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#machine_type GoogleVertexAiDeploymentResourcePool#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c4665abc72e28bf32aea572aadb023915ad26c434e42cba9244169818dd40b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d94f6fea15852717f46a3e98d349527c70622e13d8aa876a6233b32d128888e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="acceleratorType")
    def accelerator_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acceleratorType"))

    @accelerator_type.setter
    def accelerator_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00181762cf89f5fdcc3d09ef398f32e4b3b5779e2bf4cc7affae4d645383a377)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acceleratorType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062aa13e45e7de8e6aaad6ab90a493bc88bc7e07fbfd6e5bf0ac0c24e4cdf56c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7d4036f4ec2d0b875f0e5a9a7d2a155f7247ff054c1f250882536d690a0bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleVertexAiDeploymentResourcePoolDedicatedResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolDedicatedResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e208c859c4493e665821fcb5c2b50117dbfe5054a1934aa2923c282bd0558e83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutoscalingMetricSpecs")
    def put_autoscaling_metric_specs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31d302ddf0253efc243ac0531abc97892119aebf4bf5ecceaf6749327d6bcec)
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
        :param accelerator_count: The number of accelerators to attach to the machine. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#accelerator_count GoogleVertexAiDeploymentResourcePool#accelerator_count}
        :param accelerator_type: The type of accelerator(s) that may be attached to the machine as per accelerator_count. See possible values `here <https://cloud.google.com/vertex-ai/docs/reference/rest/v1/MachineSpec#AcceleratorType>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#accelerator_type GoogleVertexAiDeploymentResourcePool#accelerator_type}
        :param machine_type: The type of the machine. See the `list of machine types supported for prediction <https://cloud.google.com/vertex-ai/docs/predictions/configure-compute#machine-types>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#machine_type GoogleVertexAiDeploymentResourcePool#machine_type}
        '''
        value = GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec(
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
    ) -> GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList:
        return typing.cast(GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList, jsii.get(self, "autoscalingMetricSpecs"))

    @builtins.property
    @jsii.member(jsii_name="machineSpec")
    def machine_spec(
        self,
    ) -> GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference:
        return typing.cast(GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference, jsii.get(self, "machineSpec"))

    @builtins.property
    @jsii.member(jsii_name="autoscalingMetricSpecsInput")
    def autoscaling_metric_specs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]], jsii.get(self, "autoscalingMetricSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineSpecInput")
    def machine_spec_input(
        self,
    ) -> typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec]:
        return typing.cast(typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec], jsii.get(self, "machineSpecInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0d9ed98a2d03e7e001d46261c2eca5b80f31670eb788f4478a74cfb9811c35f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minReplicaCount")
    def min_replica_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minReplicaCount"))

    @min_replica_count.setter
    def min_replica_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3864d9d67c224d159b4f808562db974c5dfbaa623012081fe75d8ec70d6ea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minReplicaCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResources]:
        return typing.cast(typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22826954b57335f481883036f75e1cd154d057fc8144da8f01f79fdd53949885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GoogleVertexAiDeploymentResourcePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#create GoogleVertexAiDeploymentResourcePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#delete GoogleVertexAiDeploymentResourcePool#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde50f4b523349f2a1816fd251add96c1487b794cda8653b09f7d001a83b07d9)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#create GoogleVertexAiDeploymentResourcePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_vertex_ai_deployment_resource_pool#delete GoogleVertexAiDeploymentResourcePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleVertexAiDeploymentResourcePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleVertexAiDeploymentResourcePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleVertexAiDeploymentResourcePool.GoogleVertexAiDeploymentResourcePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b31b2746f3bb77b46b7686b44fcff77a41099f7af89f9234be08f37a3a45244e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6276c26c5641fbcbdf95410044e8167f37101283f929c557a901fbd9040a2478)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f8946ab07ac7223b8cdd6d6b7a5ab60f9cae59cc34e5b7f45e874124c3b82f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiDeploymentResourcePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiDeploymentResourcePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiDeploymentResourcePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df55c2805dd2d5206a698f6c8e4c51c2bfbb1f03c411e92c136366b397005c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleVertexAiDeploymentResourcePool",
    "GoogleVertexAiDeploymentResourcePoolConfig",
    "GoogleVertexAiDeploymentResourcePoolDedicatedResources",
    "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs",
    "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsList",
    "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecsOutputReference",
    "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec",
    "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpecOutputReference",
    "GoogleVertexAiDeploymentResourcePoolDedicatedResourcesOutputReference",
    "GoogleVertexAiDeploymentResourcePoolTimeouts",
    "GoogleVertexAiDeploymentResourcePoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__edd7ac4ede8e3d0c2ef53c29491e48270129648f5faaba3e054ca3168b7c9005(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    dedicated_resources: typing.Optional[typing.Union[GoogleVertexAiDeploymentResourcePoolDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiDeploymentResourcePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__169834efcef2269680e7c84ae5a782faa4761a454e4cce809a964de925f003e3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b8c326e1612630f94663157b016d47f17ff65c9cfa50aeef46a2e4de8d6de8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604a6e6e8adba57abf956593c460b353375e63e56ad353ca150b95dfb894e692(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1578f1756c98c9d54be567287d38192b47e09fb3e54a7bf8bab8f8d0e047cecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191709a1017fdd335f778f79aec5c6535fd84185222aa7b39347dfeea20695ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fb80c3b3b11ed20fc4d4422e3b6b39647f671b33a7af28da5e8bd1670fbede(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    dedicated_resources: typing.Optional[typing.Union[GoogleVertexAiDeploymentResourcePoolDedicatedResources, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleVertexAiDeploymentResourcePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bac5502c939bba4c2a7d4847ff704e582bbd143a108b18f37bba69596eee0c(
    *,
    machine_spec: typing.Union[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec, typing.Dict[builtins.str, typing.Any]],
    min_replica_count: jsii.Number,
    autoscaling_metric_specs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    max_replica_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e318f392e45ae4a6c32e60a8192ac17e887ffd69b08370cd4d1c8857253cf5f0(
    *,
    metric_name: builtins.str,
    target: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bec41c361d328135ebc4427328542ade960bc85927f01a35547d0c0a826a7ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be6af8bb4771af65f8450f20aeef59f94102f0493d20380e27ceb15e7dadf47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6becae7834d088f30d06aabe74ba0f2e764777942b507faef8869d6257ede7b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073f510aa3fc899242512e5e9ee95c1def26a2afe8ab44900f359cbe6bbcc6ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8366cbc2ac69b0c00c2a547618d01b852a005da16d1ed9631ce10a5ae6be04d5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9aa6fde6986b0e09fd3fd5e09b37b07a0a88ad4d1876f21c45d1f927aca1aac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9948547656898b9f14e9690bc46543c7b504c4d8d944e958479b18e3af034de8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cba9dadf2171ef103a2fa9c36179f1ad763e948c728d297041c28d5fc5f2420(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbb98ad5730ee5dbccd6ff01b79a261f0dfdb0a3b8f20a3d4d8f59a9b5b66053(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fec1f137924a7ea2700dd7f190e3b3cb2778198153c74f5117769b4ed1a0c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2342cfcbb74714151c5c0ba2468a3f6edb794a1742cabd3a85e6fbbbb35e421d(
    *,
    accelerator_count: typing.Optional[jsii.Number] = None,
    accelerator_type: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4665abc72e28bf32aea572aadb023915ad26c434e42cba9244169818dd40b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94f6fea15852717f46a3e98d349527c70622e13d8aa876a6233b32d128888e3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00181762cf89f5fdcc3d09ef398f32e4b3b5779e2bf4cc7affae4d645383a377(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062aa13e45e7de8e6aaad6ab90a493bc88bc7e07fbfd6e5bf0ac0c24e4cdf56c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7d4036f4ec2d0b875f0e5a9a7d2a155f7247ff054c1f250882536d690a0bd7(
    value: typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesMachineSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e208c859c4493e665821fcb5c2b50117dbfe5054a1934aa2923c282bd0558e83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31d302ddf0253efc243ac0531abc97892119aebf4bf5ecceaf6749327d6bcec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleVertexAiDeploymentResourcePoolDedicatedResourcesAutoscalingMetricSpecs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9ed98a2d03e7e001d46261c2eca5b80f31670eb788f4478a74cfb9811c35f6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3864d9d67c224d159b4f808562db974c5dfbaa623012081fe75d8ec70d6ea0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22826954b57335f481883036f75e1cd154d057fc8144da8f01f79fdd53949885(
    value: typing.Optional[GoogleVertexAiDeploymentResourcePoolDedicatedResources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde50f4b523349f2a1816fd251add96c1487b794cda8653b09f7d001a83b07d9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31b2746f3bb77b46b7686b44fcff77a41099f7af89f9234be08f37a3a45244e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6276c26c5641fbcbdf95410044e8167f37101283f929c557a901fbd9040a2478(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f8946ab07ac7223b8cdd6d6b7a5ab60f9cae59cc34e5b7f45e874124c3b82f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df55c2805dd2d5206a698f6c8e4c51c2bfbb1f03c411e92c136366b397005c00(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleVertexAiDeploymentResourcePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

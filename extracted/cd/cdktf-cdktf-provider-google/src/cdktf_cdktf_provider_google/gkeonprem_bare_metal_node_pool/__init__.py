r'''
# `google_gkeonprem_bare_metal_node_pool`

Refer to the Terraform Registry for docs: [`google_gkeonprem_bare_metal_node_pool`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool).
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


class GkeonpremBareMetalNodePool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePool",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool google_gkeonprem_bare_metal_node_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bare_metal_cluster: builtins.str,
        location: builtins.str,
        name: builtins.str,
        node_pool_config: typing.Union["GkeonpremBareMetalNodePoolNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremBareMetalNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool google_gkeonprem_bare_metal_node_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bare_metal_cluster: The cluster this node pool belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#bare_metal_cluster GkeonpremBareMetalNodePool#bare_metal_cluster}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#location GkeonpremBareMetalNodePool#location}
        :param name: The bare metal node pool name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#name GkeonpremBareMetalNodePool#name}
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#node_pool_config GkeonpremBareMetalNodePool#node_pool_config}
        :param annotations: Annotations on the Bare Metal Node Pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#annotations GkeonpremBareMetalNodePool#annotations}
        :param display_name: The display name for the Bare Metal Node Pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#display_name GkeonpremBareMetalNodePool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#id GkeonpremBareMetalNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#project GkeonpremBareMetalNodePool#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#timeouts GkeonpremBareMetalNodePool#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae89f28984fcecf5c13a92970964eb933adc5a48ed4d1eda29694f6623a74c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GkeonpremBareMetalNodePoolConfig(
            bare_metal_cluster=bare_metal_cluster,
            location=location,
            name=name,
            node_pool_config=node_pool_config,
            annotations=annotations,
            display_name=display_name,
            id=id,
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
        '''Generates CDKTF code for importing a GkeonpremBareMetalNodePool resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GkeonpremBareMetalNodePool to import.
        :param import_from_id: The id of the existing GkeonpremBareMetalNodePool that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GkeonpremBareMetalNodePool to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10458978ed54ffec57656f87135bd64866d8f08d536f1508a77e01f53b6d6d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putNodePoolConfig")
    def put_node_pool_config(
        self,
        *,
        node_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]],
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalNodePoolNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#node_configs GkeonpremBareMetalNodePool#node_configs}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#labels GkeonpremBareMetalNodePool#labels}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#operating_system GkeonpremBareMetalNodePool#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#taints GkeonpremBareMetalNodePool#taints}
        '''
        value = GkeonpremBareMetalNodePoolNodePoolConfig(
            node_configs=node_configs,
            labels=labels,
            operating_system=operating_system,
            taints=taints,
        )

        return typing.cast(None, jsii.invoke(self, "putNodePoolConfig", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#create GkeonpremBareMetalNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#delete GkeonpremBareMetalNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#update GkeonpremBareMetalNodePool#update}.
        '''
        value = GkeonpremBareMetalNodePoolTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnnotations")
    def reset_annotations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotations", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="deleteTime")
    def delete_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deleteTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveAnnotations")
    def effective_annotations(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveAnnotations"))

    @builtins.property
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfig")
    def node_pool_config(
        self,
    ) -> "GkeonpremBareMetalNodePoolNodePoolConfigOutputReference":
        return typing.cast("GkeonpremBareMetalNodePoolNodePoolConfigOutputReference", jsii.get(self, "nodePoolConfig"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> "GkeonpremBareMetalNodePoolStatusList":
        return typing.cast("GkeonpremBareMetalNodePoolStatusList", jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GkeonpremBareMetalNodePoolTimeoutsOutputReference":
        return typing.cast("GkeonpremBareMetalNodePoolTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="bareMetalClusterInput")
    def bare_metal_cluster_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bareMetalClusterInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodePoolConfigInput")
    def node_pool_config_input(
        self,
    ) -> typing.Optional["GkeonpremBareMetalNodePoolNodePoolConfig"]:
        return typing.cast(typing.Optional["GkeonpremBareMetalNodePoolNodePoolConfig"], jsii.get(self, "nodePoolConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremBareMetalNodePoolTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GkeonpremBareMetalNodePoolTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="annotations")
    def annotations(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "annotations"))

    @annotations.setter
    def annotations(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da79d6e1552c0e192f19122171115ddb6157e17cc35a4844abbabafe8d81537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bareMetalCluster")
    def bare_metal_cluster(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bareMetalCluster"))

    @bare_metal_cluster.setter
    def bare_metal_cluster(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0813367eb14fd40f02dcdff9b371d0abda578a8133ab8ca0adf85c8f2e185a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bareMetalCluster", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d43f66432034b9273978da10883bf1f1075b7be2746ab000f755f8637fa586b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__506eaf4a9f9a9423cd357b4c23a37509bd0637a2928f17154b769c393426ed47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e7b33bf05eed1cad0a234e26f5c89db5626034f7316737c0b6873e52ade922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f614fc263e020a9c6f8945b675e64fb6aaee4df9ef7da488a4d67bcb16ca491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471347c95299bf836159dc37d9340041fc1592b2e9c76fd317b9c2358e92130a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bare_metal_cluster": "bareMetalCluster",
        "location": "location",
        "name": "name",
        "node_pool_config": "nodePoolConfig",
        "annotations": "annotations",
        "display_name": "displayName",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GkeonpremBareMetalNodePoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bare_metal_cluster: builtins.str,
        location: builtins.str,
        name: builtins.str,
        node_pool_config: typing.Union["GkeonpremBareMetalNodePoolNodePoolConfig", typing.Dict[builtins.str, typing.Any]],
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GkeonpremBareMetalNodePoolTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bare_metal_cluster: The cluster this node pool belongs to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#bare_metal_cluster GkeonpremBareMetalNodePool#bare_metal_cluster}
        :param location: The location of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#location GkeonpremBareMetalNodePool#location}
        :param name: The bare metal node pool name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#name GkeonpremBareMetalNodePool#name}
        :param node_pool_config: node_pool_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#node_pool_config GkeonpremBareMetalNodePool#node_pool_config}
        :param annotations: Annotations on the Bare Metal Node Pool. This field has the same restrictions as Kubernetes annotations. The total size of all keys and values combined is limited to 256k. Key can have 2 segments: prefix (optional) and name (required), separated by a slash (/). Prefix must be a DNS subdomain. Name must be 63 characters or less, begin and end with alphanumerics, with dashes (-), underscores (_), dots (.), and alphanumerics between. **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration. Please refer to the field 'effective_annotations' for all of the annotations present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#annotations GkeonpremBareMetalNodePool#annotations}
        :param display_name: The display name for the Bare Metal Node Pool. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#display_name GkeonpremBareMetalNodePool#display_name}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#id GkeonpremBareMetalNodePool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#project GkeonpremBareMetalNodePool#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#timeouts GkeonpremBareMetalNodePool#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(node_pool_config, dict):
            node_pool_config = GkeonpremBareMetalNodePoolNodePoolConfig(**node_pool_config)
        if isinstance(timeouts, dict):
            timeouts = GkeonpremBareMetalNodePoolTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c90ade27064406d3f5985f29eff7d6f5b30504e08feede2ced5515a143aa03)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bare_metal_cluster", value=bare_metal_cluster, expected_type=type_hints["bare_metal_cluster"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_pool_config", value=node_pool_config, expected_type=type_hints["node_pool_config"])
            check_type(argname="argument annotations", value=annotations, expected_type=type_hints["annotations"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bare_metal_cluster": bare_metal_cluster,
            "location": location,
            "name": name,
            "node_pool_config": node_pool_config,
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
        if display_name is not None:
            self._values["display_name"] = display_name
        if id is not None:
            self._values["id"] = id
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
    def bare_metal_cluster(self) -> builtins.str:
        '''The cluster this node pool belongs to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#bare_metal_cluster GkeonpremBareMetalNodePool#bare_metal_cluster}
        '''
        result = self._values.get("bare_metal_cluster")
        assert result is not None, "Required property 'bare_metal_cluster' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''The location of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#location GkeonpremBareMetalNodePool#location}
        '''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The bare metal node pool name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#name GkeonpremBareMetalNodePool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_pool_config(self) -> "GkeonpremBareMetalNodePoolNodePoolConfig":
        '''node_pool_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#node_pool_config GkeonpremBareMetalNodePool#node_pool_config}
        '''
        result = self._values.get("node_pool_config")
        assert result is not None, "Required property 'node_pool_config' is missing"
        return typing.cast("GkeonpremBareMetalNodePoolNodePoolConfig", result)

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Annotations on the Bare Metal Node Pool.

        This field has the same restrictions as Kubernetes annotations.
        The total size of all keys and values combined is limited to 256k.
        Key can have 2 segments: prefix (optional) and name (required),
        separated by a slash (/).
        Prefix must be a DNS subdomain.
        Name must be 63 characters or less, begin and end with alphanumerics,
        with dashes (-), underscores (_), dots (.), and alphanumerics between.

        **Note**: This field is non-authoritative, and will only manage the annotations present in your configuration.
        Please refer to the field 'effective_annotations' for all of the annotations present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#annotations GkeonpremBareMetalNodePool#annotations}
        '''
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name for the Bare Metal Node Pool.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#display_name GkeonpremBareMetalNodePool#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#id GkeonpremBareMetalNodePool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#project GkeonpremBareMetalNodePool#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GkeonpremBareMetalNodePoolTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#timeouts GkeonpremBareMetalNodePool#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GkeonpremBareMetalNodePoolTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolNodePoolConfig",
    jsii_struct_bases=[],
    name_mapping={
        "node_configs": "nodeConfigs",
        "labels": "labels",
        "operating_system": "operatingSystem",
        "taints": "taints",
    },
)
class GkeonpremBareMetalNodePoolNodePoolConfig:
    def __init__(
        self,
        *,
        node_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs", typing.Dict[builtins.str, typing.Any]]]],
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        operating_system: typing.Optional[builtins.str] = None,
        taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalNodePoolNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param node_configs: node_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#node_configs GkeonpremBareMetalNodePool#node_configs}
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#labels GkeonpremBareMetalNodePool#labels}
        :param operating_system: Specifies the nodes operating system (default: LINUX). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#operating_system GkeonpremBareMetalNodePool#operating_system}
        :param taints: taints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#taints GkeonpremBareMetalNodePool#taints}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb0a8420261b7d19e12a7146b1176d8e247d66088f4b2252587e19d5eb1e9947)
            check_type(argname="argument node_configs", value=node_configs, expected_type=type_hints["node_configs"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument operating_system", value=operating_system, expected_type=type_hints["operating_system"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "node_configs": node_configs,
        }
        if labels is not None:
            self._values["labels"] = labels
        if operating_system is not None:
            self._values["operating_system"] = operating_system
        if taints is not None:
            self._values["taints"] = taints

    @builtins.property
    def node_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs"]]:
        '''node_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#node_configs GkeonpremBareMetalNodePool#node_configs}
        '''
        result = self._values.get("node_configs")
        assert result is not None, "Required property 'node_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs"]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The map of Kubernetes labels (key/value pairs) to be applied to each node.

        These will added in addition to any default label(s)
        that Kubernetes may apply to the node. In case of conflict in
        label keys, the applied set may differ depending on the Kubernetes
        version -- it's best to assume the behavior is undefined and
        conflicts should be avoided. For more information, including usage
        and the valid values, see:

        - http://kubernetes.io/v1.1/docs/user-guide/labels.html
          An object containing a list of "key": value pairs.
          For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#labels GkeonpremBareMetalNodePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def operating_system(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#operating_system GkeonpremBareMetalNodePool#operating_system}
        '''
        result = self._values.get("operating_system")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalNodePoolNodePoolConfigTaints"]]]:
        '''taints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#taints GkeonpremBareMetalNodePool#taints}
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalNodePoolNodePoolConfigTaints"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalNodePoolNodePoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels", "node_ip": "nodeIp"},
)
class GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        node_ip: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param labels: The map of Kubernetes labels (key/value pairs) to be applied to each node. These will added in addition to any default label(s) that Kubernetes may apply to the node. In case of conflict in label keys, the applied set may differ depending on the Kubernetes version -- it's best to assume the behavior is undefined and conflicts should be avoided. For more information, including usage and the valid values, see: - http://kubernetes.io/v1.1/docs/user-guide/labels.html An object containing a list of "key": value pairs. For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#labels GkeonpremBareMetalNodePool#labels}
        :param node_ip: The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#node_ip GkeonpremBareMetalNodePool#node_ip}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad77d61f72128997d51c62d670eb5faa75438ab14dcd3cdb0516508b797dd983)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument node_ip", value=node_ip, expected_type=type_hints["node_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels
        if node_ip is not None:
            self._values["node_ip"] = node_ip

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The map of Kubernetes labels (key/value pairs) to be applied to each node.

        These will added in addition to any default label(s)
        that Kubernetes may apply to the node. In case of conflict in
        label keys, the applied set may differ depending on the Kubernetes
        version -- it's best to assume the behavior is undefined and
        conflicts should be avoided. For more information, including usage
        and the valid values, see:

        - http://kubernetes.io/v1.1/docs/user-guide/labels.html
          An object containing a list of "key": value pairs.
          For example: { "name": "wrench", "mass": "1.3kg", "count": "3" }.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#labels GkeonpremBareMetalNodePool#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def node_ip(self) -> typing.Optional[builtins.str]:
        '''The default IPv4 address for SSH access and Kubernetes node. Example: 192.168.0.1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#node_ip GkeonpremBareMetalNodePool#node_ip}
        '''
        result = self._values.get("node_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b71d77b0e69b101772b91fa7897a5d687c6746fa62068a102afe48f2bd6cd0d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ead402050febc0173bdced756a9f86c7d619efecca459181d4f83230a47beb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__202fee8ada5b77726d3dac9b33ded9a8ecdb574230699e702f604abd8e43ec60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c4fbc4e6de87afa19c7bd1688c9ea7475348bcba0a14c0c0db0d03a05ac038c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__681c2e0dbc35c28ea550b9b0c15b69f0cc60a72cbd28d4553d1927f22cb76392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be20363eb5af0c5e46febecdc3104bf10d9c9232d39abfdc3767d6610bc6e1d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50976940805a191db7082eeb3b3d7e7fd40fbc673cf89083deaa531589f0e09a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetNodeIp")
    def reset_node_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeIp", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeIpInput")
    def node_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeIpInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d83358bc91d2f9ca15233a7820c286be6f573bf13fa75c1e8306a6f93392ac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeIp")
    def node_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeIp"))

    @node_ip.setter
    def node_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f930f4d3003969163617f5091146db5157a8803a227e3a0badfecbdc20476e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8884382c40aa2efb26e1469b5d444d708aa23e8a444db4712ab0a65656b80652)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalNodePoolNodePoolConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolNodePoolConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a326e14bda5cb1fc44b5241f0c82e4d4263398a6fe2937bf85b75b5bb99271ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putNodeConfigs")
    def put_node_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515c6d4968e70d7b4b6b5274c53d75b4a0a3e1cbc53f430bb42a50f66b61a873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNodeConfigs", [value]))

    @jsii.member(jsii_name="putTaints")
    def put_taints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GkeonpremBareMetalNodePoolNodePoolConfigTaints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6b87ff452c7fddc53a291638c0bb76f4b5bf2754488ea9c0ec793d9dc2f573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTaints", [value]))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetOperatingSystem")
    def reset_operating_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperatingSystem", []))

    @jsii.member(jsii_name="resetTaints")
    def reset_taints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTaints", []))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigs")
    def node_configs(self) -> GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsList:
        return typing.cast(GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsList, jsii.get(self, "nodeConfigs"))

    @builtins.property
    @jsii.member(jsii_name="taints")
    def taints(self) -> "GkeonpremBareMetalNodePoolNodePoolConfigTaintsList":
        return typing.cast("GkeonpremBareMetalNodePoolNodePoolConfigTaintsList", jsii.get(self, "taints"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeConfigsInput")
    def node_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]]], jsii.get(self, "nodeConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatingSystemInput")
    def operating_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatingSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="taintsInput")
    def taints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalNodePoolNodePoolConfigTaints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GkeonpremBareMetalNodePoolNodePoolConfigTaints"]]], jsii.get(self, "taintsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ead5e5f9fd47f87a2e6168e6e9a404fa53700f8d94da240a3d55858b4e90144)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operatingSystem")
    def operating_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operatingSystem"))

    @operating_system.setter
    def operating_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ec5c4137339e4caf4e9818940bbe4b8465064ac6c3e26450ad9dbd56ec5755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operatingSystem", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GkeonpremBareMetalNodePoolNodePoolConfig]:
        return typing.cast(typing.Optional[GkeonpremBareMetalNodePoolNodePoolConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalNodePoolNodePoolConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18495bebff0a6d1066b922e014428b8b30186738bb676884bd1ec83d08e35ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolNodePoolConfigTaints",
    jsii_struct_bases=[],
    name_mapping={"effect": "effect", "key": "key", "value": "value"},
)
class GkeonpremBareMetalNodePoolNodePoolConfigTaints:
    def __init__(
        self,
        *,
        effect: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effect: Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#effect GkeonpremBareMetalNodePool#effect}
        :param key: Key associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#key GkeonpremBareMetalNodePool#key}
        :param value: Value associated with the effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#value GkeonpremBareMetalNodePool#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8178cab448e78912e3612024100ac2e0a1e158b2848ac8024e9a33ad291d7d88)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if effect is not None:
            self._values["effect"] = effect
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def effect(self) -> typing.Optional[builtins.str]:
        '''Specifies the nodes operating system (default: LINUX). Possible values: ["EFFECT_UNSPECIFIED", "PREFER_NO_SCHEDULE", "NO_EXECUTE"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#effect GkeonpremBareMetalNodePool#effect}
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Key associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#key GkeonpremBareMetalNodePool#key}
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Value associated with the effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#value GkeonpremBareMetalNodePool#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalNodePoolNodePoolConfigTaints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalNodePoolNodePoolConfigTaintsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolNodePoolConfigTaintsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__26727363da200f4b0e81c07d8e8bea28afc15716814fd3eb11cad115dead5186)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalNodePoolNodePoolConfigTaintsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eedbfe7bcf888a57a7cb09bb41a3ab2d7720b7a6100093471b555c3ef5a658bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalNodePoolNodePoolConfigTaintsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c361d8782c72263319c9ed05cc0a029b9ebb7ece9cab06858d8bd815df56b7af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__004a799c6910f0e6ffa8a83ba7d78672aaa52883d446de7c4df8fc5ff0f008cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc09c58f64a893283172f31a855cc6b506f2885bd52fe829b592943d504e46de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigTaints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigTaints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigTaints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d27ad6cef2072f1a2fec4c89097af476f59476ab21660117184014739537166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalNodePoolNodePoolConfigTaintsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolNodePoolConfigTaintsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80268ffaa134b87b2bb74620c1c84dee999a08b4fa245d6a2fb87f20995585d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEffect")
    def reset_effect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffect", []))

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57359ef42e744354a63a07ba647e3434d61f6513ab5baafaede7e7fd6bcc0aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238f9c2ba139954dd9b294acb419ab94d41df7978dc3e503cd3b3ebc1fc8a353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17677ecc9769bb558d9c819f559754c149bf03d2f4fe517a414e1b53b335121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolNodePoolConfigTaints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolNodePoolConfigTaints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolNodePoolConfigTaints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28894c37456f9f78ac8015004acc4fe5ebcfd5ae40ea8e51f69216a03b2e242c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalNodePoolStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalNodePoolStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolStatusConditions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GkeonpremBareMetalNodePoolStatusConditions:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalNodePoolStatusConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalNodePoolStatusConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolStatusConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__545a7f1da4db8473b80ca118032a47f5156e9634336d4175488724ffa19b8981)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalNodePoolStatusConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c166ab80fa1d40a683783f4da8cd1fb9583f5907aef1867b67feafb27a1090c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalNodePoolStatusConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25f3facc9d5d28dbb7601a871f6885f1b239576b10ae89e954523a82d4483b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5525269c1c155bf5c5b2656aadd41e70a933396ae949f54aaef4749b26c002ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24ce48d0d1d2e1b27587d3f4686e627650eaf0a4102fa2d70db9043f67a8af2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalNodePoolStatusConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolStatusConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd7d6275fadbc13c15680e0f34007488c70370a8a00ce5bcd694216b55c78cd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
    ) -> typing.Optional[GkeonpremBareMetalNodePoolStatusConditions]:
        return typing.cast(typing.Optional[GkeonpremBareMetalNodePoolStatusConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalNodePoolStatusConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66762ec141b40cdb73c3dd7b993a99cd8c141e6a5416bc8fb373382f2c096046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalNodePoolStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolStatusList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bb3f3f6c4b6372252c659f38d5b3e8699aeb8b53f23a03472b820edea3a4033)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GkeonpremBareMetalNodePoolStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3ff4c2ab2c24304018887ba6dcb1b8f97754c1b485a60cd847b364683ffccb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GkeonpremBareMetalNodePoolStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da4a154bfa05ef9ac977167d877ee5997ca1f0f7f4c5ee4d9c2c9cf25bdc2d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed9c5b116a11d53d1f181785edb1d2f8a8803d0de28cbc389cdd59b104d273b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31052e045ee8716ff1b29493c4a2e2dd8d7903d8b49f1f753f3adad072954b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GkeonpremBareMetalNodePoolStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolStatusOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42beb3e7460ee4d5f7b07005a6d4c5aea58f86ba63f26d14502366f80ee037a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> GkeonpremBareMetalNodePoolStatusConditionsList:
        return typing.cast(GkeonpremBareMetalNodePoolStatusConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="errorMessage")
    def error_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "errorMessage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GkeonpremBareMetalNodePoolStatus]:
        return typing.cast(typing.Optional[GkeonpremBareMetalNodePoolStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GkeonpremBareMetalNodePoolStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4306b7d3e2fc353431f0349c83c03eb2b81c0bf14ddbb67dba426b0bb731d0b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GkeonpremBareMetalNodePoolTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#create GkeonpremBareMetalNodePool#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#delete GkeonpremBareMetalNodePool#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#update GkeonpremBareMetalNodePool#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63d88615a9ce9e16759af1d3b56f1ef64b47074cde9162433bef226e2f166e4)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#create GkeonpremBareMetalNodePool#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#delete GkeonpremBareMetalNodePool#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/gkeonprem_bare_metal_node_pool#update GkeonpremBareMetalNodePool#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GkeonpremBareMetalNodePoolTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GkeonpremBareMetalNodePoolTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gkeonpremBareMetalNodePool.GkeonpremBareMetalNodePoolTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81a0ac267514155af7762fd329279b4b6aaf24b97f5827aeae0e80b1be093b89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0fdacbfaf5bdf8090fb1767c45dd063cc2ceb9b4d83eb832f6e999c566aaa1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071c26b8ba58439557dade9fa4e153267d328c31bd38206d69bd7d8d86a26845)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6582acae2fc28e68587ccbbbb25a10afae9d1d9ea3eece9d67facce9774a15b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__424e6b43e3064d8bb40ffb58054afead921726bcb068dd98cbd6e45febc51550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GkeonpremBareMetalNodePool",
    "GkeonpremBareMetalNodePoolConfig",
    "GkeonpremBareMetalNodePoolNodePoolConfig",
    "GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs",
    "GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsList",
    "GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigsOutputReference",
    "GkeonpremBareMetalNodePoolNodePoolConfigOutputReference",
    "GkeonpremBareMetalNodePoolNodePoolConfigTaints",
    "GkeonpremBareMetalNodePoolNodePoolConfigTaintsList",
    "GkeonpremBareMetalNodePoolNodePoolConfigTaintsOutputReference",
    "GkeonpremBareMetalNodePoolStatus",
    "GkeonpremBareMetalNodePoolStatusConditions",
    "GkeonpremBareMetalNodePoolStatusConditionsList",
    "GkeonpremBareMetalNodePoolStatusConditionsOutputReference",
    "GkeonpremBareMetalNodePoolStatusList",
    "GkeonpremBareMetalNodePoolStatusOutputReference",
    "GkeonpremBareMetalNodePoolTimeouts",
    "GkeonpremBareMetalNodePoolTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__4ae89f28984fcecf5c13a92970964eb933adc5a48ed4d1eda29694f6623a74c7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bare_metal_cluster: builtins.str,
    location: builtins.str,
    name: builtins.str,
    node_pool_config: typing.Union[GkeonpremBareMetalNodePoolNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremBareMetalNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c10458978ed54ffec57656f87135bd64866d8f08d536f1508a77e01f53b6d6d0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da79d6e1552c0e192f19122171115ddb6157e17cc35a4844abbabafe8d81537(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0813367eb14fd40f02dcdff9b371d0abda578a8133ab8ca0adf85c8f2e185a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d43f66432034b9273978da10883bf1f1075b7be2746ab000f755f8637fa586b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__506eaf4a9f9a9423cd357b4c23a37509bd0637a2928f17154b769c393426ed47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e7b33bf05eed1cad0a234e26f5c89db5626034f7316737c0b6873e52ade922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f614fc263e020a9c6f8945b675e64fb6aaee4df9ef7da488a4d67bcb16ca491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471347c95299bf836159dc37d9340041fc1592b2e9c76fd317b9c2358e92130a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c90ade27064406d3f5985f29eff7d6f5b30504e08feede2ced5515a143aa03(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bare_metal_cluster: builtins.str,
    location: builtins.str,
    name: builtins.str,
    node_pool_config: typing.Union[GkeonpremBareMetalNodePoolNodePoolConfig, typing.Dict[builtins.str, typing.Any]],
    annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GkeonpremBareMetalNodePoolTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0a8420261b7d19e12a7146b1176d8e247d66088f4b2252587e19d5eb1e9947(
    *,
    node_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    operating_system: typing.Optional[builtins.str] = None,
    taints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalNodePoolNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad77d61f72128997d51c62d670eb5faa75438ab14dcd3cdb0516508b797dd983(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    node_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b71d77b0e69b101772b91fa7897a5d687c6746fa62068a102afe48f2bd6cd0d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ead402050febc0173bdced756a9f86c7d619efecca459181d4f83230a47beb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__202fee8ada5b77726d3dac9b33ded9a8ecdb574230699e702f604abd8e43ec60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4fbc4e6de87afa19c7bd1688c9ea7475348bcba0a14c0c0db0d03a05ac038c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681c2e0dbc35c28ea550b9b0c15b69f0cc60a72cbd28d4553d1927f22cb76392(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be20363eb5af0c5e46febecdc3104bf10d9c9232d39abfdc3767d6610bc6e1d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50976940805a191db7082eeb3b3d7e7fd40fbc673cf89083deaa531589f0e09a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d83358bc91d2f9ca15233a7820c286be6f573bf13fa75c1e8306a6f93392ac6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f930f4d3003969163617f5091146db5157a8803a227e3a0badfecbdc20476e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8884382c40aa2efb26e1469b5d444d708aa23e8a444db4712ab0a65656b80652(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a326e14bda5cb1fc44b5241f0c82e4d4263398a6fe2937bf85b75b5bb99271ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515c6d4968e70d7b4b6b5274c53d75b4a0a3e1cbc53f430bb42a50f66b61a873(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalNodePoolNodePoolConfigNodeConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f6b87ff452c7fddc53a291638c0bb76f4b5bf2754488ea9c0ec793d9dc2f573(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GkeonpremBareMetalNodePoolNodePoolConfigTaints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ead5e5f9fd47f87a2e6168e6e9a404fa53700f8d94da240a3d55858b4e90144(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ec5c4137339e4caf4e9818940bbe4b8465064ac6c3e26450ad9dbd56ec5755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18495bebff0a6d1066b922e014428b8b30186738bb676884bd1ec83d08e35ec(
    value: typing.Optional[GkeonpremBareMetalNodePoolNodePoolConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8178cab448e78912e3612024100ac2e0a1e158b2848ac8024e9a33ad291d7d88(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26727363da200f4b0e81c07d8e8bea28afc15716814fd3eb11cad115dead5186(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eedbfe7bcf888a57a7cb09bb41a3ab2d7720b7a6100093471b555c3ef5a658bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c361d8782c72263319c9ed05cc0a029b9ebb7ece9cab06858d8bd815df56b7af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__004a799c6910f0e6ffa8a83ba7d78672aaa52883d446de7c4df8fc5ff0f008cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc09c58f64a893283172f31a855cc6b506f2885bd52fe829b592943d504e46de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d27ad6cef2072f1a2fec4c89097af476f59476ab21660117184014739537166(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GkeonpremBareMetalNodePoolNodePoolConfigTaints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80268ffaa134b87b2bb74620c1c84dee999a08b4fa245d6a2fb87f20995585d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57359ef42e744354a63a07ba647e3434d61f6513ab5baafaede7e7fd6bcc0aec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238f9c2ba139954dd9b294acb419ab94d41df7978dc3e503cd3b3ebc1fc8a353(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17677ecc9769bb558d9c819f559754c149bf03d2f4fe517a414e1b53b335121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28894c37456f9f78ac8015004acc4fe5ebcfd5ae40ea8e51f69216a03b2e242c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolNodePoolConfigTaints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545a7f1da4db8473b80ca118032a47f5156e9634336d4175488724ffa19b8981(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c166ab80fa1d40a683783f4da8cd1fb9583f5907aef1867b67feafb27a1090c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25f3facc9d5d28dbb7601a871f6885f1b239576b10ae89e954523a82d4483b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5525269c1c155bf5c5b2656aadd41e70a933396ae949f54aaef4749b26c002ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ce48d0d1d2e1b27587d3f4686e627650eaf0a4102fa2d70db9043f67a8af2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7d6275fadbc13c15680e0f34007488c70370a8a00ce5bcd694216b55c78cd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66762ec141b40cdb73c3dd7b993a99cd8c141e6a5416bc8fb373382f2c096046(
    value: typing.Optional[GkeonpremBareMetalNodePoolStatusConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb3f3f6c4b6372252c659f38d5b3e8699aeb8b53f23a03472b820edea3a4033(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3ff4c2ab2c24304018887ba6dcb1b8f97754c1b485a60cd847b364683ffccb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da4a154bfa05ef9ac977167d877ee5997ca1f0f7f4c5ee4d9c2c9cf25bdc2d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9c5b116a11d53d1f181785edb1d2f8a8803d0de28cbc389cdd59b104d273b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31052e045ee8716ff1b29493c4a2e2dd8d7903d8b49f1f753f3adad072954b27(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42beb3e7460ee4d5f7b07005a6d4c5aea58f86ba63f26d14502366f80ee037a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4306b7d3e2fc353431f0349c83c03eb2b81c0bf14ddbb67dba426b0bb731d0b8(
    value: typing.Optional[GkeonpremBareMetalNodePoolStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63d88615a9ce9e16759af1d3b56f1ef64b47074cde9162433bef226e2f166e4(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a0ac267514155af7762fd329279b4b6aaf24b97f5827aeae0e80b1be093b89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0fdacbfaf5bdf8090fb1767c45dd063cc2ceb9b4d83eb832f6e999c566aaa1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071c26b8ba58439557dade9fa4e153267d328c31bd38206d69bd7d8d86a26845(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6582acae2fc28e68587ccbbbb25a10afae9d1d9ea3eece9d67facce9774a15b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424e6b43e3064d8bb40ffb58054afead921726bcb068dd98cbd6e45febc51550(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GkeonpremBareMetalNodePoolTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

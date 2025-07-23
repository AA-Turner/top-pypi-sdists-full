r'''
# `google_network_services_http_route`

Refer to the Terraform Registry for docs: [`google_network_services_http_route`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route).
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


class NetworkServicesHttpRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route google_network_services_http_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hostnames: typing.Sequence[builtins.str],
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesHttpRouteRules", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesHttpRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route google_network_services_http_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hostnames: Set of hosts that should match against the HTTP host header to select a HttpRoute to process the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#hostnames NetworkServicesHttpRoute#hostnames}
        :param name: Name of the HttpRoute resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#name NetworkServicesHttpRoute#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#rules NetworkServicesHttpRoute#rules}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#description NetworkServicesHttpRoute#description}
        :param gateways: Gateways defines a list of gateways this HttpRoute is attached to, as one of the routing rules to route the requests served by the gateway. Each gateway reference should match the pattern: projects/* /locations/global/gateways/<gateway_name> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#gateways NetworkServicesHttpRoute#gateways} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#id NetworkServicesHttpRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the HttpRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#labels NetworkServicesHttpRoute#labels}
        :param meshes: Meshes defines a list of meshes this HttpRoute is attached to, as one of the routing rules to route the requests served by the mesh. Each mesh reference should match the pattern: projects/* /locations/global/meshes/<mesh_name>. The attached Mesh should be of a type SIDECAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#meshes NetworkServicesHttpRoute#meshes} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#project NetworkServicesHttpRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#timeouts NetworkServicesHttpRoute#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c305cc4def0e7d84ad90252987aaaee7eecb9190e0d8c1e504d552b4cfd35a80)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkServicesHttpRouteConfig(
            hostnames=hostnames,
            name=name,
            rules=rules,
            description=description,
            gateways=gateways,
            id=id,
            labels=labels,
            meshes=meshes,
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
        '''Generates CDKTF code for importing a NetworkServicesHttpRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkServicesHttpRoute to import.
        :param import_from_id: The id of the existing NetworkServicesHttpRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkServicesHttpRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2f0fc791c29ff5e27baee8bdf133c693719c925e43aaaaf50f119018d5832c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesHttpRouteRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a3875fd223efb3c343e731b00bc34cbb1b9eedf3ae9b9011e74af25a16d85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#create NetworkServicesHttpRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#delete NetworkServicesHttpRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#update NetworkServicesHttpRoute#update}.
        '''
        value = NetworkServicesHttpRouteTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetGateways")
    def reset_gateways(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGateways", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMeshes")
    def reset_meshes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMeshes", []))

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
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "NetworkServicesHttpRouteRulesList":
        return typing.cast("NetworkServicesHttpRouteRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetworkServicesHttpRouteTimeoutsOutputReference":
        return typing.cast("NetworkServicesHttpRouteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewaysInput")
    def gateways_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gatewaysInput"))

    @builtins.property
    @jsii.member(jsii_name="hostnamesInput")
    def hostnames_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostnamesInput"))

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
    @jsii.member(jsii_name="meshesInput")
    def meshes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "meshesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesHttpRouteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesHttpRouteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11cecc59284f0d66aff4d20bd6a649656ba8ee3fc6a6ec720077ca473b2f53c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gateways")
    def gateways(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gateways"))

    @gateways.setter
    def gateways(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86d78f808efb1fcb75e09e1882cd362c90604549cbbaeb4eae9618c2f6e63b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateways", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostnames")
    def hostnames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostnames"))

    @hostnames.setter
    def hostnames(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bcd3a5a33a3858329ea03482cd320c94ba36b4a1e9c05f29fcd08d5c7a602a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caaf01b18285ecf904b9449b8a7685ab3dab96fdb0eacd913e94b20c38223ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__322b9ba204ae321e174534f830736479cecedba30a9c8e498f9b7ce78aff0a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshes")
    def meshes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "meshes"))

    @meshes.setter
    def meshes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf064eed1ec4eb5220ad4f895c36f9bafc2961b58c3bf4adf3ad4dd53d0dc861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__747e8577dda277cc3177ac6a748e98ed797245217fd9a74430ad38d8145daaa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e65bff319ee0df7515bcb38a28c7afd3bfefc5b678cf285dbfdc58cc411ae4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "hostnames": "hostnames",
        "name": "name",
        "rules": "rules",
        "description": "description",
        "gateways": "gateways",
        "id": "id",
        "labels": "labels",
        "meshes": "meshes",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class NetworkServicesHttpRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        hostnames: typing.Sequence[builtins.str],
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesHttpRouteRules", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesHttpRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hostnames: Set of hosts that should match against the HTTP host header to select a HttpRoute to process the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#hostnames NetworkServicesHttpRoute#hostnames}
        :param name: Name of the HttpRoute resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#name NetworkServicesHttpRoute#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#rules NetworkServicesHttpRoute#rules}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#description NetworkServicesHttpRoute#description}
        :param gateways: Gateways defines a list of gateways this HttpRoute is attached to, as one of the routing rules to route the requests served by the gateway. Each gateway reference should match the pattern: projects/* /locations/global/gateways/<gateway_name> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#gateways NetworkServicesHttpRoute#gateways} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#id NetworkServicesHttpRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the HttpRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#labels NetworkServicesHttpRoute#labels}
        :param meshes: Meshes defines a list of meshes this HttpRoute is attached to, as one of the routing rules to route the requests served by the mesh. Each mesh reference should match the pattern: projects/* /locations/global/meshes/<mesh_name>. The attached Mesh should be of a type SIDECAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#meshes NetworkServicesHttpRoute#meshes} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#project NetworkServicesHttpRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#timeouts NetworkServicesHttpRoute#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkServicesHttpRouteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c5203647b013b52b91161ef3d81f4f99f5d3f46c962926b7f4051645dd31bf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument hostnames", value=hostnames, expected_type=type_hints["hostnames"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument gateways", value=gateways, expected_type=type_hints["gateways"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument meshes", value=meshes, expected_type=type_hints["meshes"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hostnames": hostnames,
            "name": name,
            "rules": rules,
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
        if gateways is not None:
            self._values["gateways"] = gateways
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if meshes is not None:
            self._values["meshes"] = meshes
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
    def hostnames(self) -> typing.List[builtins.str]:
        '''Set of hosts that should match against the HTTP host header to select a HttpRoute to process the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#hostnames NetworkServicesHttpRoute#hostnames}
        '''
        result = self._values.get("hostnames")
        assert result is not None, "Required property 'hostnames' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the HttpRoute resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#name NetworkServicesHttpRoute#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#rules NetworkServicesHttpRoute#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRules"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#description NetworkServicesHttpRoute#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateways(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Gateways defines a list of gateways this HttpRoute is attached to, as one of the routing rules to route the requests served by the gateway.

        Each gateway reference should match the pattern: projects/* /locations/global/gateways/<gateway_name>

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#gateways NetworkServicesHttpRoute#gateways}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("gateways")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#id NetworkServicesHttpRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of label tags associated with the HttpRoute resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#labels NetworkServicesHttpRoute#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def meshes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Meshes defines a list of meshes this HttpRoute is attached to, as one of the routing rules to route the requests served by the mesh.

        Each mesh reference should match the pattern: projects/* /locations/global/meshes/<mesh_name>.
        The attached Mesh should be of a type SIDECAR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#meshes NetworkServicesHttpRoute#meshes}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("meshes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#project NetworkServicesHttpRoute#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkServicesHttpRouteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#timeouts NetworkServicesHttpRoute#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRules",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "matches": "matches"},
)
class NetworkServicesHttpRouteRules:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesAction", typing.Dict[builtins.str, typing.Any]]] = None,
        matches: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesHttpRouteRulesMatches", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#action NetworkServicesHttpRoute#action}
        :param matches: matches block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#matches NetworkServicesHttpRoute#matches}
        '''
        if isinstance(action, dict):
            action = NetworkServicesHttpRouteRulesAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf3aa0040e3cba738360de80c856e683a6417889b98109f3da225d251ddf9b7)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument matches", value=matches, expected_type=type_hints["matches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if matches is not None:
            self._values["matches"] = matches

    @builtins.property
    def action(self) -> typing.Optional["NetworkServicesHttpRouteRulesAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#action NetworkServicesHttpRoute#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesAction"], result)

    @builtins.property
    def matches(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesMatches"]]]:
        '''matches block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#matches NetworkServicesHttpRoute#matches}
        '''
        result = self._values.get("matches")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesMatches"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesAction",
    jsii_struct_bases=[],
    name_mapping={
        "cors_policy": "corsPolicy",
        "destinations": "destinations",
        "fault_injection_policy": "faultInjectionPolicy",
        "redirect": "redirect",
        "request_header_modifier": "requestHeaderModifier",
        "request_mirror_policy": "requestMirrorPolicy",
        "response_header_modifier": "responseHeaderModifier",
        "retry_policy": "retryPolicy",
        "timeout": "timeout",
        "url_rewrite": "urlRewrite",
    },
)
class NetworkServicesHttpRouteRulesAction:
    def __init__(
        self,
        *,
        cors_policy: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionCorsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesHttpRouteRulesActionDestinations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fault_injection_policy: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionFaultInjectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        request_header_modifier: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionRequestHeaderModifier", typing.Dict[builtins.str, typing.Any]]] = None,
        request_mirror_policy: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionRequestMirrorPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        response_header_modifier: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionResponseHeaderModifier", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[builtins.str] = None,
        url_rewrite: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cors_policy: cors_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#cors_policy NetworkServicesHttpRoute#cors_policy}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#destinations NetworkServicesHttpRoute#destinations}
        :param fault_injection_policy: fault_injection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#fault_injection_policy NetworkServicesHttpRoute#fault_injection_policy}
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#redirect NetworkServicesHttpRoute#redirect}
        :param request_header_modifier: request_header_modifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#request_header_modifier NetworkServicesHttpRoute#request_header_modifier}
        :param request_mirror_policy: request_mirror_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#request_mirror_policy NetworkServicesHttpRoute#request_mirror_policy}
        :param response_header_modifier: response_header_modifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#response_header_modifier NetworkServicesHttpRoute#response_header_modifier}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#retry_policy NetworkServicesHttpRoute#retry_policy}
        :param timeout: Specifies the timeout for selected route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#timeout NetworkServicesHttpRoute#timeout}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#url_rewrite NetworkServicesHttpRoute#url_rewrite}
        '''
        if isinstance(cors_policy, dict):
            cors_policy = NetworkServicesHttpRouteRulesActionCorsPolicy(**cors_policy)
        if isinstance(fault_injection_policy, dict):
            fault_injection_policy = NetworkServicesHttpRouteRulesActionFaultInjectionPolicy(**fault_injection_policy)
        if isinstance(redirect, dict):
            redirect = NetworkServicesHttpRouteRulesActionRedirect(**redirect)
        if isinstance(request_header_modifier, dict):
            request_header_modifier = NetworkServicesHttpRouteRulesActionRequestHeaderModifier(**request_header_modifier)
        if isinstance(request_mirror_policy, dict):
            request_mirror_policy = NetworkServicesHttpRouteRulesActionRequestMirrorPolicy(**request_mirror_policy)
        if isinstance(response_header_modifier, dict):
            response_header_modifier = NetworkServicesHttpRouteRulesActionResponseHeaderModifier(**response_header_modifier)
        if isinstance(retry_policy, dict):
            retry_policy = NetworkServicesHttpRouteRulesActionRetryPolicy(**retry_policy)
        if isinstance(url_rewrite, dict):
            url_rewrite = NetworkServicesHttpRouteRulesActionUrlRewrite(**url_rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8693db77520f6f22af82c8da15570290b37071807c648f1328b31aa3176b70)
            check_type(argname="argument cors_policy", value=cors_policy, expected_type=type_hints["cors_policy"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument fault_injection_policy", value=fault_injection_policy, expected_type=type_hints["fault_injection_policy"])
            check_type(argname="argument redirect", value=redirect, expected_type=type_hints["redirect"])
            check_type(argname="argument request_header_modifier", value=request_header_modifier, expected_type=type_hints["request_header_modifier"])
            check_type(argname="argument request_mirror_policy", value=request_mirror_policy, expected_type=type_hints["request_mirror_policy"])
            check_type(argname="argument response_header_modifier", value=response_header_modifier, expected_type=type_hints["response_header_modifier"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument url_rewrite", value=url_rewrite, expected_type=type_hints["url_rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cors_policy is not None:
            self._values["cors_policy"] = cors_policy
        if destinations is not None:
            self._values["destinations"] = destinations
        if fault_injection_policy is not None:
            self._values["fault_injection_policy"] = fault_injection_policy
        if redirect is not None:
            self._values["redirect"] = redirect
        if request_header_modifier is not None:
            self._values["request_header_modifier"] = request_header_modifier
        if request_mirror_policy is not None:
            self._values["request_mirror_policy"] = request_mirror_policy
        if response_header_modifier is not None:
            self._values["response_header_modifier"] = response_header_modifier
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if timeout is not None:
            self._values["timeout"] = timeout
        if url_rewrite is not None:
            self._values["url_rewrite"] = url_rewrite

    @builtins.property
    def cors_policy(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionCorsPolicy"]:
        '''cors_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#cors_policy NetworkServicesHttpRoute#cors_policy}
        '''
        result = self._values.get("cors_policy")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionCorsPolicy"], result)

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesActionDestinations"]]]:
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#destinations NetworkServicesHttpRoute#destinations}
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesActionDestinations"]]], result)

    @builtins.property
    def fault_injection_policy(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionFaultInjectionPolicy"]:
        '''fault_injection_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#fault_injection_policy NetworkServicesHttpRoute#fault_injection_policy}
        '''
        result = self._values.get("fault_injection_policy")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionFaultInjectionPolicy"], result)

    @builtins.property
    def redirect(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRedirect"]:
        '''redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#redirect NetworkServicesHttpRoute#redirect}
        '''
        result = self._values.get("redirect")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRedirect"], result)

    @builtins.property
    def request_header_modifier(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRequestHeaderModifier"]:
        '''request_header_modifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#request_header_modifier NetworkServicesHttpRoute#request_header_modifier}
        '''
        result = self._values.get("request_header_modifier")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRequestHeaderModifier"], result)

    @builtins.property
    def request_mirror_policy(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRequestMirrorPolicy"]:
        '''request_mirror_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#request_mirror_policy NetworkServicesHttpRoute#request_mirror_policy}
        '''
        result = self._values.get("request_mirror_policy")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRequestMirrorPolicy"], result)

    @builtins.property
    def response_header_modifier(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionResponseHeaderModifier"]:
        '''response_header_modifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#response_header_modifier NetworkServicesHttpRoute#response_header_modifier}
        '''
        result = self._values.get("response_header_modifier")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionResponseHeaderModifier"], result)

    @builtins.property
    def retry_policy(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#retry_policy NetworkServicesHttpRoute#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRetryPolicy"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Specifies the timeout for selected route.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#timeout NetworkServicesHttpRoute#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url_rewrite(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionUrlRewrite"]:
        '''url_rewrite block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#url_rewrite NetworkServicesHttpRoute#url_rewrite}
        '''
        result = self._values.get("url_rewrite")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionUrlRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionCorsPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "allow_credentials": "allowCredentials",
        "allow_headers": "allowHeaders",
        "allow_methods": "allowMethods",
        "allow_origin_regexes": "allowOriginRegexes",
        "allow_origins": "allowOrigins",
        "disabled": "disabled",
        "expose_headers": "exposeHeaders",
        "max_age": "maxAge",
    },
)
class NetworkServicesHttpRouteRulesActionCorsPolicy:
    def __init__(
        self,
        *,
        allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_origin_regexes: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_credentials: In response to a preflight request, setting this to true indicates that the actual request can include user credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_credentials NetworkServicesHttpRoute#allow_credentials}
        :param allow_headers: Specifies the content for Access-Control-Allow-Headers header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_headers NetworkServicesHttpRoute#allow_headers}
        :param allow_methods: Specifies the content for Access-Control-Allow-Methods header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_methods NetworkServicesHttpRoute#allow_methods}
        :param allow_origin_regexes: Specifies the regular expression patterns that match allowed origins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_origin_regexes NetworkServicesHttpRoute#allow_origin_regexes}
        :param allow_origins: Specifies the list of origins that will be allowed to do CORS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_origins NetworkServicesHttpRoute#allow_origins}
        :param disabled: If true, the CORS policy is disabled. The default value is false, which indicates that the CORS policy is in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#disabled NetworkServicesHttpRoute#disabled}
        :param expose_headers: Specifies the content for Access-Control-Expose-Headers header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#expose_headers NetworkServicesHttpRoute#expose_headers}
        :param max_age: Specifies how long result of a preflight request can be cached in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#max_age NetworkServicesHttpRoute#max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06fdce8f8c4375deb682a11d8f3edd18b8a4fec4f1d91886409c28fb7b0e4896)
            check_type(argname="argument allow_credentials", value=allow_credentials, expected_type=type_hints["allow_credentials"])
            check_type(argname="argument allow_headers", value=allow_headers, expected_type=type_hints["allow_headers"])
            check_type(argname="argument allow_methods", value=allow_methods, expected_type=type_hints["allow_methods"])
            check_type(argname="argument allow_origin_regexes", value=allow_origin_regexes, expected_type=type_hints["allow_origin_regexes"])
            check_type(argname="argument allow_origins", value=allow_origins, expected_type=type_hints["allow_origins"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument expose_headers", value=expose_headers, expected_type=type_hints["expose_headers"])
            check_type(argname="argument max_age", value=max_age, expected_type=type_hints["max_age"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_credentials is not None:
            self._values["allow_credentials"] = allow_credentials
        if allow_headers is not None:
            self._values["allow_headers"] = allow_headers
        if allow_methods is not None:
            self._values["allow_methods"] = allow_methods
        if allow_origin_regexes is not None:
            self._values["allow_origin_regexes"] = allow_origin_regexes
        if allow_origins is not None:
            self._values["allow_origins"] = allow_origins
        if disabled is not None:
            self._values["disabled"] = disabled
        if expose_headers is not None:
            self._values["expose_headers"] = expose_headers
        if max_age is not None:
            self._values["max_age"] = max_age

    @builtins.property
    def allow_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''In response to a preflight request, setting this to true indicates that the actual request can include user credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_credentials NetworkServicesHttpRoute#allow_credentials}
        '''
        result = self._values.get("allow_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for Access-Control-Allow-Headers header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_headers NetworkServicesHttpRoute#allow_headers}
        '''
        result = self._values.get("allow_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for Access-Control-Allow-Methods header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_methods NetworkServicesHttpRoute#allow_methods}
        '''
        result = self._values.get("allow_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_origin_regexes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the regular expression patterns that match allowed origins.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_origin_regexes NetworkServicesHttpRoute#allow_origin_regexes}
        '''
        result = self._values.get("allow_origin_regexes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of origins that will be allowed to do CORS requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_origins NetworkServicesHttpRoute#allow_origins}
        '''
        result = self._values.get("allow_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the CORS policy is disabled.

        The default value is false, which indicates that the CORS policy is in effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#disabled NetworkServicesHttpRoute#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for Access-Control-Expose-Headers header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#expose_headers NetworkServicesHttpRoute#expose_headers}
        '''
        result = self._values.get("expose_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age(self) -> typing.Optional[builtins.str]:
        '''Specifies how long result of a preflight request can be cached in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#max_age NetworkServicesHttpRoute#max_age}
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionCorsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionCorsPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionCorsPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e0501a505a9f2a7d213bc60ad891657eb44ab5728e04e8a934e393fd4830ec7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowCredentials")
    def reset_allow_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowCredentials", []))

    @jsii.member(jsii_name="resetAllowHeaders")
    def reset_allow_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowHeaders", []))

    @jsii.member(jsii_name="resetAllowMethods")
    def reset_allow_methods(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowMethods", []))

    @jsii.member(jsii_name="resetAllowOriginRegexes")
    def reset_allow_origin_regexes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowOriginRegexes", []))

    @jsii.member(jsii_name="resetAllowOrigins")
    def reset_allow_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowOrigins", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetExposeHeaders")
    def reset_expose_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExposeHeaders", []))

    @jsii.member(jsii_name="resetMaxAge")
    def reset_max_age(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxAge", []))

    @builtins.property
    @jsii.member(jsii_name="allowCredentialsInput")
    def allow_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowHeadersInput")
    def allow_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowMethodsInput")
    def allow_methods_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowMethodsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOriginRegexesInput")
    def allow_origin_regexes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowOriginRegexesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowOriginsInput")
    def allow_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="exposeHeadersInput")
    def expose_headers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "exposeHeadersInput"))

    @builtins.property
    @jsii.member(jsii_name="maxAgeInput")
    def max_age_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxAgeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowCredentials")
    def allow_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowCredentials"))

    @allow_credentials.setter
    def allow_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37835fcbbbfb54f492f93962128b802e8166291c387d2b521bf097f5b7ed0ffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowHeaders")
    def allow_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowHeaders"))

    @allow_headers.setter
    def allow_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8820e0e21f94266c2bafe1ed6bb522e94d89bbb4712a957f4563ec9a0ea64be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowMethods")
    def allow_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowMethods"))

    @allow_methods.setter
    def allow_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e9086d7f7f331a8e6b88745e639682213d921c54723f7783eb73b03b71bb832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowOriginRegexes")
    def allow_origin_regexes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowOriginRegexes"))

    @allow_origin_regexes.setter
    def allow_origin_regexes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f847979f6a8fdea170d8b6b8413013aadb55d5e2c98a6528e519ba453c32b038)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOriginRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowOrigins")
    def allow_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowOrigins"))

    @allow_origins.setter
    def allow_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b4c3822b0dc3709d8ea6c102929b0bcc0233c2837952f9104df7443865fadf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOrigins", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__29ff6495c2a68b27233a3f3dcd65936b057bc139a6b61faccae716b9c46ebc4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposeHeaders")
    def expose_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposeHeaders"))

    @expose_headers.setter
    def expose_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ede1fcc7b80fe43c51b3d0a22f40423723f7a27565c913f7e6974d3e5328cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposeHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498ce007001580289c50f66fef171fada57a76451de426a4a40e99b8b92b7000)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionCorsPolicy]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionCorsPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionCorsPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f9effef0935e0af4f12b710a5dfc5d9e286b8c2dc37b81111849d474e4d3f58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionDestinations",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "weight": "weight"},
)
class NetworkServicesHttpRouteRulesActionDestinations:
    def __init__(
        self,
        *,
        service_name: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_name: The URL of a BackendService to route traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#service_name NetworkServicesHttpRoute#service_name}
        :param weight: Specifies the proportion of requests forwarded to the backend referenced by the serviceName field. This is computed as: weight/Sum(weights in this destination list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports. If only one serviceName is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend. If weights are specified for any one service name, they need to be specified for all of them. If weights are unspecified for all services, then, traffic is distributed in equal proportions to all of them. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#weight NetworkServicesHttpRoute#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8ef1d9793a185a106d53ba74ae2bab8ed59267fa00cacead113670b88d1e16)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_name is not None:
            self._values["service_name"] = service_name
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The URL of a BackendService to route traffic to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#service_name NetworkServicesHttpRoute#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Specifies the proportion of requests forwarded to the backend referenced by the serviceName field.

        This is computed as: weight/Sum(weights in this destination list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports.
        If only one serviceName is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend.
        If weights are specified for any one service name, they need to be specified for all of them.
        If weights are unspecified for all services, then, traffic is distributed in equal proportions to all of them.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#weight NetworkServicesHttpRoute#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionDestinationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionDestinationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ee725c4df4fe49eb5390b4cedb107fcb6674ed1973b5df3b420cf9768188fd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesHttpRouteRulesActionDestinationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6257e6151910f88c17b882536a11d0b124dd6dbfadc5ea190a4a8fe4e4a116a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesHttpRouteRulesActionDestinationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530ef3b5cacc314727860d597a9e6de357771015b5172001072972ffd9a6e35e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5dd664b01e57f060732c5bf8fd62e45aab514d6b9ccbc98f7cfd27ad35af1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3aadaef4421ecb539c4b596fc3b37d0bbc0fd8e7397c473516a206635aeeb3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesActionDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesActionDestinations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesActionDestinations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e15fa7179bbe2467b35ce4065c823b56535ee7601d8221cbadf37bc227a8bb0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesActionDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41cb7167779be68ae5d4d9b3294202789f7ebaf4f93d4c4bd8ac48a87fbe8746)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6eb81c950257dae0a90e73cb5fb5bac7ccc56d45ebc074c5bc64200e717ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9303a0622d6230b664a98fb8521e7b4e6232ba7866f1855f8d270b8ea42599de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesActionDestinations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesActionDestinations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesActionDestinations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2dd5956464ae67fd1d05eea90a7cd48d34382bea735a6c276942a0fa5d7f56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionFaultInjectionPolicy",
    jsii_struct_bases=[],
    name_mapping={"abort": "abort", "delay": "delay"},
)
class NetworkServicesHttpRouteRulesActionFaultInjectionPolicy:
    def __init__(
        self,
        *,
        abort: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort", typing.Dict[builtins.str, typing.Any]]] = None,
        delay: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param abort: abort block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#abort NetworkServicesHttpRoute#abort}
        :param delay: delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#delay NetworkServicesHttpRoute#delay}
        '''
        if isinstance(abort, dict):
            abort = NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort(**abort)
        if isinstance(delay, dict):
            delay = NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay(**delay)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce742f624af3eeff5eb23df147c60f4d94468bc28a1dfc709b3d70a5472b0b9)
            check_type(argname="argument abort", value=abort, expected_type=type_hints["abort"])
            check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if abort is not None:
            self._values["abort"] = abort
        if delay is not None:
            self._values["delay"] = delay

    @builtins.property
    def abort(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort"]:
        '''abort block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#abort NetworkServicesHttpRoute#abort}
        '''
        result = self._values.get("abort")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort"], result)

    @builtins.property
    def delay(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay"]:
        '''delay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#delay NetworkServicesHttpRoute#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionFaultInjectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort",
    jsii_struct_bases=[],
    name_mapping={"http_status": "httpStatus", "percentage": "percentage"},
)
class NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort:
    def __init__(
        self,
        *,
        http_status: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_status: The HTTP status code used to abort the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#http_status NetworkServicesHttpRoute#http_status}
        :param percentage: The percentage of traffic which will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#percentage NetworkServicesHttpRoute#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9704a5da7d239ad40f5b82d9a9c148982378263a964da5906e7d273c3b603578)
            check_type(argname="argument http_status", value=http_status, expected_type=type_hints["http_status"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if http_status is not None:
            self._values["http_status"] = http_status
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def http_status(self) -> typing.Optional[jsii.Number]:
        '''The HTTP status code used to abort the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#http_status NetworkServicesHttpRoute#http_status}
        '''
        result = self._values.get("http_status")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic which will be aborted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#percentage NetworkServicesHttpRoute#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__056dffdafec34a8554d9e54c379f373ad2cd43ed1d6d88fd5ac72d0fbbc15c32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHttpStatus")
    def reset_http_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpStatus", []))

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="httpStatusInput")
    def http_status_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "httpStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="httpStatus")
    def http_status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "httpStatus"))

    @http_status.setter
    def http_status(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463214f835baff323385a3d3e46473a28aab34d3b2d259d72886f6c87ecf9aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73335e521eae08ccc61ae0614f760a9f33771335955a944689a6385795e8a3b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c09f9ad121da4dd7247724b0455028d0161d9c4a526c7976a986638124b738b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay",
    jsii_struct_bases=[],
    name_mapping={"fixed_delay": "fixedDelay", "percentage": "percentage"},
)
class NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay:
    def __init__(
        self,
        *,
        fixed_delay: typing.Optional[builtins.str] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_delay: Specify a fixed delay before forwarding the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#fixed_delay NetworkServicesHttpRoute#fixed_delay}
        :param percentage: The percentage of traffic on which delay will be injected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#percentage NetworkServicesHttpRoute#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0cbe3bdc0145e3c8fce616cbc15ccd12ad35d61976c6b3de504a05e13495520)
            check_type(argname="argument fixed_delay", value=fixed_delay, expected_type=type_hints["fixed_delay"])
            check_type(argname="argument percentage", value=percentage, expected_type=type_hints["percentage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed_delay is not None:
            self._values["fixed_delay"] = fixed_delay
        if percentage is not None:
            self._values["percentage"] = percentage

    @builtins.property
    def fixed_delay(self) -> typing.Optional[builtins.str]:
        '''Specify a fixed delay before forwarding the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#fixed_delay NetworkServicesHttpRoute#fixed_delay}
        '''
        result = self._values.get("fixed_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic on which delay will be injected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#percentage NetworkServicesHttpRoute#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5feb1aa7a90a45e3ede671db6623cceb45d0d4570edd2449c126ee60553c456e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFixedDelay")
    def reset_fixed_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedDelay", []))

    @jsii.member(jsii_name="resetPercentage")
    def reset_percentage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercentage", []))

    @builtins.property
    @jsii.member(jsii_name="fixedDelayInput")
    def fixed_delay_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedDelayInput"))

    @builtins.property
    @jsii.member(jsii_name="percentageInput")
    def percentage_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentageInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedDelay")
    def fixed_delay(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedDelay"))

    @fixed_delay.setter
    def fixed_delay(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de08ff99a9d6db7c685e70cf91329fc2744c60586946f0c7863f6553bde8a2b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38aa0b71e73efb15b1ed8c1b636674e4847dfc86f0a0dcf6790e9a9df0758abd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a96d998b9e52e0e843d1c1dca373615d6e522a17f760a68a361d769694f640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7626c96ec3c315324778986ef4424f672ac304e1fb6e3653c163fdcfce820a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAbort")
    def put_abort(
        self,
        *,
        http_status: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_status: The HTTP status code used to abort the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#http_status NetworkServicesHttpRoute#http_status}
        :param percentage: The percentage of traffic which will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#percentage NetworkServicesHttpRoute#percentage}
        '''
        value = NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort(
            http_status=http_status, percentage=percentage
        )

        return typing.cast(None, jsii.invoke(self, "putAbort", [value]))

    @jsii.member(jsii_name="putDelay")
    def put_delay(
        self,
        *,
        fixed_delay: typing.Optional[builtins.str] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_delay: Specify a fixed delay before forwarding the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#fixed_delay NetworkServicesHttpRoute#fixed_delay}
        :param percentage: The percentage of traffic on which delay will be injected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#percentage NetworkServicesHttpRoute#percentage}
        '''
        value = NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay(
            fixed_delay=fixed_delay, percentage=percentage
        )

        return typing.cast(None, jsii.invoke(self, "putDelay", [value]))

    @jsii.member(jsii_name="resetAbort")
    def reset_abort(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAbort", []))

    @jsii.member(jsii_name="resetDelay")
    def reset_delay(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelay", []))

    @builtins.property
    @jsii.member(jsii_name="abort")
    def abort(
        self,
    ) -> NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference:
        return typing.cast(NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference, jsii.get(self, "abort"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(
        self,
    ) -> NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference:
        return typing.cast(NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference, jsii.get(self, "delay"))

    @builtins.property
    @jsii.member(jsii_name="abortInput")
    def abort_input(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort], jsii.get(self, "abortInput"))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicy]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ede56f97248fce4156aed4169367aa93b73d94ad8b9b086c6b0480cfd3e467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1161383f720b818f38ab513e0c09dd7b2603e6d529e804229ac9872d2d8e658)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCorsPolicy")
    def put_cors_policy(
        self,
        *,
        allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_origin_regexes: typing.Optional[typing.Sequence[builtins.str]] = None,
        allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_age: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_credentials: In response to a preflight request, setting this to true indicates that the actual request can include user credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_credentials NetworkServicesHttpRoute#allow_credentials}
        :param allow_headers: Specifies the content for Access-Control-Allow-Headers header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_headers NetworkServicesHttpRoute#allow_headers}
        :param allow_methods: Specifies the content for Access-Control-Allow-Methods header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_methods NetworkServicesHttpRoute#allow_methods}
        :param allow_origin_regexes: Specifies the regular expression patterns that match allowed origins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_origin_regexes NetworkServicesHttpRoute#allow_origin_regexes}
        :param allow_origins: Specifies the list of origins that will be allowed to do CORS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#allow_origins NetworkServicesHttpRoute#allow_origins}
        :param disabled: If true, the CORS policy is disabled. The default value is false, which indicates that the CORS policy is in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#disabled NetworkServicesHttpRoute#disabled}
        :param expose_headers: Specifies the content for Access-Control-Expose-Headers header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#expose_headers NetworkServicesHttpRoute#expose_headers}
        :param max_age: Specifies how long result of a preflight request can be cached in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#max_age NetworkServicesHttpRoute#max_age}
        '''
        value = NetworkServicesHttpRouteRulesActionCorsPolicy(
            allow_credentials=allow_credentials,
            allow_headers=allow_headers,
            allow_methods=allow_methods,
            allow_origin_regexes=allow_origin_regexes,
            allow_origins=allow_origins,
            disabled=disabled,
            expose_headers=expose_headers,
            max_age=max_age,
        )

        return typing.cast(None, jsii.invoke(self, "putCorsPolicy", [value]))

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6da0e4317937299a8e394cc2ab92f67dce39db08ebfc4ce6643591ef05c5d363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putFaultInjectionPolicy")
    def put_fault_injection_policy(
        self,
        *,
        abort: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort, typing.Dict[builtins.str, typing.Any]]] = None,
        delay: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param abort: abort block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#abort NetworkServicesHttpRoute#abort}
        :param delay: delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#delay NetworkServicesHttpRoute#delay}
        '''
        value = NetworkServicesHttpRouteRulesActionFaultInjectionPolicy(
            abort=abort, delay=delay
        )

        return typing.cast(None, jsii.invoke(self, "putFaultInjectionPolicy", [value]))

    @jsii.member(jsii_name="putRedirect")
    def put_redirect(
        self,
        *,
        host_redirect: typing.Optional[builtins.str] = None,
        https_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path_redirect: typing.Optional[builtins.str] = None,
        port_redirect: typing.Optional[jsii.Number] = None,
        prefix_rewrite: typing.Optional[builtins.str] = None,
        response_code: typing.Optional[builtins.str] = None,
        strip_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param host_redirect: The host that will be used in the redirect response instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#host_redirect NetworkServicesHttpRoute#host_redirect}
        :param https_redirect: If set to true, the URL scheme in the redirected request is set to https. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#https_redirect NetworkServicesHttpRoute#https_redirect}
        :param path_redirect: The path that will be used in the redirect response instead of the one that was supplied in the request. pathRedirect can not be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#path_redirect NetworkServicesHttpRoute#path_redirect}
        :param port_redirect: The port that will be used in the redirected request instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#port_redirect NetworkServicesHttpRoute#port_redirect}
        :param prefix_rewrite: Indicates that during redirection, the matched prefix (or path) should be swapped with this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#prefix_rewrite NetworkServicesHttpRoute#prefix_rewrite}
        :param response_code: The HTTP Status code to use for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#response_code NetworkServicesHttpRoute#response_code}
        :param strip_query: If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#strip_query NetworkServicesHttpRoute#strip_query}
        '''
        value = NetworkServicesHttpRouteRulesActionRedirect(
            host_redirect=host_redirect,
            https_redirect=https_redirect,
            path_redirect=path_redirect,
            port_redirect=port_redirect,
            prefix_rewrite=prefix_rewrite,
            response_code=response_code,
            strip_query=strip_query,
        )

        return typing.cast(None, jsii.invoke(self, "putRedirect", [value]))

    @jsii.member(jsii_name="putRequestHeaderModifier")
    def put_request_header_modifier(
        self,
        *,
        add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param add: Add the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#add NetworkServicesHttpRoute#add}
        :param remove: Remove headers (matching by header names) specified in the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#remove NetworkServicesHttpRoute#remove}
        :param set: Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#set NetworkServicesHttpRoute#set}
        '''
        value = NetworkServicesHttpRouteRulesActionRequestHeaderModifier(
            add=add, remove=remove, set=set
        )

        return typing.cast(None, jsii.invoke(self, "putRequestHeaderModifier", [value]))

    @jsii.member(jsii_name="putRequestMirrorPolicy")
    def put_request_mirror_policy(
        self,
        *,
        destination: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#destination NetworkServicesHttpRoute#destination}
        '''
        value = NetworkServicesHttpRouteRulesActionRequestMirrorPolicy(
            destination=destination
        )

        return typing.cast(None, jsii.invoke(self, "putRequestMirrorPolicy", [value]))

    @jsii.member(jsii_name="putResponseHeaderModifier")
    def put_response_header_modifier(
        self,
        *,
        add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param add: Add the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#add NetworkServicesHttpRoute#add}
        :param remove: Remove headers (matching by header names) specified in the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#remove NetworkServicesHttpRoute#remove}
        :param set: Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#set NetworkServicesHttpRoute#set}
        '''
        value = NetworkServicesHttpRouteRulesActionResponseHeaderModifier(
            add=add, remove=remove, set=set
        )

        return typing.cast(None, jsii.invoke(self, "putResponseHeaderModifier", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        num_retries: typing.Optional[jsii.Number] = None,
        per_try_timeout: typing.Optional[builtins.str] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param num_retries: Specifies the allowed number of retries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#num_retries NetworkServicesHttpRoute#num_retries}
        :param per_try_timeout: Specifies a non-zero timeout per retry attempt. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#per_try_timeout NetworkServicesHttpRoute#per_try_timeout}
        :param retry_conditions: Specifies one or more conditions when this retry policy applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#retry_conditions NetworkServicesHttpRoute#retry_conditions}
        '''
        value = NetworkServicesHttpRouteRulesActionRetryPolicy(
            num_retries=num_retries,
            per_try_timeout=per_try_timeout,
            retry_conditions=retry_conditions,
        )

        return typing.cast(None, jsii.invoke(self, "putRetryPolicy", [value]))

    @jsii.member(jsii_name="putUrlRewrite")
    def put_url_rewrite(
        self,
        *,
        host_rewrite: typing.Optional[builtins.str] = None,
        path_prefix_rewrite: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected destination, the requests host header is replaced by this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#host_rewrite NetworkServicesHttpRoute#host_rewrite}
        :param path_prefix_rewrite: Prior to forwarding the request to the selected destination, the matching portion of the requests path is replaced by this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#path_prefix_rewrite NetworkServicesHttpRoute#path_prefix_rewrite}
        '''
        value = NetworkServicesHttpRouteRulesActionUrlRewrite(
            host_rewrite=host_rewrite, path_prefix_rewrite=path_prefix_rewrite
        )

        return typing.cast(None, jsii.invoke(self, "putUrlRewrite", [value]))

    @jsii.member(jsii_name="resetCorsPolicy")
    def reset_cors_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCorsPolicy", []))

    @jsii.member(jsii_name="resetDestinations")
    def reset_destinations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinations", []))

    @jsii.member(jsii_name="resetFaultInjectionPolicy")
    def reset_fault_injection_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaultInjectionPolicy", []))

    @jsii.member(jsii_name="resetRedirect")
    def reset_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirect", []))

    @jsii.member(jsii_name="resetRequestHeaderModifier")
    def reset_request_header_modifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestHeaderModifier", []))

    @jsii.member(jsii_name="resetRequestMirrorPolicy")
    def reset_request_mirror_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequestMirrorPolicy", []))

    @jsii.member(jsii_name="resetResponseHeaderModifier")
    def reset_response_header_modifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseHeaderModifier", []))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetUrlRewrite")
    def reset_url_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrlRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="corsPolicy")
    def cors_policy(
        self,
    ) -> NetworkServicesHttpRouteRulesActionCorsPolicyOutputReference:
        return typing.cast(NetworkServicesHttpRouteRulesActionCorsPolicyOutputReference, jsii.get(self, "corsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> NetworkServicesHttpRouteRulesActionDestinationsList:
        return typing.cast(NetworkServicesHttpRouteRulesActionDestinationsList, jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="faultInjectionPolicy")
    def fault_injection_policy(
        self,
    ) -> NetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference:
        return typing.cast(NetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference, jsii.get(self, "faultInjectionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="redirect")
    def redirect(self) -> "NetworkServicesHttpRouteRulesActionRedirectOutputReference":
        return typing.cast("NetworkServicesHttpRouteRulesActionRedirectOutputReference", jsii.get(self, "redirect"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderModifier")
    def request_header_modifier(
        self,
    ) -> "NetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference":
        return typing.cast("NetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference", jsii.get(self, "requestHeaderModifier"))

    @builtins.property
    @jsii.member(jsii_name="requestMirrorPolicy")
    def request_mirror_policy(
        self,
    ) -> "NetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference":
        return typing.cast("NetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference", jsii.get(self, "requestMirrorPolicy"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderModifier")
    def response_header_modifier(
        self,
    ) -> "NetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference":
        return typing.cast("NetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference", jsii.get(self, "responseHeaderModifier"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(
        self,
    ) -> "NetworkServicesHttpRouteRulesActionRetryPolicyOutputReference":
        return typing.cast("NetworkServicesHttpRouteRulesActionRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="urlRewrite")
    def url_rewrite(
        self,
    ) -> "NetworkServicesHttpRouteRulesActionUrlRewriteOutputReference":
        return typing.cast("NetworkServicesHttpRouteRulesActionUrlRewriteOutputReference", jsii.get(self, "urlRewrite"))

    @builtins.property
    @jsii.member(jsii_name="corsPolicyInput")
    def cors_policy_input(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionCorsPolicy]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionCorsPolicy], jsii.get(self, "corsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesActionDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesActionDestinations]]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="faultInjectionPolicyInput")
    def fault_injection_policy_input(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicy]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicy], jsii.get(self, "faultInjectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectInput")
    def redirect_input(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRedirect"]:
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRedirect"], jsii.get(self, "redirectInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderModifierInput")
    def request_header_modifier_input(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRequestHeaderModifier"]:
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRequestHeaderModifier"], jsii.get(self, "requestHeaderModifierInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMirrorPolicyInput")
    def request_mirror_policy_input(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRequestMirrorPolicy"]:
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRequestMirrorPolicy"], jsii.get(self, "requestMirrorPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderModifierInput")
    def response_header_modifier_input(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionResponseHeaderModifier"]:
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionResponseHeaderModifier"], jsii.get(self, "responseHeaderModifierInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRetryPolicy"]:
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteInput")
    def url_rewrite_input(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionUrlRewrite"]:
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionUrlRewrite"], jsii.get(self, "urlRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d44b1051cb2cb98b2e917cdea8df9506f8a8a0903efd12221bededc76585995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkServicesHttpRouteRulesAction]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__266425d180373d188ca497499982945f416a2ef991abc43f5645944ace886030)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRedirect",
    jsii_struct_bases=[],
    name_mapping={
        "host_redirect": "hostRedirect",
        "https_redirect": "httpsRedirect",
        "path_redirect": "pathRedirect",
        "port_redirect": "portRedirect",
        "prefix_rewrite": "prefixRewrite",
        "response_code": "responseCode",
        "strip_query": "stripQuery",
    },
)
class NetworkServicesHttpRouteRulesActionRedirect:
    def __init__(
        self,
        *,
        host_redirect: typing.Optional[builtins.str] = None,
        https_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        path_redirect: typing.Optional[builtins.str] = None,
        port_redirect: typing.Optional[jsii.Number] = None,
        prefix_rewrite: typing.Optional[builtins.str] = None,
        response_code: typing.Optional[builtins.str] = None,
        strip_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param host_redirect: The host that will be used in the redirect response instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#host_redirect NetworkServicesHttpRoute#host_redirect}
        :param https_redirect: If set to true, the URL scheme in the redirected request is set to https. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#https_redirect NetworkServicesHttpRoute#https_redirect}
        :param path_redirect: The path that will be used in the redirect response instead of the one that was supplied in the request. pathRedirect can not be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#path_redirect NetworkServicesHttpRoute#path_redirect}
        :param port_redirect: The port that will be used in the redirected request instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#port_redirect NetworkServicesHttpRoute#port_redirect}
        :param prefix_rewrite: Indicates that during redirection, the matched prefix (or path) should be swapped with this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#prefix_rewrite NetworkServicesHttpRoute#prefix_rewrite}
        :param response_code: The HTTP Status code to use for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#response_code NetworkServicesHttpRoute#response_code}
        :param strip_query: If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#strip_query NetworkServicesHttpRoute#strip_query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd113a5e934c7621fc29022236f0c4556d9fb4e7fe6e40b027aa64abb08ebd25)
            check_type(argname="argument host_redirect", value=host_redirect, expected_type=type_hints["host_redirect"])
            check_type(argname="argument https_redirect", value=https_redirect, expected_type=type_hints["https_redirect"])
            check_type(argname="argument path_redirect", value=path_redirect, expected_type=type_hints["path_redirect"])
            check_type(argname="argument port_redirect", value=port_redirect, expected_type=type_hints["port_redirect"])
            check_type(argname="argument prefix_rewrite", value=prefix_rewrite, expected_type=type_hints["prefix_rewrite"])
            check_type(argname="argument response_code", value=response_code, expected_type=type_hints["response_code"])
            check_type(argname="argument strip_query", value=strip_query, expected_type=type_hints["strip_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_redirect is not None:
            self._values["host_redirect"] = host_redirect
        if https_redirect is not None:
            self._values["https_redirect"] = https_redirect
        if path_redirect is not None:
            self._values["path_redirect"] = path_redirect
        if port_redirect is not None:
            self._values["port_redirect"] = port_redirect
        if prefix_rewrite is not None:
            self._values["prefix_rewrite"] = prefix_rewrite
        if response_code is not None:
            self._values["response_code"] = response_code
        if strip_query is not None:
            self._values["strip_query"] = strip_query

    @builtins.property
    def host_redirect(self) -> typing.Optional[builtins.str]:
        '''The host that will be used in the redirect response instead of the one that was supplied in the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#host_redirect NetworkServicesHttpRoute#host_redirect}
        '''
        result = self._values.get("host_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_redirect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the URL scheme in the redirected request is set to https.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#https_redirect NetworkServicesHttpRoute#https_redirect}
        '''
        result = self._values.get("https_redirect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path_redirect(self) -> typing.Optional[builtins.str]:
        '''The path that will be used in the redirect response instead of the one that was supplied in the request.

        pathRedirect can not be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#path_redirect NetworkServicesHttpRoute#path_redirect}
        '''
        result = self._values.get("path_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_redirect(self) -> typing.Optional[jsii.Number]:
        '''The port that will be used in the redirected request instead of the one that was supplied in the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#port_redirect NetworkServicesHttpRoute#port_redirect}
        '''
        result = self._values.get("port_redirect")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefix_rewrite(self) -> typing.Optional[builtins.str]:
        '''Indicates that during redirection, the matched prefix (or path) should be swapped with this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#prefix_rewrite NetworkServicesHttpRoute#prefix_rewrite}
        '''
        result = self._values.get("prefix_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_code(self) -> typing.Optional[builtins.str]:
        '''The HTTP Status code to use for the redirect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#response_code NetworkServicesHttpRoute#response_code}
        '''
        result = self._values.get("response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strip_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#strip_query NetworkServicesHttpRoute#strip_query}
        '''
        result = self._values.get("strip_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b985ddf8a36f90189a29b8776b0b94c7700bf72cf64c7ab88b41851c0ac3d3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostRedirect")
    def reset_host_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostRedirect", []))

    @jsii.member(jsii_name="resetHttpsRedirect")
    def reset_https_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsRedirect", []))

    @jsii.member(jsii_name="resetPathRedirect")
    def reset_path_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathRedirect", []))

    @jsii.member(jsii_name="resetPortRedirect")
    def reset_port_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortRedirect", []))

    @jsii.member(jsii_name="resetPrefixRewrite")
    def reset_prefix_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixRewrite", []))

    @jsii.member(jsii_name="resetResponseCode")
    def reset_response_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponseCode", []))

    @jsii.member(jsii_name="resetStripQuery")
    def reset_strip_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStripQuery", []))

    @builtins.property
    @jsii.member(jsii_name="hostRedirectInput")
    def host_redirect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsRedirectInput")
    def https_redirect_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpsRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="pathRedirectInput")
    def path_redirect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="portRedirectInput")
    def port_redirect_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portRedirectInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixRewriteInput")
    def prefix_rewrite_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="responseCodeInput")
    def response_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="stripQueryInput")
    def strip_query_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "stripQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="hostRedirect")
    def host_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostRedirect"))

    @host_redirect.setter
    def host_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a956b51be54de3860e34dc3aa400951d14fce8593de08530b6f067d3f4f3ba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsRedirect")
    def https_redirect(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpsRedirect"))

    @https_redirect.setter
    def https_redirect(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4f681652b20fc9535dda62530081ec9a13f5f498cde89d373ca45017b5f992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathRedirect")
    def path_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathRedirect"))

    @path_redirect.setter
    def path_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7b177f463a4becf3fce745c6147119900da94177f8997827d07e0c753138ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portRedirect")
    def port_redirect(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portRedirect"))

    @port_redirect.setter
    def port_redirect(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ba26e5df32c5b23a90ebf10d077a77118d7a8def81ddfdcf5ba5e1172cec5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixRewrite")
    def prefix_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixRewrite"))

    @prefix_rewrite.setter
    def prefix_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a98faadae2bb542c396c5193f7c8aacf2845096d5d98c0a3e1bfbfac49a9a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCode")
    def response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCode"))

    @response_code.setter
    def response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f885a36d5e7a02646515ee4f71144b533daca5158b39b01c6422f2350cdbd723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="stripQuery")
    def strip_query(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "stripQuery"))

    @strip_query.setter
    def strip_query(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d14bf263238ca394ccff426c1d508596fc982919a79404e71d987fd95d244f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionRedirect]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f03a8b7aee5222eb1da317d117e39d328985f19b74db30781ec6e5a10d084f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRequestHeaderModifier",
    jsii_struct_bases=[],
    name_mapping={"add": "add", "remove": "remove", "set": "set"},
)
class NetworkServicesHttpRouteRulesActionRequestHeaderModifier:
    def __init__(
        self,
        *,
        add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param add: Add the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#add NetworkServicesHttpRoute#add}
        :param remove: Remove headers (matching by header names) specified in the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#remove NetworkServicesHttpRoute#remove}
        :param set: Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#set NetworkServicesHttpRoute#set}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9bbfe849a60ef0ed5ea8e9eb2ee18b0878138c8826ce4f98d8f302d2707348)
            check_type(argname="argument add", value=add, expected_type=type_hints["add"])
            check_type(argname="argument remove", value=remove, expected_type=type_hints["remove"])
            check_type(argname="argument set", value=set, expected_type=type_hints["set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add is not None:
            self._values["add"] = add
        if remove is not None:
            self._values["remove"] = remove
        if set is not None:
            self._values["set"] = set

    @builtins.property
    def add(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Add the headers with given map where key is the name of the header, value is the value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#add NetworkServicesHttpRoute#add}
        '''
        result = self._values.get("add")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def remove(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Remove headers (matching by header names) specified in the list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#remove NetworkServicesHttpRoute#remove}
        '''
        result = self._values.get("remove")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def set(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#set NetworkServicesHttpRoute#set}
        '''
        result = self._values.get("set")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionRequestHeaderModifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aa6350c2ae1dc2a4da5a08995a7f8601ec75c085fb03c7df80a629ee80b6ed2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdd")
    def reset_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdd", []))

    @jsii.member(jsii_name="resetRemove")
    def reset_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemove", []))

    @jsii.member(jsii_name="resetSet")
    def reset_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSet", []))

    @builtins.property
    @jsii.member(jsii_name="addInput")
    def add_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "addInput"))

    @builtins.property
    @jsii.member(jsii_name="removeInput")
    def remove_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "removeInput"))

    @builtins.property
    @jsii.member(jsii_name="setInput")
    def set_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="add")
    def add(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "add"))

    @add.setter
    def add(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815ed6bdbe732eeed8b2d78db893c3c81aa579988c06467a7539ee798b3c9083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "add", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remove")
    def remove(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remove"))

    @remove.setter
    def remove(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b81f9110ffd698e824b492e66b182652b74c1c579caaee0663577b307b73e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remove", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "set"))

    @set.setter
    def set(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8441e61a052dba9cf79410c1559cba90648f240894e915536b198f536cef6225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "set", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionRequestHeaderModifier]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionRequestHeaderModifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionRequestHeaderModifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe3a79a3e988839345571cab4018ec31310182d2458933b1a790147176d2ee6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRequestMirrorPolicy",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class NetworkServicesHttpRouteRulesActionRequestMirrorPolicy:
    def __init__(
        self,
        *,
        destination: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#destination NetworkServicesHttpRoute#destination}
        '''
        if isinstance(destination, dict):
            destination = NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination(**destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f657e7a20eef83907ecb134308bfba767c7ee24611ae281a20dbf904e2d693)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination"]:
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#destination NetworkServicesHttpRoute#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionRequestMirrorPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "weight": "weight"},
)
class NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination:
    def __init__(
        self,
        *,
        service_name: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_name: The URL of a BackendService to route traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#service_name NetworkServicesHttpRoute#service_name}
        :param weight: Specifies the proportion of requests forwarded to the backend referenced by the serviceName field. This is computed as: weight/Sum(weights in this destination list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports. If only one serviceName is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend. If weights are specified for any one service name, they need to be specified for all of them. If weights are unspecified for all services, then, traffic is distributed in equal proportions to all of them. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#weight NetworkServicesHttpRoute#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b08938db935eddb66c3025f44a6dcd07905601e6626606830e6383317cf4e6)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_name is not None:
            self._values["service_name"] = service_name
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The URL of a BackendService to route traffic to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#service_name NetworkServicesHttpRoute#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Specifies the proportion of requests forwarded to the backend referenced by the serviceName field.

        This is computed as: weight/Sum(weights in this destination list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports.
        If only one serviceName is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend.
        If weights are specified for any one service name, they need to be specified for all of them.
        If weights are unspecified for all services, then, traffic is distributed in equal proportions to all of them.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#weight NetworkServicesHttpRoute#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86ba1b2d4dda5009f086062483b125927813d50f2cfab5670cfc83b68991f440)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetServiceName")
    def reset_service_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceName", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="serviceNameInput")
    def service_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

    @service_name.setter
    def service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d39682e7bd44f3a107f58cf52c906509b3ac75f56f2c99d27c9ed021fbc87af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5909b08e4af3cc98e6b695b28136b03bed13789681c0880d9e02646f4f9174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d7763089ce890b71f4478e153cae2dcf4678ab39bc70d991c250e2e4803a2cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2cb7a85260308c5eecc33ada18008caded492bb91306e106c31501e9260ca06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestination")
    def put_destination(
        self,
        *,
        service_name: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_name: The URL of a BackendService to route traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#service_name NetworkServicesHttpRoute#service_name}
        :param weight: Specifies the proportion of requests forwarded to the backend referenced by the serviceName field. This is computed as: weight/Sum(weights in this destination list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports. If only one serviceName is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend. If weights are specified for any one service name, they need to be specified for all of them. If weights are unspecified for all services, then, traffic is distributed in equal proportions to all of them. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#weight NetworkServicesHttpRoute#weight}
        '''
        value = NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination(
            service_name=service_name, weight=weight
        )

        return typing.cast(None, jsii.invoke(self, "putDestination", [value]))

    @jsii.member(jsii_name="resetDestination")
    def reset_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestination", []))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(
        self,
    ) -> NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference:
        return typing.cast(NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicy]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d281bc1e52ea819b3dba8e421b00582da05c1fa710d939aee58dc2487d135bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionResponseHeaderModifier",
    jsii_struct_bases=[],
    name_mapping={"add": "add", "remove": "remove", "set": "set"},
)
class NetworkServicesHttpRouteRulesActionResponseHeaderModifier:
    def __init__(
        self,
        *,
        add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param add: Add the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#add NetworkServicesHttpRoute#add}
        :param remove: Remove headers (matching by header names) specified in the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#remove NetworkServicesHttpRoute#remove}
        :param set: Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#set NetworkServicesHttpRoute#set}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a4ed15ec6790e3624245947ec0ceffceaf23f1546675b97c584b1a339a9b1b)
            check_type(argname="argument add", value=add, expected_type=type_hints["add"])
            check_type(argname="argument remove", value=remove, expected_type=type_hints["remove"])
            check_type(argname="argument set", value=set, expected_type=type_hints["set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add is not None:
            self._values["add"] = add
        if remove is not None:
            self._values["remove"] = remove
        if set is not None:
            self._values["set"] = set

    @builtins.property
    def add(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Add the headers with given map where key is the name of the header, value is the value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#add NetworkServicesHttpRoute#add}
        '''
        result = self._values.get("add")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def remove(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Remove headers (matching by header names) specified in the list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#remove NetworkServicesHttpRoute#remove}
        '''
        result = self._values.get("remove")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def set(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#set NetworkServicesHttpRoute#set}
        '''
        result = self._values.get("set")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionResponseHeaderModifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dd162e7eda962f2f2e3d33c9cf8181c4c7cf8383d330b852174a0a84f2cfcc3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAdd")
    def reset_add(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdd", []))

    @jsii.member(jsii_name="resetRemove")
    def reset_remove(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemove", []))

    @jsii.member(jsii_name="resetSet")
    def reset_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSet", []))

    @builtins.property
    @jsii.member(jsii_name="addInput")
    def add_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "addInput"))

    @builtins.property
    @jsii.member(jsii_name="removeInput")
    def remove_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "removeInput"))

    @builtins.property
    @jsii.member(jsii_name="setInput")
    def set_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="add")
    def add(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "add"))

    @add.setter
    def add(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb6deb17b8ec810c556579e4ec3413308322267256aee6f98f3390b905b6bc36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "add", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remove")
    def remove(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remove"))

    @remove.setter
    def remove(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6084cac3085bc88a39e4e16a2ec8309651d4be57e9f35e51f2ed56b82f8e99b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remove", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "set"))

    @set.setter
    def set(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1e850fd86db40086ad5a33a089e76ec079ac9650e4888217ff3fd4ddb1af36a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "set", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionResponseHeaderModifier]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionResponseHeaderModifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionResponseHeaderModifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__430055a5bed2ffceddfe36d5719b4fdbde6a77f0f233b2559c51f10e55cd09f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "num_retries": "numRetries",
        "per_try_timeout": "perTryTimeout",
        "retry_conditions": "retryConditions",
    },
)
class NetworkServicesHttpRouteRulesActionRetryPolicy:
    def __init__(
        self,
        *,
        num_retries: typing.Optional[jsii.Number] = None,
        per_try_timeout: typing.Optional[builtins.str] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param num_retries: Specifies the allowed number of retries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#num_retries NetworkServicesHttpRoute#num_retries}
        :param per_try_timeout: Specifies a non-zero timeout per retry attempt. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#per_try_timeout NetworkServicesHttpRoute#per_try_timeout}
        :param retry_conditions: Specifies one or more conditions when this retry policy applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#retry_conditions NetworkServicesHttpRoute#retry_conditions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b29ccd4b56a42a75fefa6d0156165ed56c0d3d3d2fd6990dfdda622c9526297)
            check_type(argname="argument num_retries", value=num_retries, expected_type=type_hints["num_retries"])
            check_type(argname="argument per_try_timeout", value=per_try_timeout, expected_type=type_hints["per_try_timeout"])
            check_type(argname="argument retry_conditions", value=retry_conditions, expected_type=type_hints["retry_conditions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if num_retries is not None:
            self._values["num_retries"] = num_retries
        if per_try_timeout is not None:
            self._values["per_try_timeout"] = per_try_timeout
        if retry_conditions is not None:
            self._values["retry_conditions"] = retry_conditions

    @builtins.property
    def num_retries(self) -> typing.Optional[jsii.Number]:
        '''Specifies the allowed number of retries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#num_retries NetworkServicesHttpRoute#num_retries}
        '''
        result = self._values.get("num_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def per_try_timeout(self) -> typing.Optional[builtins.str]:
        '''Specifies a non-zero timeout per retry attempt.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#per_try_timeout NetworkServicesHttpRoute#per_try_timeout}
        '''
        result = self._values.get("per_try_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies one or more conditions when this retry policy applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#retry_conditions NetworkServicesHttpRoute#retry_conditions}
        '''
        result = self._values.get("retry_conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__447089d3d100b5b03f74c604305dbde9fd8317c3ee152e0ea9cd81385667f006)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNumRetries")
    def reset_num_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumRetries", []))

    @jsii.member(jsii_name="resetPerTryTimeout")
    def reset_per_try_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerTryTimeout", []))

    @jsii.member(jsii_name="resetRetryConditions")
    def reset_retry_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryConditions", []))

    @builtins.property
    @jsii.member(jsii_name="numRetriesInput")
    def num_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numRetriesInput"))

    @builtins.property
    @jsii.member(jsii_name="perTryTimeoutInput")
    def per_try_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "perTryTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="retryConditionsInput")
    def retry_conditions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "retryConditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="numRetries")
    def num_retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numRetries"))

    @num_retries.setter
    def num_retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f74d2141ae2e275e86e66b49cb2ce7fd6eab535031fd9284e5d93d8199679f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perTryTimeout")
    def per_try_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perTryTimeout"))

    @per_try_timeout.setter
    def per_try_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d972fb51472459d0c25c53186bb48747de6b068f8894d7073eac8c9263776a63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perTryTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryConditions")
    def retry_conditions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "retryConditions"))

    @retry_conditions.setter
    def retry_conditions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc44422848a293359a97491c0c0dc84f40069e0b73fe9f4c18715be76736a90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryConditions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionRetryPolicy]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c96029ce23fdbeab6ad9f339feaa555e7506430d24f094345fe72b125976dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionUrlRewrite",
    jsii_struct_bases=[],
    name_mapping={
        "host_rewrite": "hostRewrite",
        "path_prefix_rewrite": "pathPrefixRewrite",
    },
)
class NetworkServicesHttpRouteRulesActionUrlRewrite:
    def __init__(
        self,
        *,
        host_rewrite: typing.Optional[builtins.str] = None,
        path_prefix_rewrite: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected destination, the requests host header is replaced by this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#host_rewrite NetworkServicesHttpRoute#host_rewrite}
        :param path_prefix_rewrite: Prior to forwarding the request to the selected destination, the matching portion of the requests path is replaced by this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#path_prefix_rewrite NetworkServicesHttpRoute#path_prefix_rewrite}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4279740ce90e32b1e9e794bcd27a81d0bda983bc0c15dcae2c7219cd6dfec9)
            check_type(argname="argument host_rewrite", value=host_rewrite, expected_type=type_hints["host_rewrite"])
            check_type(argname="argument path_prefix_rewrite", value=path_prefix_rewrite, expected_type=type_hints["path_prefix_rewrite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if host_rewrite is not None:
            self._values["host_rewrite"] = host_rewrite
        if path_prefix_rewrite is not None:
            self._values["path_prefix_rewrite"] = path_prefix_rewrite

    @builtins.property
    def host_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected destination, the requests host header is replaced by this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#host_rewrite NetworkServicesHttpRoute#host_rewrite}
        '''
        result = self._values.get("host_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_prefix_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected destination, the matching portion of the requests path is replaced by this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#path_prefix_rewrite NetworkServicesHttpRoute#path_prefix_rewrite}
        '''
        result = self._values.get("path_prefix_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesActionUrlRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesActionUrlRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesActionUrlRewriteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff3a7dd753a725657be680dd53070db5e6941d5f308cf2c176f2daea8618c68c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostRewrite")
    def reset_host_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostRewrite", []))

    @jsii.member(jsii_name="resetPathPrefixRewrite")
    def reset_path_prefix_rewrite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathPrefixRewrite", []))

    @builtins.property
    @jsii.member(jsii_name="hostRewriteInput")
    def host_rewrite_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="pathPrefixRewriteInput")
    def path_prefix_rewrite_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathPrefixRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="hostRewrite")
    def host_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostRewrite"))

    @host_rewrite.setter
    def host_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f611f23ec92c813ca483649b1a5aac91606fb0a14f61ac88db85c6754fb725a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathPrefixRewrite")
    def path_prefix_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathPrefixRewrite"))

    @path_prefix_rewrite.setter
    def path_prefix_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388a3637da7b37dde9080a8aa7d087ff7ccf916dd77c3c6bf763171aeafa6c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathPrefixRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesActionUrlRewrite]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesActionUrlRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesActionUrlRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829e960a71e65ffd123aa6790fcc3ea1f973b221d2ecbc60dace586aea6a0a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c156b356b8e4037f4a2f899160d38574457cd66256ba827f6ee3bd5316cb118)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkServicesHttpRouteRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa568dfb157a630f9c776da591b3e78776dda31bf5e209e6a3ebba18429e1f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesHttpRouteRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5a63bda0c5adf84ec7697d956509a599d1d7e078e52792029509670afdc6d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39cb3c9e8fa629367239b4edc947b8cd0a844fbd6ac6635ffa972e00530b0153)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2795087403dda5e8b5908f10d8c30415c77e2caa40669e89822a79bec6a13088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5422cfb28956a5e156c8b616a0c8aea974195ae34db17626c0de68ea486928e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatches",
    jsii_struct_bases=[],
    name_mapping={
        "full_path_match": "fullPathMatch",
        "headers": "headers",
        "ignore_case": "ignoreCase",
        "prefix_match": "prefixMatch",
        "query_parameters": "queryParameters",
        "regex_match": "regexMatch",
    },
)
class NetworkServicesHttpRouteRulesMatches:
    def __init__(
        self,
        *,
        full_path_match: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesHttpRouteRulesMatchesHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix_match: typing.Optional[builtins.str] = None,
        query_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesHttpRouteRulesMatchesQueryParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        regex_match: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param full_path_match: The HTTP request path value should exactly match this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#full_path_match NetworkServicesHttpRoute#full_path_match}
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#headers NetworkServicesHttpRoute#headers}
        :param ignore_case: Specifies if prefixMatch and fullPathMatch matches are case sensitive. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#ignore_case NetworkServicesHttpRoute#ignore_case}
        :param prefix_match: The HTTP request path value must begin with specified prefixMatch. prefixMatch must begin with a /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#prefix_match NetworkServicesHttpRoute#prefix_match}
        :param query_parameters: query_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#query_parameters NetworkServicesHttpRoute#query_parameters}
        :param regex_match: The HTTP request path value must satisfy the regular expression specified by regexMatch after removing any query parameters and anchor supplied with the original URL. For regular expression grammar, please see https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#regex_match NetworkServicesHttpRoute#regex_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3285bbd314d367be58f3fc389c8e05905e1b183f8bf8daeb1b9a1e666108c00)
            check_type(argname="argument full_path_match", value=full_path_match, expected_type=type_hints["full_path_match"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument ignore_case", value=ignore_case, expected_type=type_hints["ignore_case"])
            check_type(argname="argument prefix_match", value=prefix_match, expected_type=type_hints["prefix_match"])
            check_type(argname="argument query_parameters", value=query_parameters, expected_type=type_hints["query_parameters"])
            check_type(argname="argument regex_match", value=regex_match, expected_type=type_hints["regex_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if full_path_match is not None:
            self._values["full_path_match"] = full_path_match
        if headers is not None:
            self._values["headers"] = headers
        if ignore_case is not None:
            self._values["ignore_case"] = ignore_case
        if prefix_match is not None:
            self._values["prefix_match"] = prefix_match
        if query_parameters is not None:
            self._values["query_parameters"] = query_parameters
        if regex_match is not None:
            self._values["regex_match"] = regex_match

    @builtins.property
    def full_path_match(self) -> typing.Optional[builtins.str]:
        '''The HTTP request path value should exactly match this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#full_path_match NetworkServicesHttpRoute#full_path_match}
        '''
        result = self._values.get("full_path_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesMatchesHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#headers NetworkServicesHttpRoute#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesMatchesHeaders"]]], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if prefixMatch and fullPathMatch matches are case sensitive. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#ignore_case NetworkServicesHttpRoute#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[builtins.str]:
        '''The HTTP request path value must begin with specified prefixMatch. prefixMatch must begin with a /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#prefix_match NetworkServicesHttpRoute#prefix_match}
        '''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesMatchesQueryParameters"]]]:
        '''query_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#query_parameters NetworkServicesHttpRoute#query_parameters}
        '''
        result = self._values.get("query_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesMatchesQueryParameters"]]], result)

    @builtins.property
    def regex_match(self) -> typing.Optional[builtins.str]:
        '''The HTTP request path value must satisfy the regular expression specified by regexMatch after removing any query parameters and anchor supplied with the original URL.

        For regular expression grammar, please see https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#regex_match NetworkServicesHttpRoute#regex_match}
        '''
        result = self._values.get("regex_match")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesMatches(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "exact_match": "exactMatch",
        "header": "header",
        "invert_match": "invertMatch",
        "prefix_match": "prefixMatch",
        "present_match": "presentMatch",
        "range_match": "rangeMatch",
        "regex_match": "regexMatch",
        "suffix_match": "suffixMatch",
    },
)
class NetworkServicesHttpRouteRulesMatchesHeaders:
    def __init__(
        self,
        *,
        exact_match: typing.Optional[builtins.str] = None,
        header: typing.Optional[builtins.str] = None,
        invert_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix_match: typing.Optional[builtins.str] = None,
        present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        range_match: typing.Optional[typing.Union["NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        regex_match: typing.Optional[builtins.str] = None,
        suffix_match: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact_match: The value of the header should match exactly the content of exactMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#exact_match NetworkServicesHttpRoute#exact_match}
        :param header: The name of the HTTP header to match against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#header NetworkServicesHttpRoute#header}
        :param invert_match: If specified, the match result will be inverted before checking. Default value is set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#invert_match NetworkServicesHttpRoute#invert_match}
        :param prefix_match: The value of the header must start with the contents of prefixMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#prefix_match NetworkServicesHttpRoute#prefix_match}
        :param present_match: A header with headerName must exist. The match takes place whether or not the header has a value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#present_match NetworkServicesHttpRoute#present_match}
        :param range_match: range_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#range_match NetworkServicesHttpRoute#range_match}
        :param regex_match: The value of the header must match the regular expression specified in regexMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#regex_match NetworkServicesHttpRoute#regex_match}
        :param suffix_match: The value of the header must end with the contents of suffixMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#suffix_match NetworkServicesHttpRoute#suffix_match}
        '''
        if isinstance(range_match, dict):
            range_match = NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch(**range_match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e135aa55ae923f84f0c26229610f6a352f4e208d099852b50d8a2ec5f446a3f)
            check_type(argname="argument exact_match", value=exact_match, expected_type=type_hints["exact_match"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument invert_match", value=invert_match, expected_type=type_hints["invert_match"])
            check_type(argname="argument prefix_match", value=prefix_match, expected_type=type_hints["prefix_match"])
            check_type(argname="argument present_match", value=present_match, expected_type=type_hints["present_match"])
            check_type(argname="argument range_match", value=range_match, expected_type=type_hints["range_match"])
            check_type(argname="argument regex_match", value=regex_match, expected_type=type_hints["regex_match"])
            check_type(argname="argument suffix_match", value=suffix_match, expected_type=type_hints["suffix_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact_match is not None:
            self._values["exact_match"] = exact_match
        if header is not None:
            self._values["header"] = header
        if invert_match is not None:
            self._values["invert_match"] = invert_match
        if prefix_match is not None:
            self._values["prefix_match"] = prefix_match
        if present_match is not None:
            self._values["present_match"] = present_match
        if range_match is not None:
            self._values["range_match"] = range_match
        if regex_match is not None:
            self._values["regex_match"] = regex_match
        if suffix_match is not None:
            self._values["suffix_match"] = suffix_match

    @builtins.property
    def exact_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header should match exactly the content of exactMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#exact_match NetworkServicesHttpRoute#exact_match}
        '''
        result = self._values.get("exact_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header(self) -> typing.Optional[builtins.str]:
        '''The name of the HTTP header to match against.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#header NetworkServicesHttpRoute#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If specified, the match result will be inverted before checking. Default value is set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#invert_match NetworkServicesHttpRoute#invert_match}
        '''
        result = self._values.get("invert_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must start with the contents of prefixMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#prefix_match NetworkServicesHttpRoute#prefix_match}
        '''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def present_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A header with headerName must exist. The match takes place whether or not the header has a value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#present_match NetworkServicesHttpRoute#present_match}
        '''
        result = self._values.get("present_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def range_match(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch"]:
        '''range_match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#range_match NetworkServicesHttpRoute#range_match}
        '''
        result = self._values.get("range_match")
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch"], result)

    @builtins.property
    def regex_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must match the regular expression specified in regexMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#regex_match NetworkServicesHttpRoute#regex_match}
        '''
        result = self._values.get("regex_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must end with the contents of suffixMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#suffix_match NetworkServicesHttpRoute#suffix_match}
        '''
        result = self._values.get("suffix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesMatchesHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesMatchesHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb048501c5ba122878c97d8d457606b942af3981d253fea04c57136fec4386de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesHttpRouteRulesMatchesHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3801769ee86bb5107cbeb6826b4f567de20acacec735ef2c4b80b5e2627a91a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesHttpRouteRulesMatchesHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2a27c73e9521c7bc6c7af6820a7852ffcf578596aa07bec287c3145767425d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84104eec01e2529be0456f337831c280cc1e74819a72925c205774291bcb7d27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93015ea414344a94da902dd936b3d855831ff69be1695ce0bba4316f813cd595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb05ff8a441a082d8a3576276eb077695f7084bcae247520e20ccf5833634aa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesMatchesHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2e9a7a1f879666eedf6df6f1bc0a00ded877381e1ab45d33009c1c8e9239125)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRangeMatch")
    def put_range_match(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: End of the range (exclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#end NetworkServicesHttpRoute#end}
        :param start: Start of the range (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#start NetworkServicesHttpRoute#start}
        '''
        value = NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch(
            end=end, start=start
        )

        return typing.cast(None, jsii.invoke(self, "putRangeMatch", [value]))

    @jsii.member(jsii_name="resetExactMatch")
    def reset_exact_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExactMatch", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetInvertMatch")
    def reset_invert_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvertMatch", []))

    @jsii.member(jsii_name="resetPrefixMatch")
    def reset_prefix_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixMatch", []))

    @jsii.member(jsii_name="resetPresentMatch")
    def reset_present_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresentMatch", []))

    @jsii.member(jsii_name="resetRangeMatch")
    def reset_range_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRangeMatch", []))

    @jsii.member(jsii_name="resetRegexMatch")
    def reset_regex_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegexMatch", []))

    @jsii.member(jsii_name="resetSuffixMatch")
    def reset_suffix_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuffixMatch", []))

    @builtins.property
    @jsii.member(jsii_name="rangeMatch")
    def range_match(
        self,
    ) -> "NetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference":
        return typing.cast("NetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference", jsii.get(self, "rangeMatch"))

    @builtins.property
    @jsii.member(jsii_name="exactMatchInput")
    def exact_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="invertMatchInput")
    def invert_match_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "invertMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixMatchInput")
    def prefix_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="presentMatchInput")
    def present_match_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "presentMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeMatchInput")
    def range_match_input(
        self,
    ) -> typing.Optional["NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch"]:
        return typing.cast(typing.Optional["NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch"], jsii.get(self, "rangeMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="regexMatchInput")
    def regex_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="suffixMatchInput")
    def suffix_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "suffixMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="exactMatch")
    def exact_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exactMatch"))

    @exact_match.setter
    def exact_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce9781780befd452d7a13e07f8cfe0b5449dc338704209e9ca70387321e7958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exactMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__189fe652842fcdbd6416ed47c15734173b2680f55c31020a06a54bfa864fa3bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="invertMatch")
    def invert_match(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "invertMatch"))

    @invert_match.setter
    def invert_match(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__658040cd9ed114e365a8d1d8b401068b63b84b16fd29d668c7ff8c096cd2d346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff262107ea69907e7c422f22bbd71e8206807a4c75db9e88fa9c0f2f5f9f417)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="presentMatch")
    def present_match(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "presentMatch"))

    @present_match.setter
    def present_match(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fddee939471a4e2e0b919b9fad08d09292cb2864ca3549fce8582ef15c8f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regexMatch")
    def regex_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regexMatch"))

    @regex_match.setter
    def regex_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d538724d1617b552abac13aa1d06e35185dada0f95c2afb14e80ec4f73ecc72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffixMatch")
    def suffix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffixMatch"))

    @suffix_match.setter
    def suffix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55179dae611a2a58086d3c948403dd74e25395b69542917f6d9704e20e12f425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatchesHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatchesHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatchesHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8695f631107451f9f3968641740919a93bd851abead44a40bea9b03b0851131)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch:
    def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: End of the range (exclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#end NetworkServicesHttpRoute#end}
        :param start: Start of the range (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#start NetworkServicesHttpRoute#start}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c7dd253f4bb7c03980a2e4f75dc23b81a1002b4939d9be7016ed1bc86dcbd7)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''End of the range (exclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#end NetworkServicesHttpRoute#end}
        '''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Start of the range (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#start NetworkServicesHttpRoute#start}
        '''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0e26befdf4009d08399dc5ffc1dc24ee49027066d005449144bf8e085d956a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="endInput")
    def end_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="end")
    def end(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "end"))

    @end.setter
    def end(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8f19aba1645829aa151fdeae9d4cc924c0dc7d8f6f3e6ad1d71254b7eb5848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfc28905ae5e33b1ab273d2e47f203414896d500b7d819b12f252a6444b489b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40af096b78acb3d13e40afec1eae7cb7af60a0df753d99cb3d8f322e9c104798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesMatchesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96ec8acad40632db9549861106a6eb6835f15dec91f77edd2dc4bacc91cf6eca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesHttpRouteRulesMatchesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__943df01b555e0d54ddc7ce07e0d928a540c2a81eff45098ebba693ecfca28440)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesHttpRouteRulesMatchesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4f3af668e8a38a68cf202b01786237de35f898abc0353824beefaec45a2cf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__770e8f25047f1a948af14d1b8cb480a405e02aedd2b4bc8d94dcf5f2c05ad60b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15b33f2ea1d6ca83ce6056ff3676c2b3bd9c307498aa59a8f8846f6ebbc3e27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatches]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatches]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatches]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__056a3c0f4588bf45c2edfc092a1c0726f1cff3b478cd5331b71b5f216e99ee35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesMatchesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38f2f842e0163b8608eff6f1c72f3f412ef24803954e42363fe833600aa7580e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7775f1f50262ffd4f754ae15ae908cdb962f3e170fede249c95a7c7a7d745e02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParameters")
    def put_query_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesHttpRouteRulesMatchesQueryParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59c427fed7b25eb3629d3ad0795cfb44fd14b310a70cb49f7c3ba02d1eeb4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQueryParameters", [value]))

    @jsii.member(jsii_name="resetFullPathMatch")
    def reset_full_path_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullPathMatch", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetIgnoreCase")
    def reset_ignore_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreCase", []))

    @jsii.member(jsii_name="resetPrefixMatch")
    def reset_prefix_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefixMatch", []))

    @jsii.member(jsii_name="resetQueryParameters")
    def reset_query_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParameters", []))

    @jsii.member(jsii_name="resetRegexMatch")
    def reset_regex_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegexMatch", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> NetworkServicesHttpRouteRulesMatchesHeadersList:
        return typing.cast(NetworkServicesHttpRouteRulesMatchesHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParameters")
    def query_parameters(
        self,
    ) -> "NetworkServicesHttpRouteRulesMatchesQueryParametersList":
        return typing.cast("NetworkServicesHttpRouteRulesMatchesQueryParametersList", jsii.get(self, "queryParameters"))

    @builtins.property
    @jsii.member(jsii_name="fullPathMatchInput")
    def full_path_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullPathMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreCaseInput")
    def ignore_case_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreCaseInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixMatchInput")
    def prefix_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParametersInput")
    def query_parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesMatchesQueryParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesHttpRouteRulesMatchesQueryParameters"]]], jsii.get(self, "queryParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="regexMatchInput")
    def regex_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="fullPathMatch")
    def full_path_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fullPathMatch"))

    @full_path_match.setter
    def full_path_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42522f50dc01fc9c14d579ec9ad5cc12f72993e4601a053c4c4aae33a7bd7b37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullPathMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreCase")
    def ignore_case(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreCase"))

    @ignore_case.setter
    def ignore_case(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc946a7e735d271b82377569d62ea57d8c3288ac6988f35fc60caa8175cc0572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e80ea303481637050758040f69a238137446005f2480f475ff88d7f608884b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regexMatch")
    def regex_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regexMatch"))

    @regex_match.setter
    def regex_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29017038d42f4aaf94ce962d38f3f90896c6128a055fbd87411081d6955c28bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatches]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatches]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatches]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89838303152263d78a6681250a4e777c963ffad44af59468ba4e4796269a0fbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesQueryParameters",
    jsii_struct_bases=[],
    name_mapping={
        "exact_match": "exactMatch",
        "present_match": "presentMatch",
        "query_parameter": "queryParameter",
        "regex_match": "regexMatch",
    },
)
class NetworkServicesHttpRouteRulesMatchesQueryParameters:
    def __init__(
        self,
        *,
        exact_match: typing.Optional[builtins.str] = None,
        present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_parameter: typing.Optional[builtins.str] = None,
        regex_match: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact_match: The value of the query parameter must exactly match the contents of exactMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#exact_match NetworkServicesHttpRoute#exact_match}
        :param present_match: Specifies that the QueryParameterMatcher matches if request contains query parameter, irrespective of whether the parameter has a value or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#present_match NetworkServicesHttpRoute#present_match}
        :param query_parameter: The name of the query parameter to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#query_parameter NetworkServicesHttpRoute#query_parameter}
        :param regex_match: The value of the query parameter must match the regular expression specified by regexMatch.For regular expression grammar, please see https://github.com/google/re2/wiki/Syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#regex_match NetworkServicesHttpRoute#regex_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de62fdb9376acf32472aa5927511b9c4ba16338804ed565eebf6e1f66f3604d)
            check_type(argname="argument exact_match", value=exact_match, expected_type=type_hints["exact_match"])
            check_type(argname="argument present_match", value=present_match, expected_type=type_hints["present_match"])
            check_type(argname="argument query_parameter", value=query_parameter, expected_type=type_hints["query_parameter"])
            check_type(argname="argument regex_match", value=regex_match, expected_type=type_hints["regex_match"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exact_match is not None:
            self._values["exact_match"] = exact_match
        if present_match is not None:
            self._values["present_match"] = present_match
        if query_parameter is not None:
            self._values["query_parameter"] = query_parameter
        if regex_match is not None:
            self._values["regex_match"] = regex_match

    @builtins.property
    def exact_match(self) -> typing.Optional[builtins.str]:
        '''The value of the query parameter must exactly match the contents of exactMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#exact_match NetworkServicesHttpRoute#exact_match}
        '''
        result = self._values.get("exact_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def present_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that the QueryParameterMatcher matches if request contains query parameter, irrespective of whether the parameter has a value or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#present_match NetworkServicesHttpRoute#present_match}
        '''
        result = self._values.get("present_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_parameter(self) -> typing.Optional[builtins.str]:
        '''The name of the query parameter to match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#query_parameter NetworkServicesHttpRoute#query_parameter}
        '''
        result = self._values.get("query_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex_match(self) -> typing.Optional[builtins.str]:
        '''The value of the query parameter must match the regular expression specified by regexMatch.For regular expression grammar, please see https://github.com/google/re2/wiki/Syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#regex_match NetworkServicesHttpRoute#regex_match}
        '''
        result = self._values.get("regex_match")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteRulesMatchesQueryParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteRulesMatchesQueryParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesQueryParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__929ecbdfba23f99f2af330a7f18bb4f5e7b38b79e1f2c882f85205d4d098f2f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0228aca4939bd6a95b32212fc080db69ba7001dcf9736266dd631415e21970)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa677cd4d411cf2176b385d7a60d1f719d7aa1fb600afb6b3ec375de490b0c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb113ca128b7b55043451c3b2029028e8553558eb0e8f51ffb36abe591fc8661)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dff646b25a70da5431f20a4a60fd237b78c58c8520bc157482827582d4f8ff67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesQueryParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesQueryParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesQueryParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a65f66d2e530c7f0cbf82679e46247200dd39bf0bbe4e86c26e65143b0b487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e7dd32932d65f9d2f8f8cc63abe8f62776be2aa9a94c6ea651a9220307018ca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExactMatch")
    def reset_exact_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExactMatch", []))

    @jsii.member(jsii_name="resetPresentMatch")
    def reset_present_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPresentMatch", []))

    @jsii.member(jsii_name="resetQueryParameter")
    def reset_query_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryParameter", []))

    @jsii.member(jsii_name="resetRegexMatch")
    def reset_regex_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegexMatch", []))

    @builtins.property
    @jsii.member(jsii_name="exactMatchInput")
    def exact_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exactMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="presentMatchInput")
    def present_match_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "presentMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="queryParameterInput")
    def query_parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryParameterInput"))

    @builtins.property
    @jsii.member(jsii_name="regexMatchInput")
    def regex_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="exactMatch")
    def exact_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "exactMatch"))

    @exact_match.setter
    def exact_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a2b2c5799f069d9faab12041fe7f1b335064737ea640688ff2e5ddbc3580ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exactMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="presentMatch")
    def present_match(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "presentMatch"))

    @present_match.setter
    def present_match(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cad8e2d1fc9f39ac694eb701442407e5864e0cd861e562764f87ef6feade15e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryParameter")
    def query_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryParameter"))

    @query_parameter.setter
    def query_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73d195d92d504c6222bae2b8cf78aafdeace8fb015c2740b5a34bd2c51dee7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regexMatch")
    def regex_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regexMatch"))

    @regex_match.setter
    def regex_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1b57b917bf3c1c8df907001a6bc39c618c8bb377f5fed99cf20dc6000018db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatchesQueryParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatchesQueryParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatchesQueryParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb54af93977051ada27c7721cde43ea72683698576a4b765d284be63d4e03520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesHttpRouteRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c6a551235720588d6744a2f70fcdaf1db5000a907ce6cd79dad94ab10be3694)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        cors_policy: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionCorsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        fault_injection_policy: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionFaultInjectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        redirect: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
        request_header_modifier: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRequestHeaderModifier, typing.Dict[builtins.str, typing.Any]]] = None,
        request_mirror_policy: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRequestMirrorPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        response_header_modifier: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionResponseHeaderModifier, typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[builtins.str] = None,
        url_rewrite: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionUrlRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cors_policy: cors_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#cors_policy NetworkServicesHttpRoute#cors_policy}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#destinations NetworkServicesHttpRoute#destinations}
        :param fault_injection_policy: fault_injection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#fault_injection_policy NetworkServicesHttpRoute#fault_injection_policy}
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#redirect NetworkServicesHttpRoute#redirect}
        :param request_header_modifier: request_header_modifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#request_header_modifier NetworkServicesHttpRoute#request_header_modifier}
        :param request_mirror_policy: request_mirror_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#request_mirror_policy NetworkServicesHttpRoute#request_mirror_policy}
        :param response_header_modifier: response_header_modifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#response_header_modifier NetworkServicesHttpRoute#response_header_modifier}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#retry_policy NetworkServicesHttpRoute#retry_policy}
        :param timeout: Specifies the timeout for selected route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#timeout NetworkServicesHttpRoute#timeout}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#url_rewrite NetworkServicesHttpRoute#url_rewrite}
        '''
        value = NetworkServicesHttpRouteRulesAction(
            cors_policy=cors_policy,
            destinations=destinations,
            fault_injection_policy=fault_injection_policy,
            redirect=redirect,
            request_header_modifier=request_header_modifier,
            request_mirror_policy=request_mirror_policy,
            response_header_modifier=response_header_modifier,
            retry_policy=retry_policy,
            timeout=timeout,
            url_rewrite=url_rewrite,
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatches")
    def put_matches(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c79a63fbea71ffa0a3972f22ea53bbda9c3b629e87eecd75207ca18d4efebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatches", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetMatches")
    def reset_matches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatches", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> NetworkServicesHttpRouteRulesActionOutputReference:
        return typing.cast(NetworkServicesHttpRouteRulesActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="matches")
    def matches(self) -> NetworkServicesHttpRouteRulesMatchesList:
        return typing.cast(NetworkServicesHttpRouteRulesMatchesList, jsii.get(self, "matches"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[NetworkServicesHttpRouteRulesAction]:
        return typing.cast(typing.Optional[NetworkServicesHttpRouteRulesAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchesInput")
    def matches_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatches]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatches]]], jsii.get(self, "matchesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa15e2d1c6c7dd841d207838068e4d749d73c744fa4a18a3ff9ef5cdb4c94f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkServicesHttpRouteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#create NetworkServicesHttpRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#delete NetworkServicesHttpRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#update NetworkServicesHttpRoute#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c070be931c822d18c156be32535c90db010ecba050be578b64d9a23d5355e474)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#create NetworkServicesHttpRoute#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#delete NetworkServicesHttpRoute#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_http_route#update NetworkServicesHttpRoute#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesHttpRouteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesHttpRouteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesHttpRoute.NetworkServicesHttpRouteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4269ac72155c26a710b23773b4647ca5a3760059472b22addf4f93bfe26f8f4f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6922d71cdfaa9834e86a0a0eb2b6d72142e52874eebc8329c10ed11ac6911337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c4d58d99c287368d45136cb1c88d656c03743e59ae0b50ea5e66b7cf0b60d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__845775e23ea36f992e2a4b9ee23ba6ebf48623efa692741008bfbe3fabc2bc99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be810e601e19701f7dc29f598fa709637f8b4b4fcc4a38ee5182c174a9063c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkServicesHttpRoute",
    "NetworkServicesHttpRouteConfig",
    "NetworkServicesHttpRouteRules",
    "NetworkServicesHttpRouteRulesAction",
    "NetworkServicesHttpRouteRulesActionCorsPolicy",
    "NetworkServicesHttpRouteRulesActionCorsPolicyOutputReference",
    "NetworkServicesHttpRouteRulesActionDestinations",
    "NetworkServicesHttpRouteRulesActionDestinationsList",
    "NetworkServicesHttpRouteRulesActionDestinationsOutputReference",
    "NetworkServicesHttpRouteRulesActionFaultInjectionPolicy",
    "NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort",
    "NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference",
    "NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay",
    "NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference",
    "NetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference",
    "NetworkServicesHttpRouteRulesActionOutputReference",
    "NetworkServicesHttpRouteRulesActionRedirect",
    "NetworkServicesHttpRouteRulesActionRedirectOutputReference",
    "NetworkServicesHttpRouteRulesActionRequestHeaderModifier",
    "NetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference",
    "NetworkServicesHttpRouteRulesActionRequestMirrorPolicy",
    "NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination",
    "NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference",
    "NetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference",
    "NetworkServicesHttpRouteRulesActionResponseHeaderModifier",
    "NetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference",
    "NetworkServicesHttpRouteRulesActionRetryPolicy",
    "NetworkServicesHttpRouteRulesActionRetryPolicyOutputReference",
    "NetworkServicesHttpRouteRulesActionUrlRewrite",
    "NetworkServicesHttpRouteRulesActionUrlRewriteOutputReference",
    "NetworkServicesHttpRouteRulesList",
    "NetworkServicesHttpRouteRulesMatches",
    "NetworkServicesHttpRouteRulesMatchesHeaders",
    "NetworkServicesHttpRouteRulesMatchesHeadersList",
    "NetworkServicesHttpRouteRulesMatchesHeadersOutputReference",
    "NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch",
    "NetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference",
    "NetworkServicesHttpRouteRulesMatchesList",
    "NetworkServicesHttpRouteRulesMatchesOutputReference",
    "NetworkServicesHttpRouteRulesMatchesQueryParameters",
    "NetworkServicesHttpRouteRulesMatchesQueryParametersList",
    "NetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference",
    "NetworkServicesHttpRouteRulesOutputReference",
    "NetworkServicesHttpRouteTimeouts",
    "NetworkServicesHttpRouteTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c305cc4def0e7d84ad90252987aaaee7eecb9190e0d8c1e504d552b4cfd35a80(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hostnames: typing.Sequence[builtins.str],
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRules, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesHttpRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9e2f0fc791c29ff5e27baee8bdf133c693719c925e43aaaaf50f119018d5832c(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a3875fd223efb3c343e731b00bc34cbb1b9eedf3ae9b9011e74af25a16d85b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11cecc59284f0d66aff4d20bd6a649656ba8ee3fc6a6ec720077ca473b2f53c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86d78f808efb1fcb75e09e1882cd362c90604549cbbaeb4eae9618c2f6e63b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcd3a5a33a3858329ea03482cd320c94ba36b4a1e9c05f29fcd08d5c7a602a1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caaf01b18285ecf904b9449b8a7685ab3dab96fdb0eacd913e94b20c38223ab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322b9ba204ae321e174534f830736479cecedba30a9c8e498f9b7ce78aff0a9e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf064eed1ec4eb5220ad4f895c36f9bafc2961b58c3bf4adf3ad4dd53d0dc861(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__747e8577dda277cc3177ac6a748e98ed797245217fd9a74430ad38d8145daaa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e65bff319ee0df7515bcb38a28c7afd3bfefc5b678cf285dbfdc58cc411ae4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c5203647b013b52b91161ef3d81f4f99f5d3f46c962926b7f4051645dd31bf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    hostnames: typing.Sequence[builtins.str],
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRules, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesHttpRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf3aa0040e3cba738360de80c856e683a6417889b98109f3da225d251ddf9b7(
    *,
    action: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesAction, typing.Dict[builtins.str, typing.Any]]] = None,
    matches: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8693db77520f6f22af82c8da15570290b37071807c648f1328b31aa3176b70(
    *,
    cors_policy: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionCorsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fault_injection_policy: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionFaultInjectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    request_header_modifier: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRequestHeaderModifier, typing.Dict[builtins.str, typing.Any]]] = None,
    request_mirror_policy: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRequestMirrorPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    response_header_modifier: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionResponseHeaderModifier, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_policy: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[builtins.str] = None,
    url_rewrite: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionUrlRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06fdce8f8c4375deb682a11d8f3edd18b8a4fec4f1d91886409c28fb7b0e4896(
    *,
    allow_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_methods: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_origin_regexes: typing.Optional[typing.Sequence[builtins.str]] = None,
    allow_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    expose_headers: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_age: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0501a505a9f2a7d213bc60ad891657eb44ab5728e04e8a934e393fd4830ec7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37835fcbbbfb54f492f93962128b802e8166291c387d2b521bf097f5b7ed0ffe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8820e0e21f94266c2bafe1ed6bb522e94d89bbb4712a957f4563ec9a0ea64be(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9086d7f7f331a8e6b88745e639682213d921c54723f7783eb73b03b71bb832(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f847979f6a8fdea170d8b6b8413013aadb55d5e2c98a6528e519ba453c32b038(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4c3822b0dc3709d8ea6c102929b0bcc0233c2837952f9104df7443865fadf1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ff6495c2a68b27233a3f3dcd65936b057bc139a6b61faccae716b9c46ebc4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ede1fcc7b80fe43c51b3d0a22f40423723f7a27565c913f7e6974d3e5328cd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498ce007001580289c50f66fef171fada57a76451de426a4a40e99b8b92b7000(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f9effef0935e0af4f12b710a5dfc5d9e286b8c2dc37b81111849d474e4d3f58(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionCorsPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8ef1d9793a185a106d53ba74ae2bab8ed59267fa00cacead113670b88d1e16(
    *,
    service_name: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee725c4df4fe49eb5390b4cedb107fcb6674ed1973b5df3b420cf9768188fd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6257e6151910f88c17b882536a11d0b124dd6dbfadc5ea190a4a8fe4e4a116a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530ef3b5cacc314727860d597a9e6de357771015b5172001072972ffd9a6e35e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5dd664b01e57f060732c5bf8fd62e45aab514d6b9ccbc98f7cfd27ad35af1e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3aadaef4421ecb539c4b596fc3b37d0bbc0fd8e7397c473516a206635aeeb3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15fa7179bbe2467b35ce4065c823b56535ee7601d8221cbadf37bc227a8bb0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesActionDestinations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cb7167779be68ae5d4d9b3294202789f7ebaf4f93d4c4bd8ac48a87fbe8746(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6eb81c950257dae0a90e73cb5fb5bac7ccc56d45ebc074c5bc64200e717ad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9303a0622d6230b664a98fb8521e7b4e6232ba7866f1855f8d270b8ea42599de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2dd5956464ae67fd1d05eea90a7cd48d34382bea735a6c276942a0fa5d7f56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesActionDestinations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce742f624af3eeff5eb23df147c60f4d94468bc28a1dfc709b3d70a5472b0b9(
    *,
    abort: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort, typing.Dict[builtins.str, typing.Any]]] = None,
    delay: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9704a5da7d239ad40f5b82d9a9c148982378263a964da5906e7d273c3b603578(
    *,
    http_status: typing.Optional[jsii.Number] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056dffdafec34a8554d9e54c379f373ad2cd43ed1d6d88fd5ac72d0fbbc15c32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463214f835baff323385a3d3e46473a28aab34d3b2d259d72886f6c87ecf9aa8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73335e521eae08ccc61ae0614f760a9f33771335955a944689a6385795e8a3b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c09f9ad121da4dd7247724b0455028d0161d9c4a526c7976a986638124b738b(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cbe3bdc0145e3c8fce616cbc15ccd12ad35d61976c6b3de504a05e13495520(
    *,
    fixed_delay: typing.Optional[builtins.str] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5feb1aa7a90a45e3ede671db6623cceb45d0d4570edd2449c126ee60553c456e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de08ff99a9d6db7c685e70cf91329fc2744c60586946f0c7863f6553bde8a2b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38aa0b71e73efb15b1ed8c1b636674e4847dfc86f0a0dcf6790e9a9df0758abd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a96d998b9e52e0e843d1c1dca373615d6e522a17f760a68a361d769694f640(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7626c96ec3c315324778986ef4424f672ac304e1fb6e3653c163fdcfce820a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ede56f97248fce4156aed4169367aa93b73d94ad8b9b086c6b0480cfd3e467(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionFaultInjectionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1161383f720b818f38ab513e0c09dd7b2603e6d529e804229ac9872d2d8e658(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da0e4317937299a8e394cc2ab92f67dce39db08ebfc4ce6643591ef05c5d363(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d44b1051cb2cb98b2e917cdea8df9506f8a8a0903efd12221bededc76585995(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__266425d180373d188ca497499982945f416a2ef991abc43f5645944ace886030(
    value: typing.Optional[NetworkServicesHttpRouteRulesAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd113a5e934c7621fc29022236f0c4556d9fb4e7fe6e40b027aa64abb08ebd25(
    *,
    host_redirect: typing.Optional[builtins.str] = None,
    https_redirect: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    path_redirect: typing.Optional[builtins.str] = None,
    port_redirect: typing.Optional[jsii.Number] = None,
    prefix_rewrite: typing.Optional[builtins.str] = None,
    response_code: typing.Optional[builtins.str] = None,
    strip_query: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b985ddf8a36f90189a29b8776b0b94c7700bf72cf64c7ab88b41851c0ac3d3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a956b51be54de3860e34dc3aa400951d14fce8593de08530b6f067d3f4f3ba0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4f681652b20fc9535dda62530081ec9a13f5f498cde89d373ca45017b5f992(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7b177f463a4becf3fce745c6147119900da94177f8997827d07e0c753138ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ba26e5df32c5b23a90ebf10d077a77118d7a8def81ddfdcf5ba5e1172cec5e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a98faadae2bb542c396c5193f7c8aacf2845096d5d98c0a3e1bfbfac49a9a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f885a36d5e7a02646515ee4f71144b533daca5158b39b01c6422f2350cdbd723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d14bf263238ca394ccff426c1d508596fc982919a79404e71d987fd95d244f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f03a8b7aee5222eb1da317d117e39d328985f19b74db30781ec6e5a10d084f(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9bbfe849a60ef0ed5ea8e9eb2ee18b0878138c8826ce4f98d8f302d2707348(
    *,
    add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa6350c2ae1dc2a4da5a08995a7f8601ec75c085fb03c7df80a629ee80b6ed2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815ed6bdbe732eeed8b2d78db893c3c81aa579988c06467a7539ee798b3c9083(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b81f9110ffd698e824b492e66b182652b74c1c579caaee0663577b307b73e7f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8441e61a052dba9cf79410c1559cba90648f240894e915536b198f536cef6225(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe3a79a3e988839345571cab4018ec31310182d2458933b1a790147176d2ee6c(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionRequestHeaderModifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f657e7a20eef83907ecb134308bfba767c7ee24611ae281a20dbf904e2d693(
    *,
    destination: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b08938db935eddb66c3025f44a6dcd07905601e6626606830e6383317cf4e6(
    *,
    service_name: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ba1b2d4dda5009f086062483b125927813d50f2cfab5670cfc83b68991f440(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d39682e7bd44f3a107f58cf52c906509b3ac75f56f2c99d27c9ed021fbc87af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5909b08e4af3cc98e6b695b28136b03bed13789681c0880d9e02646f4f9174(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7763089ce890b71f4478e153cae2dcf4678ab39bc70d991c250e2e4803a2cb(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2cb7a85260308c5eecc33ada18008caded492bb91306e106c31501e9260ca06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d281bc1e52ea819b3dba8e421b00582da05c1fa710d939aee58dc2487d135bd(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionRequestMirrorPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a4ed15ec6790e3624245947ec0ceffceaf23f1546675b97c584b1a339a9b1b(
    *,
    add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd162e7eda962f2f2e3d33c9cf8181c4c7cf8383d330b852174a0a84f2cfcc3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb6deb17b8ec810c556579e4ec3413308322267256aee6f98f3390b905b6bc36(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6084cac3085bc88a39e4e16a2ec8309651d4be57e9f35e51f2ed56b82f8e99b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1e850fd86db40086ad5a33a089e76ec079ac9650e4888217ff3fd4ddb1af36a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__430055a5bed2ffceddfe36d5719b4fdbde6a77f0f233b2559c51f10e55cd09f9(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionResponseHeaderModifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b29ccd4b56a42a75fefa6d0156165ed56c0d3d3d2fd6990dfdda622c9526297(
    *,
    num_retries: typing.Optional[jsii.Number] = None,
    per_try_timeout: typing.Optional[builtins.str] = None,
    retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447089d3d100b5b03f74c604305dbde9fd8317c3ee152e0ea9cd81385667f006(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f74d2141ae2e275e86e66b49cb2ce7fd6eab535031fd9284e5d93d8199679f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d972fb51472459d0c25c53186bb48747de6b068f8894d7073eac8c9263776a63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc44422848a293359a97491c0c0dc84f40069e0b73fe9f4c18715be76736a90(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c96029ce23fdbeab6ad9f339feaa555e7506430d24f094345fe72b125976dc(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4279740ce90e32b1e9e794bcd27a81d0bda983bc0c15dcae2c7219cd6dfec9(
    *,
    host_rewrite: typing.Optional[builtins.str] = None,
    path_prefix_rewrite: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3a7dd753a725657be680dd53070db5e6941d5f308cf2c176f2daea8618c68c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f611f23ec92c813ca483649b1a5aac91606fb0a14f61ac88db85c6754fb725a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388a3637da7b37dde9080a8aa7d087ff7ccf916dd77c3c6bf763171aeafa6c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829e960a71e65ffd123aa6790fcc3ea1f973b221d2ecbc60dace586aea6a0a14(
    value: typing.Optional[NetworkServicesHttpRouteRulesActionUrlRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c156b356b8e4037f4a2f899160d38574457cd66256ba827f6ee3bd5316cb118(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa568dfb157a630f9c776da591b3e78776dda31bf5e209e6a3ebba18429e1f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5a63bda0c5adf84ec7697d956509a599d1d7e078e52792029509670afdc6d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39cb3c9e8fa629367239b4edc947b8cd0a844fbd6ac6635ffa972e00530b0153(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2795087403dda5e8b5908f10d8c30415c77e2caa40669e89822a79bec6a13088(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5422cfb28956a5e156c8b616a0c8aea974195ae34db17626c0de68ea486928e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3285bbd314d367be58f3fc389c8e05905e1b183f8bf8daeb1b9a1e666108c00(
    *,
    full_path_match: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix_match: typing.Optional[builtins.str] = None,
    query_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesMatchesQueryParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    regex_match: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e135aa55ae923f84f0c26229610f6a352f4e208d099852b50d8a2ec5f446a3f(
    *,
    exact_match: typing.Optional[builtins.str] = None,
    header: typing.Optional[builtins.str] = None,
    invert_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix_match: typing.Optional[builtins.str] = None,
    present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    range_match: typing.Optional[typing.Union[NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    regex_match: typing.Optional[builtins.str] = None,
    suffix_match: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb048501c5ba122878c97d8d457606b942af3981d253fea04c57136fec4386de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3801769ee86bb5107cbeb6826b4f567de20acacec735ef2c4b80b5e2627a91a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2a27c73e9521c7bc6c7af6820a7852ffcf578596aa07bec287c3145767425d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84104eec01e2529be0456f337831c280cc1e74819a72925c205774291bcb7d27(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93015ea414344a94da902dd936b3d855831ff69be1695ce0bba4316f813cd595(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb05ff8a441a082d8a3576276eb077695f7084bcae247520e20ccf5833634aa9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e9a7a1f879666eedf6df6f1bc0a00ded877381e1ab45d33009c1c8e9239125(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce9781780befd452d7a13e07f8cfe0b5449dc338704209e9ca70387321e7958(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__189fe652842fcdbd6416ed47c15734173b2680f55c31020a06a54bfa864fa3bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658040cd9ed114e365a8d1d8b401068b63b84b16fd29d668c7ff8c096cd2d346(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff262107ea69907e7c422f22bbd71e8206807a4c75db9e88fa9c0f2f5f9f417(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fddee939471a4e2e0b919b9fad08d09292cb2864ca3549fce8582ef15c8f6d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d538724d1617b552abac13aa1d06e35185dada0f95c2afb14e80ec4f73ecc72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55179dae611a2a58086d3c948403dd74e25395b69542917f6d9704e20e12f425(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8695f631107451f9f3968641740919a93bd851abead44a40bea9b03b0851131(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatchesHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c7dd253f4bb7c03980a2e4f75dc23b81a1002b4939d9be7016ed1bc86dcbd7(
    *,
    end: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e26befdf4009d08399dc5ffc1dc24ee49027066d005449144bf8e085d956a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8f19aba1645829aa151fdeae9d4cc924c0dc7d8f6f3e6ad1d71254b7eb5848(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfc28905ae5e33b1ab273d2e47f203414896d500b7d819b12f252a6444b489b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40af096b78acb3d13e40afec1eae7cb7af60a0df753d99cb3d8f322e9c104798(
    value: typing.Optional[NetworkServicesHttpRouteRulesMatchesHeadersRangeMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ec8acad40632db9549861106a6eb6835f15dec91f77edd2dc4bacc91cf6eca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__943df01b555e0d54ddc7ce07e0d928a540c2a81eff45098ebba693ecfca28440(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4f3af668e8a38a68cf202b01786237de35f898abc0353824beefaec45a2cf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770e8f25047f1a948af14d1b8cb480a405e02aedd2b4bc8d94dcf5f2c05ad60b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b33f2ea1d6ca83ce6056ff3676c2b3bd9c307498aa59a8f8846f6ebbc3e27a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__056a3c0f4588bf45c2edfc092a1c0726f1cff3b478cd5331b71b5f216e99ee35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatches]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f2f842e0163b8608eff6f1c72f3f412ef24803954e42363fe833600aa7580e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7775f1f50262ffd4f754ae15ae908cdb962f3e170fede249c95a7c7a7d745e02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59c427fed7b25eb3629d3ad0795cfb44fd14b310a70cb49f7c3ba02d1eeb4de(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesMatchesQueryParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42522f50dc01fc9c14d579ec9ad5cc12f72993e4601a053c4c4aae33a7bd7b37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc946a7e735d271b82377569d62ea57d8c3288ac6988f35fc60caa8175cc0572(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80ea303481637050758040f69a238137446005f2480f475ff88d7f608884b07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29017038d42f4aaf94ce962d38f3f90896c6128a055fbd87411081d6955c28bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89838303152263d78a6681250a4e777c963ffad44af59468ba4e4796269a0fbe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatches]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de62fdb9376acf32472aa5927511b9c4ba16338804ed565eebf6e1f66f3604d(
    *,
    exact_match: typing.Optional[builtins.str] = None,
    present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_parameter: typing.Optional[builtins.str] = None,
    regex_match: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929ecbdfba23f99f2af330a7f18bb4f5e7b38b79e1f2c882f85205d4d098f2f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0228aca4939bd6a95b32212fc080db69ba7001dcf9736266dd631415e21970(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa677cd4d411cf2176b385d7a60d1f719d7aa1fb600afb6b3ec375de490b0c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb113ca128b7b55043451c3b2029028e8553558eb0e8f51ffb36abe591fc8661(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff646b25a70da5431f20a4a60fd237b78c58c8520bc157482827582d4f8ff67(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a65f66d2e530c7f0cbf82679e46247200dd39bf0bbe4e86c26e65143b0b487(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesHttpRouteRulesMatchesQueryParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7dd32932d65f9d2f8f8cc63abe8f62776be2aa9a94c6ea651a9220307018ca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a2b2c5799f069d9faab12041fe7f1b335064737ea640688ff2e5ddbc3580ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cad8e2d1fc9f39ac694eb701442407e5864e0cd861e562764f87ef6feade15e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73d195d92d504c6222bae2b8cf78aafdeace8fb015c2740b5a34bd2c51dee7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b57b917bf3c1c8df907001a6bc39c618c8bb377f5fed99cf20dc6000018db8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb54af93977051ada27c7721cde43ea72683698576a4b765d284be63d4e03520(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRulesMatchesQueryParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6a551235720588d6744a2f70fcdaf1db5000a907ce6cd79dad94ab10be3694(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c79a63fbea71ffa0a3972f22ea53bbda9c3b629e87eecd75207ca18d4efebf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesHttpRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa15e2d1c6c7dd841d207838068e4d749d73c744fa4a18a3ff9ef5cdb4c94f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c070be931c822d18c156be32535c90db010ecba050be578b64d9a23d5355e474(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4269ac72155c26a710b23773b4647ca5a3760059472b22addf4f93bfe26f8f4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6922d71cdfaa9834e86a0a0eb2b6d72142e52874eebc8329c10ed11ac6911337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c4d58d99c287368d45136cb1c88d656c03743e59ae0b50ea5e66b7cf0b60d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845775e23ea36f992e2a4b9ee23ba6ebf48623efa692741008bfbe3fabc2bc99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be810e601e19701f7dc29f598fa709637f8b4b4fcc4a38ee5182c174a9063c85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesHttpRouteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

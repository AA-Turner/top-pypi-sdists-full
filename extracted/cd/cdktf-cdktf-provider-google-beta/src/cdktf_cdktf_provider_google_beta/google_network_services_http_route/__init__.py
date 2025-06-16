r'''
# `google_network_services_http_route`

Refer to the Terraform Registry for docs: [`google_network_services_http_route`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route).
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


class GoogleNetworkServicesHttpRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route google_network_services_http_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hostnames: typing.Sequence[builtins.str],
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesHttpRouteRules", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route google_network_services_http_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hostnames: Set of hosts that should match against the HTTP host header to select a HttpRoute to process the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#hostnames GoogleNetworkServicesHttpRoute#hostnames}
        :param name: Name of the HttpRoute resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#name GoogleNetworkServicesHttpRoute#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#rules GoogleNetworkServicesHttpRoute#rules}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#description GoogleNetworkServicesHttpRoute#description}
        :param gateways: Gateways defines a list of gateways this HttpRoute is attached to, as one of the routing rules to route the requests served by the gateway. Each gateway reference should match the pattern: projects/* /locations/global/gateways/<gateway_name> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#gateways GoogleNetworkServicesHttpRoute#gateways} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#id GoogleNetworkServicesHttpRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the HttpRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#labels GoogleNetworkServicesHttpRoute#labels}
        :param meshes: Meshes defines a list of meshes this HttpRoute is attached to, as one of the routing rules to route the requests served by the mesh. Each mesh reference should match the pattern: projects/* /locations/global/meshes/<mesh_name>. The attached Mesh should be of a type SIDECAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#meshes GoogleNetworkServicesHttpRoute#meshes} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#project GoogleNetworkServicesHttpRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#timeouts GoogleNetworkServicesHttpRoute#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1ada8f0e59e0b22412f009f37576e14cf1891a3f205ff38303a7d9fe804ea8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleNetworkServicesHttpRouteConfig(
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
        '''Generates CDKTF code for importing a GoogleNetworkServicesHttpRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleNetworkServicesHttpRoute to import.
        :param import_from_id: The id of the existing GoogleNetworkServicesHttpRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleNetworkServicesHttpRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1179798df7526f035736b13f5856dd6c39fc034ee1ef1a9c5058f28a6123865d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesHttpRouteRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a279b8bbde934f34acebcc85652ed9385432e4884a4219debc8647a25672cab)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#create GoogleNetworkServicesHttpRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#delete GoogleNetworkServicesHttpRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#update GoogleNetworkServicesHttpRoute#update}.
        '''
        value = GoogleNetworkServicesHttpRouteTimeouts(
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
    def rules(self) -> "GoogleNetworkServicesHttpRouteRulesList":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesList", jsii.get(self, "rules"))

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
    def timeouts(self) -> "GoogleNetworkServicesHttpRouteTimeoutsOutputReference":
        return typing.cast("GoogleNetworkServicesHttpRouteTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesHttpRouteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleNetworkServicesHttpRouteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6665e433a48763dca5cb9546b16e0f247f3daf2485968ea024deb3c27d3a9aed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gateways")
    def gateways(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gateways"))

    @gateways.setter
    def gateways(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971273a21195f8e45b1e75c6a993832ab38da8b0f41122c2549d6164ceff1b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateways", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostnames")
    def hostnames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostnames"))

    @hostnames.setter
    def hostnames(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6af21428adce2efb4614b2c72093290419d6a25fb2a5217960c3772de54911b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2349595266fd1ed32bf8c180222f5347e807f3a82e353e653bbc9230c2e6dc9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__360a84fe36f53bf368bead6fb67b88211857cc39135e7c50fb74e237c56331c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshes")
    def meshes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "meshes"))

    @meshes.setter
    def meshes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a211463009688c0a21d6655efe44f001f789a1908d2798624ff3d5d5457af2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e4308c401768d1c1d900b70fa8c7f25b322cf41d67436b7e5c660a4dbb3a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a7ab82aaa2d036885dc2845e77b377e3712cf93250044d96874463a35be5c25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteConfig",
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
class GoogleNetworkServicesHttpRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesHttpRouteRules", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hostnames: Set of hosts that should match against the HTTP host header to select a HttpRoute to process the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#hostnames GoogleNetworkServicesHttpRoute#hostnames}
        :param name: Name of the HttpRoute resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#name GoogleNetworkServicesHttpRoute#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#rules GoogleNetworkServicesHttpRoute#rules}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#description GoogleNetworkServicesHttpRoute#description}
        :param gateways: Gateways defines a list of gateways this HttpRoute is attached to, as one of the routing rules to route the requests served by the gateway. Each gateway reference should match the pattern: projects/* /locations/global/gateways/<gateway_name> Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#gateways GoogleNetworkServicesHttpRoute#gateways} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#id GoogleNetworkServicesHttpRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the HttpRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#labels GoogleNetworkServicesHttpRoute#labels}
        :param meshes: Meshes defines a list of meshes this HttpRoute is attached to, as one of the routing rules to route the requests served by the mesh. Each mesh reference should match the pattern: projects/* /locations/global/meshes/<mesh_name>. The attached Mesh should be of a type SIDECAR. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#meshes GoogleNetworkServicesHttpRoute#meshes} Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#project GoogleNetworkServicesHttpRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#timeouts GoogleNetworkServicesHttpRoute#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GoogleNetworkServicesHttpRouteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2aca307d88ff7f04d271fbd4628adfb1115890547e3fea8f170d86998d20dc3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#hostnames GoogleNetworkServicesHttpRoute#hostnames}
        '''
        result = self._values.get("hostnames")
        assert result is not None, "Required property 'hostnames' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the HttpRoute resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#name GoogleNetworkServicesHttpRoute#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#rules GoogleNetworkServicesHttpRoute#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRules"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#description GoogleNetworkServicesHttpRoute#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateways(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Gateways defines a list of gateways this HttpRoute is attached to, as one of the routing rules to route the requests served by the gateway.

        Each gateway reference should match the pattern: projects/* /locations/global/gateways/<gateway_name>

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#gateways GoogleNetworkServicesHttpRoute#gateways}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("gateways")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#id GoogleNetworkServicesHttpRoute#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#labels GoogleNetworkServicesHttpRoute#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def meshes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Meshes defines a list of meshes this HttpRoute is attached to, as one of the routing rules to route the requests served by the mesh.

        Each mesh reference should match the pattern: projects/* /locations/global/meshes/<mesh_name>.
        The attached Mesh should be of a type SIDECAR.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#meshes GoogleNetworkServicesHttpRoute#meshes}

        Note: The above comment contained a comment block ending sequence (* followed by /). We have introduced a space between to prevent syntax errors. Please ignore the space.
        '''
        result = self._values.get("meshes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#project GoogleNetworkServicesHttpRoute#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GoogleNetworkServicesHttpRouteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#timeouts GoogleNetworkServicesHttpRoute#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRules",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "matches": "matches"},
)
class GoogleNetworkServicesHttpRouteRules:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesAction", typing.Dict[builtins.str, typing.Any]]] = None,
        matches: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesHttpRouteRulesMatches", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#action GoogleNetworkServicesHttpRoute#action}
        :param matches: matches block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#matches GoogleNetworkServicesHttpRoute#matches}
        '''
        if isinstance(action, dict):
            action = GoogleNetworkServicesHttpRouteRulesAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b6ab124cdef24af2d9543dab9fc5e4225e0d41382bf9a09b85c5ab355f8fcd)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument matches", value=matches, expected_type=type_hints["matches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if matches is not None:
            self._values["matches"] = matches

    @builtins.property
    def action(self) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#action GoogleNetworkServicesHttpRoute#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesAction"], result)

    @builtins.property
    def matches(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesMatches"]]]:
        '''matches block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#matches GoogleNetworkServicesHttpRoute#matches}
        '''
        result = self._values.get("matches")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesMatches"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesAction",
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
class GoogleNetworkServicesHttpRouteRulesAction:
    def __init__(
        self,
        *,
        cors_policy: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionCorsPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesHttpRouteRulesActionDestinations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fault_injection_policy: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        redirect: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionRedirect", typing.Dict[builtins.str, typing.Any]]] = None,
        request_header_modifier: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier", typing.Dict[builtins.str, typing.Any]]] = None,
        request_mirror_policy: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        response_header_modifier: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[builtins.str] = None,
        url_rewrite: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionUrlRewrite", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cors_policy: cors_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#cors_policy GoogleNetworkServicesHttpRoute#cors_policy}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#destinations GoogleNetworkServicesHttpRoute#destinations}
        :param fault_injection_policy: fault_injection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#fault_injection_policy GoogleNetworkServicesHttpRoute#fault_injection_policy}
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#redirect GoogleNetworkServicesHttpRoute#redirect}
        :param request_header_modifier: request_header_modifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#request_header_modifier GoogleNetworkServicesHttpRoute#request_header_modifier}
        :param request_mirror_policy: request_mirror_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#request_mirror_policy GoogleNetworkServicesHttpRoute#request_mirror_policy}
        :param response_header_modifier: response_header_modifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#response_header_modifier GoogleNetworkServicesHttpRoute#response_header_modifier}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#retry_policy GoogleNetworkServicesHttpRoute#retry_policy}
        :param timeout: Specifies the timeout for selected route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#timeout GoogleNetworkServicesHttpRoute#timeout}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#url_rewrite GoogleNetworkServicesHttpRoute#url_rewrite}
        '''
        if isinstance(cors_policy, dict):
            cors_policy = GoogleNetworkServicesHttpRouteRulesActionCorsPolicy(**cors_policy)
        if isinstance(fault_injection_policy, dict):
            fault_injection_policy = GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy(**fault_injection_policy)
        if isinstance(redirect, dict):
            redirect = GoogleNetworkServicesHttpRouteRulesActionRedirect(**redirect)
        if isinstance(request_header_modifier, dict):
            request_header_modifier = GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier(**request_header_modifier)
        if isinstance(request_mirror_policy, dict):
            request_mirror_policy = GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy(**request_mirror_policy)
        if isinstance(response_header_modifier, dict):
            response_header_modifier = GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier(**response_header_modifier)
        if isinstance(retry_policy, dict):
            retry_policy = GoogleNetworkServicesHttpRouteRulesActionRetryPolicy(**retry_policy)
        if isinstance(url_rewrite, dict):
            url_rewrite = GoogleNetworkServicesHttpRouteRulesActionUrlRewrite(**url_rewrite)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6645bb248d56ef305f57429e385092697a31d2cfb1a88c65ea84d32733da36c)
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
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionCorsPolicy"]:
        '''cors_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#cors_policy GoogleNetworkServicesHttpRoute#cors_policy}
        '''
        result = self._values.get("cors_policy")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionCorsPolicy"], result)

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesActionDestinations"]]]:
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#destinations GoogleNetworkServicesHttpRoute#destinations}
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesActionDestinations"]]], result)

    @builtins.property
    def fault_injection_policy(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy"]:
        '''fault_injection_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#fault_injection_policy GoogleNetworkServicesHttpRoute#fault_injection_policy}
        '''
        result = self._values.get("fault_injection_policy")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy"], result)

    @builtins.property
    def redirect(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRedirect"]:
        '''redirect block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#redirect GoogleNetworkServicesHttpRoute#redirect}
        '''
        result = self._values.get("redirect")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRedirect"], result)

    @builtins.property
    def request_header_modifier(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier"]:
        '''request_header_modifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#request_header_modifier GoogleNetworkServicesHttpRoute#request_header_modifier}
        '''
        result = self._values.get("request_header_modifier")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier"], result)

    @builtins.property
    def request_mirror_policy(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy"]:
        '''request_mirror_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#request_mirror_policy GoogleNetworkServicesHttpRoute#request_mirror_policy}
        '''
        result = self._values.get("request_mirror_policy")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy"], result)

    @builtins.property
    def response_header_modifier(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier"]:
        '''response_header_modifier block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#response_header_modifier GoogleNetworkServicesHttpRoute#response_header_modifier}
        '''
        result = self._values.get("response_header_modifier")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier"], result)

    @builtins.property
    def retry_policy(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#retry_policy GoogleNetworkServicesHttpRoute#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRetryPolicy"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Specifies the timeout for selected route.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#timeout GoogleNetworkServicesHttpRoute#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url_rewrite(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionUrlRewrite"]:
        '''url_rewrite block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#url_rewrite GoogleNetworkServicesHttpRoute#url_rewrite}
        '''
        result = self._values.get("url_rewrite")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionUrlRewrite"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionCorsPolicy",
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
class GoogleNetworkServicesHttpRouteRulesActionCorsPolicy:
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
        :param allow_credentials: In response to a preflight request, setting this to true indicates that the actual request can include user credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_credentials GoogleNetworkServicesHttpRoute#allow_credentials}
        :param allow_headers: Specifies the content for Access-Control-Allow-Headers header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_headers GoogleNetworkServicesHttpRoute#allow_headers}
        :param allow_methods: Specifies the content for Access-Control-Allow-Methods header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_methods GoogleNetworkServicesHttpRoute#allow_methods}
        :param allow_origin_regexes: Specifies the regular expression patterns that match allowed origins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_origin_regexes GoogleNetworkServicesHttpRoute#allow_origin_regexes}
        :param allow_origins: Specifies the list of origins that will be allowed to do CORS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_origins GoogleNetworkServicesHttpRoute#allow_origins}
        :param disabled: If true, the CORS policy is disabled. The default value is false, which indicates that the CORS policy is in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#disabled GoogleNetworkServicesHttpRoute#disabled}
        :param expose_headers: Specifies the content for Access-Control-Expose-Headers header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#expose_headers GoogleNetworkServicesHttpRoute#expose_headers}
        :param max_age: Specifies how long result of a preflight request can be cached in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#max_age GoogleNetworkServicesHttpRoute#max_age}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ece41eb137d3a6e39a7e2e05f66e3ae58aa1e372b9a003a1600512b61750725)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_credentials GoogleNetworkServicesHttpRoute#allow_credentials}
        '''
        result = self._values.get("allow_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for Access-Control-Allow-Headers header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_headers GoogleNetworkServicesHttpRoute#allow_headers}
        '''
        result = self._values.get("allow_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_methods(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for Access-Control-Allow-Methods header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_methods GoogleNetworkServicesHttpRoute#allow_methods}
        '''
        result = self._values.get("allow_methods")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_origin_regexes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the regular expression patterns that match allowed origins.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_origin_regexes GoogleNetworkServicesHttpRoute#allow_origin_regexes}
        '''
        result = self._values.get("allow_origin_regexes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allow_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of origins that will be allowed to do CORS requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_origins GoogleNetworkServicesHttpRoute#allow_origins}
        '''
        result = self._values.get("allow_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, the CORS policy is disabled.

        The default value is false, which indicates that the CORS policy is in effect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#disabled GoogleNetworkServicesHttpRoute#disabled}
        '''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def expose_headers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the content for Access-Control-Expose-Headers header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#expose_headers GoogleNetworkServicesHttpRoute#expose_headers}
        '''
        result = self._values.get("expose_headers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_age(self) -> typing.Optional[builtins.str]:
        '''Specifies how long result of a preflight request can be cached in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#max_age GoogleNetworkServicesHttpRoute#max_age}
        '''
        result = self._values.get("max_age")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionCorsPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionCorsPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionCorsPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbab113bd720f526b74a3b5d346ab6a7d8e150c8453024ffed69419b9c3f77c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65500fceba94ed6e1a330eae19192fc8628df2c902b72a5077aba27df9ff1ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowHeaders")
    def allow_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowHeaders"))

    @allow_headers.setter
    def allow_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aaa95af16fdb48b3b11480c3baa4b49aacf9d46132ac5a490917116e73d3cbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowMethods")
    def allow_methods(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowMethods"))

    @allow_methods.setter
    def allow_methods(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f42e7ad9c90b2043438c9929eb0e94d89c704fc48de2704be46d2a7b7a60fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowMethods", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowOriginRegexes")
    def allow_origin_regexes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowOriginRegexes"))

    @allow_origin_regexes.setter
    def allow_origin_regexes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3216e627c5a0485faf0662d8232f3116681374282c1c54bc780bfdeec040d53b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowOriginRegexes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowOrigins")
    def allow_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowOrigins"))

    @allow_origins.setter
    def allow_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107d99fbe1b7d871fad11d4920db7d9d30e10cc5001ffa43363256199e525d0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbbda47ac0396c98bed2241207864671bc644f32a24e337bd003dd6d19cdbdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="exposeHeaders")
    def expose_headers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "exposeHeaders"))

    @expose_headers.setter
    def expose_headers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2a1292630ad9b013e00714159b7fbed02adf382fed3bc58b8944bda0189b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exposeHeaders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxAge")
    def max_age(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxAge"))

    @max_age.setter
    def max_age(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7648dfe7cd15c21770c4de4f847027db23e331c565454b27b914b818148f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxAge", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionCorsPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionCorsPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionCorsPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edf049f2d1c3e3a70783edbb40a35b7d31e976771d3f665f686b96fa004d4462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionDestinations",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "weight": "weight"},
)
class GoogleNetworkServicesHttpRouteRulesActionDestinations:
    def __init__(
        self,
        *,
        service_name: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_name: The URL of a BackendService to route traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#service_name GoogleNetworkServicesHttpRoute#service_name}
        :param weight: Specifies the proportion of requests forwarded to the backend referenced by the serviceName field. This is computed as: weight/Sum(weights in this destination list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports. If only one serviceName is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend. If weights are specified for any one service name, they need to be specified for all of them. If weights are unspecified for all services, then, traffic is distributed in equal proportions to all of them. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#weight GoogleNetworkServicesHttpRoute#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c3690b223fa877a38a1f6c409037a01297e760e87ad9ec11950ffc15ffbee6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#service_name GoogleNetworkServicesHttpRoute#service_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#weight GoogleNetworkServicesHttpRoute#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionDestinationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionDestinationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa8fc734b4e04f6dc1a36e5564d214a64fba457e3d56a351c6d62d2785aa4799)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesHttpRouteRulesActionDestinationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19857a66d7fcf44e9f292af4622210a2a59b1b8946941ce67a46ba17a2cdc77)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesHttpRouteRulesActionDestinationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb0bd943af92103df3fdaa3100e7cf4f6b712dbeda080593078421f068a57876)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54b44a5504cc681ac4cedc0ad7e0930c2e914544408a9bab9f0b8a98e22451b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4c6d2e30c0906437c0eb3f363b6f8b86a0a0cf1c18ec8e2548f4da40c411cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesActionDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesActionDestinations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesActionDestinations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4dcd5b4909387d006186e76343797062f42f007099a302ba9906b9f56104b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesActionDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1da918991e956597cafdd1ecd825a61d198bae82f573467f64b83cbd4527c6a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa4346f2ae78ad1026f44960ab14bf79d0e8601f1a7b78055d91b6252ef95b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a37c837be0c562ca74e1c8593248a10f9cbb0d46921c3ca1c20916465958900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesActionDestinations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesActionDestinations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesActionDestinations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75712e6bd65442f5b3829bda16fcaead2a91fb67783f51576f2cf51e19aa175c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy",
    jsii_struct_bases=[],
    name_mapping={"abort": "abort", "delay": "delay"},
)
class GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy:
    def __init__(
        self,
        *,
        abort: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort", typing.Dict[builtins.str, typing.Any]]] = None,
        delay: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param abort: abort block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#abort GoogleNetworkServicesHttpRoute#abort}
        :param delay: delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#delay GoogleNetworkServicesHttpRoute#delay}
        '''
        if isinstance(abort, dict):
            abort = GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort(**abort)
        if isinstance(delay, dict):
            delay = GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay(**delay)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514e80f5e02d1e7839979a7d24f917d99d749af811ee5847c8f8124040ded2d0)
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
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort"]:
        '''abort block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#abort GoogleNetworkServicesHttpRoute#abort}
        '''
        result = self._values.get("abort")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort"], result)

    @builtins.property
    def delay(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay"]:
        '''delay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#delay GoogleNetworkServicesHttpRoute#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort",
    jsii_struct_bases=[],
    name_mapping={"http_status": "httpStatus", "percentage": "percentage"},
)
class GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort:
    def __init__(
        self,
        *,
        http_status: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_status: The HTTP status code used to abort the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#http_status GoogleNetworkServicesHttpRoute#http_status}
        :param percentage: The percentage of traffic which will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#percentage GoogleNetworkServicesHttpRoute#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a2ad22465ba905b05a8fa925347f4aa30d844bc23e3d451a673b2690baa8dc)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#http_status GoogleNetworkServicesHttpRoute#http_status}
        '''
        result = self._values.get("http_status")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic which will be aborted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#percentage GoogleNetworkServicesHttpRoute#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8e5b412097b6c008b1e2402ae905a0b22e38f21ca492147700872914a328a44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__581958fd1a1e8b248c1b576b599273dbdf4baf93f1ebe1bfca33404cdcdb8a2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03a02d045d35da4c1b2991683d422358a4fee506d93f211ca17d53b2e9cc1d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44baa4ebb1a8ddad7d2c3ea02a77bb01971ec3822bbef6b789b98edfb60fdbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay",
    jsii_struct_bases=[],
    name_mapping={"fixed_delay": "fixedDelay", "percentage": "percentage"},
)
class GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay:
    def __init__(
        self,
        *,
        fixed_delay: typing.Optional[builtins.str] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_delay: Specify a fixed delay before forwarding the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#fixed_delay GoogleNetworkServicesHttpRoute#fixed_delay}
        :param percentage: The percentage of traffic on which delay will be injected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#percentage GoogleNetworkServicesHttpRoute#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa7c226a9302d17a6446554dba863f5b834fa911e0befd0479636503eadaaea)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#fixed_delay GoogleNetworkServicesHttpRoute#fixed_delay}
        '''
        result = self._values.get("fixed_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic on which delay will be injected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#percentage GoogleNetworkServicesHttpRoute#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0621f89685a6cbf182310c2b8c9ba775e27ff8bdee1419fadf237926c58714d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6958010a13ade43ca5a46fdaf3cb390eae4a2bd4f633546d4c8323065c231d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__351fda843c72e6cf0aa2f14a14aa4a92e4df83d31652dea43691d48311e7a8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ce4cfa3f657bf15931be361aeafe58f715e7cd15dd977e5d5d042573ab19f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c858e070d0337aedec6db8506a82841631cbc5858b8c96a99078e5ac95e92678)
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
        :param http_status: The HTTP status code used to abort the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#http_status GoogleNetworkServicesHttpRoute#http_status}
        :param percentage: The percentage of traffic which will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#percentage GoogleNetworkServicesHttpRoute#percentage}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort(
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
        :param fixed_delay: Specify a fixed delay before forwarding the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#fixed_delay GoogleNetworkServicesHttpRoute#fixed_delay}
        :param percentage: The percentage of traffic on which delay will be injected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#percentage GoogleNetworkServicesHttpRoute#percentage}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay(
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
    ) -> GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference, jsii.get(self, "abort"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(
        self,
    ) -> GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference, jsii.get(self, "delay"))

    @builtins.property
    @jsii.member(jsii_name="abortInput")
    def abort_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort], jsii.get(self, "abortInput"))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d342d51b0b81bc0d4a23ce195557e3d98eb377c38ea3df3463b9db62f8e6fc9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__248b1e7821de95401979302646508dca38a31e9367b55a7280efa744729f4491)
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
        :param allow_credentials: In response to a preflight request, setting this to true indicates that the actual request can include user credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_credentials GoogleNetworkServicesHttpRoute#allow_credentials}
        :param allow_headers: Specifies the content for Access-Control-Allow-Headers header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_headers GoogleNetworkServicesHttpRoute#allow_headers}
        :param allow_methods: Specifies the content for Access-Control-Allow-Methods header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_methods GoogleNetworkServicesHttpRoute#allow_methods}
        :param allow_origin_regexes: Specifies the regular expression patterns that match allowed origins. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_origin_regexes GoogleNetworkServicesHttpRoute#allow_origin_regexes}
        :param allow_origins: Specifies the list of origins that will be allowed to do CORS requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#allow_origins GoogleNetworkServicesHttpRoute#allow_origins}
        :param disabled: If true, the CORS policy is disabled. The default value is false, which indicates that the CORS policy is in effect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#disabled GoogleNetworkServicesHttpRoute#disabled}
        :param expose_headers: Specifies the content for Access-Control-Expose-Headers header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#expose_headers GoogleNetworkServicesHttpRoute#expose_headers}
        :param max_age: Specifies how long result of a preflight request can be cached in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#max_age GoogleNetworkServicesHttpRoute#max_age}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionCorsPolicy(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5287bf7ef55b306dc834a41e0f38f3c789aa948e91adf70eeb2cc21000afd490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putFaultInjectionPolicy")
    def put_fault_injection_policy(
        self,
        *,
        abort: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort, typing.Dict[builtins.str, typing.Any]]] = None,
        delay: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param abort: abort block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#abort GoogleNetworkServicesHttpRoute#abort}
        :param delay: delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#delay GoogleNetworkServicesHttpRoute#delay}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy(
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
        :param host_redirect: The host that will be used in the redirect response instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#host_redirect GoogleNetworkServicesHttpRoute#host_redirect}
        :param https_redirect: If set to true, the URL scheme in the redirected request is set to https. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#https_redirect GoogleNetworkServicesHttpRoute#https_redirect}
        :param path_redirect: The path that will be used in the redirect response instead of the one that was supplied in the request. pathRedirect can not be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#path_redirect GoogleNetworkServicesHttpRoute#path_redirect}
        :param port_redirect: The port that will be used in the redirected request instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#port_redirect GoogleNetworkServicesHttpRoute#port_redirect}
        :param prefix_rewrite: Indicates that during redirection, the matched prefix (or path) should be swapped with this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#prefix_rewrite GoogleNetworkServicesHttpRoute#prefix_rewrite}
        :param response_code: The HTTP Status code to use for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#response_code GoogleNetworkServicesHttpRoute#response_code}
        :param strip_query: If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#strip_query GoogleNetworkServicesHttpRoute#strip_query}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionRedirect(
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
        :param add: Add the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#add GoogleNetworkServicesHttpRoute#add}
        :param remove: Remove headers (matching by header names) specified in the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#remove GoogleNetworkServicesHttpRoute#remove}
        :param set: Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#set GoogleNetworkServicesHttpRoute#set}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier(
            add=add, remove=remove, set=set
        )

        return typing.cast(None, jsii.invoke(self, "putRequestHeaderModifier", [value]))

    @jsii.member(jsii_name="putRequestMirrorPolicy")
    def put_request_mirror_policy(
        self,
        *,
        destination: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#destination GoogleNetworkServicesHttpRoute#destination}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy(
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
        :param add: Add the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#add GoogleNetworkServicesHttpRoute#add}
        :param remove: Remove headers (matching by header names) specified in the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#remove GoogleNetworkServicesHttpRoute#remove}
        :param set: Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#set GoogleNetworkServicesHttpRoute#set}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier(
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
        :param num_retries: Specifies the allowed number of retries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#num_retries GoogleNetworkServicesHttpRoute#num_retries}
        :param per_try_timeout: Specifies a non-zero timeout per retry attempt. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#per_try_timeout GoogleNetworkServicesHttpRoute#per_try_timeout}
        :param retry_conditions: Specifies one or more conditions when this retry policy applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#retry_conditions GoogleNetworkServicesHttpRoute#retry_conditions}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionRetryPolicy(
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
        :param host_rewrite: Prior to forwarding the request to the selected destination, the requests host header is replaced by this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#host_rewrite GoogleNetworkServicesHttpRoute#host_rewrite}
        :param path_prefix_rewrite: Prior to forwarding the request to the selected destination, the matching portion of the requests path is replaced by this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#path_prefix_rewrite GoogleNetworkServicesHttpRoute#path_prefix_rewrite}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionUrlRewrite(
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
    ) -> GoogleNetworkServicesHttpRouteRulesActionCorsPolicyOutputReference:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesActionCorsPolicyOutputReference, jsii.get(self, "corsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> GoogleNetworkServicesHttpRouteRulesActionDestinationsList:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesActionDestinationsList, jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="faultInjectionPolicy")
    def fault_injection_policy(
        self,
    ) -> GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference, jsii.get(self, "faultInjectionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="redirect")
    def redirect(
        self,
    ) -> "GoogleNetworkServicesHttpRouteRulesActionRedirectOutputReference":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesActionRedirectOutputReference", jsii.get(self, "redirect"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderModifier")
    def request_header_modifier(
        self,
    ) -> "GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference", jsii.get(self, "requestHeaderModifier"))

    @builtins.property
    @jsii.member(jsii_name="requestMirrorPolicy")
    def request_mirror_policy(
        self,
    ) -> "GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference", jsii.get(self, "requestMirrorPolicy"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderModifier")
    def response_header_modifier(
        self,
    ) -> "GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference", jsii.get(self, "responseHeaderModifier"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(
        self,
    ) -> "GoogleNetworkServicesHttpRouteRulesActionRetryPolicyOutputReference":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesActionRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="urlRewrite")
    def url_rewrite(
        self,
    ) -> "GoogleNetworkServicesHttpRouteRulesActionUrlRewriteOutputReference":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesActionUrlRewriteOutputReference", jsii.get(self, "urlRewrite"))

    @builtins.property
    @jsii.member(jsii_name="corsPolicyInput")
    def cors_policy_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionCorsPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionCorsPolicy], jsii.get(self, "corsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesActionDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesActionDestinations]]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="faultInjectionPolicyInput")
    def fault_injection_policy_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy], jsii.get(self, "faultInjectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectInput")
    def redirect_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRedirect"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRedirect"], jsii.get(self, "redirectInput"))

    @builtins.property
    @jsii.member(jsii_name="requestHeaderModifierInput")
    def request_header_modifier_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier"], jsii.get(self, "requestHeaderModifierInput"))

    @builtins.property
    @jsii.member(jsii_name="requestMirrorPolicyInput")
    def request_mirror_policy_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy"], jsii.get(self, "requestMirrorPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="responseHeaderModifierInput")
    def response_header_modifier_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier"], jsii.get(self, "responseHeaderModifierInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRetryPolicy"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="urlRewriteInput")
    def url_rewrite_input(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionUrlRewrite"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionUrlRewrite"], jsii.get(self, "urlRewriteInput"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9dcf59e57677e141268e11d8b20ef1af816a446ea93debfdda879cc2e90f224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesAction]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a583f3b97bd35a1c80c0811c8f9eafeead1f8cac122a97ece68ec5f792548ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRedirect",
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
class GoogleNetworkServicesHttpRouteRulesActionRedirect:
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
        :param host_redirect: The host that will be used in the redirect response instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#host_redirect GoogleNetworkServicesHttpRoute#host_redirect}
        :param https_redirect: If set to true, the URL scheme in the redirected request is set to https. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#https_redirect GoogleNetworkServicesHttpRoute#https_redirect}
        :param path_redirect: The path that will be used in the redirect response instead of the one that was supplied in the request. pathRedirect can not be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#path_redirect GoogleNetworkServicesHttpRoute#path_redirect}
        :param port_redirect: The port that will be used in the redirected request instead of the one that was supplied in the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#port_redirect GoogleNetworkServicesHttpRoute#port_redirect}
        :param prefix_rewrite: Indicates that during redirection, the matched prefix (or path) should be swapped with this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#prefix_rewrite GoogleNetworkServicesHttpRoute#prefix_rewrite}
        :param response_code: The HTTP Status code to use for the redirect. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#response_code GoogleNetworkServicesHttpRoute#response_code}
        :param strip_query: If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#strip_query GoogleNetworkServicesHttpRoute#strip_query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca52603c6f42a6773806d0476124b0d53075e65dbe6fc92474f9c620a3890c7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#host_redirect GoogleNetworkServicesHttpRoute#host_redirect}
        '''
        result = self._values.get("host_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_redirect(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, the URL scheme in the redirected request is set to https.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#https_redirect GoogleNetworkServicesHttpRoute#https_redirect}
        '''
        result = self._values.get("https_redirect")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def path_redirect(self) -> typing.Optional[builtins.str]:
        '''The path that will be used in the redirect response instead of the one that was supplied in the request.

        pathRedirect can not be supplied together with prefixRedirect. Supply one alone or neither. If neither is supplied, the path of the original request will be used for the redirect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#path_redirect GoogleNetworkServicesHttpRoute#path_redirect}
        '''
        result = self._values.get("path_redirect")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port_redirect(self) -> typing.Optional[jsii.Number]:
        '''The port that will be used in the redirected request instead of the one that was supplied in the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#port_redirect GoogleNetworkServicesHttpRoute#port_redirect}
        '''
        result = self._values.get("port_redirect")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prefix_rewrite(self) -> typing.Optional[builtins.str]:
        '''Indicates that during redirection, the matched prefix (or path) should be swapped with this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#prefix_rewrite GoogleNetworkServicesHttpRoute#prefix_rewrite}
        '''
        result = self._values.get("prefix_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_code(self) -> typing.Optional[builtins.str]:
        '''The HTTP Status code to use for the redirect.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#response_code GoogleNetworkServicesHttpRoute#response_code}
        '''
        result = self._values.get("response_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strip_query(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If set to true, any accompanying query portion of the original URL is removed prior to redirecting the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#strip_query GoogleNetworkServicesHttpRoute#strip_query}
        '''
        result = self._values.get("strip_query")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__563853dfc208d1f06be513d8304c7cbdbadb866f28770fdbb70450f9684feb62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f578c9f70d034b85fecf9ccd15a2d2d26ff3d29aadd5d32c6e19294cb44ec157)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36a343e63b2845546659419aebba5e159b4fb691f403d8a5973ab6d198ba3936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathRedirect")
    def path_redirect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathRedirect"))

    @path_redirect.setter
    def path_redirect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b3ae197a5b66bacaeef1689069e37978d9b08358d8a2db41b5516a5471c9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portRedirect")
    def port_redirect(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "portRedirect"))

    @port_redirect.setter
    def port_redirect(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976a7026b1034a1a4898211229e037681f79e738f7becf662c92497be2ad82fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portRedirect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixRewrite")
    def prefix_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixRewrite"))

    @prefix_rewrite.setter
    def prefix_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa8b07b2c72b6d5a467421082198ed2325c0e3f3560fd869926900c22b0085a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responseCode")
    def response_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseCode"))

    @response_code.setter
    def response_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9c90eea284d73f9cb4e8f48711ea07dcdb774d4ffff70163d69e857535e231)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6721926f17e0a527249a13fdd01a30476a85674f88670f6d166b9cc3111ef88b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stripQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRedirect]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRedirect], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRedirect],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3c9ada1d62c9c587247a46cc9f44cece37b918cf5d53cb207d091704f1d72bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier",
    jsii_struct_bases=[],
    name_mapping={"add": "add", "remove": "remove", "set": "set"},
)
class GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier:
    def __init__(
        self,
        *,
        add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param add: Add the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#add GoogleNetworkServicesHttpRoute#add}
        :param remove: Remove headers (matching by header names) specified in the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#remove GoogleNetworkServicesHttpRoute#remove}
        :param set: Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#set GoogleNetworkServicesHttpRoute#set}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d57648f79c585bfee045d1ccd858358f505a49585d5e830cd0dd6032bedca1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#add GoogleNetworkServicesHttpRoute#add}
        '''
        result = self._values.get("add")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def remove(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Remove headers (matching by header names) specified in the list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#remove GoogleNetworkServicesHttpRoute#remove}
        '''
        result = self._values.get("remove")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def set(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#set GoogleNetworkServicesHttpRoute#set}
        '''
        result = self._values.get("set")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__993ca6857d34205da98319fb5e24bfe8fb7c944783e16e4d6a7929db66d97f2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__270c162ad412abc5bd17461cb9f35d03060953f0caad0fc2bb21613d3422c4db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "add", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remove")
    def remove(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remove"))

    @remove.setter
    def remove(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6227776d179754e23a373d85539067257fab21a5a001d56ac1e5e25b7ebea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remove", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "set"))

    @set.setter
    def set(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03276e5d11b81de836805071d9580aec7ed24673c44cdf84dc68c1273c2ca2fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "set", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b398fbc7f2fd586ee430b084108ba82ec9c83929b458f02288b2b827919e1866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination"},
)
class GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy:
    def __init__(
        self,
        *,
        destination: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param destination: destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#destination GoogleNetworkServicesHttpRoute#destination}
        '''
        if isinstance(destination, dict):
            destination = GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination(**destination)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e9e8d3c24fcbecb5d76bb76e2c1ede270c31002a2c281ed53aa16c57cf704f)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination"]:
        '''destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#destination GoogleNetworkServicesHttpRoute#destination}
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "weight": "weight"},
)
class GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination:
    def __init__(
        self,
        *,
        service_name: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_name: The URL of a BackendService to route traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#service_name GoogleNetworkServicesHttpRoute#service_name}
        :param weight: Specifies the proportion of requests forwarded to the backend referenced by the serviceName field. This is computed as: weight/Sum(weights in this destination list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports. If only one serviceName is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend. If weights are specified for any one service name, they need to be specified for all of them. If weights are unspecified for all services, then, traffic is distributed in equal proportions to all of them. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#weight GoogleNetworkServicesHttpRoute#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4882ba70501a32eb58401b78f7025e7f88270dd7d39735f110dd361ccdafee43)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#service_name GoogleNetworkServicesHttpRoute#service_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#weight GoogleNetworkServicesHttpRoute#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a4aaad078cb538f2d6ab0add2c30011b5ec899bfcc1f92f07f47089150e7ea1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1b62c1ed7ebba85904aa781b8bf046013021432f1bffb0686b7bf82568193a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebd702703d307d28c1cde84b4fb2a0096749f426c1244179d57f2b380c68bed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76abeeca5fd5d62dd3298f1a3f44ca99da10b0ad3e5f15489808e77e1cbf4856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6fc5a21f998d455ed546146a81621eb68f2eefd23a519e262759f087c6fd64b)
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
        :param service_name: The URL of a BackendService to route traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#service_name GoogleNetworkServicesHttpRoute#service_name}
        :param weight: Specifies the proportion of requests forwarded to the backend referenced by the serviceName field. This is computed as: weight/Sum(weights in this destination list). For non-zero values, there may be some epsilon from the exact proportion defined here depending on the precision an implementation supports. If only one serviceName is specified and it has a weight greater than 0, 100% of the traffic is forwarded to that backend. If weights are specified for any one service name, they need to be specified for all of them. If weights are unspecified for all services, then, traffic is distributed in equal proportions to all of them. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#weight GoogleNetworkServicesHttpRoute#weight}
        '''
        value = GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination(
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
    ) -> GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="destinationInput")
    def destination_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination], jsii.get(self, "destinationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2164a1dde40ac1e2d685a97bfa6e5c5a3346db62269744e43152ca044ad77a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier",
    jsii_struct_bases=[],
    name_mapping={"add": "add", "remove": "remove", "set": "set"},
)
class GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier:
    def __init__(
        self,
        *,
        add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param add: Add the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#add GoogleNetworkServicesHttpRoute#add}
        :param remove: Remove headers (matching by header names) specified in the list. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#remove GoogleNetworkServicesHttpRoute#remove}
        :param set: Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#set GoogleNetworkServicesHttpRoute#set}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d893f8186cf93278996d2ae76b564a19824a99eca77ab053df3b973d94ddd7e8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#add GoogleNetworkServicesHttpRoute#add}
        '''
        result = self._values.get("add")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def remove(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Remove headers (matching by header names) specified in the list.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#remove GoogleNetworkServicesHttpRoute#remove}
        '''
        result = self._values.get("remove")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def set(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Completely overwrite/replace the headers with given map where key is the name of the header, value is the value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#set GoogleNetworkServicesHttpRoute#set}
        '''
        result = self._values.get("set")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6a7308c7a8dd55e2e61b675d40876e312495a8a89d4b553fb4a6444a32b3645)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a625fa176ae5537544c8f7f3c733352d271a3b7c9c01208b8447b5223c73f257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "add", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remove")
    def remove(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remove"))

    @remove.setter
    def remove(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cce15c77641ba24582646d6f2ebbf8826e4996d5bf9429e5b50fbd3e13f100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remove", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "set"))

    @set.setter
    def set(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967b3b2e70edb7d2b44ff5c61cf184d0a6cdbc1cdcee676573ed9cc2be401ed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "set", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e2fe104a09ce6ed09af81327ad2ee40d2d8a80f5a358380c5aeb162fbb0396b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "num_retries": "numRetries",
        "per_try_timeout": "perTryTimeout",
        "retry_conditions": "retryConditions",
    },
)
class GoogleNetworkServicesHttpRouteRulesActionRetryPolicy:
    def __init__(
        self,
        *,
        num_retries: typing.Optional[jsii.Number] = None,
        per_try_timeout: typing.Optional[builtins.str] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param num_retries: Specifies the allowed number of retries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#num_retries GoogleNetworkServicesHttpRoute#num_retries}
        :param per_try_timeout: Specifies a non-zero timeout per retry attempt. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#per_try_timeout GoogleNetworkServicesHttpRoute#per_try_timeout}
        :param retry_conditions: Specifies one or more conditions when this retry policy applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#retry_conditions GoogleNetworkServicesHttpRoute#retry_conditions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f97ec1bd7eaadb0933c01bf9d78c9843041f83f31e73cfc2609622e006c1b1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#num_retries GoogleNetworkServicesHttpRoute#num_retries}
        '''
        result = self._values.get("num_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def per_try_timeout(self) -> typing.Optional[builtins.str]:
        '''Specifies a non-zero timeout per retry attempt.

        A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#per_try_timeout GoogleNetworkServicesHttpRoute#per_try_timeout}
        '''
        result = self._values.get("per_try_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retry_conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies one or more conditions when this retry policy applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#retry_conditions GoogleNetworkServicesHttpRoute#retry_conditions}
        '''
        result = self._values.get("retry_conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c75a5ae845569747ee7ecd76dc6f0943baae6ba41c9508d43215a6ca44eefb71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__433c3cd064ce096f08be891517ca9f3abf03da128d2a0544cc136dfd7400de96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="perTryTimeout")
    def per_try_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "perTryTimeout"))

    @per_try_timeout.setter
    def per_try_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfff189b67b281386782c7727fef99db1d43232b4a5e7b19b7a836e69bef6856)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "perTryTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryConditions")
    def retry_conditions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "retryConditions"))

    @retry_conditions.setter
    def retry_conditions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acdfd76605d03b319c48e27066b8a54747112912c15afcbe88597a9d472a918f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryConditions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRetryPolicy]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__597a9d48a2dc3adbc36917609e8fba4458e4e4154c6e6f3b12ace2c3710cb078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionUrlRewrite",
    jsii_struct_bases=[],
    name_mapping={
        "host_rewrite": "hostRewrite",
        "path_prefix_rewrite": "pathPrefixRewrite",
    },
)
class GoogleNetworkServicesHttpRouteRulesActionUrlRewrite:
    def __init__(
        self,
        *,
        host_rewrite: typing.Optional[builtins.str] = None,
        path_prefix_rewrite: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param host_rewrite: Prior to forwarding the request to the selected destination, the requests host header is replaced by this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#host_rewrite GoogleNetworkServicesHttpRoute#host_rewrite}
        :param path_prefix_rewrite: Prior to forwarding the request to the selected destination, the matching portion of the requests path is replaced by this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#path_prefix_rewrite GoogleNetworkServicesHttpRoute#path_prefix_rewrite}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c69b2e5f5c999a7ae5e71e3dc909b11731ea2c77124b917fb908bcb6022fb4b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#host_rewrite GoogleNetworkServicesHttpRoute#host_rewrite}
        '''
        result = self._values.get("host_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_prefix_rewrite(self) -> typing.Optional[builtins.str]:
        '''Prior to forwarding the request to the selected destination, the matching portion of the requests path is replaced by this value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#path_prefix_rewrite GoogleNetworkServicesHttpRoute#path_prefix_rewrite}
        '''
        result = self._values.get("path_prefix_rewrite")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesActionUrlRewrite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesActionUrlRewriteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesActionUrlRewriteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__420cd6af91a88914c58517814cc4d89b62053088db6c5ab202e74ab5507983fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8682f63bac2d39f7b92df0d343c3b035533f5d148ff6e86de98379e59d7dcca1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathPrefixRewrite")
    def path_prefix_rewrite(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathPrefixRewrite"))

    @path_prefix_rewrite.setter
    def path_prefix_rewrite(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9297e8e54bf8bac611202b365fd14ae1a48b77f0787f17491175966119bbfacc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathPrefixRewrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesActionUrlRewrite]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesActionUrlRewrite], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionUrlRewrite],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7298b1a16967bc750c4ef5d50c5cc3bd455cab5b6c37757320a569a5318cf58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41271cd0aa25691d135e3a6d250e52c1b48a0a48051f5355ab179ff441193ef4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesHttpRouteRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86fccca34aa6c4ffc3c3ca1d68be51979959d97278e5ee7513888a31ded46bc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesHttpRouteRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a2025472fb98881614336f2eec29c3b44ba8d5cf123d6d1def472c688d989e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12459c9348afd05c3b0d03c8d241e780aff87dd6a4e2b88facb92fe620766430)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b406b5d188d851263652f2bad49ba9a5fa1cb3898da9a0e9d61316726537ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9cacccac2857fae3cfd4220dea39f532504c993cd5ef257d3e9e115b5ef0b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatches",
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
class GoogleNetworkServicesHttpRouteRulesMatches:
    def __init__(
        self,
        *,
        full_path_match: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesHttpRouteRulesMatchesHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix_match: typing.Optional[builtins.str] = None,
        query_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        regex_match: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param full_path_match: The HTTP request path value should exactly match this value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#full_path_match GoogleNetworkServicesHttpRoute#full_path_match}
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#headers GoogleNetworkServicesHttpRoute#headers}
        :param ignore_case: Specifies if prefixMatch and fullPathMatch matches are case sensitive. The default value is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#ignore_case GoogleNetworkServicesHttpRoute#ignore_case}
        :param prefix_match: The HTTP request path value must begin with specified prefixMatch. prefixMatch must begin with a /. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#prefix_match GoogleNetworkServicesHttpRoute#prefix_match}
        :param query_parameters: query_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#query_parameters GoogleNetworkServicesHttpRoute#query_parameters}
        :param regex_match: The HTTP request path value must satisfy the regular expression specified by regexMatch after removing any query parameters and anchor supplied with the original URL. For regular expression grammar, please see https://github.com/google/re2/wiki/Syntax Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#regex_match GoogleNetworkServicesHttpRoute#regex_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4ef0821fab685a5f1ab4f0769e11b5c2b7e5a273ce7eb1c45ef9e805080a39a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#full_path_match GoogleNetworkServicesHttpRoute#full_path_match}
        '''
        result = self._values.get("full_path_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesMatchesHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#headers GoogleNetworkServicesHttpRoute#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesMatchesHeaders"]]], result)

    @builtins.property
    def ignore_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if prefixMatch and fullPathMatch matches are case sensitive. The default value is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#ignore_case GoogleNetworkServicesHttpRoute#ignore_case}
        '''
        result = self._values.get("ignore_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[builtins.str]:
        '''The HTTP request path value must begin with specified prefixMatch. prefixMatch must begin with a /.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#prefix_match GoogleNetworkServicesHttpRoute#prefix_match}
        '''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters"]]]:
        '''query_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#query_parameters GoogleNetworkServicesHttpRoute#query_parameters}
        '''
        result = self._values.get("query_parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters"]]], result)

    @builtins.property
    def regex_match(self) -> typing.Optional[builtins.str]:
        '''The HTTP request path value must satisfy the regular expression specified by regexMatch after removing any query parameters and anchor supplied with the original URL.

        For regular expression grammar, please see https://github.com/google/re2/wiki/Syntax

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#regex_match GoogleNetworkServicesHttpRoute#regex_match}
        '''
        result = self._values.get("regex_match")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesMatches(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesHeaders",
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
class GoogleNetworkServicesHttpRouteRulesMatchesHeaders:
    def __init__(
        self,
        *,
        exact_match: typing.Optional[builtins.str] = None,
        header: typing.Optional[builtins.str] = None,
        invert_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prefix_match: typing.Optional[builtins.str] = None,
        present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        range_match: typing.Optional[typing.Union["GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch", typing.Dict[builtins.str, typing.Any]]] = None,
        regex_match: typing.Optional[builtins.str] = None,
        suffix_match: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact_match: The value of the header should match exactly the content of exactMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#exact_match GoogleNetworkServicesHttpRoute#exact_match}
        :param header: The name of the HTTP header to match against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#header GoogleNetworkServicesHttpRoute#header}
        :param invert_match: If specified, the match result will be inverted before checking. Default value is set to false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#invert_match GoogleNetworkServicesHttpRoute#invert_match}
        :param prefix_match: The value of the header must start with the contents of prefixMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#prefix_match GoogleNetworkServicesHttpRoute#prefix_match}
        :param present_match: A header with headerName must exist. The match takes place whether or not the header has a value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#present_match GoogleNetworkServicesHttpRoute#present_match}
        :param range_match: range_match block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#range_match GoogleNetworkServicesHttpRoute#range_match}
        :param regex_match: The value of the header must match the regular expression specified in regexMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#regex_match GoogleNetworkServicesHttpRoute#regex_match}
        :param suffix_match: The value of the header must end with the contents of suffixMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#suffix_match GoogleNetworkServicesHttpRoute#suffix_match}
        '''
        if isinstance(range_match, dict):
            range_match = GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch(**range_match)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c9b9fc3af48078d5f870b9dda49bb0a883d186b54be8c4e37c2ac598114307)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#exact_match GoogleNetworkServicesHttpRoute#exact_match}
        '''
        result = self._values.get("exact_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def header(self) -> typing.Optional[builtins.str]:
        '''The name of the HTTP header to match against.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#header GoogleNetworkServicesHttpRoute#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def invert_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If specified, the match result will be inverted before checking. Default value is set to false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#invert_match GoogleNetworkServicesHttpRoute#invert_match}
        '''
        result = self._values.get("invert_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prefix_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must start with the contents of prefixMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#prefix_match GoogleNetworkServicesHttpRoute#prefix_match}
        '''
        result = self._values.get("prefix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def present_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A header with headerName must exist. The match takes place whether or not the header has a value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#present_match GoogleNetworkServicesHttpRoute#present_match}
        '''
        result = self._values.get("present_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def range_match(
        self,
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch"]:
        '''range_match block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#range_match GoogleNetworkServicesHttpRoute#range_match}
        '''
        result = self._values.get("range_match")
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch"], result)

    @builtins.property
    def regex_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must match the regular expression specified in regexMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#regex_match GoogleNetworkServicesHttpRoute#regex_match}
        '''
        result = self._values.get("regex_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suffix_match(self) -> typing.Optional[builtins.str]:
        '''The value of the header must end with the contents of suffixMatch.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#suffix_match GoogleNetworkServicesHttpRoute#suffix_match}
        '''
        result = self._values.get("suffix_match")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesMatchesHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesMatchesHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b02e0b326c6a6a288ff57873443c952a5d2e44dc590f3dbbc21057352c865a2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesHttpRouteRulesMatchesHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74b92d95ee54591828ceb59d9cdbb35fe856151aac4fb693a71126e9285cd4b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesHttpRouteRulesMatchesHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c21da82b01260cec883fbea0f6ee7beb364083bb13e524df7a20e579a1c41df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd0f3fff76b0f273eaeb97ba40ef9816ee962aab0c9c4c03a97ad2d9ee0d5da5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdcdd659fc466f10a47efb67867afc56bc588132005831dfed96a32ea2a9b07d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d4557e1a5fcff2f57ce7f7321abf6d34be87857dbc6acf857c8e8e27669f1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesMatchesHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce935c0ed8d44a06c5ffd5fc27d943cb2fee30a80e6d92bfd08f72e5c80a1eb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRangeMatch")
    def put_range_match(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: End of the range (exclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#end GoogleNetworkServicesHttpRoute#end}
        :param start: Start of the range (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#start GoogleNetworkServicesHttpRoute#start}
        '''
        value = GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch(
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
    ) -> "GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference", jsii.get(self, "rangeMatch"))

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
    ) -> typing.Optional["GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch"]:
        return typing.cast(typing.Optional["GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch"], jsii.get(self, "rangeMatchInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__424892b7d08377d7148f8d9fda67c93fbd6c0306b181817f4592518d442ee623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exactMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e80e692a857681034d14ba96ce33a1d5600ca4d1650fa63735e954114f0e4c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb7eb3eeaa66955a670b35c13ef5bea2a35abd2407d297c644fbdb84b95dcb43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invertMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be475406584c1bd434fe601682996c4e0e586bad88452300f19bb2866fbf2ff3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5e65065152e7527f3052ba98267b20ec138398c35a403683e77e96c7ced268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regexMatch")
    def regex_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regexMatch"))

    @regex_match.setter
    def regex_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e785e1fc1a1e56b1f0cb247133418d333959014f050adb373c464a63764ac99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suffixMatch")
    def suffix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "suffixMatch"))

    @suffix_match.setter
    def suffix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21329efcbf66e7ae888b7ebd9a6d14110dd0291599161c03fbee47f00a65e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suffixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatchesHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatchesHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatchesHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b86c4fec9d3da12c0d663cf216415be17aaafdb9ae08919ddff65cbaa3cbc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch",
    jsii_struct_bases=[],
    name_mapping={"end": "end", "start": "start"},
)
class GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch:
    def __init__(self, *, end: jsii.Number, start: jsii.Number) -> None:
        '''
        :param end: End of the range (exclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#end GoogleNetworkServicesHttpRoute#end}
        :param start: Start of the range (inclusive). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#start GoogleNetworkServicesHttpRoute#start}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6678ff5417c758f633f7975be28399fa7a956744ce8a6b0c9e929000aa3a79)
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end": end,
            "start": start,
        }

    @builtins.property
    def end(self) -> jsii.Number:
        '''End of the range (exclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#end GoogleNetworkServicesHttpRoute#end}
        '''
        result = self._values.get("end")
        assert result is not None, "Required property 'end' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start(self) -> jsii.Number:
        '''Start of the range (inclusive).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#start GoogleNetworkServicesHttpRoute#start}
        '''
        result = self._values.get("start")
        assert result is not None, "Required property 'start' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57932cb6c61d2550285275ec3049008ae3c8330634c1b5dd5d30b2ce6924ed00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f42e4a8883a921caa696f8d8c9170c9a91135317ae5255e5161ddc4a9d191707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "end", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb98832dcc6adf444ef9e2378de1d02c8202b368c3b6e57154c8419f6fba293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821f8f47847c537bb1c1e80b8e0c1121e9eb0154a4d90e56914f23ec59f2173b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesMatchesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b31193dca3b4c84922d4b1fd13b96f24033808b2960ed86cef4ae5abe7950472)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesHttpRouteRulesMatchesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a109732f35aa21d660a4c0aa4cb4754ae253f874914b7b208b0c8862c1be9f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesHttpRouteRulesMatchesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d3825f89e10f009eeed85cddfc0937a5d999d41b094f8e2e75efd788373d54c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5116521e2b7c26d242c19dcc426342cc4ede0dc10df323e6e39a2d72473dfddd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ec061895566a7e80a5ec0ea9947f77f696b81047335e4a19df6dc4018e23c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatches]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatches]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatches]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c061066c38af16403be5bad9b5fcad60929ee3e82fa5441ca2ca9a446902ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesMatchesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3167ab93daaa3b3735ffb79535355ca5d452f06164b881d1a5cdcf72f76ebf48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df8e55e9cf4b3f664b538998a6de4d94400371ad82b7788e1aa9e90b423d24e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putQueryParameters")
    def put_query_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76fa274308a98b8448a8943dec054bede8249a1fa3c9ee39117bff55c20fb073)
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
    def headers(self) -> GoogleNetworkServicesHttpRouteRulesMatchesHeadersList:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesMatchesHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="queryParameters")
    def query_parameters(
        self,
    ) -> "GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersList":
        return typing.cast("GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersList", jsii.get(self, "queryParameters"))

    @builtins.property
    @jsii.member(jsii_name="fullPathMatchInput")
    def full_path_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fullPathMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesHeaders]]], jsii.get(self, "headersInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters"]]], jsii.get(self, "queryParametersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b7fa52a408f3017fb6173dfe840c1e88e8b8642fc2abf05583e24df33b070d83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7d9a70940348828dc4d492cedb19d9098f431ac8462ce91ac2a4c8542cf5c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreCase", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="prefixMatch")
    def prefix_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefixMatch"))

    @prefix_match.setter
    def prefix_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5609a338f97cb780d1d46ccb0f5ae21883f267617eb28797a2b6cdc227e4ec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefixMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regexMatch")
    def regex_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regexMatch"))

    @regex_match.setter
    def regex_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4dc0f121d4823ba3c2a33e18105ab5b46359882036df3b2e5abb442e21186c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatches]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatches]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatches]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f5a80966dd2b996b67c78a1fe9807f1b3c683ed04e633202e4c512fed30c0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters",
    jsii_struct_bases=[],
    name_mapping={
        "exact_match": "exactMatch",
        "present_match": "presentMatch",
        "query_parameter": "queryParameter",
        "regex_match": "regexMatch",
    },
)
class GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters:
    def __init__(
        self,
        *,
        exact_match: typing.Optional[builtins.str] = None,
        present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_parameter: typing.Optional[builtins.str] = None,
        regex_match: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exact_match: The value of the query parameter must exactly match the contents of exactMatch. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#exact_match GoogleNetworkServicesHttpRoute#exact_match}
        :param present_match: Specifies that the QueryParameterMatcher matches if request contains query parameter, irrespective of whether the parameter has a value or not. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#present_match GoogleNetworkServicesHttpRoute#present_match}
        :param query_parameter: The name of the query parameter to match. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#query_parameter GoogleNetworkServicesHttpRoute#query_parameter}
        :param regex_match: The value of the query parameter must match the regular expression specified by regexMatch.For regular expression grammar, please see https://github.com/google/re2/wiki/Syntax. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#regex_match GoogleNetworkServicesHttpRoute#regex_match}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d9a826cb897909433a389e4e7712d38ecb3042804bd67c6b8495adbdd6b27c2)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#exact_match GoogleNetworkServicesHttpRoute#exact_match}
        '''
        result = self._values.get("exact_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def present_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that the QueryParameterMatcher matches if request contains query parameter, irrespective of whether the parameter has a value or not.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#present_match GoogleNetworkServicesHttpRoute#present_match}
        '''
        result = self._values.get("present_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_parameter(self) -> typing.Optional[builtins.str]:
        '''The name of the query parameter to match.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#query_parameter GoogleNetworkServicesHttpRoute#query_parameter}
        '''
        result = self._values.get("query_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def regex_match(self) -> typing.Optional[builtins.str]:
        '''The value of the query parameter must match the regular expression specified by regexMatch.For regular expression grammar, please see https://github.com/google/re2/wiki/Syntax.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#regex_match GoogleNetworkServicesHttpRoute#regex_match}
        '''
        result = self._values.get("regex_match")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__99ecae835679efbe9f78d801aeca3d214acc912e1a985db0bb41fa0a093d8c84)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea3972830e8123dfd79cfa9d5ce8da464a74fbccd9dd7ad7a49db52785dfbc96)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f6840465e60b74e48f0a383db3b2ca36b100d00adf03c964f04ce23d25bf36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d70b8272eaf80cc63e1143fc8d18c2be726f02d789e33c921516cb93e21b763)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba728ab69f0a7a1d9df27c1016589bab4af2d22fc90a0af0df2615cdbee2b7be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85da23d61d16ddbe3010a2d476ad96e923c7ac3d335ee6c006fbbcccdaaeb353)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__813bd9efd5072f42dad7fa3ff2497996a38385391aa32b578d366689e3ac58b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e68d0e868ceab15aa919b9743a43895b2d4c95a29e77fbedb5ee77a286a4c440)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a02b256c23affcf9f645e424cad1b7dae7edf73c5113beb440850ce9f510b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "presentMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryParameter")
    def query_parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryParameter"))

    @query_parameter.setter
    def query_parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21656b087ba6b04e495e05e6c5784deb205312cade9f30c34136628ef9349dd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryParameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regexMatch")
    def regex_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regexMatch"))

    @regex_match.setter
    def regex_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6d1393f087abd18227cde42298ad0681cb28f2c935d9788b6949032e81c413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regexMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2cc1d2405e39d5f9a70915c66ba3340eb25262fedc44e6a01fa94f09a54c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleNetworkServicesHttpRouteRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__952f443caa190b9c8eaee32a0f1f045714d65b1aa44e8b0bc2193015e94cd587)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        cors_policy: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionCorsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        fault_injection_policy: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        redirect: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
        request_header_modifier: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier, typing.Dict[builtins.str, typing.Any]]] = None,
        request_mirror_policy: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        response_header_modifier: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier, typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[builtins.str] = None,
        url_rewrite: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionUrlRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cors_policy: cors_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#cors_policy GoogleNetworkServicesHttpRoute#cors_policy}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#destinations GoogleNetworkServicesHttpRoute#destinations}
        :param fault_injection_policy: fault_injection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#fault_injection_policy GoogleNetworkServicesHttpRoute#fault_injection_policy}
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#redirect GoogleNetworkServicesHttpRoute#redirect}
        :param request_header_modifier: request_header_modifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#request_header_modifier GoogleNetworkServicesHttpRoute#request_header_modifier}
        :param request_mirror_policy: request_mirror_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#request_mirror_policy GoogleNetworkServicesHttpRoute#request_mirror_policy}
        :param response_header_modifier: response_header_modifier block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#response_header_modifier GoogleNetworkServicesHttpRoute#response_header_modifier}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#retry_policy GoogleNetworkServicesHttpRoute#retry_policy}
        :param timeout: Specifies the timeout for selected route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#timeout GoogleNetworkServicesHttpRoute#timeout}
        :param url_rewrite: url_rewrite block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#url_rewrite GoogleNetworkServicesHttpRoute#url_rewrite}
        '''
        value = GoogleNetworkServicesHttpRouteRulesAction(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c4b39a5891b9046c25d1733068b6a0da88e50f65d4240eb3a8e514b7e99ad1b)
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
    def action(self) -> GoogleNetworkServicesHttpRouteRulesActionOutputReference:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="matches")
    def matches(self) -> GoogleNetworkServicesHttpRouteRulesMatchesList:
        return typing.cast(GoogleNetworkServicesHttpRouteRulesMatchesList, jsii.get(self, "matches"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[GoogleNetworkServicesHttpRouteRulesAction]:
        return typing.cast(typing.Optional[GoogleNetworkServicesHttpRouteRulesAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchesInput")
    def matches_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatches]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatches]]], jsii.get(self, "matchesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6050aeed11651df0c681f0581d4fd5975bbf84969729732c3f9c0c4b02db9b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleNetworkServicesHttpRouteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#create GoogleNetworkServicesHttpRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#delete GoogleNetworkServicesHttpRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#update GoogleNetworkServicesHttpRoute#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f658a22019ae8dc465ea99f6d439939a46c9467749ae76c31ae23ada76bc75eb)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#create GoogleNetworkServicesHttpRoute#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#delete GoogleNetworkServicesHttpRoute#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_network_services_http_route#update GoogleNetworkServicesHttpRoute#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleNetworkServicesHttpRouteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleNetworkServicesHttpRouteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleNetworkServicesHttpRoute.GoogleNetworkServicesHttpRouteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b47dbdaa9c6847ce4c9b3bf08c8f25d393b24d229284721c61e283b0381cc4cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7886a2d184372c7ddf79d85f21851204667c67aa77d8040d4711522dc12d11ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c18c9d1781c44b969b12ce85421caedaca69a76c18e730fe03184875a9c36c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324bb2c033df95c6f07995dfef463ff66e253314842fe6c3774cc5a205551e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140db52509587c7e286d286badf2892ec7d5d409b0d3505b114ebbbaa2eff9d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleNetworkServicesHttpRoute",
    "GoogleNetworkServicesHttpRouteConfig",
    "GoogleNetworkServicesHttpRouteRules",
    "GoogleNetworkServicesHttpRouteRulesAction",
    "GoogleNetworkServicesHttpRouteRulesActionCorsPolicy",
    "GoogleNetworkServicesHttpRouteRulesActionCorsPolicyOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionDestinations",
    "GoogleNetworkServicesHttpRouteRulesActionDestinationsList",
    "GoogleNetworkServicesHttpRouteRulesActionDestinationsOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy",
    "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort",
    "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbortOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay",
    "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelayOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionRedirect",
    "GoogleNetworkServicesHttpRouteRulesActionRedirectOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier",
    "GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifierOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy",
    "GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination",
    "GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestinationOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier",
    "GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifierOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionRetryPolicy",
    "GoogleNetworkServicesHttpRouteRulesActionRetryPolicyOutputReference",
    "GoogleNetworkServicesHttpRouteRulesActionUrlRewrite",
    "GoogleNetworkServicesHttpRouteRulesActionUrlRewriteOutputReference",
    "GoogleNetworkServicesHttpRouteRulesList",
    "GoogleNetworkServicesHttpRouteRulesMatches",
    "GoogleNetworkServicesHttpRouteRulesMatchesHeaders",
    "GoogleNetworkServicesHttpRouteRulesMatchesHeadersList",
    "GoogleNetworkServicesHttpRouteRulesMatchesHeadersOutputReference",
    "GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch",
    "GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatchOutputReference",
    "GoogleNetworkServicesHttpRouteRulesMatchesList",
    "GoogleNetworkServicesHttpRouteRulesMatchesOutputReference",
    "GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters",
    "GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersList",
    "GoogleNetworkServicesHttpRouteRulesMatchesQueryParametersOutputReference",
    "GoogleNetworkServicesHttpRouteRulesOutputReference",
    "GoogleNetworkServicesHttpRouteTimeouts",
    "GoogleNetworkServicesHttpRouteTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cc1ada8f0e59e0b22412f009f37576e14cf1891a3f205ff38303a7d9fe804ea8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hostnames: typing.Sequence[builtins.str],
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRules, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__1179798df7526f035736b13f5856dd6c39fc034ee1ef1a9c5058f28a6123865d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a279b8bbde934f34acebcc85652ed9385432e4884a4219debc8647a25672cab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6665e433a48763dca5cb9546b16e0f247f3daf2485968ea024deb3c27d3a9aed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971273a21195f8e45b1e75c6a993832ab38da8b0f41122c2549d6164ceff1b4f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6af21428adce2efb4614b2c72093290419d6a25fb2a5217960c3772de54911b4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2349595266fd1ed32bf8c180222f5347e807f3a82e353e653bbc9230c2e6dc9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360a84fe36f53bf368bead6fb67b88211857cc39135e7c50fb74e237c56331c5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a211463009688c0a21d6655efe44f001f789a1908d2798624ff3d5d5457af2c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e4308c401768d1c1d900b70fa8c7f25b322cf41d67436b7e5c660a4dbb3a03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a7ab82aaa2d036885dc2845e77b377e3712cf93250044d96874463a35be5c25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2aca307d88ff7f04d271fbd4628adfb1115890547e3fea8f170d86998d20dc3(
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
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRules, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b6ab124cdef24af2d9543dab9fc5e4225e0d41382bf9a09b85c5ab355f8fcd(
    *,
    action: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesAction, typing.Dict[builtins.str, typing.Any]]] = None,
    matches: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6645bb248d56ef305f57429e385092697a31d2cfb1a88c65ea84d32733da36c(
    *,
    cors_policy: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionCorsPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fault_injection_policy: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    redirect: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRedirect, typing.Dict[builtins.str, typing.Any]]] = None,
    request_header_modifier: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier, typing.Dict[builtins.str, typing.Any]]] = None,
    request_mirror_policy: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    response_header_modifier: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_policy: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[builtins.str] = None,
    url_rewrite: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionUrlRewrite, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ece41eb137d3a6e39a7e2e05f66e3ae58aa1e372b9a003a1600512b61750725(
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

def _typecheckingstub__bbab113bd720f526b74a3b5d346ab6a7d8e150c8453024ffed69419b9c3f77c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65500fceba94ed6e1a330eae19192fc8628df2c902b72a5077aba27df9ff1ddd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aaa95af16fdb48b3b11480c3baa4b49aacf9d46132ac5a490917116e73d3cbc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f42e7ad9c90b2043438c9929eb0e94d89c704fc48de2704be46d2a7b7a60fa(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3216e627c5a0485faf0662d8232f3116681374282c1c54bc780bfdeec040d53b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107d99fbe1b7d871fad11d4920db7d9d30e10cc5001ffa43363256199e525d0d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbbda47ac0396c98bed2241207864671bc644f32a24e337bd003dd6d19cdbdc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2a1292630ad9b013e00714159b7fbed02adf382fed3bc58b8944bda0189b31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7648dfe7cd15c21770c4de4f847027db23e331c565454b27b914b818148f8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edf049f2d1c3e3a70783edbb40a35b7d31e976771d3f665f686b96fa004d4462(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionCorsPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c3690b223fa877a38a1f6c409037a01297e760e87ad9ec11950ffc15ffbee6(
    *,
    service_name: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8fc734b4e04f6dc1a36e5564d214a64fba457e3d56a351c6d62d2785aa4799(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19857a66d7fcf44e9f292af4622210a2a59b1b8946941ce67a46ba17a2cdc77(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb0bd943af92103df3fdaa3100e7cf4f6b712dbeda080593078421f068a57876(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b44a5504cc681ac4cedc0ad7e0930c2e914544408a9bab9f0b8a98e22451b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c6d2e30c0906437c0eb3f363b6f8b86a0a0cf1c18ec8e2548f4da40c411cc4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4dcd5b4909387d006186e76343797062f42f007099a302ba9906b9f56104b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesActionDestinations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da918991e956597cafdd1ecd825a61d198bae82f573467f64b83cbd4527c6a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4346f2ae78ad1026f44960ab14bf79d0e8601f1a7b78055d91b6252ef95b00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a37c837be0c562ca74e1c8593248a10f9cbb0d46921c3ca1c20916465958900(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75712e6bd65442f5b3829bda16fcaead2a91fb67783f51576f2cf51e19aa175c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesActionDestinations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514e80f5e02d1e7839979a7d24f917d99d749af811ee5847c8f8124040ded2d0(
    *,
    abort: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort, typing.Dict[builtins.str, typing.Any]]] = None,
    delay: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a2ad22465ba905b05a8fa925347f4aa30d844bc23e3d451a673b2690baa8dc(
    *,
    http_status: typing.Optional[jsii.Number] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e5b412097b6c008b1e2402ae905a0b22e38f21ca492147700872914a328a44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581958fd1a1e8b248c1b576b599273dbdf4baf93f1ebe1bfca33404cdcdb8a2b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a02d045d35da4c1b2991683d422358a4fee506d93f211ca17d53b2e9cc1d36(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44baa4ebb1a8ddad7d2c3ea02a77bb01971ec3822bbef6b789b98edfb60fdbb(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyAbort],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa7c226a9302d17a6446554dba863f5b834fa911e0befd0479636503eadaaea(
    *,
    fixed_delay: typing.Optional[builtins.str] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0621f89685a6cbf182310c2b8c9ba775e27ff8bdee1419fadf237926c58714d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6958010a13ade43ca5a46fdaf3cb390eae4a2bd4f633546d4c8323065c231d5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351fda843c72e6cf0aa2f14a14aa4a92e4df83d31652dea43691d48311e7a8f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ce4cfa3f657bf15931be361aeafe58f715e7cd15dd977e5d5d042573ab19f9(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicyDelay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c858e070d0337aedec6db8506a82841631cbc5858b8c96a99078e5ac95e92678(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d342d51b0b81bc0d4a23ce195557e3d98eb377c38ea3df3463b9db62f8e6fc9c(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionFaultInjectionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248b1e7821de95401979302646508dca38a31e9367b55a7280efa744729f4491(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5287bf7ef55b306dc834a41e0f38f3c789aa948e91adf70eeb2cc21000afd490(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9dcf59e57677e141268e11d8b20ef1af816a446ea93debfdda879cc2e90f224(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a583f3b97bd35a1c80c0811c8f9eafeead1f8cac122a97ece68ec5f792548ec0(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca52603c6f42a6773806d0476124b0d53075e65dbe6fc92474f9c620a3890c7(
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

def _typecheckingstub__563853dfc208d1f06be513d8304c7cbdbadb866f28770fdbb70450f9684feb62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f578c9f70d034b85fecf9ccd15a2d2d26ff3d29aadd5d32c6e19294cb44ec157(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36a343e63b2845546659419aebba5e159b4fb691f403d8a5973ab6d198ba3936(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b3ae197a5b66bacaeef1689069e37978d9b08358d8a2db41b5516a5471c9ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__976a7026b1034a1a4898211229e037681f79e738f7becf662c92497be2ad82fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa8b07b2c72b6d5a467421082198ed2325c0e3f3560fd869926900c22b0085a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9c90eea284d73f9cb4e8f48711ea07dcdb774d4ffff70163d69e857535e231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6721926f17e0a527249a13fdd01a30476a85674f88670f6d166b9cc3111ef88b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3c9ada1d62c9c587247a46cc9f44cece37b918cf5d53cb207d091704f1d72bb(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRedirect],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d57648f79c585bfee045d1ccd858358f505a49585d5e830cd0dd6032bedca1(
    *,
    add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993ca6857d34205da98319fb5e24bfe8fb7c944783e16e4d6a7929db66d97f2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270c162ad412abc5bd17461cb9f35d03060953f0caad0fc2bb21613d3422c4db(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6227776d179754e23a373d85539067257fab21a5a001d56ac1e5e25b7ebea5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03276e5d11b81de836805071d9580aec7ed24673c44cdf84dc68c1273c2ca2fe(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b398fbc7f2fd586ee430b084108ba82ec9c83929b458f02288b2b827919e1866(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestHeaderModifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e9e8d3c24fcbecb5d76bb76e2c1ede270c31002a2c281ed53aa16c57cf704f(
    *,
    destination: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4882ba70501a32eb58401b78f7025e7f88270dd7d39735f110dd361ccdafee43(
    *,
    service_name: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4aaad078cb538f2d6ab0add2c30011b5ec899bfcc1f92f07f47089150e7ea1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b62c1ed7ebba85904aa781b8bf046013021432f1bffb0686b7bf82568193a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebd702703d307d28c1cde84b4fb2a0096749f426c1244179d57f2b380c68bed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76abeeca5fd5d62dd3298f1a3f44ca99da10b0ad3e5f15489808e77e1cbf4856(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicyDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fc5a21f998d455ed546146a81621eb68f2eefd23a519e262759f087c6fd64b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2164a1dde40ac1e2d685a97bfa6e5c5a3346db62269744e43152ca044ad77a22(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRequestMirrorPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d893f8186cf93278996d2ae76b564a19824a99eca77ab053df3b973d94ddd7e8(
    *,
    add: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    set: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a7308c7a8dd55e2e61b675d40876e312495a8a89d4b553fb4a6444a32b3645(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a625fa176ae5537544c8f7f3c733352d271a3b7c9c01208b8447b5223c73f257(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cce15c77641ba24582646d6f2ebbf8826e4996d5bf9429e5b50fbd3e13f100(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967b3b2e70edb7d2b44ff5c61cf184d0a6cdbc1cdcee676573ed9cc2be401ed9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2fe104a09ce6ed09af81327ad2ee40d2d8a80f5a358380c5aeb162fbb0396b(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionResponseHeaderModifier],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f97ec1bd7eaadb0933c01bf9d78c9843041f83f31e73cfc2609622e006c1b1(
    *,
    num_retries: typing.Optional[jsii.Number] = None,
    per_try_timeout: typing.Optional[builtins.str] = None,
    retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75a5ae845569747ee7ecd76dc6f0943baae6ba41c9508d43215a6ca44eefb71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433c3cd064ce096f08be891517ca9f3abf03da128d2a0544cc136dfd7400de96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfff189b67b281386782c7727fef99db1d43232b4a5e7b19b7a836e69bef6856(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acdfd76605d03b319c48e27066b8a54747112912c15afcbe88597a9d472a918f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__597a9d48a2dc3adbc36917609e8fba4458e4e4154c6e6f3b12ace2c3710cb078(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c69b2e5f5c999a7ae5e71e3dc909b11731ea2c77124b917fb908bcb6022fb4b(
    *,
    host_rewrite: typing.Optional[builtins.str] = None,
    path_prefix_rewrite: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420cd6af91a88914c58517814cc4d89b62053088db6c5ab202e74ab5507983fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8682f63bac2d39f7b92df0d343c3b035533f5d148ff6e86de98379e59d7dcca1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9297e8e54bf8bac611202b365fd14ae1a48b77f0787f17491175966119bbfacc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7298b1a16967bc750c4ef5d50c5cc3bd455cab5b6c37757320a569a5318cf58(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesActionUrlRewrite],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41271cd0aa25691d135e3a6d250e52c1b48a0a48051f5355ab179ff441193ef4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86fccca34aa6c4ffc3c3ca1d68be51979959d97278e5ee7513888a31ded46bc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a2025472fb98881614336f2eec29c3b44ba8d5cf123d6d1def472c688d989e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12459c9348afd05c3b0d03c8d241e780aff87dd6a4e2b88facb92fe620766430(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b406b5d188d851263652f2bad49ba9a5fa1cb3898da9a0e9d61316726537ce9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9cacccac2857fae3cfd4220dea39f532504c993cd5ef257d3e9e115b5ef0b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4ef0821fab685a5f1ab4f0769e11b5c2b7e5a273ce7eb1c45ef9e805080a39a(
    *,
    full_path_match: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ignore_case: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix_match: typing.Optional[builtins.str] = None,
    query_parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    regex_match: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c9b9fc3af48078d5f870b9dda49bb0a883d186b54be8c4e37c2ac598114307(
    *,
    exact_match: typing.Optional[builtins.str] = None,
    header: typing.Optional[builtins.str] = None,
    invert_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prefix_match: typing.Optional[builtins.str] = None,
    present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    range_match: typing.Optional[typing.Union[GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch, typing.Dict[builtins.str, typing.Any]]] = None,
    regex_match: typing.Optional[builtins.str] = None,
    suffix_match: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02e0b326c6a6a288ff57873443c952a5d2e44dc590f3dbbc21057352c865a2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74b92d95ee54591828ceb59d9cdbb35fe856151aac4fb693a71126e9285cd4b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c21da82b01260cec883fbea0f6ee7beb364083bb13e524df7a20e579a1c41df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0f3fff76b0f273eaeb97ba40ef9816ee962aab0c9c4c03a97ad2d9ee0d5da5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcdd659fc466f10a47efb67867afc56bc588132005831dfed96a32ea2a9b07d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d4557e1a5fcff2f57ce7f7321abf6d34be87857dbc6acf857c8e8e27669f1e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce935c0ed8d44a06c5ffd5fc27d943cb2fee30a80e6d92bfd08f72e5c80a1eb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__424892b7d08377d7148f8d9fda67c93fbd6c0306b181817f4592518d442ee623(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e80e692a857681034d14ba96ce33a1d5600ca4d1650fa63735e954114f0e4c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7eb3eeaa66955a670b35c13ef5bea2a35abd2407d297c644fbdb84b95dcb43(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be475406584c1bd434fe601682996c4e0e586bad88452300f19bb2866fbf2ff3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5e65065152e7527f3052ba98267b20ec138398c35a403683e77e96c7ced268(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e785e1fc1a1e56b1f0cb247133418d333959014f050adb373c464a63764ac99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21329efcbf66e7ae888b7ebd9a6d14110dd0291599161c03fbee47f00a65e14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b86c4fec9d3da12c0d663cf216415be17aaafdb9ae08919ddff65cbaa3cbc12(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatchesHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6678ff5417c758f633f7975be28399fa7a956744ce8a6b0c9e929000aa3a79(
    *,
    end: jsii.Number,
    start: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57932cb6c61d2550285275ec3049008ae3c8330634c1b5dd5d30b2ce6924ed00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42e4a8883a921caa696f8d8c9170c9a91135317ae5255e5161ddc4a9d191707(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb98832dcc6adf444ef9e2378de1d02c8202b368c3b6e57154c8419f6fba293(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821f8f47847c537bb1c1e80b8e0c1121e9eb0154a4d90e56914f23ec59f2173b(
    value: typing.Optional[GoogleNetworkServicesHttpRouteRulesMatchesHeadersRangeMatch],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31193dca3b4c84922d4b1fd13b96f24033808b2960ed86cef4ae5abe7950472(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a109732f35aa21d660a4c0aa4cb4754ae253f874914b7b208b0c8862c1be9f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d3825f89e10f009eeed85cddfc0937a5d999d41b094f8e2e75efd788373d54c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5116521e2b7c26d242c19dcc426342cc4ede0dc10df323e6e39a2d72473dfddd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec061895566a7e80a5ec0ea9947f77f696b81047335e4a19df6dc4018e23c6c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c061066c38af16403be5bad9b5fcad60929ee3e82fa5441ca2ca9a446902ca5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatches]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3167ab93daaa3b3735ffb79535355ca5d452f06164b881d1a5cdcf72f76ebf48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df8e55e9cf4b3f664b538998a6de4d94400371ad82b7788e1aa9e90b423d24e2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76fa274308a98b8448a8943dec054bede8249a1fa3c9ee39117bff55c20fb073(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fa52a408f3017fb6173dfe840c1e88e8b8642fc2abf05583e24df33b070d83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d9a70940348828dc4d492cedb19d9098f431ac8462ce91ac2a4c8542cf5c3c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5609a338f97cb780d1d46ccb0f5ae21883f267617eb28797a2b6cdc227e4ec1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4dc0f121d4823ba3c2a33e18105ab5b46359882036df3b2e5abb442e21186c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5a80966dd2b996b67c78a1fe9807f1b3c683ed04e633202e4c512fed30c0bd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatches]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9a826cb897909433a389e4e7712d38ecb3042804bd67c6b8495adbdd6b27c2(
    *,
    exact_match: typing.Optional[builtins.str] = None,
    present_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_parameter: typing.Optional[builtins.str] = None,
    regex_match: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ecae835679efbe9f78d801aeca3d214acc912e1a985db0bb41fa0a093d8c84(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3972830e8123dfd79cfa9d5ce8da464a74fbccd9dd7ad7a49db52785dfbc96(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f6840465e60b74e48f0a383db3b2ca36b100d00adf03c964f04ce23d25bf36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d70b8272eaf80cc63e1143fc8d18c2be726f02d789e33c921516cb93e21b763(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba728ab69f0a7a1d9df27c1016589bab4af2d22fc90a0af0df2615cdbee2b7be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85da23d61d16ddbe3010a2d476ad96e923c7ac3d335ee6c006fbbcccdaaeb353(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__813bd9efd5072f42dad7fa3ff2497996a38385391aa32b578d366689e3ac58b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68d0e868ceab15aa919b9743a43895b2d4c95a29e77fbedb5ee77a286a4c440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a02b256c23affcf9f645e424cad1b7dae7edf73c5113beb440850ce9f510b74(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21656b087ba6b04e495e05e6c5784deb205312cade9f30c34136628ef9349dd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6d1393f087abd18227cde42298ad0681cb28f2c935d9788b6949032e81c413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2cc1d2405e39d5f9a70915c66ba3340eb25262fedc44e6a01fa94f09a54c0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRulesMatchesQueryParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952f443caa190b9c8eaee32a0f1f045714d65b1aa44e8b0bc2193015e94cd587(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4b39a5891b9046c25d1733068b6a0da88e50f65d4240eb3a8e514b7e99ad1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleNetworkServicesHttpRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6050aeed11651df0c681f0581d4fd5975bbf84969729732c3f9c0c4b02db9b86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f658a22019ae8dc465ea99f6d439939a46c9467749ae76c31ae23ada76bc75eb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47dbdaa9c6847ce4c9b3bf08c8f25d393b24d229284721c61e283b0381cc4cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7886a2d184372c7ddf79d85f21851204667c67aa77d8040d4711522dc12d11ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c18c9d1781c44b969b12ce85421caedaca69a76c18e730fe03184875a9c36c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324bb2c033df95c6f07995dfef463ff66e253314842fe6c3774cc5a205551e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140db52509587c7e286d286badf2892ec7d5d409b0d3505b114ebbbaa2eff9d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleNetworkServicesHttpRouteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

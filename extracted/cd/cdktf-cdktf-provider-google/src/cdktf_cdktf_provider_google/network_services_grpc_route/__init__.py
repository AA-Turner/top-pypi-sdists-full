r'''
# `google_network_services_grpc_route`

Refer to the Terraform Registry for docs: [`google_network_services_grpc_route`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route).
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


class NetworkServicesGrpcRoute(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRoute",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route google_network_services_grpc_route}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        hostnames: typing.Sequence[builtins.str],
        name: builtins.str,
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesGrpcRouteRules", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesGrpcRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route google_network_services_grpc_route} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param hostnames: Required. Service hostnames with an optional port for which this route describes traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#hostnames NetworkServicesGrpcRoute#hostnames}
        :param name: Name of the GrpcRoute resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#name NetworkServicesGrpcRoute#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#rules NetworkServicesGrpcRoute#rules}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#description NetworkServicesGrpcRoute#description}
        :param gateways: List of gateways this GrpcRoute is attached to, as one of the routing rules to route the requests served by the gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#gateways NetworkServicesGrpcRoute#gateways}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#id NetworkServicesGrpcRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the GrpcRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#labels NetworkServicesGrpcRoute#labels}
        :param location: Location (region) of the GRPCRoute resource to be created. Only the value 'global' is currently allowed; defaults to 'global' if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#location NetworkServicesGrpcRoute#location}
        :param meshes: List of meshes this GrpcRoute is attached to, as one of the routing rules to route the requests served by the mesh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#meshes NetworkServicesGrpcRoute#meshes}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#project NetworkServicesGrpcRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#timeouts NetworkServicesGrpcRoute#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c822b2f5a138681d9cc7677ca74efc8b3c52ded73397566f3f8a3e10dda4b55d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkServicesGrpcRouteConfig(
            hostnames=hostnames,
            name=name,
            rules=rules,
            description=description,
            gateways=gateways,
            id=id,
            labels=labels,
            location=location,
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
        '''Generates CDKTF code for importing a NetworkServicesGrpcRoute resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetworkServicesGrpcRoute to import.
        :param import_from_id: The id of the existing NetworkServicesGrpcRoute that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetworkServicesGrpcRoute to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5a827121d2edb5e7c215af2abc43668deb1465ae0739a38b1c78d96184617a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesGrpcRouteRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb68898e369a8b75991c34f2ce1f4f1b681d31fdc42df52b821da89e2710ae7)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#create NetworkServicesGrpcRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#delete NetworkServicesGrpcRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#update NetworkServicesGrpcRoute#update}.
        '''
        value = NetworkServicesGrpcRouteTimeouts(
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

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

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
    def rules(self) -> "NetworkServicesGrpcRouteRulesList":
        return typing.cast("NetworkServicesGrpcRouteRulesList", jsii.get(self, "rules"))

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
    def timeouts(self) -> "NetworkServicesGrpcRouteTimeoutsOutputReference":
        return typing.cast("NetworkServicesGrpcRouteTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesGrpcRouteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetworkServicesGrpcRouteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a554ad676e0c2945fdeb572a51f7f512f4c41f93382a53d32b60d10002f026)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gateways")
    def gateways(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gateways"))

    @gateways.setter
    def gateways(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd85b696603254e6269efe52fdc38c7d42943ec287a17d6035847193a572d40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateways", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostnames")
    def hostnames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostnames"))

    @hostnames.setter
    def hostnames(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797045954933e17a33c3261c3dd29a85eb7c1d69df2cb44ea8785be56b1b4941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostnames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee69d459d36ddd2d3a0eadf7efd7aa4e21fd9e48b253b6ca0f7bbe2f35610626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f3c21d81974fced95183e630537eae33cf27c8123ea957fb553201fc09b987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d465a0e3116424cd59a6836b1cd630a96883115e75ffb41c782daf46e175aad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="meshes")
    def meshes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "meshes"))

    @meshes.setter
    def meshes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__891c419bdb581bb9b6264fba1021d424daa8943e69b1c5e45787b6f8baca323a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "meshes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a032c5ae21ca8aa3801e6dbec762486741479f6c522894f81af72dfcdfd41613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c02fe1f94777f4b6697e891e19d2a070fcdaa09db00e73f8a992908d4cfb597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteConfig",
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
        "location": "location",
        "meshes": "meshes",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class NetworkServicesGrpcRouteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesGrpcRouteRules", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetworkServicesGrpcRouteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param hostnames: Required. Service hostnames with an optional port for which this route describes traffic. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#hostnames NetworkServicesGrpcRoute#hostnames}
        :param name: Name of the GrpcRoute resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#name NetworkServicesGrpcRoute#name}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#rules NetworkServicesGrpcRoute#rules}
        :param description: A free-text description of the resource. Max length 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#description NetworkServicesGrpcRoute#description}
        :param gateways: List of gateways this GrpcRoute is attached to, as one of the routing rules to route the requests served by the gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#gateways NetworkServicesGrpcRoute#gateways}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#id NetworkServicesGrpcRoute#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Set of label tags associated with the GrpcRoute resource. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#labels NetworkServicesGrpcRoute#labels}
        :param location: Location (region) of the GRPCRoute resource to be created. Only the value 'global' is currently allowed; defaults to 'global' if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#location NetworkServicesGrpcRoute#location}
        :param meshes: List of meshes this GrpcRoute is attached to, as one of the routing rules to route the requests served by the mesh. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#meshes NetworkServicesGrpcRoute#meshes}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#project NetworkServicesGrpcRoute#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#timeouts NetworkServicesGrpcRoute#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetworkServicesGrpcRouteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e2662deba4d84368af1b160bf1f7f955242fc72536ec5a9b586a02643c1883d)
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
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
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
        if location is not None:
            self._values["location"] = location
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
        '''Required. Service hostnames with an optional port for which this route describes traffic.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#hostnames NetworkServicesGrpcRoute#hostnames}
        '''
        result = self._values.get("hostnames")
        assert result is not None, "Required property 'hostnames' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the GrpcRoute resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#name NetworkServicesGrpcRoute#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRules"]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#rules NetworkServicesGrpcRoute#rules}
        '''
        result = self._values.get("rules")
        assert result is not None, "Required property 'rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRules"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A free-text description of the resource. Max length 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#description NetworkServicesGrpcRoute#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateways(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of gateways this GrpcRoute is attached to, as one of the routing rules to route the requests served by the gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#gateways NetworkServicesGrpcRoute#gateways}
        '''
        result = self._values.get("gateways")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#id NetworkServicesGrpcRoute#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of label tags associated with the GrpcRoute resource.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#labels NetworkServicesGrpcRoute#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location (region) of the GRPCRoute resource to be created.

        Only the value 'global' is currently allowed; defaults to 'global' if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#location NetworkServicesGrpcRoute#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def meshes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of meshes this GrpcRoute is attached to, as one of the routing rules to route the requests served by the mesh.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#meshes NetworkServicesGrpcRoute#meshes}
        '''
        result = self._values.get("meshes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#project NetworkServicesGrpcRoute#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetworkServicesGrpcRouteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#timeouts NetworkServicesGrpcRoute#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetworkServicesGrpcRouteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRules",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "matches": "matches"},
)
class NetworkServicesGrpcRouteRules:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union["NetworkServicesGrpcRouteRulesAction", typing.Dict[builtins.str, typing.Any]]] = None,
        matches: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesGrpcRouteRulesMatches", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#action NetworkServicesGrpcRoute#action}
        :param matches: matches block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#matches NetworkServicesGrpcRoute#matches}
        '''
        if isinstance(action, dict):
            action = NetworkServicesGrpcRouteRulesAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f072a3049c804972279086d6990f078fbd128634fff3096d3dd17fba62049166)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument matches", value=matches, expected_type=type_hints["matches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if matches is not None:
            self._values["matches"] = matches

    @builtins.property
    def action(self) -> typing.Optional["NetworkServicesGrpcRouteRulesAction"]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#action NetworkServicesGrpcRoute#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional["NetworkServicesGrpcRouteRulesAction"], result)

    @builtins.property
    def matches(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRulesMatches"]]]:
        '''matches block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#matches NetworkServicesGrpcRoute#matches}
        '''
        result = self._values.get("matches")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRulesMatches"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesAction",
    jsii_struct_bases=[],
    name_mapping={
        "destinations": "destinations",
        "fault_injection_policy": "faultInjectionPolicy",
        "retry_policy": "retryPolicy",
        "timeout": "timeout",
    },
)
class NetworkServicesGrpcRouteRulesAction:
    def __init__(
        self,
        *,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesGrpcRouteRulesActionDestinations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        fault_injection_policy: typing.Optional[typing.Union["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union["NetworkServicesGrpcRouteRulesActionRetryPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#destinations NetworkServicesGrpcRoute#destinations}
        :param fault_injection_policy: fault_injection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#fault_injection_policy NetworkServicesGrpcRoute#fault_injection_policy}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#retry_policy NetworkServicesGrpcRoute#retry_policy}
        :param timeout: Specifies the timeout for selected route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#timeout NetworkServicesGrpcRoute#timeout}
        '''
        if isinstance(fault_injection_policy, dict):
            fault_injection_policy = NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy(**fault_injection_policy)
        if isinstance(retry_policy, dict):
            retry_policy = NetworkServicesGrpcRouteRulesActionRetryPolicy(**retry_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d650170bd7b0f9669159ac791c4d4c505f9c5fb663f58fa7beb4e5464c49f5d6)
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument fault_injection_policy", value=fault_injection_policy, expected_type=type_hints["fault_injection_policy"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destinations is not None:
            self._values["destinations"] = destinations
        if fault_injection_policy is not None:
            self._values["fault_injection_policy"] = fault_injection_policy
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRulesActionDestinations"]]]:
        '''destinations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#destinations NetworkServicesGrpcRoute#destinations}
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRulesActionDestinations"]]], result)

    @builtins.property
    def fault_injection_policy(
        self,
    ) -> typing.Optional["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy"]:
        '''fault_injection_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#fault_injection_policy NetworkServicesGrpcRoute#fault_injection_policy}
        '''
        result = self._values.get("fault_injection_policy")
        return typing.cast(typing.Optional["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy"], result)

    @builtins.property
    def retry_policy(
        self,
    ) -> typing.Optional["NetworkServicesGrpcRouteRulesActionRetryPolicy"]:
        '''retry_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#retry_policy NetworkServicesGrpcRoute#retry_policy}
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional["NetworkServicesGrpcRouteRulesActionRetryPolicy"], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''Specifies the timeout for selected route.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#timeout NetworkServicesGrpcRoute#timeout}
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionDestinations",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "weight": "weight"},
)
class NetworkServicesGrpcRouteRulesActionDestinations:
    def __init__(
        self,
        *,
        service_name: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param service_name: The URL of a BackendService to route traffic to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#service_name NetworkServicesGrpcRoute#service_name}
        :param weight: Specifies the proportion of requests forwarded to the backend referenced by the serviceName field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#weight NetworkServicesGrpcRoute#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4000e37bfdbda197a5eb8a35ccdaef4dcfa79aa14c4b799c3a85f921726ef027)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#service_name NetworkServicesGrpcRoute#service_name}
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Specifies the proportion of requests forwarded to the backend referenced by the serviceName field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#weight NetworkServicesGrpcRoute#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesActionDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesGrpcRouteRulesActionDestinationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionDestinationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46eca5cfbc95ef6d8d82ab4ae64521aabdf7016bba9c77db3172b90f9551eabb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesGrpcRouteRulesActionDestinationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e4d7bf0ca185ce9ee80c6644e2b18d51c26473ed75c9d160cf4ed5819670984)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesGrpcRouteRulesActionDestinationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e44f6cc2fade49294915f1cc8f615357565dd207a1ed5fd8d05e361d89e0f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eaea2c182a77890592b475df55a2f9b37dee67826200104318cb211ed40b09d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__24e4284dfeb4320206c0fe0a48295e8d9fe3b7c1e2363512b08cd3037a748f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesActionDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesActionDestinations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesActionDestinations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3e6ee6f85430ebf83a6cf8ce400223298793f9ef87396ce891e562b740c5c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesGrpcRouteRulesActionDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c5c940f5f02bc72db9d5816a82ad995b28f196bb51ecec88e58a329e06bf34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef9b0ccca352a72b80fbc287d8fe1e04843f2db58311030c84ebdc74b96e08bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9ccd14214ccbca75aabf1d4c1fbe290b8a0bcbfa00b273548e2d8377c2a46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesActionDestinations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesActionDestinations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesActionDestinations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fddf2fc79e2ae6e39e83e6f96e1de6d5e7c6dde6fed6ebec045a7a820ce6736)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy",
    jsii_struct_bases=[],
    name_mapping={"abort": "abort", "delay": "delay"},
)
class NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy:
    def __init__(
        self,
        *,
        abort: typing.Optional[typing.Union["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort", typing.Dict[builtins.str, typing.Any]]] = None,
        delay: typing.Optional[typing.Union["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param abort: abort block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#abort NetworkServicesGrpcRoute#abort}
        :param delay: delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#delay NetworkServicesGrpcRoute#delay}
        '''
        if isinstance(abort, dict):
            abort = NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort(**abort)
        if isinstance(delay, dict):
            delay = NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay(**delay)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787155e07881785393a89841dbcbbac267b60e9c52533af8a2296a2ffe6a26b8)
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
    ) -> typing.Optional["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort"]:
        '''abort block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#abort NetworkServicesGrpcRoute#abort}
        '''
        result = self._values.get("abort")
        return typing.cast(typing.Optional["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort"], result)

    @builtins.property
    def delay(
        self,
    ) -> typing.Optional["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay"]:
        '''delay block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#delay NetworkServicesGrpcRoute#delay}
        '''
        result = self._values.get("delay")
        return typing.cast(typing.Optional["NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort",
    jsii_struct_bases=[],
    name_mapping={"http_status": "httpStatus", "percentage": "percentage"},
)
class NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort:
    def __init__(
        self,
        *,
        http_status: typing.Optional[jsii.Number] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param http_status: The HTTP status code used to abort the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#http_status NetworkServicesGrpcRoute#http_status}
        :param percentage: The percentage of traffic which will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#percentage NetworkServicesGrpcRoute#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b4f596cea4411e94d29e18a94644fc7ea299cae606d8465aab82a7f316aaba)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#http_status NetworkServicesGrpcRoute#http_status}
        '''
        result = self._values.get("http_status")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic which will be aborted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#percentage NetworkServicesGrpcRoute#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbortOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbortOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d594900723f0f65543e79b781428eec5617dba50cb8b495fcd3fdd4ef9b94095)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22ded17670f030aba80e53467fa222b3ca1024a980709154c0a387d115c6004f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cf84e4e585440a509823e04ae574a0bd2bb318dcb018cf0c4f1351da70a8553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__082cf57bc74c3bb69dae4c2c4e81f07d10b95628e1f359781b84ea8420c6436b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay",
    jsii_struct_bases=[],
    name_mapping={"fixed_delay": "fixedDelay", "percentage": "percentage"},
)
class NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay:
    def __init__(
        self,
        *,
        fixed_delay: typing.Optional[builtins.str] = None,
        percentage: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed_delay: Specify a fixed delay before forwarding the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#fixed_delay NetworkServicesGrpcRoute#fixed_delay}
        :param percentage: The percentage of traffic on which delay will be injected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#percentage NetworkServicesGrpcRoute#percentage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d4c4e2a5ac0fbc25625a9cae03b883a504a8fed5098ce06ef5f73404ae8e15)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#fixed_delay NetworkServicesGrpcRoute#fixed_delay}
        '''
        result = self._values.get("fixed_delay")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def percentage(self) -> typing.Optional[jsii.Number]:
        '''The percentage of traffic on which delay will be injected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#percentage NetworkServicesGrpcRoute#percentage}
        '''
        result = self._values.get("percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelayOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelayOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db6a1e349aa320613bd1261fe9d8bd5d175baff3016fd06de5b0033e6de79337)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64accdfe748d258cae00682b8348493c235a89b7090a26057493e68b5f2f6b4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedDelay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percentage")
    def percentage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percentage"))

    @percentage.setter
    def percentage(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c892e97ffc42db70c42cc94777759871b249c66546e5ca834d424a53f1a067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percentage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b315877878daabd93c636c0015f20c84035da2834cb0958533d0aa0401e31fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e22bd0dd4a04e467fdb16b0aa72f6689c2a504294456244a44e74601c2c44565)
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
        :param http_status: The HTTP status code used to abort the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#http_status NetworkServicesGrpcRoute#http_status}
        :param percentage: The percentage of traffic which will be aborted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#percentage NetworkServicesGrpcRoute#percentage}
        '''
        value = NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort(
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
        :param fixed_delay: Specify a fixed delay before forwarding the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#fixed_delay NetworkServicesGrpcRoute#fixed_delay}
        :param percentage: The percentage of traffic on which delay will be injected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#percentage NetworkServicesGrpcRoute#percentage}
        '''
        value = NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay(
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
    ) -> NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbortOutputReference:
        return typing.cast(NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbortOutputReference, jsii.get(self, "abort"))

    @builtins.property
    @jsii.member(jsii_name="delay")
    def delay(
        self,
    ) -> NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelayOutputReference:
        return typing.cast(NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelayOutputReference, jsii.get(self, "delay"))

    @builtins.property
    @jsii.member(jsii_name="abortInput")
    def abort_input(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort], jsii.get(self, "abortInput"))

    @builtins.property
    @jsii.member(jsii_name="delayInput")
    def delay_input(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay], jsii.get(self, "delayInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a4fe7ba2b62cc9ff88a66bed9d177710582becf16cd37d1fcc8c49af57ba3c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesGrpcRouteRulesActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16918f8f5fc02f6b7c243f1da75ed3328bdc71742f7c2fb71c262c3e5ac3e7b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a5764e0b1fd7beb748a5bbdbecac0105914c7cc56287817e092c4cdb3060393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

    @jsii.member(jsii_name="putFaultInjectionPolicy")
    def put_fault_injection_policy(
        self,
        *,
        abort: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort, typing.Dict[builtins.str, typing.Any]]] = None,
        delay: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param abort: abort block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#abort NetworkServicesGrpcRoute#abort}
        :param delay: delay block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#delay NetworkServicesGrpcRoute#delay}
        '''
        value = NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy(
            abort=abort, delay=delay
        )

        return typing.cast(None, jsii.invoke(self, "putFaultInjectionPolicy", [value]))

    @jsii.member(jsii_name="putRetryPolicy")
    def put_retry_policy(
        self,
        *,
        num_retries: typing.Optional[jsii.Number] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param num_retries: Specifies the allowed number of retries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#num_retries NetworkServicesGrpcRoute#num_retries}
        :param retry_conditions: Specifies one or more conditions when this retry policy applies. Possible values: ["connect-failure", "refused-stream", "cancelled", "deadline-exceeded", "resource-exhausted", "unavailable"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#retry_conditions NetworkServicesGrpcRoute#retry_conditions}
        '''
        value = NetworkServicesGrpcRouteRulesActionRetryPolicy(
            num_retries=num_retries, retry_conditions=retry_conditions
        )

        return typing.cast(None, jsii.invoke(self, "putRetryPolicy", [value]))

    @jsii.member(jsii_name="resetDestinations")
    def reset_destinations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDestinations", []))

    @jsii.member(jsii_name="resetFaultInjectionPolicy")
    def reset_fault_injection_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFaultInjectionPolicy", []))

    @jsii.member(jsii_name="resetRetryPolicy")
    def reset_retry_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryPolicy", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> NetworkServicesGrpcRouteRulesActionDestinationsList:
        return typing.cast(NetworkServicesGrpcRouteRulesActionDestinationsList, jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="faultInjectionPolicy")
    def fault_injection_policy(
        self,
    ) -> NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyOutputReference:
        return typing.cast(NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyOutputReference, jsii.get(self, "faultInjectionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicy")
    def retry_policy(
        self,
    ) -> "NetworkServicesGrpcRouteRulesActionRetryPolicyOutputReference":
        return typing.cast("NetworkServicesGrpcRouteRulesActionRetryPolicyOutputReference", jsii.get(self, "retryPolicy"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesActionDestinations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesActionDestinations]]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="faultInjectionPolicyInput")
    def fault_injection_policy_input(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy], jsii.get(self, "faultInjectionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="retryPolicyInput")
    def retry_policy_input(
        self,
    ) -> typing.Optional["NetworkServicesGrpcRouteRulesActionRetryPolicy"]:
        return typing.cast(typing.Optional["NetworkServicesGrpcRouteRulesActionRetryPolicy"], jsii.get(self, "retryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7efd5cbc2e8efaebb215c64c9f8dcac08924c7e95f6e4c480a30d84d3eb95724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkServicesGrpcRouteRulesAction]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesGrpcRouteRulesAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16ad65a748623f3d67c26464dbd234fb679f571b3f923f4e86715712c0183c72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionRetryPolicy",
    jsii_struct_bases=[],
    name_mapping={"num_retries": "numRetries", "retry_conditions": "retryConditions"},
)
class NetworkServicesGrpcRouteRulesActionRetryPolicy:
    def __init__(
        self,
        *,
        num_retries: typing.Optional[jsii.Number] = None,
        retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param num_retries: Specifies the allowed number of retries. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#num_retries NetworkServicesGrpcRoute#num_retries}
        :param retry_conditions: Specifies one or more conditions when this retry policy applies. Possible values: ["connect-failure", "refused-stream", "cancelled", "deadline-exceeded", "resource-exhausted", "unavailable"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#retry_conditions NetworkServicesGrpcRoute#retry_conditions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf9b3d2393ded65bcf1807e0e371a443edf4cf78be0d96569b4ff9f3d56060c)
            check_type(argname="argument num_retries", value=num_retries, expected_type=type_hints["num_retries"])
            check_type(argname="argument retry_conditions", value=retry_conditions, expected_type=type_hints["retry_conditions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if num_retries is not None:
            self._values["num_retries"] = num_retries
        if retry_conditions is not None:
            self._values["retry_conditions"] = retry_conditions

    @builtins.property
    def num_retries(self) -> typing.Optional[jsii.Number]:
        '''Specifies the allowed number of retries.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#num_retries NetworkServicesGrpcRoute#num_retries}
        '''
        result = self._values.get("num_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_conditions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies one or more conditions when this retry policy applies. Possible values: ["connect-failure", "refused-stream", "cancelled", "deadline-exceeded", "resource-exhausted", "unavailable"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#retry_conditions NetworkServicesGrpcRoute#retry_conditions}
        '''
        result = self._values.get("retry_conditions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesActionRetryPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesGrpcRouteRulesActionRetryPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesActionRetryPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__006f7fdcb29ff8769cd2734a5d9e61e06f8f4e2560787b9418d5f4df0fb74eb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNumRetries")
    def reset_num_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumRetries", []))

    @jsii.member(jsii_name="resetRetryConditions")
    def reset_retry_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetryConditions", []))

    @builtins.property
    @jsii.member(jsii_name="numRetriesInput")
    def num_retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numRetriesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2e8ef1519f726472e0f172b0f144d9c5880a1164ea2ec92c5b91495674f63658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numRetries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retryConditions")
    def retry_conditions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "retryConditions"))

    @retry_conditions.setter
    def retry_conditions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f7e032dd7ff32724c90f1e85bb87e3cca970c54e49b1024667408249f176e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryConditions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesActionRetryPolicy]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesActionRetryPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesGrpcRouteRulesActionRetryPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57842cee421350cb5625735cb39976f470fa85145f9c84bb5d8659a5fe6e041c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesGrpcRouteRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcafaadda4743987472d7d5c257ee7bd7c7e97840ab4b261135fb1bc79285315)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetworkServicesGrpcRouteRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c103ca055b5aad6a002a0d30b616a84619ed6d48784278efed5962a454e4f42)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesGrpcRouteRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10acbc89dc1747ad7197dca50e54581f14434d62744a92cf7198d3f1bda4c537)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b8473a9602b8de7c38f88a75b709c9c9a1d66c997d800e589f2f8f762cecc15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f9e17c0cde3157eed8fd68981d01b86b8118cc23b25d2d06f8fb035dfd59733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64981f2e9a4dc2d8384d63dcf1f1a6083194ea8603d45990eb40a739d7e3e530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesMatches",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "method": "method"},
)
class NetworkServicesGrpcRouteRulesMatches:
    def __init__(
        self,
        *,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkServicesGrpcRouteRulesMatchesHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        method: typing.Optional[typing.Union["NetworkServicesGrpcRouteRulesMatchesMethod", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param headers: headers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#headers NetworkServicesGrpcRoute#headers}
        :param method: method block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#method NetworkServicesGrpcRoute#method}
        '''
        if isinstance(method, dict):
            method = NetworkServicesGrpcRouteRulesMatchesMethod(**method)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097ed5be304e7e5636d2a8b1cd9c6bd7bdcfcaf8cda24d4c7e22d239942c1e87)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if headers is not None:
            self._values["headers"] = headers
        if method is not None:
            self._values["method"] = method

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRulesMatchesHeaders"]]]:
        '''headers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#headers NetworkServicesGrpcRoute#headers}
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkServicesGrpcRouteRulesMatchesHeaders"]]], result)

    @builtins.property
    def method(self) -> typing.Optional["NetworkServicesGrpcRouteRulesMatchesMethod"]:
        '''method block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#method NetworkServicesGrpcRoute#method}
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional["NetworkServicesGrpcRouteRulesMatchesMethod"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesMatches(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesMatchesHeaders",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value", "type": "type"},
)
class NetworkServicesGrpcRouteRulesMatchesHeaders:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Required. The key of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#key NetworkServicesGrpcRoute#key}
        :param value: Required. The value of the header. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#value NetworkServicesGrpcRoute#value}
        :param type: The type of match. Default value: "EXACT" Possible values: ["TYPE_UNSPECIFIED", "EXACT", "REGULAR_EXPRESSION"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#type NetworkServicesGrpcRoute#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bade8a69a133fffb5ac1682ccf75ec335be042d63dc74459f294ee0ddad4943)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def key(self) -> builtins.str:
        '''Required. The key of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#key NetworkServicesGrpcRoute#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Required. The value of the header.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#value NetworkServicesGrpcRoute#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of match. Default value: "EXACT" Possible values: ["TYPE_UNSPECIFIED", "EXACT", "REGULAR_EXPRESSION"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#type NetworkServicesGrpcRoute#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesMatchesHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesGrpcRouteRulesMatchesHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesMatchesHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41c224069e3ac257bf477286519c9beb53988927222003ecb6fad815a4141d15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesGrpcRouteRulesMatchesHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b7143bae9a8f25a567aeece6fd46fccee8da90966621eb0d0fa416af684a8c0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesGrpcRouteRulesMatchesHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44ae956249cf36fa3aec227a2abfe04d634d7b3eb5d955ea6d0cf192f4e7e10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86c74a46d9fd8f10b9aeffe07ecf852149f6c2c024539eea81b4a4f8a62d3041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3a94dbb1bcf94a91a670947a0d24fdd686e2731656cc60e7871a12c765cb03b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatchesHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatchesHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatchesHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57d336363f243def7ef7d1bb96e05a301ac6f7c9bff30743627e45d831365a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesGrpcRouteRulesMatchesHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesMatchesHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b64acd33e5e962440c4e69c607c56e3afc579991bcb6b128bd3d320793cf46ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77de1715a899745c2db4ad84abec26dd0e6efeb791c5fb74c7b035c367652b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997de8819f08ff00b8b7ac1f826ba7da3829ef555d149328d2a7780748762d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad30b77fb917f28bdc4de067a033db7e7de36fd7fdcb38523413696fac109f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesMatchesHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesMatchesHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesMatchesHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0cc352f95df606ea1273e228f3f28e6c8ee68e2bd52bea848ddd6673f38c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesGrpcRouteRulesMatchesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesMatchesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5270d9f2fa01682463561a6b38dd103f104cb7da4425754dba89692f7bdc1bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkServicesGrpcRouteRulesMatchesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334f31a9552830a334b770c6438074ed779ec46c4dfd63659f6d282eb85f9b05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkServicesGrpcRouteRulesMatchesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705730e7a85f2567bebfe93db698dbf4ad6f052c51eac42cf8549c93f53de851)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0abf15efba548f0d07e12e14ddd6b2c502c9f61d6e33056a4327d40f704933a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63be78ce1b2bbc16f5f62c71d157c437813ed46e3ab0bed1b255565fc105f8ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatches]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatches]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatches]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a84c7b1a7bb500c4c65cf9e5d31a5ae2722f3efe9bfcbe65646972bf129443c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesMatchesMethod",
    jsii_struct_bases=[],
    name_mapping={
        "grpc_method": "grpcMethod",
        "grpc_service": "grpcService",
        "case_sensitive": "caseSensitive",
    },
)
class NetworkServicesGrpcRouteRulesMatchesMethod:
    def __init__(
        self,
        *,
        grpc_method: builtins.str,
        grpc_service: builtins.str,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param grpc_method: Required. Name of the method to match against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#grpc_method NetworkServicesGrpcRoute#grpc_method}
        :param grpc_service: Required. Name of the service to match against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#grpc_service NetworkServicesGrpcRoute#grpc_service}
        :param case_sensitive: Specifies that matches are case sensitive. The default value is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#case_sensitive NetworkServicesGrpcRoute#case_sensitive}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b22238099b451be7140b07542a94b3c558f907147b9ccae026a04b618cd482)
            check_type(argname="argument grpc_method", value=grpc_method, expected_type=type_hints["grpc_method"])
            check_type(argname="argument grpc_service", value=grpc_service, expected_type=type_hints["grpc_service"])
            check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "grpc_method": grpc_method,
            "grpc_service": grpc_service,
        }
        if case_sensitive is not None:
            self._values["case_sensitive"] = case_sensitive

    @builtins.property
    def grpc_method(self) -> builtins.str:
        '''Required. Name of the method to match against.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#grpc_method NetworkServicesGrpcRoute#grpc_method}
        '''
        result = self._values.get("grpc_method")
        assert result is not None, "Required property 'grpc_method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grpc_service(self) -> builtins.str:
        '''Required. Name of the service to match against.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#grpc_service NetworkServicesGrpcRoute#grpc_service}
        '''
        result = self._values.get("grpc_service")
        assert result is not None, "Required property 'grpc_service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def case_sensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies that matches are case sensitive. The default value is true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#case_sensitive NetworkServicesGrpcRoute#case_sensitive}
        '''
        result = self._values.get("case_sensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteRulesMatchesMethod(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesGrpcRouteRulesMatchesMethodOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesMatchesMethodOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6cc99b6f855d8f19f3b6be712b95f21f82514dc0eb148fd37bb71711b938103)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCaseSensitive")
    def reset_case_sensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaseSensitive", []))

    @builtins.property
    @jsii.member(jsii_name="caseSensitiveInput")
    def case_sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "caseSensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcMethodInput")
    def grpc_method_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grpcMethodInput"))

    @builtins.property
    @jsii.member(jsii_name="grpcServiceInput")
    def grpc_service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grpcServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="caseSensitive")
    def case_sensitive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "caseSensitive"))

    @case_sensitive.setter
    def case_sensitive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dce5f99bd4ed102aefd5a04d99e178fd438cf142e52fd098683c0756a38fe3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseSensitive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grpcMethod")
    def grpc_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grpcMethod"))

    @grpc_method.setter
    def grpc_method(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c343a4005b83ca71e18fc27945efc919898f7b9f5fba6be691ac01414efbde89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grpcMethod", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grpcService")
    def grpc_service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grpcService"))

    @grpc_service.setter
    def grpc_service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e7f57b4e2e4766167e7106bd0c8c59e4da30c4b491d15c03b1bef800349978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grpcService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesMatchesMethod]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesMatchesMethod], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkServicesGrpcRouteRulesMatchesMethod],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b1c13d3c0f275e22504e212af555ed052c22c1bdb245035d74d270785ac7f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesGrpcRouteRulesMatchesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesMatchesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdd836196d951f857d5befb4c309de9e71b54c57519dc1273a6e9bf4527e1bc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e128b17f9d57cbf794e43814ac2411e80728231307292281b9ef29c24f9360ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="putMethod")
    def put_method(
        self,
        *,
        grpc_method: builtins.str,
        grpc_service: builtins.str,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param grpc_method: Required. Name of the method to match against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#grpc_method NetworkServicesGrpcRoute#grpc_method}
        :param grpc_service: Required. Name of the service to match against. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#grpc_service NetworkServicesGrpcRoute#grpc_service}
        :param case_sensitive: Specifies that matches are case sensitive. The default value is true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#case_sensitive NetworkServicesGrpcRoute#case_sensitive}
        '''
        value = NetworkServicesGrpcRouteRulesMatchesMethod(
            grpc_method=grpc_method,
            grpc_service=grpc_service,
            case_sensitive=case_sensitive,
        )

        return typing.cast(None, jsii.invoke(self, "putMethod", [value]))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetMethod")
    def reset_method(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMethod", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> NetworkServicesGrpcRouteRulesMatchesHeadersList:
        return typing.cast(NetworkServicesGrpcRouteRulesMatchesHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="method")
    def method(self) -> NetworkServicesGrpcRouteRulesMatchesMethodOutputReference:
        return typing.cast(NetworkServicesGrpcRouteRulesMatchesMethodOutputReference, jsii.get(self, "method"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatchesHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatchesHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="methodInput")
    def method_input(
        self,
    ) -> typing.Optional[NetworkServicesGrpcRouteRulesMatchesMethod]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesMatchesMethod], jsii.get(self, "methodInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesMatches]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesMatches]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesMatches]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7116cc20a56c9eb4143c85fef17f7063446d57670b11f501d33b121ba450f48b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetworkServicesGrpcRouteRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e76cdb9e40bb1cdcdc266d065537cf4e5caaab92e022ae21161c4e98cbedd356)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        fault_injection_policy: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesActionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#destinations NetworkServicesGrpcRoute#destinations}
        :param fault_injection_policy: fault_injection_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#fault_injection_policy NetworkServicesGrpcRoute#fault_injection_policy}
        :param retry_policy: retry_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#retry_policy NetworkServicesGrpcRoute#retry_policy}
        :param timeout: Specifies the timeout for selected route. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#timeout NetworkServicesGrpcRoute#timeout}
        '''
        value = NetworkServicesGrpcRouteRulesAction(
            destinations=destinations,
            fault_injection_policy=fault_injection_policy,
            retry_policy=retry_policy,
            timeout=timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatches")
    def put_matches(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2051d2ff4ade303e28c59bc93823238feec0f78cb2a42cd0408530a53b678765)
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
    def action(self) -> NetworkServicesGrpcRouteRulesActionOutputReference:
        return typing.cast(NetworkServicesGrpcRouteRulesActionOutputReference, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="matches")
    def matches(self) -> NetworkServicesGrpcRouteRulesMatchesList:
        return typing.cast(NetworkServicesGrpcRouteRulesMatchesList, jsii.get(self, "matches"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[NetworkServicesGrpcRouteRulesAction]:
        return typing.cast(typing.Optional[NetworkServicesGrpcRouteRulesAction], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="matchesInput")
    def matches_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatches]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatches]]], jsii.get(self, "matchesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9399c5c62c77f1bbfeefecf6104e1103c2eb9d4a67655e3fc0fb512aeefb35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class NetworkServicesGrpcRouteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#create NetworkServicesGrpcRoute#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#delete NetworkServicesGrpcRoute#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#update NetworkServicesGrpcRoute#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049f1f8159bf0b8a20289d1157d757e476b2da9c4a2aef3610e3c5a315bbbdec)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#create NetworkServicesGrpcRoute#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#delete NetworkServicesGrpcRoute#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/network_services_grpc_route#update NetworkServicesGrpcRoute#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkServicesGrpcRouteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkServicesGrpcRouteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.networkServicesGrpcRoute.NetworkServicesGrpcRouteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e385fee9cd5da0632b4510503dd3cf484a8e03912ee9b9de447b168a6385795f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d8099b3f024e917796ab4c4c45960f7cf815a7267382a2c8b38bf3ef7dea77b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fe1fe96071083c5376ed9bfb9ca2cd5c0ac873cba46733826e8c7ca7a1be21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__479f86b648beb25dd181486eaee2119b3b1798e30a25d7f91eeabfb436ee7eaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8940ca54979e0c2feacf7ce09c2b1e33f47f9e477ae68a4f2bd238b40296e23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetworkServicesGrpcRoute",
    "NetworkServicesGrpcRouteConfig",
    "NetworkServicesGrpcRouteRules",
    "NetworkServicesGrpcRouteRulesAction",
    "NetworkServicesGrpcRouteRulesActionDestinations",
    "NetworkServicesGrpcRouteRulesActionDestinationsList",
    "NetworkServicesGrpcRouteRulesActionDestinationsOutputReference",
    "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy",
    "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort",
    "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbortOutputReference",
    "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay",
    "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelayOutputReference",
    "NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyOutputReference",
    "NetworkServicesGrpcRouteRulesActionOutputReference",
    "NetworkServicesGrpcRouteRulesActionRetryPolicy",
    "NetworkServicesGrpcRouteRulesActionRetryPolicyOutputReference",
    "NetworkServicesGrpcRouteRulesList",
    "NetworkServicesGrpcRouteRulesMatches",
    "NetworkServicesGrpcRouteRulesMatchesHeaders",
    "NetworkServicesGrpcRouteRulesMatchesHeadersList",
    "NetworkServicesGrpcRouteRulesMatchesHeadersOutputReference",
    "NetworkServicesGrpcRouteRulesMatchesList",
    "NetworkServicesGrpcRouteRulesMatchesMethod",
    "NetworkServicesGrpcRouteRulesMatchesMethodOutputReference",
    "NetworkServicesGrpcRouteRulesMatchesOutputReference",
    "NetworkServicesGrpcRouteRulesOutputReference",
    "NetworkServicesGrpcRouteTimeouts",
    "NetworkServicesGrpcRouteTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c822b2f5a138681d9cc7677ca74efc8b3c52ded73397566f3f8a3e10dda4b55d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    hostnames: typing.Sequence[builtins.str],
    name: builtins.str,
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRules, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesGrpcRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7a5a827121d2edb5e7c215af2abc43668deb1465ae0739a38b1c78d96184617a(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb68898e369a8b75991c34f2ce1f4f1b681d31fdc42df52b821da89e2710ae7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a554ad676e0c2945fdeb572a51f7f512f4c41f93382a53d32b60d10002f026(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd85b696603254e6269efe52fdc38c7d42943ec287a17d6035847193a572d40(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797045954933e17a33c3261c3dd29a85eb7c1d69df2cb44ea8785be56b1b4941(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee69d459d36ddd2d3a0eadf7efd7aa4e21fd9e48b253b6ca0f7bbe2f35610626(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f3c21d81974fced95183e630537eae33cf27c8123ea957fb553201fc09b987(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d465a0e3116424cd59a6836b1cd630a96883115e75ffb41c782daf46e175aad9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__891c419bdb581bb9b6264fba1021d424daa8943e69b1c5e45787b6f8baca323a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a032c5ae21ca8aa3801e6dbec762486741479f6c522894f81af72dfcdfd41613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c02fe1f94777f4b6697e891e19d2a070fcdaa09db00e73f8a992908d4cfb597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e2662deba4d84368af1b160bf1f7f955242fc72536ec5a9b586a02643c1883d(
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
    rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRules, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    meshes: typing.Optional[typing.Sequence[builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetworkServicesGrpcRouteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f072a3049c804972279086d6990f078fbd128634fff3096d3dd17fba62049166(
    *,
    action: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesAction, typing.Dict[builtins.str, typing.Any]]] = None,
    matches: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d650170bd7b0f9669159ac791c4d4c505f9c5fb663f58fa7beb4e5464c49f5d6(
    *,
    destinations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    fault_injection_policy: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_policy: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesActionRetryPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4000e37bfdbda197a5eb8a35ccdaef4dcfa79aa14c4b799c3a85f921726ef027(
    *,
    service_name: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46eca5cfbc95ef6d8d82ab4ae64521aabdf7016bba9c77db3172b90f9551eabb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4d7bf0ca185ce9ee80c6644e2b18d51c26473ed75c9d160cf4ed5819670984(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e44f6cc2fade49294915f1cc8f615357565dd207a1ed5fd8d05e361d89e0f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eaea2c182a77890592b475df55a2f9b37dee67826200104318cb211ed40b09d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e4284dfeb4320206c0fe0a48295e8d9fe3b7c1e2363512b08cd3037a748f93(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3e6ee6f85430ebf83a6cf8ce400223298793f9ef87396ce891e562b740c5c0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesActionDestinations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c5c940f5f02bc72db9d5816a82ad995b28f196bb51ecec88e58a329e06bf34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9b0ccca352a72b80fbc287d8fe1e04843f2db58311030c84ebdc74b96e08bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9ccd14214ccbca75aabf1d4c1fbe290b8a0bcbfa00b273548e2d8377c2a46d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fddf2fc79e2ae6e39e83e6f96e1de6d5e7c6dde6fed6ebec045a7a820ce6736(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesActionDestinations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787155e07881785393a89841dbcbbac267b60e9c52533af8a2296a2ffe6a26b8(
    *,
    abort: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort, typing.Dict[builtins.str, typing.Any]]] = None,
    delay: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b4f596cea4411e94d29e18a94644fc7ea299cae606d8465aab82a7f316aaba(
    *,
    http_status: typing.Optional[jsii.Number] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d594900723f0f65543e79b781428eec5617dba50cb8b495fcd3fdd4ef9b94095(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ded17670f030aba80e53467fa222b3ca1024a980709154c0a387d115c6004f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cf84e4e585440a509823e04ae574a0bd2bb318dcb018cf0c4f1351da70a8553(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082cf57bc74c3bb69dae4c2c4e81f07d10b95628e1f359781b84ea8420c6436b(
    value: typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyAbort],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d4c4e2a5ac0fbc25625a9cae03b883a504a8fed5098ce06ef5f73404ae8e15(
    *,
    fixed_delay: typing.Optional[builtins.str] = None,
    percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6a1e349aa320613bd1261fe9d8bd5d175baff3016fd06de5b0033e6de79337(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64accdfe748d258cae00682b8348493c235a89b7090a26057493e68b5f2f6b4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c892e97ffc42db70c42cc94777759871b249c66546e5ca834d424a53f1a067(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b315877878daabd93c636c0015f20c84035da2834cb0958533d0aa0401e31fd(
    value: typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicyDelay],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22bd0dd4a04e467fdb16b0aa72f6689c2a504294456244a44e74601c2c44565(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4fe7ba2b62cc9ff88a66bed9d177710582becf16cd37d1fcc8c49af57ba3c1(
    value: typing.Optional[NetworkServicesGrpcRouteRulesActionFaultInjectionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16918f8f5fc02f6b7c243f1da75ed3328bdc71742f7c2fb71c262c3e5ac3e7b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5764e0b1fd7beb748a5bbdbecac0105914c7cc56287817e092c4cdb3060393(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesActionDestinations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7efd5cbc2e8efaebb215c64c9f8dcac08924c7e95f6e4c480a30d84d3eb95724(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16ad65a748623f3d67c26464dbd234fb679f571b3f923f4e86715712c0183c72(
    value: typing.Optional[NetworkServicesGrpcRouteRulesAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf9b3d2393ded65bcf1807e0e371a443edf4cf78be0d96569b4ff9f3d56060c(
    *,
    num_retries: typing.Optional[jsii.Number] = None,
    retry_conditions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006f7fdcb29ff8769cd2734a5d9e61e06f8f4e2560787b9418d5f4df0fb74eb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8ef1519f726472e0f172b0f144d9c5880a1164ea2ec92c5b91495674f63658(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f7e032dd7ff32724c90f1e85bb87e3cca970c54e49b1024667408249f176e9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57842cee421350cb5625735cb39976f470fa85145f9c84bb5d8659a5fe6e041c(
    value: typing.Optional[NetworkServicesGrpcRouteRulesActionRetryPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcafaadda4743987472d7d5c257ee7bd7c7e97840ab4b261135fb1bc79285315(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c103ca055b5aad6a002a0d30b616a84619ed6d48784278efed5962a454e4f42(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10acbc89dc1747ad7197dca50e54581f14434d62744a92cf7198d3f1bda4c537(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8473a9602b8de7c38f88a75b709c9c9a1d66c997d800e589f2f8f762cecc15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9e17c0cde3157eed8fd68981d01b86b8118cc23b25d2d06f8fb035dfd59733(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64981f2e9a4dc2d8384d63dcf1f1a6083194ea8603d45990eb40a739d7e3e530(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097ed5be304e7e5636d2a8b1cd9c6bd7bdcfcaf8cda24d4c7e22d239942c1e87(
    *,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    method: typing.Optional[typing.Union[NetworkServicesGrpcRouteRulesMatchesMethod, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bade8a69a133fffb5ac1682ccf75ec335be042d63dc74459f294ee0ddad4943(
    *,
    key: builtins.str,
    value: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41c224069e3ac257bf477286519c9beb53988927222003ecb6fad815a4141d15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7143bae9a8f25a567aeece6fd46fccee8da90966621eb0d0fa416af684a8c0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44ae956249cf36fa3aec227a2abfe04d634d7b3eb5d955ea6d0cf192f4e7e10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86c74a46d9fd8f10b9aeffe07ecf852149f6c2c024539eea81b4a4f8a62d3041(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a94dbb1bcf94a91a670947a0d24fdd686e2731656cc60e7871a12c765cb03b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57d336363f243def7ef7d1bb96e05a301ac6f7c9bff30743627e45d831365a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatchesHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64acd33e5e962440c4e69c607c56e3afc579991bcb6b128bd3d320793cf46ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77de1715a899745c2db4ad84abec26dd0e6efeb791c5fb74c7b035c367652b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997de8819f08ff00b8b7ac1f826ba7da3829ef555d149328d2a7780748762d4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad30b77fb917f28bdc4de067a033db7e7de36fd7fdcb38523413696fac109f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0cc352f95df606ea1273e228f3f28e6c8ee68e2bd52bea848ddd6673f38c36(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesMatchesHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5270d9f2fa01682463561a6b38dd103f104cb7da4425754dba89692f7bdc1bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334f31a9552830a334b770c6438074ed779ec46c4dfd63659f6d282eb85f9b05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__705730e7a85f2567bebfe93db698dbf4ad6f052c51eac42cf8549c93f53de851(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abf15efba548f0d07e12e14ddd6b2c502c9f61d6e33056a4327d40f704933a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63be78ce1b2bbc16f5f62c71d157c437813ed46e3ab0bed1b255565fc105f8ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a84c7b1a7bb500c4c65cf9e5d31a5ae2722f3efe9bfcbe65646972bf129443c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkServicesGrpcRouteRulesMatches]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b22238099b451be7140b07542a94b3c558f907147b9ccae026a04b618cd482(
    *,
    grpc_method: builtins.str,
    grpc_service: builtins.str,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6cc99b6f855d8f19f3b6be712b95f21f82514dc0eb148fd37bb71711b938103(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dce5f99bd4ed102aefd5a04d99e178fd438cf142e52fd098683c0756a38fe3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c343a4005b83ca71e18fc27945efc919898f7b9f5fba6be691ac01414efbde89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e7f57b4e2e4766167e7106bd0c8c59e4da30c4b491d15c03b1bef800349978(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1c13d3c0f275e22504e212af555ed052c22c1bdb245035d74d270785ac7f7c(
    value: typing.Optional[NetworkServicesGrpcRouteRulesMatchesMethod],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd836196d951f857d5befb4c309de9e71b54c57519dc1273a6e9bf4527e1bc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e128b17f9d57cbf794e43814ac2411e80728231307292281b9ef29c24f9360ee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesMatchesHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7116cc20a56c9eb4143c85fef17f7063446d57670b11f501d33b121ba450f48b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRulesMatches]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e76cdb9e40bb1cdcdc266d065537cf4e5caaab92e022ae21161c4e98cbedd356(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2051d2ff4ade303e28c59bc93823238feec0f78cb2a42cd0408530a53b678765(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkServicesGrpcRouteRulesMatches, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9399c5c62c77f1bbfeefecf6104e1103c2eb9d4a67655e3fc0fb512aeefb35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049f1f8159bf0b8a20289d1157d757e476b2da9c4a2aef3610e3c5a315bbbdec(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e385fee9cd5da0632b4510503dd3cf484a8e03912ee9b9de447b168a6385795f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8099b3f024e917796ab4c4c45960f7cf815a7267382a2c8b38bf3ef7dea77b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fe1fe96071083c5376ed9bfb9ca2cd5c0ac873cba46733826e8c7ca7a1be21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__479f86b648beb25dd181486eaee2119b3b1798e30a25d7f91eeabfb436ee7eaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8940ca54979e0c2feacf7ce09c2b1e33f47f9e477ae68a4f2bd238b40296e23(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetworkServicesGrpcRouteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

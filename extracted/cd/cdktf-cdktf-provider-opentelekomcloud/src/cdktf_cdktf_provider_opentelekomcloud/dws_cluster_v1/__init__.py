r'''
# `opentelekomcloud_dws_cluster_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_dws_cluster_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1).
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


class DwsClusterV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1 opentelekomcloud_dws_cluster_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network_id: builtins.str,
        node_type: builtins.str,
        number_of_node: jsii.Number,
        security_group_id: builtins.str,
        user_name: builtins.str,
        user_pwd: builtins.str,
        vpc_id: builtins.str,
        availability_zone: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DwsClusterV1Endpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        keep_last_manual_snapshot: typing.Optional[jsii.Number] = None,
        number_of_cn: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        public_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DwsClusterV1PublicEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_ip: typing.Optional[typing.Union["DwsClusterV1PublicIp", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DwsClusterV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1 opentelekomcloud_dws_cluster_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#name DwsClusterV1#name}.
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#network_id DwsClusterV1#network_id}.
        :param node_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#node_type DwsClusterV1#node_type}.
        :param number_of_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#number_of_node DwsClusterV1#number_of_node}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#security_group_id DwsClusterV1#security_group_id}.
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#user_name DwsClusterV1#user_name}.
        :param user_pwd: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#user_pwd DwsClusterV1#user_pwd}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#vpc_id DwsClusterV1#vpc_id}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#availability_zone DwsClusterV1#availability_zone}.
        :param endpoints: endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#endpoints DwsClusterV1#endpoints}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#id DwsClusterV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keep_last_manual_snapshot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#keep_last_manual_snapshot DwsClusterV1#keep_last_manual_snapshot}.
        :param number_of_cn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#number_of_cn DwsClusterV1#number_of_cn}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#port DwsClusterV1#port}.
        :param public_endpoints: public_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_endpoints DwsClusterV1#public_endpoints}
        :param public_ip: public_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_ip DwsClusterV1#public_ip}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#timeouts DwsClusterV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e4ce1c114e265170eb8593c0a40bd2be85708ead9884ecb026632fa95177d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DwsClusterV1Config(
            name=name,
            network_id=network_id,
            node_type=node_type,
            number_of_node=number_of_node,
            security_group_id=security_group_id,
            user_name=user_name,
            user_pwd=user_pwd,
            vpc_id=vpc_id,
            availability_zone=availability_zone,
            endpoints=endpoints,
            id=id,
            keep_last_manual_snapshot=keep_last_manual_snapshot,
            number_of_cn=number_of_cn,
            port=port,
            public_endpoints=public_endpoints,
            public_ip=public_ip,
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
        '''Generates CDKTF code for importing a DwsClusterV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DwsClusterV1 to import.
        :param import_from_id: The id of the existing DwsClusterV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DwsClusterV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a75ddb5efef90c3b799b1ca056fd8461690968f3842fb4aa0810ce4b411f898)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEndpoints")
    def put_endpoints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DwsClusterV1Endpoints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed408688d013f2b103c37d8344779b78e25bad6321676f9767a469f2cbb82da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEndpoints", [value]))

    @jsii.member(jsii_name="putPublicEndpoints")
    def put_public_endpoints(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DwsClusterV1PublicEndpoints", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aabf2e16e0699e4f53ad921f4c05b4cffa4d57771bddf561f29f577ee9069fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPublicEndpoints", [value]))

    @jsii.member(jsii_name="putPublicIp")
    def put_public_ip(
        self,
        *,
        eip_id: typing.Optional[builtins.str] = None,
        public_bind_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param eip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#eip_id DwsClusterV1#eip_id}.
        :param public_bind_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_bind_type DwsClusterV1#public_bind_type}.
        '''
        value = DwsClusterV1PublicIp(eip_id=eip_id, public_bind_type=public_bind_type)

        return typing.cast(None, jsii.invoke(self, "putPublicIp", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#create DwsClusterV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#delete DwsClusterV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#update DwsClusterV1#update}.
        '''
        value = DwsClusterV1Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAvailabilityZone")
    def reset_availability_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAvailabilityZone", []))

    @jsii.member(jsii_name="resetEndpoints")
    def reset_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoints", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKeepLastManualSnapshot")
    def reset_keep_last_manual_snapshot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepLastManualSnapshot", []))

    @jsii.member(jsii_name="resetNumberOfCn")
    def reset_number_of_cn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumberOfCn", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetPublicEndpoints")
    def reset_public_endpoints(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicEndpoints", []))

    @jsii.member(jsii_name="resetPublicIp")
    def reset_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIp", []))

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
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> "DwsClusterV1EndpointsList":
        return typing.cast("DwsClusterV1EndpointsList", jsii.get(self, "endpoints"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="publicEndpoints")
    def public_endpoints(self) -> "DwsClusterV1PublicEndpointsList":
        return typing.cast("DwsClusterV1PublicEndpointsList", jsii.get(self, "publicEndpoints"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> "DwsClusterV1PublicIpOutputReference":
        return typing.cast("DwsClusterV1PublicIpOutputReference", jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="recentEvent")
    def recent_event(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recentEvent"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="subStatus")
    def sub_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subStatus"))

    @builtins.property
    @jsii.member(jsii_name="taskStatus")
    def task_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskStatus"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DwsClusterV1TimeoutsOutputReference":
        return typing.cast("DwsClusterV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updated")
    def updated(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updated"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointsInput")
    def endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DwsClusterV1Endpoints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DwsClusterV1Endpoints"]]], jsii.get(self, "endpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keepLastManualSnapshotInput")
    def keep_last_manual_snapshot_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepLastManualSnapshotInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkIdInput")
    def network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypeInput")
    def node_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfCnInput")
    def number_of_cn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfCnInput"))

    @builtins.property
    @jsii.member(jsii_name="numberOfNodeInput")
    def number_of_node_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberOfNodeInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="publicEndpointsInput")
    def public_endpoints_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DwsClusterV1PublicEndpoints"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DwsClusterV1PublicEndpoints"]]], jsii.get(self, "publicEndpointsInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpInput")
    def public_ip_input(self) -> typing.Optional["DwsClusterV1PublicIp"]:
        return typing.cast(typing.Optional["DwsClusterV1PublicIp"], jsii.get(self, "publicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdInput")
    def security_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DwsClusterV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DwsClusterV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="userPwdInput")
    def user_pwd_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPwdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c879407eededcd5731f0ae0f55a0985f7110da7c3913d7f9c5da379767c6c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1041d6c494e0eec17ca9bb1b62dca1b27bba1717a69813acf680ae851a0ccdd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepLastManualSnapshot")
    def keep_last_manual_snapshot(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepLastManualSnapshot"))

    @keep_last_manual_snapshot.setter
    def keep_last_manual_snapshot(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e3c84002d27fc22907e62b3bc85bcf362d15266b64989532807f6dd6d498660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepLastManualSnapshot", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fbf880afe911562e2e1eae8ec7a5645c1194b7e27fdf15df0ba47e722dd894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__947b7aef88d75ec59a9182d643a24043c6ad28bf14be39b92efa43497a712f51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa27d93205c9c905d8bafee912befb78998d17618519478e384d1c908e992161)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numberOfCn")
    def number_of_cn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfCn"))

    @number_of_cn.setter
    def number_of_cn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d345c4a3450f5dfcee99276ed7fd99fa0359f1d0981cea7c88aa4f251ea9fdaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfCn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numberOfNode")
    def number_of_node(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numberOfNode"))

    @number_of_node.setter
    def number_of_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd7bb954f748245c415db4356d1f2d53a4ec50cf401078f8331c986fa658b86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numberOfNode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a7e330435c079f472f4bc152dc140658a3a0ade80f44f02c6e8bbdaf200d7fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupId"))

    @security_group_id.setter
    def security_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ec84604f319a6cd920c524d19b528c42ef098bdfd1f70d4107903a5c1f9ac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7315a9d3e2736d662c6ae59465fbd258b728c22316967a16d9ed290cbde2c93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPwd")
    def user_pwd(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPwd"))

    @user_pwd.setter
    def user_pwd(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b04f079fa1a4ffe4d76c6a7f8dca0c6fb1c910894dae93ea942f5cd947d469c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPwd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585c861ae3a2189ffd39e687ee0c058b970e6c6562d61fd79c97622e5706ceae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1Config",
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
        "network_id": "networkId",
        "node_type": "nodeType",
        "number_of_node": "numberOfNode",
        "security_group_id": "securityGroupId",
        "user_name": "userName",
        "user_pwd": "userPwd",
        "vpc_id": "vpcId",
        "availability_zone": "availabilityZone",
        "endpoints": "endpoints",
        "id": "id",
        "keep_last_manual_snapshot": "keepLastManualSnapshot",
        "number_of_cn": "numberOfCn",
        "port": "port",
        "public_endpoints": "publicEndpoints",
        "public_ip": "publicIp",
        "timeouts": "timeouts",
    },
)
class DwsClusterV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        network_id: builtins.str,
        node_type: builtins.str,
        number_of_node: jsii.Number,
        security_group_id: builtins.str,
        user_name: builtins.str,
        user_pwd: builtins.str,
        vpc_id: builtins.str,
        availability_zone: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DwsClusterV1Endpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        keep_last_manual_snapshot: typing.Optional[jsii.Number] = None,
        number_of_cn: typing.Optional[jsii.Number] = None,
        port: typing.Optional[jsii.Number] = None,
        public_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DwsClusterV1PublicEndpoints", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_ip: typing.Optional[typing.Union["DwsClusterV1PublicIp", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DwsClusterV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#name DwsClusterV1#name}.
        :param network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#network_id DwsClusterV1#network_id}.
        :param node_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#node_type DwsClusterV1#node_type}.
        :param number_of_node: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#number_of_node DwsClusterV1#number_of_node}.
        :param security_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#security_group_id DwsClusterV1#security_group_id}.
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#user_name DwsClusterV1#user_name}.
        :param user_pwd: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#user_pwd DwsClusterV1#user_pwd}.
        :param vpc_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#vpc_id DwsClusterV1#vpc_id}.
        :param availability_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#availability_zone DwsClusterV1#availability_zone}.
        :param endpoints: endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#endpoints DwsClusterV1#endpoints}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#id DwsClusterV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param keep_last_manual_snapshot: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#keep_last_manual_snapshot DwsClusterV1#keep_last_manual_snapshot}.
        :param number_of_cn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#number_of_cn DwsClusterV1#number_of_cn}.
        :param port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#port DwsClusterV1#port}.
        :param public_endpoints: public_endpoints block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_endpoints DwsClusterV1#public_endpoints}
        :param public_ip: public_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_ip DwsClusterV1#public_ip}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#timeouts DwsClusterV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(public_ip, dict):
            public_ip = DwsClusterV1PublicIp(**public_ip)
        if isinstance(timeouts, dict):
            timeouts = DwsClusterV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4740cf0aace40372812615be405267121361c5ac898e26e26003c77a8ebf11c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument number_of_node", value=number_of_node, expected_type=type_hints["number_of_node"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument user_pwd", value=user_pwd, expected_type=type_hints["user_pwd"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument keep_last_manual_snapshot", value=keep_last_manual_snapshot, expected_type=type_hints["keep_last_manual_snapshot"])
            check_type(argname="argument number_of_cn", value=number_of_cn, expected_type=type_hints["number_of_cn"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument public_endpoints", value=public_endpoints, expected_type=type_hints["public_endpoints"])
            check_type(argname="argument public_ip", value=public_ip, expected_type=type_hints["public_ip"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network_id": network_id,
            "node_type": node_type,
            "number_of_node": number_of_node,
            "security_group_id": security_group_id,
            "user_name": user_name,
            "user_pwd": user_pwd,
            "vpc_id": vpc_id,
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
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if endpoints is not None:
            self._values["endpoints"] = endpoints
        if id is not None:
            self._values["id"] = id
        if keep_last_manual_snapshot is not None:
            self._values["keep_last_manual_snapshot"] = keep_last_manual_snapshot
        if number_of_cn is not None:
            self._values["number_of_cn"] = number_of_cn
        if port is not None:
            self._values["port"] = port
        if public_endpoints is not None:
            self._values["public_endpoints"] = public_endpoints
        if public_ip is not None:
            self._values["public_ip"] = public_ip
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#name DwsClusterV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#network_id DwsClusterV1#network_id}.'''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#node_type DwsClusterV1#node_type}.'''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def number_of_node(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#number_of_node DwsClusterV1#number_of_node}.'''
        result = self._values.get("number_of_node")
        assert result is not None, "Required property 'number_of_node' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def security_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#security_group_id DwsClusterV1#security_group_id}.'''
        result = self._values.get("security_group_id")
        assert result is not None, "Required property 'security_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#user_name DwsClusterV1#user_name}.'''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_pwd(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#user_pwd DwsClusterV1#user_pwd}.'''
        result = self._values.get("user_pwd")
        assert result is not None, "Required property 'user_pwd' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#vpc_id DwsClusterV1#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#availability_zone DwsClusterV1#availability_zone}.'''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DwsClusterV1Endpoints"]]]:
        '''endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#endpoints DwsClusterV1#endpoints}
        '''
        result = self._values.get("endpoints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DwsClusterV1Endpoints"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#id DwsClusterV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keep_last_manual_snapshot(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#keep_last_manual_snapshot DwsClusterV1#keep_last_manual_snapshot}.'''
        result = self._values.get("keep_last_manual_snapshot")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def number_of_cn(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#number_of_cn DwsClusterV1#number_of_cn}.'''
        result = self._values.get("number_of_cn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#port DwsClusterV1#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def public_endpoints(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DwsClusterV1PublicEndpoints"]]]:
        '''public_endpoints block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_endpoints DwsClusterV1#public_endpoints}
        '''
        result = self._values.get("public_endpoints")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DwsClusterV1PublicEndpoints"]]], result)

    @builtins.property
    def public_ip(self) -> typing.Optional["DwsClusterV1PublicIp"]:
        '''public_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_ip DwsClusterV1#public_ip}
        '''
        result = self._values.get("public_ip")
        return typing.cast(typing.Optional["DwsClusterV1PublicIp"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DwsClusterV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#timeouts DwsClusterV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DwsClusterV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DwsClusterV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1Endpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class DwsClusterV1Endpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DwsClusterV1Endpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DwsClusterV1EndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1EndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6affa05268879efe0620d9f55b93271ce72e3f66f27e4ff0904bcb97ba88c406)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DwsClusterV1EndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d1c3ba6e1450eadbcc17e2040ff0a22afbddc65c85dbc86e809a8dd25409f4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DwsClusterV1EndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86738e0a68f798910c45e13b66fab09e58bc456e6eec6cb8aa15e046ba49f666)
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
            type_hints = typing.get_type_hints(_typecheckingstub__029848fdb9a275f086d0454d1b43111e7647277f478cc5e83adca4ac78e062a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01ab89f3f2686736bcea31217fce639a4f10b6c671ac403bf3519b1d8d9beb14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DwsClusterV1Endpoints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DwsClusterV1Endpoints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DwsClusterV1Endpoints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7c5aa791d019b48902621ebef5d17a93d66dfb9d3a2ca7fef420f6063e2f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DwsClusterV1EndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1EndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc6733b6bdb33a38e1f4f565a954acab7d938bcaa21405d23bf1ca8370dc1a70)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="connectInfo")
    def connect_info(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectInfo"))

    @builtins.property
    @jsii.member(jsii_name="jdbcUrl")
    def jdbc_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jdbcUrl"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1Endpoints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1Endpoints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1Endpoints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034fa92609e5bfe452fd6e009c1714ece29905c2f554317bc05d7c44db9e5979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1PublicEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class DwsClusterV1PublicEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DwsClusterV1PublicEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DwsClusterV1PublicEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1PublicEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36bb1c838bd66cc50292f0099d84331adb3123dfdd377b2b60e8ed65a87f2cd5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DwsClusterV1PublicEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2024989be41233b20be0b5dc8c65edc409f2362f326b8197a510c3b43a610ab8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DwsClusterV1PublicEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94753aa88d2fd15c9f334769220a451eaf92330ad7195d7937b51708dde731f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__861d1ccbb15501226ab0461e46b101a93ffb360d77bc0b838e1704a3521edcec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18e3641a3dc6cc723e787632f5009f0f724a2183083187c759d1793923d1d8d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DwsClusterV1PublicEndpoints]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DwsClusterV1PublicEndpoints]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DwsClusterV1PublicEndpoints]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c82345ef91a3fee1ab72f2fb53b0f092a1eccebd4d4dd8bb42755e23236388f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DwsClusterV1PublicEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1PublicEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5074207795470263fcd67cd2c1cdd17a1b0cadec4dcef3b45936ee0775a29d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="jdbcUrl")
    def jdbc_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "jdbcUrl"))

    @builtins.property
    @jsii.member(jsii_name="publicConnectInfo")
    def public_connect_info(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicConnectInfo"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1PublicEndpoints]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1PublicEndpoints]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1PublicEndpoints]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e3c06a29ba8b5ba66ab8ea40d5f919c90f271fd1d7e176dadfa58e0da76b07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1PublicIp",
    jsii_struct_bases=[],
    name_mapping={"eip_id": "eipId", "public_bind_type": "publicBindType"},
)
class DwsClusterV1PublicIp:
    def __init__(
        self,
        *,
        eip_id: typing.Optional[builtins.str] = None,
        public_bind_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param eip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#eip_id DwsClusterV1#eip_id}.
        :param public_bind_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_bind_type DwsClusterV1#public_bind_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04be56df1f80731425ad902edccb137b79f912fd04835c04ff5ae88055f19c4)
            check_type(argname="argument eip_id", value=eip_id, expected_type=type_hints["eip_id"])
            check_type(argname="argument public_bind_type", value=public_bind_type, expected_type=type_hints["public_bind_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if eip_id is not None:
            self._values["eip_id"] = eip_id
        if public_bind_type is not None:
            self._values["public_bind_type"] = public_bind_type

    @builtins.property
    def eip_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#eip_id DwsClusterV1#eip_id}.'''
        result = self._values.get("eip_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_bind_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#public_bind_type DwsClusterV1#public_bind_type}.'''
        result = self._values.get("public_bind_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DwsClusterV1PublicIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DwsClusterV1PublicIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1PublicIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__902d731ae077d0f0a1590fe85a07ec09485396ff06f9777d67faba4cacfb7b8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEipId")
    def reset_eip_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEipId", []))

    @jsii.member(jsii_name="resetPublicBindType")
    def reset_public_bind_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicBindType", []))

    @builtins.property
    @jsii.member(jsii_name="eipIdInput")
    def eip_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eipIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicBindTypeInput")
    def public_bind_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicBindTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="eipId")
    def eip_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eipId"))

    @eip_id.setter
    def eip_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d46fc72734dc1db0bd0da174647a3d41fa9099b23976c9b45eeb8f1375b37d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eipId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicBindType")
    def public_bind_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicBindType"))

    @public_bind_type.setter
    def public_bind_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f44033521942c0a1d1eda537fd810e44bfacc871a1d7f8f785c352f3dc4452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicBindType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DwsClusterV1PublicIp]:
        return typing.cast(typing.Optional[DwsClusterV1PublicIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DwsClusterV1PublicIp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769d299118731b848ddb1936c9f31c13d7dff64c358048275ef5c9d80070d0dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DwsClusterV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#create DwsClusterV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#delete DwsClusterV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#update DwsClusterV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9eedfab0d1fe5ef280fce85fa7f1cd420cc498dfd81ce99cefd5dacfd00d8b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#create DwsClusterV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#delete DwsClusterV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/dws_cluster_v1#update DwsClusterV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DwsClusterV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DwsClusterV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dwsClusterV1.DwsClusterV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad60c6ebfeb27f66a791141f276bcdd7382410040d063c5acf9272eacb97106c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5ba77b053ad63df2ecfc9a8b4fd51962db92330c295c81c8ffb400674cb62df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55ef8a88630bb1074828582b949c7eddbf8b642434c7b01dac56763354dad4ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__596fd12d4feed7a18ba42fccad19a588982e7e4d19f49e35d534f69577b18520)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7a3379ae9c52f816ca6be29699b23b271e7c3553879b3acc990207c2ca95d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DwsClusterV1",
    "DwsClusterV1Config",
    "DwsClusterV1Endpoints",
    "DwsClusterV1EndpointsList",
    "DwsClusterV1EndpointsOutputReference",
    "DwsClusterV1PublicEndpoints",
    "DwsClusterV1PublicEndpointsList",
    "DwsClusterV1PublicEndpointsOutputReference",
    "DwsClusterV1PublicIp",
    "DwsClusterV1PublicIpOutputReference",
    "DwsClusterV1Timeouts",
    "DwsClusterV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__87e4ce1c114e265170eb8593c0a40bd2be85708ead9884ecb026632fa95177d1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network_id: builtins.str,
    node_type: builtins.str,
    number_of_node: jsii.Number,
    security_group_id: builtins.str,
    user_name: builtins.str,
    user_pwd: builtins.str,
    vpc_id: builtins.str,
    availability_zone: typing.Optional[builtins.str] = None,
    endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DwsClusterV1Endpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    keep_last_manual_snapshot: typing.Optional[jsii.Number] = None,
    number_of_cn: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    public_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DwsClusterV1PublicEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    public_ip: typing.Optional[typing.Union[DwsClusterV1PublicIp, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DwsClusterV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8a75ddb5efef90c3b799b1ca056fd8461690968f3842fb4aa0810ce4b411f898(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed408688d013f2b103c37d8344779b78e25bad6321676f9767a469f2cbb82da3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DwsClusterV1Endpoints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabf2e16e0699e4f53ad921f4c05b4cffa4d57771bddf561f29f577ee9069fb2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DwsClusterV1PublicEndpoints, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c879407eededcd5731f0ae0f55a0985f7110da7c3913d7f9c5da379767c6c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1041d6c494e0eec17ca9bb1b62dca1b27bba1717a69813acf680ae851a0ccdd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3c84002d27fc22907e62b3bc85bcf362d15266b64989532807f6dd6d498660(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fbf880afe911562e2e1eae8ec7a5645c1194b7e27fdf15df0ba47e722dd894(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__947b7aef88d75ec59a9182d643a24043c6ad28bf14be39b92efa43497a712f51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa27d93205c9c905d8bafee912befb78998d17618519478e384d1c908e992161(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d345c4a3450f5dfcee99276ed7fd99fa0359f1d0981cea7c88aa4f251ea9fdaf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd7bb954f748245c415db4356d1f2d53a4ec50cf401078f8331c986fa658b86(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7e330435c079f472f4bc152dc140658a3a0ade80f44f02c6e8bbdaf200d7fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ec84604f319a6cd920c524d19b528c42ef098bdfd1f70d4107903a5c1f9ac0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7315a9d3e2736d662c6ae59465fbd258b728c22316967a16d9ed290cbde2c93e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b04f079fa1a4ffe4d76c6a7f8dca0c6fb1c910894dae93ea942f5cd947d469c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585c861ae3a2189ffd39e687ee0c058b970e6c6562d61fd79c97622e5706ceae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4740cf0aace40372812615be405267121361c5ac898e26e26003c77a8ebf11c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network_id: builtins.str,
    node_type: builtins.str,
    number_of_node: jsii.Number,
    security_group_id: builtins.str,
    user_name: builtins.str,
    user_pwd: builtins.str,
    vpc_id: builtins.str,
    availability_zone: typing.Optional[builtins.str] = None,
    endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DwsClusterV1Endpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    keep_last_manual_snapshot: typing.Optional[jsii.Number] = None,
    number_of_cn: typing.Optional[jsii.Number] = None,
    port: typing.Optional[jsii.Number] = None,
    public_endpoints: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DwsClusterV1PublicEndpoints, typing.Dict[builtins.str, typing.Any]]]]] = None,
    public_ip: typing.Optional[typing.Union[DwsClusterV1PublicIp, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DwsClusterV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6affa05268879efe0620d9f55b93271ce72e3f66f27e4ff0904bcb97ba88c406(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d1c3ba6e1450eadbcc17e2040ff0a22afbddc65c85dbc86e809a8dd25409f4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86738e0a68f798910c45e13b66fab09e58bc456e6eec6cb8aa15e046ba49f666(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029848fdb9a275f086d0454d1b43111e7647277f478cc5e83adca4ac78e062a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ab89f3f2686736bcea31217fce639a4f10b6c671ac403bf3519b1d8d9beb14(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7c5aa791d019b48902621ebef5d17a93d66dfb9d3a2ca7fef420f6063e2f4c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DwsClusterV1Endpoints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6733b6bdb33a38e1f4f565a954acab7d938bcaa21405d23bf1ca8370dc1a70(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034fa92609e5bfe452fd6e009c1714ece29905c2f554317bc05d7c44db9e5979(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1Endpoints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bb1c838bd66cc50292f0099d84331adb3123dfdd377b2b60e8ed65a87f2cd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2024989be41233b20be0b5dc8c65edc409f2362f326b8197a510c3b43a610ab8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94753aa88d2fd15c9f334769220a451eaf92330ad7195d7937b51708dde731f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861d1ccbb15501226ab0461e46b101a93ffb360d77bc0b838e1704a3521edcec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e3641a3dc6cc723e787632f5009f0f724a2183083187c759d1793923d1d8d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c82345ef91a3fee1ab72f2fb53b0f092a1eccebd4d4dd8bb42755e23236388f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DwsClusterV1PublicEndpoints]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5074207795470263fcd67cd2c1cdd17a1b0cadec4dcef3b45936ee0775a29d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e3c06a29ba8b5ba66ab8ea40d5f919c90f271fd1d7e176dadfa58e0da76b07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1PublicEndpoints]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04be56df1f80731425ad902edccb137b79f912fd04835c04ff5ae88055f19c4(
    *,
    eip_id: typing.Optional[builtins.str] = None,
    public_bind_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902d731ae077d0f0a1590fe85a07ec09485396ff06f9777d67faba4cacfb7b8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46fc72734dc1db0bd0da174647a3d41fa9099b23976c9b45eeb8f1375b37d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f44033521942c0a1d1eda537fd810e44bfacc871a1d7f8f785c352f3dc4452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769d299118731b848ddb1936c9f31c13d7dff64c358048275ef5c9d80070d0dc(
    value: typing.Optional[DwsClusterV1PublicIp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9eedfab0d1fe5ef280fce85fa7f1cd420cc498dfd81ce99cefd5dacfd00d8b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad60c6ebfeb27f66a791141f276bcdd7382410040d063c5acf9272eacb97106c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ba77b053ad63df2ecfc9a8b4fd51962db92330c295c81c8ffb400674cb62df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55ef8a88630bb1074828582b949c7eddbf8b642434c7b01dac56763354dad4ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596fd12d4feed7a18ba42fccad19a588982e7e4d19f49e35d534f69577b18520(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7a3379ae9c52f816ca6be29699b23b271e7c3553879b3acc990207c2ca95d5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DwsClusterV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass

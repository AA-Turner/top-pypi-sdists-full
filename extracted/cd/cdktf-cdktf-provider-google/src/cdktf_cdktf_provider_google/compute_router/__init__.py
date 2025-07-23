r'''
# `google_compute_router`

Refer to the Terraform Registry for docs: [`google_compute_router`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router).
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


class ComputeRouter(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouter",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router google_compute_router}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        network: builtins.str,
        bgp: typing.Optional[typing.Union["ComputeRouterBgp", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encrypted_interconnect_router: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        md5_authentication_keys: typing.Optional[typing.Union["ComputeRouterMd5AuthenticationKeys", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRouterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router google_compute_router} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#name ComputeRouter#name}
        :param network: A reference to the network to which this router belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#network ComputeRouter#network}
        :param bgp: bgp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#bgp ComputeRouter#bgp}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#description ComputeRouter#description}
        :param encrypted_interconnect_router: Indicates if a router is dedicated for use with encrypted VLAN attachments (interconnectAttachments). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#encrypted_interconnect_router ComputeRouter#encrypted_interconnect_router}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#id ComputeRouter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param md5_authentication_keys: md5_authentication_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#md5_authentication_keys ComputeRouter#md5_authentication_keys}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#project ComputeRouter#project}.
        :param region: Region where the router resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#region ComputeRouter#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#timeouts ComputeRouter#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf4828481ca7e6eca4587a2e90c69dcdc1b4f8af5cec8006ea2e1d314bb32de)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ComputeRouterConfig(
            name=name,
            network=network,
            bgp=bgp,
            description=description,
            encrypted_interconnect_router=encrypted_interconnect_router,
            id=id,
            md5_authentication_keys=md5_authentication_keys,
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
        '''Generates CDKTF code for importing a ComputeRouter resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ComputeRouter to import.
        :param import_from_id: The id of the existing ComputeRouter that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ComputeRouter to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72fbb73568a789e30b61638089bba94f364efb27d5689e8ecabc9637c91fabe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putBgp")
    def put_bgp(
        self,
        *,
        asn: jsii.Number,
        advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterBgpAdvertisedIpRanges", typing.Dict[builtins.str, typing.Any]]]]] = None,
        advertise_mode: typing.Optional[builtins.str] = None,
        identifier_range: typing.Optional[builtins.str] = None,
        keepalive_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param asn: Local BGP Autonomous System Number (ASN). Must be an RFC6996 private ASN, either 16-bit or 32-bit. The value will be fixed for this router resource. All VPN tunnels that link to this router will have the same local ASN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#asn ComputeRouter#asn}
        :param advertised_groups: User-specified list of prefix groups to advertise in custom mode. This field can only be populated if advertiseMode is CUSTOM and is advertised to all peers of the router. These groups will be advertised in addition to any specified prefixes. Leave this field blank to advertise no custom groups. This enum field has the one valid value: ALL_SUBNETS Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertised_groups ComputeRouter#advertised_groups}
        :param advertised_ip_ranges: advertised_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertised_ip_ranges ComputeRouter#advertised_ip_ranges}
        :param advertise_mode: User-specified flag to indicate which mode to use for advertisement. Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertise_mode ComputeRouter#advertise_mode}
        :param identifier_range: Explicitly specifies a range of valid BGP Identifiers for this Router. It is provided as a link-local IPv4 range (from 169.254.0.0/16), of size at least /30, even if the BGP sessions are over IPv6. It must not overlap with any IPv4 BGP session ranges. Other vendors commonly call this router ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#identifier_range ComputeRouter#identifier_range}
        :param keepalive_interval: The interval in seconds between BGP keepalive messages that are sent to the peer. Hold time is three times the interval at which keepalive messages are sent, and the hold time is the maximum number of seconds allowed to elapse between successive keepalive messages that BGP receives from a peer. BGP will use the smaller of either the local hold time value or the peer's hold time value as the hold time for the BGP connection between the two peers. If set, this value must be between 20 and 60. The default is 20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#keepalive_interval ComputeRouter#keepalive_interval}
        '''
        value = ComputeRouterBgp(
            asn=asn,
            advertised_groups=advertised_groups,
            advertised_ip_ranges=advertised_ip_ranges,
            advertise_mode=advertise_mode,
            identifier_range=identifier_range,
            keepalive_interval=keepalive_interval,
        )

        return typing.cast(None, jsii.invoke(self, "putBgp", [value]))

    @jsii.member(jsii_name="putMd5AuthenticationKeys")
    def put_md5_authentication_keys(
        self,
        *,
        key: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param key: Value of the key used for MD5 authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#key ComputeRouter#key}
        :param name: Name used to identify the key. Must be unique within a router. Must be referenced by exactly one bgpPeer. Must comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#name ComputeRouter#name}
        '''
        value = ComputeRouterMd5AuthenticationKeys(key=key, name=name)

        return typing.cast(None, jsii.invoke(self, "putMd5AuthenticationKeys", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#create ComputeRouter#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#delete ComputeRouter#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#update ComputeRouter#update}.
        '''
        value = ComputeRouterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetBgp")
    def reset_bgp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgp", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryptedInterconnectRouter")
    def reset_encrypted_interconnect_router(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptedInterconnectRouter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMd5AuthenticationKeys")
    def reset_md5_authentication_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMd5AuthenticationKeys", []))

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
    @jsii.member(jsii_name="bgp")
    def bgp(self) -> "ComputeRouterBgpOutputReference":
        return typing.cast("ComputeRouterBgpOutputReference", jsii.get(self, "bgp"))

    @builtins.property
    @jsii.member(jsii_name="creationTimestamp")
    def creation_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="md5AuthenticationKeys")
    def md5_authentication_keys(
        self,
    ) -> "ComputeRouterMd5AuthenticationKeysOutputReference":
        return typing.cast("ComputeRouterMd5AuthenticationKeysOutputReference", jsii.get(self, "md5AuthenticationKeys"))

    @builtins.property
    @jsii.member(jsii_name="selfLink")
    def self_link(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "selfLink"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ComputeRouterTimeoutsOutputReference":
        return typing.cast("ComputeRouterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="bgpInput")
    def bgp_input(self) -> typing.Optional["ComputeRouterBgp"]:
        return typing.cast(typing.Optional["ComputeRouterBgp"], jsii.get(self, "bgpInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptedInterconnectRouterInput")
    def encrypted_interconnect_router_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "encryptedInterconnectRouterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="md5AuthenticationKeysInput")
    def md5_authentication_keys_input(
        self,
    ) -> typing.Optional["ComputeRouterMd5AuthenticationKeys"]:
        return typing.cast(typing.Optional["ComputeRouterMd5AuthenticationKeys"], jsii.get(self, "md5AuthenticationKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRouterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ComputeRouterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede0303f8fba54fdb16bc244d46f150408ea8515dfb6c40d1b0311578bf5a176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptedInterconnectRouter")
    def encrypted_interconnect_router(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "encryptedInterconnectRouter"))

    @encrypted_interconnect_router.setter
    def encrypted_interconnect_router(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6f5aa50aef69947b05cd7685f3288a99076fe0cb275eddb954a61c3e9755f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptedInterconnectRouter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43beb847c62a975b66f89323f64329eef85833b2e2d57e0cf0900657419659b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c7fdf133db017b2465dc658764da77c9642e99b5eb8d70fa97324a46964cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "network"))

    @network.setter
    def network(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f1b92f0975ac618b242bc8ed2516afa36f0527e867d17d1e72dc44ab68ca7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "network", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__455340ceb18062141504f1fae663f57c733acd9b08b28d049d8f620474c451a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f42b4fdb3287dd2c62ed2ac28b7830bd3d98b1850a7dea183d95a440231a8ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterBgp",
    jsii_struct_bases=[],
    name_mapping={
        "asn": "asn",
        "advertised_groups": "advertisedGroups",
        "advertised_ip_ranges": "advertisedIpRanges",
        "advertise_mode": "advertiseMode",
        "identifier_range": "identifierRange",
        "keepalive_interval": "keepaliveInterval",
    },
)
class ComputeRouterBgp:
    def __init__(
        self,
        *,
        asn: jsii.Number,
        advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ComputeRouterBgpAdvertisedIpRanges", typing.Dict[builtins.str, typing.Any]]]]] = None,
        advertise_mode: typing.Optional[builtins.str] = None,
        identifier_range: typing.Optional[builtins.str] = None,
        keepalive_interval: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param asn: Local BGP Autonomous System Number (ASN). Must be an RFC6996 private ASN, either 16-bit or 32-bit. The value will be fixed for this router resource. All VPN tunnels that link to this router will have the same local ASN. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#asn ComputeRouter#asn}
        :param advertised_groups: User-specified list of prefix groups to advertise in custom mode. This field can only be populated if advertiseMode is CUSTOM and is advertised to all peers of the router. These groups will be advertised in addition to any specified prefixes. Leave this field blank to advertise no custom groups. This enum field has the one valid value: ALL_SUBNETS Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertised_groups ComputeRouter#advertised_groups}
        :param advertised_ip_ranges: advertised_ip_ranges block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertised_ip_ranges ComputeRouter#advertised_ip_ranges}
        :param advertise_mode: User-specified flag to indicate which mode to use for advertisement. Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertise_mode ComputeRouter#advertise_mode}
        :param identifier_range: Explicitly specifies a range of valid BGP Identifiers for this Router. It is provided as a link-local IPv4 range (from 169.254.0.0/16), of size at least /30, even if the BGP sessions are over IPv6. It must not overlap with any IPv4 BGP session ranges. Other vendors commonly call this router ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#identifier_range ComputeRouter#identifier_range}
        :param keepalive_interval: The interval in seconds between BGP keepalive messages that are sent to the peer. Hold time is three times the interval at which keepalive messages are sent, and the hold time is the maximum number of seconds allowed to elapse between successive keepalive messages that BGP receives from a peer. BGP will use the smaller of either the local hold time value or the peer's hold time value as the hold time for the BGP connection between the two peers. If set, this value must be between 20 and 60. The default is 20. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#keepalive_interval ComputeRouter#keepalive_interval}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f335ce4e51f2e950e883a254574ed50d6678bda6a596f88df3eaea2c66583f75)
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument advertised_groups", value=advertised_groups, expected_type=type_hints["advertised_groups"])
            check_type(argname="argument advertised_ip_ranges", value=advertised_ip_ranges, expected_type=type_hints["advertised_ip_ranges"])
            check_type(argname="argument advertise_mode", value=advertise_mode, expected_type=type_hints["advertise_mode"])
            check_type(argname="argument identifier_range", value=identifier_range, expected_type=type_hints["identifier_range"])
            check_type(argname="argument keepalive_interval", value=keepalive_interval, expected_type=type_hints["keepalive_interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asn": asn,
        }
        if advertised_groups is not None:
            self._values["advertised_groups"] = advertised_groups
        if advertised_ip_ranges is not None:
            self._values["advertised_ip_ranges"] = advertised_ip_ranges
        if advertise_mode is not None:
            self._values["advertise_mode"] = advertise_mode
        if identifier_range is not None:
            self._values["identifier_range"] = identifier_range
        if keepalive_interval is not None:
            self._values["keepalive_interval"] = keepalive_interval

    @builtins.property
    def asn(self) -> jsii.Number:
        '''Local BGP Autonomous System Number (ASN).

        Must be an RFC6996
        private ASN, either 16-bit or 32-bit. The value will be fixed for
        this router resource. All VPN tunnels that link to this router
        will have the same local ASN.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#asn ComputeRouter#asn}
        '''
        result = self._values.get("asn")
        assert result is not None, "Required property 'asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def advertised_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''User-specified list of prefix groups to advertise in custom mode.

        This field can only be populated if advertiseMode is CUSTOM and
        is advertised to all peers of the router. These groups will be
        advertised in addition to any specified prefixes. Leave this field
        blank to advertise no custom groups.

        This enum field has the one valid value: ALL_SUBNETS

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertised_groups ComputeRouter#advertised_groups}
        '''
        result = self._values.get("advertised_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def advertised_ip_ranges(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterBgpAdvertisedIpRanges"]]]:
        '''advertised_ip_ranges block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertised_ip_ranges ComputeRouter#advertised_ip_ranges}
        '''
        result = self._values.get("advertised_ip_ranges")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ComputeRouterBgpAdvertisedIpRanges"]]], result)

    @builtins.property
    def advertise_mode(self) -> typing.Optional[builtins.str]:
        '''User-specified flag to indicate which mode to use for advertisement. Default value: "DEFAULT" Possible values: ["DEFAULT", "CUSTOM"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#advertise_mode ComputeRouter#advertise_mode}
        '''
        result = self._values.get("advertise_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identifier_range(self) -> typing.Optional[builtins.str]:
        '''Explicitly specifies a range of valid BGP Identifiers for this Router.

        It is provided as a link-local IPv4 range (from 169.254.0.0/16), of
        size at least /30, even if the BGP sessions are over IPv6. It must
        not overlap with any IPv4 BGP session ranges. Other vendors commonly
        call this router ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#identifier_range ComputeRouter#identifier_range}
        '''
        result = self._values.get("identifier_range")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def keepalive_interval(self) -> typing.Optional[jsii.Number]:
        '''The interval in seconds between BGP keepalive messages that are sent to the peer.

        Hold time is three times the interval at which keepalive
        messages are sent, and the hold time is the maximum number of seconds
        allowed to elapse between successive keepalive messages that BGP
        receives from a peer.

        BGP will use the smaller of either the local hold time value or the
        peer's hold time value as the hold time for the BGP connection
        between the two peers. If set, this value must be between 20 and 60.
        The default is 20.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#keepalive_interval ComputeRouter#keepalive_interval}
        '''
        result = self._values.get("keepalive_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterBgp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterBgpAdvertisedIpRanges",
    jsii_struct_bases=[],
    name_mapping={"range": "range", "description": "description"},
)
class ComputeRouterBgpAdvertisedIpRanges:
    def __init__(
        self,
        *,
        range: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param range: The IP range to advertise. The value must be a CIDR-formatted string. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#range ComputeRouter#range}
        :param description: User-specified description for the IP range. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#description ComputeRouter#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc070e1ba50768fc78167c213f144641665d8b6e13bcc8296bd923418b67ead4)
            check_type(argname="argument range", value=range, expected_type=type_hints["range"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "range": range,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def range(self) -> builtins.str:
        '''The IP range to advertise. The value must be a CIDR-formatted string.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#range ComputeRouter#range}
        '''
        result = self._values.get("range")
        assert result is not None, "Required property 'range' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''User-specified description for the IP range.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#description ComputeRouter#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterBgpAdvertisedIpRanges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterBgpAdvertisedIpRangesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterBgpAdvertisedIpRangesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2514479606f08f3a3d177e1c9cc2e7c8827b224e0d4ac65022de24d0e19a788)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ComputeRouterBgpAdvertisedIpRangesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce99e41bea32510742c93ac91ea63587aa15357ff663a22d34f98bfe36664c40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ComputeRouterBgpAdvertisedIpRangesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034794c2eacddc185292530bc6ebc0b50f1c70ac48750e29a6cfda922934dba1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d08fca98c1aa413464221a76bdcf266d29d77a1236090a5a807b2e17078e697)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77477d43cf383c84742f5becff5b910c2c69ebc77db75a52cec3c909a7a1cb89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterBgpAdvertisedIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterBgpAdvertisedIpRanges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterBgpAdvertisedIpRanges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e361bc96e3a2f649d50551bb0113cba3db3106b8fc2e6151658544403863838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouterBgpAdvertisedIpRangesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterBgpAdvertisedIpRangesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25faa8b9d712c1071711e1d519e6e582538305b01a2ca5c2a1778e50ae4af723)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="rangeInput")
    def range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rangeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc38822983d9c2df23ce4c0499ce00f04d6103ddcb190338454c523bcd18ab61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="range")
    def range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "range"))

    @range.setter
    def range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc55fadf1684502ff2a4294ed93b9604cca3ca890560fae6ad0362359454f3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "range", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterBgpAdvertisedIpRanges]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterBgpAdvertisedIpRanges]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterBgpAdvertisedIpRanges]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d8279fcffb280c61b52fac10aa7a7bdeb530520b9b712edd43a70755e44807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ComputeRouterBgpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterBgpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00541389c2ecded916d09d6df8ec9ff60c6a21f992b05cc566250d57c5ee7637)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAdvertisedIpRanges")
    def put_advertised_ip_ranges(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterBgpAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a4e31a05371c160422319e81e4a010db487a726a4d4c098e2738f0b68ad406)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdvertisedIpRanges", [value]))

    @jsii.member(jsii_name="resetAdvertisedGroups")
    def reset_advertised_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedGroups", []))

    @jsii.member(jsii_name="resetAdvertisedIpRanges")
    def reset_advertised_ip_ranges(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertisedIpRanges", []))

    @jsii.member(jsii_name="resetAdvertiseMode")
    def reset_advertise_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvertiseMode", []))

    @jsii.member(jsii_name="resetIdentifierRange")
    def reset_identifier_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifierRange", []))

    @jsii.member(jsii_name="resetKeepaliveInterval")
    def reset_keepalive_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepaliveInterval", []))

    @builtins.property
    @jsii.member(jsii_name="advertisedIpRanges")
    def advertised_ip_ranges(self) -> ComputeRouterBgpAdvertisedIpRangesList:
        return typing.cast(ComputeRouterBgpAdvertisedIpRangesList, jsii.get(self, "advertisedIpRanges"))

    @builtins.property
    @jsii.member(jsii_name="advertisedGroupsInput")
    def advertised_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "advertisedGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedIpRangesInput")
    def advertised_ip_ranges_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterBgpAdvertisedIpRanges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterBgpAdvertisedIpRanges]]], jsii.get(self, "advertisedIpRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="advertiseModeInput")
    def advertise_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "advertiseModeInput"))

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="identifierRangeInput")
    def identifier_range_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="keepaliveIntervalInput")
    def keepalive_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepaliveIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="advertisedGroups")
    def advertised_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "advertisedGroups"))

    @advertised_groups.setter
    def advertised_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dad592d87f77892ab3a107fc22fbe610112e3e414d3c4ce720a8fd197c9bd04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertisedGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="advertiseMode")
    def advertise_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "advertiseMode"))

    @advertise_mode.setter
    def advertise_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9576a1d5ec78e6f0f6a7bec6d8c533f23a083329495ed44a99ab71e0a76d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "advertiseMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4671c15aa0fdd2502938da30d75bdba4c4c087b9a09a620e992022c04c0271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="identifierRange")
    def identifier_range(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifierRange"))

    @identifier_range.setter
    def identifier_range(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0627c2f6d6e694e3ff146e4480ece994509fe8af6435614fcdde72d02fc9d4c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identifierRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepaliveInterval")
    def keepalive_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepaliveInterval"))

    @keepalive_interval.setter
    def keepalive_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eeaa837e6b6d49b8027d404c470a116da0e6732d3da39503fff11711a8e3886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepaliveInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouterBgp]:
        return typing.cast(typing.Optional[ComputeRouterBgp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ComputeRouterBgp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f808eb06ebe3b668a27a03ac466a8a0e55f5095f77607a5a477dbb12919fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterConfig",
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
        "network": "network",
        "bgp": "bgp",
        "description": "description",
        "encrypted_interconnect_router": "encryptedInterconnectRouter",
        "id": "id",
        "md5_authentication_keys": "md5AuthenticationKeys",
        "project": "project",
        "region": "region",
        "timeouts": "timeouts",
    },
)
class ComputeRouterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        network: builtins.str,
        bgp: typing.Optional[typing.Union[ComputeRouterBgp, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        encrypted_interconnect_router: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        md5_authentication_keys: typing.Optional[typing.Union["ComputeRouterMd5AuthenticationKeys", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["ComputeRouterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the resource. The name must be 1-63 characters long, and comply with RFC1035. Specifically, the name must be 1-63 characters long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?' which means the first character must be a lowercase letter, and all following characters must be a dash, lowercase letter, or digit, except the last character, which cannot be a dash. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#name ComputeRouter#name}
        :param network: A reference to the network to which this router belongs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#network ComputeRouter#network}
        :param bgp: bgp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#bgp ComputeRouter#bgp}
        :param description: An optional description of this resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#description ComputeRouter#description}
        :param encrypted_interconnect_router: Indicates if a router is dedicated for use with encrypted VLAN attachments (interconnectAttachments). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#encrypted_interconnect_router ComputeRouter#encrypted_interconnect_router}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#id ComputeRouter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param md5_authentication_keys: md5_authentication_keys block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#md5_authentication_keys ComputeRouter#md5_authentication_keys}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#project ComputeRouter#project}.
        :param region: Region where the router resides. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#region ComputeRouter#region}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#timeouts ComputeRouter#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(bgp, dict):
            bgp = ComputeRouterBgp(**bgp)
        if isinstance(md5_authentication_keys, dict):
            md5_authentication_keys = ComputeRouterMd5AuthenticationKeys(**md5_authentication_keys)
        if isinstance(timeouts, dict):
            timeouts = ComputeRouterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a53db5df32059c8fe836c99dfab1afcdede56005908f9f0dbc20671b483bfbf9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument bgp", value=bgp, expected_type=type_hints["bgp"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encrypted_interconnect_router", value=encrypted_interconnect_router, expected_type=type_hints["encrypted_interconnect_router"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument md5_authentication_keys", value=md5_authentication_keys, expected_type=type_hints["md5_authentication_keys"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "network": network,
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
        if bgp is not None:
            self._values["bgp"] = bgp
        if description is not None:
            self._values["description"] = description
        if encrypted_interconnect_router is not None:
            self._values["encrypted_interconnect_router"] = encrypted_interconnect_router
        if id is not None:
            self._values["id"] = id
        if md5_authentication_keys is not None:
            self._values["md5_authentication_keys"] = md5_authentication_keys
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
        '''Name of the resource.

        The name must be 1-63 characters long, and
        comply with RFC1035. Specifically, the name must be 1-63 characters
        long and match the regular expression '`a-z <%5B-a-z0-9%5D*%5Ba-z0-9%5D>`_?'
        which means the first character must be a lowercase letter, and all
        following characters must be a dash, lowercase letter, or digit,
        except the last character, which cannot be a dash.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#name ComputeRouter#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def network(self) -> builtins.str:
        '''A reference to the network to which this router belongs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#network ComputeRouter#network}
        '''
        result = self._values.get("network")
        assert result is not None, "Required property 'network' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bgp(self) -> typing.Optional[ComputeRouterBgp]:
        '''bgp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#bgp ComputeRouter#bgp}
        '''
        result = self._values.get("bgp")
        return typing.cast(typing.Optional[ComputeRouterBgp], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of this resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#description ComputeRouter#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encrypted_interconnect_router(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if a router is dedicated for use with encrypted VLAN attachments (interconnectAttachments).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#encrypted_interconnect_router ComputeRouter#encrypted_interconnect_router}
        '''
        result = self._values.get("encrypted_interconnect_router")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#id ComputeRouter#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def md5_authentication_keys(
        self,
    ) -> typing.Optional["ComputeRouterMd5AuthenticationKeys"]:
        '''md5_authentication_keys block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#md5_authentication_keys ComputeRouter#md5_authentication_keys}
        '''
        result = self._values.get("md5_authentication_keys")
        return typing.cast(typing.Optional["ComputeRouterMd5AuthenticationKeys"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#project ComputeRouter#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where the router resides.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#region ComputeRouter#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ComputeRouterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#timeouts ComputeRouter#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ComputeRouterTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterMd5AuthenticationKeys",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "name": "name"},
)
class ComputeRouterMd5AuthenticationKeys:
    def __init__(self, *, key: builtins.str, name: builtins.str) -> None:
        '''
        :param key: Value of the key used for MD5 authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#key ComputeRouter#key}
        :param name: Name used to identify the key. Must be unique within a router. Must be referenced by exactly one bgpPeer. Must comply with RFC1035. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#name ComputeRouter#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348e4516c4a9048977c62ae9a38bb9148b1979ede79116154990af8441b9cf39)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "name": name,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Value of the key used for MD5 authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#key ComputeRouter#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name used to identify the key.

        Must be unique within a router.
        Must be referenced by exactly one bgpPeer. Must comply with RFC1035.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#name ComputeRouter#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterMd5AuthenticationKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterMd5AuthenticationKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterMd5AuthenticationKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__941c163b0584249a8dea4b9b312cc4590fea30b819d8f6f46a537200c5e8c2a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2c43752278a017d065256d6c60759b49094737350b2baf761fe06a6d77de88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a026087503d5c88c14970fa6ea4b0de2d14b8dd89cdfdff87785f2da562d2804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ComputeRouterMd5AuthenticationKeys]:
        return typing.cast(typing.Optional[ComputeRouterMd5AuthenticationKeys], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ComputeRouterMd5AuthenticationKeys],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f842a2ec17c3a1862f3290d507d9944950372d2fc2d91647147d018758b29f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class ComputeRouterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#create ComputeRouter#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#delete ComputeRouter#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#update ComputeRouter#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5f68724bc416767426858438b59db5d49cd466b1e70537f9b53106fd88340f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#create ComputeRouter#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#delete ComputeRouter#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/compute_router#update ComputeRouter#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeRouterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComputeRouterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.computeRouter.ComputeRouterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__40216192e9460a9a34dba38a84a4e069cdf5f731641e640080a496a04c7776ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c2ba1eb0bfdb064ea45b4f0362f1f0837710cadc4d168cd2eb56f546fb92378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0153ecfd74d6b73b091174a40efd576f6598a07acaef4b1c325cb004948b9cee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1c49a0c5cfb0cc59b38df9d1263ed545d57c863bbd74624a5006bb59a03faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d29a6e97764af78ccb8b3d7ac5ac3c8714aea282bed4109f9e11707327dfaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ComputeRouter",
    "ComputeRouterBgp",
    "ComputeRouterBgpAdvertisedIpRanges",
    "ComputeRouterBgpAdvertisedIpRangesList",
    "ComputeRouterBgpAdvertisedIpRangesOutputReference",
    "ComputeRouterBgpOutputReference",
    "ComputeRouterConfig",
    "ComputeRouterMd5AuthenticationKeys",
    "ComputeRouterMd5AuthenticationKeysOutputReference",
    "ComputeRouterTimeouts",
    "ComputeRouterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__caf4828481ca7e6eca4587a2e90c69dcdc1b4f8af5cec8006ea2e1d314bb32de(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    network: builtins.str,
    bgp: typing.Optional[typing.Union[ComputeRouterBgp, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encrypted_interconnect_router: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    md5_authentication_keys: typing.Optional[typing.Union[ComputeRouterMd5AuthenticationKeys, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRouterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e72fbb73568a789e30b61638089bba94f364efb27d5689e8ecabc9637c91fabe(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede0303f8fba54fdb16bc244d46f150408ea8515dfb6c40d1b0311578bf5a176(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6f5aa50aef69947b05cd7685f3288a99076fe0cb275eddb954a61c3e9755f8d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43beb847c62a975b66f89323f64329eef85833b2e2d57e0cf0900657419659b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c7fdf133db017b2465dc658764da77c9642e99b5eb8d70fa97324a46964cd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f1b92f0975ac618b242bc8ed2516afa36f0527e867d17d1e72dc44ab68ca7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__455340ceb18062141504f1fae663f57c733acd9b08b28d049d8f620474c451a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f42b4fdb3287dd2c62ed2ac28b7830bd3d98b1850a7dea183d95a440231a8ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f335ce4e51f2e950e883a254574ed50d6678bda6a596f88df3eaea2c66583f75(
    *,
    asn: jsii.Number,
    advertised_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    advertised_ip_ranges: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterBgpAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]]] = None,
    advertise_mode: typing.Optional[builtins.str] = None,
    identifier_range: typing.Optional[builtins.str] = None,
    keepalive_interval: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc070e1ba50768fc78167c213f144641665d8b6e13bcc8296bd923418b67ead4(
    *,
    range: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2514479606f08f3a3d177e1c9cc2e7c8827b224e0d4ac65022de24d0e19a788(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce99e41bea32510742c93ac91ea63587aa15357ff663a22d34f98bfe36664c40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034794c2eacddc185292530bc6ebc0b50f1c70ac48750e29a6cfda922934dba1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d08fca98c1aa413464221a76bdcf266d29d77a1236090a5a807b2e17078e697(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77477d43cf383c84742f5becff5b910c2c69ebc77db75a52cec3c909a7a1cb89(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e361bc96e3a2f649d50551bb0113cba3db3106b8fc2e6151658544403863838(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ComputeRouterBgpAdvertisedIpRanges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25faa8b9d712c1071711e1d519e6e582538305b01a2ca5c2a1778e50ae4af723(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc38822983d9c2df23ce4c0499ce00f04d6103ddcb190338454c523bcd18ab61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc55fadf1684502ff2a4294ed93b9604cca3ca890560fae6ad0362359454f3d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d8279fcffb280c61b52fac10aa7a7bdeb530520b9b712edd43a70755e44807(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterBgpAdvertisedIpRanges]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00541389c2ecded916d09d6df8ec9ff60c6a21f992b05cc566250d57c5ee7637(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a4e31a05371c160422319e81e4a010db487a726a4d4c098e2738f0b68ad406(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ComputeRouterBgpAdvertisedIpRanges, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dad592d87f77892ab3a107fc22fbe610112e3e414d3c4ce720a8fd197c9bd04(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9576a1d5ec78e6f0f6a7bec6d8c533f23a083329495ed44a99ab71e0a76d74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4671c15aa0fdd2502938da30d75bdba4c4c087b9a09a620e992022c04c0271(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0627c2f6d6e694e3ff146e4480ece994509fe8af6435614fcdde72d02fc9d4c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eeaa837e6b6d49b8027d404c470a116da0e6732d3da39503fff11711a8e3886(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f808eb06ebe3b668a27a03ac466a8a0e55f5095f77607a5a477dbb12919fef(
    value: typing.Optional[ComputeRouterBgp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a53db5df32059c8fe836c99dfab1afcdede56005908f9f0dbc20671b483bfbf9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    network: builtins.str,
    bgp: typing.Optional[typing.Union[ComputeRouterBgp, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    encrypted_interconnect_router: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    md5_authentication_keys: typing.Optional[typing.Union[ComputeRouterMd5AuthenticationKeys, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[ComputeRouterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348e4516c4a9048977c62ae9a38bb9148b1979ede79116154990af8441b9cf39(
    *,
    key: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941c163b0584249a8dea4b9b312cc4590fea30b819d8f6f46a537200c5e8c2a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2c43752278a017d065256d6c60759b49094737350b2baf761fe06a6d77de88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a026087503d5c88c14970fa6ea4b0de2d14b8dd89cdfdff87785f2da562d2804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f842a2ec17c3a1862f3290d507d9944950372d2fc2d91647147d018758b29f(
    value: typing.Optional[ComputeRouterMd5AuthenticationKeys],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5f68724bc416767426858438b59db5d49cd466b1e70537f9b53106fd88340f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40216192e9460a9a34dba38a84a4e069cdf5f731641e640080a496a04c7776ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2ba1eb0bfdb064ea45b4f0362f1f0837710cadc4d168cd2eb56f546fb92378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0153ecfd74d6b73b091174a40efd576f6598a07acaef4b1c325cb004948b9cee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1c49a0c5cfb0cc59b38df9d1263ed545d57c863bbd74624a5006bb59a03faf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d29a6e97764af78ccb8b3d7ac5ac3c8714aea282bed4109f9e11707327dfaf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ComputeRouterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
